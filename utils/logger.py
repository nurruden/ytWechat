# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: logger
@time: 2024/9/13 09:17
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler
import json
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

def logger(logPath=None, functionName=None):
    # 设置日志路径和默认函数名
    logPath = os.path.abspath(".") + "/" + logPath if logPath else os.path.abspath(".") + "/logs"
    functionName = functionName if functionName else "default_function_name"

    # 创建日志目录
    if not os.path.isdir(logPath):
        os.mkdir(logPath)

    # 配置日志格式
    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger(functionName)  # 为每个函数名创建独立日志记录器
    logger.setLevel(logging.DEBUG)

    # 检查是否已添加处理器，避免重复
    if not logger.handlers:
        # 文件处理器
        fileHandler = RotatingFileHandler(
            f"{logPath}/{functionName}_{os.path.basename(__file__).split('.')[0]}.log",
            maxBytes=(1048576 * 5),
            backupCount=3
        )
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.DEBUG)
        logger.addHandler(fileHandler)

        # 控制台处理器
        consoleHandler = logging.StreamHandler(sys.stdout)
        consoleHandler.setFormatter(logFormatter)
        consoleHandler.setLevel(logging.INFO)
        logger.addHandler(consoleHandler)

    return logger

if __name__ == "__main__":
    log = logger(functionName='my_function')
    log.info("This is a info level sample")
    log.debug("This is a debug level sample")
    log.warning("This is a warning level sample")