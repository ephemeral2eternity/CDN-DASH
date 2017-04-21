import urllib2
import json
import sys
from monitor.ping import *
from utils.params import *
import random
import client_config
from ipinfo import ipinfo

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
    latencies = {}
    updated_ips = ips
    print(updated_ips)
    for obj in updated_ips.keys():
        cur_time = time.time()
        if obj.startswith("network"):
            ip = random.choice(updated_ips[obj])
        else:
            ip = updated_ips[obj]
        cur_lat, _ = getMnRTT(ip)
        while (cur_lat < 0) and (obj.startswith("network")) and (len(updated_ips[obj]) > 1):
            updated_ips[obj].remove(ip)
            ip = random.choice(updated_ips[obj])
            cur_lat, _ = getMnRTT(ip)

        latencies[ip] = {cur_time:cur_lat}
    return latencies, updated_ips

# probe the closest networks/servers for a duration of time (denoted by period)
# every intvl time
def probe_closest(monitor, ips, period=600, intvl=60):
    start_time = time.time()
    cur_time = start_time
    all_data = {}
    updated_ips = ips
    # print(ips)
    updated_ips["server"] = ipinfo.host2ip(client_config.cdn_host)
    while (cur_time - start_time < period):
        cur_latencies, updated_ips = probe_ips(updated_ips)
        for ip in cur_latencies.keys():
            if ip not in all_data.keys():
                all_data[ip] = {}
            all_data[ip].update(cur_latencies[ip])
        if (time.time() < cur_time + intvl):
            time.sleep(cur_time + intvl - time.time())
        cur_time = time.time()

    num_of_tries = 0
    while (not report_probing(monitor, all_data)) and (num_of_tries < max_num_of_tries):
        num_of_tries += 1

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
    ips = {"network_31": ["195.113.161.65", "195.113.161.1"]}
    all_lats = probe_closest(monitor, ips, 10, 5)


