import pickle
from models.model import Model
from pr.pruner import Pruner
from parameters import *
from torch.nn.modules.loss import SmoothL1Loss
from torch.optim import Adam
from torch.autograd import Variable
import torch
from pathlib import Path
import numpy

def train_one_batch(model, optimizer, criterion, input_sequence, price_targets):

    running_loss=0
    # should this be called before each step?
    optimizer.zero_grad()
    output,hidden=model(input_sequence[0])

    for i in range(1,time_length//4):
        # A window where the RNN adapts to the new sequence
        # does not include end
        # how is batch training handled this way?

        # I am hoping for [batch_size, output_size]
        # and [batch_size, hidden_size] type of outputs
        output,hidden=model(input_sequence[i],hidden)

    for i in range(time_length//4, time_length):
        output,hidden=model(input_sequence[i],hidden)
        # TODO need to verify that they are aligned
        loss=criterion(output,price_targets[i])
        loss.backward()
        optimizer.step()
        running_loss+=loss.data[0]

    return running_loss


def train(model, criterion, optimizer, total_batches):

    running_loss = 0.0

    for batch_num in range(total_batches):
        data=pruner.get_batch(time_length,batch_size)

        # get the inputs
        inputs, labels = data

        # wrap them in Variable
        # inputs is a [64,128,9]
        inputs=numpy.asarray(inputs)
        labels=numpy.asarray(labels)
        inputs=torch.Tensor(inputs)
        labels=torch.Tensor(labels)
        inputs, labels = Variable(inputs), Variable(labels)

        last_loss=train_one_batch(model,optimizer,criterion,inputs,labels)

        #
        # # zero the parameter gradients
        # optimizer.zero_grad()
        #
        # # forward + backward + optimize
        # outputs = net(inputs)
        # loss = criterion(outputs, labels)
        # loss.backward()
        # optimizer.step()

        # print statistics
        print_frequency=100
        save_frequency=1000
        running_loss += last_loss
        if batch_num % print_frequency == print_frequency-1:    # print every 2000 mini-batches
            print('[%5d] loss: %.3f' %
                  (batch_num + 1, running_loss / print_frequency))
            running_loss = 0.0
        if batch_num% save_frequency==save_frequency-1:
            print("Saving state dict")
            statedict_path=Path("trainer/state_dict_"+str(batch_num)+".pkl")
            torch.save(model.state_dict(),statedict_path)
    print("Finished training")

if __name__=="__main__":
    pruner = Pruner()
    # batch_input = pruner.get_batch(time_length, batch_size)

    model = Model(input_size=input_size, hidden_size=hidden_size,
                  num_layers=num_layers, bias=True, batch_first=False,
                  dropout=0, bidirectional=False)
    total_batches = 12800

    criterion = SmoothL1Loss()
    optimizer = Adam(model.parameters())

    train(model,criterion,optimizer,total_batches)