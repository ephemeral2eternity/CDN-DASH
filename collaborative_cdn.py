from dash.fault_tolerance import *
from dash.utils import *
from qoe.dash_chunk_qoe import *
from utils.client_utils import *
import collaborative_client
import collaborative_server
import thread
from time import sleep

isDone=False
received_objs={}
def collaborative_select_best_addr():
	cdn_qoe = 0
	selected_cdn = ''
	for current_cdn in addrs.keys():
		if addrs[current_cdn]['QoE'] > cdn_qoe:
			selected_cdn = current_cdn
			cdn_qoe = addrs[current_cdn]['QoE']
	isDone=True
	return selected_cdn

def select_best_addr(addrs):
	cdn_qoe = 0
	selected_cdn = ''
	for current_cdn in addrs.keys():
		if addrs[current_cdn]['QoE'] > cdn_qoe:
			selected_cdn = current_cdn
			cdn_qoe = addrs[current_cdn]['QoE']
	return selected_cdn

def connect_and_query(video_name,clients):
	global isDone
	port = 31114;
	received_objs[video_name]=[]
	for i in range (0,len(clients)):
		try:
			mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		except socket.error:
        		print 'Failed to create socket'
        		sys.exit()
		print 'Socket Created'
		try:
			mysocket.connect((clients[i] , port))
		except socket.error:
			print "Cannot connect"
			sleep(5)
			i=i-1
			continue
		print 'Socket Connected to ' + clients[i]

		#Send some data to remote server
		message = video_name+"\r\n\r\n"
		try :
		        #Set the whole string
		        mysocket.sendall(message)
		except socket.error:
		        print 'Send failed'
		        sys.exit()

		#Now receive data
		response = mysocket.recv(4096)
		print response
		received_objs[video_name].append(response)
	isDone= True
	

## ==================================================================================================
# define the simple client agent that only downloads videos from denoted server
# @input : addr_objs ---- the dict of cdn addresses as keys initialized with QoE they have as values
#		   video_name --- the string name of the requested video
## ==================================================================================================
def collaborative_cdn(addr_objs, video_name, method=None):
	global isDone
	thread.start_new_thread(collaborative_server.setup_listening_socket,())
	#TODO get list of users from locator agents
	clients=["localhost"]
	thread.start_new_thread(connect_and_query,(video_name,clients))		
	sleep(500)

	## Define all parameters used in this client
	alpha = 0.5
	WARMUP_PERIOD = 4
	retry_num = 10

	## ==================================================================================================
	## Client name and info
	client = str(socket.gethostname())
	cur_ts = time.strftime("%m%d%H%M")
	if method is not None:
		client_ID = client + "_" + cur_ts + "_" + method
	else:
		client_ID = client + "_" + cur_ts

	## ======================================================================================
	## Select the CDN according to QoE
	# SINDHU TODO add as function parameter
	selected_cdn = select_best_addr(addr_objs)
	selected_cdn_url = addr_objs[selected_cdn]['url']
	## ==================================================================================================
	## Parse the mpd file for the streaming video
	## ==================================================================================================
	(rsts,sin_server_ip) = ft_mpd_parser(selected_cdn_url, retry_num, video_name)
	if not rsts:
		return
	print type(rsts)
	print rsts
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
	print vidBWs

	sortedVids = sorted(vidBWs.items(), key=itemgetter(1))

	# Start streaming from the minimum bitrate
	minID = sortedVids[0][0]
	vidInit = reps[minID]['initialization']
	maxBW = sortedVids[-1][1]

	# Read common parameters for all chunks
	timescale = int(reps[minID]['timescale'])
	chunkLen = int(reps[minID]['length']) / timescale
	chunkNext = int(reps[minID]['start'])
	chunkNum=1
	## ==================================================================================================
	# Start downloading the initial video chunk
	## ==================================================================================================
	curBuffer = 0
	chunk_download = 0

	## Traces to write out
	client_tr = {}
	http_errors = {}
	sqs_tr = {}

	## Download initial chunk
	loadTS = time.time()
	print "[" + client_ID + "] Start downloading video " + video_name + " at " + \
	datetime.datetime.fromtimestamp(int(loadTS)).strftime("%Y-%m-%d %H:%M:%S") + \
	" from CDN : " + selected_cdn

	(vchunk_sz, chunk_srv_ip, error_codes) = ft_download_chunk(selected_cdn_url, retry_num, video_name, vidInit)
	http_errors.update(error_codes)
	if vchunk_sz == 0:
		## Write out traces after finishing the streaming
		writeTrace(client_ID + "_cdn", client_tr)
		writeHTTPError(client_ID, http_errors)
		return

	startTS = time.time()
	print "[" + client_ID + "] Start playing video at " + datetime.datetime.fromtimestamp(int(startTS)).strftime("%Y-%m-%d %H:%M:%S")
	est_bw = vchunk_sz * 8 / (startTS - loadTS)
	print "|-- TS --|-- Chunk # --|- Representation -|-- Linear QoE --|--Cascade QoE --|-- Buffer --|-- Freezing --|-- Selected Server --|-- Selected CDN --|-- Chunk Response Time --|"
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
		(vchunk_sz, chunk_srv_ip, error_codes) = ft_download_chunk(selected_cdn_url, retry_num, video_name, vidChunk)
		http_errors.update(error_codes)
		if vchunk_sz == 0:
			## Write out traces after finishing the streaming
			writeTrace(client_ID, client_tr)
			writeTrace(client_ID + "_SQS", sqs_tr)
			writeTrace(client_ID + "_httperr", http_errors)
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

		if chunkNext > WARMUP_PERIOD:
			if(chunkNum==1):
				addr_objs[selected_cdn]['QoE']=chunk_cascading_QoE
				chunkNum=chunkNum+1
			else:
				addr_objs[selected_cdn]['QoE'] = addr_objs[selected_cdn]['QoE'] * (1 - alpha) + chunk_cascading_QoE * alpha
				## ======================================================================================
				## Select the CDN according to QoE
				if(isDone==true):
					selected_cdn = collaborative_select_best_addr(addr_objs)
					selected_cdn_url = addr_objs[selected_cdn]['url']

		cur_sqs = {}
		for cdn in addr_objs:
			print cdn, addr_objs[cdn]['QoE']
			cur_sqs[cdn] = addr_objs[cdn]['QoE']
		sqs_tr[curTS] = cur_sqs

		print "|---", str(curTS), "---|---", str(chunkNext), "---|---", nextRep, "---|---", str(chunk_linear_QoE), "---|---", str(chunk_cascading_QoE), "---|---", \
						str(curBuffer), "---|---", str(freezingTime), "---|---", chunk_srv_ip, "---|---", selected_cdn, "---|---", str(rsp_time), "---|"
		
		client_tr[chunkNext] = dict(TS=curTS, Representation=nextRep, QoE1=chunk_linear_QoE, QoE2=chunk_cascading_QoE, Buffer=curBuffer, \
			Freezing=freezingTime, Server=chunk_srv_ip, CDN = selected_cdn, Response=rsp_time)
			
		# Update iteration information
		curBuffer = curBuffer + chunkLen
		if curBuffer > 30:
			time.sleep(curBuffer - 30)

		preTS = curTS
		chunk_download += 1
		chunkNext += 1

	## Write out traces after finishing the streaming
	writeTrace(client_ID, client_tr)
	writeTrace(client_ID + "_SQS", sqs_tr)
	writeTrace(client_ID + "_httperr", http_errors)
	return addr_objs
