# -*- coding:utf-8 -*-
import re
import time
from typing import Callable, Any

import grpc
import grpc.experimental.gevent as grpc_gevent
from locust import User
from locust.env import Environment
from locust.exception import LocustError
from grpc_interceptor import ClientInterceptor

grpc_gevent.init_gevent()


class GrpcInterceptor(ClientInterceptor):
    def __init__(self, environment: Environment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.environment = environment
        self.request_meta = dict(request_type="grpc", response=None, exception=None, context=None)

    def intercept(self, method: Callable, request_or_iterator: Any, call_details: grpc.ClientCallDetails):
        self.request_meta["start_time"], start_perf_counter = time.time(), time.perf_counter()
        self.request_meta["name"] = call_details.method

        response = method(request_or_iterator, call_details)
        response_result = response.result()

        self.request_meta["response"] = response
        self.request_meta["response_time"] = 1000 * (time.perf_counter() - start_perf_counter)
        self.request_meta["response_length"] = response_result.ByteSize()

        self.environment.events.request.fire(**self.request_meta)
        return response


class GrpcUser(User):
    abstract = True
    stub_class = None
    insecure: bool = True

    def __init__(self, environment):
        super().__init__(environment)
        if self.host is None:
            raise LocustError(
                "You must specify the base host. Either in the host attribute in the User class, or on the command line using the --host option."
            )
        if not re.match(
                r"^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\:([0-9]|[1-9]\d{1,3}|[1-5]\d{4}|6[0-5]{2}[0-3][0-5])$",
                self.host, re.I):
            raise LocustError(f"Invalid host (`{self.host}`), must be a valid grpc URL. E.g. 127.0.0.1:50051")

        self._channel = grpc.insecure_channel(self.host)
        interceptor = GrpcInterceptor(environment=environment)
        self._channel = grpc.intercept_channel(self._channel, interceptor)
        self.stub = self.stub_class(self._channel)
