FROM apache/spark:3.5.1-scala2.12-java17-ubuntu

USER root

RUN set -ex; \
    apt-get update; \
    apt-get install -y rsync openssh-client openssh-server; \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

USER spark

WORKDIR /opt/spark

ENV SPARK_LOG_DIR="/opt/spark/logs" \
    SPARK_MASTER="spark://spark-master:7077" \
    SPARK_MASTER_HOST=spark-master \
    SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_MASTER_LOG="/opt/spark/logs/spark-master.out" \
    SPARK_WORKER_LOG="/opt/spark/logs/spark-worker.out" \
    SPARK_WORKER_PORT=7000 \
    SPARK_WORKER_WEBUI_PORT=8080 

COPY spark-defaults.conf "$SPARK_HOME/conf"

EXPOSE 8080 7077 7000 7001 7002 7003 4040 4041 4042 4043 18080

RUN mkdir -p $SPARK_LOG_DIR && \
    touch $SPARK_MASTER_LOG && \
    touch $SPARK_WORKER_LOG && \
    ln -sf /dev/stdout $SPARK_MASTER_LOG && \
    ln -sf /dev/stdout $SPARK_WORKER_LOG
