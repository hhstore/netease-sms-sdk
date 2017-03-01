#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import hashlib
import time
import uuid
import random

"""

# 参考文档:
http://dev.netease.im/docs?doc=server_sms

# 校验:
http://dev.netease.im/docs?doc=server&#接口概述

# 说明:
- 本模块, 有提供接口调用示例.
- 完备测试.
- 未对 网易接口返回值, 作数据提取.
- 部分接口的传入参数, 需要从其他接口提取.


"""


class NeteaseSmsAPI(object):
    """ 网易云信短信验证码服务 API 接口:
    """
    APP_KEY = "9b2a9ade419055031a6e3fab8f89e4XX"
    APP_SECRET = "5d73434078XX"

    # 接口列表:
    API_URLS = {
        "send": "https://api.netease.im/sms/sendcode.action",
        "verify": "https://api.netease.im/sms/verifycode.action",
        "send_template": "https://api.netease.im/sms/sendtemplate.action",
        "query_status": "https://api.netease.im/sms/querystatus.action",
    }

    def __init__(self, app_key=None, app_secret=None):
        self.app_key = app_key or self.APP_KEY
        self.app_secret = app_secret or self.APP_SECRET
        self.urls = self.API_URLS

    @property
    def nonce(self):
        return uuid.uuid4().hex

    @property
    def curtime(self):
        return str(int(time.time()))

    def checksum(self, nonce, curtime):
        s = "{}{}{}".format(self.app_secret, nonce, curtime).encode(encoding="utf-8")
        return hashlib.sha1(s).hexdigest()

    @property
    def http_headers(self):
        """ 构造 HTTP 请求头
        
        :return: 
        """
        nonce = self.nonce
        curtime = self.curtime
        checksum = self.checksum(nonce, curtime)

        return {
            "AppKey": self.app_key,
            "CurTime": curtime,
            "Nonce": nonce,
            "CheckSum": checksum,
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
        }

    @property
    def random_code(self):
        """ 自定义生成6位验证码
        :return: 
        """
        return str(random.randint(100000, 999999))

    @staticmethod
    def _post(url, data, headers):
        r = requests.post(url, data=data, headers=headers)
        print("url: {}\nHTTP-header: {}\nHTTP-data: {}".format(url, headers, data))
        print("\tstatus: {} \tresult: {}".format(r.status_code, r.content))
        return r.json() if r.status_code == 200 else {}

    ##################################################
    #              API 接口
    #
    ##################################################

    def send_code(self, mobile):
        """ 调用网易短信验证码服务接口, 发送验证码到手机.
        :param mobile: 手机号
        :return: 返回调用结果 
                - {'msg': '4', 'code': 200, 'obj': '4123'}
                - obj: 验证码内容
                - code: 状态码
                - msg: 对应 查询里的 send_id 参数
        """
        url = self.urls.get("send")
        data = {
            "mobile": str(mobile)
        }
        return self._post(url, data=data, headers=self.http_headers)

    def send_template(self, template_id, mobiles, params=None):
        """ 发送模板短信
        :param template_id: 模板 ID, 目前测试发现: 只支持通知类模板, 不支持验证码模板.
        :param mobiles: 手机号列表
        :param params: 参数列表
        :return: 
        """
        url = self.urls.get("send_template")
        data = {
            "mobiles": str([mobiles]) if not isinstance(mobiles, list) else mobiles
        }

        if template_id:
            data.update({"templateid": str(template_id)})

        if params:
            params = [params] if not isinstance(params, list) else params
            data.update({"params": str(params)})

        return self._post(url, data=data, headers=self.http_headers)

    def verify_code(self, mobile, code):
        """验证码正确性检查:
            - 只支持常规的验证码检查, 不支持模板验证码检查.
        :param mobile: 手机号
        :param code: 验证码, 对应 send_code() 返回值的 obj 字段
        :return: 
        """
        url = self.urls.get("verify")
        data = {
            "mobile": str(mobile),
            "code": str(code)
        }
        return self._post(url, data=data, headers=self.http_headers)

    def query_status(self, send_id):
        """验证码发送状态查询:
            - 支持常规验证码检查, 同时也支持模板验证码检查.
        :param send_id: 发送 ID, 对应 send_code() 返回值的 msg 字段
        :return: 
        """
        url = self.urls.get("query_status")
        data = {
            "sendid": str(send_id)
        }
        return self._post(url, data=data, headers=self.http_headers)


