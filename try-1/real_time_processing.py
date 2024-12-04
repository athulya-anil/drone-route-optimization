from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, StringType, FloatType

# Initialize Spark session
spark = SparkSession.builder \
    .appName("RealTimeDataProcessing") \
    .getOrCreate()

# Define schemas
traffic_schema = StructType([
    StructField("id", StringType(), True),
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("congestion", FloatType(), True)
])

weather_schema = StructType([
    StructField("id", StringType(), True),
    StructField("latitude", FloatType(), True),
    StructField("longitude", FloatType(), True),
    StructField("weather_condition", StringType(), True)
])

# Read traffic data from Kafka
traffic_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "traffic_topic") \
    .load()

# Read weather data from Kafka
weather_df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "weather_topic") \
    .load()

# Process the data
traffic_data = traffic_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), traffic_schema).alias("data")) \
    .select("data.*")

weather_data = weather_df.selectExpr("CAST(value AS STRING)") \
    .select(from_json(col("value"), weather_schema).alias("data")) \
    .select("data.*")

# Join and write data to a sink (server)
processed_data = traffic_data.join(weather_data, "id")
query = processed_data.writeStream \
    .format("console") \
    .start()

query.awaitTermination()
