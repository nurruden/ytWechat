# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: fareModify
@time: 2024/12/9 18:11
"""
import configparser
from utils.logger import logger
from eas.orderFunc import OrderManager
from eas.getExcelData import ExcelDataProcessor
from datetime import datetime
import pandas as pd


# 初始化日志
log = logger(functionName=__name__)

# 加载配置文件
def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

wechat = load_config('./conf/wechat.ini')
easConf = load_config('./conf/eas.ini')

# 读取API配置
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']

fareAdd = easConf['url']['fareAdd']
fareModify = easConf['url']['fareModify']
fareDel = easConf['url']['fareDel']

# Excel数据处理配置
file_path = '汇总表.xlsx'
sheet_name = '费用修改单'

# 定义字段映射表
dicValue = {
    '云订单编号':'number',
    '纸袋': 'zhiDai',
    '吨袋': 'dunDai',
    '海运费人民币': 'ckhyf',
    '打托缠膜': 'bjdaTuoChanMo',
    '海运费': 'ckhyfmy',
    '出口港杂费': 'ckgzf',
    '内陆运费': 'nlyfck',
    'description':'description'
}
# valueDict = {v: k for k, v in dicValue.items()}  # 反向映射


# 初始化数据处理器
processor = ExcelDataProcessor(file_path, sheet_name)
result = processor.process_data()
# [{'云订单编号': 'YDD*20241024**010069', '吨袋': nan, '纸袋': nan, '打托缠膜': nan, '海运费人民币': nan, '海运费': nan, '出口港杂费': 1537.848, '内陆运费': nan, '付款对象': {'毅鑫': ['海运费', '港杂费'], '阳光': ['报关费']}}]


# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')


def shakeData(data_list):
    tmp=[]
    for order in data_list:
        cloud_order_id = order['云订单编号']
        payment_objects = order['付款对象']

        description_parts = []
        fee_details = {}

        for company, fees in payment_objects.items():
            print(company,fees)
            for fee in fees:
                amount = order.get(fee, None)
                if amount is not None and not pd.isna(amount):
                    description_parts.append(f"{company}{fee}{amount}")
                    fee_details[fee] = amount

        if description_parts:
            description = f"{current_date}" + ', '.join(description_parts)
            entry = {'云订单编号': cloud_order_id, **fee_details, 'description': description}
            tmp.append(entry)
    return tmp
res = shakeData(result)
print(res)


def sortData(shakeRes,dicValue):
    result = []

    for item in shakeRes:
        new_item = {}
        for key, value in item.items():
            if key in dicValue:
                new_key = dicValue[key]
                new_item[new_key] = value
            else:
                new_item[key] = value
        result.append(new_item)
    return result
finalRes=sortData(res,dicValue)
print(finalRes)

def postData(data):

    order_manager = OrderManager(url)
    for i in data:
        # order_number=i.pop('number',None)
        checkStatus=order_manager.getOrder(2,1,**i)
        print(checkStatus)
        if len(checkStatus['sysnList'])==0:
            # 新增
            # order_number = i.pop('number', None)
            # res = order_manager.postOrder(fareAdd,order_number,**i)
            print(res)
        else:
            pass
postData(finalRes)