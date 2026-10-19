import sys
import os
import shlex
from src.cli import dispatch

BANNER = "  Request1 (1.0.11.0) www.ssb.surf/projects/requestone"

HELP_TEXT = """
HTTP
  -get  -post  -put  -delete  -patch  -head  -options  -postform

Flags
  -n <num>          number of requests
  -c <num>          concurrency
  -k                keep alive
  -data <str|file>  body & form data

Other protocols
  -tcp              raw TCP
  -udp              raw UDP
  -icmp             ICMP ping sweep
  -dns              DNS lookup

Port scanner
  -portscan -any                 scan common ports
  -portscan -select,80,443,22    scan specific ports

Test-all 
  -testall                       fires one request per port per protocol

Examples
  -n 1 -c 1 -get http://example.com
  -n 100 -c 10 -k -get http://example.com
  -n 1 -c 1 -post -data body.txt http://example.com/api
  -n 1 -c 1 -postform -data "user=alice&pass=secret" http://example.com/login
  -n 1 -c 1 -put -data update.txt http://example.com/items/1
  -n 1 -c 1 -delete http://example.com/items/1
  -portscan -any http://example.com
  -portscan -select,80,443,8080 http://example.com
  -n 5 -c 5 -tcp http://example.com:9000
  -dns http://example.com
  -icmp http://example.com
  -testall http://example.com

Shell
  help / clear / exit
"""


def clear_screen():
    os.system("cls" if sys.platform == "win32" else "clear")


def interactive_shell():
    clear_screen()
    print(BANNER)
    print()

    while True:
        try:
            raw = input("req1 > ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            sys.exit(0)

        if not raw:
            continue

        cmd = raw.lower()

        if cmd in ("exit", "quit", "q"):
            print("Goodbye.")
            sys.exit(0)

        if cmd in ("help", "?", "-h", "--help"):
            clear_screen()
            print(BANNER)
            print(HELP_TEXT)
            continue

        if cmd == "clear":
            clear_screen()
            print(BANNER)
            print()
            continue

        try:
            tokens = shlex.split(raw)
        except ValueError as e:
            print(f"Error: {e}")
            continue

        clear_screen()
        print(BANNER)
        print()

        try:
            dispatch(tokens)
        except SystemExit:
            pass
        except Exception as e:
            print(f"Error: {e}")
