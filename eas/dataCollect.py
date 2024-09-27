# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: dataCollect
@time: 2024/9/24 15:17
"""
from eas import EASFuc
import configparser
from utils.logger import logger
import json

log = logger(functionName=__name__)

easConf = configparser.ConfigParser()
easConf.read('./conf/eas.ini')
#
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']
token = easConf['url']['token']
TOKEN_URL = url + token
reportURI = easConf['url']['reportList']
reportURL = url + reportURI
pageSize = easConf['reportConf']['pageSize']

def get_report_data(type,token_url,url,pageSize,appKey,appSecret):
    payload = {
        "type": type,
        "pageNo": "1",
        "pageSize": pageSize,
    }
    full_data = EASFuc(token_url=token_url,appKey=appKey, appSecret=appSecret)
    log.info(f'Connect with EAS: {full_data}')

    def fetch_data(url, payload):
        try:
            response = full_data.post(url, payload=payload)
            num=json.loads(response['result'])['total']
            log.info(f'Got data number: {num}')
            return [json.loads(response['result'])['list'], json.loads(response['result'])['total']]
        except Exception as e:
            log.error(f'post failed: {e}')
            return [False,False]

    [data_list,num]=fetch_data(url,payload)

    if num != False:
        total = num
        if total > int(pageSize):
            for i in range(1, (total // int(pageSize))+1):
                payload['pageNo'] = str(i + 1)
                print(payload['pageNo'])
                data_list += fetch_data(url, payload)[0]
        log.info(f'Get data info: {data_list}')
        return data_list
    else:
        return False
# to=get_report_data("1",TOKEN_URL,reportURL,pageSize,appKey, appSecret)
# print(to)
