from communication.comm_manager import *
from communication.thread_wrapper import *
from monitor.get_hop_info import *
from multiprocessing import freeze_support, Queue
import trace_writer

### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    if sys.platform == 'win32':
        freeze_support()

    duration_to_probe = 30
    step = 10
    manager = "manage.cmu-agens.com"
    cdn = "az.cmu-agens.com"
    my_ip, _ = get_ext_ip()
    monitor = "monitor.cmu-agens.com"
    # monitor = "superman.andrew.cmu.edu:8000"

    csv_writer = trace_writer.initRTT()

    verify_agents = get_verify_agents(manager)
    ips_to_probe = [cdn]
    if verify_agents:
        ips_to_probe.append(verify_agents.keys())

    results = Queue()
    for i in range(duration_to_probe/step):
        time_start = time.time()
        procs = []

        for dst_ip in ips_to_probe:
            p = fork_probe_rtt(my_ip, dst_ip, results)
            procs.append(p)

        for p in procs:
            p.join()

        while not results.empty():
            try:
                rst = results.get()
                csv_writer.writerow(rst)
            except:
                print "Failed to write results to the csv file!"

        ### Add report rtt to monitor server.

        duration =  time.time() - time_start

        if duration < step:
            time.sleep(step - duration)

    trace_writer.out_rtt_trace.close()