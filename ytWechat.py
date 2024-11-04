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
import time
import multiprocessing
from collections import defaultdict

log = logger(functionName=__name__)

wechat = configparser.ConfigParser()
wechat.read('./conf/wechat.ini')

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
pageSize = easConf['reportConfiguration']['pageSize']
productionReport = easConf['productionReportConf']
saleReport = easConf['saleReportConf']
relation = easConf['relationship']
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

with open('./conf/userData.json', 'r') as user:
    users = json.load(user)
print(users)
'''
{'李赏': {'wechat': 'lisa', 'id': 625}, '冉哲旭': {'wechat': 'ranranruyun', 'id': 1009}}
'''

'''
[{'单据编号': 'YDD*20240925**009183', '物料名称': '大塬_DZ300_标准_吨袋500kg', '销售员': '赵晨晖', '发货日期': '2024-09-26T00:00:00'}]
'''


# def sendMessage(userInfo, dataList):
#     for data in dataList:
#         sales = data['销售员']
#         if data['销售员'] in list(userInfo.keys()):
#             print(data['销售员'])
#             materials = data['物料名称']
#             order = data['单据编号']
#             sendDate = data['发货日期']
#             userID = userInfo[data['销售员']]['wechat']
#             report = data['报表']
#             count = data['数量']
#             w.send_text(f'尊敬的同事:{sales},在{report}中，您有单据 {order}, 物料为：{materials}，数量为：{count},发货日期：{sendDate},请您及时关注',
#                         [userID])
#         else:
#
#             log.info(f'销售员：{sales} 不在维护列表')


def sendMessage(userInfo, dataList):
    grouped_data = defaultdict(list)
    for item in dataList:
        # 使用销售员和报表作为键
        key = (item['销售员'], item['报表'])
        # 将数据添加到对应的键下
        grouped_data[key].append(item)

    for key, items in grouped_data.items():


        if key[0] in list(userInfo.keys()):
            result = '\n'.join(json.dumps(it, ensure_ascii=False) for it in items)
            w.send_text(f'尊敬的同事:{key[0]},在{key[1]}中，您有{len(items)}票单据：\n {result}',
                        [userInfo[key[0]]['wechat'], ])
        else:

            log.info(f'销售员：{key[0]} 不在维护列表')


def productionReportLoop():
    for i in list(productionReport.keys()):
        res = sortReportData.getProductionReportData(productionReport[i], TOKEN_URL, reportURL, pageSize, appKey,
                                                     appSecret, relation[i], i)
        sendMessage(userInfo=users, dataList=res)


def saleReportLoop():
    for j in list(saleReport.keys()):
        res = sortReportData.getSaleReportData(saleReport[j], TOKEN_URL, reportURL, pageSize, appKey, appSecret,
                                               relation[j], j)

        sendMessage(userInfo=users, dataList=res)

if __name__ == '__main__':

    time_start = time.time()
    process1 = multiprocessing.Process(target=productionReportLoop)

    process2 = multiprocessing.Process(target=saleReportLoop)

    process1.start()

    process2.start()

    process1.join()

    process2.join()

    time_end = time.time()  # 结束计时

    time_c = time_end - time_start  # 运行所花时间
    print('time cost', time_c, 's')
    w.send_text("Send message success",["GaoBieKeLe",])