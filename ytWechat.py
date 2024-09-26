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
log=logger(functionName=__name__)

wechat=configparser.ConfigParser()
wechat.read('./conf/wechat.ini')

corpid = wechat['wechat']['corpid']
log.info(f'corpid is: {corpid}')
appid = wechat['wechat']['appid']
log.info(f'appid is: {appid}')
corpsecret = wechat['wechat']['corpsecret']
log.info(f'corpsecret is: {corpsecret}')

# users = wechat['users']['GaoBieKeLe']

# w = WechatWork(corpid=corpid,
#                appid=appid,
#                corpsecret=corpsecret)
# 发送文本
# w.send_text('Hello World!', users)
# # 发送 Markdown
# w.send_markdown('# Hello World', users)
# # 发送图片
# w.send_image('./新材料办公楼.jpg', users)
# 发送文件
# w.send_file('./订单排产库存优化.pptx', users)

import json

with open('./conf/userData.json','r') as user:
    users=json.load(user)

with open('./data.json','r') as jsonFile:
    data=json.load(jsonFile)
    # print(data)
realData=data['table']['Data']
# print(realData)
whatIWant=[]
for i in range(len(realData)):

    if realData[i]['C7']==0.0 and realData[i]['C3']==str(7):
        whatIWant.append(realData[i])
print(whatIWant)
wechat={}
for i in whatIWant:
    print(i)
    print(i['C15'])
    print(eval(i['Query']))
    if i['C15'] in wechat.keys():
        wechat[i['C15']].append(eval(i['Query'])["单据编号"])
    else:
        wechat.update({i['C15']:[eval(i['Query'])["单据编号"]]})

#{'顾晓凡': ['YDD*20240827**008247', 'YDD*20240827**008243'], '姜贺侠': ['YDD*20240806**007559', 'YDD*20240726**007292', 'YDD*20240726**007290'], '刘海燕': ['YDD*20240805**007517'], '刘春艳': ['YDD*20240729**007350', 'YDD*20240729**007348', 'YDD*20240726**007293'], '吕咏梅': ['YDD*20240711**006813', 'YDD*20240408**003499'], '马啸杰': ['YDD*20240506**004446', 'YDD*20240506**004445'], '王迎雪': ['YDD*20240103**000106'], '胡韵秋': ['YDD*20231211**002085', 'YDD*20231211**002086', 'YDD*20231017**000188']}
print(wechat)
for j in wechat.keys():
    w = WechatWork(corpid=corpid,
                   appid=appid,
                   corpsecret=corpsecret)
    # 发送文本
    w.send_text('Hello World!', )