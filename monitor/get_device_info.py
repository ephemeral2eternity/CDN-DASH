## Do Traceroute to a CDN host and gets detailed info on each hop.
# get_device_info.py
# Chen Wang, Oct. 23, 2015
# chenw@cmu.edu
import random

def get_device(dev_id=0):
    device_info = {}
    if dev_id == 1:
        device_info["device"] = "Desktop"
        device_info["os"] = "Microsoft Windows 10"
        device_info["browser"] = "Chrome"
        device_info["player"] = "v1.0"
    elif dev_id == 2:
        device_info["device"] = "Laptop"
        device_info["os"] = "Mac OS X"
        device_info["browser"] = "Safari"
        device_info["player"] = "v2.0"
    elif dev_id == 3:
        device_info["device"] = "TV"
        device_info["os"] = "Google TV"
        device_info["browser"] = "App"
        device_info["player"] = "v1.5"
    elif dev_id == 4:
        device_info["device"] = "Phone"
        device_info["os"] = "Android"
        device_info["browser"] = "App"
        device_info["player"] = "v2.0"
    elif dev_id == 5:
        device_info["device"] = "Tablet"
        device_info["os"] = "Apple iOS"
        device_info["browser"] = "App"
        device_info["player"] = "v1.2"
    else:
        device_info = get_random_device()
    return device_info


def get_random_device():
    device_info = {}
    device_types = ["Tablet", "Phone", "Laptop", "Desktop", "TV"]
    player_versions = ["v1.0", "v1.2", "v1.5", "v2.0"]
    device_info["device"] = random.choice(device_types)

    if (device_info["device"] == "Tablet") or (device_info["device"] == "Phone"):
        device_info["os"] = random.choice(["Android", "Apple iOS", "Microsoft Windows 10", "Amazon Fire OS"])
        device_info["browser"] = "app"
    elif (device_info["device"] == "Laptop") or (device_info["device"] == "Desktop"):
        device_info["os"] = random.choice(["Mac OS X", "Microsoft Windows 10", "Linux"])
        device_info["browser"] = random.choice(["Chrome", "Firefox", "IE"])
    else:
        device_info["os"] = random.choice(["Android TV", "Firefox OS", "Google TV", "Fire TV", "Apple TV OS"])
        device_info["browser"] = random.choice(["Chrome", "Firefox", "IE", "App"])

    device_info["player"] = random.choice(player_versions)

    return device_info