from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.functions import udf
from pyspark.sql.types import StringType
from pyspark.sql.functions import current_timestamp, date_format
import re
import requests
import torch

from transformers import (
    AutoTokenizer,
    AutoModelForSequenceClassification,
    TrainingArguments,
    Trainer,
    pipeline,
)

# 加载本地模型和分词器
model_path = './distilbert-base-uncased_System_analyse_sentiment'
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
# 使用pipeline简化预测过程
classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)
## mac m1/m2/m3 使用 mps , windows 使用 cuda
device = torch.device("mps" if torch.backends.mps.is_available() else "cuda")
model.eval()  # Set model to evaluation mode

def predict_sentiment(headlines):
    # Prepare input
    inputs = tokenizer(headlines, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    logits = outputs.logits
    probabilities = torch.softmax(logits, dim=-1)
    predicted_class_index = probabilities.argmax(dim=-1).item()
    
    # Mapping class index to label
    sentiment_labels = {0: "negative", 1: "neutral", 2: "positive"}
    return sentiment_labels[predicted_class_index]

## ================== 从 Kafka 读取数据 ================================================

# 初始化 Spark 会话
spark = SparkSession.builder \
    .appName("KafkaSparkStreaming") \
    .config("spark.streaming.backpressure.enabled", "true") \
    .config("spark.streaming.batchDuration", "10") \
    .getOrCreate()

# 本地资源不够，关闭检查点
spark.conf.set("spark.sql.streaming.forceDeleteTempCheckpointLocation", "true")
spark.sparkContext.setLogLevel("WARN")
# 设置 Kafka 服务器和主题
kafka_topic_name = "finance-news"
kafka_bootstrap_servers = 'kafka:9093'

# 这里使用timeout参数，避免因为网络问题导致的超时问题， 以及在使用时出现 warn警告 kafka-1894, 不要担心，pyspark与kafka兼容性问题
# 如果不喜欢warn，修改log4j.properties文件，将log4j.logger.org.apache.kafka.clients.NetworkClient=ERROR，自行google搜索
df = spark \
  .readStream \
  .format("kafka") \
  .option("kafka.bootstrap.servers", kafka_bootstrap_servers) \
  .option("subscribe", kafka_topic_name) \
  .option("startingOffsets", "latest") \
  .load()

## ================== 数据处理 ================================================
## 列名需要与 clickhouse 数据库表字段名一致
# 转换 key 和 value 从二进制到字符串
df_transformed = df.select(
    #col("key").cast("string").alias("key"),  目前不需要 key，可自行添加
    col("value").cast("string").alias("news_text")
)
# 注册 UDF
predict_sentiment_udf = udf(predict_sentiment, StringType())
# 应用 NLP 模型进行分析
df_transformed = df_transformed.withColumn("prediction_result", predict_sentiment_udf(col("news_text")))  # 传入 value 列
# 加入当天日期
df_transformed = df_transformed.withColumn("timestamp",date_format(current_timestamp(),"yyyy-MM-dd HH:mm:ss"))

# 定义 ClickHouse 的连接参数
url = "jdbc:clickhouse://clickhouse-server:8123/default"
properties = {
    "user": "default",   # 默认用户名
    "password": "123456",      # 默认没有密码，如果设置了密码需要更改
    "driver": "com.clickhouse.jdbc.ClickHouseDriver"
}


# 配置写入 ClickHouse 的数据流,但是 clickhouse 不支持dataframe的流式写入，所以我们使用foreachBatch 微批次流写入
# epoch_id 是每个批次的唯一标识符 必须写入，否则会报错
def write_to_clickhouse(batch_df, epoch_id):
  try:
    """
    写入每个批次的数据到 ClickHouse。
    """
    batch_df.write \
        .format("jdbc") \
        .option("url", url) \
        .option("dbtable", "news_analysis") \
        .option("user", properties["user"]) \
        .option("password", properties["password"]) \
        .option("driver", properties["driver"]) \
        .option("checkpointLocation", "./checkpoint/analysis") \
        .mode("append") \
        .save()
    print(f"Batch {epoch_id} successfully written to ClickHouse.")
  except Exception as e:
    print(f"Error writing batch {epoch_id} to ClickHouse: {str(e)}")


query = df_transformed.writeStream \
    .outputMode("append") \
    .foreachBatch(write_to_clickhouse) \
    .start()

query.awaitTermination()
