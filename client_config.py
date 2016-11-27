## Configuration file of the dash client
from utils.client_utils import *
from monitor.get_device_info import *
from communication.connect_cloud_agent import *
import csv

def init():
    global cdn_host, cdn_srv_addr, num_runs, video_name, manager, monitor
    global csv_trace_folder, trace_fields, out_csv_writer
    global diag_agent, diag_agent_info
    global client_name, client_ip, client_ID, client_info

    video_name = 'BBB'
    cdn_host = "az.cmu-agens.com"
    cdn_srv_addr = cdn_host + '/videos/'
    num_runs = 5

    manager = "manage.cmu-agens.com"
    monitor = "monitor.cmu-agens.com"

    trace_fields = ["TS", "Buffer", "Freezing", "QoE1", "QoE2", "Representation", "Response", "Server", "ChunkID"]

    client_name = getMyName()

    ## ==================================================================================================
    # Get Client INFO, streaming configuration file, CDN server and route to the CDN and report the route
    # INFO to the anomaly locator agent
    ## ==================================================================================================
    client_ip, client_info = get_ext_ip()
    client_info['name'] = client_name
    device_info = get_device_info()
    client_info['device'] = device_info
    ## Create Trace CSV file
    cur_ts = time.strftime("%m%d%H%M%S")
    client_ID = client_name + "_" + cur_ts

    ## ==================================================================================================
    # Trace file to write QoE and other parameters, etc.
    ## ==================================================================================================
    csv_trace_folder = os.getcwd() + "/dataQoE/"

    try:
        os.stat(csv_trace_folder)
    except:
        os.mkdir(csv_trace_folder)

    csv_trace_file = client_ID + ".csv"
    out_csv_trace = open(csv_trace_folder + csv_trace_file, 'wb')
    out_csv_writer = csv.DictWriter(out_csv_trace, fieldnames=trace_fields)
    out_csv_writer.writeheader()

    ## ==================================================================================================
    ### Manager and monitor, etc.
    ## ==================================================================================================
    diag_agent_info = get_my_cloud_agent(manager)
    diag_agent = diag_agent_info['ip']

