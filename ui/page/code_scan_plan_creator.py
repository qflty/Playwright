from ui.page.code_scan_plan_page import CodeScanPlanPage
from ui.page.login_page import LoginPage
from ui.page.navigation_page import NavigationPage
from utils.logger import logger
from utils.utils import get_number


# 新建代码扫描方案
class CodeScanPlanCreator:
    def __init__(self, controller):
        self.controller = controller
        self.login_page = LoginPage(controller)
        self.navigation_page = NavigationPage(controller)
        self.code_scan_plan_page = CodeScanPlanPage(controller)
        self.plan_name = None  # 添加实例变量存储方案名称

    def login_to_devops(self):
        """登录devops系统"""
        self.login_page.login()

    def navigate_to_scan_section(self, params):
        """导航到代码扫描区域"""
        self.navigation_page.code_change_directory()
        self.navigation_page.code_switch_tabs(params['tab'])

    def create_code_scan_plan(self, params):
        """创建扫描方案"""
        self.code_scan_plan_page.click_create_button()
        self.plan_name = params['plan_name'] + str(get_number(4))
        self.code_scan_plan_page.input_plan_name(self.plan_name)
        self.code_scan_plan_page.input_plan_description(params['description'])
        self.code_scan_plan_page.choose_language_and_rules(params['languages'])
        if params['is_default']:
            self.code_scan_plan_page.set_as_default()
        else:
            logger.info("不设为默认方案")
        self.code_scan_plan_page.confirm_plan()
        self.controller.sleep(1)
        return self.plan_name

    def add_filter_config(self, params):
        """添加过滤配置"""
        add_paths = params.get('add_paths', [])
        if add_paths:
            self.code_scan_plan_page.search_scan_plan(self.plan_name)
            self.code_scan_plan_page.add_plan_filter_path(params['add_paths'])
            self.code_scan_plan_page.save_config()
        else:
            logger.info("没有需要添加的过滤路径")

    def delete_filter_config(self, params):
        """删除过滤配置"""
        del_paths = params.get('del_paths', [])
        if del_paths:
            self.code_scan_plan_page.search_scan_plan(self.plan_name)
            self.code_scan_plan_page.delete_plan_filter_path(params['add_paths'], params['del_paths'])
            self.code_scan_plan_page.save_config()
        else:
            logger.info("没有要删除的过滤路径")

    def delete_code_scan_plan(self, params):
        """删除扫描方案"""
        if params['is_del']:
            self.code_scan_plan_page.search_scan_plan(self.plan_name)
            self.code_scan_plan_page.delete_plan()
            logger.info(f"已删除扫描方案: {self.plan_name}")
        else:
            logger.warning("不删除扫描方案")
