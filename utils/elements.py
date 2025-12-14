from utils.logger import logger
from utils.xpath_builder import XPathBuilder
from config.contants import (
    QUALITY_CONTROL, CODE_SCAN_TASK_QUALITY_BUTTON,
    SERIOUS_LEVEL, HIGH_RISK_LEVEL, MODERATE_RISK_LEVEL, LOW_RISK_LEVEL, UNRATED_LEVEL,
    QUALITY_GATES_BLOCKING, QUALITY_GATES_SERIOUS, QUALITY_GATES_PRIMARY, QUALITY_GATES_SECONDARY, SAVE_ONLY_BUTTON,
    SAVE_AND_EXECUTE_BUTTON
)



class PlanElement:
    """方案元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def choose_plan(self, plan_input_xpath, plan_name):
        """选择方案"""
        if not plan_name:
            logger.info("未选择方案，使用默认方案")
            return
        try:
            self.controller.click(plan_input_xpath)
            plan_option_xpath = XPathBuilder.build_plan_option_xpath(plan_name)
            self.controller.click(plan_option_xpath)
            logger.info(f"已选择方案: {plan_name}")
        except Exception:
            logger.error(f"未找到方案: {plan_name}")
            raise Exception(f"无法选择扫描方案: {plan_name}")


class ApplicationElement:
    """应用元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def choose_app(self, app_input_xpath, app_name):
        """选择应用"""
        self.controller.click(app_input_xpath)
        self.controller.input_text(app_input_xpath, app_name)
        app_option_xpath = f"//span[contains(text(),'{app_name}')]/.."
        self.controller.click(app_option_xpath)
        logger.info(f"已选择应用: {app_name}")


class BranchElement:
    """分支元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def choose_branch(self, branch_input_xpath, branch_name):
        """选择分支"""
        self.controller.click(branch_input_xpath)
        self.controller.input_text(branch_input_xpath, branch_name)
        branch_option_xpath = f"//span[contains(text(),'{branch_name}')]/.."
        self.controller.click(branch_option_xpath)
        logger.info(f"已选择分支: {branch_name}")


class FilterPathElement:
    """过滤路径元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def add_filter_paths(self, add_paths, add_button_xpath, input_base_xpath):
        """添加过滤路径"""
        if not add_paths:
            logger.info("未添加过滤路径")
            return
        for index, add_path in enumerate(add_paths, start=1):
            self.controller.click(add_button_xpath)
            logger.info("已点击添加按钮")
            self.controller.sleep(1)
            input_xpath = f"{input_base_xpath}[{index}]"
            self.controller.input_text(input_xpath, add_path)
            logger.info(f"已添加过滤路径: {add_path}")
        logger.info("已添加所有过滤路径")


class QualityGatesElement:
    """质量门禁元素封装类"""
    # 制品扫描任务质量门禁字段映射
    ARTIFACT_QUALITY_FIELDS = {
        "serious": SERIOUS_LEVEL,
        "high_risk": HIGH_RISK_LEVEL,
        "moderate_risk": MODERATE_RISK_LEVEL,
        "low_risk": LOW_RISK_LEVEL,
        "unrated": UNRATED_LEVEL
    }
    # 代码扫描任务质量门禁字段映射
    CODE_QUALITY_FIELDS = {
        "blocking": QUALITY_GATES_BLOCKING,
        "serious": QUALITY_GATES_SERIOUS,
        "primary": QUALITY_GATES_PRIMARY,
        "secondary": QUALITY_GATES_SECONDARY
    }

    def __init__(self, controller):
        """
        初始化质量门禁元素对象
        :param controller: BrowserController实例
        """
        self.controller = controller

    def set_threshold(self, level, value, page_type="artifact"):
        """
        设置质量门禁阈值
        :param level: 门禁级别
        :param value: 阈值 (字符串形式)
        :param page_type: 页面类型 ("artifact" 或 "code")
        """
        if not value:
            logger.info(f"质量门禁 {level} 未设置值")
            return
        # 根据页面类型选择对应的字段映射
        if page_type == "artifact":
            field_xpath = self.ARTIFACT_QUALITY_FIELDS.get(level)
        else:
            field_xpath = self.CODE_QUALITY_FIELDS.get(level)
        if not field_xpath:
            logger.warning(f"不支持的质量门禁级别: {level}")
            raise ValueError(f"不支持的质量门禁级别: {level}")
        try:
            self.controller.input_text(field_xpath, value)
            logger.info(f"已设置质量门禁: {level} - {value}")
        except Exception as e:
            logger.error(f"设置质量门禁失败: {level} - {value}, 错误信息: {str(e)}")
            raise Exception(f"设置质量门禁 {level} 失败") from e

    def batch_set_thresholds(self, quality_gates, page_type="artifact"):
        """
        批量设置质量门禁阈值
        :param quality_gates: 质量门禁配置字典
        :param page_type: 页面类型 ("artifact" 或 "code")
        """
        if not quality_gates:
            logger.info("未设置质量门禁")
            return
        # 点击质量门禁展开按钮
        try:
            if page_type == "artifact":
                self.controller.click(QUALITY_CONTROL)
            elif page_type == "code":
                self.controller.click(CODE_SCAN_TASK_QUALITY_BUTTON)
            else:
                logger.warning(f"不支持的页面类型: {page_type}")
        except Exception as e:
            logger.warning(f"点击质量门禁按钮失败: {str(e)}")
        # 批量设置各个门禁级别
        for gate_type, gate_value in quality_gates.items():
            self.set_threshold(gate_type, gate_value, page_type)


