# -*- coding: utf-8 -*-
"""
 主要实现验证码识别;
 账号密码模拟登陆;
"""


from requestHeaders import RequestHeaders
import requests
from lxml import etree
import pytesseract
from PIL import Image
import time
import http.cookiejar as cookielib
import base64
import hashlib
import json
import os
import sqlite3
import decrypt
# from win32.win32crypt import CryptUnprotectData

class VerificationCode(object):
    
    loginUrl = RequestHeaders.loginUrl
    headers = RequestHeaders.header
    loginFromData = RequestHeaders.loginFromData
    randJpg = RequestHeaders.randJpg
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=UckOcNY8HXHCoDWUY3fLKMHs&client_secret=RjkRU6Qlf41YIS71Y2waLD57jKic8bqz'
    ocrUrl = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 车辆号
    # results = RequestHeaders.results
    fittingUrl = 'http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/queryEquipment?equipmentNo={}&relaEquip='
    loginRequestHeaders = RequestHeaders.loginRequestHeaders
    welcomeUrl = "http://gcpnew.sany.com.cn/SanyGCP/actions/validate/firstpage/welcome?result=1"
    validateUrl = "http://gcpnew.sany.com.cn/SanyGCP/actions/validate/personal/countDeliver?toDo=1"
    loginJsp = "http://gcpnew.sany.com.cn/SanyGCP/pages/common/login.jsp"
    welcomeRequestHeaders = RequestHeaders.welcomeRequestHeaders
    # loginOut = "http://gcpnew.sany.com.cn/SanyGCP/actions/anonymity/login/logout"

    # 保存验证码到本地
    def getRand(self, cookies):
        randResp = requests.get(url=self.randJpg, headers=self.headers, verify=False, cookies=cookies)
        with open("sany-spider/src/rand.jpg","wb") as f:
            f.write(randResp.content)
   
    def is_login(self, cookies):
        time.sleep(0.5)
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36"
        }
        response = requests.get(url=self.validateUrl, verify=False, headers=headers, cookies=cookies, allow_redirects=False)
        print(response.text)
        if response.text:
            data = response.json()
            if 'rowsCount' in data.keys():
                return True
            else:
                return False
        else:
            return False

    # 对验证码进行OCR识别, 调用百度通用文字识别进行处理API
    def randJpgOcr(self):
        # 调用百度Api
        tokenResp = requests.get(self.host, verify=False)
        access_token = ""
        if tokenResp:
            access_token = tokenResp.json()['access_token']
        f = open("sany-spider/src/rand.jpg", "rb")
        image = base64.b64encode(f.read())
        params = {"image": image}
        ocrUrl = self.ocrUrl + "?access_token=" + access_token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        randResp = requests.post(ocrUrl, data=params, headers=headers, verify=False)
        randJson = randResp.json()
        if 'words_result' in randJson.keys():
            words = randJson["words_result"][0]["words"]
            # print("rand================", words)
        return words

    # 登陆
    def login_user(self, rand, cookies):
        loginFromData = self.loginFromData
        m1 = hashlib.md5("".encode())
        pas = m1.hexdigest()
        strs = pas + rand
        m2 = hashlib.md5(strs.encode())
        password = m2.hexdigest()
        # 构造data数据
        loginFromData["password"] = password        
        loginFromData["rand"] = rand
        response = requests.post(url=self.loginUrl, headers=self.loginRequestHeaders, data=loginFromData, verify=False , cookies=cookies)
        if response.url == self.welcomeUrl:
            print("Login successful!", response.url)
            return True
        else:
            raise SyntaxError('Login exception...')

    def getLocationCookie(self):
        domain = "gcpnew.sany.com.cn"
        cookies = decrypt.get_cookies_from_chrome(domain)
        return cookies

    def getLoginSessionId(self):
        # 初始化登陆
        requests.get(url=self.loginJsp, headers=self.headers, verify=False)
        time.sleep(10)
        # 拿到本地cookies
        cookies = self.getLocationCookie()
        print(cookies)
        # 是否登陆
        isLogin = self.is_login(cookies)
        if not isLogin:
            self.getRand(cookies)
            time.sleep(0.5)
            rand = self.randJpgOcr()
            self.login_user(rand, cookies)               
        else:
            print("Login in", cookies)
        return cookies


# if __name__ == "__main__":
#     vc = VerificationCode()
#     vc.getLoginSessionId()