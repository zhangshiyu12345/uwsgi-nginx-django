import json
from notifications.signals import notify
from django.conf import settings
from football_platform.celery import app
from tool.sms import YunTongXin
from tool.mongodb import Mongo
from tool.send_notices import SendNotices
import pymongo

#创建任务函数
@app.task
def send_sms_c(phone,code):
    config = {
        "accountSid": settings.ACCOUNTSID,
        "accountToken": settings.ACCOUNTTOKEN,
        "appId": settings.APPID,
        "templateId": '1',
    }
    yun = YunTongXin(**config)  # 变为关键字传参
    res = yun.run(phone, code)

    return res

@app.task
def mongo_insert(file,id):
    mongo = Mongo()
    mongo.connectdb(file,id)
    data = mongo.analysis(id)
    print(data)
    return data






