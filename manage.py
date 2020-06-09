# !/usr/bin/env python3

from flask import Flask, request ,jsonify
import flask_sqlalchemy import SQLAlchemy

api =Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Metric(db.Model):
    instance_id = db.Column(db.Integer,primary_key =True)
    hotstname = db.Column(db.String(100),unique=True)
    instance_type = db.Column(db.String(50))
    public_ipv4= db.Column(db.String(50),unique=True)
    cpuutilization=db.Column(db.Integer)
    diskusage=db.Column(db.Integer)
    disksize = db.Column(db.String(50))
    diskavail = db.Column(db.String(50))
    diskused = db.Column(db.String(50))
    memoryusage = db.Column(db.String(50))
    memoryutilized = db.Column(db.Integer)
    memorytotal = db.Column(db.String(50))
    memoryavail = db.Column(db.String(50))
    time = db.Column(db.String(50))

@app.route('/post/data', method = 'POST')
def data():
    request_json = request.json()
    metric =  Metric(instance_id = request_json["Metadata"]["instance-id"]),
                hostname = request_json["Metadata"]["hostname"],
                instance_type = request_json["Metadata"]["instance-type"],
                public_ipv4= request_json["Metadata"]["public-ipv4"],
                cpuutilization=request_json["CPUUtilization"]["CPUUtilization"]["Value"],
                diskusage= request_json["DiskUsage"]["Percentageused"],
                disksize = request_json["DiskUsage"]["Totalsize"],
                diskavail = request_json["DiskUsage"]["Avail"],
                diskused = request_json["DiskUsage"]["Used"],
                memoryusage = request_json["MemmoryUtilization"]["Mem_used"],
                memoryutilized = request_json["MemmoryUtilization"]["MemoryUtilized"]["Value"],
                memorytotal = request_json["MemmoryUtilization"]["Total_Mem"]
                memoryavail = request_json["MemmoryUtilization"]["Available_Mem"]
                time = request_json["Time"]
                )

    db.session.add(metric)
    db.session.commit()
    return({"Status":"Updated"})


 

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=6000)