## Common parameters
import os

# cdn_host = "cache-01.cmu-agens.com"
cdn_host = "az.cmu-agens.com"
manager = "manage.cmu-agens.com"
locator = "geo"
# locator = "locator-02"
monitor = "monitor.cmu-agens.com"
# monitor = "superman.andrew.cmu.edu:8000"
reportMonitor = True

### Parameters for streaming
num_runs = 5
video_name = "BBB"
update_period = 12
cdn_srv_addr = cdn_host + '/videos/'

## Number of chunks to skip
num_of_chunks_to_skip = 5

## Parameter for the user device
device_id = 1

### Parameters for verify agents
duration_to_probe = 3600
probe_step = 10

csv_trace_folder = os.getcwd() + "/dataQoE/"
route_trace_folder = os.getcwd() + "/routeData/"
monitor_trace_folder = os.getcwd() + "/monitorData/"
qoe_trace_fields = ["TS", "Buffer", "Freezing", "QoE1", "QoE2", "Representation", "Response", "Server", "ChunkID"]
rtt_trace_fields = ["TS", "src", "dst", "rtt"]

try:
    os.stat(csv_trace_folder)
except:
    os.mkdir(csv_trace_folder)

try:
    os.stat(route_trace_folder)
except:
    os.mkdir(route_trace_folder)
