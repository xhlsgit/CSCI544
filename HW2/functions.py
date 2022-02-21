import os
import numpy as np
import json
import re

# sentence_num * words_num * 2
def tuple_check(tuple):
    word = tuple[0]
    if not word.isalnum():
        print(tuple)

def preprocess(word):
    digits = re.findall(r'\d', word)
    if len(digits) != 0:
        word = 'NumBer'
    return word


def load_data(path, train=True):
    if train:
        ans = []
        lines = []
        with open(path) as f:
            lines = f.readlines()
            f.close()
        for line in lines:
            # print(line)
            line = line.replace('\n', '')
            pairs = line.split(' ')
            # print(pairs)
            pair_wise = []
            for pair in pairs:
                tuple = pair.rsplit('/', maxsplit=1)
                tuple[0] = preprocess(tuple[0])
                # tuple_check(tuple)
                pair_wise.append(tuple)
            ans.append(pair_wise)
        return ans
    else:
        ans = []
        with open(path) as f:
            lines = f.readlines()
            f.close()
        for line in lines:
            line = line.replace('\n', '')
            words = line.split(' ')
            ans.append(words)
        return ans


def get_matrix(data):
    words = []
    tags = ['BEGIN_']
    for sentence in data:
        for tupler in sentence:
            word = tupler[0]
            tag = tupler[1]
            if word not in words:
                words.append(word)
            if tag not in tags:
                tags.append(tag)
    tags.append('END_')
    # print(words)
    # print(tags)
    # pre_tag = 'BEGIN_'
    # print(tags.index(pre_tag))
    emission_matrix = np.array([[0.01 for _ in range(len(tags))] for _ in range(len(words))]).astype(float)
    for wi in range(len(words)):
        emission_matrix[wi][0] = 0
        emission_matrix[wi][len(tags) - 1] = 0
    transit_matrix = np.array([[0.01 for _ in range(len(tags))] for _ in range(len(tags))]).astype(float)

    for ti in range(len(tags)):
        transit_matrix[len(tags) - 1][ti] = 0  # p[end][tag] = 0
        transit_matrix[ti][0] = 0  # p[tag][begin] = 0
    for sentence in data:
        pre_tag = 'BEGIN_'
        for tupler in sentence:
            word_i = words.index(tupler[0])
            tag_i = tags.index(tupler[1])
            pre_tag_i = tags.index(pre_tag)
            emission_matrix[word_i][tag_i] += 1
            transit_matrix[pre_tag_i][tag_i] += 1
            pre_tag = tupler[1]
        pre_tag_i = tags.index(pre_tag)
        tag_i = tags.index('END_')
        transit_matrix[pre_tag_i][tag_i] += 1
    for ti in range(len(tags)):
        if ti == 0 or ti == len(tags) - 1:
            continue
        w_sum = np.sum(emission_matrix[:, ti])
        emission_matrix[:, ti] /= w_sum

    for ti in range(len(tags)):
        if ti == len(tags) - 1:
            continue
        t_sum = np.sum(transit_matrix[ti, :])
        transit_matrix[ti, :] /= t_sum
    return words, tags, transit_matrix, emission_matrix


def save_model(words, tags, transition_matrix, emission_matrix):
    file = dict()
    file['words'] = words
    file['tags'] = tags
    transition_matrix = transition_matrix.tolist()
    emission_matrix = emission_matrix.tolist()
    file['transition_matrix'] = transition_matrix #[pre_tag, now_tag]
    file['emission_matrix'] = emission_matrix #[words_cnt, tag_cnt]
    with open('hmmmodel.txt', 'w+') as f:
        json.dump(file, f)


class HmmModel:
    def __init__(self):
        self.final_index = -1
        self.orgin_sentence = []
        self.sentence = []
        self.T = []
        self.pre_tag = []
        self.words = []
        self.tags = []
        self.transition_matrix = []
        self.emission_matrix = []

    def load(self):
        with open('hmmmodel.txt', 'r') as f:
            model = json.load(f)
            self.words = model['words']
            self.tags = model['tags']
            self.transition_matrix = model['transition_matrix']
            self.emission_matrix = model['emission_matrix']
            self.transition_matrix = np.array(self.transition_matrix)
            self.emission_matrix = np.array(self.emission_matrix)

    def search(self, word):
        if word in self.words:
            return self.words.index(word)
        else:
            return -1

    def forward(self):
        x = self.sentence
        # print(self.tags)
        self.T = np.zeros([len(self.tags), len(x) + 2])
        self.pre_tag = [[-1 for _ in range(len(x) + 2)] for _ in range(len(self.tags))]
        self.T[0][0] = 1
        wi = 0
        # print(self.sentence)
        # print('transition')
        # print(self.transition_matrix)
        # print('emission')
        # print(self.emission_matrix)
        for word in x:
            # print(word)
            # print(self.T[:, wi])
            wi += 1
            w_dic_i = self.search(word)
            for ti in range(len(self.tags)):
                parr = []
                for pre_ti in range(len(self.tags)):
                    if w_dic_i == -1:
                        prob_f = self.T[pre_ti][wi-1] * self.transition_matrix[pre_ti][ti]
                    else:
                        prob_f = self.T[pre_ti][wi-1] * self.transition_matrix[pre_ti][ti] * self.emission_matrix[w_dic_i][ti]
                    # print(ti, pre_ti, )
                    parr.append(prob_f)
                self.T[ti][wi] = max(parr)
                self.pre_tag[ti][wi] = parr.index(self.T[ti][wi])
        p_final = []
        for ti in range(len(self.tags)):
            prob = self.T[ti][wi] * self.transition_matrix[ti][len(self.tags) - 1]
            p_final.append(prob)
        # print(p_final)
        return p_final.index(max(p_final))

    def backward(self):
        now_ti = self.final_index
        ans = []
        sen_len = len(self.sentence)
        for ind in range(sen_len):
            ans.append(now_ti)
            now_ti = self.pre_tag[now_ti][sen_len - ind]
        ans.reverse()
        str_ans = []
        for ind in ans:
            str_ans.append(self.tags[ind])
        return str_ans

    def get_ans(self):
        self.final_index = self.forward()
        tags_ans = self.backward()
        str_ans = ''
        assert len(self.orgin_sentence) == len(tags_ans)
        for i in range(len(self.orgin_sentence)):
            str_ans += self.orgin_sentence[i] + '/' + tags_ans[i]
            if i != len(self.orgin_sentence) - 1:
                str_ans += ' '
        str_ans += '\n'
        return str_ans

    def solve(self, lines):
        ans = []
        # print('Length of file: ', len(lines))
        ind_line = 0
        # print('Start to tag...')
        for line in lines:
            # print(line)
            ind_line += 1
            # if ind_line % 10 == 0:
            #     print('Solved ', ind_line, ' lines.')
            self.orgin_sentence = line
            self.sentence = []
            for word in line:
                self.sentence.append(preprocess(word))
            # print(self.sentence)
            ans.append(self.get_ans())
        # print('start writing output')
        with open('hmmoutput.txt', 'w+') as f:
            for line in ans:
                f.write(line)
        f.close()



