# -*- coding: utf-8 -*-
"""
    1、启动一个定时任务，在固定时间启动爬虫
    2、自动登陆：
        2.1、读取chrome保存在本地的cookie
        2.2、解密加密后的cookie值，并构造cookies
        2.3、模拟登陆，获取到验证码、密码、账号， 其中验证码利用OCR识别。通过分析js文件，加密密码以及验证码构造FROM DATA后请求登陆
        2.4、确保服务器后台确认cookies已登录
        2.5、返回cookie
    3、爬虫启动，读取数据库中状态为未爬取的车型编码，并构造成url
    4、在线程池、队列的加持下获取数据、以及存储
    5、修改已抓取数据的状态，方便下次区分是否重复抓取
"""


import json
import pymysql
import time
import requests
from lxml import etree
import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from DBUtils.PooledDB import PooledDB
from requestHeaders import RequestHeaders
from verificationCode import VerificationCode
# from utils import logger


class FittingSpider():
    name = "fitting"
    allowed_domains = ["gcpnew.sany.com.cn"]

    imgUrl = RequestHeaders.imgurl
    header = RequestHeaders.header
    cookies = VerificationCode().getLoginSessionId()
    is_not_leaf_url = RequestHeaders.is_not_leaf_url
    nextImgUrl = RequestHeaders.nextimgurl
    # 车辆号
    results = RequestHeaders().getModelUrl()
    # 存放Url的队列
    fittingUrlQueue = queue.Queue()
    # 存放返回信息的队列，分析时从这里面取
    fittingResponseQueue = queue.Queue()
    # 分析队列，从responseQueue队列中获取数据分析后，存入到analyzeQueue队列中，数据入库从改队列中获取
    fittingQueue = queue.Queue()
    # 图片url队列
    imageUrlQueue = queue.Queue()
    # 存放返回信息的队列，分析时从这里面取
    imageResponseQueue = queue.Queue()
    # 图片信息队列
    imageQueue = queue.Queue()
    # 车辆编号状态队列
    modelStatusQueue = queue.Queue()

    fittingCrawlerThreadStop = False
    analysisFittingThreadStop = False
    saveFittingInfoThreadStop = False
    imageCrawlerThreadStop = False
    imageAnalysisThreadStop = False
    saveImageInfoThreadStop = False
    modelStatusThreadStop = False

    globalData = ""

    db_pool = PooledDB(
        creator=pymysql,  # 使用链接数据库的模块
        maxconnections=5,  # 连接池允许的最大连接数，0和None表示不限制连接数
        mincached=2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
        maxcached=3,  # 链接池中最多闲置的链接，0和None不限制
        maxshared=3,
        # 链接池中最多共享的链接数量，0和None表示全部共享。PS: 无用，因为pymysql和MySQLdb等模块的 threadsafety都为1，
        # 所有值无论设置为多少，_maxcached永远为0，所以永远是所有链接都共享。
        blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
        maxusage=None,  # 一个链接最多被重复使用的次数，None表示无限制
        setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
        ping=0,
        # ping MySQL服务端，检查是否服务可用，如：0 = None = never, 1 = default = whenever it is requested,
        # 2 = when a cursor is created, 4 = when a query is executed, 7 = always
        host="172.16.30.18",
        port=3306,
        user="root",
        password="",
        database="",
    )

    # 构造配件url方法
    def createUrl(self):
        if not self.results:
            return None

        for code in self.results:
            url = 'http://gcpnew.sany.com.cn/SanyGCP/actions/validate/fittingsNavigation/queryEquipment?equipmentNo={}&relaEquip='.format(
                code[1])
            # 初始url入队列
            print("=====", url) 
            self.fittingUrlQueue.put(url)
            self.modelStatusQueue.put(code[1])
            time.sleep(30)

            # 已消费的车辆号入队列， 将状态修改为 2-已消费

            # # 为所有设备建立一个根目录
            # rootDate = {
            #     'equipmentNo': code[1],
            #     'code': code[1],
            #     'pcode': None,
            #     'caption': None,
            #     'deviceCode': None,
            #     'orderdate': None,
            #     'ebomsuffix': None,
            #     'bomsource': None,
            #     'pAdd': None,
            #     'osLayer': None,
            #     'pAbsLayer': None,
            #     'osPictureVersion': None,
            #     'is_leaf': None,
            #     'isParentPicSn': None,
            #     'osItemNo': None,
            # }
            # self.fittingQueue.put(rootDate)
    
    # 修改车辆状态方法，从构造url开始， 视为已使用的车型
    def updateModelStatus(self):
        while not self.modelStatusThreadStop:
            try:
                modelCode = self.modelStatusQueue.get(timeout=90)
            except queue.Empty:
                print("Nothing to do't will go home -- modelStatusThreadStop")
                self.modelStatusThreadStop = True
                break
            # 修改状态
            sql = 'UPDATE _source_model_code SET status = 2 WHERE model_code = "{modelCode}"'.format(modelCode=modelCode)
            conn = self.db_pool.connection()
            cursor = conn.cursor()
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print("update _source_model_code Error!  ", e)
                conn.rollback()
            finally:
                cursor.close()
                conn.close()
            self.modelStatusQueue.task_done()


    # 配件配件信息爬取方法
    def fittingCrawler(self):
        while not self.fittingCrawlerThreadStop:
            try:
                url = self.fittingUrlQueue.get(timeout=30)
            except queue.Empty:
                print("Nothing to do't will go home -- fittingCrawlerThreadStop")
                self.fittingCrawlerThreadStop = True
                break
            resp = requests.post(url, headers=self.header, cookies=self.cookies)
            # 相应信息入队列
            self.fittingResponseQueue.put(resp)
            self.fittingUrlQueue.task_done()

    # 分析配件信息方法
    def analysisFitting(self):

        while not self.analysisFittingThreadStop:
            try:
                fittingResponse = self.fittingResponseQueue.get(timeout=30)
            except queue.Empty:
                print("Nothing to do't will go home -- analysisFittingThreadStop")
                self.analysisFittingThreadStop = True
                break
            try:
                jsld = json.loads(fittingResponse.content)
            except:
                print('# # # # # # cookie错误# # # # # # # # # # # ')
                continue
            # 查询不到车辆信息的时候
            if 'rootInfo' in jsld and (jsld['rootInfo'] == "" or jsld['rootInfo'] is None):
                print('这辆车有问题，有问题啊！！！')
                continue
            if 'rootInfo' in jsld.keys():
                print("根目录入队列")
                equipmentNo = jsld['rootInfo']['equipmentNo']  # 车辆号
                fittingsCode = jsld['rootInfo']['code']  # 物料编码
                pcode = jsld['rootInfo']['pcode']  # 父类物料编码
                bomSource = jsld['rootInfo']['bomsource']
                osPictureVersion = jsld['rootInfo']['osPictureVersion']
                # 修改根目录的父类为null
                jsld['rootInfo']['pcode'] = None
                self.fittingQueue.put(jsld['rootInfo'])
                isParent = '1'
                if isParent == '1':
                    imageUrl = self.imgUrl % (fittingsCode, equipmentNo, bomSource, osPictureVersion, isParent,
                                              int(time.time()))
                    imageUrlDict = {
                        "imageUrl": imageUrl,
                        "fittingsCode": fittingsCode,
                        "equipmentNo": equipmentNo,
                        "pcode": pcode
                    }
                    # 图片url入队列
                    self.imageUrlQueue.put(imageUrlDict)
            # 子类入队列
            for part_type in jsld['childNodeList']:
                equipmentNo = part_type['equipmentNo']  # 车辆号
                fittingsCode = part_type['code']  # 物料编码
                pcode = part_type['pcode']  # 父类物料编码
                # part_name = part_type['caption']  # 物料名称
                deviceCode = part_type['deviceCode']
                orderDate = part_type['orderdate']
                ebomSuffix = part_type['ebomsuffix']
                bomSource = part_type['bomsource']
                padd = part_type['pAdd']
                osLayer = part_type['osLayer']
                pAbsLayer = part_type['pAbsLayer']
                osPictureVersion = part_type['osPictureVersion']
                is_leaf = part_type['is_leaf']
                # 子类配件信息入队列
                self.fittingQueue.put(part_type)
                # 定义一个绝对的层数，只要不是第二次就不为零
                isParent = 'true'
                # 判断是否为叶
                if is_leaf == 0:
                    # 构造下一层级的url入队列
                    isNotLeafUrl = self.is_not_leaf_url % (
                        equipmentNo, fittingsCode, deviceCode, orderDate, ebomSuffix, bomSource, padd, osLayer,
                        pAbsLayer, osPictureVersion)
                    # 配件URL入队列
                    self.fittingUrlQueue.put(isNotLeafUrl)
                    nextImageUrl = self.nextImgUrl % (fittingsCode, bomSource, osPictureVersion, '', '', '', '',
                                                      '', '', isParent, int(time.time()))
                    imageUrlDict = {
                        "imageUrl": nextImageUrl,
                        "fittingsCode": fittingsCode,
                        "equipmentNo": equipmentNo,
                        "pcode": pcode
                    }
                    # 图片信息URL入队列
                    self.imageUrlQueue.put(imageUrlDict)
            self.fittingResponseQueue.task_done()

    # 存储配件方法
    def saveFittingInfo(self):
        while not self.saveFittingInfoThreadStop:
            try:
                # 取值, 超过30s 抛出异常
                fitting = self.fittingQueue.get(timeout=30)
            except queue.Empty:
                print("Nothing to do't will go home -- saveFittingInfoThreadStop")
                self.saveFittingInfoThreadStop = True
                break
            # 定义SQL语句
            sql_insert = 'insert into _sany_crane_fitting' \
                         '(part_code, part_name, parent_code, model_code, model_name, deviceCode, orderDate, ebomSuffix, bomSource,' \
                         'padd, osLayer, pAbsLayer, osPictureVersion, is_leaf, inParentPicSn, osItemNo) ' \
                         'values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
            # 定义值
            if len(fitting):
                value = (fitting['code'], fitting['caption'], fitting['pcode'],
                         fitting['equipmentNo'], fitting['equipmentNo'], fitting['deviceCode'],
                         fitting['orderdate'], fitting['ebomsuffix'], fitting['bomsource'],
                         fitting['pAdd'], fitting['osLayer'], fitting['pAbsLayer'],
                         fitting['osPictureVersion'], fitting['is_leaf'], fitting['inParentPicSn'], fitting['osItemNo'])
                # self.globalData = value
                conn = self.db_pool.connection()
                cursor = conn.cursor()
                try:
                    cursor.execute(sql_insert, value)
                    conn.commit()
                    print(value)
                except Exception as e:
                    print("sss", e)
                    conn.rollback()
                finally:
                    cursor.close()
                    conn.close()
            else:
                print('item Waring!')
            self.fittingQueue.task_done()

    # 图片信息抓取
    def imageCrawler(self):
        while not self.imageCrawlerThreadStop:
            try:
                imageInfo = self.imageUrlQueue.get(timeout=30)
            except queue.Empty:
                print("Nothing to do't will go home -- imageCrawlerThreadStop")
                self.imageCrawlerThreadStop = True
                break

            imageResp = requests.post(imageInfo["imageUrl"], headers=self.header, cookies=self.cookies, )
            imageInfo["imageResp"] = imageResp
            # 响应图片信息入队列
            self.imageResponseQueue.put(imageInfo)
            self.imageUrlQueue.task_done()

    # 图片信息分析方法
    def imageAnalysis(self):
        while not self.imageAnalysisThreadStop:
            try:
                imageResponse = self.imageResponseQueue.get(timeout=30)
            except queue.Empty:
                print("Nothing to do't will go home -- imageAnalysisThreadStop")
                self.imageAnalysisThreadStop = True
                break
            # 接收传递过来的json对象，对象里面包含除了主体外的所有第二级目录
            fittingsCode = imageResponse['fittingsCode']  # 初始等于起重机主体，url里面的物料码，等于是下面的父类物料码
            equipmentNo = imageResponse['equipmentNo']  # 起重机车辆号
            # 图片的url
            html = etree.HTML(imageResponse["imageResp"].text)
            imgurl = html.xpath('//div[@id="draggable"]/img/@src')[0]
            # 获取map里面的信息
            img_list = html.xpath('//map[@name="mapImg"]/area')
            # 定义一个字典，存放图片的坐标和href
            for img in img_list:
                # 图片的坐标, 图片的href
                map_coords = "".join(img.xpath('@coords')[0])
                map_href = "".join(img.xpath('@href')[0])
                # 获取相应的物料码
                map_href_H = map_href.replace(fittingsCode, 'H')  # 将href中的父类替换成一个容易识别的字符，然后获取字符所在的位置
                site = map_href_H.find('H')
                wcode = map_href_H[site + 1:]  # 获取最后一个物料码
                # 图片信息入队列
                itemImg = {
                    'wcode': wcode,
                    'pcode': fittingsCode,
                    'url': imgurl,
                    'coords': map_coords,
                    'href': map_href,
                    'model_code': equipmentNo
                }
                self.imageQueue.put(itemImg)
            self.imageResponseQueue.task_done()

    # 存储图片信息方法
    def saveImageInfo(self):
        # 定义SQL语句
        while not self.saveImageInfoThreadStop:
            try:
                imageInfo = self.imageQueue.get(timeout=30)
            except queue.Empty:
                print("Nothing to do't will go home -- saveImageInfoThreadStop")
                self.saveImageInfoThreadStop = True
                break

            sql_insert = 'insert into _sany_crane_img(part_code, parent_code, coords, href, url, model_code)' \
                         ' values(%s,%s,%s,%s,%s,%s)'
            if len(imageInfo):
                value = (
                    imageInfo['wcode'], imageInfo['pcode'], imageInfo['coords'], imageInfo['href'], imageInfo['url'],
                    imageInfo['model_code'])
                conn = self.db_pool.connection()
                cursor = conn.cursor()
                try:
                    cursor.execute(sql_insert, value)
                    conn.commit()
                    print(value)
                except Exception as e:
                    print("ssssss", e)
                    conn.rollback()
                else:
                    cursor.close()
                    conn.close()
            else:
                print('item Waring!')
            self.imageQueue.task_done()
            
            # 图片下载功能 TODO 暂时没需求

    def run(self):
        # 线程池
        with ThreadPoolExecutor(max_workers=8) as t:
            t.submit(self.createUrl)
            t.submit(self.fittingCrawler)
            t.submit(self.analysisFitting)
            t.submit(self.saveFittingInfo)
            t.submit(self.imageCrawler)
            t.submit(self.imageAnalysis)
            t.submit(self.saveImageInfo)
            t.submit(self.updateModelStatus)

    # 扩展方法，暂时无用
    # def getData(self):
    #     return self.globalData