class ConfirmButtonElement:
    """确认按钮元素封装类"""
    # 任务确认按钮映射
    TASK_CONFIRM_BUTTONS = {
        "仅保存": SAVE_ONLY_BUTTON,
        "保存并立即执行": SAVE_AND_EXECUTE_BUTTON
    }

    def __init__(self, controller):
        self.controller = controller

    def click_confirm_button(self, task_type):
        """
        点击任务确认按钮
        :param task_type: 任务类型 ("仅保存" 或 "保存并立即执行")
        """
        button_xpath = self.TASK_CONFIRM_BUTTONS.get(task_type)
        if not button_xpath:
            raise ValueError(f"不支持的确认按钮: {task_type}")
        try:
            self.controller.click(button_xpath)
            logger.info(f"已选择确认按钮: {task_type}")
        except Exception as e:
            logger.error(f"点击确认按钮失败: {task_type}, 错误信息: {str(e)}")
            raise


class TaskOperationElement:
    """任务操作元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def query_task(self, search_input_xpath, search_button_xpath, task_name):
        """查询任务"""
        self.controller.input_text(search_input_xpath, task_name)
        self.controller.click(search_button_xpath)
        logger.info(f"已查询任务: {task_name}")

    def delete_task(self, delete_button_xpath, confirm_button_xpath):
        """删除任务"""
        self.controller.click(delete_button_xpath)
        self.controller.click(confirm_button_xpath)
        logger.info("已删除任务")


class ScanModeElement:
    """扫描模式元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def choose_scan_mode(self, mode, mode_mapping):
        """选择扫描模式"""
        if not mode:
            logger.info("未指定扫描模式，使用默认模式")
            return
        mode_xpath = mode_mapping.get(mode)
        if not mode_xpath:
            logger.error(f"不支持的扫描模式: {mode}")
            raise Exception(f"不支持的扫描模式: {mode}")
        try:
            self.controller.click(mode_xpath)
            logger.info(f"已选择扫描模式: {mode}")
        except Exception as e:
            logger.error(f"选择扫描模式失败: {mode}, 错误信息: {str(e)}")
            raise Exception(f"选择扫描模式失败: {mode}")


class ArtifactTypeElement:
    """制品类型元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def choose_artifact_type(self, artifact_type, type_mapping):
        """选择制品类型"""
        if not artifact_type:
            logger.info("未指定制品类型，使用默认制品类型")
            return
        type_xpath = type_mapping.get(artifact_type)
        if not type_xpath:
            logger.error(f"不支持的制品类型: {artifact_type}")
            raise Exception(f"不支持的制品类型: {artifact_type}")
        try:
            self.controller.click(type_xpath)
            logger.info(f"已选择制品类型: {artifact_type}")
        except Exception as e:
            logger.error(f"选择制品类型失败: {artifact_type}, 错误信息: {str(e)}")
            raise Exception(f"选择制品类型失败: {artifact_type}")


class ConfigOperationElement:
    """配置操作元素封装类"""
    def __init__(self, controller):
        self.controller = controller

    def save_config(self, save_button_xpath):
        """保存配置"""
        self.controller.click(save_button_xpath)
        logger.info("已点击保存配置")
        self.controller.sleep(1)

    def delete_config(self, delete_button_xpath, confirm_button_xpath):
        """删除方案"""
        self.controller.click(delete_button_xpath)
        self.controller.click(confirm_button_xpath)
