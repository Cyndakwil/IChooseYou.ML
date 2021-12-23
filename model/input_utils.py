"""
Provides tools for preprocessing input from the showdown simulator.

Functionality:
--------------
(for more information check docstrings of each function)
one_hot_encode_mia(sarr, topk_moves = -1, topk_items = -1, topk_abilities = -1)
"""

import numpy as np
import json

# Move, item, ability lookup tables
with open("../data/moves.json", "r") as rf:
    ID2MOVE = json.load(rf)
    MOVE2ID = {ID2MOVE[i]: i for i in range(len(ID2MOVE))}
with open("../data/items.json", "r") as rf:
    ID2ITEM = json.load(rf)
    ITEM2ID = {ID2ITEM[i]: i for i in range(len(ID2ITEM))}
with open("../data/abilities.json", "r") as rf:
    ID2ABILITY = json.load(rf)
    ABILITY2ID = {ID2ABILITY[i]: i for i in range(len(ID2ABILITY))}


# Functionality
def one_hot_encode_mia(sarr, topk_moves = -1, topk_items = -1, topk_abilities = -1):
    """
    Returns a one hot vector encoding moves, items, and abilities

    Args:
        - (string[]) sarr: Array of string values for a categorical variable (eg. move "tackle", item "heavydutyboots", ability "ironbarbs")
        - (int) topk_moves: Only encodes moves ranked less than topk_moves based on usage rankings.
                            If value is -1, encode all moves.
        - (int) topk_items: See topk_moves
        - (int) topk_abilities: See topk_moves
    Returns:
        - One-hot numpy array with the entry corresponding to s set equal to 1
        - Returns zero vector if s is not recognized
        - Dimension of output array determined by topk_moves, topk_items, and topk_abilities
            - Will always be just large enough to encode all necessary moves, items, abilities
    """

    if topk_moves == -1:
        topk_moves = len(ID2MOVE)
    if topk_items == -1:
        topk_items = len(ID2ITEM)
    if topk_abilities == -1:
        topk_abilities = len(ID2ABILITY)
    
    n_moves = min(len(ID2MOVE), topk_moves)
    n_items = min(len(ID2ITEM), topk_items)
    n_abilities = min(len(ID2ABILITY), topk_abilities)

    # Compute output dimension necessary to support one hot encoding every move, item, ability type
    output_dim = n_moves + n_items + n_abilities
    
    # Vector is seperated into 3 blocks, one for moves, items, and abilities, in that order.
    moves_start = 0
    items_start = n_moves
    abilities_start = n_moves + n_items
    one_hot_vector = np.zeros(output_dim)

    for s in sarr:
        moveID = MOVE2ID.get(s, None)
        itemID = ITEM2ID.get(s, None)
        abilityID = ABILITY2ID.get(s, None)

        if moveID != None:
            one_hot_vector[moves_start + moveID] = 1
        if itemID != None:
            one_hot_vector[items_start + itemID] = 1
        if abilityID != None:
            one_hot_vector[abilities_start + abilityID] = 1
    
    return one_hot_vector


# TESTS
if __name__ == "__main__":
    # Test lookup tables
    assert ID2MOVE[MOVE2ID[ID2MOVE[0]]] == ID2MOVE[0]
    assert ID2ITEM[ITEM2ID[ID2ITEM[0]]] == ID2ITEM[0]
    assert ID2ABILITY[ABILITY2ID[ID2ABILITY[0]]] == ID2ABILITY[0]

    # Test one_hot_encode_mia
    v = one_hot_encode_mia(["earthquake", "earthquake", "focussash", "yeeet", "intimidate"])
    print("one_hot_encode_mia test:", v, "Shape:", v.shape)
    assert v.sum() == 3
    assert v[MOVE2ID["earthquake"]] == 1
    assert v[len(MOVE2ID) + ITEM2ID["focussash"]] == 1
    assert v[len(MOVE2ID) + len(ITEM2ID) + ABILITY2ID["intimidate"]] == 1
