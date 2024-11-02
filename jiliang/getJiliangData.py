# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: dataCollect
@time: 2024/9/24 15:17
"""
from jiliang import jiliangFunc
import configparser
from utils.logger import logger
import json

log = logger(functionName=__name__)

easConf = configparser.ConfigParser()
easConf.read('../conf/jiliang.ini')
#
username = easConf['basic']['username']
password = easConf['basic']['password']
url = easConf['basic']['url']
token = easConf['url']['token']
TOKEN_URL = url + token
reportURI = easConf['url']['SaleExamine']
reportURL = url + reportURI


def get_report_data(token_url, url, username, password,startTime,endTime):
    payload = {
        # 2024-10-01
        "startTime": startTime,
        "endTime": endTime
    }
    try:
        full_data = jiliangFunc(token_url=token_url,username=username,password=password)

        log.info(f'Connect with Jiangliang: {full_data}')
        response = full_data.post(url, payload=payload)
        return response
    except Exception as e:
        log.error(f'post failed: {e}')
        return False


#
# to=get_report_data(TOKEN_URL, reportURL, username, password,"2024-09-30","2024-09-30")
# print(to)

