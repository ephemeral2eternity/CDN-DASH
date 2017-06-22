## An emlator of DASH streaming in Python

#### by Chen Wang, chenw@cmu.edu

1. Test DASH video streaming in Python from a CDN URL
  * Sample CDN url: http://az.cmu-agens.com
  * Sample Video ID:
    - BBB: http://az.cmu-agens.com/demo.html?vidID=BBB
    - ToS: http://az.cmu-agens.com/demo.html?vidID=ToS
    - st: http://az.cmu-agens.com/demo.html?vidID=st

2. Usage
  * DASH Client to stream videos from a CDN url
    - `python test_cdn_client.py cdn_url video_name`
  * QRank DASH Client with QoE Anomaly Identification reported to Cloud agent: qrank.cmu-agens.com
    - `python CDN-DASH/test_qdiag_client_agent.py`
    - Configure monitor agent, cloud agent and manager agent in client_config.py

3. Requirements
  * System libraries required:
    - `sudo apt-get install traceroute`
    - `sudo apt-get install python-pip`
  * Python libraries required: requirements.txt
