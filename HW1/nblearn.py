import os
from functions import *
import sys
import random

# code:  python nblearn.py /Users/xinhuli/Documents/GitHub/CSCI544/HW1/op_spam_training_data/

# fold_names = ["fold1", "fold2", "fold3", "fold4"]
if __name__ == "__main__":
    print(f"Arguments count: {len(sys.argv)}")
    for i, arg in enumerate(sys.argv):
        print(f"Argument {i:>6}: {arg}")
    train_data_path = sys.argv[1]
    nd_dir_path = findPath(train_data_path, "negative", "deceptive")
    nt_dir_path = findPath(train_data_path, "negative", "truthful")
    pd_dir_path = findPath(train_data_path, "positive", "deceptive")
    pt_dir_path = findPath(train_data_path, "positive", "truthful")
    print(nd_dir_path)
    print(nt_dir_path)
    print(pd_dir_path)
    print(pt_dir_path)
    # example_files = readFiles(os.path.join(nd_dir_path, fold_names[0]))
    # print(len(example_files))

    nd_train_files = readTrainData(nd_dir_path)
    nt_train_files = readTrainData(nt_dir_path)
    pd_train_files = readTrainData(pd_dir_path)
    pt_train_files = readTrainData(pt_dir_path)

    # start to do pre-train
    # now we have train&test files for nd, nt, pd, pt
    trainMain(nd_train_files, nt_train_files, pd_train_files, pt_train_files)
    print("Train finished!!")