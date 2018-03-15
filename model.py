from mongoengine import *
import datetime
from mongoengine import connect

connect('test', host='mywsq.cn')


class Survey(Document):
    oid = ObjectIdField(name='_id')
    user_id = StringField(required=True)
    title = StringField(required=True)
    sub_title = StringField(null=True)
    information = StringField(required=True)
    start_date = DateTimeField(required=True)  # 调查开始时间
    end_date = DateTimeField(required=False)  # 调查结束时间
    datetime = DateTimeField(default=datetime.datetime.now)  # 问卷创建时间


# 问题 实例仅用于问卷的创建
class Question(Document):
    oid = ObjectIdField(name='_id')
    title = StringField(required=True)
    type = StringField(required=True, choices=['单项选择题', '多项选择题', '填空题'])
    required = BooleanField(required=True, default=True)  # 是否必答
    option_list = StringField(default='')  # 选择题选项列表 选项以'|'分割
    survey_oid = StringField(required=True)


# # 问卷填写的结果
# class Result(Document):
#     oid = ObjectIdField(name='_id')
#     user_id = StringField(required=True)


# 每个问题的答案
class Answer(Document):
    oid = ObjectIdField(name='_id')
    user_id = StringField(required=True)
    question_oid = StringField(required=True)
    content = StringField(required=True)  # 多项选择题以`|`分割即可
