import urllib2
from monitor.ping import *

def addRTT(monitor, src, dst):
    rtt = getMnRTT(dst)
    url = "http://%s/rtt/add?src=%s&dst=%s&rtt=%.4f" % (monitor, src, dst, rtt)
    try:
        rsp = urllib2.urlopen(url)
        print "Probing %s successfully" % dst
    except:
        print "Failed to probe %s" % dst
