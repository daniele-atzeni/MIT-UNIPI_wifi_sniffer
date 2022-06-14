# this for taking inputs from command line
import sys
#
import pandas as pd
import numpy as np


def parse_single_scan(scan_str:str) -> list:
    scan_str = scan_str[1:-1]       # delete last and first squared brackets
    scan_list = scan_str.split(',')
    # now we have to cast the entries into ints
    for i, el in enumerate(scan_list):
        if el == 'null' or el == 'FF:FF:FF:FF:FF:FF':
            scan_list[i] = np.nan   # type: ignore
        else:
            try:
                scan_list[i] = int(el)  # type: ignore
            except ValueError:
                scan_list[i] = el
    return scan_list
    

def parse_scan_list(scan_str:str) -> list:
    '''
    function that transforms the scan results, saved as strings, into lists of lists
    '''
    scan_str = scan_str[1: -1]     # delete last and first squared brackets
    scan_list = scan_str.split(']')    # this also remove the closed square bracket
    scan_list = [el+ ']' for el in scan_list] # add the closed square bracket back
    scan_list = [el[2:] for i, el in enumerate(scan_list) if i != 0]   # remove commas and spaces between the scans
    # since the last char of the string is a closed square bracket, we have to remove the last element of this list
    scan_list = scan_list[:-1]
    scan_list = [el.replace(' ', '') for el in scan_list] # delete spaces

    scan_list = [parse_single_scan(el) for el in scan_list] 
    
    return scan_list


def main():
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

    _, INPUT_FILENAME, OUTPUT_FILENAME = sys.argv
    #INPUT_FILENAME = 'scripts_and_nbs/example.csv'
    #OUTPUT_FILENAME = 'example_parsed.csv'

    original_df = pd.read_csv(INPUT_FILENAME)

    # the original df contains also information about when the data is stored into the zdm etc.
    # we are just interest in the payload, i.e., the data we sent from the devices,
    # and the device_id

    interesting_data = original_df[['ts', 'device_id', 'scans']]
    # we want to change the granularity of the data, i.e., we want a row for each 
    # device scanned instead of a row for each scan
    new_data = []
    for i, row in interesting_data.iterrows():
        dev_id = row.device_id
        ts = row.ts
        scans = parse_scan_list(row.scans)  # this is a list of scans (lists)
        for scan in scans:
            new_data.append([ts, dev_id] + scan)
    
    new_df = pd.DataFrame(new_data, columns = ['ts', 'device_id'] + SCAN_OUTPUTS)
    new_df.to_csv(OUTPUT_FILENAME)
    

if __name__ == "__main__":
    main()