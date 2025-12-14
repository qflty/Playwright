import logging
from logging.handlers import RotatingFileHandler
from config.config import config


def setup_logger(name: str = __name__) -> logging.Logger:
    """配置并返回logger实例"""
    # 创建未配置的logger实例
    logger = logging.getLogger(name)
    # 创建日志记录器
    logger.setLevel(getattr(logging, config.log.log_level))
    # 避免重复添加处理器
    if not logger.handlers:
        # 创建格式化器
        formatter = logging.Formatter(
            "%(asctime)s | %(name)-30s | %(levelname)-8s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(formatter)
        # 创建文件处理器
        file_handler = RotatingFileHandler(
            config.log.log_file,
            maxBytes=config.log.log_max_size,
            backupCount=config.log.log_backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        # 添加处理器
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    return logger


def format_log_message(action, target, details=None):
    """
    格式化日志消息，实现统一的日志格式
    :param action: 操作类型 (CLICK, INPUT, SELECT, SKIP等)
    :param target: 操作目标 (元素名称、对象等)
    :param details: 详细信息 (可选)
    :return: 格式化后的日志消息
    """
    if details:
        return f"[{action}] {target} - {details}"
    return f"[{action}] {target}"


def log_execution_time(operation_name):
    """
    装饰器：记录函数执行时间
    :param operation_name: 操作名称
    """
    def decorator(func):
        import functools
        import time
        
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            logger.info(f"开始执行: {operation_name}")
            try:
                result = func(*args, **kwargs)
                execution_time = time.time() - start_time
                logger.info(f"完成执行: {operation_name} (耗时: {execution_time:.2f}s)")
                return result
            except Exception as e:
                execution_time = time.time() - start_time
                logger.error(f"执行失败: {operation_name} (耗时: {execution_time:.2f}s) - 错误: {str(e)}")
                raise
        return wrapper
    return decorator


# 立即创建并配置logger实例
logger = setup_logger(__name__)
logger.info("日志初始化完成")