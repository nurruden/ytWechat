# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: sendZichanData
@time: 2024/12/17 14:47
"""
from wechat_work import WechatWork
import configparser
from utils.logger import logger
from eas import sortReportData
import os
import json
import requests
import datetime

eas_path = os.path.abspath('./conf/eas.ini')
wechat_path = os.path.abspath('./conf/wechat.ini')
log = logger(functionName=__name__)

# 配置加载函数
def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path,encoding='utf-8')
    return config

# 加载配置文件
wechat = load_config(wechat_path)
easConf = load_config(eas_path)

# 读取 API 配置
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']
token=easConf['url']['token']
tokenUrl=url+token
reportList=easConf['url']['reportList']
reportUrl=url+reportList
dayDel=easConf['reportConfiguration']['dayDelta']



data=sortReportData.getCloudZichanData(tokenUrl,reportUrl,pagesize=100,appkey=appKey,appsecret=appSecret,daysDelta=int(dayDel))
starttime=datetime.datetime.now()
for item in range(len(data)):
    total=0
    code = data[item]['物料编码']
    payload = json.dumps({
        "materialNumber": code,
        "pageNum": 100,
        "page": 1
    })
    headers = {
        'Content-Type': 'application/json',

    }
    response = requests.request("POST", "http://139.9.135.148:8081/geteasdata/getInventory", headers=headers, data=payload)
    if response.status_code == 200:
        # print(json.loads(response.content))
        for store in json.loads(response.content)['sysnList']:
            if float(store['curstoreQty'])>=float(data[item]['订单数量']):
                total=total+1
                print(data[item]['销售员']+'\n'+data[item]['物料名称']+'\n'+store['orgName']+'\n'+store['warehoseName']+'\n'+str(data[item]['订单数量'])+'\n'+str(store['curstoreQty']))

    else:
        # 如果请求失败，返回错误信息和状态码
        raise response.status_code
endtime=datetime.datetime.now()
delta = endtime-starttime
print(f"Totally cost {delta} seconds")
print(total)
