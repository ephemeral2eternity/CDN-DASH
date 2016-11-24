from communication.comm_manager import *
from communication.thread_wrapper import *
from monitor.get_hop_info import *
from multiprocessing import freeze_support

### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    if sys.platform == 'win32':
        freeze_support()

    duration_to_probe = 600
    step = 5
    manager = "manage.cmu-agens.com"
    cdn = "az.cmu-agens.com"
    my_ip, _ = get_ext_ip()
    # monitor = "monitor.cmu-agens.com"
    monitor = "superman.andrew.cmu.edu:8000"

    verify_agents = get_verify_agents(manager)
    ips_to_probe = [cdn]
    if verify_agents:
        ips_to_probe.append(verify_agents.keys())

    for i in range(duration_to_probe/step):
        for dst_ip in ips_to_probe:
            p = fork_add_rtt(monitor, my_ip, dst_ip)
        time.sleep(step)



