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

    def process_data(self, columns, status_values=['新增', '修改']):
        # 读取Excel文件的指定Sheet
        data = pd.read_excel(self.file_path, sheet_name=self.sheet_name, header=None)

        # 将第三行设置为表头
        data.columns = data.iloc[2]  # 第三行作为表头
        data = data[3:].reset_index(drop=True)  # 删除前3行

        # 过滤数据
        filtered_data = data[data['状态'].isin(status_values)].fillna(0)

        # 提取指定列，加上'系统号'列
        if '系统号' not in columns:
            columns = ['系统号'] + columns
        result_data = filtered_data[columns]

        # 转换为字典
        result_list = []
        for _, row in result_data.iterrows():

            result_list.append({col: row[col] for col in columns})

        return result_list


# 使用示例
# file_path = '../汇总表.xlsx'
# sheet_name = '汇总表'
# processor = ExcelDataProcessor(file_path, sheet_name)
# columns = ['销售员', '产品包装', 'PackagingCOST/MT包装费（人民币/吨）', 'Pallet&Wrap/MT打托缠膜（人民币/吨）', '海运费(CNY)', '海运费', '港杂费', '额外费用',
#            '内陆运费总额（人民币）']
# result = processor.process_data(columns)
# print(result)

# 打印结果
# for system_number, details in result.items():
#     print(system_number, details)
