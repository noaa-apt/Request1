"""
CLI argument parser and dispatcher.
"""

import sys
import argparse
from src.http_runner  import run_http
from src.port_scanner import run_portscan
from src.tcp_udp      import run_tcp, run_udp
from src.extras       import run_icmp, run_dns
from src.testall      import run_testall


def _extract_scan_flags(argv):
    cleaned  = []
    any_flag = False
    ports    = None
    for arg in argv:
        if arg == "-any":
            any_flag = True
        elif arg.startswith("-select"):
            parts = arg.split(",")
            try:
                ports = [int(p) for p in parts[1:] if p]
            except ValueError:
                print(f"Bad port list in '{arg}'")
                sys.exit(1)
        else:
            cleaned.append(arg)
    return any_flag, ports, cleaned


def _build_parser():
    p = argparse.ArgumentParser(prog="req1", add_help=True)

    p.add_argument("-n",    type=int, default=1,  metavar="NUM")
    p.add_argument("-c",    type=int, default=1,  metavar="NUM")
    p.add_argument("-k",    action="store_true")
    p.add_argument("-data", type=str, metavar="DATA_OR_FILE")

    m = p.add_mutually_exclusive_group()
    m.add_argument("-get",      action="store_true")
    m.add_argument("-post",     action="store_true")
    m.add_argument("-put",      action="store_true")
    m.add_argument("-delete",   action="store_true")
    m.add_argument("-patch",    action="store_true")
    m.add_argument("-head",     action="store_true")
    m.add_argument("-options",  action="store_true")
    m.add_argument("-postform", action="store_true")
    m.add_argument("-tcp",      action="store_true")
    m.add_argument("-udp",      action="store_true")
    m.add_argument("-icmp",     action="store_true")
    m.add_argument("-dns",      action="store_true")

    p.add_argument("-portscan", action="store_true")
    p.add_argument("-testall",  action="store_true")
    p.add_argument("url", nargs="?")

    return p


def dispatch(argv):
    any_flag, select_ports, argv = _extract_scan_flags(argv)
    parser = _build_parser()

    try:
        args = parser.parse_args(argv)
    except SystemExit:
        raise

    if not args.url and not args.portscan and not args.testall:
        parser.print_help()
        return

    # -testall
    if args.testall:
        if not args.url:
            print("Usage: -testall <url>")
            return
        run_testall(args.url)
        return

    if args.portscan:
        if not any_flag and select_ports is None:
            print("Usage: -portscan -any <url>  or  -portscan -select,80,443 <url>")
            return
        if not args.url:
            print("Missing URL.")
            return
        run_portscan(args.url, any_flag=any_flag, select_ports=select_ports)
        return

    if args.tcp:
        run_tcp(args.url, n=args.n, c=args.c)
        return
    if args.udp:
        run_udp(args.url, n=args.n, c=args.c)
        return
    if args.icmp:
        run_icmp(args.url, n=args.n)
        return
    if args.dns:
        run_dns(args.url)
        return

    method_map = {
        "get":"GET","post":"POST","put":"PUT","delete":"DELETE",
        "patch":"PATCH","head":"HEAD","options":"OPTIONS","postform":"POST",
    }
    method = None
    form   = False
    for flag, verb in method_map.items():
        if getattr(args, flag, False):
            method = verb
            form   = (flag == "postform")
            break

    if method is None:
        print("No method given. Try: help")
        return

    run_http(
        url=args.url, method=method, n=args.n, c=args.c,
        keep_alive=args.k, data_arg=args.data, form=form,
    )
