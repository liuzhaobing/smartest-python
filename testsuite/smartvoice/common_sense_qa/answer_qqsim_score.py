# -*- coding:utf-8 -*-
"""
从测试日志中拉取QA测试数据 对期望answer与实际answer进行qqsim打分
"""
import os

from api.client.database_client import MongoDB
from api.client.qqsim_client import CmQqSimSimilarGRPC
from main import DATABASE_CONFIG, DATA_DIR
import util.util

qqsim_grpc = CmQqSimSimilarGRPC(address="172.16.23.15:32070")
smartest_mongo = MongoDB(**DATABASE_CONFIG.get("smartest_mongo"))
qa_results_col = smartest_mongo.db["qa_results"]


def get_score(sentence1, sentence2):
    data = [{"id": 1, "text_1": sentence1, "text_2": sentence2, "es_score": 0}]
    try:
        grpc_call_result = qqsim_grpc(text_pair=data)
        score = grpc_call_result["metadata"]["answers"][0]["score"]
        return score
    except:
        return 0


if __name__ == '__main__':
    """直接从mongo库里拉数据"""
    job_instance_id = "d6d9faad-9255-4c59-aae3-cfd5f323b674"
    test_results = qa_results_col.find({"job_instance_id": job_instance_id})
    test_results = list(test_results)


    def get_row_max_score(args):
        exp = args["exp_answer"]
        if not isinstance(exp, str):
            args["answer_qqsim_score"] = 0
            return args

        exp_list = exp.split("&&")

        act_answer = args["act_answer"]
        scores = []
        for exp_answer in exp_list:
            score = get_score(act_answer, exp_answer)
            scores.append(score)
        args["answer_qqsim_score"] = max(scores)
        return args


    results = util.util.runner(get_row_max_score, test_results, threads=6)
    util.util.save_data_to_xlsx(results, os.path.join(DATA_DIR, f"{job_instance_id}_{util.util.time_strf_now()}.xlsx"))

if __name__ == '__main__':
    """从excel中读取数据"""
    filename = os.path.join(DATA_DIR, "common_sense_qa融合RobotGPT效果测试.xlsx")
    sheet_names = [
        "已训练过的QA数据",
        "达闼集团相关的QA数据",
        "通用库随机QA数据"
    ]


    def get_row_max_score(args):
        exp = args["期望回复"]
        if not isinstance(exp, str):
            args["answer_qqsim_score"] = 0
            return args

        exp_list = exp.split("&&")

        act_answer = args["实际回复"]
        scores = []
        for exp_answer in exp_list:
            score = get_score(act_answer, exp_answer)
            scores.append(score)
        args["answer_qqsim_score"] = max(scores)
        return args


    for sheet in sheet_names:
        data = util.util.load_data_from_xlsx(filename, sheet_name=sheet)
        results = util.util.runner(get_row_max_score, data, threads=5)
        util.util.save_data_to_xlsx(results, os.path.join(DATA_DIR, f"{sheet}_{util.util.time_strf_now()}.xlsx"))
