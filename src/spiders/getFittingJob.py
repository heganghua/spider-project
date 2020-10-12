# -*- coding: utf-8 -*-

import os
import sys
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) #当前程序上上一级目录，这里为mycompany
# e:\workspace\workspace-jxzj-python\sany-spider-project\sany-spider\src
# print(BASE_DIR)
sys.path.append(BASE_DIR)
# print(sys.path)
import traceback
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import time
import logging
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
import datetime
# from utils import logger


logging.basicConfig(level=logging.INFO, 
                format='%(asctime)s - %(filename)s[line:%(lineno)d] %(levelname)s %(message)s', 
                filename='log1', 
                datefmt='%Y-%m-%d %H:%M:%S',
                filemode='a')            

def job_function():
    from main import FittingSpider
    FittingSpider().run()

"""
    hour = 19, minute = 23  每天的晚上七点23分执行
    hour = '19', minute = '23' 同上，可以传整型也可以传字符类型
    minute = '*/5' 表示每5分钟执行一次？
    hour = '19-21', minute = '23' 表示 19:23、20:23、21:23 各执行一次任务
"""
def sanySpiderJob():
    print("开始任务")
    # 创建一个调度器
    scheduler = BlockingScheduler()
    # 将任务触发器， 运行方法添加进入调度器
    scheduler.add_job(job_function, 'cron', hour=15, minute=48)
    print('Press Ctral+{0} to exit '.format('Break' if os.name == 'nt' else 'C   '))
    scheduler.start()
    # try:
    #     scheduler.start()
    # except (KeyboardInterrupt, SystemExit):
    #     logging.debug(traceback.format_exc())
    scheduler._logger = logging

if __name__ == "__main__":
    sanySpiderJob()

# logger = logger.Logger(__name__).get_log()

# def tick():
#     print("TICK ! the time is : %s" % datetime.now())
#     i = 1
#     while(i <= 10):
#         print("i for each %s" %i)
#         i+=1
#     return None

# def blockingSchedulerTest(self):
#     scheduler = BlockingScheduler()
#     scheduler.add_job(self.tick, 'interval', seconds=3)
#     print('Press ctrl + {0} to exit'.format('Break' if os.name == 'nt' else 'C'))
#     try:
#         scheduler.start()
#     except (KeyboardInterrupt, SystemExit):
#         pass

# def backgroundSchedulerTest(self):
#     scheduler = BackgroundScheduler()
#     scheduler.add_job(self.tick, 'interval', seconds = 3)
#     scheduler.start()
#     print('Press ctrl + {0} to exit'.format('C  ' if os.name == 'nt' else 'Break  '))
#     try :
#         while True:
#             time.sleep(2)
#     except (KeyboardInterrupt, SystemExit):
#         scheduler.shutdown()