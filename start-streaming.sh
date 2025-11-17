#!/bin/bash

echo "🚀 launching flink sql jobs to ingest and join from source tables which are backed by data generator"
docker compose exec jobmanager ./sql-client-jobs

echo "🚀 launching flink job for lakehouse tiering"
docker compose exec jobmanager \
    /opt/flink/bin/flink run \
    /opt/flink/opt/fluss-flink-tiering-0.8.0-incubating.jar \
    --fluss.bootstrap.servers coordinator-server:9123 \
    --datalake.format lance \
    --datalake.lance.warehouse s3://fluss-lakehouse \
    --datalake.lance.region us-east-1 \
    --datalake.lance.endpoint http://minio:9000 \
    --datalake.lance.allow_http true \
    --datalake.lance.access_key_id admin \
    --datalake.lance.secret_access_key minio12345

echo "🕵️‍♂️ opening flink web dashboard"
open http://localhost:8083/
