import os
from functions import *
import sys

# code: python nbclassify.py /Users/xinhuli/Documents/GitHub/CSCI544/HW1/op_spam_training_data/

if __name__ == "__main__":
    # print(os.path.isdir('positive_polarity'))
    # print(f"Arguments count: {len(sys.argv)}")
    # for i, arg in enumerate(sys.argv):
    #     print(f"Argument {i:>6}: {arg}")
    test_data_path = sys.argv[1]
    # print(os.listdir(test_data_path))
    dirs = os.listdir(test_data_path)
    # print(dirs)
    for dirr in dirs:
        if os.path.isdir(os.path.join(test_data_path, dirr)):
            sub_dirs = os.listdir(os.path.join(test_data_path, dirr))
            # print(sub_dirs)
            for sub_dir in sub_dirs:
                if os.path.isdir(os.path.join(test_data_path, dirr, sub_dir)):
                    sub_sub_dirs = os.listdir(os.path.join(test_data_path, dirr, sub_dir))
                    for sub_sub_dir in sub_sub_dirs:
                        if os.path.isdir(os.path.join(test_data_path, dirr, sub_dir, sub_sub_dir)):
                            test_files = [files for files in os.listdir(os.path.join(test_data_path, dirr, sub_dir, sub_sub_dir))
                                          if ((files.find('txt') > -1) and (files.find('README.txt') <= -1))]
                            # print(test_files)
                            classifier = bayes_classifier()
                            classifier.load()
                            with open('nboutput.txt', 'w+') as f_ans:
                                for file in test_files:
                                    file_path = os.path.join(test_data_path, dirr, sub_dir, sub_sub_dir, file)
                                    with open(file_path) as f:
                                        content = f.readlines()
                                        content = featurePreprocess(content[0])
                                        ans = classifier.test(content)
                                        f_ans.write(ans + ' ' + file_path + '\n')
    print('Test finished!')