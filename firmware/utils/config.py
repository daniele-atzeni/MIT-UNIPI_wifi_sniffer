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
#WIFI_PASSWORD = 'seneshot'
### AP Mick
#WIFI_NAME = "NETGEAR62"
#WIFI_PASSWORD = "helpfulzoo125"
# MIT
WIFI_NAME = "MIT"
WIFI_PASSWORD = ''

SCAN_TIME = 5 * 1000
MAX_PACKETS = 1000

RELEVANT_FIELDS = (4, 5, 6, 8, 11, 12, 13)

#====================== Publish settings
PUB_DICT = {}