#######################################
from bsp import board
from zdm import zdm
# Zerynth
import gc
import mcu
import time
import json
import queue
import serial
import timers
import watchdog
import threading as th
from tslog import tslog
########################################
from networking import wifi, wifisniff, socket
########################################
import utils.config as cfg
from crypto import element


board.init()
board.summary()
print('Board initialized!')

# Open the log and provide a record format
# This accumulates results if the connection goes down
tlog = tslog.TSLog(cfg.LOG_PATH,
                    record_size=cfg.RECORD_SIZE,
                    serializer=json,
                    commit_delta=cfg.DELTA_COMMIT
                    )
# lets get a reader from the tslog
treader = tlog.reader(0)
print("TSLog initialized!")

try:
    print("Connecting to WiFi...")
    if cfg.WIFI_NAME != "MIT" and cfg.WIFI_NAME != "MIT GUEST":
        wifi.configure(cfg.WIFI_NAME, cfg.WIFI_PWORD)
    else:
        wifi.configure(cfg.WIFI_NAME, '')   # set the password to '' for MIT
    wifi.start()
    print("...connected!", wifi.info())

    wifisniff.configure(max_packets=1000)

    print("Connecting to ZDM...")
    device = zdm.Agent(host="zmqtt.zdm.zerynth.com")
    device.start()
    print("ZDM: ", device.firmware())
    print("...Agent started!")
except Exception as e:
    print("Error in initializations: ", e)

while True:
    try:
        ts = time.now()
        if ts % (cfg.SCAN_TIME // 1000) == 0:   # ts is in seconds
            print("Scanning...")
            # start scanning for SCAN_TIME milliseconds
            #wifisniff.configure()
            wifisniff.start()
            scan_res = wifisniff.sniff(n=-1, hex=True, wait=cfg.SCAN_TIME)
            wifisniff.stop()
            print("...scanning done!")
            print("Devices found: ", len(scan_res))

            cfg.PUB_DICT['ts'] = ts
            cfg.PUB_DICT['n_devices'] = len(scan_res)
            cfg.PUB_DICT['sum_rssi'] = sum([x[11] for x in scan_res])       # 11 is the index of the RSSI in the scans (look at utils/config.py)
            # we can compute other statistics here, or we can just publish and compute them after download the data

            # hash the MAC addresses and publish the results
            for i, scan in enumerate(scan_res):
                for j, entry in enumerate(scan):
                    if 'addr' in cfg.SCAN_OUTPUTS[j] and entry != 'FF:FF:FF:FF:FF:FF':
                        scan_res[i][j] = element.sha256(entry)

            cfg.PUB_DICT['scans'] = scan_res

            # publish the results
            try: 
                print("Publishing...")
                #print(cfg.PUB_DICT)
                device.publish(cfg.PUB_DICT, "data")
                print("...published!")
                cfg.PUB_DICT = {}

            except Exception as e:
                # save results to the log
                print("Publish on ZDM Error: ", e)
                try:
                    seqn = tlog.store_object(cfg.PUB_DICT)
                    print("<=", cfg.PUB_DICT)
                except Exception as e:
                    print("Store error: ", e)

    except Exception as e:
        print(e)