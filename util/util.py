# -*- coding:utf-8 -*-
import time
import re
import uuid
import logging
from typing import Callable
from tqdm import tqdm
import concurrent.futures
from multiprocessing.pool import ThreadPool
from main import BASE_DIR
import yaml
import pandas as pd


def time_strf_now():
    """返回当前时间格式"""
    return time.strftime("%Y%m%d%H%M%S")


def runner(function: Callable, work_items, threads: int = 5, time_out: int = 30, show_progress: bool = True):
    """多线程执行任务
    :param function: 调用的方法
    :param work_items: 列表数据
    :param threads: 并发数
    :param time_out: 单个并发超时时长控制
    :param show_progress: 是否显示进度条
    :return:
    """

    def worker_thread(args):
        """
        Worker thread for evaluating a single sample.
        """
        while True:
            executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
            future = executor.submit(function, args=args)
            try:
                result = future.result(timeout=time_out)
                return result
            except concurrent.futures.TimeoutError as e:
                executor.shutdown(wait=False)
                logging.info(f"wait future.result timeout [{time_out}] {e}")
                return None

    with ThreadPool(threads) as pool:
        logging.info(f"Running in threaded mode with {threads} threads!")
        iter = pool.imap_unordered(worker_thread, work_items)
        idx_and_result = list(tqdm(iter, total=len(work_items), disable=not show_progress))
    return idx_and_result


def list_duplicate_removal(input_list):
    """列表数据去重"""
    output_list = []
    [output_list.append(v) for v in input_list if v not in output_list]
    return output_list


def load_data_from_xlsx(filename: str, sheet_name: str, **kwargs) -> list[dict]:
    """从excel中读取数据为JSON格式的对象
    Parameters
    ----------

    filename : str
        /home/download/xxx.xlsx
    sheet_name : str
        Sheet1

        | id   | text_1                    | text_2                 |
        | ---- | ------------------ ------ | --------------------- |
        | 1    | 后面的那几个机器人是你的朋友吗 | 后面的机器人是你的朋友吗   |
        | 2    | 后面的那几个机器人是你的朋友吗 | 你的机器人朋友是谁       |
        | 3    | 后面的那几个机器人是你的朋友吗 | 那坏人是你的朋友吗       |
        | 4    | 后面的那几个机器人是你的朋友吗 | 你们的朋友都是机器人吗   |

    Returns
    -------
    list[dict]
        [{"id": 1, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "后面的机器人是你的朋友吗"},
         {"id": 2, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你的机器人朋友是谁"},
         {"id": 3, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "那坏人是你的朋友吗"},
         {"id": 4, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你们的朋友都是机器人吗"}]
    """
    df = pd.read_excel(io=filename, sheet_name=sheet_name, **kwargs)
    return [dict(zip(list(df.columns), line)) for line in df.values]


def save_data_to_xlsx(data: list[dict], filename: str, **kwargs):
    """将JSON格式的数据写入到excel中
    Parameters
    ----------
    data : list[dict]
        [{"id": 1, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "后面的机器人是你的朋友吗"},
         {"id": 2, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你的机器人朋友是谁"},
         {"id": 3, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "那坏人是你的朋友吗"},
         {"id": 4, "text_1": "后面的那几个机器人是你的朋友吗", "text_2": "你们的朋友都是机器人吗"}]
    filename : str
        /home/download/xxx.xlsx

    Returns
    -------
    excel
        | id   | text_1                    | text_2                 |
        | ---- | ------------------ ------ | --------------------- |
        | 1    | 后面的那几个机器人是你的朋友吗 | 后面的机器人是你的朋友吗   |
        | 2    | 后面的那几个机器人是你的朋友吗 | 你的机器人朋友是谁       |
        | 3    | 后面的那几个机器人是你的朋友吗 | 那坏人是你的朋友吗       |
        | 4    | 后面的那几个机器人是你的朋友吗 | 你们的朋友都是机器人吗   |
    """
    return pd.DataFrame(data).to_excel(excel_writer=filename, index=False, **kwargs)


def mock_trace_id():
    return f"{uuid.uuid4()}@cloudminds-test.com.cn"


def check_grpc_url(address: str) -> bool:
    """检查GRPC地址是否合法
    Parameters
    ----------
    address : str
        172.16.23.33:8080

    Returns
    -------
    bool
        True/False
    """
    pattern = re.compile(
        '(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5]):(6[0-5]{2}[0-3][0-5]|[1-5]\d{4}|[1-9]\d{1,3}|[0-9])')
    return True if pattern.match(address) else False


def check_http_url(address: str) -> bool:
    """检查HTTP地址是否合法
        Parameters
        ----------
        address : str
            http://172.16.23.84:32194/nlp-sdk/qqsim

        Returns
        -------
        bool
            True/False
        """
    pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    return True if pattern.match(address) else False


def load_data_from_yaml(filename: str):
    return yaml.load(open(filename, "r", encoding="UTF-8"), Loader=yaml.FullLoader)


def test(args):
    time.sleep(1)


if __name__ == '__main__':
    all_data = []
    for i in range(100):
        all_data.append(i)
    start_time = time.time()
    runner(test, all_data, 20)
    cost = time.time() - start_time
    print(cost)
