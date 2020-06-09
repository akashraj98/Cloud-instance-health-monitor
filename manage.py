# !/usr/bin/env python3

from flask import Flask, request ,jsonify
import sqlite3

managerapp =Flask(__name__)

conn = sqlite3.connect("sqlite3.db")

cursor= conn.cursor()
table = 'Report'

#Table is created
cursor.execute(f"CREATE TABLE IF NOT EXISTS {table} (INSTANCE_ID TEXT ,HOSTNAME TEXT,INSTANCE_TYPE TEXT,\
                PUBLIC_IPV4 TEXT,CPUUTILIZATION INTEGER,DISKUTILIZATION INTEGER,DISKSIZE TEXT \
                DISKAVAIL TEXT,DISKUSED TEXT,MEMORYUSAGE TEXT , MEMORYUTILIZATION INTEGER \
                MEMORYTOTAL TEXT, MEMORYAVAIL TEXT, LOG_TIME TEXT );")

conn.commit()
conn.close()

@managerapp.route('/app/post/data', methods=["POST"])
def data():
    if request.method == 'POST':
        json_request = request.json()
        
        #Parsing value from request
        instance_id = request_json["Metadata"]["instance-id"],
        hostname = request_json["Metadata"]["hostname"],
        instance_type = request_json["Metadata"]["instance-type"],
        public_ipv4= request_json["Metadata"]["public-ipv4"],
        cpuutilization=request_json["CPUUtilization"]["CPUUtilization"]["Value"],
        diskutilization= request_json["Diskutilization"]["Percentageused"],
        disksize = request_json["Diskutilization"]["Totalsize"],
        diskavail = request_json["Diskutilization"]["Avail"],
        diskused = request_json["Diskutilization"]["Used"],
        memoryusage = request_json["MemmoryUtilization"]["Mem_used"],
        memoryutilized = request_json["MemmoryUtilization"]["MemoryUtilized"]["Value"],
        memorytotal = request_json["MemmoryUtilization"]["Total_Mem"],
        memoryavail = request_json["MemmoryUtilization"]["Available_Mem"],
        log_time = request_json["Time"] 
        c = conn.cursor()

        c.execute(f"INSERT INTO {table} (INSTANCE_ID ,HOSTNAME ,INSTANCE_TYPE ,\
                    PUBLIC_IPV4 ,CPUUTILIZATION ,DISKUTILIZATION ,DISKSIZE  \
                    DISKAVAIL ,DISKUSED ,MEMORYUSAGE , MEMORYUTILIZATION \
                    MEMORYTOTAL, MEMORYAVAIL , LOG_TIME ) SELECT({instance_id}),\
                    ({hostname}),({instance_type}),({public_ipv4}),({cpuutilization}),\
                    ({diskutilization}), ({disksize}),({diskavail}),({diskused}), \
                    ({memoryusage}),({memoryutilized}),({memorytotal}), ({memoryavail}),\
                    ({log_time}) WHERE NOT EXISTS(SELECT * FROM {table}  \
                    WHERE INSTANCE_ID=({instance_id}));")
        conn.commit()
        conn.close()
        return jsonify({"Status":"Sucessfully recieved"})



if __name__ == '__main__':
    managerapp.run(host='0.0.0.0', port=6000)