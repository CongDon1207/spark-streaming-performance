#!/bin/bash
# socket_source.sh
# Nguồn dữ liệu socket đơn giản thay thế Kafka cho demo
#
# Chức năng:
# - Sử dụng netcat (nc -lk 9999) 
# - Tạo socket server trên port 9999
# - Gửi dữ liệu test qua socket
# - Thay thế Kafka cho các demo đơn giản
#
# Sử dụng: ./socket_source.sh