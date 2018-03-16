import os
from model import Dict
import pymongo
client = pymongo.MongoClient("mongodb://m.mywsq.cn:27017")
data_list = open(os.path.join(os.path.dirname(__file__), 'data', 'neg_all_dict.txt'))

if __name__ == '__main__':
    count = len(data_list.readline())
    tmp = 0
    for each in data_list:
        Dict(word=each, type='pos').save()
        tmp += 1
        print(float(tmp) / count)

