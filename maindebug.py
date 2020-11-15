import unittest
import time
from BeautifulReport import BeautifulReport
from common.handle_path import casesdebugdir
from common.handle_path import reportdir


print(casesdebugdir)
s = unittest.TestLoader().discover(casesdebugdir)
br = BeautifulReport(s)
report_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
br.report("api接口测试报告", "api_test_report{}.html".format(report_time), reportdir)
