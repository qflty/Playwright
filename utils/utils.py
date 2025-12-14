import json
import os
import random
import time
import yaml
from functools import wraps
from utils.logger import logger


# 自动重试失败的函数，直到达到最大重试次数或成功为止
def retry(tries: int = 3, delay: int = 1):
    """重试装饰器"""
    def decorator(func):
        @wraps(func)  # 使用 functools.wraps 保留原始函数的元信息
        def wrapper(*args, **kwargs):  # 包装函数，负责处理重试逻辑并调用原始函数
            attempt = 0
            while attempt < tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt == tries:
                        logger.error(f"所有重试失败: {e}")
                        raise
                    logger.warning(f"尝试 {attempt} 失败: {e}, {delay}秒后重试")
                    time.sleep(delay)
        return wrapper
    return decorator


def get_number(length: int) -> int:
    """生成指定长度的随机数"""
    return random.randint(10 ** (length - 1), 10 ** length - 1)


def read_yaml(yaml_path):
    """读取YAML文件"""
    try:
        # 检查文件是否存在
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML文件不存在: {yaml_path}")
        with open(yaml_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except yaml.YAMLError as e:
        logger.error(f"解析YAML文件失败: {e}")
        raise
    except Exception as e:
        logger.error(f"读取YAML文件异常: {e}")
        raise


def get_ids_from_json(json_data):
    """从JSON数据中提取所有的id"""
    try:
        # 解析JSON数据
        if isinstance(json_data, str):
            data_dict = json.loads(json_data)
        else:
            data_dict = json_data

        # 检查响应是否包含data.list
        if 'data' in data_dict and 'list' in data_dict['data']:
            items_list = data_dict['data']['list']

            # 从每个项目中提取id
            ids = []  # 初始化一个空列表
            for item in items_list:  # 遍历 items_list 中的每个元素
                if 'id' in item:  # 检查当前 item 是否有 'id' 键
                    ids.append(item['id'])  # 如果有，则提取 'id' 的值并添加到列表中
            return ids
        else:
            print("错误: JSON数据中不包含data.list结构")
            return []
    except json.JSONDecodeError:
        print("错误: JSON解析失败")
        return []
    except Exception as e:
        print(f"错误: 发生了未知错误: {e}")
        return []
