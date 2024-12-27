# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: sendZichanData
@time: 2024/12/17 14:47
"""
from wechat_work import WechatWork
import configparser
import json
import requests
import datetime
from utils.logger import logger
from eas import sortReportData
import os

# 配置文件路径
eas_path = os.path.abspath('./conf/eas.ini')
wechat_path = os.path.abspath('./conf/wechat.ini')

# 初始化日志
log = logger(functionName=__name__)

# 加载配置函数
def load_config(file_path):
    config = configparser.ConfigParser()
    config.read(file_path, encoding='utf-8')
    return config

# 加载配置文件
wechat = load_config(wechat_path)
easConf = load_config(eas_path)

# 获取企业微信配置信息
corpid = wechat['wechat']['corpid']
appid = wechat['wechat']['appid']
corpsecret = wechat['wechat']['corpsecret']
log.info(f'corpid: {corpid}, appid: {appid}, corpsecret: {corpsecret}')

# 获取EAS配置信息
appKey = easConf['basic']['appKey']
appSecret = easConf['basic']['appSecret']
url = easConf['basic']['url']
token_url = url + easConf['url']['token']
report_url = url + easConf['url']['reportList']
inventory_url = url + easConf['url']['inventory']
day_delta = int(easConf['reportConfiguration']['dayDelta'])

# 初始化企业微信接口
w = WechatWork(corpid=corpid, appid=appid, corpsecret=corpsecret)

# 读取用户数据
def load_user_data():
    with open('./conf/architect.json', 'r') as user_file:
        return json.load(user_file)

# 解析用户数据，构建成员字典
def parse_user_data(user_data):
    dic_user = {}
    for region, region_data in user_data['sale'].items():
        leader_name = region_data['内勤']
        leader_wechat = region_data['wechat']
        for member_name, member_data in region_data['member'].items():
            dic_user[member_name] = {
                'member_wechat': member_data['wechat'],
                'leader_name': leader_name,
                'leader_wechat': leader_wechat
            }
    return dic_user

# 请求库存数据
def request_inventory(code):
    payload = json.dumps({
        "materialNumber": code,
        "pageNum": 100,
        "page": 1
    })
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(inventory_url, headers=headers, data=payload)
        response.raise_for_status()
        print(response.json())
        return response.json()
    except requests.exceptions.RequestException as e:
        log.error(f"Inventory request failed for code {code}: {e}")
        return []

# 获取云资产数据
def get_cloud_zichan_data():
    return sortReportData.getCloudZichanData(token_url, report_url, pagesize=100, appkey=appKey, appsecret=appSecret, daysDelta=day_delta)

# 处理云资产数据
def process_zichan_data(data):
    res_dic = {}
    for item in data:
        code = item['物料编码']
        inventory_res = request_inventory(code)

        if inventory_res:
            for store in inventory_res.get('sysnList', []):
                if float(store['curstoreQty']) >= float(item['订单数量']):
                    sales_person = item['销售员']
                    order_id = item['单据编号']
                    if sales_person not in res_dic:
                        res_dic[sales_person] = {}
                    if order_id not in res_dic[sales_person]:
                        res_dic[sales_person][order_id] = {
                            "可用库存": {},
                            "发货日期": item['发货日期'],
                            "物料名称": item['物料名称'],
                            "物料编码": code,
                            "订单数量": item['订单数量']
                        }

                    res_dic[sales_person][order_id]["可用库存"][store['warehoseName']] = {
                        '公司名称': store['orgName'],
                        '可用数量': store['curstoreQty']
                    }
    return res_dic

# 生成并发送报告
def generate_and_send_reports(res_dic, dic_user):
    for sales_person, orders in res_dic.items():
        markdown_content = f"# {sales_person}\n\n"
        wechat_id = dic_user[sales_person]['member_wechat']
        leader_wechat_id = dic_user[sales_person]['leader_wechat']

        for order_id, details in orders.items():
            markdown_content += f"## 云订单号：{order_id}\n"
            markdown_content += f" - 可用库存：\n"
            for warehouse, stock in details['可用库存'].items():
                markdown_content += f" - {warehouse}: {stock} \n"
            markdown_content += f" - 发货日期：{details['发货日期']}\n"
            markdown_content += f" - 物料名称：{details['物料名称']}\n"
            markdown_content += f" - 订单数量：{details['订单数量']}\n"

        # 生成文件并发送
        report_file = f'{sales_person}.txt'
        with open(report_file, 'w') as f:
            f.write(markdown_content)

        log.info(f"Sending report for {sales_person}...")
        w.send_text(f'Hi, {sales_person} 附件是目前您的处于审核状态的自产云订单，以下仓库有库存，可以生成销售订单。', [wechat_id,])
        w.send_file(report_file, [wechat_id,leader_wechat_id])

# 主函数
def main():
    global flag

    res=request_inventory('B0207.0024')
    for pro in res.get('sysnList', []):
        if pro['orgName']=='吉林远通矿业有限公司'and float(pro['quantity'])>20:
            flag=True
        else:
            print(flag)

    print(flag)
#     start_time = datetime.datetime.now()
#
#     # 加载和解析用户数据
#     user_data = load_user_data()
#     dic_user = parse_user_data(user_data)
#
#     # 获取云资产数据
#     cloud_data = get_cloud_zichan_data()
#
#     # 处理资产数据
#     res_dic = process_zichan_data(cloud_data)
#
#     # 生成并发送报告
#     generate_and_send_reports(res_dic, dic_user)
#
#     end_time = datetime.datetime.now()
#     delta = end_time - start_time
#     log.info(f"Total execution time: {delta} seconds")
#
if __name__ == "__main__":
    main()

