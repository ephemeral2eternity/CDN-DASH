import urllib2
import json
import sys
from monitor.ping import *
from monitor.get_hop_info import *
from utils.params import *
import random
import client_config

# Get the list of ips to probe
def get_probing_ips(monitor):
    url = "http://%s/get_probing_ips/" % monitor

    ips = {}
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        ips = json.load(response)
    except:
        print("Failed to get the list of ips to probe. Check if " + monitor + "is working!")

    return ips

# Obtain the round trip time to a list of ips
def probe_ips(ips):
    latencies = []
    client, _ = get_ext_ip()
    for ip in ips:
        ip_lats = getRTTStat(ip, 10)
        ip_lats["src"] = client
        latencies.append(ip_lats)
    return latencies

# probe the closest networks/servers for a duration of time (denoted by period)
# every intvl time
def probe_closest(monitor, ips, period=60, intvl=5):
    start_time = time.time()
    cur_time = start_time
    all_data = {}
    updated_ips = ips
    # print(ips)
    # updated_ips["server"] = ipinfo.host2ip(client_config.cdn_host)
    while (cur_time - start_time < period):
        cur_latencies = probe_ips(updated_ips)
        # print(cur_latencies)
        for ip in cur_latencies.keys():
            if ip not in all_data.keys():
                all_data[ip] = {}
            all_data[ip].update(cur_latencies[ip])
        if (time.time() < cur_time + intvl):
            time.sleep(cur_time + intvl - time.time())
        cur_time = time.time()

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
    ips = ["195.113.161.65", "195.113.161.1"]
    all_lats = probe_ips(ips)
    print(all_lats)


