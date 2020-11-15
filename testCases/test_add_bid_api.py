import os
import unittest

from common.handel_excel import HandleExcel
from common.handle_log import logger
from common.myddt import ddt, data
from common.handle_path import datadir
from common.handle_data import Data, replace_case_with_re, set_dataclass_attr_from_resp
from common.handle_requests import HandleRequests

excel_path = os.path.join(datadir, "api_cases.xlsx")
he = HandleExcel(excel_path, "add")
cases = he.read_all_data()


@ddt
class TestAddBidApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()

    @data(*cases)
    def test_add_bid_api(self, case):
        logger.info("########################开始执行添加项目接口#########################")
        # 替换
        case = replace_case_with_re(case)

        logger.info("当前执行用例为：\n {}".format(case))
        # 请求
        # 判断是否需要传递token
        if hasattr(Data, "token"):
            resp = self.hr.send_requests(case["method"], case["url"], case["request_data"],
                                         token=getattr(Data, "token"))
        else:
            resp = self.hr.send_requests(case["method"], case["url"], case["request_data"])

        # 提取需要的变量
        if case["extract"]:
            set_dataclass_attr_from_resp(resp.json(), case["extract"])

        # 如果有预期结果则用实际结果与预期结果进行比较
        if case["expected"]:
            actual = resp.json()
            logger.info("用例执行结果为: {}".format(actual))
            expected = eval(case["expected"])
            logger.info("用例预期结果为：{}".format(expected))
            try:
                assert actual["code"] == expected["code"]
                if expected.get("msg"):
                    assert actual["msg"] == expected["msg"]
            except AssertionError:
                logger.exception("断言失败！")
                raise AssertionError
            except:
                logger.exception("断言以外的报错！")
                raise
