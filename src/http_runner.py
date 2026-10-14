import threading
import time
import urllib.request
import urllib.parse
import urllib.error
import os

from src.display import print_result, print_summary, reset_counter


def _resolve_data(data_arg):
    if data_arg and data_arg.lower().endswith(".txt") and os.path.isfile(data_arg):
        with open(data_arg, "r", encoding="utf-8") as f:
            return f.read().strip()
    return data_arg


def run_http(url, method, n, c, keep_alive, data_arg, form):
    body = _resolve_data(data_arg) if data_arg else None
    reset_counter()

    ka = "yes" if keep_alive else "no"
    print(f"  {method} {url}")
    print(f"  n={n} c={c} keep-alive={ka}")
    print()

    results   = []
    lock      = threading.Lock()
    semaphore = threading.Semaphore(c)

    def do_request():
        with semaphore:
            start  = time.perf_counter()
            status = None
            error  = None
            try:
                if form and body:
                    pairs = {}
                    for pair in body.split("&"):
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            pairs[k] = v
                    encoded = urllib.parse.urlencode(pairs).encode()
                    req = urllib.request.Request(url, data=encoded, method=method)
                    req.add_header("Content-Type", "application/x-www-form-urlencoded")
                elif body:
                    data = body.encode() if isinstance(body, str) else body
                    req  = urllib.request.Request(url, data=data, method=method)
                    req.add_header("Content-Type", "application/octet-stream")
                else:
                    req = urllib.request.Request(url, method=method)

                req.add_header("Connection", "keep-alive" if keep_alive else "close")
                req.add_header("User-Agent", "req1/1.0")

                with urllib.request.urlopen(req, timeout=15) as resp:
                    status = resp.status
                    resp.read(256)

            except urllib.error.HTTPError as e:
                status = e.code
                error  = str(e.reason)
            except Exception as e:
                error = str(e)

            elapsed = time.perf_counter() - start
            with lock:
                results.append((status, elapsed, error))
                print_result(status, elapsed, error)

    threads = [threading.Thread(target=do_request) for _ in range(n)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    print_summary(results)
