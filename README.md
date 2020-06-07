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


The data collected by reported is exposed by endpoints:
  - Available Endpoints
    - GET
      -  /get/metrics : Returns all metrics data
      -  /get/graph
    Can be use to make graph of a perticular metrics
    Query parameter to pass
          - interval = seconds
          - metric = name of metric
     - /get/metadata
    Returns all metadata about the instance

#### Testing Instance

By default, the Replorter app will use port 5000, 

```sh
http://13.233.126.248:5000/get/metadata
```