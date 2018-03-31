import pickle
from models.model import Model
from pr.pruner import Pruner
from parameters import *

pruner=Pruner()
batch_input=pruner.get_batch(time_length,batch_size)

model=Model(input_size, hidden_size,
                 num_layers, bias=True, batch_first=False,
                 dropout=0, bidirectional=False)
total_epochs=100
epoch_batches=128
for epoch in total_epochs:
    pass