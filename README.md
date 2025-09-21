# Spark Streaming Performance Demo

## Tổng quan dự án
Demo về hiệu suất Spark Streaming với các kỹ thuật tối ưu hóa và xử lý bottleneck.

## Cấu trúc thư mục
```
nhom10/
├─ docker-compose.yml           # Container orchestration
├─ app/                         # Ứng dụng chính
│  ├─ streaming_demo.py         # Kafka → Spark → Postgres
│  ├─ batch_demo.py             # Demo shuffle/partitions
│  └─ requirements.txt          # Python dependencies
├─ postgres/
│  └─ init.sql                  # Schema cho events_sink
├─ kafka/
│  └─ create-topics.sh          # Tạo topic 'events'
├─ spark/
│  └─ spark-defaults.conf       # Cấu hình Spark
├─ demo/                        # Demo performance (Slide 18-26)
│  ├─ phase1_baseline.py        # Baseline: Processing < BI
│  ├─ phase2_slow_map.py        # Bottleneck: Processing > BI  
│  ├─ phase3_parallelism.py     # Fix: Tăng parallelism
│  ├─ socket_source.sh          # Simple data source
│  └─ run_examples.md           # Hướng dẫn chạy demo
└─ exercises/                   # Bài tập (Slide 27-31)
   ├─ level1_fill_gaps/         # Điền chỗ trống cơ bản
   │  ├─ exercise_fill_gaps.py
   │  └─ SOLUTION.md
   └─ level2_skew_salt/         # Xử lý data skew
      ├─ exercise_skew_fill_gaps.py
      └─ SOLUTION.md
```

## Hướng dẫn sử dụng

### 1. Khởi động environment
```bash
docker-compose up -d
./kafka/create-topics.sh
```

### 2. Chạy demo performance
```bash
# Phase 1: Baseline
spark-submit demo/phase1_baseline.py

# Phase 2: Bottleneck  
spark-submit demo/phase2_slow_map.py

# Phase 3: Optimized
spark-submit demo/phase3_parallelism.py
```

### 3. Quan sát Spark UI
- URL: http://localhost:4040
- Chú ý: Streaming tab, Jobs, Stages
- Metrics: Processing Time, Scheduling Delay, Input Rate

### 4. Bài tập
- Level 1: Điền chỗ trống trong `exercises/level1_fill_gaps/`
- Level 2: Xử lý data skew trong `exercises/level2_skew_salt/`

## Checklist quan sát UI
- [ ] Input Rate vs Processing Rate
- [ ] Batch Processing Time trend
- [ ] Scheduling Delay pattern  
- [ ] Task duration distribution
- [ ] Memory usage và GC behavior
- [ ] Shuffle read/write metrics

## Mục tiêu học tập
1. Hiểu bottleneck trong streaming applications
2. Áp dụng kỹ thuật tối ưu parallelism
3. Xử lý data skew với salting/pre-aggregation
4. Sử dụng Spark UI để performance tuning
5. Best practices cho production streaming jobs
