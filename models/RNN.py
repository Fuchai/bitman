import torch
import torch.nn as nn
from torch.nn.modules.rnn import RNN

"""
This is a recurrent network model.
"""

class Bitman(nn.Module):

    def __init__(self):
        pass

    def forward(self,input):
        '''
        Takes a vector from t, predict the price at t+1
s
        :param input:
        :return:
        '''
