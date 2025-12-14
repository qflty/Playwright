from ui.page.artifact_scan_plan_page import ArtifactScanPlanPage
from ui.page.navigation_page import NavigationPage
from ui.page.login_page import LoginPage
from utils.logger import logger
from utils.utils import get_number


# 新建制品扫描方案
class ArtifactScanPlanCreator:
    def __init__(self, controller):
        self.controller = controller
        self.login_page = LoginPage(controller)
        self.navigation_page = NavigationPage(controller)
        self.artifact_scan_plan_page = ArtifactScanPlanPage(controller)
        self.plan_name = None

    def login_to_devops(self):
        """登录devops系统"""
        self.login_page.login()

    def navigate_to_scan_section(self, params):
        """导航到制品扫描区域"""
        self.navigation_page.artifact_change_directory()
        self.navigation_page.artifact_switch_tabs(params['tab'])

    def create_artifact_scan_plan(self, params):
        """创建扫描方案"""
        self.artifact_scan_plan_page.click_create_button()
        self.plan_name = params['plan_name'] + str(get_number(4))
        self.artifact_scan_plan_page.input_plan_name(self.plan_name)
        if params['is_default']:
            self.artifact_scan_plan_page.set_as_default()
        else:
            logger.info("不设为默认方案")
        self.artifact_scan_plan_page.input_plan_description(params['description'])
        self.artifact_scan_plan_page.add_vuln_ids(params['vuln_ids'], params['is_import'])
        self.artifact_scan_plan_page.confirm_plan()
        return self.plan_name

    def delete_artifact_scan_plan(self, params):
        """删除扫描方案"""
        if params['is_del']:
            self.artifact_scan_plan_page.query_plan(self.plan_name)
            self.artifact_scan_plan_page.delete_plan()
            logger.info(f"已删除扫描方案: {self.plan_name}")
        else:
            logger.warning("不删除扫描方案")
