# -*- coding:utf-8 -*-
import json
import requests
import logging
import urllib3
from main import BASE_DIR

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class MMUE:
    HEADERS = None

    def __init__(self, base_url, username, password):
        self.base_url, self.username, self.__password = base_url, username, password
        self.HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                                      "(KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"}
        self.login_data = None
        self.__login()

    def __request(self, path, headers=HEADERS, *args, **kwargs):
        return requests.request(url=self.base_url + path, headers=headers, verify=False, *args, **kwargs)

    def __login(self):
        response = self.__request(method="POST", path="/mmue/api/login",
                                  json={"username": self.username, "pwd": self.__password,
                                        "captchaid": "5555", "authcode": "5555"})
        if response.status_code == 200:
            response_data = response.json()["data"]
            self.HEADERS["Authorization"] = response_data["token"]
            if not response_data.__contains__("data"):
                logging.error(f"user {self.username} login failed!")
                self.login_data = None
                return False
            self.login_data = response_data["data"]
            """enumerate in [user_name, user_id, user_power, tenant_name, tenant_id, tenant_logo, otype]"""
            logging.info(f"user {self.username} login success!")
            return True
        else:
            logging.error(f"user {self.username} login failed!")
            self.login_data = None
            return False

    def mmue_request(self, path, *args, **kwargs):
        response = self.__request(path=path, *args, **kwargs)
        logging.info(f'{kwargs.get("method")} {response.status_code} => {path}')
        if response.status_code >= 400:
            try:
                logging.error(f'error message => {response.json()}')
            except Exception as e:
                logging.error(f'error message => {response.content} {e}')
        return response

    def talk(self, payload):
        """
        :param payload:  = {"text": "现在几点了",
                           "agent_id": 666,
                           "env": "87",
                           "tanant_code": "cloudminds",
                           "event_type": 0,
                           "robot_id": "5C1AEC03573747D",
                           "session_id": "liuzhaobing@cloudminds",
                           "event_info": {}}
        :return:
        """
        url = "/v1/sv/talk"
        self.HEADERS["authinfo"] = json.dumps({"userid": self.login_data["user_id"], "username": self.username,
                                               "lang": "zh-CN", "agentid": 1})
        return self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)


