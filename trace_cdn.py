## Streaming Videos from a CDN and do traceroute and pings to the CDN
# trace_cdn.py
# Chen Wang, Jan. 3, 2016
# chenw@cmu.edu
import random
import sys
import os
import logging
import shutil
import time
from datetime import datetime
from cdn_client import *
from monitor.ping import *
from monitor.get_hop_info import *

### Get client name and attache to the closest cache agent
client_name = getMyName()

## Denote the server info
# cdn_host = 'cmu-agens.azureedge.net'
# cdn_host = 'aws.cmu-agens.com'
cdn_host = 'd18lrcyaw704ym.cloudfront.net'
video_name = 'BBB'

### Get the server to start streaming
for i in range(20):
	cur_ts = time.strftime("%m%d%H%M")
	client_ID = client_name + "_" + cur_ts

	## ping all servers
	mnRTT = getMnRTT(cdn_host)
	print mnRTT

	## Traceroute all srvs
	cdnHops = get_hop_by_host(cdn_host)
	print cdnHops

	traceData = {'RTT' : mnRTT, 'Hops' : cdnHops, 'TS' : time.time()}
	writeJson("TR_" + client_ID, traceData)

	## Testing rtt based server selection
	selected_srv_addr = cdn_host + '/videos'
	cdn_client(selected_srv_addr, video_name)