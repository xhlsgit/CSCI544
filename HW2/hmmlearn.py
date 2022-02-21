import sys
import numpy as np
from functions import load_data, get_matrix, save_model
import json

'''
train_data_path:
hmm-training-data/it_isdt_train_tagged.txt
hmm-training-data/ja_gsd_train_tagged.txt


'''

if __name__ == '__main__':

    # train_data_path = sys.argv[1]
    train_data_path = 'hmm-training-data/it_isdt_train_tagged.txt'
    # print('Loading...')
    processed_data = load_data(train_data_path) # sentence_num * words_num * 2
    # processed_data = processed_data[0:1]
    # print(processed_data)
    # print('Start to learn model...')
    words, tags, transition_matrix, emission_matrix = get_matrix(processed_data)
    # print(words)
    # print(tags)
    # print(transition_matrix)
    # print(emission_matrix)
    save_model(words, tags, transition_matrix, emission_matrix)

    # arr = np.zeros([48, 1])
    # print(arr)



