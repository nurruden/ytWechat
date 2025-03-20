import requests
import logging
from datetime import datetime
from wechat_work import WechatWork

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class WechatWorkManager:
    def __init__(self, corp_id, secret, app_id):
        self.corp_id = corp_id
        self.secret = secret
        self.app_id = app_id
        print(corp_id)
        print(secret)
        print(app_id)
        self.wechat_client = WechatWork(corpid=corp_id, appid=app_id, corpsecret=secret)
        self.access_token = self.wechat_client.get_access_token()  # 复用 WechatWork 的 get_access_token

    def get_smart_table_data(self, doc_id):
        """获取智能表格数据"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/get_sheet?access_token={self.access_token}"
        payload = {"docid": doc_id}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("errcode") == 0:
                return data.get("data")
            else:
                raise Exception(f"Failed to get smart table data: {data.get('errmsg')}")
        except Exception as e:
            logging.error(f"Error getting smart table data: {e}")
            raise

    def get_basic_info(self, doc_id, sheet_id):
        """获取表格基本信息"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/get_doc_base_info?access_token={self.access_token}"
        payload = {"docid": doc_id, "sheet_id": sheet_id, "offset": 0, "limit": 1}
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            logging.info(f"Basic info: {data}")
            return data
        except Exception as e:
            logging.error(f"Error getting basic info: {e}")
            raise

    def get_row_list_info(self, doc_id, sheet_id):
        """获取表格行数据"""
        url = f"https://qyapi.weixin.qq.com/cgi-bin/wedoc/smartsheet/get_records?access_token={self.access_token}"
        payload = {
            "docid": doc_id,
            "sheet_id": sheet_id,
            "record_ids": [],
            "key_type": "CELL_VALUE_KEY_TYPE_FIELD_TITLE",
            "field_titles": [],
            "field_ids": [],
            "sort": [],
            "offset": 0,
            "limit": 100,
        }
        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            data = response.json()
            if data.get("errcode") == 0:
                return data.get("records")
            else:
                raise Exception(f"Failed to get row list info: {data.get('errmsg')}")
        except Exception as e:
            logging.error(f"Error getting row list info: {e}")
            raise

    def send_task_reminders(self, doc_id, sheet_id):
        """发送任务提醒"""
        records = self.get_row_list_info(doc_id, sheet_id)
        print(records)
        for record in records:
            values = record.get("values", {})
            if "状态" not in values or values["状态"][0]["text"] != "已完成":
                task_promotion = values.get("任务提醒内容", [{}])[0].get("text", "未知任务")
                deadline_timestamp = int(values.get("需完成时间", 0)) / 1000
                deadline = datetime.fromtimestamp(deadline_timestamp)
                current_time = datetime.now()
                days_difference = (current_time - deadline).days
                order_number = values.get("订单号", [{}])[0].get("text", "未知订单")
                users = [user["user_id"] for user in values.get("需完成人", [])]

                if users:
                    message = (
                        f"云订单：{order_number} 的任务：{task_promotion}, "
                        f"需要完成时间为：{deadline}, "
                        f"现在已经接近或者超过最后完成时间 {days_difference} 天，请注意进度并及时完成"
                    )
                    self.wechat_client.send_text(message, users)
                    logging.info(f"Sent reminder to users {users}: {message}")


def main():
    # 企业微信配置
    import configparser
    wechat = configparser.ConfigParser()
    wechat.read('./conf/wechat.ini')

    CORP_ID = wechat['wechat']['corpid']
    SECRET = wechat['wechat']['corpsecret']
    APP_ID = wechat['wechat']['appid']
    DOC_ID = "dcETTm2j8nQOn-ThUCG2sK2NfIhIZV9S9VPOKWfBoS0KsT6_7SKWRGIZdHzyB6WaP_LK4_Oui63rjCI_7yq7wrlg"
    SHEET_ID = "q979lj"

    try:
        # 初始化 WechatWorkManager
        manager = WechatWorkManager(CORP_ID, SECRET, APP_ID)

        # 获取表格基本信息
        manager.get_basic_info(DOC_ID, SHEET_ID)

        # 发送任务提醒
        manager.send_task_reminders(DOC_ID, SHEET_ID)
    except Exception as e:
        logging.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()