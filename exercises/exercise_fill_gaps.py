# exercises/exercise_fill_gaps.py

from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import time

SLEEP_MS = 15  # chậm 15ms/record

def slow_map(x: str) -> str:
    # TODO: thêm chậm theo SLEEP_MS
    __________________________
    return x

if __name__ == "__main__":
    conf = (
        SparkConf()
        .setAppName("Exercise-FillGaps")
        .set("spark.ui.port", "4040")
        .set("spark.default.parallelism", "4")
    )
    sc = SparkContext(conf=conf)

    # TODO: Tạo StreamingContext với Batch Interval = 2 giây
    ssc = __________________________

    # Nguồn dữ liệu socket (khớp với demo/socket_source.py)
    lines = ssc.socketTextStream("localhost", 9999)

    # TODO: tăng parallelism trước khi xử lý nặng
    faster = lines.__________________________.map(slow_map)

    # Tách từ và đếm
    pairs = faster.flatMap(lambda line: line.split()).map(lambda w: (w, 1))

    # TODO: reduceByKey với 4 partitions
    counts = pairs.reduceByKey(lambda a, b: a + b, numPartitions=____)

    # TODO: in ra 5 dòng/ batch
    counts.________(5)

    ssc.start()
    ssc.awaitTermination()
