# Cloud Monitoring


Cloud Monitoring Application Consists of two main scripts Reorter[reporter.py] and Manager[manage.py]

  - This application can be use to monitor different instances running on cloud and send atomated emails if something went wrong on any instance

### Reporter


  - Reporter is the  script that is run on each instance and collect data 
  - Data collected by reporter 
    - CPUUtilization
    - DiskActivity
    - MemmoryUtilization
    - DiskUsage
    - NetworkActivity
    - MetaData

Reporter keep sending data to Monitor through a post request which can be use to monitor instance

The data collected by reported is exposed by endpoints:
  - Available Endpoints
    - GET
      -  /get/metrics : Returns all metrics data
      ```
      {
              "CPUUtilization": {
                  "CPUUtilization": {
                      "Unit": "percentage",
                      "Value": "1.96"
                  },
                  "Time": "2020-06-16 19:32:16"
              },
              "DiskActivity": {
                  "BytesRead/s": "3.09",
                  "BytesWrite/s": "11.03",
                  "ReadTransections/s": "0.41",
                  "Time": "2020-06-16 19:32:16",
                  "TotalTransections/s": "3.50",
                  "WriteTransections/s": "0.41"
              },
              "Diskutilization": {
                  "Avail": "6.6G",
                  "Hostname": "ip-172-31-43-219.ap-south-1.compute.internal",
                  "MountPoint": "/",
                  "Percentageused": "19",
                  "Time": "2020-06-16 19:32:16",
                  "Totalsize": "8.0G",
                  "Used": "1.5G"
              },
              "MemmoryUtilization": {
                  "Available_Mem": "597M",
                  "Mem_used": "231M",
                  "MemoryUtilized": {
                      "Unit": "percentage",
                      "Value": "39"
                  },
                  "Time": "2020-06-16 19:32:16",
                  "Total_Mem": "983M"
              },
              "Metadata": {
                  "ami-id": "ami-0447a12f28fddb066",
                  "hostname": "ip-172-31-43-219.ap-south-1.compute.internal",
                  "instance-id": "i-08e80892f2cb506cd",
                  "instance-type": "t2.micro",
                  "public-ipv4": "13.126.53.116"
              },
              "NetworkActivity": {
                  "Time": "2020-06-16 19:32:16",
                  "rxkB/s": "32.85",
                  "rxpck/s": "28.54",
                  "txkB/s": "4.28",
                  "txpck/s": "10.98"
              },
              "Time": "2020-06-16 19:32:16"
          }
      ```
      -  /get/graph
        Can be use to make graph of a perticular metrics
        Query parameter to pass
          - interval = seconds
          - metric = name of metric

      - /get/metadata
Returns all  metadata about the instance
    -  /update/status
    Can be use to stop or resume the reporter app
     Query parameter to pass
        - status = {pause,resume,stop}
    - /update/interval
    Update the time after which the the reporter sends post request to manager
    
    

#### Testing Instance

By default, the Replorter app will use port 5000, 

```sh
http://13.126.53.116:5000/get/metadata
```

## Manager
 - Manager will recives post request from all the reporter running on different instance
 - Maintain record of every instance in a databse
  - Checks different metrics and sends notification to the user in form of email or slack message.
    - CPUCheck 
    - MemoryCheck
    - DiskCheck
 - Available Endpoints
    - POST
        - /app/post/data
        Data is sent to this endpoint in json format
