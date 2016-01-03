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
for i in range(5):
	cur_ts = time.time()

	## ping all servers
	mnRTT = getMnRTT(cdn_host)
	print mnRTT

	## Traceroute all srvs
	cdnHops = traceroute(cdn_host)
	print cdnHops

	traceData = {'RTT' : mnRTT, 'Hops' : cdnHops}
	writeJson("TR_" + client_name + "_" + str(int(cur_ts)), traceData)

	## Testing rtt based server selection
	# waitRandom(1, 100)
	selected_srv_addr = cdn_host + '/videos/'
	cdn_client(selected_srv_addr, video_name)