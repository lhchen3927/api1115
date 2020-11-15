from common.handle_db import HandleDB
from decimal import Decimal
from common.handle_log import logger


class HandleAssert:
    def __init__(self):
        self.sql_com_res = {}  # 存储sql查询之后的比较结果
        self.db = HandleDB()  # 打开数据库连接

    def assert_sql(self, check_sql_str):
        self.get_sql_comp_res(check_sql_str)
        # 关闭数据库连接
        self.db.close()

        if False in self.sql_com_res.values():
            logger.error("断言失败，数据库比对不成功！")
            raise AssertionError
        else:
            logger.info("数据库比对成功！")

    def get_sql_comp_res(self, check_sql_str):

        check_sql_dict = eval(check_sql_str)
        logger.info("数据库校验为：\n{}".format(check_sql_dict))

        if check_sql_dict["check_type"] == "value":
            logger.info("比较sql语句查询结果之后的值")
            sql_res = self.db.get_one(check_sql_dict["check_sql"])
            logger.info("执行sql：{}".format(check_sql_dict["check_sql"]))
            logger.info("查询结果：{}".format(sql_res))
            logger.info("预期结果为：{}".format(check_sql_dict["expected"]))

            # 执行的结果进行比较。sql_res为字典类型
            for key, value in check_sql_dict["expected"].items():
                if key in sql_res.keys():
                    if isinstance(sql_res[key], Decimal):
                        sql_res[key] = float(sql_res[key])
                        logger.info("将Decimal转换为float后的值：{}".format(sql_res[key]))
                    if value == sql_res[key]:
                        self.sql_com_res[key] = True  # 比较成功 存储到sql_com_res中
                        logger.info("比较成功！")
                    else:
                        self.sql_com_res[key] = False  # 比较失败 存储到sql_com_res中
                        logger.info("比较失败！")
                else:
                    logger.info("sql查询结果里面没有对应的列名{}，请检查预期结果或查询语句是否正确}".format(key))
        # 比对slq语句查询之后的条数
        elif check_sql_dict["check_type"] == "count":
            logger.info("比较sql语句查询之后的条数，sql查询结果为整数，只要比对数字即可！")
            sql_res = self.db.get_count(check_sql_dict["check_sql"])
            logger.info("执行sql：{}".format(["check_sql"]))
            logger.info("查询结果：{}".format(sql_res))
            logger.info("预期结果为：{}".format(check_sql_dict["expected"]))
            # 比对
            if sql_res == check_sql_dict["expected"]:
                self.sql_com_res["count"] = True
                logger.info("比较成功！")
            else:
                self.sql_com_res["count"] = False
                logger.info("比较失败！")


if __name__ == '__main__':
    check_sql_str = '{"check_type":"value",' \
                    '"check_sql":"select leave_amount from member where id=33",' \
                    '"expected":{"leave_amount":float(199.99)+55}}'
    ha = HandleAssert()
    # ha.get_sql_comp_res(check_sql_str)
    ha.assert_sql(check_sql_str)



