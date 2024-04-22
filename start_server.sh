#!/bin/bash

# 启动所有 Docker 服务
# 没有使用docker-compose 可以使用docker-compose 卷管理 持久化存储
echo "Starting all Docker services..."
docker start clickhouse-server
docker start zookeeper
docker start spark_sentiment
docker start kafka

#这里还有问题，请广大网友 自行解决，方法有很多
# 确保 Kafka 和 Spark 服务已经启动
#echo "Waiting for services to start..."
#sleep 10  # 等待10秒，确保服务完全启动

# 启动 Kafka 生产者脚本
#echo "Starting Kafka producer..."
#/Users/chenchenjunjie/anaconda3/envs/nlp/bin/python ./kafka_connector.py 

# 运行 Spark 应用 这里还有问题，请广大网友 自行解决，方法有很多
#echo "Running Spark application..."
#docker exec -d spark_sentiment \ 
#spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.0,com.clickhouse:clickhouse-jdbc:0.6.0,org.apache.httpcomponents.client5:httpclient5:5.3.1 kf_to_sstreaming.py 


# 输出结束语
echo "All services have been started."
