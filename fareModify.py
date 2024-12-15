# -*- coding: utf-8 -*-
"""
@author: Allan
@software: PyCharm
@file: fareModify.py
@time: 2024/12/9 18:11
"""
import configparser
from utils.logger import logger
from eas.orderFunc import OrderManager
from eas.getExcelData import ExcelDataProcessor
from datetime import datetime
import pandas as pd

# todo
# 1。数字截取
# 初始化日志
log = logger(functionName=__name__)

# 配置加载函数
def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path)
    return config

# 加载配置文件
wechat = load_config('./conf/wechat.ini')
easConf = load_config('./conf/eas.ini')

# 读取 API 配置
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']

fareAdd = easConf['url']['fareAdd']
fareModify = easConf['url']['fareModify']
fareDel = easConf['url']['fareDel']

# Excel 数据处理配置
file_path = '汇总表.xlsx'
sheet_name = '费用修改单'

# 定义字段映射表
dicValue = {
    '云订单编号': 'number',
    '纸袋': 'zhiDai',
    '吨袋': 'dunDai',
    '海运费人民币': 'ckhyf',
    '打托缠膜': 'bjdaTuoChanMo',
    '海运费': 'ckhyfmy',
    '出口港杂费': 'ckgzf',
    '内陆运费': 'nlyfck',
    'description': 'description'
}

# 获取当前日期
current_date = datetime.now().strftime('%Y-%m-%d')

# 数据整理函数
def process_data(data_list):
    processed_data = []

    for order in data_list:
        cloud_order_id = order.get('云订单编号')
        payment_objects = order.get('付款对象', {})

        description_parts = []
        fee_details = {}

        for company, fees in payment_objects.items():
            for fee in fees:
                amount = order.get(fee)
                if amount is not None and not pd.isna(amount):
                    description_parts.append(f"{company}{fee}")
                    fee_details[fee] = "%.2f" %amount

        description = f"{current_date} " + ", ".join(description_parts)
        processed_data.append({'云订单编号': cloud_order_id, **fee_details, 'description': description})
        log.info(f'本次所有需要推送的数据：{processed_data}')

    return processed_data

# 数据字段映射函数
def map_fields(data, mapping):
    return [
        {mapping.get(k, k): v for k, v in item.items()}
        for item in data
    ]

# 提交数据函数
def submit_data(data, url, fare_add, fare_modify):
    order_manager = OrderManager(url)

    for item in data:
        try:
            check_status = order_manager.getOrder(1, 2, **item)
            log.info(f"Check Status: {check_status}")

            if not check_status['sysnList']:
                order_number = item.pop('number', None)
                response = order_manager.postOrder(fare_add, number=order_number, **item)
                log.info(f"推送数据：{item}")
                log.info(f"Added Order: {response}")

            elif len(check_status['sysnList']) > 1:
                log.warning(f"多条数据，无法确定订单: {item}")

            else:
                existing_description = check_status['sysnList'][0].get('description', '')
                log.info(f'本次云订单需要推送的数据：{item}')
                log.info(f'现在需要与现有云订单云订单费用修改单做对比')
                changes = {
                    key: value
                    for key, value in item.items()
                    if key not in ['description', 'number'] and str(value) != str(check_status['sysnList'][0].get(key))
                }

                if not changes:
                    log.info(f"数据无变化，无需修改: {item}")
                    continue

                changes['description'] = f"{existing_description}|{item['description']}"
                log.info(f"经过对比后推送数据：{changes}")
                response = order_manager.postOrder(fare_modify, number=item['number'], **changes)
                log.info(f"Modified Order: {response}")

        except Exception as e:
            log.error(f"处理订单时发生错误: {e}")

# 执行流程函数
def execute_pipeline():
    try:
        processor = ExcelDataProcessor(file_path, sheet_name)
        raw_data = processor.process_data()

        processed_data = process_data(raw_data)
        mapped_data = map_fields(processed_data, dicValue)

        submit_data(mapped_data, url, fareAdd, fareModify)

        log.info("全部数据处理完成！")

    except Exception as e:
        log.error(f"执行管道时发生错误: {e}")

# 主执行入口
if __name__ == "__main__":
    execute_pipeline()
