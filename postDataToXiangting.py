# -*- coding: utf-8 -*-
"""
Simplified and robust version for processing production reports.
"""
import configparser
import os
from datetime import datetime
from eas.sortReportData import getProductionReportData
from wechat_work import WechatWork
from utils.logger import logger
import traceback

# 初始化日志记录
log = logger(functionName=__name__)

def load_config(file_path):
    """
    读取配置文件。
    """
    try:
        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')
        return config
    except Exception as e:
        log.error(f"Failed to load config from {file_path}: {e}")
        raise

# 读取企业微信配置
wechat_path = os.path.abspath('./conf/wechat.ini')
wechat_config = load_config(wechat_path)
corpid = wechat_config['wechat']['corpid']
appid = wechat_config['wechat']['appid']
corpsecret = wechat_config['wechat']['corpsecret']

# 初始化企业微信实例
w = WechatWork(corpid=corpid, appid=appid, corpsecret=corpsecret)
log.info("WeChatWork initialized successfully.")

# 读取EAS配置
eas_path = os.path.abspath('./conf/eas.ini')
eas_config = load_config(eas_path)

# 提取EAS基础配置
appKey = eas_config['basic']['appKey']
appSecret = eas_config['basic']['appSecret']
base_url = eas_config['basic']['url']
TOKEN_URL = base_url + eas_config['url']['token']
reportURL = base_url + eas_config['url']['reportList']
pageSize = int(eas_config['reportConfiguration']['pageSize'])
productionReport = dict(eas_config['productionReportConf'])
relation = dict(eas_config['relationship'])

def production_report_loop():
    """
    遍历生产报表类型，获取数据并筛选符合条件的记录。
    """
    for report_type, report_value in productionReport.items():
        try:
            # 获取对应的关系数据
            relation_data = relation.get(report_type)
            if not relation_data:
                log.warning(f"No relation data found for report type '{report_type}', skipping.")
                continue

            # 调用获取生产报表数据的函数
            result_data = getProductionReportData(
                reportValue=report_value,
                token_url=TOKEN_URL,
                report_url=reportURL,
                pagesize=pageSize,
                appkey=appKey,
                appsecret=appSecret,
                keyValue=relation_data,
                reportName=report_type
            )

            if not result_data:
                log.info(f"No matching records found for report type '{report_type}'.")
                continue

            # 统计数据并生成汇报信息
            total_records = len(result_data)
            total_quantity = sum(record.get('数量', 0) for record in result_data if record.get('销售员') != "王家鹏")
            log.info(f"Report '{report_type}' processed successfully. Total records: {total_records}, Total quantity: {total_quantity}")

            # 发送微信通知
            message = f"尊敬的同事，在{report_type}中，共计有{total_records}条数据，共计{total_quantity}吨。"
            w.send_text(message, ['GaoBieKeLe','XiangTing-YuanTongKuangYe'])
            log.info(f"WeChat notification sent for report '{report_type}'.")

        except Exception as e:
            log.error(f"Error while processing report type '{report_type}': {e}")
            log.error(traceback.format_exc())

if __name__ == "__main__":
    try:
        production_report_loop()
    except Exception as main_error:
        log.error(f"Critical error in main execution: {main_error}")
