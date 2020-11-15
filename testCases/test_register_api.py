import unittest
import os
from time import sleep
from common.myddt import ddt, data
from common.handel_excel import HandleExcel
from common.handle_db import HandleDB
from common.handle_path import datadir
from common.handle_requests import HandleRequests
from common.handle_log import logger
from common.handle_phone import get_new_phone
from common.handle_conf import conf
from common.handle_assert import HandleAssert
from common.handle_data import replace_case_with_re

# 获取用例数据
excel_path = os.path.join(datadir, "api_cases.xlsx")
he = HandleExcel(excel_path, "register")
cases = he.read_all_data()


# print(cases)

@ddt
class TestRegisterApi(unittest.TestCase):
    @classmethod
    def setUp(cls) -> None:
        cls.hr = HandleRequests()
        cls.hd = HandleDB()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.hd.close()

    @data(*cases)
    def test_register(self, case):
        logger.info("*************************** 开始执行注册接口测试用例 ***************************")
        # 替换手机号
        case = replace_case_with_re(case)
        # 替换需要替换的--系统中已存在的手机号--从配置文件读取
        if case["request_data"].find("*phone*") != -1:
            phone = conf.get("user", "user")
            case["request_data"] = case["request_data"].replace("*phone*", phone)
            # 替换需要替换的--系统中已存在的手机号--从配置文件读取
        if case["request_data"].find("*pwd*") != -1:
            pwd = conf.get("user", "pwd")
            case["request_data"] = case["request_data"].replace("*pwd*", pwd)

        # 发起请求
        resp = self.hr.send_requests(case["method"], case["url"], case["request_data"])
        logger.info("当前测试用例为：\n {}".format(case))
        if case["expected"]:
            # 响应结果
            actual = resp.json()
            logger.info("用例实际执行结果：\n {}".format(actual))
            expected = eval(case["expected"])
            logger.info("用例预期结果：\n {}".format(expected))

            # 断言
            try:
                assert actual["code"] == expected["code"]
                assert actual["msg"] == expected["msg"]
            except AssertionError:
                logger.exception("断言失败！")
                raise  # 把异常抛给unittest框架
            except Exception:
                logger.exception("除断言以外的异常报错！")
                raise

        if case["check_sql"]:
            sleep(0.5)  # 等待服务器数据与数据库交互完成
            ha = HandleAssert()
            ha.assert_sql(case["check_sql"])
