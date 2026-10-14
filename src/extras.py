import socket
import subprocess
import sys
import time
from urllib.parse import urlparse

from src.display import GREEN, RED, RESET


def _host(url):
    parsed = urlparse(url)
    return parsed.hostname or parsed.path or url
def run_icmp(url, n=4):
    host = _host(url)
    print(f"  ICMP ping  {host}  ({n} packets)")
    print()

    system = sys.platform
    if system == "win32":
        cmd = ["ping", "-n", str(n), host]
    else:
        cmd = ["ping", "-c", str(n), host]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        output = result.stdout or result.stderr
        for line in output.splitlines():
            stripped = line.strip()
            if stripped:
                print(f"  {stripped}")
    except FileNotFoundError:
        print("  ping not available on this system.")
    except subprocess.TimeoutExpired:
        print("  ping timed out.")
    except Exception as e:
        print(f"  Error: {e}")

def run_dns(url):
    host = _host(url)
    print(f"  DNS lookup  {host}")
    print()

    try:
        infos = socket.getaddrinfo(host, None)
        seen = set()
        for info in infos:
            family = "IPv4" if info[0] == socket.AF_INET else "IPv6"
            addr   = info[4][0]
            if addr not in seen:
                seen.add(addr)
                print(f"  {family:<6}  {addr}")

        print()
        try:
            reverse = socket.gethostbyaddr(list(seen)[0])[0]
            print(f"  Reverse  {reverse}")
        except Exception:
            pass
        try:
            if sys.platform == "win32":
                r = subprocess.run(["nslookup", "-type=MX", host],
                                   capture_output=True, text=True, timeout=5)
            else:
                r = subprocess.run(["dig", "+short", "MX", host],
                                   capture_output=True, text=True, timeout=5)
            mx = r.stdout.strip()
            if mx:
                print()
                print("  MX records:")
                for line in mx.splitlines():
                    line = line.strip()
                    if line and not line.startswith(";"):
                        print(f"    {line}")
        except Exception:
            pass

    except socket.gaierror as e:
        print(f"  {RED}Lookup failed: {e}{RESET}")
    except Exception as e:
        print(f"  Error: {e}")
