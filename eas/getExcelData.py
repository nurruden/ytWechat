# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: getExcelData
@time: 2024/12/8 16:51
"""
import pandas as pd
from utils.logger import logger
log=logger(functionName=__name__)

class ExcelDataProcessor:
    def __init__(self, file_path, sheet_name):
        self.file_path = file_path
        self.sheet_name = sheet_name

    def process_data(self):
        # 读取Excel文件的指定Sheet
        try:
            # 读取 Excel 文件，从第二行开始
            df = pd.read_excel(self.file_path, self.sheet_name, skiprows=1)

            # 将空值填充为 None
            df = df.where(pd.notnull(df), None)

            # 过滤掉 "付款对象" 为空的行
            df = df[df['付款对象'].notna()]

            # 处理 "付款对象" 列
            def process_row(value):
                if isinstance(value, str) and '#' in value:
                    split_values = value.split('#')  # 按 '#' 分隔为列表
                    return process_payment_object_company(split_values)
                elif isinstance(value, str):
                    return process_payment_object_company([value])  # 单个值处理
                return None

            df['付款对象'] = df['付款对象'].apply(process_row)

            # 转换为字典列表
            data_list = df.to_dict(orient='records')
            return data_list

        except Exception as e:
            print(f"读取 Excel 数据时发生错误: {e}")
            return []

def process_payment_object_list(value):
    if "#" in value:
        return value.split("#")  # 分隔内容存为列表
    return [value]  # 单个元素存为列表
def process_payment_object_company(value):
    """
    处理付款对象的值：
    1. 以 '@' 为分隔符，分隔符后的部分作为 key，分隔符前的部分作为 value。
    2. 如果 value 中包含 '&'，以 '&' 为分隔符分割为列表。
    3. 如果 value 不包含 '&'，将其包装成单元素列表。
    :param value: 付款对象的原始值 (列表)
    :return: 处理后的字典
    """
    processed_result = {}
    for item in value:
        if '@' in item:
            val, key = item.split('@', 1)  # 分隔符 '@'
            if '&' in val:
                val = val.split('&')  # 分隔符 '&'
            else:
                val = [val]  # 单元素列表
            processed_result[key] = val
        else:
            processed_result[item] = None  # 如果没有 '@'，存为 None
    return processed_result

# 使用示例
# file_path = '../汇总表.xlsx'
# sheet_name = '费用修改单'
# processor = ExcelDataProcessor(file_path, sheet_name)
#
# result = processor.process_data()
# print(result)

# 打印结果
# for system_number, details in result.items():
#     print(system_number, details)
