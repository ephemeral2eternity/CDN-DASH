## Streaming Videos from a CDN and do traceroute and pings to the CDN
# trace_cdn.py
# Chen Wang, Mar. 3, 2016
# chenw@cmu.edu
import random
import sys
import os
import logging
import shutil
import time
from datetime import datetime
from qoe_agent import *
from monitor.ping import *
from multiprocessing import freeze_support
from monitor.get_hop_info import *
from communication.connect_locator import *

## Denote the server info
# cdn_host = 'cmu-agens.azureedge.net'
# cdn_host = 'aws.cmu-agens.com'
if __name__ == '__main__':
	if sys.platform == 'win32':
		freeze_support()
	cdn_host = 'az.cmu-agens.com'
	video_name = 'BBB'

	### Get the server to start streaming
	manager = "manage.cmu-agens.com"
	for i in range(1):
		## Testing rtt based server selection
		locator_info = get_my_locator(manager)
		print "Connected Locator: ", locator_info
		locator = locator_info['ip']
		selected_srv_addr = cdn_host + '/videos/'
		# client_ID, CDN_SQS, uniq_srvs = qoe_agent(selected_srv_addr, video_name, locator)
		qoe_agent(selected_srv_addr, video_name, locator)