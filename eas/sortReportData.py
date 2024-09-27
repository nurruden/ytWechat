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
from datetime import datetime,timedelta

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
reportName2=easConf['reportConf']['有订单未排产']
reportName3=easConf['reportConf']['排产超7天未完成']


def convert_to_datetime(date_str):
    date_formats = ['%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']

    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(date_str, date_format)
            return date_obj
        except ValueError:
            pass

    raise ValueError("Date format not recognized")


def getReport1Data(reportName,token_url,report_url,pagesize,appkey,appsecret):
    '''
    已生产未出库：
    单据状态：7（关闭）或者 4（审核），
    累计出库数量：0.0
    发货日期：早于当期日期

    返回：单据编号，物料名称，'销售员': '赵晨晖'，'发货日期':'发货日期','数量':'数量_','报表':'已生产未出库'

    '''
    resList = dataCollect.get_report_data(reportName, token_url, report_url, pagesize, appkey, appsecret)
    date_format = "%Y-%m-%dT%H:%M:%S"
    dataList=[]
    for i in range(len(resList)):
        date_obj = datetime.strptime(resList[i]['发货日期'], date_format)
        if date_obj < datetime.now() and resList[i]['累计出库数量']==float(0) and resList[i]['单据状态']=="7" or resList[i]['单据状态']=="4":
            data={}
            data['单据编号']=resList[i]['单据编号']
            data['物料名称']=resList[i]['物料名称']
            data['销售员']=resList[i]['销售员']
            data['发货日期']=resList[i]['发货日期']
            data['数量']=resList[i]['数量_']
            data['报表']='已生产未出库'
            dataList.append(data)
    return dataList

# res=getReport1Data(reportName1,TOKEN_URL,reportURL,pageSize,appKey,appSecret)
# print(res)
# print(len(res))
def getReport2Data(reportName,token_url,report_url,pagesize,appkey,appsecret):
    '''
        有订单未排产：
        单据状态：4，(审核)
        累计出库数量：0.0
        订单日期：早于当前日期-7

        返回：单据编号，物料名称，'销售员': '赵晨晖','发货日期':'发货日期','数量':'数量_','报表':'有订单未排产'

        '''
    resList = dataCollect.get_report_data(reportName, token_url, report_url, pagesize, appkey, appsecret)


    dataList = []
    for i in range(len(resList)):
        date_obj = convert_to_datetime(resList[i]['订单日期'])

        if date_obj < datetime.now() - timedelta(days=7) and resList[i]['单据状态']=="4" and resList[i]['累计出库数量']==float(0):
            data={}
            data['单据编号'] = resList[i]['单据编号']
            data['物料名称'] = resList[i]['物料名称']
            data['销售员'] = resList[i]['销售员']
            data['发货日期'] = resList[i]['发货日期']
            data['数量'] = resList[i]['数量_']
            data['报表'] = '有订单未排产'
            dataList.append(data)
    return dataList
# res=getReport2Data(reportName2,TOKEN_URL,reportURL,pageSize,appKey,appSecret)
# print(res)

def getReport3Data(reportName,token_url,report_url,pagesize,appkey,appsecret):
    '''
        排产超7天未完成：
        单据状态：4，(审核)
        累计出库数量：0.0
        排产日期：早于当前日期-7

        返回：单据编号，物料名称，'销售员': '赵晨晖','发货日期':'发货日期','数量':'数量_','报表':'有订单未排产'

        '''
    resList = dataCollect.get_report_data(reportName, token_url, report_url, pagesize, appkey, appsecret)

    print(resList)
    # dataList = []
    # for i in range(len(resList)):
    #     date_obj = convert_to_datetime(resList[i]['订单日期'])
    #
    #     if date_obj < datetime.now() - timedelta(days=7) and resList[i]['单据状态']=="4" and resList[i]['累计出库数量']==float(0):
    #         data={}
    #         data['单据编号'] = resList[i]['单据编号']
    #         data['物料名称'] = resList[i]['物料名称']
    #         data['销售员'] = resList[i]['销售员']
    #         data['发货日期'] = resList[i]['发货日期']
    #         data['数量'] = resList[i]['数量_']
    #         data['报表'] = '有订单未排产'
    #         dataList.append(data)
    # return dataList

res=getReport3Data(reportName3,TOKEN_URL,reportURL,pageSize,appKey,appSecret)
# print(res)