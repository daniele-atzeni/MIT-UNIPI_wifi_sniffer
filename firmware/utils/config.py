#====================== TSLog config
# LOG path
LOG_PATH = "/zerynth/log"
# TSLOG Record Size
RECORD_SIZE = 2048 #512
# TSLOG COMMIT
DELTA_COMMIT = 1

#====================== WiFi settings
### Hotspot
#WIFI_NAME = 'Senes_cell'
#WIFI_PWORD = 'seneshot'
### AP Mick
#WIFI_NAME = "NETGEAR62"
#WIFI_PASSWORD = "helpfulzoo125"
# MIT
WIFI_NAME = "MIT"

SCAN_TIME = 5 * 1000

#====================== Scan outputs
SCAN_OUTPUTS = ['type',
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
            'payload']

#====================== Publish settings
PUB_DICT = {}