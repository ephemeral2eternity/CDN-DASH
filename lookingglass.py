import requests
from bs4 import BeautifulSoup
import json
import os

def looking_glass(url, host_name, cmd="T4", loc="jfk02"):
    post_data = {"FKT": "go!", "CMD": cmd, "LOC": loc, "DST": host_name}

    rsp = requests.post(url, data=post_data)
    soup = BeautifulSoup(rsp.text, 'html.parser')
    print(soup.prettify())
    data = soup.pre.contents
    print(data)
    return data[0]

### Connect to the manager to obtain the verfification agents to ping
if __name__ == '__main__':
    host_name = "az.cmu-agens.com"
    cogent_cmds = ["P4", "P6", "T4", "T6", "BGP"]
    cogent_locs = {
        "AT - Vienna":"vie01",
        "BE - Brussels":"bru01",
        "BG - Sofia":"sof02",
        "CA - Montreal":"ymq01",
        "CA - Toronto":"yyz01",
        "CH - Zurich":"zrh01",
        "DE - Berlin":"ber01",
        "DE - Dusseldorf":"dus01",
        "DE - Frankfurt":"fra03",
        "DE - Hamburg":"ham01",
        "DE - Munich":"muc03",
        "DE - Nuremberg":"nue01",
        "DK - Copenhagen":"cph01",
        "EE - Tallinn":"tll01",
        "ES - Barcelona":"bcn01",
        "ES - Madrid":"mad05",
        "ES - Valencia":"vlc02",
        "FR - Bordeaux":"bod01",
        "FR - Marseille":"mrs01",
        "FR - Paris":"par01",
        "GB - London":"lon13",
        "GB - Southport":"lpl01",
        "GR - Athens":"ath01",
        "HK - Hong Kong":"hkg02",
        "HU - Budapest":"bud01",
        "IE - Dublin":"dub01",
        "IT - Milan":"mil01",
        "IT - Rome":"rom01",
        "JP - Tokyo":"tyo01",
        "MX - Mexico City":"mex01",
        "NL - Amsterdam":"ams04",
        "NO - Oslo":"osl01",
        "PL - Warsaw":"waw01",
        "PT - Lisbon":"lis01",
        "RO - Bucharest":"buh01",
        "SE - Stockholm":"sto03",
        "SG - Singapore":"sin01",
        "SK - Bratislava":"bts01",
        "UA - Kharkiv":"hrk01",
        "US - Atlanta":"atl01",
        "US - Boston":"bos01",
        "US - Chicago":"ord01",
        "US - Dallas":"dfw01",
        "US - Denver":"den01",
        "US - Houston":"iah01",
        "US - Jacksonville":"jax01",
        "US - Kansas City": "mci01",
        "US - Los Angeles": "lax01",
        "US - Miami":"mia01",
        "US - Minneapolis":"msp01",
        "US - New York":"jfk02",
        "US - Orlando":"mco01",
        "US - Philadelphia":"phl01",
        "US - Sacramento":"smf01",
        "US - San Diego":"san01",
        "US - San Francisco":"sfo01",
        "US - San Jose":"sjc01",
        "US - Seattle":"sea01",
        "US - Tampa":"tpa01",
        "US - Washington, DC":"dca01"
    }

    cogent_url = "http://www.cogentco.com/lookingglass.php"
    # ntt_url = "https://ssp.pme.gin.ntt.net/lg/lg.cgi"

    all_tr_data = {}
    for loc_name, loc_code in cogent_locs.iteritems():
        print(loc_name)
        t4_str = looking_glass(cogent_url, host_name, loc=loc_code)
        print(t4_str)
        all_tr_data[loc_name] = t4_str


    with open(os.getcwd() + "\\routeData\\cogent_tr_20170501.json", "w") as f:
        json.dump(all_tr_data, f, indent=4, sort_keys=True)