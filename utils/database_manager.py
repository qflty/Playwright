from typing import Optional, List, Dict, Any, Union
from config.config import config
from utils.mysql_manager import MysqlManager
from utils.pgsql_manager import PgsqlManager


class DatabaseManager:
    """数据库管理器，提供统一的数据库访问接口"""
    def __init__(self):
        """初始化数据库管理器"""
        self._mysql_conn = None
        self._pgsql_conn = None

    def _get_mysql_connection(self) -> MysqlManager:
        """获取MySQL连接实例"""
        if not self._mysql_conn:
            host = config.mysql_test_host
            port = config.mysql_test_port
            user = config.mysql_test_user
            password = config.mysql_test_password
            database = config.mysql_test_database
            self._mysql_conn = MysqlManager(host, port, user, password, database)
        return self._mysql_conn

    def _get_pgsql_connection(self) -> PgsqlManager:
        """获取PostgreSQL连接实例"""
        if not self._pgsql_conn:
            host = config.pg_test_host
            port = config.pg_test_port
            user = config.pg_test_user
            password = config.pg_test_password
            database = config.pg_test_database
            self._pgsql_conn = PgsqlManager(host, port, user, password, database)
        return self._pgsql_conn

    def execute_mysql_query(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> List[Dict[str, Any]]:
        """
        执行MySQL查询，返回所有结果
        Args:
            sql: SQL查询语句
            params: SQL参数
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        try:
            mysql_conn = self._get_mysql_connection()
            return mysql_conn.execute_query(sql, params)
        except Exception as e:
            print(f"MySQL查询执行失败: {e}")
            return []

    def execute_mysql_query_one(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> Optional[
        Dict[str, Any]]:
        """
        执行MySQL查询，返回单条结果
        Args:
            sql: SQL查询语句
            params: SQL参数
        Returns:
            Optional[Dict[str, Any]]: 单条查询结果或None
        """
        try:
            mysql_conn = self._get_mysql_connection()
            return mysql_conn.execute_query_one(sql, params)
        except Exception as e:
            print(f"MySQL单条查询执行失败: {e}")
            return None

    def execute_mysql_update(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> int:
        """
        执行MySQL更新操作
        Args:
            sql: SQL更新语句
            params: SQL参数
        Returns:
            int: 受影响的行数
        """
        try:
            mysql_conn = self._get_mysql_connection()
            return mysql_conn.execute_update(sql, params)
        except Exception as e:
            print(f"MySQL更新操作执行失败: {e}")
            return 0

    def execute_pgsql_query(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> List[Dict[str, Any]]:
        """
        执行PostgreSQL查询，返回所有结果
        Args:
            sql: SQL查询语句
            params: SQL参数
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        """
        try:
            pgsql_conn = self._get_pgsql_connection()
            return pgsql_conn.execute_query(sql, params)
        except Exception as e:
            print(f"PostgreSQL查询执行失败: {e}")
            return []

    def execute_pgsql_query_one(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> Optional[
        Dict[str, Any]]:
        """
        执行PostgreSQL查询，返回单条结果
        Args:
            sql: SQL查询语句
            params: SQL参数
        Returns:
            Optional[Dict[str, Any]]: 单条查询结果或None
        """
        try:
            pgsql_conn = self._get_pgsql_connection()
            return pgsql_conn.execute_query_one(sql, params)
        except Exception as e:
            print(f"PostgreSQL单条查询执行失败: {e}")
            return None

    def execute_pgsql_update(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> int:
        """
        执行PostgreSQL更新操作
        Args:
            sql: SQL更新语句
            params: SQL参数
        Returns:
            int: 受影响的行数
        """
        try:
            pgsql_conn = self._get_pgsql_connection()
            return pgsql_conn.execute_update(sql, params)
        except Exception as e:
            print(f"PostgreSQL更新操作执行失败: {e}")
            return 0


# 全局数据库管理器实例
db_manager = DatabaseManager()

# 使用示例
# if __name__ == "__main__":
#     pgsql_results = db_manager.execute_pgsql_query_one(
#         "SELECT id FROM mars_case_library WHERE space_id = %s and is_deleted = %s ORDER BY gmt_created DESC LIMIT 1;",
#         ('8143', 'Y')
#     )
#     print(pgsql_results.get('id'))


