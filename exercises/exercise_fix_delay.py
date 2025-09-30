# exercises/exercise_fix_delay_gap.py
# Mục tiêu: Fix delay → Processing Time < Batch Interval (BI),
# Scheduling Delay ≈ 0, Queued Batches = 0.

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import time

# ====== TODO: điền các tham số "chìa khóa" ======
BI_SECONDS     = ____
SLEEP_MS       = ____ 
REPARTITIONS   = ____ 
REDUCE_PARTS   = ____ 

def slow_map(x: str) -> str:
    # TODO: vẫn giữ "tải" nhẹ để so sánh, nhưng nhỏ hơn bài 1
    _______________________________
    return x

if __name__ == "__main__":
    conf = (
        SparkConf()
        .setAppName("Exercise-FixDelay")
        .set("spark.ui.port", "4040")
        .set("spark.default.parallelism", str(REPARTITIONS))
    )
    sc = SparkContext(conf=conf)

    # TODO: Tạo StreamingContext với Batch Interval đã chọn
    ssc = _______________________________

    # Nguồn socket
    lines = ssc.socketTextStream("localhost", 9999)

    # TODO: Tăng parallelism TRƯỚC khi xử lý "chậm"
    faster = lines.repartition(__________).map(slow_map)

    # Tách từ & đếm
    pairs = faster.flatMap(lambda line: line.split()).map(lambda w: (w, 1))

    # TODO: reduceByKey với số partitions phù hợp
    counts = pairs.reduceByKey(lambda a, b: a + b, numPartitions=__________)

    # TODO: in ra 5 dòng/batch để quan sát
    counts.pprint(____)

    ssc.start()
    ssc.awaitTermination()
