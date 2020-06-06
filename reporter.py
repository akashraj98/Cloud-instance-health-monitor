# !/usr/bin/env python

import sys, subprocess, json, os
import requests
import socket


def convert_to_json(res):
    return json.dump(res)

def disk_usage_mem():
    disklog = []
    df = subprocess.Popen(["df| grep -w / "], shell=True ,stdout=subprocess.PIPE)
    for line in df.stdout:
        splitline = line.decode().split()
        disklog.append(splitline)
    data = [disklog]
    return(data)

def get_metadata():
    url='http://169.254.169.254/latest/meta-data/'
    fileds=['instance-id' ,'instance-type' , 'public-ipv4', 'ami-id', 'hostname']
    res={}
    for field in fields:
        req= requests.get(url+field)
        res[field]=req.text()
    return json.dumps(res)

if __name__ == "__main__":
    path = '/'
    url = 'https://diskbot.cloudstuff.tech/post'
    log = disk_usage_mem()
    for disklog in log[0]:
        if path in disklog[5] and len(disklog[-1]) == 1:
            payload= {'hostname':socket.gethostname(),'mountPoint':disklog[-1],'totalsize':disklog[1],'used':disklog[2],
            'avail':disklog[3],'percentageused':disklog[4]}
            # r = requests.post(url, data=json.dumps(payload),headers={"Content-Type": "application/json"})#provide with url
            # print(r.text)
            print(payload)