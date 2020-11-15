from jsonpath import jsonpath
import re
from common.handle_log import logger
from common.handle_phone import get_new_phone


# # excel中数据
# expr = '{"member_id":"$..id","token":"$..token"}'
# res = {'code': 0,
#        'msg': 'OK',
#        'data': {'id': 204737,
#                 'leave_amount': 0.0,
#                 'mobile_phone': '13770830399',
#                 'reg_name': 'qianyu',
#                 'reg_time': '2020-11-01 14:12:12.0',
#                 'type': 1,
#                 'token_info': {'token_type': 'Bearer',
#                                'expires_in': '2020-11-01 14:35:53',
#                                'token': 'eyJhbGciOiJIUzUxMiJ9.eyJtZW1iZXJfaWQiOjIwNDczNywiZXhwIjoxNjA0MjEyNTUzfQ.e7PbF1FDBRLqU3pfOZpfwsu1GKeejfDZat6cAfowTNDKq-76g6PrrsPq3O_bWiK719aTLSvtiCBp3KU3JUSgnA'}},
#        'copyright': 'Copyright 柠檬班 © 2017-2020 湖南省零檬信息技术有限公司 All Rights Reserved'}


# 专门用来放数据，用例执行过程中，可以动态设置此类的属性
class Data:
    pass


# 设置提取数据
def set_dataclass_attr_from_resp(resp, extract):
    """
    :param resp: 请求的响应结果的字典类型
    :param extract:从excel中读取的，要从响应结果中提取的key-value，字符串类型
    """
    # 将字符串转换为字典类型
    data_dict = eval(extract)
    # 遍历key-value，将每一个jsonpath的表达式，替换成对应的数据
    for key, value in data_dict.items():
        # 将每一个jsonpath的表达式替换成对应的数据
        real_value = jsonpath(resp, value)
        if real_value:
            setattr(Data, key, str(real_value[0]))  # 给Data类动态设置key-value
    # print("Data类属性", Data.__dict__)


# 原始版本不用
def replace_data_from_re_v1(case_dict):
    """
    1、遍历case中的每一个key-value，如果value匹配到"#(\w+)#"，提取出来
    2、将Data类中对应的数据替换到value中
    3、全部替换完成后将case[key]重新赋值
    :param case_dict:从excel中读取出来的用例数据，字典类型
    :return:全部替换完成后的case
    """
    # case是从excel中读取出来的用例-字典类型，包含了excel中的多个key
    for key, value in case_dict.items():
        if isinstance(value, str):
            # 正则提取
            res = re.findall("#(\w+)#", value)  # 列表
            if res:  # 列表不为空
                for item in res:
                    value = value.replace(f"#{item}#", getattr(Data, item))
                case_dict[key] = value
    return case_dict


# 原始版本不用
def replace_data_from_re_v2(case_dict):
    """
    1、遍历case中的每一个key-value，如果value匹配到"#(\w+)#"，提取出来
    2、将Data类中对应的数据替换到value中
    3、全部替换完成后将case[key]重新赋值
    :param case_dict:从excel中读取出来的用例数据，字典类型
    :return:全部替换完成后的case
    """
    case_str = str(case_dict)
    # 正则提取
    res = re.findall("#(\w+)#", case_str)  # 列表
    if res:  # 列表不为空
        for item in res:
            case_str = case_str.replace(f"#{item}#", getattr(Data, item))
    return eval(case_str)


# 最后更新版本--替换正则表达式后的用例
def replace_case_with_re(case_dict):
    case_str = str(case_dict)
    # 提取正则表达式
    replace_mark_list = re.findall("#(\w+)#", case_str)
    logger.info("用例中提取到的正则结果{}".format(replace_mark_list))

    # 如果有手机号需要未注册的，调用函数生成新的未注册过手机号
    if "phone" in replace_mark_list:
        new_phone = get_new_phone()
        setattr(Data, "phone", new_phone)  # 将新生成的手机号设置成Data类属性
        logger.info("如果有手机号需要未注册的，调用函数生成新的未注册过手机号,将新生成的手机号设置成Data类属性")
    if replace_mark_list:
        for mark in replace_mark_list:  # 遍历正则结果列表
            case_str = case_str.replace(f"#{mark}#", getattr(Data, mark))
            logger.info(f"替换#{mark}#,替换后{mark}值为：{getattr(Data, mark)}")
        logger.info("替换后用例为：\n {}".format(case_str))
    return eval(case_str)

