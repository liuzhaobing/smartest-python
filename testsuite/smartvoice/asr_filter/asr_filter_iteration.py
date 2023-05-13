# -*- coding:utf-8 -*-
import json
import os.path

import util.util
from api.client.database_client import MySQL, MongoDB
from api.client.mmue_client import AgentManage
from main import DATABASE_CONFIG, DATA_DIR
from util.util import runner, list_duplicate_removal


def asr_filter_test():
    """用于新版本asr filter 集成到smartvoice后的自动化测试
    Date: 20230512

    用例正集：从线上[杂音无意义]的标注日志中抽取，排除掉命中system_service 的部分
    用例负集：从线上通用QA库的短句中抽取
    DM流程：standard 流程 去掉common_sense_qa和 openkg_qa
    :return:
    """

    def get_negative_cases(query_length: int = 5):
        """
        用例负集：从线上通用QA库的短句中抽取
        """
        cms_mysql = MySQL(**DATABASE_CONFIG.get("smartvoice_cms_mysql"))
        # sql = 'select id, question, answer from fqaitem where is_del="no" and need_push="no"'
        sql = 'select question from fqaitem where is_del="no" and need_push="no"'
        sql_results = cms_mysql(query_string=sql)
        sql_results = list(sql_results)

        def put_questions(args):
            if not args["question"]:
                return ""
            try:
                question_list = json.loads(args["question"])
                if question_list:
                    for q in question_list:
                        if q:
                            if len(q) <= query_length:
                                return q
                return ""
            except Exception as e:
                return ""

        """由于通用库数据量 136w+ 数据量太大 因此使用多线程并行执行"""
        all_questions = runner(put_questions, sql_results, threads=100)
        while "" in all_questions:
            all_questions.remove("")
        all_questions = list_duplicate_removal(all_questions)
        sv_negative_cases = [{"source": "asr_filter", "question": q, "id": all_questions.index(q)} for q in
                             all_questions]
        asr_filter_neg_excel = os.path.join(DATA_DIR, f"asr_filter_neg_{util.util.time_strf_now()}.xlsx")
        util.util.save_data_to_xlsx(sv_negative_cases, filename=asr_filter_neg_excel)
        return sv_negative_cases, asr_filter_neg_excel

    def get_positive_cases():
        """
        用例正集：从线上[杂音无意义]的标注日志中抽取，排除掉命中system_service 的部分
        """
        smartest_mongo = MongoDB(**DATABASE_CONFIG.get("smartest_mongo"))
        sql_results = smartest_mongo.db["asr_filter_results"].find({"source": {"$ne": "system_service"}})
        sql_results = list(sql_results)

        def put_questions(args):
            return args["question"]

        """由于日志数据量 3w+ 数据量太大 因此使用多线程并行执行"""
        all_questions = runner(put_questions, sql_results, threads=100)
        while "" in all_questions:
            all_questions.remove("")
        all_questions = list_duplicate_removal(all_questions)

        sv_positive_cases = [{"source": "asr_filter", "question": q, "id": all_questions.index(q)} for q in
                             all_questions]
        asr_filter_pos_excel = os.path.join(DATA_DIR, f"asr_filter_pos_{util.util.time_strf_now()}.xlsx")
        util.util.save_data_to_xlsx(sv_positive_cases, filename=asr_filter_pos_excel)
        return sv_positive_cases, asr_filter_pos_excel

    def set_dm_flow(dm_name):
        """复制standard DM流程 只关掉fqa 和 openkg_qa
        """
        mmue_client = AgentManage(base_url="https://mmue-dit87.harix.iamidata.com",
                                  username="sevel.liu@cloudminds.com", password="cloud1688")
        resp = mmue_client.get_dm_detail("standard")
        data = resp.json()["data"]
        for i in range(len(data)):
            data[i]["templateName"] = dm_name
            del data[i]["id"]
            if data[i]["dmRoutineName"] in ["fqa", "openkg_qa"]:
                data[i]["isCore"] = False
                data[i]["isOpen"] = False

        if mmue_client.get_dm_detail(dm_name).json()["data"]:
            mmue_client.delete_a_dm(dm_name)
        return mmue_client.create_new_dm(dm_name, dm_detail=data)

    dm = "standard_without_faq_openkg"
    set_dm_flow(dm_name=dm)

    negative_cases = get_negative_cases(query_length=4)
    positive_cases = get_positive_cases()


if __name__ == '__main__':
    asr_filter_test()
