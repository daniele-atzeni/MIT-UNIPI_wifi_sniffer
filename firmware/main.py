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

'''
SCAN FIELDS:
'type',
'subtype',
'to_ds',
'from_ds',
'flags',
'duration_id',
'sequence_ctrl',
'addr1',
'addr2',
'addr3',
'addr4',
'rssi',
'channel',
'payload_size',
'payload'
'''


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
    wifi.configure(cfg.WIFI_NAME, cfg.WIFI_PASSWORD)
    wifi.start()
    print("...connected!", wifi.info())

    # the only subtypes of frames are beacon and probe requests
    # we are not interested in beacon frames (code 5), but only in probe requests (code 4)
    wifisniff.configure(max_packets=cfg.MAX_PACKETS, mgmt_subtypes=(4,))

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

            cfg.PUB_DICT['n_devices'] = len(scan_res)
            cfg.PUB_DICT['sum_rssi'] = sum([x[11] for x in scan_res])       # 11 is the index of the RSSI in the scans (look at utils/config.py)

            # we can avoid saving a lot of fields. 
            # we are just going to save flags, duration_id, sequence_ctr, source_mac_addr, RSSI, channel, payload_size
            # indices relative to these fields are saved in cfg.RELEVANT_FIELDS
            for i, scan in enumerate(scan_res):
                scan_res[i] = [scan[j] for j in cfg.RELEVANT_FIELDS]
            # hashing the MAC address
            # scan_res[3] = element.sha256(scan_res[3])

            cfg.PUB_DICT['ts'] = ts
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