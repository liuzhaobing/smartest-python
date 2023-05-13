# -*- coding:utf-8 -*-
"""
验证faiss流程
"""
import json
import os.path

import requests
from api.client import qqsim_client
from main import DATA_DIR
from util import util

qqsim = qqsim_client.CmQqSimSimilarGRPC("172.16.23.15:32070")


def qqsim_interface(questions: list):
    text_pair = [dict(text_1=questions[0], text_2=questions[i], id=i) for i in range(1, len(questions))]
    response = qqsim(text_pair)
    sorted_data = sorted(response["metadata"]["answers"], key=lambda x: x["score"], reverse=True)  # 按照得分由高至低排序
    return dict(text_pairs=[[j["text1"], j["text2"]] for j in sorted_data], scores=[j["score"] for j in sorted_data])


def es_interface(query: str, agent_id: int = 191, size: int = 20):
    url = "http://172.16.31.100:39200/qa_ch_fit/_search?pretty"

    payload = {
        "query": {
            "bool": {
                "must": {
                    "match": {
                        "question": query
                    }
                },
                "filter": {
                    "term": {
                        "agentId": f"{agent_id}"
                    }
                }
            }
        },
        "from": 0,
        "size": size
    }
    res = requests.request(method="POST", url=url, json=payload)
    response = res.json()
    result = {
        "questions": [],
        "scores": [],
        "qgroupid": []
    }
    for r in response["hits"]["hits"]:
        result["qgroupid"].append(r["_source"]["qgroupId"])
        result["questions"].append(r["_source"]["question"])
        result["scores"].append(r["_score"])
    return result


def faiss_interface(query: str, agent_id: int = 191, threshold: int = 1000, num: int = 10):
    url = "http://172.16.23.85:31356/faiss_search_docs_with_scores"
    res = requests.post(url=url, json=dict(query=query, agent_id=agent_id, threshold=threshold, num=num))
    if res.status_code != 200:
        return {}
    response = res.json()
    response["questions"] = []
    response["answers"] = []
    for i in range(len(response["scores"])):
        pair = response["docs"][i].split("answer:")
        response["questions"].append(pair[0].removeprefix("question:").replace(" ", ""))
        response["answers"].append(pair[-1])
    return response


def load_questions_from_txt(filename, spt: str = ","):
    """读取txt中的测试用例"""
    content = open(filename, "r", encoding="UTF-8").readlines()
    return [c.split(spt)[0] for c in content]


def query_to_faiss_interface(test_cases):
    results = []
    for c in test_cases:
        res = faiss_interface(c["query"])
        results.append(dict(id=c["id"],
                            query=c["query"],
                            questions=json.dumps(res["questions"], ensure_ascii=False),
                            score=json.dumps(res["scores"], ensure_ascii=False),
                            answers=json.dumps(res["answers"], ensure_ascii=False)))
    return results


def query_to_es_interface(test_cases):
    results = []
    for c in test_cases:
        res = es_interface(c["query"])
        results.append(dict(id=c["id"],
                            query=c["query"],
                            questions=json.dumps(res["questions"], ensure_ascii=False),
                            score=json.dumps(res["scores"], ensure_ascii=False),
                            qgroupid=json.dumps(res["qgroupid"], ensure_ascii=False)))
    return results


def query_to_faiss_and_qqsim_and_es(test_cases: list[dict], base_line: float = 0.75):
    """调用faiss 获取到相似q列表 然后调用qqsim算法 同时请求es的结果"""
    results = []
    for c in test_cases:
        faiss_res = faiss_interface(c["query"])
        qqsim_res = qqsim_interface([c["query"]] + faiss_res["questions"])
        es_res = es_interface(c["query"])
        result = dict(id=c["id"],  # 用例编号
                      query=c["query"],  # 测试语句
                      groupid=c["groupid"],  # 期望命中group id
                      faiss_questions=faiss_res["questions"],  # faiss返回的question列表
                      faiss_score=faiss_res["scores"],  # faiss返回的score列表
                      faiss_answers=faiss_res["answers"],  # faiss返回的answer列表
                      qqsim_score=qqsim_res["scores"],  # qqsim返回的score列表(已排序)
                      qqsim_text_pair=qqsim_res["text_pairs"],  # qqsim排序后的query对
                      is_qqsim_hit=qqsim_res["scores"][0] >= base_line,  # query是否命中qqsim(得分有一个高于base_line)
                      es_questions=es_res["questions"],  # es返回的question列表
                      es_scores=es_res["scores"],  # es返回的score列表
                      es_qgroupid=es_res["qgroupid"],  # es返回的group id列表
                      is_es_hit=str(c["groupid"]) in es_res["qgroupid"],  # es返回值中是否包含期望的group id
                      )
        results.append(result)
    return results


if __name__ == '__main__':
    testcase_filename = os.path.join(DATA_DIR, "yuanyao_testcase.xlsx")
    resolve = {
        "positive": {
            "filename": testcase_filename,
            "sheet_name": "positive"
        },
        "negative": {
            "filename": testcase_filename,
            "sheet_name": "negative"
        }
    }
    for key, value in resolve.items():
        cases = util.load_data_from_xlsx(filename=value["filename"], sheet_name=value["sheet_name"])
        filename = os.path.join(DATA_DIR, f"./query_to_faiss_and_qqsim_and_es_{key}.xlsx")
        util.save_data_to_xlsx(query_to_faiss_and_qqsim_and_es(cases), filename)
