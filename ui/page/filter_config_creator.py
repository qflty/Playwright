from ui.page.filter_config_page import FilterConfigPage
from ui.page.login_page import LoginPage
from ui.page.navigation_page import NavigationPage
from utils.logger import logger


# 新建过滤配置
class FilterConfigCreator:
    def __init__(self, controller):
        """初始化过滤配置创建器"""
        self.controller = controller
        self.login_page = LoginPage(controller)
        self.navigation_page = NavigationPage(controller)
        self.filter_config_page = FilterConfigPage(controller)

    def login_to_devops(self):
        """登录devops系统"""
        self.login_page.login()

    def navigate_to_scan_section(self, params):
        """导航到代码扫描区域"""
        self.navigation_page.code_change_directory()
        self.navigation_page.code_switch_tabs(params['tab'])

    def create_filter_config(self, params):
        """创建过滤配置"""
        self.filter_config_page.click_create_button()
        self.filter_config_page.choose_app(params['app_name'])
        self.filter_config_page.input_description(params['description'])
        self.filter_config_page.click_confirm_button()

        # 检查配置状态
        config_exists = self.filter_config_page.is_config_exists()
        if config_exists:
            error_msg = f"应用配置已存在: {params['app_name']}"
            logger.warning(error_msg)
            raise AssertionError(error_msg)

        self.filter_config_page.query_filter(params['app_name'])
        self.filter_config_page.choose_tab(params['tab_name'])
        self.filter_config_page.add_filter_path(params['add_paths'], params['tab_name'])
        self.filter_config_page.delete_filter_path(params['tab_name'], params['add_paths'], params['del_paths'])
        self.filter_config_page.save_filter()

    def delete_filter_config(self, params):
        """删除过滤配置"""
        if params['is_del']:
            self.filter_config_page.delete_filter()
            logger.info(f"已删除过滤配置: {params['app_name']}")
        else:
            logger.warning(f"不删除过滤配置")
