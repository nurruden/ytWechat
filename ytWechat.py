# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: ytWechat
@time: 2024/9/12 11:47
"""
from wechat_work import WechatWork
import configparser
from utils.logger import logger
log=logger(functionName=__name__)

wechat=configparser.ConfigParser()
wechat.read('./conf/wechat.ini')

corpid = wechat['wechat']['corpid']
log.info(f'corpid is: {corpid}')
appid = wechat['wechat']['appid']
log.info(f'appid is: {appid}')
corpsecret = wechat['wechat']['corpsecret']
log.info(f'corpsecret is: {corpsecret}')

users = wechat['users']['GaoBieKeLe']

w = WechatWork(corpid=corpid,
               appid=appid,
               corpsecret=corpsecret)
# 发送文本
# w.send_text('Hello World!', users)
# # 发送 Markdown
w.send_markdown('# Hello World', users)
# # 发送图片
w.send_image('./新材料办公楼.jpg', users)
# 发送文件
w.send_file('./订单排产库存优化.pptx', users)

