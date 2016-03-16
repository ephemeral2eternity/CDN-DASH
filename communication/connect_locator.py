import urllib2
import json
import os
import socket
from ipinfo.ipinfo import *
from monitor.ping import *

# Get the list of all locators
def get_locators(manager):
    url = "http://%s/getJsonData/" % manager

    locators = []
    try:
        req = urllib2.Request(url)
        response = urllib2.urlopen(req)
        data = json.load(response)
        locators = data['data']
    except:
        print "Failed to get the list of locator agents! Please initialize the locator list on the manager!"

    return locators

def get_geo_dist(coord1, coord2):
    geo_dist_squre = (coord2[0] - coord1[0])**2 + (coord2[1] - coord1[1])**2
    geo_dist = geo_dist_squre ** 0.5
    return geo_dist


def geo_connect(client_info, locators):
    client_coords = [float(client_info['latitude']), float(client_info['longitude'])]
    geo_dist_dict = {}
    locator_ips = {}
    for node in locators:
        node_name = node['name']
        node_ip = node['ip']
        locator_ips[node_name] = node_ip
        node_geo_dist = get_geo_dist(client_coords, [float(node['lat']), float(node['lon'])])
        geo_dist_dict[node_name] = node_geo_dist

    connected_locator = min(geo_dist_dict.items(), key=lambda x:x[1])[0]
    connected_locator_ip = locator_ips[connected_locator]
    return connected_locator, connected_locator_ip

def net_connect(locators):
    net_dist_dict = {}
    locator_ips = {}
    for node in locators:
        node_name = node['name']
        node_ip = node['ip']
        locator_ips[node_name] = node_ip
        rtt = getMnRTT(node_ip)
        net_dist_dict[node_name] = rtt

    connected_locator = min(net_dist_dict.items(), key=lambda x:x[1])[0]
    connected_locator_ip = locator_ips[connected_locator]
    return connected_locator, connected_locator_ip


def notify_manager(manager, method, client_info):
    url = "http://%s/client/add?method=%s" % (manager, method)
    isSuccess = True
    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(client_info))
    except:
        isSuccess = False

    return isSuccess


def connect_locator(manager, method="geo"):
    locators = get_locators(manager)
    client_info = ipinfo()
    if "No" in client_info['hostname']:
        client_info['hostanme'] = socket.gethostname()

    if method == "geo":
        connected_locator, connected_locator_ip = geo_connect(client_info, locators)
    elif method == "net":
        connected_locator, connected_locator_ip = net_connect(locators)
    else:
        print "Unknown method to connect to a locator!"
        return None
    ## Post the info the the centralized manager
    client_info['locator'] = connected_locator

    num_tries = 0
    while (not notify_manager(manager, method, client_info)) and (num_tries < 3):
        num_tries += 1

    if num_tries == 3:
        print "Try to notify the manager 3 times but all failed."

    return {'name' : connected_locator, 'ip' : connected_locator_ip}

if __name__ == '__main__':
    manager = "manage.cmu-agens.com"
    geo_connected = connect_locator(manager, "geo")
    net_connected = connect_locator(manager, "net")
    print "Geo-connected locator: ", geo_connected
    print "Net-connected locator: ", net_connected

