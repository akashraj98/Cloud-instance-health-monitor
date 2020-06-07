# Cloud-instance-health-monitor
Consists of two script 
reporter.py | Reporter
manage.py | Manager

Reporter
Reporter is the  script that is run on each instance and collect data 
Data collected by reporter 
    -CPUUtilization
    -DiskActivity
    -MemmoryUtilization
    -DiskUsage
    -NetworkActivity
    -MetaData

The data collected by reported is exposed by endpoints
Available Endpoints
    -/get/metrics
    -Returns all metrics 

    -/get/graph
    -Can be use to make graph of a perticular metrics
    -Query parameter to pass
        -interval = seconds
        -metric = name of metric

    -/get/metadata
Returns metadata about the instance

