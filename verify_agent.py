from communication.comm_manager import *
from communication.thread_wrapper import *
from monitor.get_hop_info import *
from multiprocessing import freeze_support
from utils.client_utils import *
import client_config
import csv


### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    if sys.platform == 'win32':
        freeze_support()

    client_name = getMyName()
    cur_ts = time.strftime("%m%d%H%M%S")
    client_ID = client_name + "_" + cur_ts
    rtt_trace_file = client_ID  + "_rtt.csv"
    out_rtt_trace = open(client_config.csv_trace_folder + rtt_trace_file, 'wb')
    rtt_csv_writer = csv.DictWriter(out_rtt_trace, fieldnames=client_config.rtt_trace_fields)
    rtt_csv_writer.writeheader()

    my_ip, _ = get_ext_ip()
    verify_agents = get_verify_agents(client_config.manager)
    ips_to_probe = [client_config.cdn_host]
    if verify_agents:
        ips_to_probe.append(verify_agents.keys())

    print verify_agents

    for i in range(client_config.duration_to_probe/client_config.probe_step):
        time_start = time.time()
        procs = []

        for dst_ip in ips_to_probe:
            p = fork_probe_rtt(my_ip, dst_ip, rtt_csv_writer)
            procs.append(p)

        for p in procs:
            p.join()

        ### Add report rtt to monitor server.

        duration =  time.time() - time_start

        if duration < client_config.probe_step:
            time.sleep(client_config.probe_step - duration)

    out_rtt_trace.close()