# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: dataParse
@time: 2024/9/14 14:41
"""
import json

with open('../data.json','r') as jsonFile:
    data=json.load(jsonFile)
    # print(data)
realData=data['result']['list']
print(realData)
whatIWant=[]
# for i in range(len(realData)):
#     print(type(realData[i]['C7']))
#     print(type(realData[i]['C3']))
#     if realData[i]['C7']==0.0 and realData[i]['C3']==str(7):
#         whatIWant.append(realData[i])
# print(len(whatIWant))
# print(whatIWant)
ytWechat.py