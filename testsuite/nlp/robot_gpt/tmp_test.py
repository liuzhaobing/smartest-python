# -*- coding:utf-8 -*-
import os.path
import random
import threading
import time
import uuid

import requests
import concurrent.futures

from multiprocessing.pool import ThreadPool
from tqdm import tqdm

from main import DATA_DIR


def robot_gpt(query: str = "是谁开发的智能系统"):
    flag = 0
    start_time = time.time()
    responses = requests.post(url="http://172.16.32.201:7080/chat_stream",
                              json=dict(
                                  prompt=query,
                                  robotId=f"{uuid.uuid4()}@cloudminds-test.com.cn",
                                  history=[]
                              ),
                              stream=True)
    for chunk in responses.iter_content(decode_unicode=True):
        if chunk:
            if flag == 0:
                edg_cost = time.time() - start_time
            flag += 1
    return edg_cost


total_cost = 0
valid_times = 0


def worker_thread(question):
    while True:
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
        future = executor.submit(robot_gpt, question)
        try:
            result = future.result(timeout=300)
            return result
        except concurrent.futures.TimeoutError as e:
            executor.shutdown(wait=False)
            return 0


def main():
    pth = os.path.join(DATA_DIR, "questions.txt")
    questions = open(pth, "r", encoding="UTF-8").readlines()
    questions = random.sample(questions, 100)

    for threads in range(1, 100):
        with ThreadPool(threads) as pool:
            iter = pool.imap_unordered(worker_thread, questions)
            idx_and_result = list(tqdm(iter, total=len(questions), disable=False))
        count, total = 0, 0
        for item in idx_and_result:
            if item:
                total += item
                count += 1
        with open(os.path.join(os.path.dirname(pth), "./result.txt"), "a") as f:
            content = f"{threads}\t{total / count}\n"
            f.write(content)
            print(content)
        time.sleep(30)


class MyThread(threading.Thread):
    def __init__(self, question):
        threading.Thread.__init__(self)
        self.result = None
        self.question = question

    def run(self):
        self.result = robot_gpt(self.question)

    def get_result(self):
        return self.result


def main2():
    pth = os.path.join(DATA_DIR, "questions.txt")
    old_questions = open(pth, "r", encoding="UTF-8").readlines()
    for threads in range(1, 61):
        for retry in range(10):
            thread_list = []
            out_put = []
            for i in range(threads):
                thread_list.append(MyThread(old_questions[-1]))
            for t in thread_list:
                t.setDaemon(True)
                t.start()
            for t in thread_list:
                t.join()
            for t in thread_list:
                out_put.append(t.get_result())

            max_cost = max(out_put)

            content = f"{threads}\t{max_cost}\n"
            print(content)

            with open(os.path.join(os.path.dirname(pth), "./result2.txt"), "a") as f:
                f.write(content)


if __name__ == '__main__':
    main2()
