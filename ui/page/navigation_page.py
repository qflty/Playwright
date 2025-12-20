from config.constants import CODE_MANAGEMENT_BUTTON, CODE_SCANNER_BUTTON, CODE_SACN_PLAN, \
    CODE_SACN_TASK, CODE_SACN_UNIT, FIlTER_CONFIGURATION, ARTIFACT_SCANNER_BUTTON, ARTIFACT_MANAGEMENT_BUTTON, \
    PLAN_BUTTON, TASK_BUTTON
from utils.logger import logger


class NavigationPage:
    def __init__(self, controller):
        """
        初始化导航页面对象
        :param controller: BrowserController实例
        """
        self.controller = controller

    def code_change_directory(self):
        """进入代码扫描"""
        try:
            self.controller.click(CODE_MANAGEMENT_BUTTON)
            self.controller.sleep(1)
            logger.info("已点击代码按钮")
        except Exception as e:
            logger.error(f"点击代码异常: {e}")
            raise AssertionError("点击代码失败") from e
        try:
            self.controller.click(CODE_SCANNER_BUTTON)
            self.controller.sleep(1)
            logger.info("已点击代码扫描按钮")
        except Exception as e:
            logger.error(f"点击代码扫描异常: {e}")
            raise AssertionError("点击代码扫描失败") from e

    def code_switch_tabs(self, tab):
        """代码扫描选择目录"""
        tab_mapping = {
            '扫描方案': CODE_SACN_PLAN,
            '扫描任务': CODE_SACN_TASK,
            '单元测试': CODE_SACN_UNIT,
            '过滤配置': FIlTER_CONFIGURATION
        }
        tab_locator = tab_mapping.get(tab)
        if not tab_locator:
            error_msg = f"不支持的tab名称: {tab}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        try:
            self.controller.click(tab_locator)
            self.controller.sleep(1)
            logger.info(f"已切换到tab: {tab}")
        except Exception as e:
            logger.error(f"点击代码扫描下目录异常: {e}")
            raise AssertionError(f"点击代码扫描下目录失败: {tab}") from e

    def artifact_change_directory(self):
        """进入制品扫描"""
        try:
            self.controller.click(ARTIFACT_MANAGEMENT_BUTTON)
            self.controller.sleep(1)
            logger.info("已点击制品按钮")
        except Exception as e:
            logger.error(f"点击制品异常: {e}")
            raise AssertionError("点击制品失败") from e
        try:
            self.controller.click(ARTIFACT_SCANNER_BUTTON)
            self.controller.sleep(1)
            logger.info("已点击制品扫描按钮")
        except Exception as e:
            logger.error(f"点击制品扫描异常: {e}")
            raise AssertionError("点击制品扫描失败") from e

    def artifact_switch_tabs(self, tab):
        """制品扫描选择目录"""
        tab_mapping = {
            '扫描方案': PLAN_BUTTON,
            '扫描任务': TASK_BUTTON,
        }
        tab_locator = tab_mapping.get(tab)
        if not tab_locator:
            error_msg = f"不支持的tab名称: {tab}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        try:
            self.controller.click(tab_locator)
            self.controller.sleep(1)
            logger.info(f"已切换到tab: {tab}")
        except Exception as e:
            logger.error(f"点击制品扫描下目录异常: {e}")
            raise AssertionError(f"点击制品扫描下目录失败: {tab}") from e
