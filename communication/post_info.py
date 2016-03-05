import urllib2
import json
import os
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

def updateRoute(locator, client_ip, srv_ip):
    url = "http://%s/locator/exist?client=%s&server=%s" % (locator, client_ip, srv_ip)

    isRouteUpdated = True
    try:
        response = urllib2.urlopen(url)
        if response == "Yes":
            isRouteUpdated = True
        else:
            isRouteUpdated = False
    except:
        isRouteUpdated = False

    return isRouteUpdated


def cache_client_info(locator, client_info, srv_ip):
    client_info['server'] = srv_ip
    client_ip = client_info['ip']
    isRouteCached = checkRouteCached(locator, client_ip, srv_ip)

    if not isRouteCached:
        cdnHops = get_hop_by_host(srv_ip)
        srv_info = get_node_info(srv_ip)
        cdnHops.append(srv_info)
        client_info['route'] = cdnHops

        # route_str = route2str(cdnHops)
        # print route_str
        isSuccess = False
        tries = 0
        while (tries < 3) and (not isSuccess):
            isSuccess = report_route(locator, client_info)
            tries += 1

def fork_cache_client_info(locator, client_info, srv_ip):
    tr_process = os.fork()
    if tr_process == 0:
        print "We are in the child process has PID = %d running the traceroute and client info reporting!" % os.getpid()
        cache_client_info(locator, client_info, srv_ip)
    else:
        print "We are in the parent process and out child process has PID = %d running dash streaming!" % os.getpid()


def route2str(full_route):
    route_list = []
    for node in full_route:
        route_list.append(node['ip'])

    route_str = ','.join(str(e) for e in route_list)
    return route_str

