import json
from copy import copy
from utils import stripped_lower

# Load id tables
with open("../data/idtables.json", "r") as rf:
    IDTABLES = json.load(rf)

def get_id(table, s):
    return IDTABLES[table].get(stripped_lower(s), 0)

# Load mean and stddev of pokemon stats for z-score normalization
with open("../data/stat_mean.json", "r") as rf:
    STAT_MEAN = list(json.load(rf).values())
with open("../data/stat_stddev.json", "r") as rf:
    STAT_STDDEV = list(json.load(rf).values())

def zscore_normalize(x, mean, stddev):
    return (x - mean)/stddev


class Pokemon:
    """ Struct to store pokemon info
    """
    def __init__(self, moves = [0, 0, 0, 0], items = [0], abilities = [0], types = [0],
                 status = 0, hp = 1, base_stats = None, boosts = [0, 0, 0, 0, 0, 0, 0]):
        """ Constructor
            For unknown values, leave the unknown kwargs blank for default values.

        args:
        moves   --  List of move IDs.
                    For player pokemon, stores the pokemon's known moves (four moves)
                    For opponent pokemon, stores all possible moves      (any number of moves)
        items    -- List of possible item IDs (for known item this will be a one element list)
        abilities -- List of possible ability ID (for known ability this will be a one element list)
        types   -- List of type IDs
        status  -- status ID
        hp      -- Float ranging from [0, 1]
        base_stats -- List of ints, not normalized (ordered [hp, atk, def, spa, spd, spe])
        boosts  -- List of ints ranging from [-6, 6] (ordered [atk, def, spa, spd, spe])
        """
        self.moves = moves
        self.items = items
        self.abilities = abilities
        self.types = types
        self.status = status
        self.hp = hp
        self.base_stats = base_stats or STAT_MEAN # Assume mean stats if stats unknown
        self.boosts = boosts

        # Normalize base_stats
        for i in range(len(self.base_stats)):
            self.base_stats[i] = zscore_normalize(
                self.base_stats[i],
                STAT_MEAN[i],
                STAT_STDDEV[i]
            )


