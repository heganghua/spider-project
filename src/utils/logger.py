# -*- coding: utf-8 -*-

import os
import logging


class Logger(object):

    def __init__(self, loggerName):
        
        # 日志基础设置
        # logging.basicConfig(level=logging.INFO, 
        #             format='%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
        #             filename='log1', 
        #             datefmt='%Y-%m-%d %H:%M:%S',
        #             filemode='a')

        # 创建一个logger
        self.logger = logging.getLogger(loggerName)
        # 定义日志级别······
        self.logger.setLevel(logging.INFO)

        # 创建一个handler, Handler对象的作用是（基于日志消息的level）将消息分发到handler指定的位置（文件、网络、邮件等）
        paths =os.path.dirname(__file__)
        # print(paths)
        lf = logging.FileHandler(paths+'/info.log', encoding='utf-8')
        lf.setLevel(logging.INFO)
        lf.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"))
        #  format='%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 

        # 创建一个用于控制台输出
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO) 
        ch.setFormatter(logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s"))
        
        self.logger.addHandler(lf)
        self.logger.addHandler(ch)

    def get_log(self):
        return self.logger


# if __name__ == "__main__":
#     logger = Logger(__name__).get_log()
#     logger.info("niaoniaopingpingyingying")
#     logger.debug("你的困难流浪")

    

