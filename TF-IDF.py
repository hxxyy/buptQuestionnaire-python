import jieba.analyse
import jieba.posseg as pseg
from model import Dict
import text_process as tp
# 程度副词词典
mostdict = tp.read_lines('degree_dict/most.txt')   # 权值为2
verydict = tp.read_lines('degree_dict/very.txt')   # 权值为1.5
moredict = tp.read_lines('degree_dict/more.txt')   # 权值为1.25
ishdict = tp.read_lines('degree_dict/ish.txt')   # 权值为0.5
insufficientdict = tp.read_lines('degree_dict/insufficiently.txt')  # 权值为0.25
inversedict = tp.read_lines('degree_dict/inverse.txt')  # 权值为-1


# 2.程度副词处理，根据程度副词的种类不同乘以不同的权值
def match(word, sentiment_value):
    if word in mostdict:
        sentiment_value *= 2.0
    elif word in verydict:
        sentiment_value *= 1.75
    elif word in moredict:
        sentiment_value *= 1.5
    elif word in ishdict:
        sentiment_value *= 1.2
    elif word in insufficientdict:
        sentiment_value *= 0.5
    elif word in inversedict:
        #print "inversedict", word
        sentiment_value *= -1
    return sentiment_value

def single_review_sentiment_score(pinglun_sent):
        total = jieba.analyse.extract_tags(
        pinglun_sent,
        topK=20, withWeight=True, allowPOS=())  #找关键词
        '''
        for each in total:
            try:
                tmp = Dict.objects.get(word=each[0])
                if tmp.type == 'pos':
                    print(each, tmp.type)
                elif tmp.type == 'neg':
                    print(each, tmp.type)
            except:
                print(each, '没找到')
        '''
        seg_sent = tp.segmentation(pinglun_sent)   # 分词
        i = 0    # 记录扫描到的词的位置
        s = 0    # 记录情感词的位置
        pos_count = 0    # 记录该分句中的积极情感得分
        neg_count = 0    # 记录该分句中的消极情感得分

        for each in seg_sent:   # 逐词分析
            try:
                tmp=Dict.objects.get(word=each[0])
                if tmp.type == 'pos':
                    print(each, tmp.type)
                    for w in total:
                        if each == w[0]:
                            pos_count += w[1]
                    pos_count += 1
                    for w in seg_sent[s:i]:
                        pos_count = match(w, pos_count)
                    s = i + 1  # 记录情感词的位置变化

                elif tmp.type == 'neg':  # 如果是消极情感词
                    print(each, tmp.type)
                    for w in total:
                        if each == w[0]:
                            neg_count += w[1]
                    neg_count += 1
                    for w in seg_sent[s:i]:
                       neg_count = match(w, neg_count)
                    s = i + 1  # 记录情感词的位置变化
            except:
                print(each, '没找到')
            i += 1
        total_count = len(total)
        print(pos_count, neg_count, total_count, float(pos_count - neg_count) / total_count)
        return float(pos_count - neg_count) / total_count

if __name__ == '__main__':
    line='小明比较伤心'
    single_review_sentiment_score(line)
    line2 = '小明不伤心'
    single_review_sentiment_score(line2)
    line3 = '小明很伤心'
    single_review_sentiment_score(line3)
    line4 = '小明比较快乐'
    single_review_sentiment_score(line4)
