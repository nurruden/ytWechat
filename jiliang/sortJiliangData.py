# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: sortJiliangData
@time: 2024/10/11 09:18
"""
from jiliang import jiliangFunc
import configparser
from utils.logger import logger
from datetime import datetime
from jiliang import getJiliangData

log = logger(functionName=__name__)

easConf = configparser.ConfigParser()
easConf.read('../conf/jiliang.ini')
#
username = easConf['basic']['username']
password = easConf['basic']['password']
url = easConf['basic']['url']
token = easConf['url']['token']
TOKEN_URL = url + token
SaleExamine = easConf['url']['SaleExamine']
SaleExamineURL = url + SaleExamine
MaterialExamine = easConf['url']['MaterialExamine']
MaterialExamineURL = url + MaterialExamine

def getData(token_url,report_url,username,password,startTime,endTime):
    '''


        '''
    start = startTime if startTime else datetime.date(datetime.now()).isoformat()
    end = endTime if endTime else datetime.date(datetime.now()).isoformat()
    resList=getJiliangData.get_report_data(token_url,url=report_url,username=username,password=password,startTime=start,endTime=end)
    print(resList)
    return resList

getData(token_url=TOKEN_URL,report_url=MaterialExamineURL,username=username,password=password,startTime="2024-09-30",endTime="2024-10-06")

# def sortSaleData()
# res = getReportData(token_url=TOKEN_URL,report_url=SaleExamineURL,username=username,password=password,startTime="2024-10-10",endTime="2024-10-10")
# if res != False and res['code'] == 200:
#     print(len(res['data']))
#     print(res['data'])

