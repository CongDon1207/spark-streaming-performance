# streaming_demo.py
# Demo Kafka → Spark → Postgres với foreachBatch và throttling
# 
# Chức năng:
# - Đọc dữ liệu từ Kafka topic 'events'
# - Xử lý streaming với Spark Structured Streaming
# - Ghi kết quả vào PostgreSQL bằng foreachBatch
# - Áp dụng throttling để kiểm soát tốc độ xử lý
