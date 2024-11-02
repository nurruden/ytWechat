# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: jiliangFunc
@time: 2024/10/10 18:23
"""
import datetime
import requests
import configparser
from utils.logger import logger
log=logger(functionName=__name__)
#
# eas=configparser.ConfigParser()
# eas.read('./conf/eas.ini')
#
# url=eas['basic']['url']
# token=eas['url']['token']
# TOKEN_URL=url+token
class jiliangFunc:

    """

    """

    token: str = None
    def __init__(self, token_url: str, username: str, password: str) -> None:
        self.token_url = token_url
        self.username = username
        self.password = password
        self.token = self.get_token()

    def get_token(self) -> str:
        """
        获取EAS token

        Returns
        -------
        str
            jiliang token

        Raises
        ------
        Exception
            当无法获取 token 时

        """

        params = {
            'username': self.username,
            'password': self.password

        }
        response = requests.post(
            self.token_url,json=params)
        js: dict = response.json()
        token = js.get('token')
        if token is None:
            log.error('获取 token 失败 请确保相关信息填写的正确性')
        self.token = token

        log.debug(f'Got token: {self.token}')

        return token

    def post(self, url: str = None, headers: dict = None, payload: dict = None):
        """
        发送请求
        Parameters
        ----------
        url : str
            请求的目标 URL
        headers : dict
            请求头
        payload : dict
            请求的内容
        Returns
        -------

        """
        try:
            token = self.get_token()

            # Set headers and payload if not provided
            if headers is None:
                headers = {
                    "Authorization": f"Bearer {token}",
                    'Content-Type': 'application/json'
                }

            if payload is None:
                payload = {}

            # Send the POST request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an exception for HTTP error codes

            res_json = response.json()
            if res_json.get('code') == 200:
                log.info(f'Post message with payload {payload} success')
                return res_json
            else:
                log.error(f'Failed to send message. Response: {res_json}')
                return False

        except requests.RequestException as e:
            log.error(f'HTTP Request failed: {e}')
            return False

        except Exception as e:
            log.error(f'Unexpected error: {e}')
            return False

payload={
    "startTime": "2024-10-01",
    "endTime": "2024-10-01"
}
# full_data = jiliangFuc(token_url='http://139.9.223.243:8090/api/apiLogin',username='jlyt', password='123456')
# res=full_data.post('http://139.9.223.243:8090/api/select/examine/selectSaleExamineList',payload=payload)
# print(res)