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


def setup_spark_base(_builder: SparkSession.Builder) -> SparkSession.Builder:
    _builder.config("spark.sql.execution.arrow.pyspark.enabled", "true")
    return _builder


def setup_session_s3_hadoop(_builder: SparkSession.Builder) -> SparkSession.Builder:
    # """ reference for S3 file handling via Spark: https://hadoop.apache.org/docs/current/hadoop-aws/tools/hadoop-aws/committers.html#Meet_the_S3A_Committers """

    _builder.config("spark.hadoop.fs.s3a.connection.timeout", "60000").config(
        "spark.hadoop.fs.s3a.path.style.access", "true"
    ).config(
        "spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem"
    ).config(
        "spark.hadoop.fs.s3a.connection.ssl.enabled", "false"
    ).config(
        "spark.hadoop.fs.s3a.committer.magic.enabled", "true"
    ).config(
        "spark.hadoop.fs.s3a.committer.name", "magic"
    ).config(
        "spark.hadoop.fs.s3a.committer.generate.uuid", "true"
    ).config(
        "spark.hadoop.mapreduce.fileoutputcommitter.algorithm.version", "2"
    ).config(
        "spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a",
        "org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory",
    ).config(
        "spark.hadoop.mapreduce.outputcommitter.factory.scheme.s3a",
        "org.apache.hadoop.fs.s3a.commit.S3ACommitterFactory",
    )
    return _builder


def setup_session_s3(_builder: SparkSession.Builder) -> SparkSession.Builder:
    creds: Credentials = load_credentials()

    # setup all credentials and services endpóint
    _builder.config("spark.hadoop.fs.s3a.access.key", creds.accessKey).config(
        "spark.hadoop.fs.s3a.secret.key", creds.secretKey
    ).config("spark.hadoop.fs.s3a.endpoint", creds.endpointS3)

    # setup all hadoop options for low level filesystem options
    _builder.config(
        "spark.sql.sources.commitProtocolClass",
        "org.apache.spark.internal.io.cloud.PathOutputCommitProtocol",
    ).config(
        "spark.sql.parquet.output.committer.class",
        "org.apache.spark.internal.io.cloud.BindingParquetOutputCommitter",
    )
    setup_session_s3_hadoop(_builder)

    return _builder


def create_session(_builder: SparkSession.Builder):
    builder = setup_session_s3(_builder)

    sql = builder.getOrCreate()

    sql.sparkContext.setLogLevel("WARN")

    return sql


def main(app_name: str = "Simple1"):
    sql = create_session(SparkSession.builder.appName(app_name))

    df = sql.createDataFrame(
        [
            Row(
                a=1,
                b=2.0,
                c="string1",
                d=date(2000, 1, 1),
                e=datetime(2000, 1, 1, 12, 0),
            ),
            Row(
                a=2,
                b=3.0,
                c="string2",
                d=date(2000, 2, 1),
                e=datetime(2000, 1, 2, 12, 0),
            ),
            Row(
                a=4,
                b=5.0,
                c="string3",
                d=date(2000, 3, 1),
                e=datetime(2000, 1, 3, 12, 0),
            ),
        ],
        schema="a long, b double, c string, d date, e timestamp",
    )

    df.write.mode("overwrite").format("parquet").save("s3a://spark-4devs/dataframe")

    df_r: DataFrame = sql.read.format("parquet").load("s3a://spark-4devs/dataframe")

    df_r.show(truncate=False)

    sql.stop()


if __name__ == "__main__":
    main()
