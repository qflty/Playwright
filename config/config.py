from pathlib import Path
from typing import Dict, Any, Optional
from pydantic import Field, SecretStr, ConfigDict
from pydantic_settings import BaseSettings

test_path = Path(__file__).parent.parent / "test.env"


class BaseConfigSettings(BaseSettings):
    """基础配置设置类"""
    model_config = ConfigDict(
        env_file=str(test_path),
        env_file_encoding='utf-8',
        extra='ignore'
    )


class UITestSettings(BaseConfigSettings):
    """UI测试相关配置"""
    browser_type: str = Field("chromium", validation_alias="BROWSER_TYPE")
    headless: bool = Field(False, validation_alias="HEADLESS")
    default_timeout: int = Field(30000, validation_alias="UI_TIMEOUT")
    screenshot_path: str = Field("reports/ui_reports/screenshots", validation_alias="SCREENSHOT_PATH")
    test_case_path: str = Field("ui/test_cases", validation_alias="TEST_DATA_PATH")


class APISettings(BaseConfigSettings):
    """API相关配置"""
    base_url: str = Field("http://localhost:8080", validation_alias="BASE_URL")
    space_id: str = Field("1234", validation_alias="SPACE_ID")
    session_token: SecretStr = Field("", validation_alias="SESSION_TOKEN")
    timeout: int = Field(30, validation_alias="API_TIMEOUT")
    retry_times: int = Field(3, validation_alias="RETRY_TIMES")
    test_cases_dir: str = Field("api/test_cases", validation_alias="TEST_CASES_DIR")
    report_dir: str = Field("reports/api_reports", validation_alias="REPORT_DIR")
    report_title: str = Field("接口自动化测试报告", validation_alias="REPORT_TITLE")


class LogSettings(BaseConfigSettings):
    """日志相关配置"""
    log_level: str = Field("DEBUG", validation_alias="LOG_LEVEL")
    log_file: str = Field("logs/test.log", validation_alias="LOG_FILE")
    log_max_size: int = Field(10 * 1024 * 1024, validation_alias="LOG_MAX_SIZE")
    log_backup_count: int = Field(5, validation_alias="LOG_BACKUP_COUNT")


class GeneralSettings(BaseConfigSettings):
    """通用配置"""
    hub_url: str = Field('', validation_alias="HUB_URL")
    allure_path: str = Field(r"D:\Allure\allure-2.24.0\bin\allure.bat", validation_alias="ALLURE_PATH")
    env: str = Field('development', validation_alias="ENV")


class Config:
    """配置管理类"""
    def __init__(self, env_file: Optional[str] = None):
        # 初始化配置
        self.api = APISettings()
        self.log = LogSettings()
        self.ui = UITestSettings()
        self.general = GeneralSettings()
        self.hub_url = self.general.hub_url
        self.allure_path = self.general.allure_path
        print(f"配置加载完成 - 环境: {self.general.env}")

    def get_dict(self) -> Dict[str, Any]:
        """获取配置的字典形式（掩码敏感信息）"""
        config_dict = {
            'ui': {
                'browser_type': self.ui.browser_type,
                'headless': self.ui.headless,
                'default_timeout': self.ui.default_timeout,
                'screenshot_path': self.ui.screenshot_path,
                'test_case_path': self.ui.test_case_path
            },
            'api': {
                'base_url': self.api.base_url,
                'space_id': self.api.space_id,
                'timeout': self.api.timeout,
                'retry_times': self.api.retry_times,
                'session_token': '********' if self.api.session_token else ''
            },
            'logs': {
                'log_level': self.log.log_level,
                'log_file': self.log.log_file,
                'log_max_size': self.log.log_max_size,
                'log_backup_count': self.log.log_backup_count
            },
            'general': {
            'hub_url': self.general.hub_url,
            'allure_path': self.allure_path,
            'env': self.general.env
            }
        }
        return config_dict


config = Config()