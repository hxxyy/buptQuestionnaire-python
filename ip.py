import os
from model import Dict
import pymongo

client = pymongo.MongoClient("mongodb://mywsq.cn:27017")
col = client['test'].get_collection('dict')
data_list = open(os.path.join(os.path.dirname(__file__), 'data', 'stop_words.txt'))

if __name__ == '__main__':
    tmp = []
    for each in data_list:
        tmp.append({'word': each.rstrip(), 'type': 'pos'})


#