# if __name__ == '__main__':
#     fs = FittingSpider()
#     fs.run()
    # # 创捷URL 线程
    # createUrlBegin = threading.Thread(target=fs.createUrl)
    # # 爬虫方法 线程
    # fittingCrawlerBegin = threading.Thread(target=fs.fittingCrawler)
    # # 分析方法 线程
    # analysisFittingBegin = threading.Thread(target=fs.analysisFitting)
    # # 存储方法 线程
    # saveFittingInfoBegin = threading.Thread(target=fs.saveFittingInfo)
    # # 图片爬虫 线程
    # imageCrawlerBegin = threading.Thread(target=fs.imageCrawler)
    # # 图片信息分析 线程
    # imageAnalysisBegin = threading.Thread(target=fs.imageAnalysis)
    # # 图片信息存储 线程
    # saveImageInfoBegin = threading.Thread(target=fs.saveImageInfo)
    #
    # createUrlBegin.start()
    # fittingCrawlerBegin.start()
    # analysisFittingBegin.start()
    # saveFittingInfoBegin.start()
    # imageCrawlerBegin.start()
    # imageAnalysisBegin.start()
    # saveImageInfoBegin.start()
    #
    # createUrlBegin.join()
    # fittingCrawlerBegin.join()
    # analysisFittingBegin.join()
    # saveFittingInfoBegin.join()
    # imageCrawlerBegin.join()
    # imageAnalysisBegin.join()
    # saveImageInfoBegin.join()
