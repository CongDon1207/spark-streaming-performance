from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import random
import time

SLEEP_MS = 10
HOT_KEY = "word0"
CONFIG = {
    "APP_NAME": "Exercise-Skew",
    "UI_PORT": "4040",
    "BATCH_INTERVAL": 2,
    "DEFAULT_PARALLELISM": 8,
    "REPARTITION": 8,
    "REDUCE_PARTITIONS": 8,
    "SOCKET_HOST": "localhost",
    "SOCKET_PORT": 9999,
    "SALT_BUCKETS": 4,
    "ENABLE_SALTING": False,
}


def slow_map(value: str) -> str:
    time.sleep(SLEEP_MS / 1000.0)
    return value


def add_salt(word: str) -> str:
    bucket = random.randint(0, CONFIG["SALT_BUCKETS"] - 1)
    return f"{word}:{bucket}"


def strip_salt(salted_key: str) -> str:
    return salted_key.split(":")[0]


def transform_key(word: str) -> str:
    if not CONFIG["ENABLE_SALTING"] or word != HOT_KEY:
        return word
    return add_salt(word)


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
    words = (
        lines.repartition(CONFIG["REPARTITION"])
        .map(slow_map)
        .flatMap(lambda line: line.split())
    )

    keyed = words.map(lambda word: (transform_key(word), 1))
    partial_counts = keyed.reduceByKey(
        lambda a, b: a + b, numPartitions=CONFIG["REDUCE_PARTITIONS"]
    )

    if CONFIG["ENABLE_SALTING"]:
        final_counts = partial_counts.map(
            lambda kv: (strip_salt(kv[0]), kv[1])
        ).reduceByKey(lambda a, b: a + b, numPartitions=CONFIG["REDUCE_PARTITIONS"])
    else:
        final_counts = partial_counts

    final_counts.pprint(5)

    ssc.start()
    ssc.awaitTermination()


if __name__ == "__main__":
    main()
