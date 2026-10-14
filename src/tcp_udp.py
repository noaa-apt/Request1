import socket
import threading
import time
from urllib.parse import urlparse

from src.display import RED, RESET, print_result, print_summary, reset_counter


def _parse_url(url):
    parsed = urlparse(url)
    host = parsed.hostname or parsed.netloc or parsed.path
    port = parsed.port
    return host, port


def _ask_port(proto):
    while True:
        try:
            return int(input(f"  {proto} port > ").strip())
        except ValueError:
            print("  Enter a valid port number.")


def _ask_message(proto):
    return input(f"  {proto} message (blank = empty) > ").strip()


def run_tcp(url, n, c):
    host, port = _parse_url(url)
    print(f"  TCP  {host}")
    if not port:
        port = _ask_port("TCP")
    msg = _ask_message("TCP")

    reset_counter()
    print(f"\n  n={n} c={c}  target={host}:{port}")
    print()

    results   = []
    lock      = threading.Lock()
    semaphore = threading.Semaphore(c)

    def do_tcp():
        with semaphore:
            start  = time.perf_counter()
            status = None
            error  = None
            try:
                with socket.create_connection((host, port), timeout=10) as s:
                    if msg:
                        s.sendall(msg.encode())
                    s.recv(4096)
                    status = 200
            except Exception as e:
                error = str(e)
            elapsed = time.perf_counter() - start
            with lock:
                results.append((status, elapsed, error))
                print_result(status, elapsed, error)

    threads = [threading.Thread(target=do_tcp) for _ in range(n)]
    for t in threads: t.start()
    for t in threads: t.join()
    print_summary(results)


def run_udp(url, n, c):
    host, port = _parse_url(url)
    print(f"  UDP  {host}")
    if not port:
        port = _ask_port("UDP")
    msg = _ask_message("UDP")

    reset_counter()
    print(f"\n  n={n} c={c}  target={host}:{port}")
    print()

    results   = []
    lock      = threading.Lock()
    semaphore = threading.Semaphore(c)

    def do_udp():
        with semaphore:
            start  = time.perf_counter()
            status = None
            error  = None
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                    s.settimeout(5)
                    s.sendto(msg.encode() if msg else b"", (host, port))
                    try:
                        s.recvfrom(4096)
                    except socket.timeout:
                        error = "no reply (normal for UDP)"
                    status = 200
            except Exception as e:
                error = str(e)
            elapsed = time.perf_counter() - start
            with lock:
                results.append((status, elapsed, error))
                print_result(status, elapsed, error)

    threads = [threading.Thread(target=do_udp) for _ in range(n)]
    for t in threads: t.start()
    for t in threads: t.join()
    print_summary(results)
