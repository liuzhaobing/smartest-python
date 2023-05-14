# -*- coding:utf-8 -*-
import logging

import grpc
from google.protobuf import json_format

import util.util as util
from api.proto import talk_pb2, talk_pb2_grpc
from main import BASE_DIR


class TalkGRPC:
    def __init__(self, address: str):
        if not util.check_grpc_url(address):
            raise ValueError(f"invalid grpc address: [{address}]")
        self.address = address
        try:
            self.channel = grpc.insecure_channel(address)
            self.stub = talk_pb2_grpc.TalkStub(self.channel)
            logging.info(f"dial grpc address success: {address}")
        except Exception as e:
            logging.error(f"dial grpc address failed: {address} {e}")
            self.channel = None
            self.stub = None

    def __del__(self):
        if self.channel:
            self.channel.close()

    def __call__(self, *args, **kwargs):
        return self.talk(*args, **kwargs)

    def talk(self, *args, **kwargs):
        req = self.talk_request(*args, **kwargs)
        logging.info(json_format.MessageToDict(req))
        try:
            response = self.stub.Talk(req)
            response_json = json_format.MessageToDict(response)
            logging.info(response_json)
            return response_json
        except Exception as e:
            logging.error(f"grpc to {self.address} error: {e}")
            return {}

    def talk_request(self,
                     is_full: bool = True,
                     lang: str = "CH",
                     text: str = "现在几点了",
                     agent_id: int = 1,
                     session_id: str = util.mock_trace_id(),
                     question_id: str = util.mock_trace_id(),
                     event_type: int = 0,
                     env_info: dict = {"devicetype": "ginger"},
                     robot_id: str = "5C1AEC03573747D",
                     tenant_code: str = "cloudminds",
                     position: str = "104.061,30.5444",
                     version: str = "v3",
                     inputContext: str = "",
                     is_ha: bool = False,
                     test_mode: bool = True):

        try:
            return talk_pb2.TalkRequest(is_full=is_full,
                                        agent_id=agent_id,
                                        session_id=session_id,
                                        question_id=question_id,
                                        event_type=event_type,
                                        env_info=env_info,
                                        robot_id=robot_id,
                                        tenant_code=tenant_code,
                                        position=position,
                                        version=version,
                                        inputContext=inputContext,
                                        is_ha=is_ha,
                                        test_mode=test_mode,
                                        asr=talk_pb2.Asr(lang=lang, text=text))
        except Exception as e:
            logging.error(f"make {__name__} error: {e}")
            return None


class StreamTalkGRPC(TalkGRPC):
    @staticmethod
    def yield_message(message):
        yield message

    def talk(self, *args, **kwargs):

        req = self.talk_request(*args, **kwargs)
        logging.info(json_format.MessageToDict(req))
        try:
            responses = self.stub.StreamingTalk(self.yield_message(req))
            responses_json = [json_format.MessageToDict(response) for response in responses]
            logging.info(responses_json)
            return responses_json
        except Exception as e:
            logging.error(f"grpc to {self.address} error: {e}")
            return []


if __name__ == '__main__':
    talk = TalkGRPC(address="172.16.23.85:30811")
    talk_result = talk(text="现在几点了", agent_id=666)

    stream_talk = StreamTalkGRPC(address="172.16.23.85:30811")
    stream_talk_result = stream_talk(text="介绍一下马斯克", agent_id=1740)
