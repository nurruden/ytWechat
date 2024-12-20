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

corpid = wechat['wechat']['corpid']
log.info(f'corpid is: {corpid}')
appid = wechat['wechat']['appid']
log.info(f'appid is: {appid}')
corpsecret = wechat['wechat']['corpsecret']
log.info(f'corpsecret is: {corpsecret}')

# 读取 API 配置
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']
token=easConf['url']['token']
tokenUrl=url+token
reportList=easConf['url']['reportList']
reportUrl=url+reportList
dayDel=easConf['reportConfiguration']['dayDelta']
inventory=easConf['url']['inventory']
inventoryUrl=url+inventory

w = WechatWork(corpid=corpid,
               appid=appid,
               corpsecret=corpsecret)

with open('./conf/architect.json', 'r') as user:
    user_data = json.load(user)
print(user_data)

dicUser={}
# 遍历每个地区
for region, region_data in user_data['sale'].items():
    # 获取该地区的内勤名字和wechat
    leader_name = region_data['内勤']
    leader_wechat = region_data['wechat']

    # 遍历该地区的成员
    for member_name, member_data in region_data['member'].items():
        member_wechat = member_data['wechat']
        dicUser[member_name]={'member_wechat': member_wechat,'leader_name': leader_name,'leader_wechat': leader_wechat}

print(dicUser)


data=sortReportData.getCloudZichanData(tokenUrl,reportUrl,pagesize=100,appkey=appKey,appsecret=appSecret,daysDelta=int(dayDel))
starttime=datetime.datetime.now()

def requestInventory(method,url,code):
    payload = json.dumps({
        "materialNumber": code,
        "pageNum": 100,
        "page": 1
    })
    headers = {
        'Content-Type': 'application/json',

    }
    response = requests.request(method, url, headers=headers,
                                data=payload)
    if response.status_code == 200:
        return json.loads(response.content)
    else:
        return []
resDic={}
# {"冠军":{"订单1":{"物料名称":"wuliaomingc","仓库名称":"CANGKU","组织名称":"orgName","订单数量":"DINGDANSHULIANG","可用数量":"KEYONGSHULIANH","发货日期":"FAHUORIQI"}}}
for item in range(len(data)):

    total=0
    code = data[item]['物料编码']
    inventoryRes=requestInventory("POST",inventoryUrl,code=code)
    if inventoryRes is not None:
        for store in inventoryRes['sysnList']:
            if float(store['curstoreQty']) >= float(data[item]['订单数量']):
                print(store)
                if data[item]['销售员'] not in resDic:
                    resDic[data[item]['销售员']]={}
                if data[item]['单据编号'] not in resDic[data[item]['销售员']]:
                    resDic[data[item]['销售员']][data[item]['单据编号']]={}
                if "可用库存" not in resDic[data[item]['销售员']][data[item]['单据编号']]:

                    resDic[data[item]['销售员']][data[item]['单据编号']]["可用库存"]={}
                    # print(resDic[data[item]['销售员']][data[item]['单据编号']]["可用库存"])
                # print(resDic[data[item]['销售员']][data[item]['单据编号']]["可用库存"])
                if store['warehoseName'] not in resDic[data[item]['销售员']][data[item]['单据编号']]["可用库存"]:
                    resDic[data[item]['销售员']][data[item]['单据编号']]["可用库存"][store['warehoseName']]={'公司名称':store['orgName'],'可用数量':store['curstoreQty']}
                # '公司名称': store['orgName'], '仓库名称': store['warehoseName'],'可用数量':store['curstoreQty']
                resDic[data[item]['销售员']][data[item]['单据编号']]['发货日期']=data[item]['发货日期']
                resDic[data[item]['销售员']][data[item]['单据编号']]['物料名称']=data[item]['物料名称']
                resDic[data[item]['销售员']][data[item]['单据编号']]['物料编码']=code
                resDic[data[item]['销售员']][data[item]['单据编号']]['订单数量']=data[item]['订单数量']
    else:
        # 如果请求失败，返回错误信息和状态码
        raise []
print(resDic)


for data  in resDic.keys():

    markdown_content = f"# {data}\n\n"
    wechatID=dicUser[data]['member_wechat']
    leader_wechat_id=dicUser[data]['leader_wechat']

    print(wechatID)
    print(leader_wechat_id)
    for detail in resDic[data].keys():
        markdown_content+= f"## 云订单号：{detail}\n"
        markdown_content += f" - 可用库存：\n"
        for inventory in resDic[data][detail]['可用库存'].keys():
            markdown_content += f" - {inventory}：{resDic[data][detail]['可用库存'][inventory]} \n"
        markdown_content += f" - 发货日期：{resDic[data][detail]['发货日期']}\n"
        markdown_content += f" - 物料名称：{resDic[data][detail]['物料名称']}\n"
        markdown_content += f" - 订单数量：{resDic[data][detail]['订单数量']}\n"
    print(markdown_content)
    with open(f'{data}.txt', 'w') as f:
        f.write(markdown_content)
    w.send_text(f'Hi, {data} 附件是目前您的处于审核状态的自产云订单，但是经过对比库存，以下仓库有库存，可以生成销售订单',['GaoBieKeLe',])
    w.send_file(f'{data}.txt',['GaoBieKeLe',])
    # w.send_markdown(markdown_content,['GaoBieKeLe',])
endtime=datetime.datetime.now()
delta = endtime-starttime
print(f"Totally cost {delta} seconds")