class FightState:
    """ Struct to store the state of a fight at a given turn
    """
    def __init__(self):
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
        self.opp_remaining_dynamax = 0  # Float element of {0, 0.5, 1}
        self.opp_side_attrib = []       # List of side attribute IDs
        self.opp_pokemon = [Pokemon() for _ in range(6)]    # Array of pokemon objects
                                                            # (LEADING POKEMON AT IDX 0 and DO NOT CHANGE SIZE)
    def from_sim_json(self, path, side = 0):
        """ Initializes a FightState object from a request.json file

        args:
        path -- (str) path to request.json file
        side -- (int 0 or 1) specifies which side the ai is on
        """
        opp_side = not side

        # Reset state to default
        self.__init__()

        # Read request.json
        with open(path, "r") as rf:
            state_data = json.load(rf)
        
        # 1. Field attributes
        weather = state_data["field"]["weather"]
        if weather != "":
             self.field_attrib.append(get_id("fa2id", weather))
        
        terrain = state_data["field"]["terrain"]
        if terrain != "":
            self.field_attrib.append(get_id("fa2id", terrain))
        
        for pseudoweather in state_data["field"]["pseudoWeather"].keys():
            self.field_attrib.append(get_id("fa2id", pseudoweather))
        
        # 2. Player attributes
        self.used_dynamax = state_data["sides"][side]["dynamaxUsed"]
        
        # Side attributes
        for sa in state_data["sides"][side]["sideConditions"].keys():
            self.side_attrib.append(get_id("sa2id", sa))

        # Pokemon
        pokemon_unordered = []
        for pokemon in state_data["sides"][side]["pokemon"]:
            pokemon_unordered.append(
                Pokemon(
                    [get_id("move2id", move["id"]) for move in pokemon["moveSlots"]],
                    [get_id("item2id", pokemon["item"])],
                    [get_id("ability2id", pokemon["ability"])],
                    [get_id("type2id", t) for t in pokemon["types"]],
                    get_id("status2id", pokemon["status"]),
                    pokemon["percenthp"],
                    [
                        pokemon["baseStoredStats"]["hp"],
                        pokemon["baseStoredStats"]["atk"],
                        pokemon["baseStoredStats"]["def"],
                        pokemon["baseStoredStats"]["spa"],
                        pokemon["baseStoredStats"]["spd"],
                        pokemon["baseStoredStats"]["spe"],
                    ],
                    [
                        pokemon["boosts"]["atk"],
                        pokemon["boosts"]["def"],
                        pokemon["boosts"]["spa"],
                        pokemon["boosts"]["spd"],
                        pokemon["boosts"]["spe"],
                        pokemon["boosts"]["accuracy"],
                        pokemon["boosts"]["evasion"],
                    ]
                )
            )

            # If fainted, set status to fnt
            if pokemon["fainted"]:
                pokemon_unordered[-1].status = get_id("status2id", "fnt")

        # Use position attribute to order pokemon
        for i in range(len(state_data["sides"][side]["pokemon"])):
            pokemon = state_data["sides"][side]["pokemon"][i]
            self.pokemon[pokemon["position"]] = pokemon_unordered[i]
        
        # Get volatiles
        volatiles = state_data["sides"][side]["volatiles"]
        for volatile in volatiles:
            self.side_attrib.append(get_id("sa2id", volatile["id"]))
            if volatile == "dynamax":
                self.remaining_dynamax = volatile["duration"] / 2

        # 3. Opponent attributes
        self.opp_used_dynamax = state_data["sides"][opp_side]["dynamaxUsed"]
        
        # Side attributes
        for sa in state_data["sides"][opp_side]["sideConditions"].keys():
            self.opp_side_attrib.append(get_id("sa2id", sa))

        # Pokemon
        pokemon_unordered = []
        for pokemon in state_data["sides"][opp_side]["pokemon"]:
            pokemon_unordered.append(
                Pokemon(
                    [get_id("move2id", move["id"]) for move in pokemon["moveSlots"]],
                    [get_id("item2id", pokemon["item"])],
                    [get_id("ability2id", pokemon["ability"])],
                    [get_id("type2id", t) for t in pokemon["types"]],
                    get_id("status2id", pokemon["status"]),
                    pokemon["percenthp"],
                    [
                        pokemon["baseStoredStats"]["hp"],
                        pokemon["baseStoredStats"]["atk"],
                        pokemon["baseStoredStats"]["def"],
                        pokemon["baseStoredStats"]["spa"],
                        pokemon["baseStoredStats"]["spd"],
                        pokemon["baseStoredStats"]["spe"],
                    ],
                    [
                        pokemon["boosts"]["atk"],
                        pokemon["boosts"]["def"],
                        pokemon["boosts"]["spa"],
                        pokemon["boosts"]["spd"],
                        pokemon["boosts"]["spe"],
                        pokemon["boosts"]["accuracy"],
                        pokemon["boosts"]["evasion"],
                    ]
                )
            )

            # If fainted, set status to fnt
            if pokemon["fainted"]:
                pokemon_unordered[-1].status = get_id("status2id", "fnt")

        # Use position attribute to order pokemon
        for i in range(len(state_data["sides"][opp_side]["pokemon"])):
            pokemon = state_data["sides"][opp_side]["pokemon"][i]
            self.opp_pokemon[pokemon["position"]] = pokemon_unordered[i]
        
        # Get volatiles
        volatiles = state_data["sides"][opp_side]["volatiles"]
        for volatile in volatiles:
            self.opp_side_attrib.append(get_id("sa2id", volatile["id"]))
            if volatile["id"] == "dynamax":
                self.opp_remaining_dynamax = volatile["duration"] / 2
