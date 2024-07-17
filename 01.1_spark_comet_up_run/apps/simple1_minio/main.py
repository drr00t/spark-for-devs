from datetime import datetime, date
import json
from collections import namedtuple

from pyspark.sql import SparkSession
from pyspark.sql import Row, DataFrame

Credentials = namedtuple("Option", "accessKey secretKey endpointS3")


def load_credentials() -> Credentials:
    f = open("../../creds/credentials.json")
    data = json.load(f)
    accessKey: str = data["accessKey"]
    secretKey: str = data["secretKey"]
    endpointS3: str = "http://192.168.15.6:9000"
    return Credentials(accessKey=accessKey, secretKey=secretKey, endpointS3=endpointS3)


def setup_session_s3(_builder: SparkSession.Builder) -> SparkSession.Builder:
    creds: Credentials = load_credentials()

    # setup all credentials and services endpóint
    _builder.config("spark.hadoop.fs.s3a.access.key", creds.accessKey).config(
        "spark.hadoop.fs.s3a.secret.key", creds.secretKey
    ).config("spark.hadoop.fs.s3a.endpoint", creds.endpointS3)

    return _builder


def create_session(_builder: SparkSession.Builder):
    builder = setup_session_s3(_builder)

    sql = builder.getOrCreate()

    sql.sparkContext.setLogLevel("WARN")

    return sql


def main(app_name: str = "Simple1 Minio"):
    sql = create_session(SparkSession.builder.appName(app_name))

    sql.read.format("csv").load(
        "s3a://spark-4devs/datasets/amazon_co-ecommerce_sample.csv"
    ).write.mode("overwrite").format("parquet").save(
        "s3a://spark-4devs/amazon_co-ecommerce_sample.parquet"
    )

    df_r: DataFrame = sql.read.format("parquet").load(
        "s3a://spark-4devs/amazon_co-ecommerce_sample.parquet"
    )

    print(f"total de produtos: {df_r.sort('_c1').count()}")
    # df_r.show(truncate=False)
    df_r.explain()

    sql.stop()


if __name__ == "__main__":
    main()
