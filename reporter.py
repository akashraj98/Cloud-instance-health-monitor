# !/usr/bin/python3

import sys, subprocess, json, os 
import requests
from datetime import datetime
import socket


def convert_to_json(res):
    return json.dumps(res)

def disk_usage_mem(interval = None):
    df = subprocess.Popen(["df -h| grep -w / "], shell=True ,stdout=subprocess.PIPE)
    out,err = df.communicate()
    payload= {'hostname':socket.gethostname(),'mountPoint':disklog[-1],'totalsize':disklog[1],'used':disklog[2],
            'avail':disklog[3],'percentageused':disklog[4]}
    payload['time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
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
    payload['time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return convert_to_json(payload)

def CPUUtilization():
    cpu = subprocess.Popen(["sar| grep Average "], shell=True ,stdout=subprocess.PIPE)
    out,err = cpu.communicate()
    cpu = out.decode().split()
    cpu_usage = 100 - float(cpu[-1])
    payload ={'CPUUtilization': str(round(cpu_usage,2)) + ' %'}
    payload['time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return convert_to_json(payload)




if __name__ == "__main__":
    path = '/'
    url = 'https://diskbot.cloudstuff.tech/post'
    log = CPUUtilization()
            # r = requests.post(url, data=json.dumps(payload),headers={"Content-Type": "application/json"})#provide with url
            # print(r.text)
    print(log)