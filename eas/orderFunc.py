# -*- coding: utf-8 -*-

"""
@author: Allan
@software: PyCharm
@file: orderFunc
@time: 2024/12/8 14:43
"""
import requests
import json
from utils.logger import logger
log=logger(functionName=__name__)

class OrderManager:
    def __init__(self, base_url):
        self.base_url = base_url
        self.headers = {'Content-Type': 'application/json'}

    def getOrder(self, page,pageNum, **kwargs):
        url = f"{self.base_url}/geteasdata/getEasyOrder"
        payload = {"page": page,"pageNum":pageNum}
        payload.update(kwargs)  # More concise way to add kwargs to the payload
        try:
            response = requests.post(url, headers=self.headers, data=json.dumps(payload))
            if response.status_code == 200:
                log.info("获取订单详细信息：")
                return json.loads(response.content)
            else:
                log.error(f'Got error: {response.content}')
                return False
        except requests.RequestException as e:
            log.error(f'HTTP Request failed: {e}')
            return False

        except Exception as e:
            log.error(f'Unexpected error: {e}')
            return False

    def postOrder(self,url,number,**kwargs):
        postURL=self.base_url+url
        payload = {
            "number": number,
        }

        payload.update(kwargs)
        # print(json.dumps(payload))
        try:
            response = requests.post(postURL, headers=self.headers, data=json.dumps(payload))
            if response.status_code == 200:
                log.info(f"成功推送订单：{number}")
                log.info(json.loads(response.content))
                return json.loads(response.content)
            else:
                log.error(f'Got error: {response.content}')
                return False
        except requests.RequestException as e:
            log.error(f'HTTP Request failed: {e}')
            return {"error": {e}}

        except Exception as e:
            log.error(f'Unexpected error: {e}')
            return {"error": str(e)}


    # def postOrder(self, number, **kwargs):
    #     url = f"{self.base_url}/geteasdata/addEasyOrder"
    #     payload = {
    #         "number": number,
    #     }
    #     payload.update(kwargs)
    #     response = requests.post(url, headers=self.headers, data=json.dumps(payload))
    #     print(response.text)
    #


# 使用示例
# base_url = "http://139.9.135.148:8081"
# order_manager = OrderManager(base_url)
# #
# # # 调用实例方法
# # m=order_manager.getOrder("YT0101",pageNum=2,page=1,number='BJYDD-20231218-00002076')
# # print(m)
# order_manager.postOrder("/geteasdata/upEasyOrder",number="BJYDD-20241102-00008127",**{"description": "24-12-10申请深圳安信航港杂费"})
# order_manager.putOrder("BJYDD-20241207-00008947", "100")
# order_manager.delOrder("BJYDD-20241207-00008947")
