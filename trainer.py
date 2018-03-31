import pickle

with open("pr/btc_klines_pruned.pkl",'rb') as pickle_file:
    klines_dict=pickle.load(pickle_file)

# the pruner has 120 pairs
# each pair has varied lengths

