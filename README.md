# 自动化测试框架

这是一个集成了UI测试和API测试的自动化测试框架，基于Playwright和pytest构建。

## 项目结构

```
.
├── api/              # API测试相关代码
│   ├── core/         # 核心模块
│   └── client.py     # API客户端封装
├── config/           # 配置文件
├── logs/             # 日志文件
├── reports/          # 测试报告
├── ui/               # UI测试相关代码
│   ├── page/         # 页面对象模型
│   ├── test_cases/   # 测试用例
│   └── creator/      # 测试创建器
├── utils/            # 工具类
├── runner.py         # 测试运行器
└── requirements.txt  # 依赖包
```


## 环境要求

- Python 3.8+
- Playwright支持的浏览器
- Allure命令行工具（用于生成测试报告）

## 安装依赖

```bash
# 安装Python依赖
pip install -r requirements.txt

# 安装Playwright浏览器
playwright install

# 安装Allure（Windows）
# 下载并配置Allure命令行工具
```


## 配置文件

### 环境变量配置

在项目根目录创建 `.env` 文件配置环境变量：

```env
# 基础配置
ENV=test
LOG_LEVEL=INFO

# API测试配置
BASE_URL=http://localhost:8080
SPACE_ID=1234
SESSION_TOKEN=
TIMEOUT=30
RETRY_TIMES=3

# UI测试配置
BROWSER_TYPE=chromium
HEADLESS=False
UI_TIMEOUT=30000

# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
PGSQL_HOST=localhost
PGSQL_PORT=5432

# Allure配置
ALLURE_PATH=D:\Allure\allure-2.24.0\bin\allure.bat
```


## 使用方法

### 运行UI测试

```bash
# 运行所有UI测试
python runner.py ui

# 运行指定文件的UI测试
python runner.py ui --file ui/test_cases/test_case_artifact_scan_plan.py

# 运行指定标签的UI测试
python runner.py ui --mark artifact_scan_plan

# 运行包含特定关键字的UI测试
python runner.py ui --keyword "扫描方案"

# 指定测试环境
python runner.py ui --env test
```


### 运行API测试

```bash
# 运行API测试
python runner.py api

# 指定测试环境
python runner.py api --env test

# 指定测试用例文件
python runner.py api --file api/test_cases/test_data.xlsx

# 指定测试模块
python runner.py api --module user
```


### 参数说明

- `type`: 测试类型，必填，可选值为 [ui](file://D:\Pycharm\PythonProjects\Playwright\config\config.py#L59-L59) 或 [api](file://D:\Pycharm\PythonProjects\Playwright\config\config.py#L57-L57)
- `--env`: 测试环境，可选值为 `dev`/`test`/`prod`，默认为 `test`
- `--file`: 测试用例文件路径
- `--module`: 指定API测试模块
- `--mark`: 运行指定标签的UI测试用例
- `--keyword`: 通过关键字过滤UI测试用例

## 测试数据

### UI测试数据

- 测试用例文件位于 `ui/test_cases/` 目录
- 测试数据文件位于 `ui/test_cases/test_data/` 目录，使用YAML格式

### API测试数据

- 测试用例文件位于 `api/test_cases/` 目录，使用Excel格式

## 测试报告和截图

### UI测试

- **Allure报告**: `reports/ui_reports/html/index.html`
- **截图文件**: `reports/ui_reports/screenshots/`

### API测试

- **HTML报告**: 报告路径会在测试完成后输出到控制台

## 项目特点

1. **Page Object模式**: UI测试采用页面对象模型，提高代码可维护性
2. **数据驱动**: 支持YAML和Excel格式的测试数据驱动
3. **环境隔离**: 支持多环境配置切换
4. **日志记录**: 完整的日志记录和错误追踪
5. **报告生成**: 自动生成详细的测试报告
6. **异常处理**: 完善的异常处理和重试机制

## 开发规范

1. UI测试用例应继承相应的测试类
2. 测试数据应与测试用例分离
3. 遵循现有的代码风格和命名规范
4. 添加必要的日志记录以便调试
5. 确保测试用例的独立性和可重复执行性