from config.constants import CODE_SCAN_PLAN_NAME, CODE_SCAN_PLAN_DESCRIPTION, \
    CODE_PLAN_STE_DEFAULT, CODE_PLAN_CONFIRM_BUTTON, CODE_SCAN_PLAN_SEARCH_ELE, CODE_SCAN_PLAN_FIRST, \
    CODE_SCAN_PLAN_FILTER_CONFIG_TAB, SAVE_FILETR, DELETE_SCAN_PLAN, CREATE_BUTTON, ADD_BUTTON, FILTER_PATH_BASE
from utils.elements import FilterPathElement, ConfigOperationElement
from utils.logger import logger
from utils.xpath_builder import XPathBuilder

"""代码扫描方案"""


class CodeScanPlanPage:
    def __init__(self, controller):
        self.controller = controller

    def click_create_button(self):
        """点击新建按钮"""
        logger.info(f"开始创建扫描方案:")
        self.controller.click(CREATE_BUTTON)

    def input_plan_name(self, name):
        """输入方案名称"""
        self.controller.input_text(CODE_SCAN_PLAN_NAME, name)
        logger.info(f"已输入方案名称: {name}")

    def input_plan_description(self, description):
        """输入方案描述"""
        self.controller.input_text(CODE_SCAN_PLAN_DESCRIPTION, description)
        logger.info(f"已输入方案描述: {description}")

    def choose_language_and_rules(self, languages):
        """选择扫描语言和规则集"""
        i = 1
        for language in languages:
            try:
                self.controller.click(f"//span[contains(text(),'{language}')]/../span/span")
                logger.info(f"已选择语言: {language}")
            except Exception as e:
                logger.error(f'选择语言异常: {str(e)}')
                raise
            try:
                self.controller.click(XPathBuilder.build_choose_language_xpath(language))
                self.controller.sleep()
                self.controller.click(XPathBuilder.build_choose_sonar_way_xpath(i))
                self.controller.click(XPathBuilder.build_choose_language_xpath(language))
                self.controller.sleep()
                logger.info(f"选择{language}语言规则集成功")
            except Exception as e:
                logger.error(f'选择{language}语言规则集异常: {str(e)}')
                raise
            i += 2  # 每次循环结束后增加 2

    def set_as_default(self):
        """设为默认"""
        try:
            self.controller.click(CODE_PLAN_STE_DEFAULT)
            logger.info(f"设为默认成功")
        except Exception as e:
            logger.error(f'设为默认异常: {str(e)}')
            raise

    def confirm_plan(self):
        """点击确定"""
        self.controller.click(CODE_PLAN_CONFIRM_BUTTON)
        logger.info(f"已点击确定按钮")

    def search_scan_plan(self, plan_name):
        """查询扫描方案"""
        self.controller.input_text(CODE_SCAN_PLAN_SEARCH_ELE, plan_name)
        self.controller.sleep(1)
        try:
            self.controller.click(CODE_SCAN_PLAN_FIRST)
            logger.info(f"已查询到扫描方案: {plan_name}")
        except Exception as e:
            logger.error(f"未查询到扫描方案: {str(e)}")
            raise

    def add_plan_filter_path(self, add_paths):
        """方案过滤配置添加路径"""
        if not add_paths:
            logger.warning("当前没有可添加的过滤路径")
            return
        self.controller.click(CODE_SCAN_PLAN_FILTER_CONFIG_TAB)
        logger.info(f"已点击过滤配置tab")
        self.controller.sleep(1)
        add_paths_element = FilterPathElement(self.controller)
        add_paths_element.add_filter_paths(add_paths, ADD_BUTTON, FILTER_PATH_BASE)

    def delete_plan_filter_path(self, add_paths, del_paths):
        """方案过滤配置删除路径"""
        if not add_paths:
            logger.warning("当前没有可删除的过滤路径")
            return
        if not del_paths:
            return
        for del_path in del_paths:
            if del_path in add_paths:
                index = add_paths.index(del_path) + 1  # XPath索引从1开始
                delete_xpath = XPathBuilder.build_delete_filter_xpath(index)
                try:
                    self.controller.sleep(1)
                    self.controller.click(delete_xpath)
                    logger.info(f"已删除过滤路径: {del_path}")
                except Exception as e:
                    logger.error(f"删除过滤路径异常: {del_path}, 错误信息: {e}")
                    raise
            else:
                logger.warning(f"未找到过滤路径: {del_path}")
        logger.info("过滤路径删除完成")

    def save_config(self):
        """点击保存配置"""
        config_filter_element = ConfigOperationElement(self.controller)
        config_filter_element.save_config(SAVE_FILETR)

    def delete_plan(self):
        """删除方案"""
        config_filter_element = ConfigOperationElement(self.controller)
        config_filter_element.delete_config(DELETE_SCAN_PLAN, CODE_PLAN_CONFIRM_BUTTON)
