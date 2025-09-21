#!/bin/bash
# create-topics.sh
# Script tạo Kafka topic 'events' với 3 partitions
#
# Chức năng:
# - Tạo topic 'events' với 3 partitions
# - Cấu hình replication factor phù hợp
# - Thiết lập các tham số retention nếu cần
#
# Sử dụng: ./create-topics.sh