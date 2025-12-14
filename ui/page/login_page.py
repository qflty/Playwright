from config.contants import URL_TEST, USERNAME_LOCATER, DEMOUSER, PASSWORD_LOCATER, DEMOUSER_PASSWORD, LOGIN_BUTTON, BUTTON1, BUTTON2
from utils.logger import logger


class LoginPage:
    def __init__(self, controller):
        """
        初始化登录页面对象
        :param controller: BrowserController实例
        """
        self.controller = controller

    def login(self, username=DEMOUSER, password=DEMOUSER_PASSWORD):
        """登录系统"""
        self.controller.open(URL_TEST)
        logger.info(f"已打开页面: {URL_TEST}")
        # self.controller.refresh()
        try:
            # 选择组织
            # self.controller.click(TEST_ORGANIZATION)
            # self.controller.click(CHOOSE_ORGANIZATION)
            # 输入账号和密码，点击登录
            self.controller.input_text(USERNAME_LOCATER, username)
            self.controller.input_text(PASSWORD_LOCATER, password)
            self.controller.click(LOGIN_BUTTON)
            logger.info("已点击登录按钮")
            self.controller.sleep(1)
        except Exception as e:
            self.controller.capture("账号密码登录失败")
            logger.error(f"账号密码登录异常: {e}")
            raise AssertionError("账号密码登录失败") from e
        try:
            # 处理可能出现的提示框
            if self.controller.is_element_present(BUTTON1):
                self.controller.click(BUTTON1)
                logger.info("已点击我知道了按钮")
            elif self.controller.is_element_present(BUTTON2):
                self.controller.click(BUTTON2)
                logger.info("已点击工作台按钮")
            else:
                logger.warning("未找到提示框按钮")
        except Exception as e:
            self.controller.capture("处理提示框异常")
            logger.error(f"点击[我知道了]异常: {e}")
            logger.warning("提示框处理失败，但继续执行测试")
