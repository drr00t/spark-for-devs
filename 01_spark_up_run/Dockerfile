# Use an official Python image as a base
FROM python:3.11-slim

# Set the Spark version as an environment variable
ENV SPARK_VERSION=3.5.1

# Set the Python version as an environment variable
ENV PYTHON_VERSION=3.11
RUN set -ex; \
    apt update; \
    apt install -y rsync openssh-client openssh-server openjdk-17-jdk wget; \
    apt clean; \
    apt autoremove; \
    rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1000 spark

# to use external volume for for logs 
RUN addgroup --gid 1001 logs
RUN usermod -aG logs spark

RUN wget https://archive.apache.org/dist/spark/spark-${SPARK_VERSION}/spark-${SPARK_VERSION}-bin-hadoop3.tgz

RUN tar -xvf spark-${SPARK_VERSION}-bin-hadoop3.tgz && \
    mv spark-${SPARK_VERSION}-bin-hadoop3 /opt/spark && \
    rm spark-${SPARK_VERSION}-bin-hadoop3.tgz

RUN chown -R spark:spark /opt/spark

RUN mkdir -p /opt/spark/spark-events

COPY ./entrypoint.sh /

COPY spark-defaults.conf "/opt/spark/conf/"

USER spark    

# Set the Spark home directory
ENV SPARK_HOME=/opt/spark

# Set the Python path
ENV PYTHONPATH=${SPARK_HOME}/python:${PYTHONPATH}

ENV PATH=$PATH:/opt/spark/bin

ENV SPARK_MASTER="spark://spark-master:7077" \
    SPARK_MASTER_HOST=spark-master \
    SPARK_MASTER_PORT=7077 \
    SPARK_MASTER_WEBUI_PORT=8080 \
    SPARK_WORKER_PORT=7000 \
    SPARK_WORKER_WEBUI_PORT=8080 \
    SPARK_HOME="/opt/spark"

EXPOSE 8080 7077 7000 7001 7002 7003 4040 4041 4042 4043 18080 8081 8082

ENTRYPOINT ["/bin/bash","/entrypoint.sh"]
