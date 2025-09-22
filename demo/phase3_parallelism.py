from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import time

CONFIG = {
    "APP_NAME": "Phase3-Parallelism",
    "UI_PORT": "4040",
    "MASTER": "local[8]",
    "BATCH_INTERVAL": 2,
    "SOCKET_HOST": "localhost",
    "SOCKET_PORT": 9999,
    "REPARTITION": 8,
    "REDUCE_PARTITIONS": 8,
    "DEFAULT_PARALLELISM": 8,
    "SLOW_MAP_MS": 20,
    "PREVIEW_BATCHES": 5,
}


def _sleep_and_forward(value: str, delay_seconds: float) -> str:
    time.sleep(delay_seconds)
    return value


def build_streaming_context(cfg: dict) -> StreamingContext:
    conf = (
        SparkConf()
        .setAppName(cfg["APP_NAME"])
        .set("spark.ui.port", cfg["UI_PORT"])
        .set("spark.default.parallelism", str(cfg["DEFAULT_PARALLELISM"]))
    )
    master = cfg.get("MASTER")
    if master:
        conf = conf.setMaster(master)

    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, cfg["BATCH_INTERVAL"])

    stream = ssc.socketTextStream(cfg["SOCKET_HOST"], cfg["SOCKET_PORT"])
    if cfg["REPARTITION"]:
        stream = stream.repartition(cfg["REPARTITION"])

    words = stream.flatMap(lambda line: line.split())
    delay_seconds = cfg["SLOW_MAP_MS"] / 1000.0
    words = words.map(lambda w: _sleep_and_forward(w, delay_seconds))

    counts = (
        words.map(lambda w: (w, 1))
        .reduceByKey(lambda a, b: a + b, numPartitions=cfg["REDUCE_PARTITIONS"])
    )
    counts.pprint(cfg["PREVIEW_BATCHES"])
    return ssc


if __name__ == "__main__":
    streaming_context = build_streaming_context(CONFIG)
    streaming_context.start()
    streaming_context.awaitTermination()
