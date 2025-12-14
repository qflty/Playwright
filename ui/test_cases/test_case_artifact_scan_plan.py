import allure
import pytest
from pathlib import Path
from utils.step_utils import StepExecutor

TEST_DATA_FILE = Path(__file__).parent / 'test_data' / 'test_data5.yaml'


@allure.feature("制品扫描方案管理")
class TestCaseArtifactScanPlan:
    @allure.story("扫描方案")
    @pytest.mark.artifact_scan_plan
    def test_case_artifact_scan_plan(self, controller, artifact_scan_plan_creator, test_data):
        """测试创建扫描方案"""
        allure.dynamic.title(f"新建扫描方案")
        StepExecutor.execute_step('步骤1、登录devops', lambda: artifact_scan_plan_creator.login_to_devops(),'登录devops异常', controller)
        StepExecutor.execute_step(f"步骤2、导航到制品扫描 - {test_data['tab']}", lambda: artifact_scan_plan_creator.navigate_to_scan_section(test_data), '导航到代码扫描页面异常', controller)
        StepExecutor.execute_step("步骤3、创建扫描方案", lambda: artifact_scan_plan_creator.create_artifact_scan_plan(test_data), '创建扫描方案异常', controller)
        StepExecutor.execute_step("步骤4、删除扫描方案", lambda: artifact_scan_plan_creator.delete_artifact_scan_plan(test_data), '删除扫描方案异常', controller)
