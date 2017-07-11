## Common parameters
import os

# cdn_host = "cache-01.cmu-agens.com"
# cdn_host = "aws.cmu-agens.com"
cdn_host = "verizon.cmu-agens.com"
# cdn_host = "gcdn.cmu-agens.com"
manager = "manage.cmu-agens.com"
# locator = "local"
locator = "geo"
monitor = "monitor.cmu-agens.com"
# monitor = "superman.andrew.cmu.edu:8000"
reportMonitor = True

### Parameters for streaming
wait_time = 300
num_runs = 5
video_name = "BBB"
update_period = 12
cdn_srv_addr = cdn_host + '/videos/'

## Number of chunks to skip
num_of_chunks_to_skip = 5

## Parameter for the user device
device_id = 0

csv_trace_folder = os.getcwd() + "/dataQoE/"
route_trace_folder = os.getcwd() + "/routeData/"
monitor_trace_folder = os.getcwd() + "/monitorData/"
qoe_trace_fields = ["TS", "Buffer", "Freezing", "QoE1", "QoE2", "Representation", "Response", "Server", "ChunkID"]

try:
    os.stat(csv_trace_folder)
except:
    os.mkdir(csv_trace_folder)

try:
    os.stat(route_trace_folder)
except:
    os.mkdir(route_trace_folder)
