import os
import unittest

from common.handel_excel import HandleExcel
from common.handle_path import datadir
from common.handle_requests import HandleRequests
from common.handle_log import logger
from common.myddt import ddt, data
from common.handle_data import replace_case_with_re, Data, set_dataclass_attr_from_resp

excel_path = os.path.join(datadir, "api_cases.xlsx")
he = HandleExcel(excel_path, "invest")
cases = he.read_all_data()


@ddt
class TestInvestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.hr = HandleRequests()

    @data(*cases)
    def test_invest_api(self, case):
        logger.info("#################开始执行投资接口#######################")
        # 替换
        case = replace_case_with_re(case)

        # 请求
        # 判断是否要添加token
        if hasattr(Data, "token"):
            resp = self.hr.send_requests(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            resp = self.hr.send_requests(case["method"], case["url"], case["request_data"])

        # 如果有提取字段，从响应消息中提取对应字段，赋值给Data属性
        if case["extract"]:
            set_dataclass_attr_from_resp(resp.json(), case["extract"])

        # 如果有预期结果，则将实际结果与预期结果进行比较
        if case["expected"]:
            actual = resp.json()
            logger.info("用例执行实际结果：{}".format(actual))
            expected = eval(case["expected"])
            logger.info("用例预期结果：{}".format(expected))
            # 断言
            try:

                assert actual["code"] == expected["code"]
                assert actual["msg"] == expected["msg"]
            except AssertionError:
                logger.exception("断言失败！")
                raise
            except Exception:
                logger.exception("除断言以外的报错！")
                raise