class UserManage(MMUE):
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)
        auth_info = {"username": self.username, "userid": self.login_data["user_id"], "lang": "zh-CN", "agentid": None}

        """sv 接口需要auth info  在调用sv接口时，需给headers重新赋值 self.HEADERS  在调用mmue接口时不需要此操作"""
        self.HEADERS["authinfo"] = json.dumps(auth_info, ensure_ascii=False)

    def user_add_new(self, username, password, tenant_code):
        """
        注册 MMUE 用户
        :param username: 用户名
        :param password: 密码
        :param tenant_code: 租户名称
        :return: 用户 id
        """
        url = "/mmue/api/sso/create/user"
        payload = {
            "username": username,
            "password": password,
            "tenantcode": tenant_code
        }
        response = self.mmue_request(method="POST", path=url, json=payload)
        if response.status_code != 200:
            logging.error(f"request to {url} failed with status code {response.status_code}")
            return None
        res = response.json()
        if res["status"]:
            user_id = response.json()["data"]
            logging.info(f"user {username} create succeed: user_id={user_id}")
            return user_id
        else:
            logging.warning(f"user {username} create failed reason: {res['msg']}")
            return None

    def get_tenant_list(self):  # unusable 不可用
        """获取 租户列表"""
        url = "/mmue/api/tenant"
        return self.mmue_request(method="POST", path=url)

    def get_scene_list(self):
        """获取 客户场景列表"""
        url = "/sv-api/v2/ux/scenetpl/list?keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_robot_char_list(self):
        """获取 场景人设列表"""
        url = "/mmue/api/robotchar/search"
        payload = {"char_name": ""}
        return self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)

    def get_skill_type_list(self):
        """获取 技能类型列表"""
        url = "/sv-api/v2/ux/skilltpl/list?keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_dm_template_list(self):
        """获取 DM流程模板列表"""
        url = "/sv-api/v2/ux/dmtemplate/list?page=1&pagesize=100000&keyword="
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def agent_add_new(self, tenant_code, agent_name, scenetplid, scenecharid, skilltplid,
                      language, timezone, longitude, latitude, dm_name):
        """
        角色创建
        :param tenant_code: 租户名称
        :param agent_name: 角色名称
        :param scenetplid: 客户场景      id     get_scene_list()
        :param skilltplid: 技能类型      id     get_skill_type_list()
        :param scenecharid: 场景人设     id     get_robot_char_list()
        :param language: 语言     zh-CN
        :param timezone: 时区     UTC+8
        :param longitude: 经度
        :param latitude: 纬度
        :param dm_name: DM流程                 get_dm_template_list()
        :return: agent_id: 角色id
        """
        url = "/sv-api/v2/ux/agents/add"
        try:
            payload = {"tenantcode": tenant_code,
                       "agentname": agent_name,
                       "dflanguage": "zh-CN",
                       "language": language,
                       "latitude": str(latitude),
                       "longitude": str(longitude),
                       "dmName": dm_name,
                       "timezone": timezone,
                       "scenetplid": int(scenetplid),  # 客户场景
                       "scenecharid": int(scenecharid),
                       "skilltplid": int(skilltplid)}
        except Exception as e:
            logging.error(f"input param error: {e}")
            return None
        response = self.mmue_request(method="POST", path=url, json=payload, headers=self.HEADERS)
        if response.status_code != 200:
            logging.error(f"request to {url} failed with status code {response.status_code}")
            return None
        res = response.json()
        if not res["status"]:
            logging.warning(f"agent {payload['agentname']} create failed reason: {res['msg']}")
            return None
        agent_id = res["id"]
        logging.info(f"agent {payload['agentname']} create succeed: agent_id={agent_id}")
        return agent_id

    def get_agent_info(self, agent_id):
        """获取 角色信息"""
        url = f"/sv-api/v2/ux/agents/{agent_id}"
        return self.mmue_request(method="GET", path=url, headers=self.HEADERS)

    def get_agent_id_by_name(self, agent_name):
        url = f"/sv-api/v2/ux/agents?tenantcode=&scenecharid=0&agentname={agent_name}&agentid=0&page=100&pagesize=1"
        response = self.mmue_request(method="GET", path=url, headers=self.HEADERS)
        if response.status_code != 200:
            return None
        res = response.json()
        for r in res["data"]:
            if r["agentname"] == agent_name:
                return r["id"]
        return None

    def list_permissions(self):
        """获取 admin 和 user 的权限列表"""
        url = "/mmue/api/permission/list"
        payload = {"system": "mmo", "component": "/app/client#/roles"}
        return self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)

    def get_faq_cate(self):
        """获取 知识库配置列表"""
        url = "/main/fqacate/faqcate"
        return self.mmue_request(method="GET", path=url + f"?token={self.HEADERS['Authorization']}")

    def list_graphs(self):
        """获取 知识图谱库列表"""
        url = "/graph/kg/v1/graph/list"
        payload = {"spaceName": ""}
        return self.mmue_request(method="POST", path=url, json=payload)

    def get_entity_qa_cate(self):
        """获取 实体问答列表"""
        url = "/main/entityqacate/entityqacatetreelist"
        return self.mmue_request(method="GET", path=url + f"?token={self.HEADERS['Authorization']}")

    def agent_update(self, payload):
        """更新 角色信息
        payload = {"tenantcode": "cloudminds", "agentname": "lisi", "dflanguage": "zh-CN", "language": "zh-CN",
                   "latitude": "4", "longitude": "3", "dmName": "standard", "timezone": "UTC+8", "scenetplid": 1,
                   "scenecharid": 32, "skilltplid": 1,
                   # 前面的数据和创建用户时payload是一样的

                   # 这个参数好像也是查agent的时候查出来的
                   "eqaids": [10],

                   # get_faq_cate()
                   "fqaids": [188, 269, 258, 226, 210, 267, 190, 268, 189, 266],

                   # list_graphs()
                   "kgnames": ["common_kg", "db_12429135405209477533", "db_271003567416724429",
                               "zidingyitupu_479963348332101988", "shici_1549937929118056448",
                               "suibiandingyitupu_1551405104245309440",
                               "wangqiangdeceshizhishitupu_5177935683873814830", "db_7338609727454445713",
                               "db_9313390819905066577", "gushi_1555466196884180992", "db_10080664782208135874",
                               "shiciceshi_1557598135343026176", "gushici_1557614812554235904"], "agentid": 1635}
        """
        url = "/sv-api/v2/ux/agents/update"
        return self.mmue_request(method="PATCH", path=url, json=payload)

    def get_custom_robot_labels(self):
        """获取机器人人设标签列表"""
        url = "/mmue/api/robotcharvar/list"
        return self.mmue_request(method="POST", path=url)

    def save_custom_robot_labels(self, payload):
        url = "/mmue/api/robotcharagent/saveval"
        return self.mmue_request(method="POST", path=url, json=payload)

    def bind_agents_to_user(self, username, agents):
        """绑定用户与角色
        payload = {
                  "user_name": "wangerxiao",
                  "agent_ids": ["1638", "1639"]
                 }
        """
        url = "/mmue/api/agent/bind"
        payload = {"user_name": username, "agent_ids": agents}
        response = self.mmue_request(method="POST", path=url + f"?token={self.HEADERS['Authorization']}", json=payload)
        try:
            res = response.json()
            if not res["status"]:
                logging.error(f"bind agents to user failed reason: {res['msg']}")
                return False
            return True

        except Exception as e:
            logging.error(f"bind agents to user failed reason: {e}")
            return False


