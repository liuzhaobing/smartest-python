# -*- coding:utf-8 -*-
import os.path
import time
from queue import Queue
from locust import User, task, run_single_user, events
from gevent._semaphore import Semaphore

from api.client.talk_client import StreamTalkGRPC
from main import DATA_DIR

all_locusts_spawned = Semaphore()


def on_hatch_complete(**kwargs):
    all_locusts_spawned.release()


events.spawning_complete.add_listener(on_hatch_complete)


class RobotGPTUser(User):
    host = "172.16.23.85:30811"
    agent_id = 1740
    min_wait = 100
    max_wait = 60000

    @task
    def robot_gpt_test(self):
        all_locusts_spawned.wait()

        robot_id = self.robot_ids.get()
        question = self.questions.get()

        start_time, first_cost, response = self.robot_gpt(text=question, robot_id=robot_id, agent_id=self.agent_id)
        self.request_meta["start_time"] = start_time
        self.request_meta["name"] = "/talk"
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

        self.request_meta = dict(request_type="grpc_stream", response=None, exception=None, context=None)
        self.talk_client = StreamTalkGRPC(address=self.host)
        all_locusts_spawned.wait()

    def robot_gpt(self, **kwargs):
        message = self.talk_client.talk_request(**kwargs)
        start_perf_counter, start_time = time.perf_counter(), time.time()
        print(kwargs)
        responses = self.talk_client.stub.StreamingTalk(self.talk_client.yield_message(message))
        print(responses)
        flag, first_cost = 0, 0
        response = ""
        for resp in responses:
            if resp:
                if flag == 0:
                    first_cost = 1000 * (time.perf_counter() - start_perf_counter)
                # response += chunk.decode()
                flag += 1
        return start_time, first_cost, response


if __name__ == '__main__':
    run_single_user(RobotGPTUser)
