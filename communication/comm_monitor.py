import urllib2
import json
from monitor.ping import *

def addRTT(monitor, src, dst, results):
    rtt, srv_ip = getMnRTT(dst)

    if not srv_ip:
        srv_ip = dst

    # url = "http://%s/rtt/add?src=%s&dst=%s&rtt=%.4f" % (monitor, src, dst, rtt)

    curTS = time.time()
    cur_rst = dict(TS=curTS, src=src, dst=srv_ip, rtt=rtt)
    results.put(cur_rst)

    #try:
    #    rsp = urllib2.urlopen(url)
    #    print "Probing %s successfully" % dst
    #except:
    #    print "Failed to probe %s" % dst


def addQoE(monitor, src, dst, chunkID, qoe):
    url = "http://%s/qoe/add?src=%s&dst=%s&id=%d&qoe=%.4f" % (monitor, src, dst, chunkID, qoe)
    try:
        rsp = urllib2.urlopen(url)
        print "Add QoE successfully"
    except:
        print "Failed to report QoE to %s" % monitor

############################################################################
# Probe the CDN server via traceroute and report to the monitor
# Monitor server: monitor.cmu-agens.com
# route: the traceroute data including client and server as the first and last hops
#############################################################################
def report_route_to_monitor(monitor, route):
    ## Debug URL
    url = "http://%s/add_route" % monitor
    isSuccess = True
    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(route))
    except:
        print "Failed to report the traceroute data to monitor " + monitor
        isSuccess = False

    return isSuccess