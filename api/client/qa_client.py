# -*- coding:utf-8 -*-
import grpc
from google.protobuf import json_format

from api.proto import qa_pb2, qa_pb2_grpc


class SearchQuestion:
    def __init__(self, address: str):
        self.address = address
        self.channel = grpc.insecure_channel(self.address)
        self.stub = qa_pb2_grpc.SearchStub(self.channel)

    def __del__(self):
        self.channel.close()

    def __call__(self,
                 question: str,
                 qgroupId: list[str],
                 agent_id: int = 1,
                 size: int = 20,
                 search: bool = False,
                 filter: bool = False):
        self.message = qa_pb2.SearchQuestionRequest(agentId=agent_id, question=question, qgroupId=qgroupId, size=size,
                                                    filter=qa_pb2.EntityFilter(search=search, filter=filter))
        return json_format.MessageToDict(self.stub.SearchQuestion(self.message))


if __name__ == '__main__':
    es = SearchQuestion(address="10.12.32.86:9000")
    es_result = es(agent_id=191, question="如何值机", qgroupId=[])
    print(es_result)
