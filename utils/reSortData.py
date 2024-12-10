# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: reSortData
@time: 2024/11/2 21:29
"""

from collections import defaultdict

# 假定原始数据存储在名为data的列表中
data = [
    {'单据编号': 'YDD*20241024**010072', '物料名称': '大地_BS20_低铁_纸袋英文红', '销售员': '吕咏梅', '发货日期': '2024-11-09T00:00:00', '数量': 21.12, '报表': '有订单未排产'},
    {'单据编号': 'YDD*20241024**010072', '物料名称': '大地_BS20_低铁_纸袋英文红', '销售员': '王家鹏', '发货日期': '2024-11-09T00:00:00', '数量': 21.12, '报表': '有订单未排产'},
    # ... 其他数据项
    {'单据编号': 'BJYDD-20231121-00001657', '物料名称': 'F40衬膜阀口白皮（25KG/袋）', '销售员': '胡韵秋', '发货日期': '2023-11-21T00:00:00', '数量': 28.0, '报表': '有订单未排产'},
    {'单据编号': 'BJYDD-20231121-00001657', '物料名称': 'F40衬膜阀口白皮（25KG/袋）', '销售员': '王家鹏', '发货日期': '2023-11-21T00:00:00', '数量': 28.0, '报表': '有订单未排产'}
]

# 使用defaultdict来存储分组后的数据
grouped_data = defaultdict(list)

# 遍历原始数据
for item in data:
    # 使用销售员和报表作为键
    key = (item['销售员'], item['报表'])
    # 将数据添加到对应的键下
    grouped_data[key].append(item)
print(grouped_data)


# 输出分组后的数据
for key, items in grouped_data.items():
    print(f"销售员: {key[0]}, 报表: {key[1]}, 数据数量: {len(items)}")
    for item in items:
        print(item)
    print('---' * 10)  # 分隔线