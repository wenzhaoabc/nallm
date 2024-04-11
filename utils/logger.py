import datetime
import logging

# 创建一个logger
logger = logging.getLogger('retrival')
logger.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个handler，用于写入日志文件
filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S.log")
fh = logging.FileHandler('../static/logs/' + filename)
fh.setLevel(logging.DEBUG)  # 设置日志级别

# 创建一个handler，用于输出到控制台
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)  # 设置日志级别

# 定义handler的输出格式
formatter = logging.Formatter('%(asctime)s - [%(filename)s:%(lineno)d] - %(levelname)-7s : %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# 给logger添加handler
logger.addHandler(fh)
logger.addHandler(ch)

# 记录一条日志
logger.info('This is a log info')
logger.debug('Debugging')
logger.warning('Warning exists')
logger.info('Finish')