class AgentManage(MMUE):
    def __init__(self, base_url, username, password):
        super().__init__(base_url, username, password)
        auth_info = {"username": self.username, "userid": self.login_data["user_id"], "lang": "zh-CN", "agentid": None}

        """sv 接口需要auth info  在调用sv接口时，需给headers重新赋值 self.HEADERS  在调用mmue接口时不需要此操作"""
        self.HEADERS["authinfo"] = json.dumps(auth_info, ensure_ascii=False)

    def get_dm_detail(self, dm_name: str = "standard"):
        """获取指定DM流程的详细信息
        :param dm_name:
        :return: {"code":0,"status":true,"data":[{"id":2,"templateName":"standard","dmRoutineName":"user_service","priority":1,"isCore":true,"isOpen":true},{"id":3,"templateName":"standard","dmRoutineName":"user_qa","priority":2,"isCore":true,"isOpen":true},{"id":76,"templateName":"standard","dmRoutineName":"system_service_regex","priority":3,"isCore":true,"isOpen":false},{"id":5,"templateName":"standard","dmRoutineName":"system_service","priority":4,"isCore":true,"isOpen":true},{"id":281,"templateName":"standard","dmRoutineName":"robot_char","priority":5,"isCore":true,"isOpen":true},{"id":259,"templateName":"standard","dmRoutineName":"entity_qa","priority":6,"isCore":true,"isOpen":true},{"id":6,"templateName":"standard","dmRoutineName":"fqa","priority":7,"isCore":true,"isOpen":true},{"id":328,"templateName":"standard","dmRoutineName":"openkg_qa","priority":8,"isCore":true,"isOpen":true},{"id":7,"templateName":"standard","dmRoutineName":"feedback","priority":9,"isCore":true,"isOpen":true},{"id":8,"templateName":"standard","dmRoutineName":"search_cache","priority":10,"isCore":true,"isOpen":true},{"id":32,"templateName":"standard","dmRoutineName":"asr_filter","priority":11,"isCore":true,"isOpen":true},{"id":279,"templateName":"standard","dmRoutineName":"baike","priority":12,"isCore":false,"isOpen":false},{"id":9,"templateName":"standard","dmRoutineName":"search","priority":13,"isCore":false,"isOpen":true},{"id":10,"templateName":"standard","dmRoutineName":"chitchat","priority":14,"isCore":false,"isOpen":true},{"id":11,"templateName":"standard","dmRoutineName":"default_qa","priority":15,"isCore":false,"isOpen":true},{"id":435,"templateName":"standard","dmRoutineName":"yes_no","priority":16,"isCore":true,"isOpen":true},{"id":437,"templateName":"standard","dmRoutineName":"entity_extract","priority":17,"isCore":true,"isOpen":true},{"id":445,"templateName":"standard","dmRoutineName":"selection","priority":18,"isCore":true,"isOpen":true}]}
        """
        url = f"/sv-api/v2/ux/dmtemplate/listdetail/{dm_name}"
        return self.mmue_request(method="GET", path=url)

    def create_new_dm(self, dm_name: str, dm_detail: list[dict]):
        """新建DM流程
        :param dm_name:
        :param dm_detail: [{"dmRoutineName":"user_service","priority":1,"isCore":true,"isOpen":true}]
        :return: {"code":0,"status":true}
        """
        url = "/sv-api/v2/ux/dmtemplate"
        payload = {"data": dm_detail, "templateName": dm_name}
        return self.mmue_request(method="POST", path=url, json=payload)

    def delete_a_dm(self, dm_name: str):
        """删除单个DM流程
        :param dm_name:
        :return: {"code":0,"status":true}
        """
        url = f"/sv-api/v2/ux/dmtemplate/{dm_name}"
        return self.mmue_request(method="DELETE", path=url)

    def update_a_dm(self, dm_name: str, dm_detail: list[dict]):
        url = "/sv-api/v2/ux/dmtemplate"
        payload = {"data": dm_detail, "templateName": dm_name}
        return self.mmue_request(method="PUT", path=url, json=payload)


if __name__ == '__main__':
    mmue_client = AgentManage(base_url="https://mmue-dit87.harix.iamidata.com",
                              username="sevel.liu@cloudminds.com", password="cloud1688")

    req = {"text": "现在几点了", "agent_id": 666, "env": "86", "tanant_code": "cloudminds", "event_type": 0,
           "robot_id": "123456", "session_id": "sevel.liu@cloudminds.com", "event_info": {}}

    result = mmue_client.talk(req)
    print(result.json())
    print(mmue_client.get_dm_detail().json())
