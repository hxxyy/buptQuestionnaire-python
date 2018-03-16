import os
from model import Dict
import pymongo

client = pymongo.MongoClient("mongodb://mywsq.cn:27017")
col = client['test'].get_collection('dict')
pos_list = open(os.path.join(os.path.dirname(__file__), 'data', 'pos_all_dict.txt'))
stop_list = open(os.path.join(os.path.dirname(__file__), 'data', 'stop_words.txt'))
neg_list = open(os.path.join(os.path.dirname(__file__), 'data', 'neg_all_dict.txt'))
if __name__ == '__main__':
    print('删除了：', Dict.objects.all().delete())
    tmp = []
    for each in pos_list:
        tmp.append({'word': each.strip(), 'type': 'pos'})
    for each in stop_list:
        tmp.append({'word': each.strip(), 'type': 'stop'})
    for each in neg_list:
        tmp.append({'word': each.strip(), 'type': 'neg'})
    col.insert(tmp)
    print('现有', Dict.objects.count())

#
