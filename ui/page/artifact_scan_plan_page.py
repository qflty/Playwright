from config.contants import CREATE_BUTTON, PLAN_NAME_LOCATER, STE_DEFAULT, PLAN_DESCRIPTION_INPUT, ADD_BUTTON, \
    IMPORT_NUMBER_FILE_lOCATER, VULNERABILITY_NUMBER_FILE, PLAN_CONFIRM_BUTTON, SCAN_PLAN_SEARCH_ELE, \
    DELETE_SCANNER_PLAN, INPORT_NUMBER_BUTTON, IMPORT_NUMBER_CONFIRM_BUTTON, DELETE_CONFIRM_BUTTON, SCAN_CLICK_SEARCH
from utils.logger import logger
from utils.xpath_builder import XPathBuilder

"""制品扫描方案"""


class ArtifactScanPlanPage:
    def __init__(self, controller):
        self.controller = controller

    def click_create_button(self):
        """点击新建按钮"""
        logger.info(f"开始创建扫描任务:")
        self.controller.click(CREATE_BUTTON)

    def input_plan_name(self, name):
        """输入扫描方案名称"""
        logger.info(f"输入扫描方案名称: {name}")
        self.controller.input_text(PLAN_NAME_LOCATER, name)

    def set_as_default(self):
        """设为默认"""
        try:
            self.controller.click(STE_DEFAULT)
            logger.info(f"设为默认成功")
        except Exception as e:
            logger.error(f'设为默认异常: {str(e)}')
            raise

    def input_plan_description(self, description):
        """输入扫描方案描述"""
        logger.info(f"输入扫描方案描述: {description}")
        self.controller.input_text(PLAN_DESCRIPTION_INPUT, description)

    def add_vuln_ids(self, add_vuln_ids, is_import=False):
        """添加漏洞编号"""
        if not add_vuln_ids:
            logger.info(f"当前没有可添加的漏洞编号")
            return
        try:
            for index, add_vuln_id in enumerate(add_vuln_ids, start=1):
                self.controller.click(ADD_BUTTON)
                input_xpath = XPathBuilder.build_vuln_id_xpath(index)
                self.controller.input_text(input_xpath, add_vuln_id)
                logger.info(f"添加漏洞编号: {add_vuln_id}")
            logger.info(f"已添加{len(add_vuln_ids)}个漏洞编号")
            # 处理导入文件逻辑
            if is_import:
                self.controller.click(INPORT_NUMBER_BUTTON)
                self.controller.sleep(1)
                self.controller.upload_file(IMPORT_NUMBER_FILE_lOCATER, VULNERABILITY_NUMBER_FILE)
                self.controller.click(IMPORT_NUMBER_CONFIRM_BUTTON)
                logger.info("已导入漏洞编号")
        except Exception as e:
            logger.error(f"添加漏洞编号时发生异常: {str(e)}")
            raise

    def confirm_plan(self):
        """确认创建扫描方案"""
        try:
            self.controller.click(PLAN_CONFIRM_BUTTON)
            logger.info(f"已点击确认创建扫描方案")
        except Exception as e:
            logger.error(f"点击确认创建扫描方案异常: {str(e)}")
            raise

    def query_plan(self, plan_name):
        """查询扫描方案"""
        try:
            self.controller.input_text(SCAN_PLAN_SEARCH_ELE, plan_name)
            self.controller.click(SCAN_CLICK_SEARCH)
            logger.info(f"已输入查询条件: {plan_name}")
        except Exception as e:
            logger.error(f"输入查询条件异常: {str(e)}")
            raise

    def delete_plan(self):
        """删除扫描方案"""
        try:
            self.controller.click(DELETE_SCANNER_PLAN)
            self.controller.click(DELETE_CONFIRM_BUTTON)
            logger.info(f"已删除扫描方案")
        except Exception as e:
            logger.error(f"点击删除扫描方案异常: {str(e)}")
            raise
