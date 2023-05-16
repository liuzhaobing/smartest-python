# -*- coding:utf-8 -*-
"""
用于收集通用库中与公司相关的QA数据 并验证RobotGPT生成效果
"""
import json
import os.path

import util.util
from api.client.database_client import MySQL
from api.client.gpt_client import robot_gpt_http
from main import DATABASE_CONFIG, DATA_DIR, ROBOT_IDS

cms_client = MySQL(**DATABASE_CONFIG.get("smartvoice_cms_mysql"))
robot_ids = ROBOT_IDS


def fqaitem_about_iamidata():
    """查询达闼机器人相关fqaitem"""
    inner_cases, cate_ids, result = [], [], [{"cate_id": "51"}]
    while len(result) > 0:
        this_search_pids = [str(it["cate_id"]) for it in result]
        cate_ids += this_search_pids
        result = cms_client(f"""select id cate_id from fqacate 
        where is_del='no' and need_push='no' and pid in ({",".join(this_search_pids)});""")

    data_sql = f""" SELECT id, question, answer, cate_id FROM fqaitem 
        WHERE need_push = "no"  AND is_del = "no" AND cate_id in ({",".join(cate_ids)}); """
    data_result = cms_client(data_sql)

    case_id = 0
    for case in data_result:
        questions = case["question"]
        if type(questions) != str:
            continue
        try:
            questions = json.loads(questions)
            # 去除q中含有空格的部分
            while '' in questions:
                questions.remove('')

            answers = json.loads(case["answer"])
            while '' in answers:
                answers.remove("")

            case_id += 1
            inner_cases.append({
                "id": case_id,
                "question": questions[-1],
                "answer_list": "&&".join(answers),
                "qa_group_id": case["id"],
                "cate_id": case["cate_id"],
            })
        except:
            continue

    filename = os.path.join(DATA_DIR, f"集团相关QA问法_{util.util.time_strf_now()}.xlsx")
    util.util.save_data_to_xlsx(data=inner_cases, filename=filename)
    return inner_cases


def test_robot_gpt_content(args):
    robot_id = robot_ids.get()
    res = robot_gpt_http(host="http://172.16.32.201:7080", query=args["question"], robot_id=robot_id)
    robot_ids.put(robot_id)
    result = dict(question=args["question"], exp_answer=args["answer_list"], act_answer=res, robot_id=robot_id)
    return result


if __name__ == '__main__':
    test_cases = fqaitem_about_iamidata()
    all_test_result = util.util.runner(test_robot_gpt_content, test_cases, threads=5)
    filename = os.path.join(DATA_DIR, f"集团相关QA问法测试结果_{util.util.time_strf_now()}.xlsx")
    util.util.save_data_to_xlsx(all_test_result, filename)
