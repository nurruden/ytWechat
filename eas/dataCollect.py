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

# easConf = configparser.ConfigParser()
# easConf.read('./conf/eas.ini')
# #
# appKey = easConf['basic']['appKey']
# appSecret = easConf['basic']['appSecret']
# url = easConf['basic']['url']
# token = easConf['url']['token']
# TOKEN_URL = url + token
# reportURI = easConf['url']['reportList']
# reportURL = url + reportURI
# pageSize = easConf['reportConfiguration']['pageSize']

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
        # log.info(f'Get data info: {data_list}')
        return data_list
    else:
        return False
# to=get_report_data("1",TOKEN_URL,reportURL,pageSize,appKey, appSecret)
# print(to)
def get_cloud_data(token_url, url, pagesize, appkey, appsecret, **kwargs):
    """
    从云端获取数据，支持分页处理，并允许自定义 payload 参数。

    :param token_url: 令牌 URL
    :param url: 数据接口 URL
    :param page_size: 每页记录数
    :param app_key: 应用密钥
    :param app_secret: 应用密钥
    :param kwargs: 额外的 payload 参数，支持自定义查询条件
    :return: 获取的完整数据列表，或 False（如果失败）
    """
    # 默认 payload 参数
    payload = {
        "type": "4",  # 示例固定参数，可覆盖
        "pageNo": 1,
        "pageSize": pagesize
    }
    # 合并额外参数
    payload.update(kwargs)

    try:
        # 初始化 EAS 功能接口
        eas_client = EASFuc(token_url=token_url, appKey=appkey, appSecret=appsecret)
        log.info("Connected to EAS successfully.")
    except Exception as e:
        log.error(f"Failed to initialize EAS client: {e}")
        return False

    def fetch_data(page_payload):
        """
        获取单页数据。
        """
        try:
            response = eas_client.post(url,payload=page_payload)
            result = json.loads(response.get('result', '{}'))
            data_list = result.get('list', [])
            total = result.get('total', 0)
            log.info(f"Fetched {len(data_list)} records, total: {total}.")
            return data_list, total
        except Exception as e:
            log.error(f"Failed to fetch data: {e}")
            return [], 0

    # 获取第一页数据
    data_list, total_records = fetch_data(payload)

    if total_records == 0:
        log.warning("No data found.")
        return []

    # 如果数据超过一页，循环获取后续页数据
    total_pages = (total_records + pagesize - 1) // pagesize  # 计算总页数
    for page_no in range(2, total_pages + 1):
        payload["pageNo"] = page_no
        page_data, _ = fetch_data(payload)
        data_list.extend(page_data)

    log.info(f"Successfully fetched all data. Total records: {len(data_list)}.")
    return data_list