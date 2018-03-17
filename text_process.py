# _*_ coding:utf-8 _*_
import jieba
import jieba.posseg as pseg
import jieba.analyse
from jieba import analyse

def segmentation(sentence):
    seg_list = jieba.cut(sentence)
    seg_result = []
    for w in seg_list:
        seg_result.append(w)
    return seg_result


def postagger(sentence):
    pos_data = pseg.cut(sentence)
    pos_list = []
    for w in pos_data:
        pos_list.append((w.word, w.flag))
    return pos_list
'''
def del_stopwords(seg_sent):
	stopwords = open("tyc2.txt",'rb')  # 读取停用词表
	new_sent = []   # 去除停用词后的句子
	for word in seg_sent:
		if word in stopwords:
			continue
		else:
			new_sent.append(word)
	return new_sent
'''
def cut_sentence(words):
	#words = words.decode('utf8')
	start = 0
	i = 0
	token = 'meaningless'
	sents = []
	punt_list = ',.!?;~，。！？；～… '
	#print "punc_list", punt_list
	for word in words:
		#print "word", word
		if word not in punt_list:   # 如果不是标点符号
			#print "word1", word
			i += 1
			token = list(words[start:i+2]).pop()
			#print "token:", token
		elif word in punt_list and token in punt_list:  # 处理省略号
			#print "word2", word
			i += 1
			token = list(words[start:i+2]).pop()
			#print "token:", token
		else:
			#print "word3", word
			sents.append(words[start:i+1])   # 断句
			start = i + 1
			i += 1
	if start < len(words):   # 处理最后的部分
		sents.append(words[start:])
	return sents

def read_lines(filename):
	fp = open(filename,'r', encoding='UTF-8')
	#with open("data.txt", 'r', encoding='UTF-8') as data:
	lines = []
	for line in fp.readlines():
		line = line.strip()
		line = line
		lines.append(line)
	fp.close()
	return lines

# 去除停用词
def del_stopwords(seg_sent):
	stopwords = read_lines("tyc2.txt")  # 读取停用词表
	new_sent = []   # 去除停用词后的句子
	for word in seg_sent:
		if word in stopwords:
			continue
		else:
			new_sent.append(word)
	return new_sent


if __name__ == '__main__':
    test_sentence1 = "这款手机大小合适。"
    test_sentence2 = "这款手机大小合适，配置也还可以，很好用，只是屏幕有点小。。。总之，戴妃+是一款值得购买的智能手机。"
    test_sentence3 = "这手机的画面挺好，操作也比较流畅。不过拍照真的太烂了！系统也不好。"

    seg_result = segmentation(test_sentence2)  # 分词，输入一个句子，返回一个list
    for w in seg_result:
        print(w)
    print('\n')

    new_seg_result = del_stopwords(seg_result)  # 去除停用词
    for w in new_seg_result:
        print (w)
    postagger(test_sentence1)  # 分词，词性标注，词和词性构成一个元组
   # r=cut_sentence(test_sentence2)  # 句子切分
   # lines = read_lines("f://Sentiment_dict/emotion_dict/posdict.txt")
    print(r)

