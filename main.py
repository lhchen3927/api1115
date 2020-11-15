import unittest
import time
from datetime import datetime
from BeautifulReport import BeautifulReport
from common.handle_path import casesdir
from common.handle_path import reportdir


print(casesdir)
s = unittest.TestLoader().discover(casesdir)
br = BeautifulReport(s)
# report_time = time.strftime('%Y-%m-%d-%H-%M-%S', time.localtime(time.time()))
report_time = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
br.report("api接口测试报告", "api_test_report{}.html".format(report_time), reportdir)
