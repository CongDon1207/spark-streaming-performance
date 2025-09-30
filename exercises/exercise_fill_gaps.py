from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import time

SLEEP_MS = 15
CONFIG = {
    "APP_NAME": "Exercise-FillGaps",
    "UI_PORT": "4040",
    "DEFAULT_PARALLELISM": 4,
    "REPARTITION": 4,
    "REDUCE_PARTITIONS": 4,
    "BATCH_INTERVAL": 2,
    "SOCKET_HOST": "localhost",
    "SOCKET_PORT": 9999,
}


def slow_map(value: str) -> str:
    time.sleep(SLEEP_MS / 1000.0)
    return value


def main() -> None:
    conf = (
        SparkConf()
        .setAppName(CONFIG["APP_NAME"])
        .set("spark.ui.port", CONFIG["UI_PORT"])
        .set("spark.default.parallelism", str(CONFIG["DEFAULT_PARALLELISM"]))
    )
    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, CONFIG["BATCH_INTERVAL"])

    lines = ssc.socketTextStream(CONFIG["SOCKET_HOST"], CONFIG["SOCKET_PORT"])
    faster = lines.repartition(CONFIG["REPARTITION"]).map(slow_map)

    pairs = faster.flatMap(lambda line: line.split()).map(lambda word: (word, 1))
    counts = pairs.reduceByKey(
        lambda a, b: a + b, numPartitions=CONFIG["REDUCE_PARTITIONS"]
    )
    counts.pprint(5)

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
