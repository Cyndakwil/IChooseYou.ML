"""
Stores lookup tables that convert from string names
of moves, items, abilities, volatiles, etc.
into unique indices for one-hot encoding.

NOTE: STRING NAMES ARE ALL LOWERCASE AND HAVE ALL WHITESPACE STRIPPED
"""
import json

# FIELD ATTRIBUTES
ID2FA = [
    "raindance",
    "primordialsea",
    "sunnyday",
    "desolateland",
    "sandstorm",
    "hail",
    "deltastream",
    "echoedvoice",
    "fairylock",
    "gravity",
    "iondeluge",
    "magicroom",
    "mudsport",
    "trickroom",
    "watersport",
    "wonderroom",
    "electricterrain",
    "grassyterrain",
    "mistyterrain",
    "psychicterrain"
]
FA2ID = {ID2FA[i] : i for i in range(len(ID2FA))}


# SIDE ATTRIBUTES
ID2SA = [
    "mist",
    "lightscreen",
    "reflect",
    "craftyshield",
    "luckychant",
    "matblock",
    "quickguard",
    "wideguard",
    "spikes",
    "safeguard",
    "tailwind",
    "toxicspikes",
    "stealthrock",
    "waterpledge",
    "firepledge",
    "grasspledge",
    "stickyweb",
    "auroraveil",
    "pursuit",
    "gmaxsteelsurge",
    "gmaxcannonade",
    "gmaxvolcalith",
    "gmaxvinelash",
    "gmaxwildfire",
    "aquaring",
    "attract",
    "banefulbunker",
    "bide",
    "partiallytrapped",
    "charge",
    "confusion",
    "curse",
    "defensecurl",
    "destinybond",
    "protect",
    "disable",
    "electrify",
    "embargo",
    "encore",
    "endure",
    "focusenergy",
    "followme",
    "foresight",
    "gastroacid",
    "grudge",
    "healblock",
    "helpinghand",
    "imprison",
    "ingrain",
    "kingsshield",
    "laserfocus",
    "leechseed",
    "magiccoat",
    "magnetrise",
    "maxguard",
    "minimize",
    "miracleeye",
    "nightmare",
    "noretreat",
    "obstruct",
    "octolock",
    "powder",
    "powertrick",
    "ragepowder",
    "smackdown",
    "snatch",
    "spikyshield",
    "spotlight",
    "stockpile",
    "substitute",
    "tarshot",
    "taunt",
    "telekinesis",
    "torment",
    "yawn",
    "trapped",
    "trapper",
    "stall",
    "beakblast",
    "twoturnmove",
    "counter",
    "fling",
    "focuspunch",
    "partiallytrapped",
    "gmaxchistrike",
    "dynamax",
    "iceball",
    "lockon",
    "mefirst",
    "mirrorcoat",
    "perishsong",
    "rollout",
    "shelltrap",
    "throatchop",
    "lockedmove",
    "choicelock",
    "mustrecharge",
    "futuremove",
    "healreplacement",
    "gem"
]
SA2ID = {ID2SA[i] : i for i in range(len(ID2SA))}


# TYPE
ID2TYPE = [
    "bug",
    "dark",
    "dragon",
    "electric",
    "fairy",
    "fighting",
    "fire",
    "flying",
    "ghost",
    "grass",
    "ground",
    "ice",
    "normal",
    "poison",
    "psychic",
    "rock",
    "steel",
    "water"
]
TYPE2ID = {ID2TYPE[i] : i for i in range(len(ID2TYPE))}


# STATUS CONDITION
ID2STATUS = [
    "none",
    "brn",
    "par",
    "slp",
    "frz",
    "psn",
    "tox",
    "fnt"
]
STATUS2ID = {ID2STATUS[i] : i for i in range(len(ID2STATUS))}


import json

with open("./moves.json", "r") as rf:
    ID2MOVE = json.load(rf)
MOVE2ID = {ID2MOVE[i] : i for i in range(len(ID2MOVE))}

with open("./items.json", "r") as rf:
    ID2ITEM = json.load(rf)
ITEM2ID = {ID2ITEM[i] : i for i in range(len(ID2ITEM))}

with open("./abilities.json", "r") as rf:
    ID2ABILITY = json.load(rf)
ABILITY2ID = {ID2ABILITY[i] : i for i in range(len(ID2ABILITY))}

def write_json(data, path):
    with open(path, "w") as wf:
        json.dump(data, wf, indent = 4)

if __name__ == "__main__":
    for fa in ID2FA:
        assert ID2FA[FA2ID[fa]] == fa
    for fa in ID2SA:
        assert ID2SA[SA2ID[fa]] == fa
    for fa in ID2TYPE:
        assert ID2TYPE[TYPE2ID[fa]] == fa
    for fa in ID2STATUS:
        assert ID2STATUS[STATUS2ID[fa]] == fa
    for fa in ID2MOVE:
        assert ID2MOVE[MOVE2ID[fa]] == fa
    for fa in ID2ITEM:
        assert ID2ITEM[ITEM2ID[fa]] == fa
    for fa in ID2ABILITY:
        assert ID2ABILITY[ABILITY2ID[fa]] == fa

    write_json(ID2FA, "./tables/id2fa.json")
    write_json(FA2ID, "./tables/fa2id.json")
    write_json(ID2SA, "./tables/id2sa.json")
    write_json(SA2ID, "./tables/sa2id.json")
    write_json(ID2TYPE, "./tables/id2type.json")
    write_json(TYPE2ID, "./tables/type2id.json")
    write_json(ID2STATUS, "./tables/id2status.json")
    write_json(STATUS2ID, "./tables/status2id.json")
    write_json(ID2MOVE, "./tables/id2move.json")
    write_json(MOVE2ID, "./tables/move2id.json")
    write_json(ID2ITEM, "./tables/id2item.json")
    write_json(ITEM2ID, "./tables/item2id.json")
    write_json(ID2ABILITY, "./tables/id2ability.json")
    write_json(ABILITY2ID, "./tables/ability2id.json")
