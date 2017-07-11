import json
import time
import os
import csv
import client_config
from utils.client_utils import *

def logJson(fileNameSuffix, data):
    dataFolder = client_config.monitor_trace_folder
    try:
        os.stat(dataFolder)
    except:
        os.mkdir(dataFolder)

    client_ip, _ = get_ext_ip()
    cur_ts = time.strftime("%m%d%H%M%S")
    fileName = dataFolder + client_ip + "_" + cur_ts + fileNameSuffix + ".json"
    with open(fileName, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)

## ==================================================================================================
# Finished steaming videos, write out traces
# @input : client_ID --- the client ID to write traces
# 		   client_tr --- the client trace dictionary
## ==================================================================================================
def logCSV(fileNameSuffix, data):
    client_ip, _ = get_ext_ip()
    cur_ts = time.strftime("%m%d")
    client_ID = client_ip + "_" + cur_ts
    fileName = client_ID + "_" + fileNameSuffix

    dataFolder = client_config.monitor_trace_folder
    try:
        os.stat(dataFolder)
    except:
        os.mkdir(dataFolder)

    if len(data) > 0:
        csvFields = data[0].keys()
        ## ==================================================================================================
        ### Initialize the trace writer
        ## ==================================================================================================
        if os.path.exists(dataFolder + fileName):
            out_file = open(dataFolder + fileName, 'ab')
            csv_writer = csv.DictWriter(out_file, fieldnames=csvFields)
        else:
            out_file = open(dataFolder + fileName, 'wb')
            csv_writer = csv.DictWriter(out_file, fieldnames=csvFields)
            csv_writer.writeheader()

        for obj in data:
            csv_writer.writerow(obj)

        out_file.close()