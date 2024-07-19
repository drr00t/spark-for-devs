#!/bin/bash
. "${SPARK_HOME}/bin/load-spark-env.sh"

export SPARK_MASTER_HOST=`hostname`

if [ "$SPARK_WORKLOAD" == "master" ];
then

# export SPARK_MASTER_HOST=`hostname`

cd ${SPARK_HOME}/bin && ./spark-class org.apache.spark.deploy.master.Master --ip $SPARK_MASTER_HOST --port $SPARK_MASTER_PORT --webui-port $SPARK_MASTER_WEBUI_PORT

elif [ "$SPARK_WORKLOAD" == "worker" ];
then

cd ${SPARK_HOME}/bin && ./spark-class org.apache.spark.deploy.worker.Worker --webui-port $SPARK_WORKER_WEBUI_PORT $SPARK_MASTER

elif [ "$SPARK_WORKLOAD" == "history" ];
then

cd ${SPARK_HOME}/bin && ./spark-class org.apache.spark.deploy.history.HistoryServer

elif [ "$SPARK_WORKLOAD" == "thrift" ];
then

cd ${SPARK_HOME}/bin && ./sbin/start-thriftserver.sh

else
    echo "Undefined Workload Type $SPARK_WORKLOAD, must specify: master, worker, history, thrift"
fi