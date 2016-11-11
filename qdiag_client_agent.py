from communication.thread_wrapper import *
from dash.fault_tolerance import *
from dash.utils import *
from qoe.dash_chunk_qoe import *
from utils.client_utils import *
from anomaly.detect_anomaly import *
from monitor.get_device_info import *


## ==================================================================================================
# define the simple client agent that only downloads videos from denoted server
# @input : srv_addr ---- the server name address
#		   video_name --- the string name of the requested video
## ==================================================================================================
def qdiag_client_agent(cdn_host, video_name, diagAgent, client_ID, traceWriter):
	## Define all parameters used in this client
	alpha = 0.5
	retry_num = 10

	## CDN SQS
	qoe_queue = []
	uniq_srvs = []

	## Process pool
	procs = []

	## ==================================================================================================
	# Get Client INFO, streaming configuration file, CDN server and route to the CDN and report the route
	# INFO to the anomaly locator agent
	## ==================================================================================================
	client_ip, client_info = get_ext_ip()
	client = client_info["name"]

	rsts, srv_ip = ft_mpd_parser(cdn_host, retry_num, video_name)
	if not rsts:
		return

	## Fork a process doing traceroute to srv_ip and report it to the locator.
	cdn_host_name = cdn_host.split('/')[0]
	client_info["device"] = get_device_info()
	tr_proc = fork_cache_client_info(diagAgent, client_info, srv_ip, cdn_host_name, True)
	procs.append(tr_proc)

	### ===========================================================================================================
	## Read parameters from dash.mpd_parser
	### ===========================================================================================================
	vidLength = int(rsts['mediaDuration'])
	minBuffer = num(rsts['minBufferTime'])
	reps = rsts['representations']

	# Get video bitrates in each representations
	vidBWs = {}
	for rep in reps:
		if not 'audio' in rep:
			vidBWs[rep] = int(reps[rep]['bw'])
	# print vidBWs

	sortedVids = sorted(vidBWs.items(), key=itemgetter(1))

	# Start streaming from the minimum bitrate
	minID = sortedVids[0][0]
	vidInit = reps[minID]['initialization']
	maxBW = sortedVids[-1][1]

	# Read common parameters for all chunks
	timescale = int(reps[minID]['timescale'])
	chunkLen = int(reps[minID]['length']) / timescale
	chunkNext = int(reps[minID]['start'])

	## ==================================================================================================
	# Start downloading the initial video chunk
	## ==================================================================================================
	curBuffer = 0
	chunk_download = 0

	## Traces to write out
	client_tr = {}
	http_errors = {}

	## Download initial chunk
	loadTS = time.time()
	print "[" + client_ID + "] Start downloading video " + video_name + " at " + \
		  datetime.datetime.fromtimestamp(int(loadTS)).strftime("%Y-%m-%d %H:%M:%S") + \
		  " from server : " + cdn_host

	(vchunk_sz, chunk_srv_ip, error_codes) = ft_download_chunk(cdn_host, retry_num, video_name, vidInit)
	http_errors.update(error_codes)
	if vchunk_sz == 0:
		## Write out traces after finishing the streaming
		writeHTTPError(client_ID, http_errors)
		return

	startTS = time.time()
	print "[" + client_ID + "] Start playing video at " + datetime.datetime.fromtimestamp(int(startTS)).strftime("%Y-%m-%d %H:%M:%S")
	est_bw = vchunk_sz * 8 / (startTS - loadTS)
	print "|-- TS --|-- Chunk # --|- Representation -|-- Linear QoE --|-- Cascading QoE --|-- Buffer --|-- Freezing --|-- Selected Server --|-- Chunk Response Time --|"
	preTS = startTS
	chunk_download += 1
	curBuffer += chunkLen

	## ==================================================================================================
	# Start streaming the video
	## ==================================================================================================
	while (chunkNext * chunkLen < vidLength):
		nextRep = findRep(sortedVids, est_bw, curBuffer, minBuffer)
		vidChunk = reps[nextRep]['name'].replace('$Number$', str(chunkNext))
		loadTS = time.time()
		(vchunk_sz, chunk_srv_ip, error_codes) = ft_download_chunk(cdn_host, retry_num, video_name, vidChunk)

		# If the client changes servers, get the traceroute to the new server.
		if chunk_srv_ip != srv_ip:
			pre_srv_ip = srv_ip
			srv_ip = chunk_srv_ip
			eventType = "server_switch"
			## Fork a process doing traceroute to srv_ip and report it to the locator.
			tr_proc = fork_cache_client_info(diagAgent, client_info, srv_ip, cdn_host)
			procs.append(tr_proc)
			event_proc = fork_add_event(diagAgent, client_ip, eventType, pre_srv_ip, srv_ip)
			procs.append(event_proc)

		http_errors.update(error_codes)
		if vchunk_sz == 0:
			## Write out traces after finishing the streaming
			writeHTTPError(client_ID, http_errors)
			return

		curTS = time.time()
		rsp_time = curTS - loadTS
		est_bw = vchunk_sz * 8 / rsp_time
		time_elapsed = curTS - preTS

		# Compute freezing time
		if time_elapsed > curBuffer:
			freezingTime = time_elapsed - curBuffer
			curBuffer = 0
		# print "[AGENP] Client freezes for " + str(freezingTime)
		else:
			freezingTime = 0
			curBuffer = curBuffer - time_elapsed

		# Compute QoE of a chunk here
		curBW = num(reps[nextRep]['bw'])
		chunk_linear_QoE = computeLinQoE(freezingTime, curBW, maxBW)
		chunk_cascading_QoE = computeCasQoE(freezingTime, curBW, maxBW)

		qoe_queue.append(chunk_cascading_QoE)

		# print "Chunk Size: ", vchunk_sz, "estimated throughput: ", est_bw, " current bitrate: ", curBW

		if (chunkNext > update_period):
			print "|---", str(curTS), "---|---", str(chunkNext), "---|---", nextRep, "---|---", str(chunk_linear_QoE), "---|---", \
				str(chunk_cascading_QoE), "---|---", str(curBuffer), "---|---", str(freezingTime), "---|---", chunk_srv_ip, "---|---", str(rsp_time), "---|"

			cur_tr = dict(TS=curTS, Representation=nextRep, QoE1=chunk_linear_QoE, QoE2=chunk_cascading_QoE, Buffer=curBuffer, \
										Freezing=freezingTime, Server=chunk_srv_ip, Response=rsp_time, ChunkID=chunkNext)

			traceWriter.writerow(cur_tr)

		if chunk_srv_ip not in uniq_srvs:
			uniq_srvs.append(chunk_srv_ip)

		# Update iteration information
		curBuffer = curBuffer + chunkLen
		if curBuffer > 30:
			time.sleep(curBuffer - 30)

		## Detect anomalies or send updates periodically
		if (chunkNext % update_period == 0) and (chunkNext > update_period - 1):
			recent_qoes = qoe_queue[-update_period:]
			mnQoE = sum(recent_qoes) / float(len(recent_qoes))
			[isAnomaly, anomaly_type] = detect_anomaly(recent_qoes)
			if isAnomaly:
				diag_p = fork_diagnose_anomaly(diagAgent, client_ip, srv_ip, mnQoE, anomaly_type)
				procs.append(diag_p)
			else:
				update_p = fork_update_attributes(diagAgent, client_ip, srv_ip, mnQoE)
				procs.append(update_p)

		preTS = curTS
		chunk_download += 1
		chunkNext += 1

	## Write out traces after finishing the streaming
	if http_errors:
		writeTrace(client_ID + "_httperr", http_errors)

	for p in procs:
		p.join(timeout=100)
	return uniq_srvs
