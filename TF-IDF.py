import jieba.analyse
from model import Dict

if __name__ == '__main__':
    total = jieba.analyse.extract_tags(
        '不满',
        topK=20, withWeight=True, allowPOS=())
    pos_count = 0
    neg_count = 0
    total_count = len(total)
    for each in total:
        try:
            tmp = Dict.objects.get(word=each[0])
            if tmp.type == 'pos':
                pos_count += each[1]
            elif tmp.type == 'neg':
                neg_count += each[1]
            print(each, tmp.type)
        except:
            print(each, '没找到')
    print(pos_count, neg_count, total_count, float(pos_count - neg_count) / total_count)
