import os
import time
import uuid
import asyncio
import allure
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from utils.logger import logger

# 定位方式映射，简化外部使用
BY_MAPPING = {
    'id': 'id',
    'xpath': 'xpath',
    'link_text': 'text',
    'partial_link_text': 'text',
    'name': 'attribute=name',
    'tag_name': 'css',
    'class_name': 'css',
    'css_selector': 'css'
}


class BrowserController:
    """Playwright浏览器控制器，提供网页自动化操作功能"""
    def __init__(self, browser_type='chromium', headless=False, timeout=10000):
        """
        初始化浏览器控制器
        :param browser_type: 浏览器类型，支持chromium, firefox, webkit
        :param headless: 是否无头模式
        :param timeout: 超时时间(毫秒)
        """
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.browser_type = browser_type
        self.headless = headless
        self.timeout = timeout

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def start(self):
        """启动浏览器"""
        try:
            self.playwright = await async_playwright().start()

            # 根据浏览器类型启动
            if self.browser_type == 'chromium':
                self.browser = await self.playwright.chromium.launch(headless=self.headless)
            elif self.browser_type == 'firefox':
                self.browser = await self.playwright.firefox.launch(headless=self.headless)
            elif self.browser_type == 'webkit':
                self.browser = await self.playwright.webkit.launch(headless=self.headless)
            else:
                raise ValueError(f"Unsupported browser type: {self.browser_type}")

            # 创建新的浏览器上下文
            self.context = await self.browser.new_context()
            # 设置默认超时
            self.context.set_default_timeout(self.timeout)

            # 创建新页面
            self.page = await self.context.new_page()
            logger.info(f"浏览器已启动: {self.browser_type}")

        except Exception as e:
            logger.error(f"启动浏览器失败: {e}")
            raise

    async def close(self):
        """关闭浏览器并释放资源"""
        try:
            if self.page:
                await self.page.close()
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()
            logger.info("浏览器已成功关闭")
        except Exception as e:
            logger.error(f"关闭浏览器时出错: {e}")

    async def open(self, url):
        """打开指定URL"""
        try:
            logger.info(f"打开URL: {url}")
            await self.page.goto(url)
            await self.page.wait_for_load_state('networkidle')
        except Exception as e:
            logger.error(f"打开URL失败: {url}, 错误: {e}")
            await self.capture(f"打开URL失败_{url}")
            raise

    def _get_locator(self, method, locator):
        """将定位方法和表达式转换为Playwright定位器"""
        playwright_method = BY_MAPPING.get(method.lower(), method)

        if playwright_method == 'tag_name':
            # Playwright中通过CSS选择器处理tag_name
            return self.page.locator(locator)
        elif playwright_method == 'class_name':
            # Playwright中class选择器需要加点
            return self.page.locator(f".{locator}")
        else:
            return self.page.locator(f"{playwright_method}={locator}")

    async def wait_for_element(self, method, locator, timeout=None, condition='visible'):
        """
        等待元素满足指定条件
        :param method: 定位方式
        :param locator: 定位表达式
        :param timeout: 超时时间(毫秒)
        :param condition: 等待条件，支持'visible', 'hidden', 'attached', 'detached'
        :return: 定位器
        """
        try:
            element_locator = self._get_locator(method, locator)
            timeout_ms = timeout or self.timeout

            conditions = {
                'visible': element_locator.wait_for(state='visible', timeout=timeout_ms),
                'hidden': element_locator.wait_for(state='hidden', timeout=timeout_ms),
                'attached': element_locator.wait_for(state='attached', timeout=timeout_ms),
                'detached': element_locator.wait_for(state='detached', timeout=timeout_ms),
                'present': element_locator.wait_for(state='attached', timeout=timeout_ms),
                'clickable': element_locator.wait_for(state='visible', timeout=timeout_ms)
            }

            await conditions.get(condition, conditions['visible'])
            logger.info(f"元素已找到，定位方式: {method}, 路径: {locator}")
            return element_locator

        except PlaywrightTimeoutError as e:
            current_url = self.page.url
            logger.error(
                f"元素未在 {timeout_ms}ms 内满足条件: {condition}, 定位方式: {method}, 路径: {locator}, 当前URL: {current_url}")
            await self.capture(f"元素等待超时_{locator}")
            return None

    async def click(self, method, locator, timeout=None):
        """点击元素"""
        try:
            element = await self.wait_for_element(method, locator, timeout, 'clickable')
            if element:
                # 滚动到元素可见位置
                await self.scroll_to_element(method, locator)
                await element.click()
                logger.info(f"成功点击元素: {locator}")
        except Exception as e:
            logger.warning(f"点击失败: {e}")

    async def input_text(self, method, locator, text, clear=True, timeout=None):
        """输入文本"""
        try:
            element = await self.wait_for_element(method, locator, timeout, 'visible')
            if element:
                if clear:
                    await element.fill("")  # Playwright的fill方法会自动清空
                await element.fill(text)
                logger.info(f"成功输入文本到元素: {locator}")
        except Exception as e:
            logger.error(f"输入文本失败: {e}")

    async def get_text(self, method, locator, timeout=None):
        """获取元素文本"""
        try:
            element = await self.wait_for_element(method, locator, timeout, 'visible')
            if element:
                text = await element.text_content()
                return text or ""
        except Exception as e:
            logger.error(f"获取元素文本失败: {e}")
            return ""

    async def is_element_present(self, method, locator, timeout=2000):
        """检查元素是否存在"""
        try:
            element = await self.wait_for_element(method, locator, timeout, 'attached')
            return element is not None
        except Exception as e:
            logger.error(f"检查元素是否存在失败: {e}")
            return False

    async def capture(self, step, folder_path='reports/ui_reports/screenshots'):
        """截图并保存，同时添加到Allure报告"""
        await asyncio.sleep(1)  # 等待1秒

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        timestamp = time.strftime("%Y%m%d_%H%M%S")
        unique_id = uuid.uuid4().hex
        filename = f"{step}_screenshot_{timestamp}_{unique_id}.png"
        file_path = os.path.join(folder_path, filename)

        try:
            # Playwright截图
            screenshot = await self.page.screenshot(path=file_path, full_page=True)

            # 添加到Allure报告
            with open(file_path, "rb") as f:
                allure.attach(f.read(), name=step, attachment_type=allure.attachment_type.PNG)

            logger.info(f"截图已保存: {file_path}")
        except Exception as e:
            logger.error(f"截图失败: {e}")

    async def scroll_to_element(self, method, locator, timeout=None):
        """滚动到元素可见位置"""
        try:
            element = await self.wait_for_element(method, locator, timeout, 'attached')
            if element:
                await element.scroll_into_view_if_needed()
                await asyncio.sleep(1)  # 等待滚动完成
        except Exception as e:
            logger.warning(f"滚动到元素失败: {e}")

    async def execute_script(self, script, *args):
        """执行JavaScript代码"""
        try:
            result = await self.page.evaluate(script, *args)
            return result
        except Exception as e:
            logger.error(f"执行JavaScript失败: {e}")
            return None

    async def get_attribute(self, method, locator, attribute_name, timeout=None):
        """获取元素属性值"""
        try:
            element = await self.wait_for_element(method, locator, timeout, 'attached')
            if element:
                value = await element.get_attribute(attribute_name)
                return value
        except Exception as e:
            logger.error(f"获取元素属性失败: {e}")
            return None
