from datetime import datetime, date
import json
from collections import namedtuple
from pyspark.sql import SparkSession, DataFrame, functions as SF
from pyspark.sql.types import StringType, StructField, StructType, DateType

Credentials = namedtuple("Option", "accessKey secretKey")


def load_credentials() -> Credentials:
    f = open("creds/credentials-6.json")
    data = json.load(f)
    accessKey: str = data["accessKey"]
    secretKey: str = data["secretKey"]
    return Credentials(accessKey=accessKey, secretKey=secretKey)


def setup_session(_builder: SparkSession.Builder) -> SparkSession.Builder:
    creds: Credentials = load_credentials()

    # setup all credentials and services endpóint
    _builder.config("spark.hadoop.fs.s3a.access.key", creds.accessKey).config(
        "spark.hadoop.fs.s3a.secret.key", creds.secretKey
    )

    return _builder


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

    sql.sparkContext.setLogLevel("ERROR")

    return sql


def loading_data(session: SparkSession):
    df: DataFrame = (
        session.read.format("csv")
        .options(header=True, inferSchema=True)
        .load("s3a://spark-4devs/datasets/amazon_co-ecommerce_sample.csv")
        .writeTo("exploration.raw.amazon_co_ecommerce")
        .using("iceberg")
        .create()
    )


def create_table_products(sql: SparkSession):
    query: str = """
    select uniq_id, product_name, manufacturer, price, number_available_in_stock, 
        amazon_category_and_sub_category, description, sellers from exploration.
        raw.amazon_co_ecommerce 
    where uniq_id is not null 
        and price is not null 
        and description is not null 
        and number_available_in_stock is not null
    """
    sql.sql(query).writeTo("exploration.raw.products").using("iceberg").create()


def exploring_products_evolve_schema(sql: SparkSession):
    query: str = """
    select uniq_id, product_name, manufacturer, price, number_available_in_stock, 
        amazon_category_and_sub_category, description, sellers from exploration.
        raw.amazon_co_ecommerce 
    where uniq_id is not null 
        and description is not null 
        and number_available_in_stock is not null
        and price is null 
    """

    df_r: DataFrame = sql.sql(query)

    df_r.withColumn("updated_at", SF.current_date()).writeTo(
        "exploration.raw.products"
    ).option("mergeSchema", "true").append()

    sql.sql("select * from exploration.raw.products where price is null").show(5)


def query_large_csv_compressed(sql: SparkSession):
    schema: StructType = StructType(
        [
            StructField("CNPJ_BASICO", StringType(), True),
            StructField("CNPJ_ORDEM", StringType(), True),
            StructField("CNPJ_DV", StringType(), True),
            StructField("IDENTIFICADOR_MATRIZ_FILIAL", StringType(), True),
            StructField("Nome_Fantasia", StringType(), True),
            StructField("SITUACAO_CADASTRAL", StringType(), True),
            StructField("DATA_SITUACAO_CADASTRAL", StringType(), True),
            StructField("MOTIVO_SITUACAO_CADASTRAL", StringType(), True),
            StructField("NOME_DA_CIDADE_NO_EXTERIOR", StringType(), True),
            StructField("PAIS", StringType(), True),
            StructField("DATA_INICIO_ATIVIDADE", StringType(), True),
            StructField("CNAE_FISCAL_PRINCIPAL", StringType(), True),
            StructField("CNAE_FISCAL_SECUNDARIO", StringType(), True),
            StructField("TIPO_DE_LOGRADOURO", StringType(), True),
            StructField("LOGRADOURO", StringType(), True),
            StructField("NUMERO", StringType(), True),
            StructField("COMPLEMENTO", StringType(), True),
            StructField("BAIRRO", StringType(), True),
            StructField("CEP", StringType(), True),
            StructField("UF", StringType(), True),
            StructField("MUNICIPIO", StringType(), True),
            StructField("DDD1", StringType(), True),
            StructField("TELEFONE1", StringType(), True),
            StructField("DDD2", StringType(), True),
            StructField("TELEFONE2", StringType(), True),
            StructField("DDD_DO_FAX", StringType(), True),
            StructField("FAX", StringType(), True),
            StructField("CORREIO_ELETRONICO", StringType(), True),
            StructField("SITUACAO_ESPECIAL", StringType(), True),
            StructField("DATA_DA_SITUACAO_ESPECIAL", StringType(), True),
        ]
    )

    df: DataFrame = (
        sql.read.format("csv")
        .schema(schema)
        .option("delimiter", ";")
        .load("s3a://spark-4devs/datasets/K3241.K03200Y4.D40608.ESTABELE")
        # .filter("UF = 'SP'")
        # .select("CNPJ_BASICO", "Nome_Fantasia", "DATA_INICIO_ATIVIDADE", "UF")
        # .groupBy("UF")
        # .agg(SF.count("CNPJ_BASICO"))
        # .show(truncate=False)
        .writeTo("exploration.irpf.estabelecimentos")
        .using("iceberg")
        .create()
    )


