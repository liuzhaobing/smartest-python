# -*- coding:utf-8 -*-
"""
验证已经纳入训练的QA数据train_qa.jsonl 的生成效果
"""
import os.path
import util.data
from api.client.gpt_client import robot_gpt_http
from main import DATA_DIR, ROBOT_IDS
from util.util import runner

robot_ids = ROBOT_IDS


def test_robot_gpt_content(args):
    robot_id = robot_ids.get()
    res = robot_gpt_http(host="http://172.16.32.201:7080", query=args["content"], robot_id=robot_id)
    robot_ids.put(robot_id)
    result = dict(question=args["content"], exp_answer=args["summary"], act_answer=res, robot_id=robot_id)
    return result


if __name__ == '__main__':
    train_file = os.path.join(DATA_DIR, "train_qa.jsonl")
    train_data = util.data.get_jsonls(train_file)
    all_train_result = runner(test_robot_gpt_content, train_data, threads=5)
    filename = os.path.join(DATA_DIR, f"train_results_{util.util.time_strf_now()}.xlsx")
    util.util.save_data_to_xlsx(all_train_result, filename)
