# MIT-UNIPI_wifi_sniffer

Documentation about the sniffer:
https://docs.zerynth.com/latest/reference/libs/networking/wifisniff/
In this web page there is also the explanation about the meaning of the
data produced by the sniffer


To download the data:
https://cloud.zerynth.com/wks-6sdnjgqfpv98/exports
- create a new export with a (not important) name,
- set the start datetime (greater than 2022/06/13 00:00) and an end datetime
- wait a moment, refresh the page and click the down arrow

To process the data (when you download everything is saved as a string)
python3 scripts_and_nbs/parse_raw_data.py INPUT_FILEPATH OUTPUT_FILEPATH

Scan attribute names:
- 'type'
- 'subtype'
- 'to_ds'
- 'from_ds'
- 'flags'
- 'duration_id'
- 'sequence_ctrl'
- 'addr1'
- 'addr2'
- 'addr3'
- 'addr4'
- 'rssi'
- 'channel'
- 'payload_size'
- 'payload'

We can consider to collect and send just some relevant fields
