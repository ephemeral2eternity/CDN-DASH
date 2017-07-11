'''
PING a server with count times and get the RTT list
'''
from subprocess import Popen, PIPE
import re
import sys
import time
from math import sqrt
from get_hop_info import *

def stddev(lst):
    mean = float(sum(lst)) / len(lst)
    return sqrt(float(reduce(lambda x, y: x + y, map(lambda x: (x - mean) ** 2, lst))) / len(lst))

def extract_number(s):
    regex=r'[-+]?[0-9]*\.?[0-9]+(?:[eE][-+]?[0-9]+)?'
    return re.findall(regex,s)

def extractPingInfo(pingStr):
    curDataList = pingStr.split()
    pingData = {}
    for curData in curDataList:
        # print curData
        if '=' in curData:
            dataStr = curData.split('=')
            dataVal = extract_number(dataStr[1])
            pingData[dataStr[0]] = float(dataVal[0])
        elif '<' in curData:
            dataStr = curData.split('<')
            dataVal = extract_number(dataStr[1])
            pingData[dataStr[0]] = float(dataVal[0])
    return pingData

## Call system command to ping a
def ping(ip, count):
    '''
    Pings a host and return True if it is available, False if not.
    '''
    if sys.platform == 'win32':
        cmd = ['ping', '-n', str(count), ip]
    else:
        cmd = ['ping', '-c', str(count), ip]
    process = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = process.communicate()
    # print stdout
    rttList, srv_ip = parsePingRst(stdout, count)
    return rttList, srv_ip

def getMnRTT(ip, count=3):
    rttList, srv_ip = ping(ip, count)
    if len(rttList) > 0:
        mnRTT = sum(rttList) / float(len(rttList))
    else:
        mnRTT = -20.0
    return mnRTT, srv_ip

def getRTTStat(ip, count=3):
    rttList, srv_ip = ping(ip, count)
    if len(rttList) > 0:
        loss = 1 - len(rttList)/float(count)
        mnRTT = sum(rttList) / float(len(rttList))
        maxRTT = max(rttList)
        minRTT = min(rttList)
        stdRTT = stddev(rttList)
    else:
        loss = 1.0
        mnRTT = -1.0
        maxRTT = -1.0
        minRTT = -1.0
        stdRTT = -1.0

    return {"TS" : time.time(), "dst": srv_ip, "rttLoss":loss, "rttMean":mnRTT, "rttMax":maxRTT, "rttMin":minRTT, "rttStd":stdRTT}

def parsePingRst(pingString, count):
    rtts = []
    srv_ip = None
    lines = pingString.splitlines()
    for line in lines:
        curline = line
        # print curline
        if ("time=" in curline) or ("time<" in curline):
            curDataStr = curline.split(':', 2)[1]
            curDataDict = extractPingInfo(curDataStr)
            # print "curDataDict:", curDataDict
            rtts.append(curDataDict['time'])

        if not srv_ip:
            tmp = re.search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', curline)
            if tmp:
                srv_ip = tmp.group()
    return rtts, srv_ip


if __name__ == "__main__":
    latStats = getRTTStat('verizon.cmu-agens.com', 10)
    print latStats
