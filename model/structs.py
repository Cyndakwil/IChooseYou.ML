# TODO Enums/tables for IDs
# TODO get avg values for placeholder unknown pokemon

class Pokemon:
    """ Struct to store pokemon info
    """
    def __init__(self, moves = [], item = None, ability = None, pokemon_type = None,
                 status = None, hp = None, atk = None, df = None, spe = None,
                 spa = None, spd = None):
        """ Constructor
            For unknown pokemon, just call Pokemon()

        args:
        moves   --  List of move IDs.
                    For player pokemon, stores the pokemon's known moves
                    For opponent pokemon, stores all possible moves
        item    -- Item ID
        ability -- Ability ID
        type    -- type ID
        status  -- status ID
        hp      -- Float ranging from [0, 1]
        atk     -- Float. Normalized atk value ranging from [0, 1]
        df      -- Float. Normalized df value ranging from [0, 1]
        spe     -- Float. Normalized spe value ranging from [0, 1]
        spa     -- Float. Normalized spa value ranging from [0, 1]
        spd     -- Float. Normalized spd value ranging from [0, 1]
        """
        self.moves = moves
        self.item = item
        self.ability = ability
        self.type = pokemon_type
        self.status = status
        self.hp = hp
        self.atk = atk
        self.df = df
        self.spe = spe
        self.spa = spa
        self.spd = spd
    
    def from_json(self, json_dict):
        # TODO implement if pokemon are written as json
        pass


class FightState:
    """ Struct to store the state of a fight at a given turn
    """
    def __init__(self): # TODO add arguments to the constructor
        """ Constructor
            values need to be initialized manually for now
        """
        # Global fight state
        self.field_attrib = []          # List of field attribute IDs
        
        # Player state
        self.used_dynamax = False       # Boolean
        self.remaining_dynamax = 0      # Float element of {0, 0.33, 0.66, 1}
        self.side_attrib = []           # List of side attribute IDs
        self.pokemon = [Pokemon() for _ in range(6)]    # Array of pokemon objects
                                                        # (LEADING POKEMON AT IDX 0 and DO NOT CHANGE SIZE)

        # Opponent state
        self.opp_used_dynamax = False   # Boolean
        self.opp_remaining_dynamax = 0  # Float element of {0, 0.33, 0.66, 1}
        self.opp_side_attrib = []       # List of side attribute IDs
        self.opp_pokemon = [Pokemon() for _ in range(6)] # Array of pokemon objects
                                                         # (LEADING POKEMON AT IDX 0 and DO NOT CHANGE SIZE)
        