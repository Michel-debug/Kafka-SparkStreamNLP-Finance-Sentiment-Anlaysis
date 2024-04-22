#!/bin/bash

# 关闭所有 Docker 服务
# 没有使用docker-compose 可以使用docker-compose 卷管理 持久化存储
echo "Stoping all Docker services..."
docker stop clickhouse-server
docker stop zookeeper
docker stop kafka
docker stop spark_sentiment