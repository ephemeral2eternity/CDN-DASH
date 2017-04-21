# trace_cdn.py
# Chen Wang, Mar. 3, 2016
## chenw@cmu.edu
#### Report the route of the CDN video session to manager : http://manage.cmu-agens.com/verify
#### Pick up 10 nodes to do traceroute and get the verify agents
from monitor.get_hop_info import *
from monitor.probe_closest import *
from communication.comm_manager import *
from multiprocessing import freeze_support
from utils.logger import *
from utils.params import *
from client_config import *
from utils.test_utils import *

def monitor_agent(mode="TR"):
    ## Traceroute to the CDN to get the video session
    if mode != "RTT":
        route = get_route(cdn_host)
        print(route)
        success = report_route(monitor, route)
        logJson("TR_", route)

    if mode != "TR":
        ## Probe the closest server and networks.
        ips = get_probing_ips(monitor)
        latency_monitor = probe_closest(monitor, ips, period=monitor_period, intvl=monitor_intvl)
        logJson("RTT_", latency_monitor)

### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    if sys.platform == 'win32':
        freeze_support()

    if len(sys.argv) > 1:
        monitor_mode = sys.argv[1]
    else:
        monitor_mode = "TR"

    waitRandom(1, 300)

    monitor_agent(monitor_mode)