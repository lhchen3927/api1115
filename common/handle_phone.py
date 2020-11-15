from random import randint
from common.handle_db import HandleDB

prefix = [133, 153, 177, 180, 181, 189,
          130, 131, 132, 145, 155, 156, 185, 186,
          134, 135, 136, 137, 138, 139, 147, 150, 151, 152, 157, 158, 159, 182, 183, 184, 187, 188]


def __gen_phone():
    # 前3位号段
    index = randint(0, len(prefix) - 1)
    pre_three = prefix[index]
    # 后8位手机号
    after_eight = ""
    for i in range(8):
        new_num = str(randint(0, 9))
        after_eight += new_num
    new_phone = str(pre_three) + after_eight
    return new_phone


def get_new_phone():
    # 判断手机号是否已经注册，如果已经注册，重新生成新的手机号码
    while True:
        phone = __gen_phone()
        # 向数据库查询手机号是否已存在，如果查询结果为0，则为未注册，return退出循环
        hd = HandleDB()
        select_sql = f"select * from member where mobile_phone={phone};"
        count = hd.get_count(select_sql)
        if count == 0:
            hd.close()
            return phone


# print(get_new_phone())
