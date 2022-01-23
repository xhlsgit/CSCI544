import numpy
import os
def readFiles(route):
    files = os.listdir(route)
    # print(files)
    ans = []
    for file in files:
        file_path = os.path.join(route, file)
        with open(file_path) as f:
            lines = f.readlines()
            ans.append(lines)
            # print(lines)
    return ans

def findPath(route, pn, td):
    files = os.listdir(route)
    for file in files:
        if file.find(pn) > -1:
            second_dir = os.path.join(route, file)
            second_files = os.listdir(second_dir)
            for second_file in second_files:
                if second_file.find(td) > -1:
                    return os.path.join(second_dir, second_file)

def preprocess(nd_files, nt_files, pd_files, pt_files):
    data = []
    for nd_file in nd_files:
        data.append([nd_file, "nd"])
    for nt_file in nt_files:
        data.append([nt_file, "nt"])
    for pd_file in pd_files:
        data.append([pd_file, "pd"])
    for pt_file in pt_files:
        data.append([pt_file, "pt"])
    return data


def trainMain(nd_files, nt_files, pd_files, pt_files): # input:negative deceptive, negative truthful, positive deceptive, positive truthful

    data = preprocess(nd_files, nt_files, pd_files, pt_files)

    trainData = []
    nd_len = len(nd_files)
    for index in range(nd_len):

    return 1
