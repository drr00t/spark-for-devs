from abc import *
from typing import List
from pyspark.sql import SparkSession
from pyspark.sql import DataFrame, Row


class PresentDataLogic(ABC):
    _session: SparkSession
    _data: DataFrame

    def __init__(self, session: SparkSession) -> None:
        self._session = session

    @staticmethod
    def fromSession(session: SparkSession) -> "PresentDataLogic":
        return PresentDataLogic(session=session)

    def append_data(self, data: List[Row]) -> DataFrame:
        self._data = self._session.createDataFrame(
            data,
            schema="a long, b double, c string, d date, e timestamp",
        )
        return self._data

    def showData(self) -> None:
        self._data.show(truncate=False)
