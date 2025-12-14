import time
from datetime import datetime
from api.core.request_handler import RequestHandler
from api.core.response_handler import ResponseHandler
from api.core.validator import Validator
from config.config import config
from utils.excel_utils import ExcelUtils
from utils.logger import logger


class TestRunner:
    """测试用例执行器"""

    def __init__(self, excel_path):
        self.excel_path = excel_path
        self.request_handler = RequestHandler()
        self.variables = {}  # 存储提取的变量
        self.results = []  # 存储测试结果
        self.dependent_cases = set()  # 存储依赖用例ID

        # 加载Excel数据
        self.config = {}
        self.interfaces = {}
        self.testcases = []
        self.load_test_data()

    def load_test_data(self):
        """加载Excel中的测试数据"""
        logger.info(f"从 {self.excel_path} 加载测试数据")

        # 加载配置信息
        self.config = ExcelUtils.read_config_sheet(self.excel_path)
        logger.debug(f"加载配置信息: {self.config}")

        # 加载接口信息
        self.interfaces = ExcelUtils.read_interfaces_sheet(self.excel_path)
        logger.info(f"加载接口信息: {len(self.interfaces)} 个接口")

        # 加载测试用例
        self.testcases = ExcelUtils.read_testcases_sheet(self.excel_path)
        # 识别依赖用例
        for case in self.testcases:
            if case.get('依赖用例ID'):
                self.dependent_cases.add(case['依赖用例ID'])
        logger.info(f"加载测试用例: {len(self.testcases)} 个用例, 依赖用例: {len(self.dependent_cases)} 个")

    def replace_variables(self, data):
        """替换数据中的变量 ${variable_name}"""
        if not data:
            return data

        try:
            # 处理字典类型
            if isinstance(data, dict):
                data_str = str(data)
            # 处理字符串类型
            elif isinstance(data, str):
                data_str = data
            # 其他类型转为字符串
            else:
                data_str = str(data)

            # 替换变量
            for key, value in self.variables.items():
                var_pattern = f"${{{key}}}"
                if var_pattern in data_str:
                    data_str = data_str.replace(var_pattern, str(value))

            # 尝试解析回字典
            if isinstance(data, dict):
                return eval(data_str)
            return data_str
        except Exception as e:
            logger.warning(f"变量替换失败: {str(e)}, 原始数据: {data}")
            return data

    def run_dependent_case(self, dependent_id):
        """运行依赖的测试用例"""
        # 检查依赖用例是否已经执行过并成功
        for result in self.results:
            if result['用例ID'] == dependent_id:
                logger.info(f"依赖用例 {dependent_id} 已执行完成，结果: {result['测试结果']}")
                return result['测试结果'] == '通过'

        # 如果没有执行过，则执行依赖用例
        for case in self.testcases:
            if case['用例ID'] == dependent_id:
                logger.info(f"执行依赖用例: {dependent_id}")
                result = self.run_testcase(case)
                return result['测试结果'] == '通过'
        logger.warning(f"未找到依赖用例: {dependent_id}")
        return False

    def run_testcase(self, case):
        """执行单个测试用例"""
        result = {
            '用例ID': case['用例ID'],
            '用例名称': case['用例名称'],
            '接口ID': case['接口ID'],
            '开始时间': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            '结束时间': '',
            '响应时间(ms)': 0,
            '状态码': 0,
            '测试结果': '失败',
            '错误信息': '',
            '断言结果': '',
            '是否依赖用例': case['用例ID'] in self.dependent_cases  # 添加标识字段
        }

        try:
            # 处理依赖用例
            if case.get('依赖用例ID'):
                if not self.run_dependent_case(case['依赖用例ID']):
                    result['错误信息'] = f"依赖用例 {case['依赖用例ID']} 执行失败"
                    self.results.append(result)
                    return result

            # 获取接口信息
            interface = self.interfaces.get(case['接口ID'])
            if not interface:
                result['错误信息'] = f"未找到接口 {case['接口ID']}"
                self.results.append(result)
                return result

            # 准备请求数据
            # 优先使用Excel config工作表中的base_url，否则使用配置中的base_url
            base_url = self.config.get('base_url', '') or config.api.base_url
            interface_url = interface['url']
            # 对接口URL进行变量替换，支持URL中使用变量
            interface_url = self.replace_variables(interface_url)
            # 处理URL拼接，确保格式正确
            if base_url and interface_url:
                # 确保base_url末尾没有多余的斜杠
                base_url = base_url.rstrip('/')
                # 确保interface_url开头有斜杠（除非是完整URL）
                if not interface_url.startswith(('http://', 'https://')):
                    interface_url = '/' + interface_url.lstrip('/')
                url = base_url + interface_url
            else:
                # 如果没有base_url，则直接使用interface_url
                url = interface_url

            # 处理请求参数
            params = case.get('请求参数') or {}
            params = self.replace_variables(params)

            # 处理请求头
            headers = interface.get('headers', {}).copy()
            if case.get('请求头'):
                case_headers = case['请求头']
                headers.update(self.replace_variables(case_headers))

            # 发送请求
            logger.info(f"执行用例 [{case['用例ID']}] {case['用例名称']}")
            start_time = time.time()
            response = self.request_handler.send_request(
                method=interface['method'],
                url=url,
                json=params if interface.get('content_type') == 'application/json' else None,
                data=params if interface.get('content_type') != 'application/json' else None,
                headers=headers
            )

            # 记录响应时间和状态码
            response_time = int((time.time() - start_time) * 1000)
            result['响应时间(ms)'] = response_time
            result['状态码'] = response.status_code

            # 解析响应
            response_data = ResponseHandler.parse_response(response)

            # 提取变量
            extract_vars = case.get('提取变量') or {}
            extracted_vars = ResponseHandler.extract_variables(response_data, extract_vars)
            self.variables.update(extracted_vars)

            # 断言
            # 1. 状态码断言
            status_assert_success, status_assert_msg = Validator.assert_status_code(
                response.status_code,
                [200, 201, 204]  # 默认预期状态码
            )

            # 2. 响应内容断言
            content_assert_success, content_assert_msg = True, "无内容断言"
            assert_rules = case.get('断言规则') or {}
            if assert_rules:
                content_assert_success, content_assert_msg = Validator.assert_response(
                    response_data,
                    assert_rules
                )

            result['断言结果'] = f"{status_assert_msg}; {content_assert_msg}"

            # 判断测试结果
            if status_assert_success and content_assert_success:
                result['测试结果'] = '通过'
            else:
                result['测试结果'] = '失败'
                result['错误信息'] = f"断言失败: {result['断言结果']}"

        except Exception as e:
            result['错误信息'] = f"执行异常: {str(e)}"

        # 记录结束时间
        result['结束时间'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.results.append(result)
        logger.info(f"用例 [{case['用例ID']}] 执行结果: {result['测试结果']} (耗时: {result['响应时间(ms)']}ms)")
        return result

    def run_all_tests(self, module=None):
        """执行所有测试用例"""
        logger.info("开始执行所有测试用例...")
        start_time = time.time()

        # 过滤需要执行的用例
        cases_to_run = []
        for case in self.testcases:
            # 检查是否运行标记
            if case.get('是否运行', '').lower() != 'yes':
                continue
            # 检查模块过滤
            if module and case.get('模块') != module:
                continue
            # 跳过依赖用例（它们会在需要时被执行）
            if case['用例ID'] in self.dependent_cases:
                logger.debug(f"跳过依赖用例: {case['用例ID']}")
                continue
            cases_to_run.append(case)
        logger.info(f"筛选出 {len(cases_to_run)} 个主用例，{len(self.dependent_cases)} 个依赖用例")

        # 执行用例
        for case in cases_to_run:
            self.run_testcase(case)

        # 计算统计信息
        total_time = int((time.time() - start_time) * 1000)
        total = len(self.results)
        passed = sum(1 for r in self.results if r['测试结果'] == '通过')
        failed = total - passed

        logger.info("=" * 50)
        logger.info("测试执行完毕!")
        logger.info(f"总用例数: {total}")
        logger.info(f"通过用例: {passed}")
        logger.info(f"失败用例: {failed}")
        logger.info(f"总耗时: {total_time}ms")
        logger.info("=" * 50)

        # 保存结果到Excel
        ExcelUtils.save_test_results(self.excel_path, self.results)

        # 生成报告
        from api.core.report_generator import ReportGenerator
        report_generator = ReportGenerator()
        report_path = report_generator.generate_html_report(
            self.results,
            total, passed, failed, total_time
        )

        return {
            'total': total,
            'passed': passed,
            'failed': failed,
            'total_time': total_time,
            'report_path': report_path
        }

    def close(self):
        """关闭资源"""
        self.request_handler.close_session()