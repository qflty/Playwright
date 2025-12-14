import requests
from requests.exceptions import RequestException
from utils.logger import logger
from config.config import config


class RequestHandler:
    """处理所有HTTP请求的类"""

    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method, url, params=None, data=None, json=None, headers=None, **kwargs):
        """
        发送HTTP请求
        :param method: 请求方法 GET/POST/PUT/DELETE等
        :param url: 请求URL
        :param params: URL参数
        :param data: 请求体表单数据
        :param json: 请求体JSON数据
        :param headers: 请求头
        :param kwargs: 其他参数
        :return: 响应对象
        """
        method = method.upper()
        logger.info(f"发送 {method} 请求到: {url}")
        if params:
            logger.debug(f"请求参数: {params}")
        if data:
            logger.debug(f"请求体数据: {data}")
        if json:
            logger.debug(f"请求体JSON: {json}")
        if headers:
            logger.debug(f"请求头: {headers}")

        try:
            # 设置默认超时时间
            kwargs.setdefault('timeout', config.api.timeout)

            # 根据请求方法发送请求
            if method == 'GET':
                response = self.session.get(url, params=params, headers=headers, **kwargs)
            elif method == 'POST':
                response = self.session.post(url, params=params, data=data, json=json, headers=headers, **kwargs)
            elif method == 'PUT':
                response = self.session.put(url, params=params, data=data, json=json, headers=headers, **kwargs)
            elif method == 'DELETE':
                response = self.session.delete(url, params=params, headers=headers, **kwargs)
            else:
                raise ValueError(f"不支持的请求方法: {method}")

            logger.info(f"收到响应: 状态码 {response.status_code}")
            if response.status_code >= 400:
                logger.debug(f"响应内容: {response.text}")
            return response

        except RequestException as e:
            logger.error(f"请求异常: {str(e)}")
            raise

    def close_session(self):
        """关闭会话"""
        self.session.close()