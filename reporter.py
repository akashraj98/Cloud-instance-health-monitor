# !/usr/bin/python3

import sys, subprocess, json, os 
import requests
from datetime import datetime
import socket


def convert_to_json(res):
    return json.dumps(res)

def disk_usage_mem(interval = None):
    Disk = subprocess.Popen(["df -h| grep -w / "], shell=True ,stdout=subprocess.PIPE)
    out,err = Disk.communicate()
    payload= {'Hostname':socket.gethostname(),'MountPoint':disklog[-1],'Totalsize':disklog[1],
                'Used':disklog[2],'Avail':disklog[3],'Percentageused':disklog[4]}
    payload['Time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    disklog = out.decode().split()
    # if interval:
    #     threading.Timer(interval,disk_usage_mem).start()
    print(payload)
    return convert_to_json(payload)

def get_metadata():
    url='http://169.254.169.254/latest/meta-data/'
    fields=['instance-id' ,'instance-type' , 'public-ipv4', 'ami-id', 'hostname']
    res={}
    for field in fields:
        req= requests.get(url+field)
        res[field]=req.content.decode()
    return json.dumps(res)

def get_mem_usage():
    mem = subprocess.Popen(["free -h| grep Mem "], shell=True ,stdout=subprocess.PIPE)
    out,err = mem.communicate()
    mem = out.decode().split()
    MemUtilization_per = int(((int(mem[1][:-1])-int(mem[-1][:-1]))/int(mem[1][:-1]))*100)
    payload = {'Total_Mem':mem[1],'MemoryUtilized':str(MemUtilization_per)+' %',
                'Available_Mem':mem[-1],'Mem_used':mem[2]}
    payload['Time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return convert_to_json(payload)

def CPUUtilization():
    cpu = subprocess.Popen(["sar| grep Average "], shell=True ,stdout=subprocess.PIPE)
    out,err = cpu.communicate()
    cpu = out.decode().split()
    cpu_usage = 100 - float(cpu[-1])
    payload ={'CPUUtilization': str(round(cpu_usage,2)) + ' %'}
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return convert_to_json(payload)

def NetworkActivity():
    net = subprocess.Popen(["sar -n DEV| grep Average | grep eth0"], shell=True ,stdout=subprocess.PIPE)
    out,err = net.communicate()
    net = out.decode().split()
    payload = {'rxpck/2':net[2],'txpck/s':net[3],'rxkB/s':net[4],'txkB/s':net[5]}
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return convert_to_json(payload)

def NetworkStatus():
    net_status = subprocess.Popen(["ping -c 1 -q google.com >&/dev/null; echo $?"], shell=True \
                    ,stdout=subprocess.PIPE)
    out,err = net_status.communicate()
    net_status = out.decode().strip()
    status = 'Connected'
    if net_status != '0':
        status = 'Disconnected'
    payload = {'NetworkStatus': status , 'Hostname':socket.gethostname()}
    return convert_to_json(payload)

def DiskActivity():
    DiskOps = subprocess.Popen(["sar -b | grep Average"], shell=True ,stdout=subprocess.PIPE)
    out,err = DiskOps.communicate()
    DiskOps = out.decode().split()
    payload = {'TotalTransections/s':DiskOps[1], 'WriteTransections/s':DiskOps[2],
                'ReadTransections/s':DiskOps[2] ,'BytesRead/s':DiskOps[3], 'BytesWrite/s':DiskOps[4]}
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return convert_to_json(payload)

if __name__ == "__main__":
    path = '/'
    url = 'https://diskbot.cloudstuff.tech/post'
    log = DiskActivity()
            # r = requests.post(url, data=json.dumps(payload),headers={"Content-Type": "application/json"})#provide with url
            # print(r.text)
    print(log)