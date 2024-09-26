# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: easFunc
@time: 2024/9/19 13:34
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
class EASFuc:

    """

    """

    access_token: str = None
    access_token_expires_time: datetime.datetime = None

    def __init__(self, token_url: str, appKey: str, appSecret: str) -> None:
        self.token_url = token_url
        self.appKey = appKey
        self.appSecret = appSecret
        self.access_token = self.get_access_token()

    def get_access_token(self) -> str:
        """
        获取EAS token

        Returns
        -------
        str
            EAS token

        Raises
        ------
        Exception
            当无法获取 token 时

        """
        if self.access_token_expires_time and self.access_token and datetime.datetime.now() < self.access_token_expires_time:
            return self.access_token

        params = {
            'appKey': self.appKey,
            'appSecret': self.appSecret

        }
        response = requests.post(
            self.token_url,json=params)
        js: dict = response.json()
        access_token = js.get('access_token')
        if access_token is None:
            log.error('获取 token 失败 请确保相关信息填写的正确性')
        self.access_token = access_token
        self.access_token_expires_time = datetime.datetime.now(
        ) + datetime.timedelta(seconds=js.get('expires_in') - 60)
        log.debug(f'Got token: {self.access_token}')
        log.info(f'Token expire time is: {self.access_token_expires_time}')

        return access_token

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
            access_token = self.get_access_token()

            # Set headers and payload if not provided
            if headers is None:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    'Content-Type': 'application/json'
                }

            if payload is None:
                payload = {}

            # Send the POST request
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an exception for HTTP error codes

            res_json = response.json()
            if res_json.get('ErrCode') == 0:
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


