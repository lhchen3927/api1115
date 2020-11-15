import unittest
import os
from jsonpath import jsonpath
from common.myddt import ddt, data
from common.handel_excel import HandleExcel
from common.handle_path import datadir
from common.handle_log import logger
from common.handle_requests import HandleRequests
from common.handle_data import Data, set_dataclass_attr_from_resp, replace_case_with_re
from common.handle_assert import HandleAssert

excel_path = os.path.join(datadir, "api_cases.xlsx")
he = HandleExcel(excel_path, "recharge")
cases = he.read_all_data()


# print(cases)


@ddt
class TestRechargeApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        # 实例化HandleRequests类
        cls.hr = HandleRequests()
        # 调用登录接口，从响应结果中获取token member_id
        # resp = cls.hr.send_requests("post",
        #                             "member/login",
        #                             {"mobile_phone": "13770830372", "pwd": "1234567890"})
        # # 转换成字典，提取
        # resp_dict = resp.json()
        # # cls.member_id = resp_dict["data"]["id"]
        # # cls.token = resp_dict["data"]["token_info"]["token"]
        # 通过jsonpath提取响应结果
        # cls.member_id = jsonpath(resp_dict, "$..id")[0]
        # cls.token = jsonpath(resp_dict, "$..token")[0]

    @data(*cases)
    def testRecharge(self, case):
        logger.info("*****************开始执行充值接口用例**************************")
        # 替换
        case = replace_case_with_re(case)

        logger.info("当前测试用例为：\n {}".format(case))
        # 发起请求
        # 判断是否要传递token值
        if hasattr(Data, "token"):
            res = self.hr.send_requests(case["method"], case["url"], case["request_data"], token=getattr(Data, "token"))
        else:
            res = self.hr.send_requests(case["method"], case["url"], case["request_data"])

        # 如果有提取字段，那么需要从响应中提取对应数据,设置为Data.token
        if case["extract"]:
            set_dataclass_attr_from_resp(res.json(), case["extract"])

        # 如果有预期结果，需要把响应结果与预期结果进行比较
        if case["expected"]:
            # 响应结果
            actual = res.json()
            logger.info("用例实际执行结果：\n {}".format(actual))
            expected = eval(case["expected"])
            logger.info("用例预期结果：\n {}".format(expected))

            # 断言
            try:
                assert actual["code"] == expected["code"]
                assert actual["msg"] == expected["msg"]
                if actual["data"]['leave_amount']:
                    assert actual["data"]['leave_amount'] == float(getattr(Data, "money"))
            except AssertionError:
                logger.exception("断言失败！")
                raise  # 把异常抛给unittest框架
            except Exception:
                logger.exception("除断言以外的异常报错！")
                raise

        # 如果有数据库校验，则进行数据库校验
        if case["check_sql"]:
            ha = HandleAssert()
            ha.assert_sql(case["check_sql"])
