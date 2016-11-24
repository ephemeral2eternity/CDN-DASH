## Streaming Videos from a CDN and do traceroute and pings to the CDN
# trace_cdn.py
# Chen Wang, Mar. 3, 2016
# chenw@cmu.edu
import csv
from qdiag_client_agent import *
from multiprocessing import freeze_support
from monitor.get_hop_info import *
from communication.connect_cloud_agent import *

global cdn_host, num_runs, video_name, manager, monitor
global csv_trace_folder, trace_fields, out_csv_writer
global diag_agent, diag_agent_info
global client_name, client_ip, client_ID, client_info

## Denote the server info
# cdn_host = 'cmu-agens.azureedge.net'
# cdn_host = 'aws.cmu-agens.com'
if __name__ == '__main__':
	if sys.platform == 'win32':
		freeze_support()

	if len(sys.argv) > 2:
		cdn_host = sys.argv[1]
	else:
		cdn_host = "az.cmu-agens.com"
	if len(sys.argv) > 2:
		num_runs = int(sys.argv[2])
	else:
		num_runs = 1
	
	if len(sys.argv) > 3:
		client_name = sys.argv[3]
	else:
		# client_name = "local"
		client_name = getMyName()

	video_name = 'BBB'

	## ==================================================================================================
	# Get Client INFO, streaming configuration file, CDN server and route to the CDN and report the route
	# INFO to the anomaly locator agent
	## ==================================================================================================
	client_ip, client_info = get_ext_ip()
	client_info['name'] = client_name
	device_info = get_device_info()
	client_info['device'] = device_info
	## Create Trace CSV file
	cur_ts = time.strftime("%m%d%H%M%S")
	client_ID = client_name + "_" + cur_ts

	## ==================================================================================================
	# Trace file to write QoE and other parameters, etc.
	## ==================================================================================================
	trace_fields = ["TS", "Buffer", "Freezing", "QoE1", "QoE2", "Representation", "Response", "Server", "ChunkID"]
	csv_trace_folder = os.getcwd() + "/dataQoE/"

	try:
		os.stat(csv_trace_folder)
	except:
		os.mkdir(csv_trace_folder)

	csv_trace_file = client_ID + ".csv"
	out_csv_trace = open(csv_trace_folder + csv_trace_file, 'wb')
	out_csv_writer = csv.DictWriter(out_csv_trace, fieldnames=trace_fields)
	out_csv_writer.writeheader()

	## ==================================================================================================
	### Manager and monitor, etc.
	## ==================================================================================================
	manager = "manage.cmu-agens.com"
	monitor = "monitor.cmu-agens.com"
	diag_agent_info = get_my_cloud_agent(manager)
	print "Connected cloud agent: ", diag_agent_info
	diag_agent = diag_agent_info['ip']

	# waitRandom(1, 300)
	for i in range(num_runs):
		## Testing rtt based server selection
		selected_srv_addr = cdn_host + '/videos/'
		# client_ID, CDN_SQS, uniq_srvs = qoe_agent(selected_srv_addr, video_name, locator)
		qdiag_client_agent()

		if os.path.exists(os.getcwd() + "/tmp/"):
			shutil.rmtree(os.getcwd() + "/tmp/")

	## Close tracefile
	out_csv_trace.close()
