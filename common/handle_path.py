import os

# 项目根目录
rootdir = os.path.dirname(os.path.dirname(__file__))
# 配置文件目录
confdir = os.path.join(rootdir, "conf")
# 日志文件目录
logdir = os.path.join(rootdir, "outputs", "logs")
# 测试报告目录
reportdir = os.path.join(rootdir, "outputs", "reports")
# 测试用例目录
casesdir = os.path.join(rootdir, "testCases")
# 测试数据目录
datadir = os.path.join(rootdir, "testDatas")
# 测试用例debug目录
casesdebugdir = os.path.join(rootdir, "testdebug")

