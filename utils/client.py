import requests
from requests.exceptions import RequestException
from config.config import config
from utils.logger import logger


class ApiClient:
    """API客户端封装"""

    def __init__(self, base_url=None):
        self.base_url = base_url or config.api.base_url
        self.session = requests.Session()
        self.token = None

    def set_headers(self, headers=None):
        """设置默认请求头"""
        if headers:
            self.session.headers.update(headers)

    def set_token(self, token):
        """设置认证token"""
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def request(self, method, url, **kwargs):
        """通用请求方法"""
        full_url = f"{self.base_url}{url}" if url.startswith("/") else f"{self.base_url}/{url}"

        try:
            logger.info(f"请求: {method} {full_url}")
            logger.debug(f"请求参数: {kwargs}")

            response = self.session.request(method, full_url, **kwargs)
            response.raise_for_status()  # 抛出HTTP错误

            logger.info(f"响应: {response.status_code}")
            logger.debug(f"响应内容: {response.text}")

            return response

        except RequestException as e:
            logger.error(f"请求错误: {str(e)}")
            raise

    def get(self, url, params=None, **kwargs):
        """GET请求"""
        return self.request("GET", url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        """POST请求"""
        return self.request("POST", url, data=data, json=json, **kwargs)

    def put(self, url, data=None, json=None, **kwargs):
        """PUT请求"""
        return self.request("PUT", url, data=data, json=json, **kwargs)

    def delete(self, url, **kwargs):
        """DELETE请求"""
        return self.request("DELETE", url, **kwargs)

    def login(self, username=None, password=None):
        """登录并获取token"""
        username = username or config.username
        password = password or config.password

        response = self.post(
            "/auth/login",
            json={"username": username, "password": password}
        )

        result = response.json()
        if "token" in result:
            self.set_token(result["token"])
            return result["token"]

        return None
