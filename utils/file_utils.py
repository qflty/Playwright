import os
import shutil
from utils.logger import logger


class FileUtils:
    """文件处理工具类"""

    @staticmethod
    def ensure_dir_exists(dir_path):
        """确保目录存在，如果不存在则创建"""
        try:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
                logger.info(f"创建目录: {dir_path}")
            return True
        except Exception as e:
            logger.error(f"创建目录失败 {dir_path}: {str(e)}")
            return False

    @staticmethod
    def get_file_extension(filename):
        """获取文件扩展名"""
        return os.path.splitext(filename)[1].lower()

    @staticmethod
    def get_file_name_without_extension(filename):
        """获取不带扩展名的文件名"""
        return os.path.splitext(filename)[0]

    @staticmethod
    def copy_file(src, dst):
        """复制文件"""
        try:
            shutil.copy2(src, dst)
            logger.info(f"复制文件: {src} -> {dst}")
            return True
        except Exception as e:
            logger.error(f"复制文件失败 {src} -> {dst}: {str(e)}")
            return False

    @staticmethod
    def delete_file(file_path):
        """删除文件"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"删除文件: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"删除文件失败 {file_path}: {str(e)}")
            return False