def run_1():
    mobile = "13380789XXX"
    api = NeteaseSmsAPI()
    api.send_code(mobile)  # 发送短信验证码


def run_2():
    mobile = "13380789XXX"
    api = NeteaseSmsAPI()

    api.query_status("14")             # 状态检查
    api.verify_code(mobile, "3367")    # 验证码正确性验证


def run_3():
    mobile = "13380789XXX"

    # 验证码模板:
    tp_login_id = "3057103"       # 不支持
    tp_register_id = "3061023"    # 不支持
    tp_id = "3049132"             # 支持

    api = NeteaseSmsAPI()

    code = api.random_code
    print("\t\tcode:{}".format(code))
    api.send_template(tp_id, mobile, code)  # 发送模板类验证码


def run_4():
    mobile = "13380789XXX"
    api = NeteaseSmsAPI()

    api.query_status("15")                 # 正常返回, 支持模板类验证码查询
    api.verify_code(mobile, "472451")      # 验证码, 出错, 不支持模板类.


def run():
    # 逐个打开注释, 测试 API 调用
    #run_1()
    #run_2()
    #run_3()
    run_4()


if __name__ == '__main__':
    run()

"""
# 发送验证码短信:
url: https://api.netease.im/sms/sendcode.action
HTTP-header: {'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'CurTime': '1488347303', 'CheckSum': 'daf9bf5bf2d68715c9c12d5612b370ff27623273', 'Nonce': '775dd54709e74a808202a318fbb453eb', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4d0'}

HTTP-data: {'mobile': '13380789XXX'}
	status: 200 	result: b'{"code":200,"msg":"14","obj":"3367"}'


# 查询发送状态:
url: https://api.netease.im/sms/querystatus.action
HTTP-header: {'Nonce': '61e9df9723e54bbf9f14892915ee4406', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'CurTime': '1488347349', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4d0', 'CheckSum': 'e9d47dc5c3347d906de1dbe8f8261a93fe7da01d'}

HTTP-data: {'sendid': '14'}
	status: 200 	result: b'{"code":200,"obj":[{"updatetime":1488347319329,"status":1,"mobile":"+86-13380789XXX"}]}'


# 验证验证码是否正确:
url: https://api.netease.im/sms/verifycode.action
HTTP-header: {'Nonce': 'eb66cf06072647f5af66a8e7ef6dcba0', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'CurTime': '1488347350', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4d0', 'CheckSum': '205618d4dc2d152b6ba1b3a85dc855292991109f'}

HTTP-data: {'mobile': '13380789XXX', 'code': '3367'}
	status: 200 	result: b'{"code":200}'


###############################################

# 发送模板验证码:
		code:472451
url: https://api.netease.im/sms/sendtemplate.action
HTTP-header: {'CurTime': '1488347659', 'CheckSum': '371657b31fb74b94d91a155930f3b2f4d8ce0766', 'Nonce': '164d8355b7464bef93bfe31fefe927d7', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4d0'}
HTTP-data: {'mobiles': "['13380789XXX']", 'params': "['472451']", 'templateid': '3049132'}
	status: 200 	result: b'{"code":200,"msg":"sendid","obj":15}'


# 模板验证码, 状态校验:(支持查询状态)
url: https://api.netease.im/sms/querystatus.action
HTTP-header: {'CurTime': '1488347793', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4d0', 'CheckSum': 'a309b5ec0b978bc09ba4fd4de6487e5e3662231e', 'Nonce': '0a603bd67b434acab1b37ee14e9b7dc4'}
HTTP-data: {'sendid': '15'}
	status: 200 	result: b'{"code":200,"obj":[{"updatetime":1488347672407,"status":1,"mobile":"13380789XXX"}]}'

# 模板验证码, 正确性检查:
#   - 不支持模板检查:
#   - 413	验证失败(短信服务)
#
url: https://api.netease.im/sms/verifycode.action
HTTP-header: {'CurTime': '1488347794', 'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8', 'AppKey': '9b2a9ade419055031a6e3fab8f89e4d0', 'CheckSum': '981c8e6888676d67eaea0139e12890cb8984c3f4', 'Nonce': '87e511c76e1947008f684529ee3f02e7'}
HTTP-data: {'mobile': '13380789XXX', 'code': '472451'}
	status: 200 	result: b'{"code":413,"msg":"verify err","obj":1}'



"""
