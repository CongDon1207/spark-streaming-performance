# demo/socket_source.py
# Socket source có cấu hình rõ ràng để phục vụ 3 kịch bản demo
import random
import socket
import time

CONFIG = {
    "HOST": "0.0.0.0",
    "PORT": 9999,
    "WORDS_PER_LINE": 3,
    "WORD_VARIANTS": 50,
    "LINES_PER_SECOND": 150,  # đặt cao để pha 2 tạo backlog
}

_SLEEP_BETWEEN_LINES = 1.0 / CONFIG["LINES_PER_SECOND"]


def gen_line() -> str:
    words_per_line = CONFIG["WORDS_PER_LINE"]      # số từ trong 1 dòng (vd: 3)
    word_variants = CONFIG["WORD_VARIANTS"]        # số loại từ khác nhau (vd: 50)

    words = []
    for _ in range(words_per_line):
        number = random.randint(0, word_variants - 1)
        words.append(f"word{number}")

    line = " ".join(words)
    return line + "\n"


# Tạo socket IPv4 (AF_INET) dùng TCP (SOCK_STREAM)
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((CONFIG["HOST"], CONFIG["PORT"]))
    server.listen(1)
    print(f"[socket_source] listening on {CONFIG['HOST']}:{CONFIG['PORT']}")

    while True:
        conn, addr = server.accept()
        print(f"[socket_source] client connected from {addr}")
        with conn:
            while True:
                try:
                    conn.sendall(gen_line().encode("utf-8"))
                    time.sleep(_SLEEP_BETWEEN_LINES)
                except (BrokenPipeError, ConnectionResetError):
                    print("[socket_source] client disconnected")
                    break
