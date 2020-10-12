# -*- coding: utf-8 -*-
"""
@author:华仔 
@file: requestHeaders.py
@time: 2020/06/29 
"""
import pymysql
import os


class RequestHeaders(object):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    referer = "http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/init"
    accept = "application/json, text/javascript, */*; q=0.01"
    is_not_leaf_url = 'http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/lQueryNodeInfo?equipmentNo=%s&fittingsCode=%s&deviceCode=%s&orderDate=%s&ebomSuffix=%s&bomSource=%s&padd=%s&osLayer=%s&pAbsLayer=%s&osPictureVersion=%s'
    imgurl = 'http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/getImages?fittingsCode=%s&equipmentNo=%s&bomSource=%s&osPictureVersion=%s&isParent=%s&time=%s'
    nextimgurl = 'http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/getImages?fittingsCode=%s&bomSource=%s&osPictureVersion=%s&nodeId=%s&itemNo=%s&pOsPictureVersion=%s&pNodeId=%s&inParentPicSn=%s&pFittingsCode=%s&isParent=%s&time=%s'
    # 登陆URL
    loginUrl = "http://gcpnew.sany.com.cn/SanyGCP/actions/anonymity/login/login"
    # 生成验证码
    randJpg = "http://gcpnew.sany.com.cn/SanyGCP/pages/common/rand.jsp"

    # cookies = {}
    # cookies = VerificationCode.run()
    # path = os.path.abspath(os.path.dirname(__file__))
    # print(path)
    # with open(path+"/cookies.txt") as f:
    #     for line in f.read().split(';'):
    #         name, value = line.strip().split('=', 1)
    #         cookies[name] = value

    header = {
        "user-Agent": user_agent,
        "Connection": "keep-alive",
        "Referer": referer,
        "Accept": accept,
        "Proxy_Connection": "keep-alive",
    }

    loginRequestHeaders = {
        "Host": "gcpnew.sany.com.cn",
        "Content-Length": "85",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Origin": "http://gcpnew.sany.com.cn",
        "Content-Type": "application/x-www-form-urlencoded",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://gcpnew.sany.com.cn/SanyGCP/pages/common/login.jsp",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7",
        # "Cookie": "JSESSIONID=A7E193275FCE987F192CECD8692BC8DB",
        "Connection": "keep-alive"
    }

    welcomeRequestHeaders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,und;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        # "Cookie": "JSESSIONID=91B0899938F5953014BC4CDAC20CABBC",
        "Host": "gcpnew.sany.com.cn",
        "Referer": "http://gcpnew.sany.com.cn/SanyGCP/actions/validate/firstpage/welcome?result=1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36"
    }

    conn = pymysql.connect(
        host='172.16.30.18',
        user='root',
        passwd='',
        db='',
        port=3306,
        charset='utf8', )
    cursor = conn.cursor()

    def getModelUrl(self):
        sql = 'SELECT * FROM _source_model_code where status = 1'
        results = []
        try:
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
        except Exception as e:
            # print(e)
            print('Error: unable to fecth data', e)
        # urls = []
        # for code in results:
        #     urls.append(
        #         'http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/queryEquipment?equipmentNo={}&relaEquip='.format(
        #             code[1]))
        # items = []
        return results


    loginFromData = {
        "accountName": "",
        # 密码经过MD5加密后的密文加上验证码后MD5， MD5(MD5(password)+rand)
        "password": "",
        "rand": "",
        "Language": "zh-CN"
    }


# if __name__ == '__main__':
#     cookies = RequestHeaders().cookies
#     print(cookies)
