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
    logPath = os.path.abspath(".") + "/" + logPath if logPath else os.path.abspath(".") + "/logs"
    functionName = functionName if functionName else "default_function_name"

    if not os.path.isdir(logPath):
        os.mkdir(logPath)

    logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    fileHandler = RotatingFileHandler("{0}/{1}_{2}.log".format(logPath, functionName, os.path.basename(__file__).split(".")[0]), maxBytes=(1048576*5), backupCount=3)
    fileHandler.setFormatter(logFormatter)
    fileHandler.setLevel(logging.DEBUG)
    logger.addHandler(fileHandler)

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