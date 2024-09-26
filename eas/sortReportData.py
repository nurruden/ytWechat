# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: sortReportData
@time: 2024/9/26 10:33
"""
from eas import dataCollect
import configparser
from utils.logger import logger
from datetime import datetime

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
reportName1=easConf['reportConf']['已生产未出库']



def getReport1Data(reportName,token_url,report_url,pagesize,appkey,appsecret):
    '''
    已生产未出库：
    单据状态：7，
    累计出库数量：0.0
    发货日期：早于当期日期

    返回：单据编号，物料名称，'销售员': '赵晨晖'，'userId': 'zhaochenhui'

    '''
    resList = dataCollect.get_report_data(reportName, token_url, report_url, pagesize, appkey, appsecret)
    date_format = "%Y-%m-%dT%H:%M:%S"
    dataList=[]
    for i in range(len(resList)):
        date_obj = datetime.strptime(resList[i]['发货日期'], date_format)
        if date_obj < datetime.now() and resList[i]['单据状态']=="7" and resList[i]['累计出库数量']==float(0):
            data={}
            data['单据编号']=resList[i]['单据编号']
            data['物料名称']=resList[i]['物料名称']
            data['销售员']=resList[i]['销售员']
            data['发货日期']=resList[i]['发货日期']
            data['数量']=resList[i]['数量_']
            data['报表']='已生产未出库'
            dataList.append(data)
    return dataList

# getReport1Data(reportName1,TOKEN_URL,reportURL,pageSize,appKey,appSecret)