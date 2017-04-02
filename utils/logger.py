import json
import time
import os
import client_config
from utils.client_utils import *

def logJson(fileNamePrefix, data):
    dataFolder = client_config.monitor_trace_folder
    try:
        os.stat(dataFolder)
    except:
        os.mkdir(dataFolder)

    client_name = getMyName()
    cur_ts = time.strftime("%m%d%H%M%S")
    fileName = dataFolder + fileNamePrefix + "_" + client_name + "_" + cur_ts + ".json"
    with open(fileName, "w") as f:
        json.dump(data, f, indent=4, sort_keys=True)