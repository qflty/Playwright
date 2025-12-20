from config.constants import CODE_SCAN_TASK_APP, FILTER_DESCRIPTION, FILTER_CONFIG_CREATE, \
    IMPORT_NUMBER_CONFIRM_BUTTON, CHOOSE_APP, STATIC_SCAN_TAB, UNIT_TEST_TAB, SAVE_FILETR, \
    UNIT_TEST_ADD, DELETE_FILETR, APPLICATION_CONFIG_EXIST, CODE_PLAN_CONFIRM_BUTTON, FILTER_PATH_BASE, \
    ADD_BUTTON
from utils.elements import FilterPathElement
from utils.logger import logger
from utils.xpath_builder import XPathBuilder

"""过滤配置"""


class FilterConfigPage:
    def __init__(self, controller):
        """
        初始化过滤配置页面对象
        :param controller: BrowserController实例
        """
        self.controller = controller

    def click_create_button(self):
        """点击新建按钮"""
        logger.info(f"开始创建过滤配置:")
        try:
            self.controller.click(FILTER_CONFIG_CREATE)
        except Exception as e:
            # 尝试使用JavaScript点击
            logger.warning(f"常规点击失败，尝试JavaScript点击: {e}")
            self.controller.execute_script(f"document.evaluate('{FILTER_CONFIG_CREATE.replace('xpath=', '')}', document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue.click()")
        # 验证点击后是否跳转到选择应用页面
        logger.info("等待选择应用页面加载...")
        if not self.controller.is_element_present(CODE_SCAN_TASK_APP):
            raise TimeoutError("选择应用页面加载超时")
        logger.info("选择应用页面已加载")

    def choose_app(self, app_name):
        """选择应用"""
        if not app_name:
            logger.warning("应用名称为空，跳过选择应用")
            return
        try:
            # 点击应用选择框
            self.controller.click(CODE_SCAN_TASK_APP)
            logger.info(f"已点击应用选择框，准备输入应用名称: {app_name}")
            # 输入应用名称
            self.controller.input_text(CODE_SCAN_TASK_APP, app_name)
            self.controller.sleep(1)  # 等待搜索结果加载
            # 使用XPathBuilder构建应用选项的XPath
            app_option_xpath = XPathBuilder.build_app_option_xpath(app_name)
            # 检查应用是否存在
            if not self.controller.is_element_present(app_option_xpath):
                error_msg = f"应用不存在: {app_name}"
                logger.error(error_msg)
                raise AssertionError(error_msg)
            # 点击选择应用
            self.controller.click(app_option_xpath)
            logger.info(f"已选择应用: {app_name}")
        except Exception as e:
            logger.error(f"选择应用失败: {app_name}, 错误信息: {str(e)}")
            raise AssertionError(f"选择应用失败: {app_name}") from e

    def input_description(self, description):
        """输入描述"""
        self.controller.input_text(FILTER_DESCRIPTION, description)
        logger.info(f"已输入描述: {description}")

    def click_confirm_button(self):
        """点击确定按钮"""
        self.controller.click(IMPORT_NUMBER_CONFIRM_BUTTON)
        logger.info("已点击确定按钮")

    def is_config_exists(self):
        """检查应用配置是否已存在"""
        return self.controller.is_element_present(APPLICATION_CONFIG_EXIST, timeout=5000)

    def query_filter(self, app_name):
        """查询应用过滤配置"""
        self.controller.click(CHOOSE_APP)
        self.controller.input_text(CHOOSE_APP, app_name)
        self.controller.sleep(1)  # 明确等待时间
        self.controller.click(XPathBuilder.build_choose_filter_xpath(app_name))
        logger.info("查询应用过滤配置")

    def choose_tab(self, tab_name):
        """选择tab页"""
        tab_mapping = {
            '静态扫描': STATIC_SCAN_TAB,
            '单元测试': UNIT_TEST_TAB
        }
        tab_xpath = tab_mapping.get(tab_name)
        if not tab_xpath:
            raise ValueError(f"不支持的tab名称: {tab_name}")
        self.controller.click(tab_xpath)
        self.controller.sleep(1)
        logger.info(f"已选择tab: {tab_name}")

    def add_filter_path(self, add_paths, tab_name):
        """添加过滤路径"""
        if not add_paths:
            logger.warning("当前没有可添加的过滤路径")
            return
        # 确定使用的添加按钮和输入框基础路径
        if tab_name == '静态扫描':
            add_button = ADD_BUTTON
        elif tab_name == '单元测试':
            add_button = UNIT_TEST_ADD
        else:
            raise ValueError(f"不支持的tab名称: {tab_name}")
        filter_path_element = FilterPathElement(self.controller)
        filter_path_element.add_filter_paths(add_paths, add_button, FILTER_PATH_BASE)

    def delete_filter_path(self, tab_name, add_paths, del_paths):
        """删除过滤路径"""
        if not del_paths:
            logger.warning("当前没有可删除的过滤路径")
            return
        if tab_name == '静态扫描':
            for del_path in del_paths:
                if del_path in add_paths:
                    index = add_paths.index(del_path) + 1  # XPath索引从1开始
                    delete_xpath = XPathBuilder.build_static_delete_filter_xpath(index)
                    self.controller.click(delete_xpath)
                    logger.info(f"已删除过滤路径: {del_path}")
        elif tab_name == '单元测试':
            for del_path in del_paths:
                if del_path in add_paths:
                    index = add_paths.index(del_path) + 1  # XPath索引从1开始
                    delete_xpath = XPathBuilder.build_unit_delete_filter_xpath(index)
                    self.controller.click(delete_xpath)
                    logger.info(f"已删除过滤路径: {del_path}")
        logger.info("过滤路径删除完成")

    def save_filter(self):
        """点击保存配置"""
        self.controller.click(SAVE_FILETR)
        logger.info("已点击保存配置")
        self.controller.sleep(1)

    def delete_filter(self):
        """删除配置"""
        self.controller.click(DELETE_FILETR)
        self.controller.click(CODE_PLAN_CONFIRM_BUTTON)
        self.controller.sleep(1)
