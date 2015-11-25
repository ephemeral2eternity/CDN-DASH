## Testing the CDN client in a VoD System
# test_cdn_client.py
# Chen Wang, Oct. 23, 2015
# chenw@cmu.edu
import random
import sys
import os
import logging
import shutil
import time
import random
from datetime import datetime
from cdn_client import *
from adaptive_cdn_client import *
from test_utils import *
from client_utils import *


### Get client name and attache to the closest cache agent
client_name = getMyName()

## Denote the server info
# srv_addr = 'www.cmu-agens.tk.global.prod.fastly.net/videos/'
# srv_addr = '23.251.129.31'
# srv_addr = 'cache-01.cloudapp.net/videos/'
# srv_addr = 'az833905.vo.msecnd.net/videos/'

cdns = {
			'Azure' : {'url' : 'az833905.vo.msecnd.net/videos/', 'QoE' : 5.0}, 
			'Fastly' : {'url' : 'www.cmu-agens.tk.global.prod.fastly.net/videos/', 'QoE': 5.0}
		}

methods = ['Azure', 'Fastly', 'Azure', 'AdaptCDN', 'AdaptCDN', 'AdaptCDN']
video_name = 'BBB'

### Get the server to start streaming
for i in range(1):
	cur_ts = time.time()

	## Testing rtt based server selection
	# waitRandom(1, 100)
	selected_method = methods[i]

	if selected_method is 'AdaptCDN':
		print "Use Adaptive CDN selection methods!"
		cdns = adaptive_cdn_client(cdns, video_name, selected_method)
	else:
		print "Use " + selected_method + " CDN to stream video!"
		selected_url = cdns[selected_method]['url']
		sqs = cdn_client(selected_url, video_name, selected_method)
		cdns[selected_method]['QoE'] = sqs

	print "Updated CDN SQS: ", cdns

	time_elapsed = time.time() - cur_ts
	if time_elapsed < 900:
		time.sleep(900 - time_elapsed)