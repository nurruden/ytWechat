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

def getCloudZichanData(token_url, report_url, pagesize, appkey, appsecret, daysDelta, extra_params=None):
    """
    获取云端资产数据，筛选符合条件的记录。
    """
    # 计算开始日期
    bizDateStart = (datetime.now() - timedelta(days=daysDelta)).strftime("%Y-%m-%d")

    # 默认参数
    '''
    审核状态，自产订单，daysDelta天前到现在
    '''
    common_params = {
        "status": "4",
        "bizDateStart": bizDateStart,
        "scmType": "2",
    }

    # 合并额外参数（若存在）
    if extra_params:
        common_params.update(extra_params)

    # 获取云端数据
    resList = dataCollect.get_cloud_data(
        token_url=token_url,
        url=report_url,
        pagesize=pagesize,
        appkey=appkey,
        appsecret=appsecret,
        **common_params  # 传入参数
    )

    # 返回结果列表
    dataLi = []

    if not resList:
        log.warning("No data retrieved from cloud.")
        return dataLi

    # 遍历结果，筛选数据
    for data in resList:
        if data.get('是否作废') is None:
            entry = data.get('entrys', [{}])[0]

            dataDic = {
                '单据编号': data.get('单据编号'),
                '销售员': data.get('销售员'),
                '累计出库数量': entry.get('累计出库数量'),
                '物料名称': entry.get('物料名称'),
                '物料编码': entry.get('物料编码'),
                '生产库存组织': data.get('库存组织'),
                '订单日期': data.get('订单日期'),
                '发货日期': entry.get('发货日期'),
                '订单数量': entry.get('数量_'),
                '累计生产数量':entry.get('累计生产数量')

            }
            dataLi.append(dataDic)
    print(dataLi)
    return dataLi



# getCloudZichanData(token_url="http://139.9.135.148:8081/getToken",report_url="http://139.9.135.148:8081/httpsList",pagesize=100,appkey="921ed4d5-c918-49e4-a00c-58b72d58",appsecret="bd754be7-7768-43cc-a061-347ac223",daysDelta=60)


# report=easConf['saleReportConf']
# # print(list(report.keys()))
# relation=easConf['relationship']
# for i in list(report.keys()):
#     # print(report[i]) reportValue
#     # print(relation[i]) keyValue
#     # print(i) reportName
#     res=getSaleReportData(report[i],TOKEN_URL,reportURL,pageSize,appKey,appSecret,relation[i],i)
#     # res=getProductionReportData(report[i],TOKEN_URL,reportURL,pageSize,appKey,appSecret,relation[i],i)
#     print(res)
#     print("*"*10+"+++"+"*"*10)