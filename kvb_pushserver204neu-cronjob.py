#!/usr/bin/env python
# coding: utf-8

# In[29]:


import json
import time
import requests
import paho.mqtt.client as mqtt
from datetime import datetime

client = mqtt.Client('52dc166c-2en7-43c1-88ff-f80211c7a8f6','92.205.57.181')
server = "192.168.133.240"
url_get = 'https://www.vrs.de/index.php?eID=tx_vrsinfo_departuremonitor&i=7631f76d2d4a181120c4ff470ef4c856'
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
linie3 = []
linie13 = []
linie18 = []

def catchdata():
    linie3 = [ ]
    linie13 = [ ]
    linie18 = [ ]
    try:
        r = requests.get(url_get, headers=headers)
        r = json.loads(r.text)
        s  = json.dumps(r, indent = 4, sort_keys=True)
    except:
        print("Request failed!")
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    try:
        for i in range(0,len(r["events"])):
            AbfahrtIn = int((float(r["events"][i]["departure"]["timestamp"])-timestamp)/60)+1
            if AbfahrtIn <=59:
                if int(r["events"][i]["line"]["number"])==3:
                    linie3.append(AbfahrtIn)
                if int(r["events"][i]["line"]["number"])==13:
                    linie13.append(AbfahrtIn)
                if int(r["events"][i]["line"]["number"])==18:
                    linie18.append(AbfahrtIn)
    except:
        print("Reading events failed!")
    client.connect(server, 1883, 60)
    client.publish('linie3', '[]')
    if len(linie3)>0:
        client.publish('linie3', str(linie3))
    client.publish('linie13', '[]')
    if len(linie13)>0:
        client.publish('linie13', str(linie13))
    client.publish('linie18', '[]')
    if len(linie18)>0:
        client.publish('linie18', str(linie18))
    print(linie3)
    print(linie13)
    print(linie18)
    return
   
 
catchdata()
 