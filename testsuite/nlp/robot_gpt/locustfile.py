# -*- coding:utf-8 -*-
import os.path
import time
from queue import Queue

import requests
from locust import User, task, run_single_user, events
from gevent._semaphore import Semaphore

from main import DATA_DIR

all_locusts_spawned = Semaphore()


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()


events.spawning_complete.add_listener(on_hatch_complete)


def robot_gpt(host: str, query: str, robot_id: str):
    url = host + "/chat_stream"
    start_perf_counter = time.perf_counter()
    start_time = time.time()

    responses = requests.post(url=url, json=dict(prompt=query, robotId=robot_id, history=[]), stream=True)
    flag, first_cost = 0, 0
    response = ""
    for chunk in responses.iter_content(decode_unicode=True):
        if chunk:
            if flag == 0:
                first_cost = 1000 * (time.perf_counter() - start_perf_counter)
            # response += chunk.decode()
            flag += 1

    return start_time, first_cost, response


class RobotGPTUser(User):
    host = "http://172.16.32.201:7080"
    min_wait = 100
    max_wait = 6000

    @task
    def robot_gpt_test(self):
        all_locusts_spawned.wait()

        robot_id = self.robot_ids.get()
        question = self.questions.get()

        start_time, first_cost, response = robot_gpt(host=self.host, query=question, robot_id=robot_id)
        self.request_meta["start_time"] = start_time
        self.request_meta["name"] = "/chat_stream"
        self.request_meta["response"] = response
        self.request_meta["response_time"] = first_cost
        self.request_meta["response_length"] = len(response)
        if first_cost >= 3000:
            self.request_meta["exception"] = Exception("first chunk cost > 3000 ms")
        self.environment.events.request.fire(**self.request_meta)
        self.questions.put(question)
        self.robot_ids.put(robot_id)

    def on_start(self):
        self.robot_ids = Queue()
        self.questions = Queue()
        for q in open(os.path.join(DATA_DIR, "questions.txt"), "r", encoding="UTF-8").readlines():
            self.questions.put(q.strip())

        for r in open(os.path.join(DATA_DIR, "robot_id.txt"), "r", encoding="UTF-8").readlines():
            self.robot_ids.put(r.strip())

        self.request_meta = dict(request_type="http_stream", response=None, exception=None, context=None)
        all_locusts_spawned.wait()


if __name__ == '__main__':
    run_single_user(RobotGPTUser)
