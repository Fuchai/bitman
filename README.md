## Introduction

This is an application that predicts the price of some cryptocurrency
with machine learning models.

The goal of this project is place automated bets to earn some money.

The purpose of this project is to familiarize myself with time series
prediction with highly discontinuous, high dimensional inputs, which is
going to be my work at Mayo Clinic this summer.

## Modules
### Bridge
Communicates with Binance API.

Bridge will get data from Binance for prediction.

Bridge will relay the model decision to Binance.

### Pruner
Pruner takes in data from Bridge and prune them into PyTorch acceptable
formats.

Pruner takes model decision output and pass it to API-compatible commands.

### Model
This is the statistical model that takes in the pruned data and outputs decisions.
This will likely be a PyTorch model.

Who knows? Maybe SVM or tree? Anything that makes money, right?

Multiple models should be produced and selected for the best performance.


### Trainer

If a neural network model is chosen, then Trainer will train the neural
network model.