from communication.connect_locator import *
from client_utils import *
from communication.post_info import *

#manager = "manage.cmu-agens.com"
#geo_connected = connect_locator(manager, "geo")
#net_connected = connect_locator(manager, "net")
#print "Geo-connected locator: ", geo_connected
#print "Net-connected locator: ", net_connected

client_ip = "128.237.172.152"
# server_ip = "72.21.81.200"
server_ip = "192.16.48.200"
cdn_host = "az.cmu-agens.com"
locator = "40.121.147.110"
_, client_info = get_ext_ip()
client = client_info["name"]
cache_client_info(locator, client_info, server_ip, cdn_host)