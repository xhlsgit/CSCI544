import sys
import numpy as np
from functions import load_data, get_matrix, save_model, HmmModel
import json

'''
test_data_path:
hmm-training-data/it_isdt_dev_raw.txt
hmm-training-data/ja_gsd_dev_raw.txt


'''



if __name__ == '__main__':
    test_data_path = sys.argv[1]
    # test_data_path = 'hmm-training-data/it_isdt_dev_raw.txt'
    input_data = load_data(test_data_path, train=False)
    input_data = input_data
    hmm_model = HmmModel()
    hmm_model.load()
    hmm_model.solve(input_data)



