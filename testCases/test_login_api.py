import unittest
import os
from common.myddt import ddt, data
from common.handel_excel import HandleExcel
from common.handle_path import datadir
from common.handle_log import logger
from common.handle_requests import HandleRequests
from common.handle_data import replace_case_with_re
from common.handle_conf import conf

excel_path = os.path.join(datadir, "api_cases.xlsx")
he = HandleExcel(excel_path, "login")
cases = he.read_all_data()


# print(cases)


@ddt
class TestLoginApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 实例化HandleRequests类
        cls.hr = HandleRequests()

    @data(*cases)
    def testLogin(self, case):
        logger.info("*****************开始执行登录接口用例**************************")
        # 替换需要替换的未注册的手机号
        case = replace_case_with_re(case)
        # 替换需要替换的--系统中已存在的手机号--从配置文件读取
        if case["request_data"].find("*phone*") != -1:
            phone = conf.get("user", "user")
            case["request_data"] = case["request_data"].replace("*phone*", phone)
            # 替换需要替换的--系统中已存在的手机号--从配置文件读取
        if case["request_data"].find("*pwd*") != -1:
            pwd = conf.get("user", "pwd")
            case["request_data"] = case["request_data"].replace("*pwd*", pwd)

        logger.info("当前测试用例为：\n {}".format(case))
        # 发起请求
        res = self.hr.send_requests(case["method"], case["url"], case["request_data"])

        if case["expected"]:
            try:
                # 实际结果
                actual = res.json()
                logger.info("实际结果为：{}".format(actual))
                expected = eval(case["expected"])
                logger.info("预期结果为：{}".format(case["expected"]))
                assert actual["code"] == expected["code"]
                assert actual["msg"] == expected["msg"]
            except AssertionError:
                logger.exception("断言失败")
                raise
            except Exception:
                logger.exception("除断言以外的报错")
                raise
