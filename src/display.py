import sys

def _enable_ansi():
    if sys.platform == "win32":
        try:
            import ctypes
            ctypes.windll.kernel32.SetConsoleMode(
                ctypes.windll.kernel32.GetStdHandle(-11), 7
            )
        except Exception:
            pass

_enable_ansi()

RESET = "\033[0m"
RED   = "\033[31m"
GREEN = "\033[32m"

_counter = 0
_lock    = __import__("threading").Lock()

def next_index():
    global _counter
    with _lock:
        _counter += 1
        return _counter

def reset_counter():
    global _counter
    with _lock:
        _counter = 0

def status_color(status):
    if status and 200 <= status < 300:
        return f"{GREEN}{status}{RESET}"
    if status and 300 <= status < 400:
        return str(status)
    if status:
        return f"{RED}{status}{RESET}"
    return f"{RED}ERR{RESET}"

def print_result(status, elapsed_s, error=None):
    idx = next_index()
    ms  = elapsed_s * 1000
    s   = status_color(status)
    err = f"  ({error})" if error else ""
    print(f"  #{idx}  {s}  {ms:.0f}ms{err}")

def print_summary(results):
    total     = len(results)
    successes = sum(1 for r in results if r[0] and 200 <= r[0] < 400)
    failures  = total - successes
    times     = [r[1] for r in results if r[1] is not None]
    avg = (sum(times) / len(times) * 1000) if times else 0
    mn  = min(times) * 1000 if times else 0
    mx  = max(times) * 1000 if times else 0

    print()
    print(f"  total {total}  ok {successes}  fail {failures}")
    print(f"  avg {avg:.0f}ms  min {mn:.0f}ms  max {mx:.0f}ms")
