import torch
import torch.nn as nn
import torch.nn.functional as F
from structs import Pokemon, FightState
from utils import one_hot_encode, input_vector_summary
from config import *

class EntityEmbedding(nn.Module):
    """ Entity embedding layer
        Consists of a single trainable linear layer with no bias or activation
    """
    def __init__(self, input_dim, embedding_dim):
        """ Constructor

        args:
        input_dim -- (int) input dimensions
        embedding_dim -- (int) output dimensions
        """
        super(EntityEmbedding, self).__init__()
        self.embedding = nn.Linear(input_dim, embedding_dim, bias = False)
    
    def forward(self, x):
        """ Forward pass through embedding layer

        args:
        x -- (torch.Tensor) input tensor

        returns: (torch.Tensor) embedding
        """
        return self.embedding(x)
    
    def __call__(self, x):
        return self.forward(x)
    
    def idx2vec(self, idx):
        """ Get embedding from an index

        args:
        idx -- (int) index

        returns: (torch.Tensor) embedding of the entity corresponding to idx
        """
        return self.embedding.weight[:, idx]


class InputEncoder(nn.Module):
    """ Handles embedding and encoding of fight data
    """
    def __init__(self):
        """ Constructor
        """
        super(InputEncoder, self).__init__()

        # Embedding models
        self.move2vec = EntityEmbedding(N_MOVE, MOVE_VEC_DIM)
        self.item2vec = EntityEmbedding(N_ITEM, ITEM_VEC_DIM)
        self.ability2vec = EntityEmbedding(N_ABILITY, ABILITY_VEC_DIM)
        self.sideattrib2vec = EntityEmbedding(N_SIDE_ATTRIB, SIDE_ATTRIB_VEC_DIM)
        self.fieldattrib2vec = EntityEmbedding(N_FIELD_ATTRIB, FIELD_ATTRIB_VEC_DIM)
        self.type2vec = EntityEmbedding(N_TYPE, TYPE_VEC_DIM)
        self.status2vec = EntityEmbedding(N_STATUS, STATUS_VEC_DIM)
    
    def encoding(self, fight_states):
        """ Serialize a list of fight_states into a (FN_INPUT_DIM, len(fight_states)) tensor
            Fight states should be in chronological order starting from left to right

        args:
        fight_states -- list of FightState objects
        """
        # List of input subvectors for each fight state
        encoded_subvectors = [[] for _ in range(len(fight_states))]
        for i in range(len(fight_states)):
            state = fight_states[i]
            arr = encoded_subvectors[i] # Reference to relevant array of subvectors
            
            # 1. Battlefield attributes
            field_attrib_oh = one_hot_encode(state.field_attrib, N_FIELD_ATTRIB)
            arr.append(self.fieldattrib2vec(field_attrib_oh))

            # 2. Player info
            # a. Dynamax info
            arr.append(torch.Tensor([state.used_dynamax, state.remaining_dynamax]))

            # b. Side attributes
            side_attrib_oh = one_hot_encode(state.side_attrib, N_SIDE_ATTRIB)
            arr.append(self.sideattrib2vec(side_attrib_oh))

            # c. Pokemon info
            for pokemon in state.pokemon:
                # i. moves
                for move in pokemon.moves:
                    move_oh = one_hot_encode([move], N_MOVE)
                    arr.append(self.move2vec(move_oh))
                
                # ii. items
                item_oh = one_hot_encode(pokemon.items, N_ITEM)
                arr.append(self.item2vec(item_oh) / len(pokemon.items))

                # iii. abilities
                ability_oh = one_hot_encode(pokemon.abilities, N_ABILITY)
                arr.append(self.ability2vec(ability_oh) / len(pokemon.abilities))

                # iv. type
                type_oh = one_hot_encode(pokemon.types, N_TYPE)
                arr.append(self.type2vec(type_oh))

                # v. condition
                status_oh = one_hot_encode([pokemon.status], N_STATUS)
                arr.append(self.status2vec(status_oh))

                # vi. hp and stats and boosts
                arr.append(torch.Tensor([pokemon.hp] + pokemon.base_stats))
                arr.append(torch.Tensor(pokemon.boosts)/6)
            
            # 3. Opponent info
            # a. Dynamax info
            arr.append(torch.Tensor([state.opp_used_dynamax, state.opp_remaining_dynamax]))

            # b. Side attributes
            side_attrib_oh = one_hot_encode(state.opp_side_attrib, N_SIDE_ATTRIB)
            arr.append(self.sideattrib2vec(side_attrib_oh))

            # c. Pokemon info
            for pokemon in state.opp_pokemon:
                # i. moves (Take average of move embeddings)
                move_oh = one_hot_encode(pokemon.moves, N_MOVE)
                arr.append(self.move2vec(move_oh) / len(pokemon.moves))
                
                # ii. items
                item_oh = one_hot_encode(pokemon.items, N_ITEM)
                arr.append(self.item2vec(item_oh) / len(pokemon.items))

                # iii. abilities
                ability_oh = one_hot_encode(pokemon.abilities, N_ABILITY)
                arr.append(self.ability2vec(ability_oh) / len(pokemon.abilities))

                # iv. type
                type_oh = one_hot_encode(pokemon.types, N_TYPE)
                arr.append(self.type2vec(type_oh))

                # v. condition
                status_oh = one_hot_encode([pokemon.status], N_STATUS)
                arr.append(self.status2vec(status_oh))

                # vi. hp and stats
                arr.append(torch.Tensor([pokemon.hp] + pokemon.base_stats))
                arr.append(torch.Tensor(pokemon.boosts)/6)
            

        # Combined input tensor
        encoded = torch.stack([torch.cat(arr) for arr in encoded_subvectors], dim = 1)
        
        # Pad tensor to have 3 columns
        if encoded.shape[1] < 3:
            encoded = torch.cat([torch.zeros(FN_INPUT_DIM, 3 - encoded.shape[1]), encoded], dim = 1)

        return encoded
    
    def __call__(self, fight_states):
        return self.encoding(fight_states)


