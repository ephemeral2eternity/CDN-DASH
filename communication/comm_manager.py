import urllib2
import json


############################################################################
# Report the route information to the centralized manager
# Centralized manager: manage.cmu-agens.com
# Client info: client_info
#############################################################################
def report_route_to_manager(manager, client_info):
    ## Debug URL
    url = "http://%s/nodeinfo/add" % manager
    isSuccess = True
    try:
        req = urllib2.Request(url)
        req.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(req, json.dumps(client_info))
        print(response)
    except:
        isSuccess = False

    return isSuccess