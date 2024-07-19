from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.functions import col, date_format
from datetime import datetime, date
import os
from pyspark.sql import Row


def init_spark() -> SparkSession:
    builder: SparkSession.Builder = SparkSession.builder.appName("Simple1")

    sql = builder.getOrCreate()

    sql.sparkContext.setLogLevel("WARN")

    return sql


def main():
    sql: SparkSession = init_spark()
    df: DataFrame = sql.createDataFrame(
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
    sql.sql("")
    df.writeTo("exploring.product_sales").using("iceberg").create()
    df.show(truncate=False)
    sql.stop()


if __name__ == "__main__":
    main()
