from typing import List
from datetime import datetime, date
import os
import pytest
from pyspark.sql import SparkSession, DataFrame, Row

from app.business import PresentDataLogic

os.environ["PYARROW_IGNORE_TIMEZONE"] = "1"


@pytest.fixture
def get_spark_session():
    spark = SparkSession.builder.appName("Testing App").getOrCreate()
    yield spark


@pytest.fixture
def get_data():
    yield [
        Row(a=1, b=2.0, c="string1", d=date(2000, 1, 1), e=datetime(2000, 1, 1, 12, 0)),
        Row(a=2, b=3.0, c="string2", d=date(2000, 2, 1), e=datetime(2000, 1, 2, 12, 0)),
        Row(a=4, b=5.0, c="string3", d=date(2000, 3, 1), e=datetime(2000, 1, 3, 12, 0)),
    ]


def test_session_created(get_spark_session: SparkSession):
    assert get_spark_session is not None


def test_append_data_ok(get_spark_session: SparkSession, get_data: List[Row]):
    # arrange
    apl: PresentDataLogic = PresentDataLogic.fromSession(get_spark_session)

    # operate
    df: DataFrame = apl.append_data(get_data)

    # check
    assert df.count() == 3
