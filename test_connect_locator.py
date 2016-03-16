from communication.connect_locator import *

manager = "manage.cmu-agens.com"
geo_connected = connect_locator(manager, "geo")
net_connected = connect_locator(manager, "net")
print "Geo-connected locator: ", geo_connected
print "Net-connected locator: ", net_connected