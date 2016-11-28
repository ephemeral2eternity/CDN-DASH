import csv
import os
import client_config

def initFolder():
    global csv_trace_folder
    ## ==================================================================================================
    # Trace file to write QoE and other parameters, etc.
    ## ==================================================================================================
    csv_trace_folder = os.getcwd() + "/dataQoE/"

    try:
        os.stat(csv_trace_folder)
    except:
        os.mkdir(csv_trace_folder)

    client_config.init()


def initQoE():
    global qoe_trace_file, qoe_trace_fields, out_qoe_trace

    initFolder()

    qoe_trace_fields = ["TS", "Buffer", "Freezing", "QoE1", "QoE2", "Representation", "Response", "Server", "ChunkID"]

    qoe_trace_file = client_config.client_ID  + "_QoE.csv"
    out_qoe_trace = open(csv_trace_folder + qoe_trace_file, 'wb')
    qoe_csv_writer = csv.DictWriter(out_qoe_trace, fieldnames=qoe_trace_fields)
    qoe_csv_writer.writeheader()
    return qoe_csv_writer


def initRTT():
    global rtt_trace_file, rtt_trace_fields, out_rtt_trace

    initFolder()
    rtt_trace_fields = ["TS", "src", "dst", "rtt"]

    rtt_trace_file = client_config.client_ID  + "_rtt.csv"
    out_rtt_trace = open(csv_trace_folder + rtt_trace_file, 'wb')
    rtt_csv_writer = csv.DictWriter(out_rtt_trace, fieldnames=rtt_trace_fields)
    rtt_csv_writer.writeheader()

    return rtt_csv_writer

