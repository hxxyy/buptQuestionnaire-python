from graphene import *
from model import Survey as Sur
from model import Question as Que
from model import Answer as Ans

from graphene_mongo import MongoengineObjectType, MongoengineConnectionField
from graphene.relay import Node


def obj_copy(origin, result):
    for k, v in origin.__dict__.items():
        result.__setattr__(k, v)
    return result


class Question(MongoengineObjectType):
    class Meta:
        model = Que
        interfaces = (Node,)


class Survey(MongoengineObjectType):
    class Meta:
        model = Sur
        interfaces = (Node,)


# class Result(MongoengineObjectType):
#     class Meta:
#         model = Res
#         interfaces = (Node,)


class Answer(MongoengineObjectType):
    class Meta:
        model = Ans
        interfaces = (Node,)


class AnswerAnalyseItem(ObjectType):
    content = String()
    rating = Int()

    def __init__(self, content):
        self.content = content
        self.rating = 3


class QuestionAnalyseItem(ObjectType):
    oid = ID()
    title = String()
    count = Int()
    rating = Int()
    answer = List(AnswerAnalyseItem)

    def __init__(self, oid):
        tmp = Que.objects.get(oid=oid)
        self.oid = oid
        self.title = tmp.title
        self.count = len(Ans.objects(question_oid=str(tmp.oid)))
        self.rating = 3
        self.answer = []
        for each in Ans.objects(question_oid=oid):
            self.answer.append(AnswerAnalyseItem(content=each.content))


class Query(ObjectType):
    node = Node.Field()
    survey = MongoengineConnectionField(Survey)
    question = MongoengineConnectionField(Question)
    answer = MongoengineConnectionField(Answer)
    question_analyse_item = Field(QuestionAnalyseItem, oid=ID(required=True))
    question_analyse_items = List(QuestionAnalyseItem)

    def resolve_question_analyse_items(self, info):
        tmp = []
        for each in Sur.objects.all():
            for item in Que.objects(survey_oid=str(each.oid)):
                tmp.append(QuestionAnalyseItem(oid=str(item.oid)))
        return tmp

    def resolve_question_analyse_item(self, info, oid):
        return QuestionAnalyseItem(oid=oid)

    # get_question = List(Question,survey_oid=String(required=True))
    #
    # def resolve_get_question(self,info,survey_oid):
    #     Que.objects(survey)


class QuestionInput(InputObjectType):
    title = String(required=True)
    type = String(required=True)
    required = Boolean(required=True)
    option_list = String()  # 选择题选项列表 选项以'|'分割
    survey_oid = String(required=True)


class CreateQuestion(Mutation):
    class Arguments:
        question_input = QuestionInput(required=True)

    question = Field(Question)

    @staticmethod
    def mutate(root, info, question_input):
        tmp = Que()
        tmp = obj_copy(question_input, tmp)
        tmp.save()
        tmp.oid = tmp.auto_id_0
        return CreateQuestion(question=tmp)


class DeleteQuestion(Mutation):
    class Arguments:
        oid = ID(required=True)

    status = Int()

    @staticmethod
    def mutate(root, info, oid):
        return Que.objects(oid=str(oid)).delete()


class SurveyInput(InputObjectType):
    user_id = String(required=True)
    title = String(required=True)
    sub_title = String()
    information = String(required=True)
    start_date = String(required=True)  # 调查开始时间
    end_date = String()  # 调查结束时间


class CreateSurvey(Mutation):
    class Arguments:
        survey_input = SurveyInput(required=True)

    survey = Field(Survey)

    @staticmethod
    def mutate(root, info, survey_input):
        tmp = Sur()
        tmp = obj_copy(survey_input, tmp)
        tmp.save()
        tmp.oid = tmp.auto_id_0
        return CreateSurvey(survey=tmp)


class DeleteSurvey(Mutation):
    class Arguments:
        oid = ID(required=True)

    oid = ID()

    @staticmethod
    def mutate(root, info, oid):
        Sur.objects(oid=str(oid)).delete()
        return DeleteSurvey(oid=oid)


class AnswerInput(InputObjectType):
    user_id = String(required=True)
    question_oid = String(required=True)
    content = String(required=True)  # 多项选择题以`|`分割即可


class CreateAnswer(Mutation):
    class Arguments:
        answer_input = AnswerInput(required=True)

    answer = Field(Answer)

    @staticmethod
    def mutate(root, info, answer_input):
        tmp = Ans()
        tmp = obj_copy(answer_input, tmp)
        tmp.save()
        tmp.oid = tmp.auto_id_0
        return CreateAnswer(answer=tmp)


class DeleteAnswer(Mutation):
    class Arguments:
        oid = ID(required=True)

    status = Int()

    @staticmethod
    def mutate(root, info, oid):
        return Ans.objects(oid=str(oid)).delete()


class Mutation(ObjectType):
    createSurvey = CreateSurvey.Field()
    deleteSurvey = DeleteSurvey.Field()
    createAnswer = CreateAnswer.Field()
    deleteAnswer = DeleteAnswer.Field()
    createQuestion = CreateQuestion.Field()
    deleteQuestion = DeleteQuestion.Field()


schema = Schema(query=Query, mutation=Mutation, types=[Survey, Answer, Question])
