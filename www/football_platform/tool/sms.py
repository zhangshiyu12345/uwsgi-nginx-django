import datetime
import hashlib
import base64
import json

import requests
#发送短信


class YunTongXin():
    base_url = 'https://app.cloopen.com:8883'

    def __init__(self,accountSid,accountToken,appId,templateId):
        #账户id
        self.accountSid = accountSid
        #授权令牌
        self.accountToken = accountToken
        self.appId = appId
        self.templateId = templateId #模板id

    def get_request_url(self,sig):
        self.url = self.base_url + '/2013-12-26/Accounts/%s/SMS/TemplateSMS?sig=%s'%(self.accountSid,sig)

        return self.url


    def get_timestamp(self):
        #生成时间戳
        return datetime.datetime.now().strftime('%Y%m%d%H%M%S')

    def get_sig(self,timestamp):
        #生成业务url中的sig
        s = self.accountSid + self.accountToken + timestamp
        m = hashlib.md5() #md5的计算对象
        m.update(s.encode())
        return m.hexdigest().upper()

    def get_request_header(self,timestamp):
        #生成请求头
        s = self.accountSid + ':' + timestamp
        auth = base64.b64encode(s.encode()).decode()
        return {
            'Accept': 'application/json',
            'Content-Type': 'application/json;charset=utf-8',
            'Authorization': auth
        }

    def get_request_body(self,phone,code):
        return {
            'to': phone,
            'appId': self.appId,
            'templateId': self.templateId,
            'datas': [code, "1"] #一分钟有效

        }

    def request_api(self,url,header,body):
        res = requests.post(url,headers=header,data=body)
        return res.text


    def run(self,phone,code):
        timestamp = self.get_timestamp()
        #生成签名
        sig = self.get_sig(timestamp)
        url = self.get_request_url(sig)

        header = self.get_request_header(timestamp)
        #print(url)
        #print(header)
        body = self.get_request_body(phone,code)
        #发请求
        data = self.request_api(url,header,json.dumps(body))

        return data

if __name__ == '__main__':
    config = {
        "accountSid": '8aaf07087f77bf96017faa847ecb12ba',
        "accountToken": '396dec387f0d45b2b96ca77400adec99',
        "appId":'8aaf07087f77bf96017faa847fe912c1',
        "templateId": '1',
    }
    yun = YunTongXin(**config) #变为关键字传参
    res = yun.run("15016299762",200229)
    print(res)




