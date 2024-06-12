FROM apache/spark:3.5.1-scala2.12-java17-ubuntu

USER root

RUN set -ex; \
    apt update; \
    apt install -y rsync openssh-client openssh-server; \
    apt clean; \
    apt autoremove; \
    rm -rf /var/lib/apt/lists/*

COPY ./entrypoint.sh /
ENTRYPOINT ["/bin/bash","/entrypoint.sh"]

RUN addgroup --gid 1000 logs
RUN usermod -aG logs spark

USER spark

WORKDIR /opt/spark

ENV SPARK_MASTER="spark://spark-master:7077" \
    SPARK_MASTER_HOST=spark-master \
    SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_WORKER_PORT=7000 \
    SPARK_WORKER_WEBUI_PORT=8080 \
    SPARK_HOME="/opt/spark"

COPY spark-defaults.conf "./conf/"

EXPOSE 8080 7077 7000 7001 7002 7003 4040 4041 4042 4043 18080 8081 8082
