# trace_cdn.py
# Chen Wang, Mar. 3, 2016
## chenw@cmu.edu
#### Report the route of the CDN video session to manager : http://manage.cmu-agens.com/verify
#### Pick up 10 nodes to do traceroute and get the verify agents
from monitor.get_hop_info import *
from monitor.probe_closest import *
from communication.comm_manager import *
from communication.connect_cloud_agent import *
import random
from utils.test_utils import *
from utils.logger import *

## Denote the server info
cdn_host = 'az.cmu-agens.com'
# cdn_host = 'cache-01.cmu-agens.com'
# manager = 'superman.andrew.cmu.edu:8000'
# manager = 'manage.cmu-agens.com'

## Connect cloud agent and add the client itself to available clients in the manager
monitor = 'monitor.cmu-agens.com'
# monitor = 'superman.andrew.cmu.edu:8000'

## Traceroute to the CDN to get the video session
route = get_route(cdn_host)
print(route)
success = report_route(monitor, route)
logJson("TR_", route)

## Probe the closest server and networks.
ips = get_probing_ips(monitor)
if len(ips) > 0:
    latency_monitor = probe_closest(monitor, ips, period=600, intvl=60)
    logJson("RTT_", latency_monitor)