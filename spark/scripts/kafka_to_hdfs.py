from pyspark.sql import SparkSession # type: ignore

spark = SparkSession.builder.appName("KafkaToHDFS").getOrCreate()
df = spark.readStream.format("kafka").option("kafka.bootstrap.servers", "kafka:9092").option("subscribe", "iot_data").load()
df.writeStream.format("parquet").option("path", "hdfs://hadoop:9000/data/iot_data/").option("checkpointLocation", "/tmp/checkpoints").start().awaitTermination()
