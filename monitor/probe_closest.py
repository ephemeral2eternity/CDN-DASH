import urllib2
import json
import sys
from monitor.ping import *

# Get the list of ips to probe
def get_probing_ips(monitor):
    url = "http://%s/get_probing_ips/" % monitor

    ips = []
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = json.load(response)
        ips = data["ips"]
    except:
        print("Failed to get the list of ips to probe. Check if " + monitor + "is working!")

    return ips

# Obtain the round trip time to a list of ips
def probe_ips(ips):
    latencies = {}
    for ip in ips:
        cur_time = time.time()
        cur_lat, _ = getMnRTT(ip)
        latencies[ip] = {cur_time:cur_lat}
    return latencies

# probe the closest networks/servers for a duration of time (denoted by period)
# every intvl time
def probe_closest(monitor, ips, period=600, intvl=60):
    start_time = time.time()
    cur_time = start_time
    all_data = {}
    for ip in ips:
        all_data[ip] = {}
    while (cur_time - start_time < period):
        cur_latencies = probe_ips(ips)
        for ip in ips:
            all_data[ip].update(cur_latencies[ip])
        if (time.time() < cur_time + intvl):
            time.sleep(cur_time + intvl - time.time())
        cur_time = time.time()

    report_probing(monitor, all_data)
    return all_data

def report_probing(monitor, data):
    url = "http://%s/report" % monitor

    isReported = False

    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(data))
        print(response.read())
        isReported = True
    except:
        print("Failed to report monitored data to " + monitor)
    return isReported

if __name__ == "__main__":
    monitor = "superman.andrew.cmu.edu:8000"
    # ips = get_probing_ips(monitor)
    ips = ["68.65.124.84", "128.2.208.1", "198.71.47.129", "72.21.81.200"]
    all_lats = probe_closest(monitor, ips, 60, 10)


