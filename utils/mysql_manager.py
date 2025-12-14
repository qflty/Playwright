import pymysql
from contextlib import contextmanager
from typing import Optional, List, Dict, Any


class MysqlManager:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """
        初始化数据库连接参数
        Args:
            host: 数据库主机地址
            port: 数据库端口
            user: 用户名
            password: 密码
            database: 数据库名
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database

    @contextmanager
    def get_connection(self):
        """
        数据库连接上下文管理器，确保连接正确关闭
        Yields:
            pymysql.Connection: 数据库连接对象
        """
        conn = None
        try:
            # 1. 进入上下文：建立数据库连接
            conn = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                cursorclass=pymysql.cursors.DictCursor,
                charset='utf8mb4'
            )
            yield conn  # 2. 返回连接给with语句使用
        except pymysql.Error as e:
            # 3. 退出上下文：异常处理
            if conn:
                conn.rollback()
            raise e
        finally:
            # 4. 退出上下文：确保连接关闭
            if conn:
                conn.close()

    @contextmanager
    def get_cursor(self):
        """
        数据库游标上下文管理器，确保游标和连接正确关闭
        Yields:
            pymysql.cursors.DictCursor: 数据库游标对象
        """
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                yield cursor
                conn.commit()
            except pymysql.Error as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

    def execute_query(self, sql: str, params: Optional[tuple] = None) -> List[Dict[str, Any]]:
        """
        执行查询SQL语句，返回所有结果
        Args:
            sql: SQL查询语句
            params: SQL参数元组，用于参数化查询
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        Raises:
            pymysql.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params)
                results = cursor.fetchall()
                print(f"总共查到{len(results)}条记录")
                return list(results)
        except pymysql.Error as e:
            print(f"数据库查询失败: {e}")
            raise

    def execute_query_one(self, sql: str, params: Optional[tuple] = None) -> Optional[Dict[str, Any]]:
        """
        执行查询SQL语句，返回单条结果
        Args:
            sql: SQL查询语句
            params: SQL参数元组，用于参数化查询
        Returns:
            Optional[Dict[str, Any]]: 单条查询结果或None
        Raises:
            pymysql.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        except pymysql.Error as e:
            print(f"数据库查询失败: {e}")
            raise

    def execute_update(self, sql: str, params: Optional[tuple] = None) -> int:
        """
        执行更新SQL语句（INSERT, UPDATE, DELETE）
        Args:
            sql: SQL更新语句
            params: SQL参数元组，用于参数化查询
        Returns:
            int: 受影响的行数
        Raises:
            pymysql.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                return affected_rows
        except pymysql.Error as e:
            print(f"数据库更新失败: {e}")
            raise

    def execute_many(self, sql: str, params_list: List[tuple]) -> int:
        """
        批量执行SQL语句
        Args:
            sql: SQL语句
            params_list: 参数元组列表
        Returns:
            int: 受影响的总行数
        Raises:
            pymysql.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                affected_rows = cursor.executemany(sql, params_list)
                return affected_rows
        except pymysql.Error as e:
            print(f"数据库批量操作失败: {e}")
            raise
