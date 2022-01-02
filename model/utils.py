import re
import torch
from config import *

def stripped_lower(s):
    """ Returns s as lowercase with all non alphanumeric chars stripped
    """
    return re.sub(r"\W+", "", s.lower())


def one_hot_encode(idxs, l):
    """ Returns a one-hot encoded vector of length l
        with all the indices in list idxs set to 1
    """
    out = torch.zeros(l)
    for i in idxs:
        out[i] = 1
    return out


def input_vector_summary(v):
    """ Decomposes and prints info on all the components of an
        individual FightNet input vector

    args:
    v -- FightNet input vector of shape (FN_INPUT_DIM,)
    """
    i = 0
    print(f"BATTLEFIELD ATTRIBUTE EMBEDDING: {v[i : i + FIELD_ATTRIB_VEC_DIM]}")
    i = FIELD_ATTRIB_VEC_DIM

    print("PLAYER TEAM:")
    print("---------------------------------------------")
    print(f"DYNAMAX USED: {v[i]}")
    print(f"REMAINING DYNAMAX: {v[i + 1]}")
    i += 2
    print(f"SIDE ATTRIBUTE EMBEDDING: {v[i : i + SIDE_ATTRIB_VEC_DIM]}")
    print()
    i += SIDE_ATTRIB_VEC_DIM
    print(f"PLAYER POKEMON:")
    print("---------------------------------------------")
    for j in range(6):
        print(f"POKEMON {j + 1}")
        print("MOVE EMBEDDINGS:")
        for k in range(4):
            print(f"    {k + 1}. {v[i : i + MOVE_VEC_DIM]}")
            i += MOVE_VEC_DIM
        print(f"ITEM EMBEDDING: {v[i : i + ITEM_VEC_DIM]}")
        i += ITEM_VEC_DIM
        print(f"ABILITY EMBEDDING: {v[i : i + ABILITY_VEC_DIM]}")
        i += ABILITY_VEC_DIM
        print(f"TYPE EMBEDDING: {v[i : i + TYPE_VEC_DIM]}")
        i += TYPE_VEC_DIM
        print(f"STATUS EMBEDDING: {v[i : i + STATUS_VEC_DIM]}")
        i += STATUS_VEC_DIM
        print(f"HP%: {v[i]}")
        i += 1
        print(f"BASE STATS: {v[i : i + 6]}")
        i += 6
        print(f"BOOSTS: {v[i : i + 7]}")
        i += 7
    print()
    
    print("OPPONENT TEAM:")
    print("---------------------------------------------")
    print(f"DYNAMAX USED: {v[i]}")
    print(f"REMAINING DYNAMAX: {v[i + 1]}")
    i += 2
    print(f"SIDE ATTRIBUTE EMBEDDING: {v[i : i + SIDE_ATTRIB_VEC_DIM]}")
    print()
    i += SIDE_ATTRIB_VEC_DIM
    print(f"OPPONENT POKEMON:")
    print("---------------------------------------------")
    for j in range(6):
        print(f"POKEMON {j + 1}")
        print(f"MOVE EMBEDDINGS: {v[i : i + MOVE_VEC_DIM]}")
        i += MOVE_VEC_DIM
        print(f"ITEM EMBEDDING: {v[i : i + ITEM_VEC_DIM]}")
        i += ITEM_VEC_DIM
        print(f"ABILITY EMBEDDING: {v[i : i + ABILITY_VEC_DIM]}")
        i += ABILITY_VEC_DIM
        print(f"TYPE EMBEDDING: {v[i : i + TYPE_VEC_DIM]}")
        i += TYPE_VEC_DIM
        print(f"STATUS EMBEDDING: {v[i : i + STATUS_VEC_DIM]}")
        i += STATUS_VEC_DIM
        print(f"HP%: {v[i]}")
        i += 1
        print(f"BASE STATS: {v[i : i + 6]}")
        i += 6
        print(f"BOOSTS: {v[i : i + 7]}")
        i += 7
