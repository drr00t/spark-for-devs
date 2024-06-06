https://medium.com/@SaphE/testing-apache-spark-locally-docker-compose-and-kubernetes-deployment-94d35a54f222

## run spark cluster 

### build local image

```console
docker compose build
```

### start up cluster
```console
docker compose up
```

### scale up to workers
```console
docker compose up --scale spark-worker=2
```

## execute app simple1

### local threaded execution 
```console
spark-submit  main.py 
```

### execution in local cluster
```console
spark-submit --master spark://192.168.15.6:7077 --executor-memory 500M --driver-memory 500M  main.py 
```

#### execution in local cluster (not enough resource) stay waiting forever
```console
spark-submit --master spark://192.168.15.6:7077 --executor-memory 10G --driver-memory 10G  main.py 
```
