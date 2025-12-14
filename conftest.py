import pytest
from ui.page.artifact_scan_plan_creator import ArtifactScanPlanCreator
from ui.page.artifact_scan_task_creator import ArtifactScanTaskCreator
from ui.page.code_scan_plan_creator import CodeScanPlanCreator
from ui.page.code_scan_task_creator import CodeScanTaskCreator
from ui.page.unit_test_task_creator import UnitTestTaskCreator
from ui.page.filter_config_creator import FilterConfigCreator
from utils.sync_playwright_browser_controller import BrowserController
from utils.utils import read_yaml
from utils.logger import logger
from config.config import config


@pytest.fixture(scope='function')
def controller():
    """创建并管理BrowserController实例（浏览器控制器）"""
    c = BrowserController(config.ui.browser_type, headless=config.ui.headless, timeout=config.ui.default_timeout)
    try:
        yield c
    finally:
        c.close()


@pytest.fixture(scope='function')
def code_scan_plan_creator(controller):
    """创建代码扫描方案操作器实例（封装页面对象）"""
    return CodeScanPlanCreator(controller)


@pytest.fixture(scope='function')
def code_scan_task_creator(controller):
    """创建代码扫描任务操作器实例（封装页面对象）"""
    return CodeScanTaskCreator(controller)


@pytest.fixture(scope='function')
def unit_test_task_creator(controller):
    """创建单元测试任务操作器实例（封装页面对象）"""
    return UnitTestTaskCreator(controller)


@pytest.fixture(scope='function')
def filter_config_creator(controller):
    """创建过滤配置操作器实例（封装页面对象）"""
    return FilterConfigCreator(controller)


@pytest.fixture(scope='function')
def artifact_scan_plan_creator(controller):
    """创建制品扫描方案操作器实例（封装页面对象）"""
    return ArtifactScanPlanCreator(controller)


@pytest.fixture(scope='function')
def artifact_scan_task_creator(controller):
    """创建制品扫描任务操作器实例（封装页面对象）"""
    return ArtifactScanTaskCreator(controller)


@pytest.fixture(scope='module')
def test_data_list(request):
    """根据当前测试文件，动态获取对应的测试数据列表"""
    # 获取当前测试用例所在的模块（即测试文件）
    test_module = request.module
    # 从测试模块中获取其定义的 TEST_DATA_FILE
    if not hasattr(test_module, 'TEST_DATA_FILE'):
        raise AttributeError(f"测试文件 {test_module.__file__} 中未定义 TEST_DATA_FILE 变量")

    test_data_file = test_module.TEST_DATA_FILE
    logger.info(f"测试数据文件路径: {test_data_file}")
    logger.info(f"文件是否存在: {test_data_file.exists()}")
    if not test_data_file.exists():
        raise FileNotFoundError(f"测试数据文件不存在: {test_data_file}")
    test_data = read_yaml(str(test_data_file))
    return test_data['test_cases']


def pytest_generate_tests(metafunc):
    """动态生成测试用例参数（根据当前测试文件获取对应数据）"""
    if 'test_data' in metafunc.fixturenames:
        try:
            # 获取当前测试模块（测试文件）
            test_module = metafunc.module
            # 从测试模块中获取其定义的 TEST_DATA_FILE
            if not hasattr(test_module, 'TEST_DATA_FILE'):
                raise AttributeError(f"测试文件 {test_module.__file__} 中未定义 TEST_DATA_FILE 变量")

            test_data_file = test_module.TEST_DATA_FILE
            test_data = read_yaml(str(test_data_file))
            test_cases = test_data['test_cases']
            metafunc.parametrize(
                "test_data",
                test_cases
                # ids=[tc['app_name'] for tc in test_cases]
            )
        except Exception as e:
            logger.error(f"读取测试数据时出错: {e}")
            metafunc.parametrize("test_data", [])  # 出错时传入空列表，避免测试崩溃
