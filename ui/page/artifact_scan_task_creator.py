from ui.page.artifact_scan_task_page import ArtifactScanTaskPage
from ui.page.navigation_page import NavigationPage
from ui.page.login_page import LoginPage
from utils.logger import logger
from utils.utils import get_number


# 新建制品扫描任务
class ArtifactScanTaskCreator:
    def __init__(self, controller):
        self.controller = controller
        self.login_page = LoginPage(controller)
        self.navigation_page = NavigationPage(controller)
        self.artifact_scan_task_page = ArtifactScanTaskPage(controller)
        self.task_name = None

    def login_to_devops(self):
        """登录devops系统"""
        self.login_page.login()

    def navigate_to_scan_section(self, params):
        """导航到制品扫描区域"""
        self.navigation_page.artifact_change_directory()
        self.navigation_page.artifact_switch_tabs(params['tab'])

    def create_artifact_scan_task(self, params):
        """创建制品扫描任务"""
        self.artifact_scan_task_page.click_create_button()
        self.artifact_scan_task_page.choose_node(params['node'])
        self.artifact_scan_task_page.choose_plan(params['plan_name'])
        self.task_name = params['task_name'] + str(get_number(4))
        self.artifact_scan_task_page.input_task_name(self.task_name)
        self.artifact_scan_task_page.choose_artifact_type(params['artifact_type'])
        self.artifact_scan_task_page.choose_artifact_path(params['artifact_type'])
        self.artifact_scan_task_page.set_quality_gate(params['quality_gates'])
        self.artifact_scan_task_page.confirm_task(params['task_type'])
        return self.task_name

    def delete_artifact_scan_task(self, params):
        """删除制品扫描任务"""
        if params['is_del']:
            self.artifact_scan_task_page.query_task(self.task_name)
            self.artifact_scan_task_page.delete_task()
            logger.info(f"已删除扫描方案: {self.task_name}")
        else:
            logger.warning("不删除扫描任务")
