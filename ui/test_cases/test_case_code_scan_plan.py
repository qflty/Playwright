import allure
import pytest
from pathlib import Path
from utils.step_utils import StepExecutor

TEST_DATA_FILE = Path(__file__).parent / 'test_data' / 'test_data1.yaml'


@allure.feature("代码扫描方案管理")
class TestCodeScanPlan:
    @allure.story("扫描方案")
    @pytest.mark.code_scan_plan
    def test_case_code_scan_plan(self, controller, code_scan_plan_creator, test_data):
        """测试创建扫描方案"""
        allure.dynamic.title(f"新建扫描方案")
        StepExecutor.execute_step('步骤1、登录devops', lambda: code_scan_plan_creator.login_to_devops(), '登录devops异常', controller)
        StepExecutor.execute_step(f"步骤2、导航到代码扫描 - {test_data['tab']}", lambda: code_scan_plan_creator.navigate_to_scan_section(test_data), '导航到代码扫描页面异常', controller)
        StepExecutor.execute_step("步骤3、创建扫描方案", lambda: code_scan_plan_creator.create_code_scan_plan(test_data), '创建扫描方案异常', controller)
        StepExecutor.execute_step("步骤4、添加过滤路径", lambda: code_scan_plan_creator.add_filter_config(test_data), '添加过滤路径异常', controller)
        StepExecutor.execute_step("步骤5、删除过滤路径", lambda: code_scan_plan_creator.delete_filter_config(test_data), '删除过滤路径异常', controller)
        StepExecutor.execute_step("步骤6、删除扫描方案", lambda: code_scan_plan_creator.delete_code_scan_plan(test_data), '删除扫描方案异常', controller)
