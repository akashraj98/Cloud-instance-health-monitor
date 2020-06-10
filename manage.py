# !/usr/bin/env python3

from flask import Flask, request ,jsonify
import sqlite3
import json #not req

managerapp =Flask(__name__)

conn = sqlite3.connect("sqlite3.db" ,check_same_thread=False)

cursor= conn.cursor()
table = 'Report'

#Table is created
cursor.execute("DROP TABLE IF EXISTS Report;")
cursor.execute(f"CREATE TABLE {table} (INSTANCE_ID TEXT ,HOSTNAME TEXT,INSTANCE_TYPE TEXT,"
                "PUBLIC_IPV4 TEXT,CPUUTILIZATION REAL,DISKUTILIZATION INTEGER,DISKSIZE TEXT,"
                "DISKAVAIL TEXT,DISKUSED TEXT,MEMORYUSAGE TEXT , MEMORYUTILIZATION INTEGER,"
                "MEMORYTOTAL TEXT, MEMORYAVAIL TEXT, LOG_TIME TEXT );")

conn.commit()


@managerapp.route('/app/post/data', methods=["POST"])
def data():
    if request.method == 'POST':
        request_json = request.json
        
        #Parsing value from request
        instance_id = request_json["Metadata"]["instance-id"]
        hostname = request_json["Metadata"]["hostname"]
        instance_type =request_json["Metadata"]["instance-type"]
        public_ipv4= request_json["Metadata"]["public-ipv4"]
        cpuutilization=float(request_json["CPUUtilization"]["CPUUtilization"]["Value"])
        diskutilization= int(request_json["Diskutilization"]["Percentageused"])
        disksize = request_json["Diskutilization"]["Totalsize"]
        diskavail = request_json["Diskutilization"]["Avail"]
        diskused = request_json["Diskutilization"]["Used"]
        memoryusage = request_json["MemmoryUtilization"]["Mem_used"]
        memoryutilized = int(request_json["MemmoryUtilization"]["MemoryUtilized"]["Value"])
        memorytotal = request_json["MemmoryUtilization"]["Total_Mem"]
        memoryavail = request_json["MemmoryUtilization"]["Available_Mem"]
        log_time = request_json["Time"]

        with conn:
            cursor.execute("""INSERT INTO Report (INSTANCE_ID ,HOSTNAME ,INSTANCE_TYPE ,
                        PUBLIC_IPV4 ,CPUUTILIZATION ,DISKUTILIZATION ,DISKSIZE,  
                        DISKAVAIL ,DISKUSED ,MEMORYUSAGE , MEMORYUTILIZATION ,
                        MEMORYTOTAL, MEMORYAVAIL , LOG_TIME ) SELECT(?),
                        (?),(?),(?),(?),(?), (?),(?),(?),(?),(?),(?), (?),
                        (?) WHERE NOT EXISTS(SELECT * FROM Report  
                        WHERE INSTANCE_ID=?)""",(instance_id,hostname,instance_type, \
                        public_ipv4,cpuutilization,diskutilization,disksize,diskavail,\
                        diskused,memoryusage,memoryutilized,memorytotal,memoryavail,\
                        log_time,instance_id))

        return jsonify({"Status":"Sucessfully recieved"})



if __name__ == '__main__':
    managerapp.run(host='0.0.0.0', port=6000)