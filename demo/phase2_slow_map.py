from pyspark import SparkConf, SparkContext
from pyspark.streaming import StreamingContext
import time

CONFIG = {
    "APP_NAME": "Phase2-SlowMap",
    "UI_PORT": "4040",
    "MASTER": "local[4]",
    "BATCH_INTERVAL": 2,
    "SOCKET_HOST": "localhost",
    "SOCKET_PORT": 9999,
    "PARALLELISM": 4,
    "DELAY_SECONDS": 0.004,  # 4ms
}


def build_streaming_context(cfg: dict) -> StreamingContext:
    conf = (
        SparkConf()
        .setAppName(cfg["APP_NAME"])
        .set("spark.ui.port", cfg["UI_PORT"])
        .set("spark.default.parallelism", str(cfg["PARALLELISM"]))
    )
    master = cfg.get("MASTER")
    if master:
        conf = conf.setMaster(master)

    sc = SparkContext(conf=conf)
    ssc = StreamingContext(sc, cfg["BATCH_INTERVAL"])

    

    stream = ssc.socketTextStream(cfg["SOCKET_HOST"], cfg["SOCKET_PORT"])
    if cfg["PARALLELISM"]:
        stream = stream.repartition(cfg["PARALLELISM"])

    words = stream.flatMap(lambda line: line.split())
    words = words.map(lambda w: (time.sleep(cfg["DELAY_SECONDS"]), w)[1])

    counts = (
        words.map(lambda w: (w, 1))
        .reduceByKey(lambda a, b: a + b, numPartitions=cfg["PARALLELISM"])
    )
    counts.pprint(5)
    return ssc


if __name__ == "__main__":
    streaming_context = build_streaming_context(CONFIG)
    streaming_context.start()
    streaming_context.awaitTermination()
