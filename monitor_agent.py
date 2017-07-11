# trace_cdn.py
# Chen Wang, Mar. 3, 2016
## chenw@cmu.edu
#### Report the route of the CDN video session to manager : http://manage.cmu-agens.com/verify
#### Pick up 10 nodes to do traceroute and get the verify agents
from monitor.get_hop_info import *
from monitor.probe_closest import *
from communication.comm_monitor import *
from multiprocessing import freeze_support
from utils.logger import *
from utils.params import *
from client_config import *
from ipinfo import ipinfo
from utils.test_utils import *

def route2ips(route):
    ips = []
    for hop_id in route.keys():
        if (int(hop_id) > 0) and (route[hop_id]["ip"] != "*") and (not ipinfo.is_reserved(route[hop_id]["ip"])):
            ips.append(route[hop_id]["ip"])
    return ips

def monitor_agent(period=3000, intvl=300):
    ## Traceroute to the CDN to get the video session
    start_ts = time.time()
    cur_ts = time.time()
    while cur_ts < start_ts + period:
        route = get_route(cdn_host)
        print("%d seconds passed after probing!" % (cur_ts - start_ts))
        print(route)
        success = report_route_to_monitor(monitor, route)
        logJson("_TR", route)
        pre_ts = cur_ts
        cur_ts = time.time()

        while cur_ts < pre_ts + intvl:
            ips = route2ips(route)
            lats = probe_ips(ips)
            logCSV("_RTT", lats)
            cur_ts = time.time()
    # latency_monitor = probe_closest(monitor, ips, period=monitor_period, intvl=monitor_intvl)
    # logJson("RTT_", latency_monitor)


### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    if sys.platform == 'win32':
        freeze_support()

    waitRandom(1, client_config.wait_time)
    monitor_agent()