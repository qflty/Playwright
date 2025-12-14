import psycopg2
from psycopg2.extras import DictCursor
from contextlib import contextmanager
from typing import Optional, List, Dict, Any, Union


class PgsqlManager:
    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        """
        初始化PostgreSQL数据库连接参数
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
            psycopg2.connection: 数据库连接对象
        Raises:
            psycopg2.Error: 数据库连接或操作异常
        """
        conn = None
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            yield conn
        except psycopg2.Error as e:
            if conn:
                conn.rollback()
            raise e
        finally:
            if conn:
                conn.close()

    @contextmanager
    def get_cursor(self):
        """
        数据库游标上下文管理器，确保游标和连接正确关闭
        Yields:
            psycopg2.cursor: 数据库游标对象（DictCursor）
        """
        with self.get_connection() as conn:
            cursor = conn.cursor(cursor_factory=DictCursor)
            try:
                yield cursor
                conn.commit()
            except psycopg2.Error as e:
                conn.rollback()
                raise e
            finally:
                cursor.close()

    def execute_query(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> List[Dict[str, Any]]:
        """
        执行查询SQL语句，返回所有结果
        Args:
            sql: SQL查询语句
            params: SQL参数，可以是元组或字典形式
        Returns:
            List[Dict[str, Any]]: 查询结果列表
        Raises:
            psycopg2.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params)
                results = cursor.fetchall()
                print(f"总共查到{len(results)}条记录")
                return [dict(row) for row in results]
        except psycopg2.Error as e:
            print(f"数据库查询失败: {e}")
            raise

    def execute_query_one(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> Optional[Dict[str, Any]]:
        """
        执行查询SQL语句，返回单条结果
        Args:
            sql: SQL查询语句
            params: SQL参数，可以是元组或字典形式
        Returns:
            Optional[Dict[str, Any]]: 单条查询结果或None
        Raises:
            psycopg2.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params)
                result = cursor.fetchone()
                return dict(result) if result else None
        except psycopg2.Error as e:
            print(f"数据库查询失败: {e}")
            raise

    def execute_update(self, sql: str, params: Optional[Union[tuple, dict]] = None) -> int:
        """
        执行更新SQL语句（INSERT, UPDATE, DELETE）
        Args:
            sql: SQL更新语句
            params: SQL参数，可以是元组或字典形式
        Returns:
            int: 受影响的行数
        Raises:
            psycopg2.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.rowcount
        except psycopg2.Error as e:
            print(f"数据库更新失败: {e}")
            raise

    def execute_many(self, sql: str, params_list: List[Union[tuple, dict]]) -> int:
        """
        批量执行SQL语句
        Args:
            sql: SQL语句
            params_list: 参数列表，每个元素可以是元组或字典
        Returns:
            int: 受影响的总行数
        Raises:
            psycopg2.Error: 数据库操作异常
        """
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(sql, params_list)
                return cursor.rowcount
        except psycopg2.Error as e:
            print(f"数据库批量操作失败: {e}")
            raise
