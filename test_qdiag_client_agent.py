## Streaming Videos from a CDN and do traceroute and pings to the CDN
# trace_cdn.py
# Chen Wang, Mar. 3, 2016
# chenw@cmu.edu
import csv
from qdiag_client_agent import *
from multiprocessing import freeze_support
from monitor.get_hop_info import *
from utils.test_utils import *
import client_config
import trace_writer


## Denote the server info
# cdn_host = 'cmu-agens.azureedge.net'
# cdn_host = 'aws.cmu-agens.com'
if __name__ == '__main__':
	if sys.platform == 'win32':
		freeze_support()

	if len(sys.argv) > 2:
		client_config.cdn_host = sys.argv[1]

	if len(sys.argv) > 2:
		client_config.num_runs = int(sys.argv[2])
	
	if len(sys.argv) > 3:
		client_config.client_name = sys.argv[3]

	waitRandom(1, 300)
	csv_writer = trace_writer.initQoE()
	for i in range(client_config.num_runs):
		qdiag_client_agent(csv_writer)

		if os.path.exists(os.getcwd() + "/tmp/"):
			shutil.rmtree(os.getcwd() + "/tmp/")

	## Close tracefile
	trace_writer.out_qoe_trace.close()
