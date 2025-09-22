# Spark Streaming Performance Demo

## 📋 Tổng quan dự án
Demo về hiệu suất Spark Streaming với các kỹ thuật tối ưu hóa và xử lý bottleneck. Bao gồm 3 phase demo minh họa từ baseline → bottleneck → optimization, cùng với các bài tập thực hành.

## 📁 Cấu trúc thư mục
```
nhom10/
├── 📄 README.md                    # Tài liệu hướng dẫn
├── 📄 AGENTS.md                    # Quy tắc cho AI agents
├── 📄 docker-compose.yml           # Container orchestration
├── 📄 Dockerfile                   # Custom Spark image
├── 📄 .gitignore                   # Git ignore rules
│
├── 📁 demo/                        # Demo Performance (Slides 18-26)
│   ├── 🐍 phase1_baseline.py       # Phase 1: Baseline (BI=2s, cores=4)
│   ├── 🐍 phase2_slow_map.py       # Phase 2: Bottleneck (thêm sleep)
│   ├── 🐍 phase3_parallelism.py    # Phase 3: Tối ưu (cores=8)
│   ├── 🐍 socket_source.py         # Socket server tạo dữ liệu test
│   
│
├── 📁 spark/                       # Cấu hình Spark
│   └── 📄 spark-defaults.conf      # Spark configuration settings
│
├── 📁 exercises/                   # Bài tập thực hành (Slides 27-31)
│  
│
├── 📁 docs/                        # Tài liệu thuyết trình
│   └── 📄 nội dung thuyết trình.docx
│
└── 📁 scripts/ (tùy chọn)          # Scripts tiện ích
    ├── 🔧 run_socket_source.sh     # Chạy socket source
    └── 🔧 run_phase3_demo.sh       # Chạy phase 3 demo
```

## 🚀 Hướng dẫn sử dụng

### 1. 🏗️ Khởi động môi trường
```bash
# Build và khởi động containers
docker-compose up -d --build

# Kiểm tra containers đang chạy
docker-compose ps
```

### 2. 🎯 Chạy demo performance

> **⚠️ Lưu ý:** Cần chạy socket source trước khi chạy Spark jobs

#### **Terminal 1: Socket Source (Data Generator)**
```bash
# PowerShell hoặc CMD
docker exec -it spark-master python /opt/app/demo/socket_source.py
```
*Giữ terminal này mở - nó sẽ sinh dữ liệu liên tục*

#### **Terminal 2: Spark Streaming Jobs**
```bash
# Phase 1: Baseline (Processing Time < Batch Interval)
docker exec -it spark-master spark-submit --master local[4] /opt/app/demo/phase1_baseline.py

# Phase 2: Bottleneck (Processing Time > Batch Interval) 
docker exec -it spark-master spark-submit --master local[4] /opt/app/demo/phase2_slow_map.py

# Phase 3: Optimized (Tăng parallelism để giảm Processing Time)
docker exec -it spark-master spark-submit --master local[8] /opt/app/demo/phase3_parallelism.py
```

### 3. 📊 Truy cập Spark UI

| Service | URL | Mô tả |
|---------|-----|-------|
| **Spark Master UI** | http://localhost:8081 | Quản lý cluster, workers |
| **Spark Driver UI** | http://localhost:4040 | Monitoring jobs (khi job đang chạy) |


### 4. 📝 Bài tập thực hành




