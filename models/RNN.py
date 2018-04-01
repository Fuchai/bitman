import torch
import torch.nn as nn
from torch.nn.modules.rnn import RNN

"""
This is a recurrent network model.
A RNN has a window of 1/4 of the total timestamps to learn the behavior of the curve.
That can be used to adjust the internal state of the RNN.
After 1/4 of the total timestamps, the derivative starts to flow back and guide the training.
"""

class RMM(RNN):

    def __init__(self,input_size, hidden_size,
                 num_layers=1, bias=True, batch_first=False,
                 dropout=0, bidirectional=False):
        super(RMM, self).__init__(input_size=input_size,hidden_size=hidden_size,
                                  num_layers=num_layers,bias=bias,batch_first=batch_first,
                                  dropout=dropout,bidirectional=bidirectional)