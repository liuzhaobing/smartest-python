# -*- coding:utf-8 -*-
import requests


def robot_gpt_http(host: str, query: str, robot_id: str, history: list = []):
    resp = requests.post(url=f"{host}/chat_stream", json=dict(prompt=query, robotId=robot_id, history=history))
    return resp.content.decode()
