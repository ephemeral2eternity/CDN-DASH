# trace_cdn.py
# Chen Wang, Mar. 3, 2016
## chenw@cmu.edu
#### Report the route of the CDN video session to manager : http://manage.cmu-agens.com/verify
#### Pick up 10 nodes to do traceroute and get the verify agents
from monitor.get_hop_info import *
from communication.comm_manager import *
from communication.connect_cloud_agent import *
import random
from utils.test_utils import *

## Denote the server info
# cdn_host = 'cmu-agens.azureedge.net'
# cdn_host = 'aws.cmu-agens.com'
cdn_host = 'az.cmu-agens.com'
video_name = 'BBB'
# manager = 'superman.andrew.cmu.edu:8000'
# manager = 'manage.cmu-agens.com'

## Connect cloud agent and add the client itself to available clients in the manager
# monitor_agent = 'monitor.cmu-agens.com'
monitor = 'superman.andrew.cmu.edu:8000'

## Traceroute to the CDN to get the video session
waitRandom(1, 100)
route = get_route(cdn_host)
ft_report_route(monitor, route)