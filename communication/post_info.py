import urllib2
import json
import os
from multiprocessing import Process, freeze_support
from monitor.get_hop_info import *

def report_route(locator, client_info):
    url = "http://%s/locator/add" % locator

    isSuccess = True
    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(client_info))
    except:
        isSuccess = False

    return isSuccess

def checkRouteCached(locator, client_ip, srv_ip):
    url = "http://%s/locator/exist?client=%s&server=%s" % (locator, client_ip, srv_ip)

    isRouteCached = True
    try:
        response = urllib2.urlopen(url)
        client_info = json.load(response)
        if client_info['ip'] == client_ip:
            isRouteCached = True
        else:
            isRouteCached = False
    except:
        isRouteCached = False

    return isRouteCached

def updateRoute(locator, client_ip, srv_ip, qoe):
    url = "http://%s/locator/update?client=%s&server=%s&qoe=%f" % (locator, client_ip, srv_ip, qoe)

    isRouteUpdated = True
    try:
        response = urllib2.urlopen(url)
        response_str = response.read()
        if response_str == "Yes":
            isRouteUpdated = True
        else:
            isRouteUpdated = False
    except:
        isRouteUpdated = False

    return isRouteUpdated


def cache_client_info(locator, client_info, srv_ip, cdn_host):
    client_info['server'] = srv_ip
    client_ip = client_info['ip']
    # isRouteCached = checkRouteCached(locator, client_ip, srv_ip)

    # if not isRouteCached:
    cdnHops = get_hop_by_host(srv_ip)
    srv_info = get_node_info(srv_ip)
    if cdnHops[-1]['ip'] != srv_info['ip']:
        cdnHops.append(srv_info)
    cdnHops[-1]['name'] = cdn_host

    client_info['route'] = cdnHops

    outJsonFileName = os.getcwd() + "/dataQoE/" + client_info['name'] + "-" + client_info['server'] + ".json"
    with open(outJsonFileName, 'wb') as f:
        json.dump(client_info, f)

    # route_str = route2str(cdnHops)
    # print route_str
    isSuccess = False
    tries = 0
    while (tries < 3) and (not isSuccess):
        isSuccess = report_route(locator, client_info)
        tries += 1

    if isSuccess:
        print "Successfully report route from client ", client_ip, " to server ", srv_ip, " to the anomaly locator " \
                , "agent ", locator
    else:
        print "Failed to report route to anomaly locator agent:", locator

    # else:
    #    print "Route from client ", client_ip, " to server ", srv_ip, " is cached in the anomaly locator!"


def locate_anomaly(locator, client_ip, srv_ip, qoe):
    url = "http://%s/locator/locate?client=%s&server=%s&qoe=%.3f" % (locator, client_ip, srv_ip, qoe)

    anomaly_info = {}
    try:
        response = urllib2.urlopen(url)
        response_str = response.read()
        anomaly_info = json.loads(response_str)
        print "Located anomaly info:", anomaly_info
    except:
        print "Failed to locate the anomaly for streaming session from client ", client_ip, " to server ", srv_ip
    return anomaly_info


def fork_cache_client_info(locator, client_info, srv_ip, cdn_host):
    p = Process(target=cache_client_info, args=(locator, client_info, srv_ip, cdn_host))
    p.start()
    return p

def fork_locate_anomaly(locator, client_ip, srv_ip, qoe):
    p = Process(target=locate_anomaly, args=(locator, client_ip, srv_ip, qoe))
    p.start()
    return p


def route2str(full_route):
    route_list = []
    for node in full_route:
        route_list.append(node['ip'])

    route_str = ','.join(str(e) for e in route_list)
    return route_str

if __name__ == '__main__':
    client_ip = "128.2.57.73"
    server_ip = "72.21.81.200"
    locator = "40.121.147.110"
    #client_ip, client_info = get_ext_ip()
    #client = client_info["name"]
    #cache_client_info(locator, client_info, srv_ip)
    qoe = 3.5
    # anomaly_info = locate_anomaly(locator, client_ip, server_ip, qoe)
    isUpdated = updateRoute(locator, client_ip, server_ip, qoe)
    print isUpdated
    #isUpdated = updateRoute(locator, client_ip, srv2_ip, qoe)
    #print isUpdated
    qoe = 0.5
    client_ip = "128.237.191.151"
    anomaly_info = locate_anomaly(locator, client_ip, server_ip, qoe)
    # anomaly_info = locate_anomaly(locator, client_ip, srv2_ip, qoe)