import json
import numpy as np

with open("stats.json", "r") as rf:
    stats = np.array(json.load(rf))

mean = stats.sum(axis = 0) / stats.shape[0]
stddev = np.sqrt(((stats - mean)**2).sum(axis = 0) / stats.shape[0])

with open("stat_mean.json", "w") as wf:
    json.dump({
        "hp":  mean[0],
        "atk": mean[1],
        "def": mean[2],
        "spa": mean[3],
        "spd": mean[4],
        "spe": mean[5]
    }, wf)

with open("stat_stddev.json", "w") as wf:
    json.dump({
        "hp":  stddev[0],
        "atk": stddev[1],
        "def": stddev[2],
        "spa": stddev[3],
        "spd": stddev[4],
        "spe": stddev[5]
    }, wf)

# TODO DATA SHOULD BE STATS AFTER EVs AND IVs, NOT BASE STATS