import torch
import torch.nn as nn
import torch.nn.functional as F
from structs import Pokemon, FightState

"""
MODEL HYPERPARAMETERS
"""

# Embedding models
N_MOVE = 297
MOVE_VEC_DIM = 50

N_ITEM = 61
ITEM_VEC_DIM = 50

N_ABILITY = 182
ABILITY_VEC_DIM = 50

N_SIDE_ATTRIB = 100
SIDE_ATTRIB_VEC_DIM = 100

N_FIELD_ATTRIB = 20
FIELD_ATTRIB_VEC_DIM = 20

N_TYPE = 18
TYPE_VEC_DIM = 18

N_STATUS = 8
STATUS_VEC_DIM = 8

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
                    1 + 5 + 5
                ) + \
                2 + \
                SIDE_ATTRIB_VEC_DIM + \
                6*(
                    MOVE_VEC_DIM + \
                    ITEM_VEC_DIM + \
                    ABILITY_VEC_DIM + \
                    TYPE_VEC_DIM + \
                    STATUS_VEC_DIM + \
                    1 + 5
                )

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
        """ Serialize a list of 3 fight_states into a (FN_INPUT_DIM, 3) tensor
        """
        # TODO implement InputEncoder encoding function
        return
    
    def __call__(self, fight_states):
        return self.encoding()


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

        self.fc2 = nn.Linear(256, 128)
        self.bn_fc2 = nn.BatchNorm1d(128)

        self.fc3 = nn.Linear(128, 128)
        self.bn_fc3 = nn.BatchNorm1d(128)

        self.out_fc = nn.Linear(128, 11)

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

        x = self.fc2(x)                     # (batch_size, 128)
        x = self.bn_fc2(x)
        x = self.lrelu(x)
        x = self.dropout(x)

        x = x + self.fc3(x) # Skip connection
        x = self.bn_fc3(x)
        x = self.lrelu(x)
        x = self.dropout(x)

        x = self.out_fc(x)                  # (batch_size, 11)
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
