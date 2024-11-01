from pyspark.sql import SparkSession # type: ignore
from pyspark.sql.functions import col, when, round # type: ignore
from pyspark.sql.types import FloatType # type: ignore

spark = SparkSession.builder.appName("EnrichAndCleanData").getOrCreate()
df = spark.read.parquet("hdfs://hadoop:9000/data/iot_data/")

df_cleaned = df.withColumn("temperature", when(col("temperature") > 0, col("temperature")).otherwise(None)).dropna()
df_enriched = df_cleaned.withColumn("temperature_rounded", round(col("temperature"), 1)).withColumn("energy_usage_kwh", (col("energy_usage") / 1000).cast(FloatType()))
df_enriched.write.mode("overwrite").parquet("hdfs://hadoop:9000/data/iot_data_enriched/")
