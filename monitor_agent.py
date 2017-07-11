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
        if (int(hop_id) > 0) and (route[hop_id]["ip"] != "*"):
            ips.append(route[hop_id]["ip"])
    return ips

def monitor_agent():
    ## Traceroute to the CDN to get the video session
    start_ts = time.time()
    route = get_route(cdn_host)
    print(route)
    success = report_route_to_monitor(monitor, route)
    logJson("TR_", route)
    duration = time.time() - start_ts
    print("The total time to obtain traceroute from the CDN is: %.2f seconds!" % duration)



    ## Probe the closest server and networks.
    start_ts = time.time()
    ips = route2ips(route)
    lats = probe_ips(ips)
    logCSV("RTT_", lats)
    duration = time.time() - start_ts
    print("The total time to probe all ips in the route is: %.2f seconds!" % duration)
    # latency_monitor = probe_closest(monitor, ips, period=monitor_period, intvl=monitor_intvl)
    # logJson("RTT_", latency_monitor)


### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    if sys.platform == 'win32':
        freeze_support()

    if len(sys.argv) > 1:
        monitor_mode = sys.argv[1]
    else:
        monitor_mode = "TR"

    # waitRandom(1, 300)
    monitor_agent()