class FightNet(nn.Module):
    """ Model as specified in pocvketmnans doc
    """
    def __init__(self):
        """ Constructor
        """
        super(FightNet, self).__init__()

        self.output = None # Stores output tensor from previous forward pass

        # Model
        self.dropout = nn.Dropout(p = FN_DROPOUT_P)
        self.lrelu = nn.LeakyReLU(negative_slope = FN_LRELU_NEGATIVE_SLOPE)
        self.sigmoid = nn.Sigmoid()
        self.log_softmax = nn.LogSoftmax(dim = 1)

        self.conv1 = nn.Conv2d(1, 256, (FN_INPUT_DIM, 3), padding = 0, bias = False)
        self.pad_c1 = nn.ConstantPad2d((2, 0, 0, 0), 0)
        self.bn_c1 = nn.BatchNorm2d(256)

        self.conv2 = nn.Conv2d(1, 256, (256, 3), padding = 0, bias = False)
        self.bn_c2 = nn.BatchNorm1d(256)

        self.fc1 = nn.Linear(256, 256)
        self.bn_fc1 = nn.BatchNorm1d(256)

        self.fc2 = nn.Linear(256, 256)
        self.bn_fc2 = nn.BatchNorm1d(256)

        self.fc3 = nn.Linear(256, 256)
        self.bn_fc3 = nn.BatchNorm1d(256)

        self.out_fc = nn.Linear(256, 11)

    def forward(self, x):
        """ Forward pass through network

        args:
        x -- (torch.Tensor (batch, channel, h, w)) input tensor after embedding and concatenation

        returns: (torch.Tensor (11,)) output tensor
        """
        # (batch_size, 1, FN_INPUT_DIM, 3)
        x = self.pad_c1(x)                  # (batch_size, 1, FN_INPUT_DIM, 5)
        x = self.conv1(x)                   # (batch_size, 256, 1, 3)
        x = self.bn_c1(x)
        x = self.lrelu(x)
        x = self.dropout(x)
        x = torch.permute(x, (0, 2, 1, 3))  # (batch_size, 1, 256, 3)

        x = self.conv2(x)                   # (batch_size, 256, 1, 1)
        x = x.view(x.size()[0], 256)        # (batch_size, 256)
        x = self.bn_c2(x)
        x = self.lrelu(x)
        x = self.dropout(x)

        x = x + self.fc1(x) # Skip connection
        x = self.bn_fc1(x)
        x = self.lrelu(x)
        x = self.dropout(x)

        x = x + self.fc2(x) # Skip connection
        x = self.bn_fc2(x)
        x = self.lrelu(x)
        x = self.dropout(x)

        x = x + self.fc3(x) # Skip connection
        x = self.bn_fc3(x)
        x = self.lrelu(x)
        x = self.dropout(x)

        x = self.out_fc(x)                      # (batch_size, 11)
        x[:, :9] = self.log_softmax(x[:, :9])   # Softmax on possible actions
        x[:,  9] = self.sigmoid(x[:,  9])       # Sigmoid on dynamax
        x[:, 10] = self.sigmoid(x[:, 10])       # Sigmoid on win percentage

        self.output = x
        return x
    
    def __call__(self, x):
        return self.forward(x)
    
    def move_prob(self):
        """ Returns output probabilities for each move

        returns: (torch.Tensor (4,) or (batch_size, 4), depending on batch size)
        """
        if not torch.is_tensor(self.output):
            raise AttributeError("Referencing model ouput before forward pass.")
        return torch.exp(self.output[:, :4]).squeeze()
    
    def swap_prob(self):
        """ Returns output probabilities for each move

        returns: (torch.Tensor (4,) or (batch_size, 4), depending on batch size)
        """
        if not torch.is_tensor(self.output):
            raise AttributeError("Referencing model ouput before forward pass.")
        return torch.exp(self.output[:, 4:9]).squeeze()
    
    def dynamax_prob(self):
        """ Returns probability of dynamax

        returns: (torch.Tensor (batch_size,) or (0,), depending on batch size)
        """
        if not torch.is_tensor(self.output):
            raise AttributeError("Referencing model ouput before forward pass.")
        return self.output[:, 9].squeeze()
    
    def win_prob(self):
        """ Returns probability of winning from previously given position

        returns: (torch.Tensor (batch_size,) or (0,), depending on batch size)
        """
        if not torch.is_tensor(self.output):
            raise AttributeError("Referencing model ouput before forward pass.")
        return self.output[:, 10].squeeze()


