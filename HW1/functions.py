import numpy
import os
import re
import json
from math import log2


def readFiles(route):
    files = os.listdir(route)
    # print(files)
    ans = []
    for file in files:
        if file.find("README") > -1:
            continue
        file_path = os.path.join(route, file)
        with open(file_path) as f:
            lines = f.readlines()
            ans.append(lines[0])
            # if(len(lines) != 1):
            #     print(len(lines))
    return ans


def readTrainData(route):
    data = []
    file_names = os.listdir(route)
    for file_name in file_names:
        if file_name.find('.') > -1:
            continue
        data = data + readFiles(os.path.join(route, file_name))
    return data


def findPath(route, pn, td):
    subdirs = os.listdir(route)
    # for dir in subdirs:
    #     if dir == '.':
    #         continue
    #     route = os.path.join(route, dir)

    files = os.listdir(route)
    for file in files:
        if file.find(pn) > -1:
            second_dir = os.path.join(route, file)
            second_files = os.listdir(second_dir)
            for second_file in second_files:
                if second_file.find(td) > -1:
                    return os.path.join(second_dir, second_file)


# useless info: ?, @, #, %, ...,

def splitData(data):
    text_info = data
    text_info = text_info.lower()
    words = re.findall(r'\b[a-z]+[\']*[a-z]*\b', text_info)
    money = re.findall(r'[$]+[0-9]+[.]*[0-9]*', text_info)
    for index in range(len(money)):
        money[index] = 'Money'

    exclamation = re.findall(r'[!]+', text_info)
    time = re.findall(r'[0-9][0-9][:][0-9][0-9]', text_info)
    for index in range(len(time)):
        time[index] = 'Time'
    pm = re.findall(r'[--]+', text_info)
    # if len(pm) > 0:
    #     print(text_info)

    ans = words + money + exclamation + time + pm
    return ans


def remove_special_characters(data):
    stop_words = ['a', 'an', 'the', 'his', 'her', 'was', 'were', 'is', 'are', 'am']
    special_character = stop_words

    # special_character = []
    processed_data = []
    for word_index, word in enumerate(data):
        if word in special_character:
            continue

        # if word.find('$') > -1:
        #     # word = '$'
        #     print(word)

        processed_data.append(word)

        # if not word.isalnum():
        #     print(word)
    return processed_data


def featurePreprocess(data):
    processed_data = splitData(data)
    processed_data = remove_special_characters(processed_data)
    return processed_data


def preprocess(nd_files, nt_files, pd_files, pt_files):
    data_x = []
    data_y = []
    for nd_file in nd_files:
        data_x.append(nd_file)
        data_y.append([0, 0])
    for nt_file in nt_files:
        data_x.append(nt_file)
        data_y.append([0, 1])
    for pd_file in pd_files:
        data_x.append(pd_file)
        data_y.append([1, 0])
    for pt_file in pt_files:
        data_x.append(pt_file)
        data_y.append([1, 1])
    # print(data[0][0])
    # print(len(data))
    for index, row in enumerate(data_x):
        data_x[index] = featurePreprocess(row)
    # print(data[0])
    return data_x, data_y


def add_feature(dictation, features):
    for feature in features:
        if feature in dictation:
            dictation[feature] += 1
        else:
            dictation[feature] = 1


