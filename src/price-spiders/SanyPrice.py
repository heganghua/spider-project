# -*- coding: utf-8 -*-
"""
@author:华仔 
@file: SanyPrice.py 
@time: 2019/12/19 
"""
from sanyPriceHeaders import Headers
import requests
import pymysql
from lxml import etree
import time

conn = pymysql.connect(
    host='172.16.30.20',
    user='root',
    passwd='hua1315579747',
    db='heganghua_copy',
    port=3306,
    charset='utf8', )
cursor = conn.cursor()

sql = 'select product_code from sany_price'
res = ''
try:
    cursor.execute(sql)
    res = cursor.fetchall()
except BaseException as e:
    print('select Error!', e)
partList = res

def insertData(productCode, price):
    sql = 'update sany_price set part_price  = %s where product_code = %s'
    value = (price, productCode)
    try:
        cursor.execute(sql, value)
        conn.commit()
    except Exception as e:
        conn.rollback()
        print("update Error！！", e)
    else:
        print("successfully!")

def getPage():
    for i in range(0, len(partList)):
        print(">>>>>>>> " + str(i) + ": " + partList[i][0])
        price = 0
        productCode = partList[i]
        sanyData = Headers.data
        sanyData["C14_W48_V52_V51_searchnode_parameters[2].value1"] = productCode[0]
        url = Headers.url
        sanyHeaders = Headers.headers
        sanyCookies = Headers.cookies
        priceList = ""
        # try:
        response = requests.post(url=url, data=sanyData, headers=sanyHeaders, allow_redirects=False,
                            cookies=sanyCookies, verify=False)
        # print(response.text)
        html = etree.HTML(response.text)
        response.close()
        priceList = html.xpath('//*[@id="C15_W49_V55_CondRecList_Table[1].KBETR_PRT"]/text()')
        # except Exception as e:
        #     time.sleep(60)
            # pass
        print(priceList)
        price = priceList[0] if priceList else ''
        if price:
            print(price)
            insertData(productCode, price)
            print("\n")
        time.sleep(1.5)



if __name__ == '__main__':
    getPage()
