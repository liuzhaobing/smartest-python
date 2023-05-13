# -*- coding:utf-8 -*-
from api.proto import qqsim_pb2, qqsim_pb2_grpc
from util.locust_grpc import GrpcUser
from locust import task, run_single_user
from google.protobuf import json_format


class MyGrpcUser(GrpcUser):
    stub_class = qqsim_pb2_grpc.QqsimServiceStub
    host = "127.0.0.1:50051"

    @task
    def test(self):
        data = [
            {"id": 1, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "后面的机器人是你的朋友吗", "es_score": 0},
            {"id": 2, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你的机器人朋友是谁", "es_score": 0},
            {"id": 3, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "那坏人是你的朋友吗", "es_score": 0},
            {"id": 4, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你们的朋友都是机器人吗", "es_score": 0},
            {"id": 5, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "机器人交个朋友吧", "es_score": 0},
            {"id": 6, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你有机器人朋友吗", "es_score": 0},
            {"id": 7, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "刚才的机器人是你的朋友吗", "es_score": 0},
            {"id": 8, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "机器人朋友你好", "es_score": 0},
            {"id": 9, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "机器人鸣鸣是你的好朋友吗", "es_score": 0},
            {"id": 10, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你和农行的机器人是朋友吗", "es_score": 0},
            {"id": 11, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你后面那些机器人是谁啊", "es_score": 0},
            {"id": 12, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你面前有几个小朋友呀", "es_score": 0},
            {"id": 13, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "小朋友机器人", "es_score": 0},
            {"id": 14, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "机器人有女朋友吗", "es_score": 0},
            {"id": 15, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "朋友说你是可爱的机器人了", "es_score": 0},
            {"id": 16, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你几个朋友啊", "es_score": 0},
            {"id": 17, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "那你把后面那台机器人关掉吧",
             "es_score": 0},
            {"id": 18, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你和农业银行的机器人是朋友吗",
             "es_score": 0},
            {"id": 19, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你有没有机器人朋友", "es_score": 0},
            {"id": 20, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "把你的后面那台机器人关闭吧",
             "es_score": 0},
            {"id": 21, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你是个机器怎么和你交朋友", "es_score": 0},
            {"id": 22, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "那是你女朋友", "es_score": 0},
            {"id": 23, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你有几个好朋友", "es_score": 0},
            {"id": 24, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你有几个男朋友", "es_score": 0},
            {"id": 25, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "朋友那个长沙市是那个省份", "es_score": 0}
        ]
        texts = [json_format.ParseDict(pair, qqsim_pb2.TextPairReqMsg()) for pair in data]
        req = qqsim_pb2.CmQsimSimilarRequest(agent_id=1, trace_id="1", robot_name="小达", texts=texts)
        self.stub.CmQqSimSimilar(req)


if __name__ == '__main__':
    run_single_user(MyGrpcUser)
