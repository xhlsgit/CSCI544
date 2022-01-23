import os
from functions import *
import sys
import random

train_data_path = "/Users/xinhuli/Documents/GitHub/CSCI544/HW1/op_spam_training_data/"
# nd_path = train_data_path + "negative_polarity/deceptive_from_MTurk/"
# nt_path = train_data_path + "negative_polarity/truthful_from_Web/"
# pd_path = train_data_path + "positive_polarity/deceptive_from_MTurk/"
# pt_path = train_data_path + "positive_polarity/truthful_from_TripAdvisor/"
fold_names = ["fold1", "fold2", "fold3", "fold4"]
if __name__ == "__main__":
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")

    nd_dir_path = findPath(train_data_path, "negative", "deceptive")
    nt_dir_path = findPath(train_data_path, "negative", "truthful")
    pd_dir_path = findPath(train_data_path, "positive", "deceptive")
    pt_dir_path = findPath(train_data_path, "positive", "truthful")

    # example_files = readFiles(os.path.join(nd_dir_path, fold_names[0]))
    # print(len(example_files))

    # train&test for negative deceptive
    nd_train_files = []
    nd_test_label = random.randint(0, 3)
    for index in range(0, 4):
        if index != nd_test_label:
            read_files = readFiles(os.path.join(nd_dir_path, fold_names[index]))
            for read_file in read_files:
                nd_train_files.append(read_file)
    # print(len(nd_train_files))
    nd_test_files = readFiles(os.path.join(nd_dir_path, fold_names[nd_test_label]))

    # train&test for negative truthful
    nt_train_files = []
    nt_test_label = random.randint(0, 3)
    for index in range(0, 4):
        if index != nt_test_label:
            read_files = readFiles(os.path.join(nt_dir_path, fold_names[index]))
            for read_file in read_files:
                nt_train_files.append(read_file)
    # print(len(nd_train_files))
    nt_test_files = readFiles(os.path.join(nt_dir_path, fold_names[nt_test_label]))

    # train&test for positive deceptive
    pd_train_files = []
    pd_test_label = random.randint(0, 3)
    for index in range(0, 4):
        if index != pd_test_label:
            read_files = readFiles(os.path.join(pd_dir_path, fold_names[index]))
            for read_file in read_files:
                pd_train_files.append(read_file)
    # print(len(nd_train_files))
    pd_test_files = readFiles(os.path.join(pd_dir_path, fold_names[pd_test_label]))

    # train&test for positive truthful
    pt_train_files = []
    pt_test_label = random.randint(0, 3)
    for index in range(0, 4):
        if index != pt_test_label:
            read_files = readFiles(os.path.join(pt_dir_path, fold_names[index]))
            for read_file in read_files:
                pt_train_files.append(read_file)
    # print(len(nd_train_files))
    pt_test_files = readFiles(os.path.join(pt_dir_path, fold_names[pt_test_label]))

    # start to do pre-train


    # now we have train&test files for nd, nt, pd, pt
    trainMain(nd_train_files, nt_train_files, pd_train_files, pt_train_files)

    # for fold_index in range(4):
    #     train_data =
