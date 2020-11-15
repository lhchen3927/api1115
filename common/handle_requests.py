import requests
import json
from common.handle_log import logger
from common.handle_conf import conf


class HandleRequests:
    def __init__(self):
        self.headers = {"X-Lemonban-Media-Type": "lemonban.v2"}

    def send_requests(self, method, url, data=None, token=None):
        logger.info("==================开始发起请求============================")
        logger.info("请求方法为：{}".format(method))
        # 请求头处理
        self.__deal_header(token)
        # 请求数据处理
        self.__deal_data(data)
        # 处理url
        self.__deal_url(url)
        if method.upper() == "GET":
            response = requests.get(self.url, self.data, headers=self.headers)
        elif method.upper() == "PATCH":
            response = requests.patch(self.url, json=self.data, headers=self.headers)
        else:
            response = requests.post(self.url, json=self.data, headers=self.headers)
        logger.info("请求响应状态码：{}".format(response.status_code))
        logger.info("请求响应为：\n {}".format(response.json()))
        return response

    def __deal_header(self, token=None):
        if token is not None:
            self.headers["Authorization"] = f"Bearer {token}"
        logger.info("请求头为：\n {}".format(self.headers))

    def __deal_data(self, data):
        if isinstance(data, str):
            self.data = json.loads(data)
        else:
            self.data = data
        logger.info("请求数据为：\n {}".format(self.data))

    # 处理url 读取配置文件中的baseurl与excel中读取的拼接
    def __deal_url(self, url):
        if url.startswith("http://") or url.startswith("https://"):
            self.url = url
        else:
            # 从配置文件读取url地址，excel中以/结尾
            base_url = conf.get("server", "baseurl")
            self.url = base_url + url
        logger.info("请求url为：\n {}".format(self.url))


if __name__ == '__main__':
    hr = HandleRequests()
    url = "member/login"
    data1 = '{"mobile_phone": "13770830372", "pwd": "1234567890"}'
    resp = hr.send_requests("post", url, data1)
    print(resp.json())
