import os
import time
import uuid
import allure
from playwright.sync_api import sync_playwright, TimeoutError, Error
from config.config import config
from utils.logger import logger


class BrowserController:
    """Playwright浏览器控制器，提供网页自动化操作功能"""

    def __init__(self, browser_type='chromium', headless=True, timeout=10000):
        """
        初始化浏览器控制器
        :param browser_type: 浏览器类型，支持chromium, firefox, webkit
        :param headless: 是否无头模式运行
        :param timeout: 操作超时时间，默认10秒(单位毫秒)
        """
        self.browser_type = browser_type
        self.headless = headless
        self.timeout = timeout
        self.pw = None
        self.browser = None
        self.context = None
        self.page = None
        self._initialize()

    def _initialize(self):
        """初始化Playwright和浏览器"""
        try:
            self.pw = sync_playwright().start()
            self.browser = self._initialize_browser()
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
        except Exception as e:
            logger.error(f"初始化浏览器失败: {e}")
            self.close()
            raise

    def _initialize_browser(self):
        """根据浏览器类型初始化Playwright浏览器实例"""
        browser_types = {
            'chromium': self.pw.chromium,
            'firefox': self.pw.firefox,
            'webkit': self.pw.webkit
        }
        if self.browser_type not in browser_types:
            raise ValueError(f"Unsupported browser type: {self.browser_type}")
        # 配置浏览器启动选项
        launch_options = {
            'headless': self.headless,
            'timeout': self.timeout
        }
        # 如果不是无头模式，设置窗口大小为全屏
        if not self.headless:
            if self.browser_type == 'chromium':
                launch_options['args'] = [
                    '--start-maximized',
                    '--disable-infobars',
                    '--disable-extensions'
                ]
            elif self.browser_type == 'firefox':
                launch_options['args'] = [
                    '--start-maximized'
                ]
            launch_options['args'].append('--window-size=1920,1080')
        # 如果是远程执行，添加远程连接配置
        if hasattr(config, 'hub_url') and config.hub_url and self.browser_type == 'chromium':
            launch_options['ws_endpoint'] = config.hub_url
            logger.info(f"使用远程浏览器连接: {config.hub_url}")
        return browser_types[self.browser_type].launch(**launch_options)

    def open(self, url):
        """打开指定URL"""
        try:
            logger.info(f"打开URL: {url}")
            self.page.goto(url, wait_until='networkidle')
            self.sleep(2)  # 初始加载等待
        except Error as e:
            logger.error(f"打开URL失败: {url}, 错误: {e}")
            raise

    def close(self):
        """关闭浏览器并释放资源"""
        try:
            if hasattr(self, 'context') and self.context:
                self.context.close()
            if hasattr(self, 'browser') and self.browser:
                self.browser.close()
            if hasattr(self, 'pw') and self.pw:
                self.pw.stop()
            logger.info("浏览器已成功关闭")
        except Error as e:
            logger.error(f"关闭浏览器时出错: {e}")

    # def __del__(self):
    #     """对象销毁时确保浏览器关闭"""
    #     self.close()

    # 添加上下文管理器支持，确保资源可靠释放
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False  # 不抑制异常

    def refresh(self, timeout=None):
        """刷新当前页面"""
        try:
            logger.info("刷新页面")
            self.page.reload(timeout=timeout or self.timeout)
            self.sleep(1)  # 刷新后短暂等待
        except Error as e:
            logger.error(f"刷新页面失败: {e}")
            raise

    def sleep(self, seconds=1):
        """线程休眠指定时间"""
        time.sleep(seconds)

    def locate(self, selector):
        """定位元素"""
        return self.page.locator(selector)

    def _get_element(self, selector, timeout=None):
        """获取元素并应用超时设置"""
        if timeout is not None:
            self.page.set_default_timeout(timeout)
            element = self.locate(selector)
            self.page.set_default_timeout(self.timeout)
            return element
        return self.locate(selector)

    def click(self, selector, timeout=None):
        """点击元素"""
        try:
            self._get_element(selector, timeout).click()
        except Error as e:
            logger.warning(f"点击失败: {e}")
            raise

    def input_text(self, selector, text, clear=True, timeout=None):
        """输入文本"""
        element = self._get_element(selector, timeout)
        if clear:
            element.clear()
        element.fill(text)

    def upload_file(self, selector, file_path):
        """上传文件"""
        try:
            element = self._get_element(selector)
            element.set_input_files(file_path)
            logger.info(f"上传文件成功: {file_path}")
        except Error as e:
            logger.error(f"上传文件失败: {e}")
            raise

    def get_text(self, selector):
        """获取元素文本"""
        return self.locate(selector).text_content()

    def is_element_present(self, selector, timeout=None):
        """检查元素是否存在"""
        try:
            if timeout is not None:
                # 使用显式等待而不是修改默认超时
                self.locate(selector).wait_for(state='attached', timeout=timeout)
            else:
                self.locate(selector).wait_for(state='attached', timeout=self.timeout)
            return True
        except Error:
            return False

    def wait_for_element_to_disappear(self, selector, timeout=None):
        """等待元素消失"""
        timeout = timeout or self.timeout
        try:
            self.locate(selector).wait_for(state='detached', timeout=timeout)
            return True
        except TimeoutError:
            return False

    def switch_to_iframe(self, selector, timeout=None):
        """切换到iframe"""
        timeout = timeout or self.timeout
        frame = self.page.frame_locator(selector).frame(timeout=timeout)
        if frame:
            self.page = frame.page
            return True
        return False

    def switch_to_default_content(self):
        """切换回主文档"""
        self.page = self.context.pages[0]

    def switch_to_new_window(self, trigger_action=None, trigger_selector=None, url=None):
        """切换到最新打开的窗口
        :param trigger_action: 触发动作类型 ('click', 'js', None)
        :param trigger_selector: 触发元素选择器
        :param url: 新窗口要打开的URL
        """
        with self.context.expect_page() as new_page_info:
            if trigger_action == 'click' and trigger_selector:
                # 点击元素触发新窗口
                self.page.click(trigger_selector)
            elif trigger_action == 'js':
                # JavaScript触发新窗口
                target_url = url or 'about:blank'
                self.page.evaluate(f"window.open('{target_url}', '_blank')")
            # 如果没有指定触发动作，则假定新窗口已经在其他地方被触发
        try:
            new_page = new_page_info.value
            if new_page:
                new_page.wait_for_load_state()
                self.page = new_page
                logger.info("成功切换到新窗口")
                return True
            else:
                logger.warning("未检测到新窗口")
                return False
        except Exception as e:
            logger.error(f"切换新窗口失败: {e}")
            return False

    def capture(self, step, folder_path=None):
        """截图并保存，同时添加到Allure报告"""
        self.sleep(1)
        # 如果没有指定路径，默认保存到项目根目录的reports/ui_reports文件夹
        if folder_path is None:
            # 获取项目根目录
            project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            folder_path = os.path.join(project_root, 'reports', 'ui_reports', 'screenshots')
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex
        filename = f"{step}_screenshot_{timestamp}_{unique_id}.png"
        file_path = os.path.join(folder_path, filename)
        try:
            screenshot = self.page.screenshot(path=file_path, full_page=True)
            allure.attach(screenshot, name=step, attachment_type=allure.attachment_type.PNG)
            logger.info(f"截图已保存: {file_path}")
        except Exception as e:
            logger.error(f"截图失败: {e}")

    def execute_script(self, script, *args):
        """执行JavaScript代码"""
        return self.page.evaluate(script, args)

    def scroll_to_element(self, selector, timeout=None):
        """滚动到元素可见位置"""
        self.locate(selector).scroll_into_view_if_needed()
        self.sleep(1)  # 等待滚动完成

    def scroll_page(self, x=0, y=0):
        """滚动页面"""
        self.page.mouse.wheel(x, y)

    def get_attribute(self, selector, attribute_name, timeout=None):
        """获取元素属性值"""
        return self.locate(selector).get_attribute(attribute_name)

    def set_attribute(self, selector, attribute_name, value, timeout=None):
        """设置元素属性值"""
        element = self.locate(selector)
        self.execute_script(f"(element) => element.{attribute_name} = '{value}'", element)
