import torch
import torch.nn as nn
from torch.nn.modules.rnn import RNN

"""
This is a recurrent network model.
A RNN has a window of 1/4 of the total timestamps to learn the behavior of the curve.
That can be used to adjust the internal state of the RNN.
After 1/4 of the total timestamps, the derivative starts to flow back and guide the training.
"""

class RMM(nn.Module):
    '''
    RMM is a composite of RNN,
    with a dense network in the end
    '''

    def __init__(self,input_size, hidden_size, output_size,
                 dense_layers_count=1, num_layers=1,
                 bias=True,
                 batch_first=False, dropout=0,
                 bidirectional=False):
        super(RMM, self).__init__()
        self.output_size=output_size
        self.rnn=RNN(input_size=input_size,hidden_size=hidden_size,
                                  num_layers=num_layers,bias=bias,batch_first=batch_first,
                                  dropout=dropout,bidirectional=bidirectional)
        # of course, this is a critical line.
        self.dense_layers=nn.ModuleList()
        self.dense_layers_count=dense_layers_count

        try:
            for _ in range(self.dense_layers_count-1):
                self.dense_layers.append(nn.Linear(hidden_size,hidden_size))
            self.dense_layers.append(nn.Linear(hidden_size,output_size))
        except:
            raise

    def forward(self, input, hx=None):
        x, hidden_k=self.rnn(input,hx)
        for _ in range(self.dense_layers_count):
            try:
                x=self.dense_layers[_](x)
            except AttributeError:
                print("what the fuck")
                raise
        return x


