import socket
import threading
import time
import urllib.request
import urllib.error
from urllib.parse import urlparse

from src.display import GREEN, RED, RESET
from src.port_scanner import COMMON_PORTS

SCAN_TIMEOUT = 0.5
REQ_TIMEOUT  = 8.0

HTTPS_PORTS = {443, 8443, 2083, 2087, 2096, 9443}

def _http(host, port, method):
    scheme = "https" if port in HTTPS_PORTS else "http"
    url = f"{scheme}://{host}:{port}/"
    try:
        req = urllib.request.Request(url, method=method)
        req.add_header("User-Agent", "req1/1.0")
        req.add_header("Connection", "close")
        with urllib.request.urlopen(req, timeout=REQ_TIMEOUT) as resp:
            return True, str(resp.status)
    except urllib.error.HTTPError as e:
        return (e.code < 500), f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)[:70]


def _tcp(host, port):
    try:
        with socket.create_connection((host, port), timeout=REQ_TIMEOUT) as s:
            s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
            s.settimeout(3)
            try:
                data = s.recv(256)
                detail = data.decode(errors="replace").split("\n")[0].strip()[:70]
            except Exception:
                detail = "connected"
            return True, detail or "connected"
    except Exception as e:
        return False, str(e)[:70]


def _udp(host, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.settimeout(3)
            s.sendto(b"\x00", (host, port))
            try:
                s.recvfrom(256)
                return True, "replied"
            except socket.timeout:
                return True, "no reply?"
    except Exception as e:
        return False, str(e)[:70]

def _build_request_types(host):
    return [
        ("HTTP GET",     lambda h=host, p=None: _http(h, p, "GET")),
        ("HTTP HEAD",    lambda h=host, p=None: _http(h, p, "HEAD")),
        ("HTTP OPTIONS", lambda h=host, p=None: _http(h, p, "OPTIONS")),
        ("TCP",          lambda h=host, p=None: _tcp(h, p)),
        ("UDP",          lambda h=host, p=None: _udp(h, p)),
    ]
def run_testall(url):
    parsed = urlparse(url)
    host   = parsed.hostname or parsed.path or url
    print(f"  -testall  {host}")
    print(f"  Scanning {len(COMMON_PORTS)} ports silently …", end="", flush=True)

    open_ports = []
    lock       = threading.Lock()

    def _scan(port):
        try:
            with socket.create_connection((host, port), timeout=SCAN_TIMEOUT):
                with lock:
                    open_ports.append(port)
        except Exception:
            pass

    scan_threads = [threading.Thread(target=_scan, args=(p,), daemon=True) for p in COMMON_PORTS]
    t0 = time.perf_counter()
    for t in scan_threads: t.start()
    for t in scan_threads: t.join()
    elapsed_scan = time.perf_counter() - t0

    open_ports.sort()
    print(f"\r  Testall Completed within {len(open_ports)} Found open port(s) in {elapsed_scan:.1f}s          ")

    if not open_ports:
        print(f"  {RED}No open ports found? There is nothing to probe.{RESET}")
        return

    print(f"  Open ports: {', '.join(str(p) for p in open_ports)}")
    print()

    request_types = [
        ("HTTP GET",     lambda h, p: _http(h, p, "GET")),
        ("HTTP HEAD",    lambda h, p: _http(h, p, "HEAD")),
        ("HTTP OPTIONS", lambda h, p: _http(h, p, "OPTIONS")),
        ("TCP",          lambda h, p: _tcp(h, p)),
        ("UDP",          lambda h, p: _udp(h, p)),
    ]
    results  = {}
    res_lock = threading.Lock()

    def _run(req_name, port, fn):
        ok, detail = fn(host, port)
        with res_lock:
            results[(req_name, port)] = (ok, detail)

    threads = []
    for req_name, fn in request_types:
        for port in open_ports:
            t = threading.Thread(target=_run, args=(req_name, port, fn), daemon=True)
            threads.append(t)

    for t in threads: t.start()
    for t in threads: t.join()

    port_col = max(len(str(p)) for p in open_ports) + 2
    det_col  = 70

    total_allowed = 0
    total_denied  = 0

    for req_name, _ in request_types:
        print(f"  {req_name}")
        req_allowed = 0
        req_denied  = 0
        for port in open_ports:
            ok, detail = results.get((req_name, port), (False, "no result"))
            color  = GREEN if ok else RED
            status = "allowed" if ok else "denied"
            port_str = f":{port}"
            print(f"    {port_str:<{port_col}} {color}{status:<8}{RESET}  {detail}")
            if ok:
                req_allowed += 1
            else:
                req_denied  += 1
        print(f"    {GREEN}allowed {req_allowed}{RESET}  {RED}denied {req_denied}{RESET}")
        print()
        total_allowed += req_allowed
        total_denied  += req_denied
    total = total_allowed + total_denied
    print(f"  In total, There is: {GREEN}Allowed: {total_allowed}{RESET}   {RED}Denied: {total_denied}{RESET}")
