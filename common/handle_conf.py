from configparser import ConfigParser
import os
from common.handle_path import confdir


class MyConf(ConfigParser):
    def __init__(self, filename):
        super().__init__()
        # 读取配置文件
        self.read(filename, encoding="utf-8")


# 获取文件路径
file_path = os.path.join(confdir, "register.ini")
conf = MyConf(file_path)
# print(conf.get("log", "name"))

