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
from copy import deepcopy
from datetime import datetime


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
sheet_name = '汇总表'

# 定义字段映射表
dicValue = {
    '纸袋': 'zhiDai',
    '吨袋': 'dunDai',
    '海运费(CNY)': 'ckhyf',
    'Pallet&Wrap/MT打托缠膜（人民币/吨）': 'bjdaTuoChanMo',
    '海运费': 'ckhyfmy',
    '出口港杂费': 'ckgzf',
    '内陆运费总额（人民币）': 'nlyfck',
    '摘要': 'description'
}
valueDict = {v: k for k, v in dicValue.items()}  # 反向映射

columns = [
    '销售员', '产品包装', 'PackagingCOST/MT包装费（人民币/吨）',
    'Pallet&Wrap/MT打托缠膜（人民币/吨）', '海运费(CNY)', '海运费',
    '港杂费', '额外费用', '内陆运费总额（人民币）', '状态', '数量（吨）', '摘要'
]

# 初始化数据处理器
processor = ExcelDataProcessor(file_path, sheet_name)
result = processor.process_data(columns)
print(result)
order_manager = OrderManager(url)

# 处理包装费用
def process_packaging(data):
    packaging_type = data.pop('产品包装', None)
    quantity = data.pop('数量（吨）', 0)
    cost_per_unit = data.pop('PackagingCOST/MT包装费（人民币/吨）', 0)

    if '纸袋' in packaging_type:
        data['纸袋'] = cost_per_unit * quantity
    elif '吨袋' in packaging_type:
        data['吨袋'] = cost_per_unit * quantity
    return data

# 处理费用字段
def process_fees(data):
    data['出口港杂费'] = data.pop('港杂费', 0) + data.pop('额外费用', 0)
    return data

# 根据状态执行对应的操作
def handle_status(record, status, number):
    current_time = datetime.now().strftime("%Y/%m/%d %H:%M")

    if status == '新增':
        data = {dicValue[k]: v for k, v in record.items() if v != 0}
        des={k:v for k,v in record.items() if v !=0 }
        print(des)
        data['description'] = f"{current_time} || {des}"
        print(data)
        # log.info(f"新增记录: {data}")
        # Uncomment to make API call
        # response = order_manager.postOrder(fareAdd, number, **data)
        # log.info(response)

    elif status == '修改':
        existing_data = order_manager.getOrder(pageNum=2, page=1, number=number)
        log.info(f"现有记录: {existing_data}")

        modified_data = {}
        description = {}

        for key, value in record.items():
            if existing_data['sysnList'][0][dicValue[key]] != str(value):
                modified_data[dicValue[key]] = value
                description[valueDict[dicValue[key]]] = value

        if '摘要' in description:
            old_desc = description.pop('摘要')
            description = f"{current_time} {description} || {old_desc}"
        modified_data['description'] = description
        log.info(f"修改记录: {modified_data}")
        # Uncomment to make API call
        response = order_manager.postOrder(fareModify, number, **modified_data)
        print(response)

# 主处理逻辑
def main():
    for record in result:
        if '系统号' not in record:
            continue

        number = record.pop('系统号')
        status = record.pop('状态', None)
        record.pop('销售员', None)

        record = process_packaging(record)
        record = process_fees(record)
        log.info(f"处理后的记录: {record}")

        handle_status(record, status, number)

# 执行主程序
if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        log.error(f"程序执行时发生错误: {e}")



