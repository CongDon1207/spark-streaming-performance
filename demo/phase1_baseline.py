from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext

CONFIG = {
    "APP_NAME": "Phase1-Baseline",
    "UI_PORT": "4040",
    "MASTER": None,
    "BATCH_INTERVAL": 2,
    "SOCKET_HOST": "localhost",
    "SOCKET_PORT": 9999,
    "REPARTITION": 4,
    "REDUCE_PARTITIONS": 4,
    "DEFAULT_PARALLELISM": 4,
    "PREVIEW_BATCHES": 5,
}


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
