from utils.logger import logger


class Validator:
    """处理断言验证的类"""

    @staticmethod
    def assert_response(response_data, assert_rules):
        """
        断言响应结果
        :param response_data: 解析后的响应数据
        :param assert_rules: 断言规则，格式为字典 {"json路径": "预期值"}
        :return: (是否成功, 断言消息)
        """
        if not assert_rules or not isinstance(assert_rules, dict):
            return True, "无断言规则"

        success = True
        messages = []

        for key, expected_value in assert_rules.items():
            # 简单的JSON路径解析
            keys = key.split('.')
            actual_value = response_data
            try:
                for k in keys:
                    if isinstance(actual_value, list) and k.isdigit():
                        actual_value = actual_value[int(k)]
                    else:
                        actual_value = actual_value[k]

                if actual_value != expected_value:
                    success = False
                    messages.append(f"断言失败: {key} 预期 {expected_value}, 实际 {actual_value}")
                else:
                    messages.append(f"断言成功: {key} = {expected_value}")
            except (KeyError, IndexError, TypeError) as e:
                success = False
                messages.append(f"断言失败: 无法获取 {key} 的值，错误: {str(e)}")

        logger.debug("; ".join(messages))
        return success, "; ".join(messages)

    @staticmethod
    def assert_status_code(status_code, expected_codes):
        """
        断言状态码
        :param status_code: 实际状态码
        :param expected_codes: 预期状态码，可以是单个值或列表
        :return: (是否成功, 断言消息)
        """
        if not isinstance(expected_codes, list):
            expected_codes = [expected_codes]

        if status_code in expected_codes:
            msg = f"状态码断言成功: {status_code} 在预期范围内 {expected_codes}"
            logger.debug(msg)
            return True, msg
        else:
            msg = f"状态码断言失败: 实际 {status_code}, 预期 {expected_codes}"
            logger.error(msg)
            return False, msg