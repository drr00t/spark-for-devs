from datetime import datetime, date
import json
from collections import namedtuple
from threading import Thread

from pyspark import InheritableThread
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame, DataFrameWriterV2

import os

Credentials = namedtuple("Option", "accessKey secretKey")


def load_credentials() -> Credentials:
    f = open("../../01_spark_up_run/creds/credentials.json")
    data = json.load(f)
    accessKey: str = data["accessKey"]
    secretKey: str = data["secretKey"]
    return Credentials(accessKey=accessKey, secretKey=secretKey)


def setup_session_s3(_builder: SparkSession.Builder) -> SparkSession.Builder:
    creds: Credentials = load_credentials()

    # setup all credentials and services endpóint
    _builder.config("spark.hadoop.fs.s3a.access.key", creds.accessKey).config(
        "spark.hadoop.fs.s3a.secret.key", creds.secretKey
    )

    return _builder


def create_session(_builder: SparkSession.Builder):
    builder = setup_session_s3(_builder)

    sql = builder.getOrCreate()

    sql.sparkContext.setLogLevel("WARN")

    return sql


def loading_data(session: SparkSession) -> DataFrame:
    # session.sparkContext.setLocalProperty("spark.scheduler.pool", "pool1")
    df: DataFrame = (
        session.read.format("csv")
        .load("s3a://spark-4devs/datasets/amazon_co-ecommerce_sample.csv")
        .writeTo("exploration.raw.loaded.amazon_co_ecommerce_sample")
        .using("iceberg")
        .create()
    )
    df.printSchema()


# session.sparkContext.setLocalProperty("spark.scheduler.pool", None)


# def streaming_data(session: SparkSession):
#     df_r: DataFrame = session.read.format("parquet").load(
#         "s3a://spark-4devs/amazon_co-ecommerce_sample.parquet"
#     )


def main(app_name: str = "Simple1 Batch to Streaming"):
    sql = create_session(SparkSession.builder.appName(app_name))

    # carregando dados
    loading_data(session=sql)

    sql.stop()


if __name__ == "__main__":
    main()
