# -*- coding: utf-8 -*-

import logging
import os
import sys

from time import strftime

PATH = os.path.abspath('.') + '/logs/'
FMT = '%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s\t: %(message)s'
# AFMT = '%(asctime)s\t: [%(remote_addr)s %(url)s] %(method)s %(request_data)s %(message)s'
DATETIMEFMT = '%Y-%m-%d %H:%M:%S'


class RequestFormatter(logging.Formatter):
    def format(self, record):
        return super().format(record)


class MyLogger(object):
    def __init__(self):
        self.logger = logging.getLogger("nallm")
        self.formatter = RequestFormatter(fmt=FMT, datefmt=DATETIMEFMT)

        self.log_filename = '{0}{1}.log'.format(PATH, strftime("%Y-%m-%d"))
        # self.mylog.addHandler(self.get_file_handler(self.log_filename))
        self.logger.addHandler(self.get_console_handler())
        self.logger.setLevel(logging.DEBUG)

    # 输出到文件handler的函数定义
    def get_file_handler(self, filename):
        filehandler = logging.FileHandler(filename, encoding="utf-8")
        filehandler.setFormatter(self.formatter)
        return filehandler

    # 输出到控制台handler的函数定义
    def get_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(self.formatter)
        return console_handler


log = MyLogger().logger