def exploring_exploration_iprf_estabelecimentos(sql: SparkSession):
    query: str = """
    select * from exploration.irpf.estabelecimentos 
    where UF = 'RS' 
    """
    sql.sql(query).show(truncate=False)


def carregando_dataset_irpf(session: SparkSession):
    schema: StructType = StructType(
        [
            StructField("CNPJ_BASICO", StringType(), True),
            StructField("CNPJ_ORDEM", StringType(), True),
            StructField("CNPJ_DV", StringType(), True),
            StructField("IDENTIFICADOR_MATRIZ_FILIAL", StringType(), True),
            StructField("Nome_Fantasia", StringType(), True),
            StructField("SITUACAO_CADASTRAL", StringType(), True),
            StructField("DATA_SITUACAO_CADASTRAL", StringType(), True),
            StructField("MOTIVO_SITUACAO_CADASTRAL", StringType(), True),
            StructField("NOME_DA_CIDADE_NO_EXTERIOR", StringType(), True),
            StructField("PAIS", StringType(), True),
            StructField("DATA_INICIO_ATIVIDADE", StringType(), True),
            StructField("CNAE_FISCAL_PRINCIPAL", StringType(), True),
            StructField("CNAE_FISCAL_SECUNDARIO", StringType(), True),
            StructField("TIPO_DE_LOGRADOURO", StringType(), True),
            StructField("LOGRADOURO", StringType(), True),
            StructField("NUMERO", StringType(), True),
            StructField("COMPLEMENTO", StringType(), True),
            StructField("BAIRRO", StringType(), True),
            StructField("CEP", StringType(), True),
            StructField("UF", StringType(), True),
            StructField("MUNICIPIO", StringType(), True),
            StructField("DDD1", StringType(), True),
            StructField("TELEFONE1", StringType(), True),
            StructField("DDD2", StringType(), True),
            StructField("TELEFONE2", StringType(), True),
            StructField("DDD_DO_FAX", StringType(), True),
            StructField("FAX", StringType(), True),
            StructField("CORREIO_ELETRONICO", StringType(), True),
            StructField("SITUACAO_ESPECIAL", StringType(), True),
            StructField("DATA_DA_SITUACAO_ESPECIAL", StringType(), True),
        ]
    )

    df: DataFrame = (
        session.read.format("csv")
        .option("delimiter", ";")
        .schema(schema)
        .load("s3a://spark-4devs/datasets/0-10-ESTABELE.csv")
        .writeTo("exploration.raw.estabelecimentos")
        .using("iceberg")
        .create()
    )


def carregando_dataset_irpf_schema(session: SparkSession):

    session.read.table("exploration.raw.estabelecimentos").printSchema()

    session.sql(
        "ALTER TABLE exploration.raw.estabelecimentos ADD COLUMN DATA_SITUACAO_CADASTRAL_TIPADA date;"
    ).show()

    session.sql(
        "UPDATE exploration.raw.estabelecimentos SET DATA_SITUACAO_CADASTRAL_TIPADA = to_date(DATA_SITUACAO_CADASTRAL,'yyyyMMdd')"
    )

    session.sql(
        "select CNPJ_BASICO,DATA_INICIO_ATIVIDADE,DATA_SITUACAO_CADASTRAL_TIPADA from exploration.raw.estabelecimentos"
    ).show(truncate=False)

    # session.read.table("exploration.raw.estabelecimentos").printSchema()

    # df: DataFrame = (
    #     session.read.format("csv")
    #     .options(header=False, inferSchema=True)
    #     .load("s3a://spark-4devs/datasets/0-1000000-ESTABELE.csv")
    #     .writeTo("exploration.raw.estab")
    #     .using("iceberg")
    #     .create()
    # )


def main(app_name: str = "Simple1 Batch to Streaming"):
    sql = create_session(SparkSession.builder.appName(app_name))

    # carregando dados
    # loading_data(session=sql)
    # exploring_products_evolve_schema(sql)
    # query_large_csv_compressed(sql)
    # exploring_exploration_iprf_estabelecimentos(sql)
    # carregando_dataset_irpf(session=sql)
    carregando_dataset_irpf_schema(session=sql)
    sql.stop()


if __name__ == "__main__":
    main()
