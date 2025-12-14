import allure
import pytest
from pathlib import Path
from utils.step_utils import StepExecutor

TEST_DATA_FILE = Path(__file__).parent / 'test_data' / 'test_data3.yaml'


@allure.feature("单元测试任务管理")
class TestCaseUnitTestTask:
    @allure.story("单元测试")
    @pytest.mark.unit_test_task
    def test_case_unit_test_task(self, controller, unit_test_task_creator, test_data):
        """测试创建单元测试任务"""
        allure.dynamic.title(f"新建单元测试任务")
        StepExecutor.execute_step('步骤1、登录devops', lambda: unit_test_task_creator.login_to_devops(), '登录devops异常', controller)
        StepExecutor.execute_step(f"步骤2、导航到代码扫描 - {test_data['tab']}", lambda: unit_test_task_creator.navigate_to_scan_section(test_data), '导航到代码扫描页面异常', controller)
        StepExecutor.execute_step("步骤3、创建扫描任务", lambda: unit_test_task_creator.create_unit_test_task(test_data), '创建单元测试任务异常', controller)
        StepExecutor.execute_step("步骤4、删除扫描任务", lambda: unit_test_task_creator.delete_unit_test_task(test_data), '删除单元测试任务异常', controller)
