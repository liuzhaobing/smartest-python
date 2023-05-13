# -*- coding:utf-8 -*-
import logging

import requests
from main import BASE_DIR


class Smartest:
    def __init__(self, base_url: str = "http://172.16.23.33:27997"):
        self.base_url = base_url

    def _request(self, path, *args, **kwargs):
        return requests.request(url=self.base_url + path, *args, **kwargs)

    def smartest_request(self, path, **kwargs):
        response = self._request(path=path, **kwargs)
        logging.info(f'{kwargs.get("method")} {response.status_code} => {path}')
        if response.status_code >= 400:
            try:
                logging.error(f'error message => {response.json()}')
            except Exception as e:
                logging.error(f'error message => {response.content} {e}')
        return response

    def get_plans(self, **kwargs):
        path = f"/api/v1/plan"
        return self.smartest_request(method="GET", path=path, params=kwargs)

    def run_plan(self, plan_id: int):
        path = f"/api/v1/plan/{plan_id}"
        return self.smartest_request(method="POST", path=path)

    def create_plan(self, payload):
        path = f"/api/v1/plan"
        return self.smartest_request(method="POST", path=path, json=payload)

    def get_history(self, **kwargs):
        path = f"/api/v1/history"
        return self.smartest_request(method="GET", path=path, params=kwargs)


if __name__ == '__main__':
    smartest_client = Smartest()
    result = smartest_client.get_history()
    print(result)
