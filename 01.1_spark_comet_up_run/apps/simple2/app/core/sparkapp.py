from abc import ABC, abstractmethod
from pyspark import SparkContext
from pyspark.sql import SparkSession


class SparkApplication(ABC):
    _spk_builder: SparkSession.Builder

    def __init__(self, name: str) -> None:
        self._spk_builder = SparkSession.builder.appName(name)

        # opções padrão para todas aplicações Spark
        self._spk_builder.config(
            "spark.sql.execution.arrow.pyspark.enabled", "true"
        ).config("spark.executorEnv.PEX_ROOT", "./app.pex").config(
            "spark.files", "app.pex"
        ).config(
            "spark.py-files", "app.zip"
        ).config(
            "spark.sql.session.timeZone", "UTC"
        )

    def start(self) -> None:
        session: SparkSession = self._spk_builder.getOrCreate()
        session.sparkContext.setLogLevel("WARN")

        # lógica da aplicação
        self.executeAppLogic(session)
        session.stop()

    @abstractmethod
    def executeAppLogic(self, session: SparkSession, context: SparkContext) -> None:
        pass
