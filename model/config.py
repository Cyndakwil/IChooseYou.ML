"""
MODEL HYPERPARAMETERS
"""

# Embedding models
N_MOVE = 298
MOVE_VEC_DIM = 50

N_ITEM = 62
ITEM_VEC_DIM = 50

N_ABILITY = 183
ABILITY_VEC_DIM = 50

N_SIDE_ATTRIB = 101
SIDE_ATTRIB_VEC_DIM = 100

N_FIELD_ATTRIB = 21
FIELD_ATTRIB_VEC_DIM = 20

N_TYPE = 19
TYPE_VEC_DIM = 18

N_STATUS = 8
STATUS_VEC_DIM = 7

# FightNet
FN_DROPOUT_P = 0.5
FN_LRELU_NEGATIVE_SLOPE = 0.01
FN_INPUT_DIM =  FIELD_ATTRIB_VEC_DIM + \
                2 + \
                SIDE_ATTRIB_VEC_DIM + \
                6*(
                    4*MOVE_VEC_DIM + \
                    ITEM_VEC_DIM + \
                    ABILITY_VEC_DIM + \
                    TYPE_VEC_DIM + \
                    STATUS_VEC_DIM + \
                    1 + 6 + 7
                ) + \
                2 + \
                SIDE_ATTRIB_VEC_DIM + \
                6*(
                    MOVE_VEC_DIM + \
                    ITEM_VEC_DIM + \
                    ABILITY_VEC_DIM + \
                    TYPE_VEC_DIM + \
                    STATUS_VEC_DIM + \
                    1 + 6 + 7
                )
