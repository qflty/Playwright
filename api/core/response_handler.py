import json

from utils.logger import logger


class ResponseHandler:
    """处理响应解析和变量提取的类"""

    @staticmethod
    def parse_response(response):
        """
        解析响应内容
        :param response: 响应对象
        :return: 解析后的响应数据（JSON或文本）
        """
        try:
            return response.json()
        except json.JSONDecodeError:
            logger.warning("响应不是JSON格式，返回文本内容")
            return response.text
        except Exception as e:
            logger.error(f"解析响应失败: {str(e)}")
            return None

    @staticmethod
    def extract_variables(response_data, extract_rules):
        """
        从响应中提取变量
        :param response_data: 解析后的响应数据
        :param extract_rules: 提取规则，格式为字典 {"变量名": "json路径"}
        :return: 提取的变量字典
        """
        variables = {}
        if not extract_rules or not isinstance(extract_rules, dict):
            return variables

        for var_name, json_path in extract_rules.items():
            # 简单的JSON路径解析，支持a.b.c格式
            keys = json_path.split('.')
            value = response_data
            try:
                for key in keys:
                    if isinstance(value, list) and key.isdigit():
                        value = value[int(key)]
                    else:
                        value = value[key]
                variables[var_name] = value
                logger.debug(f"提取变量成功: {var_name} = {value}")
            except (KeyError, IndexError, TypeError) as e:
                logger.warning(f"提取变量失败: {var_name}，路径: {json_path}，错误: {str(e)}")

        return variables