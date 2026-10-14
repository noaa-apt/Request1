import sys
import os
BASE = os.path.dirname(os.path.abspath(sys.executable if getattr(sys, "frozen", False) else __file__))
SRC  = os.path.join(BASE, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)
from src.shell import interactive_shell
from src.cli   import dispatch
def main():
    args = sys.argv[1:]
    if args:
        dispatch(args)
    else:
        interactive_shell()
if __name__ == "__main__":
    main()