# Tests
if __name__ == "__main__":
    from random import randint, randrange, random
    from torchinfo import summary

    # Embedding test
    test_embed = EntityEmbedding(5, 8)
    assert torch.equal(test_embed.idx2vec(3), test_embed(torch.Tensor([0, 0, 0, 1, 0])))

    # FightNet test
    test_fn = FightNet()
    x = torch.rand(32, 1, FN_INPUT_DIM, 3)
    y = test_fn(x)
    assert torch.allclose(torch.exp(y)[:, :9].sum(dim = 1), torch.ones(32))
    assert y.shape == (32, 11)
    summary(test_fn, input_size = (32, 1, FN_INPUT_DIM, 3))
    print()
    print("FROM TEST CALL:")
    print("---------------")
    print("Move probabilities:", test_fn.move_prob()[0])
    print("Swap probabilities:", test_fn.swap_prob()[0])
    print("Dynamax probability:", test_fn.dynamax_prob()[0])
    print("Win probability:", test_fn.win_prob()[0])
    print()

    # InputEncoder test
    t1 = [
        Pokemon(
            [randrange(N_MOVE) for _ in range(4)],
            [randrange(N_ITEM)],
            [randrange(N_ABILITY)],
            types = [randrange(N_TYPE) for _ in range(randint(1, 2))],
            status = randrange(N_STATUS),
            hp = random(),
            base_stats = [random() for _ in range(6)],
            boosts = [randint(-6, 6) for _ in range(7)]
        )
        for _ in range(6)
    ]
    t2 = [
        Pokemon(
            hp = 6969,
        )
        for _ in range(6)
    ]

    s = [FightState()]
    s[0].pokemon = t1
    s[0].opp_pokemon = t2
    s[0].side_attrib.append(30)

    test_ie = InputEncoder()
    inpt = test_ie(s)
    assert inpt.shape == x.shape[2:]
    input_vector_summary(inpt[:, 2])
