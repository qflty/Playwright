import pytest
import allure
from pathlib import Path
from utils.step_utils import StepExecutor

TEST_DATA_FILE = Path(__file__).parent / 'test_data' / 'test_data4.yaml'  # 路径需根据实际调整


@allure.feature("过滤配置管理")
class TestFilterConfig:
    @allure.story("创建过滤配置")
    @pytest.mark.filter_config
    def test_create_filter_config(self, controller, filter_config_creator, test_data):
        """测试创建过滤配置"""
        allure.dynamic.title(f"新建过滤配置 - {test_data['app_name']}")
        StepExecutor.execute_step('步骤1、登录devops', lambda: filter_config_creator.login_to_devops(), '登录devops异常', controller)
        StepExecutor.execute_step(f"步骤2、导航到代码扫描-{test_data['tab']}", lambda: filter_config_creator.navigate_to_scan_section(test_data), '导航到代码扫描异常', controller)
        StepExecutor.execute_step(f"步骤3、创建过滤配置", lambda: filter_config_creator.create_filter_config(test_data), '创建过滤配置异常', controller)
        StepExecutor.execute_step(f"步骤4、删除过滤配置", lambda: filter_config_creator.delete_filter_config(test_data), '删除过滤配置异常', controller)

    # @allure.story("验证过滤配置存在性")
    # @pytest.mark.parametrize("test_data",
    #                          lambda: read_yaml(str(TEST_DATA_FILE))['test_cases'],
    #                          ids=lambda tc: tc['app_name'])
    # def test_verify_filter_config_exists(self, controller, test_data):
    #     """验证创建的过滤配置是否存在"""
    #     allure.dynamic.title(f"验证过滤配置 - {test_data['app_name']}")
    #     filter_config_creator = FilterConfigCreator(controller)
    #
    #     with allure.step("登录系统并导航到配置页面"):
    #         filter_config_creator.login_to_devops()
    #         filter_config_creator.navigate_to_scan_section(test_data['tab'])
    #
    #     with allure.step(f"查询配置 {test_data['app_name']}"):
    #         filter_config_creator.filter_config_page.query_app(test_data['app_name'])
    #
    #     with allure.step("验证配置存在"):
    #         assert filter_config_creator.filter_config_page.is_config_exists(), \
    #             f"配置 {test_data['app_name']} 创建后未找到"
