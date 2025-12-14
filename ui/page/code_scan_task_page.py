from config.contants import CREATE_BUTTON, CODE_SCAN_TASK_NAME, CODE_SCAN_TASK_APP, CODE_SCAN_TASK_BRANCH, \
    SCAN_MODE_FULL, SCAN_MODE_INCREMENTAL, ADD_BUTTON, GENERATE_PDF, CODE_SCAN_TASK_SEARCH, SCAN_CLICK_SEARCH, DELETE_SCAN_TASK, CODE_PLAN_CONFIRM_BUTTON, \
    CODE_SCAN_TASK_FILTER_PATH, CODE_SCAN_TASK_TIME, CODE_SCAN_TASK_TIME_RANGE, CODE_SCAN_TASK_BASIC_VERSION_BUTTON, CODE_SCAN_TASK_BASIC_VERSION, CODE_SCAN_TASK_COMPARE_VERSION_BUTTON, \
    CODE_SCAN_TASK_COMPARE_VERSION, CODE_SCAN_TASK_PLAN_NAME
from utils.elements import QualityGatesElement, ConfirmButtonElement, FilterPathElement, BranchElement, \
    ApplicationElement, PlanElement, TaskOperationElement, ScanModeElement
from utils.logger import logger

"""代码扫描任务"""


class CodeScanTaskPage:
    def __init__(self, controller):
        self.controller = controller

    def click_create_button(self):
        """点击新建按钮"""
        logger.info(f"开始创建扫描任务:")
        self.controller.click(CREATE_BUTTON)

    def choose_plan(self, plan_name):
        """选择扫描方案"""
        plan_element = PlanElement(self.controller)
        plan_element.choose_plan(CODE_SCAN_TASK_PLAN_NAME, plan_name)

    def input_task_name(self, name):
        """输入任务名称"""
        self.controller.input_text(CODE_SCAN_TASK_NAME, name)
        logger.info(f"已输入任务名称:{name}")

    def choose_app(self, app_name):
        """选择应用"""
        app_element = ApplicationElement(self.controller)
        app_element.choose_app(CODE_SCAN_TASK_APP, app_name)

    def choose_branch(self, branch_name):
        """选择分支"""
        branch_element = BranchElement(self.controller)
        branch_element.choose_branch(CODE_SCAN_TASK_BRANCH, branch_name)

    def choose_scan_mode(self, mode):
        """选择扫描模式"""
        mode_map = {
            "全量": SCAN_MODE_FULL,
            "增量": SCAN_MODE_INCREMENTAL
        }
        scan_mode_element = ScanModeElement(self.controller)
        scan_mode_element.choose_scan_mode(mode, mode_map)
        # 如果是增量模式，设置额外的配置信息
        if mode == "增量":
            self._set_incremental_mode_details()

    def _set_incremental_mode_details(self):
        """设置增量模式的详细配置"""
        try:
            self.controller.click(CODE_SCAN_TASK_TIME)
            self.controller.click(CODE_SCAN_TASK_TIME_RANGE)
            self.controller.click(CODE_SCAN_TASK_BASIC_VERSION_BUTTON)
            self.controller.click(CODE_SCAN_TASK_BASIC_VERSION)
            self.controller.click(CODE_SCAN_TASK_COMPARE_VERSION_BUTTON)
            self.controller.click(CODE_SCAN_TASK_COMPARE_VERSION)
            logger.info("已设置增量模式详细配置")
        except Exception as e:
            logger.error(f"设置增量模式详细配置失败: {str(e)}")
            raise Exception(f"设置增量模式详细配置失败: {str(e)}")

    def set_quality_gate(self, quality_gates):
        """设置质量门禁"""
        quality_gates_element = QualityGatesElement(self.controller)
        quality_gates_element.batch_set_thresholds(quality_gates, page_type="code")

    def add_filter_path(self, add_paths):
        """添加任务的过滤路径"""
        if not add_paths:
            logger.warning("当前没有可添加的过滤路径")
            return
        add_paths_element = FilterPathElement(self.controller)
        add_paths_element.add_filter_paths(add_paths, ADD_BUTTON, CODE_SCAN_TASK_FILTER_PATH)

    def choose_generate_pdf(self):
        """打开生成PDF"""
        self.controller.click(GENERATE_PDF)
        logger.info(f"已打开生成PDF报告")

    def confirm_task(self, task_type):
        """确认按钮"""
        confirm_button = ConfirmButtonElement(self.controller)
        confirm_button.click_confirm_button(task_type)

    def query_task(self, task_name):
        """查询任务"""
        task_operation = TaskOperationElement(self.controller)
        task_operation.query_task(CODE_SCAN_TASK_SEARCH, SCAN_CLICK_SEARCH, task_name)

    def delete_task(self):
        """删除任务"""
        task_operation = TaskOperationElement(self.controller)
        task_operation.delete_task(DELETE_SCAN_TASK, CODE_PLAN_CONFIRM_BUTTON)
