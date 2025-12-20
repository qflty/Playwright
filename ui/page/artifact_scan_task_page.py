from config.constants import CREATE_BUTTON, BELONGING_NODE, CHOOSE_PLAN_NAME, SCAN_TASK_NAME, GENERIC_PATH, DOCKER_PATH, \
    ARTIFACT_WAREHOUSE, CHOOSE_DROPDOWN, ARTIFACT_NAME, ARTIFACT_VERSION, ADD_BUTTON, HARBOR_NODE, REGISTRY_NODE, \
    NEXUS_NODE, ENTER_KEYWORDS_IN_SEARCH_BOX, SCAN_CLICK_SEARCH, DELETE_SCAN_TASK, DELETE_CONFIRM_BUTTON, ARTIFACT_PATH
from utils.elements import QualityGatesElement, ConfirmButtonElement, PlanElement, TaskOperationElement, \
    ArtifactTypeElement
from utils.logger import logger

"""制品扫描任务"""


class ArtifactScanTaskPage:
    def __init__(self, controller):
        self.controller = controller

    def click_create_button(self):
        logger.info(f"开始创建扫描任务:")
        self.controller.click(CREATE_BUTTON)

    def choose_node(self, node):
        """选择所属节点"""
        self.controller.click(BELONGING_NODE)
        node_map = {
            "harbor": HARBOR_NODE,
            "registry": REGISTRY_NODE,
            "nexus": NEXUS_NODE
        }
        node_path = node_map.get(node)
        if not node_path:
            logger.error(f"所属节点不存在: {node}")
            raise Exception(f"所属节点不存在: {node}")
        self.controller.click(node_path)

    def choose_plan(self, plan_name):
        """选择扫描方案"""
        plan_element = PlanElement(self.controller)
        plan_element.choose_plan(CHOOSE_PLAN_NAME, plan_name)

    def input_task_name(self, name):
        """输入任务名称"""
        self.controller.input_text(SCAN_TASK_NAME, name)
        logger.info(f"已输入任务名称: {name}")

    def choose_artifact_type(self, artifact_type):
        """选择要扫描的制品类型"""
        type_map = {
            "generic": GENERIC_PATH,
            "docker": DOCKER_PATH
        }
        artifact_type_element = ArtifactTypeElement(self.controller)
        artifact_type_element.choose_artifact_type(artifact_type, type_map)

    def choose_artifact_path(self, artifact_type):
        """选择制品"""
        try:
            self.controller.click(ADD_BUTTON)
            self.controller.click(ARTIFACT_WAREHOUSE)
            self.controller.sleep(1)
            self.controller.click(CHOOSE_DROPDOWN)
            logger.info(f"已选择制品仓库")
            self.controller.click(ARTIFACT_NAME)
            self.controller.sleep(1)
            self.controller.click(CHOOSE_DROPDOWN)
            logger.info(f"已选择制品名称")
            self.controller.click(ARTIFACT_VERSION)
            self.controller.sleep(1)
            self.controller.click(CHOOSE_DROPDOWN)
            logger.info(f"已选择制品版本")
            if artifact_type == "generic" or not artifact_type:
                self.controller.click(ARTIFACT_PATH)
                logger.info(f"已选择制品路径")
            logger.info(f"已选择制品")
        except Exception as e:
            logger.error(f"选择制品失败: {artifact_type}, 错误信息: {str(e)}")
            raise Exception(f"选择制品失败: {artifact_type}")

    def set_quality_gate(self, quality_gates):
        """设置质量门禁"""
        quality_gates_element = QualityGatesElement(self.controller)
        quality_gates_element.batch_set_thresholds(quality_gates, page_type="artifact")

    def confirm_task(self, task_type):
        """确认按钮"""
        confirm_button = ConfirmButtonElement(self.controller)
        confirm_button.click_confirm_button(task_type)

    def query_task(self, task_name):
        """查询任务"""
        task_operation = TaskOperationElement(self.controller)
        task_operation.query_task(ENTER_KEYWORDS_IN_SEARCH_BOX, SCAN_CLICK_SEARCH, task_name)

    def delete_task(self):
        """删除任务"""
        task_operation = TaskOperationElement(self.controller)
        task_operation.delete_task(DELETE_SCAN_TASK, DELETE_CONFIRM_BUTTON)
