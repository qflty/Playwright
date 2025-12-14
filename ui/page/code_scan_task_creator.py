from ui.page.code_scan_task_page import CodeScanTaskPage
from ui.page.login_page import LoginPage
from ui.page.navigation_page import NavigationPage
from utils.logger import logger
from utils.utils import get_number


# 新建代码扫描任务
class CodeScanTaskCreator:
    def __init__(self, controller):
        self.controller = controller
        self.login_page = LoginPage(controller)
        self.navigation_page = NavigationPage(controller)
        self.code_scan_task_page = CodeScanTaskPage(controller)
        self.task_name = None  # 添加实例变量存储方案名称

    def login_to_devops(self):
        """登录devops系统"""
        self.login_page.login()

    def navigate_to_scan_section(self, params):
        """导航到代码扫描区域"""
        self.navigation_page.code_change_directory()
        self.navigation_page.code_switch_tabs(params['tab'])

    def create_code_scan_task(self, params):
        """创建代码扫描任务"""
        self.code_scan_task_page.click_create_button()
        self.code_scan_task_page.choose_plan(params["plan_name"])
        self.task_name = params['task_name'] + str(get_number(4))
        self.code_scan_task_page.input_task_name(self.task_name)
        self.code_scan_task_page.choose_app(params["app_name"])
        self.code_scan_task_page.choose_branch(params["branch_name"])
        self.code_scan_task_page.choose_scan_mode(params["scan_mode"])
        self.code_scan_task_page.set_quality_gate(params["quality_gates"])
        self.code_scan_task_page.add_filter_path(params["add_paths"])
        if params["generate_pdf"]:
            self.code_scan_task_page.choose_generate_pdf()
        self.code_scan_task_page.confirm_task(params["task_type"])

    def delete_code_scan_task(self, params):
        """删除代码扫描任务"""
        if params["is_del"]:
            self.code_scan_task_page.query_task(self.task_name)
            self.code_scan_task_page.delete_task()
            logger.info(f"已删除扫描任务: {self.task_name}")
        else:
            logger.warning("不删除扫描任务")
