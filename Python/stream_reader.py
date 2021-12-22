import sys
import os;
import json;
from client import Client

if sys.argv[1] == "output": #received stream output
    data = sys.argv[2].split("\n")
    dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    abspath = os.path.join(dir, "bin\\request.json")
    with open(abspath, "a") as f:
        for i in range(len(data)):
            if data[i] == "p1":
                f.truncate(0)
                f.write(json.dumps(json.loads(data[i + 1][9:]), indent=4))
        f.close()