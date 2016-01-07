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
from client_utils import *
from monitor.ping import *
from monitor.traceroute import *

### Get client name and attache to the closest cache agent
client_name = getMyName()

## Denote the server info
cdn_host = 'cmu-agens.azureedge.net'
video_name = 'BBB'

### Get the server to start streaming
for i in range(20):
	cur_ts = time.strftime("%m%d%H%M")
	client_ID = client_name + "_" + cur_ts

	## ping all servers
	mnRTT = getMnRTT(cdn_host)
	print mnRTT

	## Traceroute all srvs
	cdnHops = traceroute(cdn_host)
	print cdnHops

	traceData = {'RTT' : mnRTT, 'Hops' : cdnHops, 'TS' : time.time()}
	writeJson("TR_" + client_ID, traceData)

	## Testing rtt based server selection
	selected_srv_addr = cdn_host + '/videos/'
	cdn_client(selected_srv_addr, video_name)