class bayes_classifier:
    def __init__(self):

        self.voc_size = 0
        self.nd_size = 0
        self.nt_size = 0
        self.pd_size = 0
        self.pt_size = 0
        self.nd_voc = 0
        self.nt_voc = 0
        self.pd_voc = 0
        self.pt_voc = 0
        self.nd_feature_dict = dict()
        self.nt_feature_dict = dict()
        self.pd_feature_dict = dict()
        self.pt_feature_dict = dict()

    def save(self):
        model = dict()
        model['voc_size'] = self.voc_size

        model['nd_size'] = self.nd_size
        model['nt_size'] = self.nt_size
        model['pd_size'] = self.pd_size
        model['pt_size'] = self.pt_size

        model['nd_voc'] = self.nd_voc
        model['nt_voc'] = self.nt_voc
        model['pd_voc'] = self.pd_voc
        model['pt_voc'] = self.pt_voc

        model['nd_feature_dict'] = self.nd_feature_dict
        model['nt_feature_dict'] = self.nt_feature_dict
        model['pd_feature_dict'] = self.pd_feature_dict
        model['pt_feature_dict'] = self.pt_feature_dict
        with open('nbmodel.txt', 'w+') as f:
            json.dump(model, f)

    def load(self):
        with open('nbmodel.txt', 'r') as f:
            model = json.load(f)
            self.voc_size = model['voc_size']

            self.nd_size = model['nd_size']
            self.nt_size = model['nt_size']
            self.pd_size = model['pd_size']
            self.pt_size = model['pt_size']

            self.nd_voc = model['nd_voc']
            self.nt_voc = model['nt_voc']
            self.pd_voc = model['pd_voc']
            self.pt_voc = model['pt_voc']

            self.nd_feature_dict = model['nd_feature_dict']
            self.nt_feature_dict = model['nt_feature_dict']
            self.pd_feature_dict = model['pd_feature_dict']
            self.pt_feature_dict = model['pt_feature_dict']

    def train(self, data_x, data_y):
        self.nd_voc = 0
        self.nt_voc = 0
        self.pd_voc = 0
        self.pt_voc = 0
        self.voc_size = 0
        voc = set()
        for index, x in enumerate(data_x):
            # print(x)
            for feature in x:
                voc.add(feature)
            if data_y[index][0] == 0 and data_y[index][1] == 0:
                add_feature(self.nd_feature_dict, x)
                self.nd_voc += len(x)
                self.nd_size += 1
            elif data_y[index][0] == 0 and data_y[index][1] == 1:
                add_feature(self.nt_feature_dict, x)
                self.nt_voc += len(x)
                self.nt_size += 1
            elif data_y[index][0] == 1 and data_y[index][1] == 0:
                add_feature(self.pd_feature_dict, x)
                self.pd_voc += len(x)
                self.pd_size += 1
            else:
                add_feature(self.pt_feature_dict, x)
                self.pt_voc += len(x)
                self.pt_size += 1

        self.voc_size = len(voc)

        for feature in self.nd_feature_dict:
            self.nd_feature_dict[feature] = \
                log2((self.nd_feature_dict[feature] + 1) / (self.nd_voc + self.voc_size))
        for feature in self.nt_feature_dict:
            self.nt_feature_dict[feature] = \
                log2((self.nt_feature_dict[feature] + 1) / (self.nt_voc + self.voc_size))
        for feature in self.pd_feature_dict:
            self.pd_feature_dict[feature] = \
                log2((self.pd_feature_dict[feature] + 1) / (self.pd_voc + self.voc_size))
        for feature in self.pt_feature_dict:
            self.pt_feature_dict[feature] = \
                log2((self.pt_feature_dict[feature] + 1) / (self.pt_voc + self.voc_size))
        self.save()

    def get_score(self, word, feature_dict, voc_size, voc_len):
        if word in feature_dict:
            return feature_dict[word]
        else:
            return log2(1 / (voc_size + voc_len))

    def test(self, features):
        # print(features)
        self.load()
        nd_score = log2(self.nd_size / (self.nd_size + self.nt_size + self.pd_size + self.pt_size))
        nt_score = log2(self.nt_size / (self.nd_size + self.nt_size + self.pd_size + self.pt_size))
        pd_score = log2(self.pd_size / (self.nd_size + self.nt_size + self.pd_size + self.pt_size))
        pt_score = log2(self.pt_size / (self.nd_size + self.nt_size + self.pd_size + self.pt_size))

        for feature in features:
            nd_score += self.get_score(feature, self.nd_feature_dict, self.voc_size, self.nd_voc)
            nt_score += self.get_score(feature, self.nt_feature_dict, self.voc_size, self.nt_voc)
            pd_score += self.get_score(feature, self.pd_feature_dict, self.voc_size, self.pd_voc)
            pt_score += self.get_score(feature, self.pt_feature_dict, self.voc_size, self.pt_voc)
        max_score = max(nd_score, nt_score, pd_score, pt_score)
        if max_score == nd_score:
            return 'deceptive negative'
        elif max_score == nt_score:
            return 'truthful negative'
        elif max_score == pd_score:
            return 'deceptive positive'
        elif max_score == pt_score:
            return 'truthful positive'


def trainMain(nd_files, nt_files, pd_files,
              pt_files):  # input:negative deceptive, negative truthful, positive deceptive, positive truthful
    data_x, data_y = preprocess(nd_files, nt_files, pd_files, pt_files)
    classifer = bayes_classifier()
    classifer.train(data_x, data_y)
