import allure

from utils.logger import logger


class StepExecutor:
    """测试步骤执行器，封装通用的步骤执行、日志、截图逻辑"""
    @staticmethod
    def execute_step(step_name, action, error_message, controller, capture_on_success=True):
        """
        执行测试步骤的通用方法
        :param step_name: 步骤名称（用于Allure报告）
        :param action: 要执行的操作（lambda或函数）
        :param error_message: 错误提示信息
        :param controller: 浏览器控制器（用于截图）
        :param capture_on_success: 是否在出错时截图
        """
        with allure.step(step_name):
            try:
                action()
                # 可选：成功时截图
                if capture_on_success:
                    controller.capture(step=f"{step_name} - 成功")
            except Exception as e:
                logger.error(f"{error_message}: {e}", exc_info=True)
                controller.capture(step=f"{step_name} - 失败")
                raise AssertionError(f"{error_message}: {str(e)}")
