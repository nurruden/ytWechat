# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: ytWechat
@time: 2024/9/12 11:47
"""
from wechat_work import WechatWork
import configparser
from utils.logger import logger
from eas import sortReportData
log=logger(functionName=__name__)

wechat=configparser.ConfigParser()
wechat.read('./conf/wechat.ini')
print(wechat['users'])

corpid = wechat['wechat']['corpid']
log.info(f'corpid is: {corpid}')
appid = wechat['wechat']['appid']
log.info(f'appid is: {appid}')
corpsecret = wechat['wechat']['corpsecret']
log.info(f'corpsecret is: {corpsecret}')

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
reportName1=easConf['reportConf']['已生产未出库']

# users = wechat['users']['GaoBieKeLe']

w = WechatWork(corpid=corpid,
               appid=appid,
               corpsecret=corpsecret)
# 发送文本

# # 发送 Markdown
# w.send_markdown('# Hello World', users)
# # 发送图片
# w.send_image('./新材料办公楼.jpg', users)
# 发送文件
# w.send_file('./订单排产库存优化.pptx', users)

import json

with open('./conf/userData.json','r') as user:
    users=json.load(user)

'''
{'李赏': {'wechat': 'lisa', 'id': 625}, '冉哲旭': {'wechat': 'ranranruyun', 'id': 1009}}
'''
# with open('./data.json','r') as jsonFile:
#     data=json.load(jsonFile)
#     # print(data)
# realData=data['table']['Data']
# # print(realData)
# whatIWant=[]

dataList=sortReportData.getReport1Data(reportName1,TOKEN_URL,reportURL,pageSize,appKey,appSecret)
print(dataList)
'''
[{'单据编号': 'YDD*20240925**009183', '物料名称': '大塬_DZ300_标准_吨袋500kg', '销售员': '赵晨晖', '发货日期': '2024-09-26T00:00:00'}]
'''
# w = WechatWork(corpid=corpid,
#                                appid=appid,
#                                corpsecret=corpsecret)

def sendMessage(userInfo,dataList):
    for data in dataList:
        if data['销售员'] in list(userInfo.keys()):
            print(userInfo[data['销售员']])
            sales=data['销售员']
            materials=data['物料名称']
            order=data['单据编号']
            sendDate=data['发货日期']
            userID=userInfo[data['销售员']]['wechat']
            report=data['报表']
            count=data['数量']
            w.send_text(f'尊敬的同事:{sales},在{report}中，您有单据 {order}, 物料为：{materials}，数量为：{count},发货日期：{sendDate},请您及时关注',[userID])

sendMessage(userInfo=users,dataList=dataList)
# for i in range(len(realData)):
#
#     if realData[i]['C7']==0.0 and realData[i]['C3']==str(7):
#         whatIWant.append(realData[i])
# print(whatIWant)
# wechat={}
# for i in whatIWant:
#     print(i)
#     print(i['C15'])
#     print(eval(i['Query']))
#     if i['C15'] in wechat.keys():
#         wechat[i['C15']].append(eval(i['Query'])["单据编号"])
#     else:
#         wechat.update({i['C15']:[eval(i['Query'])["单据编号"]]})
#
# #{'顾晓凡': ['YDD*20240827**008247', 'YDD*20240827**008243'], '姜贺侠': ['YDD*20240806**007559', 'YDD*20240726**007292', 'YDD*20240726**007290'], '刘海燕': ['YDD*20240805**007517'], '刘春艳': ['YDD*20240729**007350', 'YDD*20240729**007348', 'YDD*20240726**007293'], '吕咏梅': ['YDD*20240711**006813', 'YDD*20240408**003499'], '马啸杰': ['YDD*20240506**004446', 'YDD*20240506**004445'], '王迎雪': ['YDD*20240103**000106'], '胡韵秋': ['YDD*20231211**002085', 'YDD*20231211**002086', 'YDD*20231017**000188']}
# print(wechat)
# for j in wechat.keys():
#     w = WechatWork(corpid=corpid,
#                    appid=appid,
#                    corpsecret=corpsecret)
#     # 发送文本
#     w.send_text('Hello World!', )