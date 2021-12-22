import sys
import os;
from client import Client

if sys.argv[1] == "output": #received stream output
    data = sys.argv[2].split("\n")
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abspath = os.path.join(dir, "bin\\request.json")
    with open(abspath, "w") as f:
        if data[1] == "p1":
            f.write(data[2][9:])