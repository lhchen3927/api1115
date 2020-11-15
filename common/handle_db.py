import pymysql
from common.handle_conf import conf
from common.handle_log import logger


class HandleDB:
    def __init__(self):
        try:
            # 1、创建数据库连接
            self.conn = pymysql.connect(host=conf.get("mysql", "host"),
                                        user=conf.get("mysql", "user"),
                                        password=conf.get("mysql", "password"),
                                        database=conf.get("mysql", "db"),
                                        port=conf.getint("mysql", "port"),
                                        charset="utf8",
                                        cursorclass=pymysql.cursors.DictCursor)
            # 2、建立游标
            self.cur = self.conn.cursor()
        except:
            logger.exception("数据库连接失败，请检查！")
            raise

    # 获取查询结果个数
    def get_count(self, sql, args=None):
        try:
            self.conn.commit()
            ct = self.cur.execute(sql, args)
            logger.info(f"查询个数{ct}")
            return ct
        except:
            logger.exception("查询报错，请检查sql语句！")

    # 获取一条数据
    def get_one(self, sql, args=None):
        self.conn.commit()
        self.get_count(sql, args=args)
        return self.cur.fetchone()

    # 获取所有数据
    def get_all(self, sql, args=None):
        self.conn.commit()
        self.get_count(sql, args=args)
        return self.cur.fetchall()

    # 修改数据 - 事务回滚(rollback)和提交(commit)
    def update(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except:
            logger.exception("数据操作失败!")
            self.conn.rollback()

    # 关闭连接
    def close(self):
        self.cur.close()
        self.conn.close()


if __name__ == '__main__':
    hd = HandleDB()
    count = hd.get_count("select * from member where mobile_phone=13770830372;")
    print(count)
    print(hd.get_one("select * from member where mobile_phone=13770830372;"))
    hd.close()
