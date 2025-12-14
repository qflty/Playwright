from ui.page.login_page import LoginPage
from ui.page.navigation_page import NavigationPage
from ui.page.unit_test_task_page import UnitTestTaskPage
from utils.logger import logger
from utils.utils import get_number


# 新建单元测试任务
class UnitTestTaskCreator:
    def __init__(self, controller):
        self.controller = controller
        self.login_page = LoginPage(controller)
        self.navigation_page = NavigationPage(controller)
        self.unit_test_page = UnitTestTaskPage(controller)
        self.task_name = None

    def login_to_devops(self):
        """登录devops系统"""
        self.login_page.login()

    def navigate_to_scan_section(self, params):
        """导航到代码扫描区域"""
        self.navigation_page.code_change_directory()
        self.navigation_page.code_switch_tabs(params['tab'])

    def create_unit_test_task(self, params):
        """创建单元测试任务"""
        self.unit_test_page.click_create_button()
        self.task_name = params['task_name'] + str(get_number(4))
        self.unit_test_page.input_task_name(self.task_name)
        self.unit_test_page.choose_app(params["app_name"])
        self.unit_test_page.choose_branch(params["branch_name"])
        self.unit_test_page.choose_scan_mode(params["scan_mode"])
        self.unit_test_page.confirm_task(params["task_type"])

    def delete_unit_test_task(self, params):
        """删除单元测试任务"""
        if params['is_del']:
            self.unit_test_page.query_task(self.task_name)
            self.unit_test_page.delete_task()
            logger.info(f"已删除扫描任务: {self.task_name}")
        else:
            logger.warning("不删除扫描任务")

