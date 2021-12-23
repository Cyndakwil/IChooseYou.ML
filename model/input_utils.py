"""
Provides tools for preprocessing input from the showdown simulator.

Functionality:
--------------
one_hot_encode(sarr, dim)
    - Args:
        - (string[]) sarr: Array of string values for a categorical variable (eg. move "tackle", item "heavydutyboots", ability "ironbarbs")
        - (int) dim: Length of the output vector 
    - Returns:
        - One-hot numpy array with the entry corresponding to s set equal to 1
        - Returns zero vector if s is not recognized
"""

