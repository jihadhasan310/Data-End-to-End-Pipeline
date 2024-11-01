import json
from pyspark.sql import SparkSession # type: ignore
import requests

spark = SparkSession.builder.appName("HDFSToDruid").getOrCreate()
df = spark.read.parquet("hdfs://hadoop:9000/data/iot_data_enriched/")
data_json = df.toJSON().map(lambda j: json.loads(j)).collect()
requests.post("http://druid:8888/druid/v2", json=data_json)
spark.stop()
