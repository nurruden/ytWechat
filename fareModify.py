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


log = logger(functionName=__name__)

wechat = configparser.ConfigParser()
wechat.read('./conf/wechat.ini')


easConf = configparser.ConfigParser()
easConf.read('./conf/eas.ini')
#
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']

fareAdd = easConf['url']['fareAdd']
fareModify = easConf['url']['fareModify']
fareDel = easConf['url']['fareDel']


file_path = '汇总表.xlsx'
sheet_name = '汇总表'
processor = ExcelDataProcessor(file_path, sheet_name)
dicValue={'纸袋':'zhiDai','吨袋':'dunDai','海运费(CNY)':'ckhyf','Pallet&Wrap/MT打托缠膜（人民币/吨）':'bjdaTuoChanMo','海运费':'ckhyfmy','出口港杂费':'ckgzf','内陆运费总额（人民币）':'nlyfck','摘要':'description'}
# 出口港杂费=港杂费+额外费用
valueDict={'zhiDai':'纸袋','dunDai':'吨袋','ckhyf':'海运费(CNY)','bjdaTuoChanMo':'Pallet&Wrap/MT打托缠膜（人民币/吨）','ckhyfmy':'海运费','ckgzf':'出口港杂费','nlyfck':'内陆运费总额（人民币）','description':'摘要'}
columns = ['销售员', '产品包装', 'PackagingCOST/MT包装费（人民币/吨）', 'Pallet&Wrap/MT打托缠膜（人民币/吨）', '海运费(CNY)', '海运费', '港杂费', '额外费用',
           '内陆运费总额（人民币）','状态','数量（吨）','摘要']
result = processor.process_data(columns)
order_manager = OrderManager(url)
for i in result:
    if '系统号' not in i.keys():
        pass
    copyDic=deepcopy(i)
    number=i['系统号']
    print(number)
    i.pop('系统号')
    status=i['状态']
    i.pop('状态')
    saler=i['销售员']
    i.pop('销售员')
    if '纸袋' in i['产品包装']:
        value=i['PackagingCOST/MT包装费（人民币/吨）']*i['数量（吨）']
        i.pop('PackagingCOST/MT包装费（人民币/吨）')
        i.pop('产品包装')
        i['纸袋']=value
    elif '吨袋' in i['产品包装']:
        value=i['PackagingCOST/MT包装费（人民币/吨）']*i['数量（吨）']
        i.pop('PackagingCOST/MT包装费（人民币/吨）')
        i.pop('产品包装')
        i['吨袋']=value
    i['出口港杂费']=i['港杂费']+i['额外费用']
    i.pop('额外费用')
    i.pop('港杂费')
    print(copyDic)
    print(i)
    des={}
    for t in i.keys():
        if i[t]!= 0:
            des[t]=i[t]
    des.pop('数量（吨）')
    print(des)
    currentDateAndTime = datetime.now()
    currentTime = currentDateAndTime.strftime("%Y/%m/%d %H:%M")
    if status=='新增':
        tmp={}
        for j in dicValue.keys():
            if j in des.keys():
                tmp[dicValue[j]]=des[j]
        tmp['description']=str(currentTime)+str(des)
        print(tmp)
        # res=order_manager.postOrder(fareAdd,number,**tmp)
        # print(res)
    elif status == '修改':
        m = order_manager.getOrder(pageNum=2, page=1, number=number)
        print(m)
        tmp = {}
        for j in dicValue.keys():
            if j in i.keys():
                tmp[dicValue[j]] = i[j]
        print(tmp)
        finaldic={}
        desc={}
        for x in tmp.keys():
            if m['sysnList'][0][x]!=str(tmp[x]):
                finaldic[x]=tmp[x]
                desc[valueDict[x]]=tmp[x]
        print(finaldic)
        if '摘要' in desc.keys():
            oldDesc=desc['摘要']
            desc.pop('摘要')
            newDes=str(currentTime)+str(desc)+str('|')+str(oldDesc)
        finaldic['description']=newDes
        print(finaldic)
    #     modify=order_manager.postOrder(fareModify,number=number,**finaldic)
    #     print(modify)
    #


