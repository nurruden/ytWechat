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
import os

# config_path = os.path.abspath('../conf/eas.ini')  # 将路径转换为绝对路径


log = logger(functionName=__name__)

# easConf = configparser.ConfigParser()
# easConf.read(config_path, encoding='utf-8')
# # easConf.read('./conf/eas.ini',encoding='utf-8')
# #
# print(f"配置文件路径: {config_path}")
# print(f"文件是否存在: {os.path.exists(config_path)}")
#
#
# appKey = easConf['basic']['appKey']
# appSecret = easConf['basic']['appSecret']
# url = easConf['basic']['url']
# token = easConf['url']['token']
# TOKEN_URL = url + token
# reportURI = easConf['url']['reportList']
# reportURL = url + reportURI
# pageSize = easConf['reportConfiguration']['pageSize']




def convert_to_datetime(date_str):
    date_formats = ['%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%d']

    for date_format in date_formats:
        try:
            date_obj = datetime.strptime(date_str, date_format)
            return date_obj
        except ValueError:
            pass

    raise ValueError("Date format not recognized")



def getProductionReportData(reportValue,token_url,report_url,pagesize,appkey,appsecret,keyValue,reportName):
    '''
        排产超7天未完成：
        单据状态：4，(审核)
        累计出库数量：0.0
        排产日期：早于当前日期-7

        返回：单据编号，物料名称，'销售员': '赵晨晖','发货日期':'发货日期','数量':'数量_','报表':'有订单未排产'

        '''
    resList = dataCollect.get_report_data(reportValue, token_url, report_url, pagesize, appkey, appsecret)

    dataList = []
    for i in range(len(resList)):
        if resList[i][keyValue] == None:
            date_str = "2024-01-01T00:00:00"
            date_format = "%Y-%m-%dT%H:%M:%S"

            date_obj = datetime.strptime(date_str, date_format)
        else:
            date_obj = convert_to_datetime(resList[i][keyValue])

        if date_obj < datetime.now() - timedelta(days=8) and resList[i]['单据状态']=="4" and resList[i]['累计出库数量']==float(0)or resList[i]['累计出库数量'] ==None :
            data={}
            data['单据编号'] = resList[i]['单据编号']
            data['物料名称'] = resList[i]['物料名称']
            data['销售员'] = resList[i]['销售员']
            data['发货日期'] = resList[i]['发货日期']
            data['数量'] = resList[i]['数量_']
            data['报表'] = reportName
            dataList.append(data)
            #加入生产
            pro=data.copy()
            pro['销售员']="王家鹏"
            dataList.append(pro)
    return dataList


def getSaleReportData(reportValue,token_url,report_url,pagesize,appkey,appsecret,keyValue,reportName):
    '''
        排产超7天未完成：
        单据状态：4，(审核)
        累计出库数量：0.0
        排产日期：早于当前日期-7

        返回：单据编号，物料名称，'销售员': '赵晨晖','发货日期':'发货日期','数量':'数量_','报表':'有订单未排产'

        '''
    resList = dataCollect.get_report_data(reportValue, token_url, report_url, pagesize, appkey, appsecret)

    dataList = []
    for i in range(len(resList)):
        if resList[i][keyValue] == None:
            date_str = "2024-01-01T00:00:00"
            date_format = "%Y-%m-%dT%H:%M:%S"

            date_obj = datetime.strptime(date_str, date_format)
        else:
            date_obj = convert_to_datetime(resList[i][keyValue])


        if date_obj < datetime.now() and resList[i]['累计出库数量'] == float(0) and resList[i]['单据状态'] == "7" or \
                resList[i]['单据状态'] == "4":
            data = {}
            data['单据编号'] = resList[i]['单据编号']
            data['物料名称'] = resList[i]['物料名称']
            data['销售员'] = resList[i]['销售员']
            data['发货日期'] = resList[i]['发货日期']
            data['数量'] = resList[i]['数量_']
            data['报表'] = reportName
            dataList.append(data)
    return dataList

# report=easConf['productionReportConf']
# # print(list(report.keys()))
# relation=easConf['relationship']
# for i in list(report.keys()):
#     # print(report[i]) reportValue
#     # print(relation[i]) keyValue
#     # print(i) reportName
#     res=getProductionReportData(report[i],TOKEN_URL,reportURL,pageSize,appKey,appSecret,relation[i],i)
#     print(res)
#     print("*"*10+"+++"+"*"*10)