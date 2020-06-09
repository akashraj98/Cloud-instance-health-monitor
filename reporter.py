# !/usr/bin/python3

import sys, subprocess, json, os , time
import requests
from datetime import datetime
from flask import Flask, request ,jsonify


def DiskUsage():
    Disk = subprocess.Popen(["df -h| grep -w / "], shell=True ,stdout=subprocess.PIPE)
    out,err = Disk.communicate()
    disklog = out.decode().split()
    payload= {'MountPoint':disklog[-1],'Totalsize':disklog[1],
                'Used':disklog[2],'Avail':disklog[3],'Percentageused':disklog[4][:-1]}
    Hostname = requests.get('http://169.254.169.254/latest/meta-data/hostname')
    payload['Hostname']= Hostname.content.decode()
    payload['Time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return(payload)


def Metadata():
    url='http://169.254.169.254/latest/meta-data/'
    fields=['instance-id' ,'instance-type' , 'public-ipv4', 'ami-id', 'hostname']
    res={}
    for field in fields:
        req= requests.get(url+field)
        res[field]=str(req.content.decode())
    return res


def MemmoryUtilization():
    mem = subprocess.Popen(["free -h| grep Mem "], shell=True ,stdout=subprocess.PIPE)
    out,err = mem.communicate()
    mem = out.decode().split()
    MemUtilization_per = int(((int(mem[1][:-1])-int(mem[-1][:-1]))/int(mem[1][:-1]))*100)
    payload = {'Total_Mem':mem[1],'MemoryUtilized':{'Value': str(MemUtilization_per) , 'Unit' : 'percentage'},
                'Available_Mem':mem[-1],'Mem_used':mem[2]}
    payload['Time']= datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    return(payload)


def CPUUtilization():
    cpu = subprocess.Popen(["sar| grep Average "], shell=True ,stdout=subprocess.PIPE)
    out,err = cpu.communicate()
    cpu = out.decode().split()
    cpu_usage = 100 - float(cpu[-1])
    payload ={'CPUUtilization':{'Value': str(round(cpu_usage,2)) , 'Unit' : 'percentage'}  }
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return(payload)


def NetworkActivity():
    net = subprocess.Popen(["sar -n DEV| grep Average | grep eth0"], shell=True ,stdout=subprocess.PIPE)
    out,err = net.communicate()
    net = out.decode().split()
    payload = {'rxpck/s':net[2],'txpck/s':net[3],'rxkB/s':net[4],'txkB/s':net[5]}
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return(payload)


def NetworkStatus():
    net_status = subprocess.Popen(["ping -c 1 -q google.com >&/dev/null; echo $?"], shell=True \
                    ,stdout=subprocess.PIPE)
    out,err = net_status.communicate()
    net_status = out.decode().strip()
    status = 'Connected'
    if net_status != '0':
        status = 'Disconnected'
    payload = {'NetworkStatus': status , 'Hostname':socket.gethostname()}
    return(payload)


def DiskActivity():
    DiskOps = subprocess.Popen(["sar -b | grep Average"], shell=True ,stdout=subprocess.PIPE)
    out,err = DiskOps.communicate()
    DiskOps = out.decode().split()
    payload = {'TotalTransections/s':DiskOps[1], 'WriteTransections/s':DiskOps[2],
                'ReadTransections/s':DiskOps[2] ,'BytesRead/s':DiskOps[3], 'BytesWrite/s':DiskOps[4]}
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return(payload)

    # routes

app = Flask(__name__)

@app.route('/get/metadata')
def metadata():
    data =Metadata()
    return jsonify(data)

@app.route('/')
def index():
    return "Hey there!"

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route('/get/metrics')
def metrics():
    payload = {'CPUUtilization': CPUUtilization(),'DiskActivity':DiskActivity(),'MemmoryUtilization':MemmoryUtilization(),
                'DiskUsage':DiskUsage(),'NetworkActivity':NetworkActivity(),'Metadata':Metadata()}
    payload['Time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    return jsonify(payload)

@app.route('/get/graph')
def graph():
    interval = request.args.get('interval')
    metric_name = request.args.get('metric')
    Metrics = ['CPUUtilization','DiskActivity','MemmoryUtilization',
                'DiskUsage','NetworkActivity']
    No_of_Execution=3   # Default value 3
    # if No_of_Execution is None:
    #     No_of_Execution = 3
    payload={"Datapoints":[]}
    payload["Label"]=metric_name
    if metric_name in Metrics:
        for i in range(No_of_Execution):
            Datapoint=globals()[metric_name]()
            payload["Datapoints"].append(Datapoint)
            time.sleep(int(interval))              #query  parametr is always string 

    return jsonify(payload)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
    # log = metadata()
    # print(type(log))      # for testing functions