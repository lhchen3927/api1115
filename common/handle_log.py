import logging
import os
import time
from common.handle_conf import conf
from common.handle_path import logdir


class MyLogger(logging.Logger):
    def __init__(self):
        super().__init__(conf.get("log", "name"))  # 日志收集器名字
        self.setLevel(conf.get("log", "level"))  # 日志收集器级别

        # 3、设置日志输出格式
        fmt = "%(asctime)s %(name)s %(levelname)s %(filename)s [第%(lineno)d行] %(message)s"
        formatter = logging.Formatter(fmt)

        # 4、创建一个输出渠道到终端
        handle1 = logging.StreamHandler()
        handle1.setFormatter(formatter)

        # 4、创建一个输出渠道到文件
        log_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime())
        log_name = conf.get("log", "file") + f" {log_time}.log"
        handle2 = logging.FileHandler(os.path.join(logdir, log_name), encoding="utf-8")
        handle2.setFormatter(formatter)

        # 5、把输出渠道添加到日志收集器对象中
        self.addHandler(handle1)
        self.addHandler(handle2)


# 初始化日志收集器对象
logger = MyLogger()
# logger.info("test")
