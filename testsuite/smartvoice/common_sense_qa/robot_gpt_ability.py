# -*- coding:utf-8 -*-
"""
验证训练集中加入fqa数据后 是否可以关闭common_sense_qa
"""
import os.path

import requests
import util.util
from time import sleep
from api.client.qqsim_client import CmQqSimSimilarGRPC
from api.client.database_client import MongoDB
from main import DATABASE_CONFIG, DATA_DIR

qqsim_grpc = CmQqSimSimilarGRPC(address="172.16.23.15:32070")
smartest_mongo = MongoDB(**DATABASE_CONFIG.get("smartest_mongo"))
qa_results_col = smartest_mongo.db["asr_filter_results"]


def get_score(sentence1, sentence2):
    data = [{"id": 1, "text_1": sentence1, "text_2": sentence2, "es_score": 0}]
    try:
        grpc_call_result = qqsim_grpc(text_pair=data)
        score = grpc_call_result["metadata"]["answers"][0]["score"]
        return score
    except:
        return 0


def record_qqsim_result(data: list, start_point: int = 0):
    new_data = []
    for i in range(start_point, len(data)):
        answer_list = data[i]["exp_answer"].split("&&")
        act_answer = data[i]["act_answer"]
        scores = []
        for exp_answer in answer_list:
            score = get_score(act_answer, exp_answer)
            scores.append(score)
        data[i]["robot_gpt_qqsim_score"] = max(scores)
        new_data.append(data[i])
    return new_data


def check_task_running(job_instance_id: str):
    url = f"http://172.16.23.33:27997/api/v1/history?job_instance_id={job_instance_id}"
    response = requests.request(method="GET", url=url)
    if response.json()["data"]["data"][0]["status"] == 256:
        """运行中"""
        return True
    """已完成"""
    return False


if __name__ == '__main__':
    job_instance_id = "34af0e39-becb-43eb-974c-9a609796ff8c"
    final_results = []
    while True:
        test_results = qa_results_col.find({"job_instance_id": job_instance_id})
        test_results = list(test_results)
        final_results += record_qqsim_result(test_results, len(final_results))

        filename = os.path.join(DATA_DIR, "robot_gpt_and_common_sense_qa_answer_compare_by_qqsim.xlsx")
        util.util.save_data_to_xlsx(final_results, filename)
        if not check_task_running(job_instance_id):
            break
        print("running...", len(final_results))
        sleep(300)
