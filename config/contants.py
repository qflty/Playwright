# 定义常量，使用大写字母和下划线命名
# 测试环境 --------------------
# 测试环境
URL_TEST = "http://cube-front.product.poc.za-tech.net/"
# 试跑环境
ALPHA_URL = "http://cube.alpha.za-tech.net/"
# 开发环境
DEV_URL = "http://713-cube-front.product.poc.za-tech.net/"
# 远程Hub
HUB_URL = "http://cube-ui.alpha.za-tech.net"
LOCAL_URL = "http://192.168.85.60:4444"
# 组织
TEST_ORGANIZATION = "//p[contains(text(),'请选择要登录的组织')]/../div"
CHOOSE_ORGANIZATION = "//div[@title='研发运维一体化平台']"
# 账号
USERNAME_LOCATER = "//input[@placeholder='域账号']"
USERNAME = "admin"
DEMOUSER = "demouser"
# 密码
PASSWORD_LOCATER = "//input[@placeholder='密码']"
PASSWORD = "Admin@2024"
DEMOUSER_PASSWORD = "2wsx!QAZ"
# 登录按钮
LOGIN_BUTTON = "//span[contains(text(),'登 录')]/.."
# 选择团队
# CHOOSE_TEAM = "//*[@id='form']/div[1]/div[1]/div/div/div/div[1]/div/div"
# 登录后弹窗
BUTTON1 = "//span[contains(text(),'我知道了')]/.."
BUTTON2 = "//p[contains(text(),'工作台')]/../.."
# 用户名称
USER_BUTTON = "(//span[contains(text(),'梅')]/..)[1]"
LOGOUT_BUTTON = "//span[contains(text(),'登出')]/.."
# 菜单
PROJECT_MANAGEMENT_BUTTON = "//p[contains(text(),'项目')]/../.."
ARTIFACT_MANAGEMENT_BUTTON = "//p[contains(text(),'制品')]/../.."
ARTIFACT_SCANNER_BUTTON = "//p[contains(text(),'制品扫描')]/../../.."
CODE_MANAGEMENT_BUTTON = "(//p[contains(text(),'代码')]/../..)[1]"
CODE_SCANNER_BUTTON = "//p[contains(text(),'代码扫描')]/../../.."
# 制品扫描定位---------------------------------------
# 制品扫描下子目录
PLAN_BUTTON = "(//p[contains(text(),'制品扫描')]/../../../../div/div/div/div/div/button)[1]"
TASK_BUTTON = "(//p[contains(text(),'制品扫描')]/../../../../div/div/div/div/div/button)[2]"
# 创建按钮
CREATE_BUTTON = "//*[@id='app']/div/section/div/main/div/div[1]/div[1]/button"
# 方案名称
PLAN_NAME_LOCATER = "//label[contains(text(),'方案名称')]/../div/div/div/input"
# 设为默认
STE_DEFAULT = "//label[contains(text(),'设为默认')]/../div/div/div/span"
# 方案描述
PLAN_DESCRIPTION_INPUT = "//label[contains(text(),'描述')]/../div/div/div/textarea"
# 添加按钮
ADD_BUTTON = "(//span[contains(text(),'添加')]/..)[1]"
# 添加漏洞编号
ADD_VULN_IDS = "(//input[@placeholder='请输入内容'])"
# 导入编号按钮
INPORT_NUMBER_BUTTON = "//span[text()=' 导入编号 ']/.."
# 导入编号文件
IMPORT_NUMBER_FILE_lOCATER = "(//input[@type='file'])[2]"
# 漏洞编号文件
VULNERABILITY_NUMBER_FILE = r"D:\Downloads\谷歌下载\漏洞白名单模板.csv"
# 导入编号确定按钮
IMPORT_NUMBER_CONFIRM_BUTTON = "//div[2]/div/div[2]/button[2]"
# 输入漏洞编号
CVE_NUMBER_INPUT = "//*[@placeholder='请输入内容']"
# 确定按钮
PLAN_CONFIRM_BUTTON = "//*[@id='app']/div/section/div/main/div/div[2]/div/div/section/div/div[3]/button[2]"
# 扫描方案搜索框
SCAN_PLAN_SEARCH_ELE = "//input[@placeholder='请输入方案名称搜索']"
# 点击查询
SCAN_CLICK_SEARCH = "//span[contains(text(),'查询')]/.."
# 点击编辑扫描方案
EDIT_SCANNER_PLAN = "//*[@id='app']/div/section/div/main/div/div[1]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[8]/div/div/a[1]"
# 点击删除扫描方案
DELETE_SCANNER_PLAN = "//*[@id='app']/div/section/div/main/div/div[1]/div[3]/div[4]/div[2]/table/tbody/tr[1]/td[8]/div/div/a[2]"
# 删除弹窗
DELETE_CONFIRM = "//*[contains(text(), '确定删除当前方案吗')]"
# 删除方案点击确定
DELETE_CONFIRM_BUTTON = "//*[contains(text(), '确 定')]/.."
# 创建扫描任务页面
CREATE_TASK = "//*[contains(text(),'创建扫描任务')]"
# 所属节点
BELONGING_NODE = "//label[contains(text(), '所属节点')]/../div/div/div/div/input"
# 选择节点
HARBOR_NODE = "//span[contains(text(),'harbor')]/.."
REGISTRY_NODE = "//span[contains(text(),'registry')]/.."
NEXUS_NODE = "//span[contains(text(),'nexus')]/.."
# 方案名称
CHOOSE_PLAN_NAME = "//label[contains(text(),'方案名称')]/../div/div/div/div[1]"
# 任务名称
SCAN_TASK_NAME = "//label[contains(text(),'任务名称')]/../div/div/div/input"
# 制品类型
GENERIC_PATH = "//label[contains(text(),'制品类型')]/../div/div/div/div/div[contains(text(),'Generic')]/.."
DOCKER_PATH = "//label[contains(text(),'制品类型')]/../div/div/div/div/div[contains(text(),'Docker')]/.."
# 制品路径
ARTIFACT_WAREHOUSE = "//td[1]/div/div/div/div/div/input"
ARTIFACT_NAME = "//td[2]/div/div/div/div/div/input"
ARTIFACT_VERSION = "//td[3]/div/div/div/div/div/input"
ARTIFACT_PATH = "//td[4]/div/div/div/div/div/input"
# 选择下拉框
CHOOSE_DROPDOWN = "//div[@x-placement='bottom-start']/div/div/ul/li[1]"
# 质量门禁
QUALITY_CONTROL = "//label[contains(text(),'质量门禁')]/../div/div/div"
# 门禁等级
SERIOUS_LEVEL = "//span[contains(text(),'严重')]/../../../../../td[3]/div/div/div/div/div/input"
HIGH_RISK_LEVEL = "//span[contains(text(),'高危')]/../../../../../td[3]/div/div/div/div/div/input"
MODERATE_RISK_LEVEL = "//span[contains(text(),'中危')]/../../../../../td[3]/div/div/div/div/div/input"
LOW_RISK_LEVEL = "//span[contains(text(),'低危')]/../../../../../td[3]/div/div/div/div/div/input"
UNRATED_LEVEL = "//span[contains(text(),'未定级')]/../../../../../td[3]/div/div/div/div/div/input"
# 仅保存按钮
SAVE_ONLY_BUTTON = "//span[contains(text(),'仅保存')]/.."
# 保存并立即执行
SAVE_AND_EXECUTE_BUTTON = "//span[contains(text(),'保存并立即执行')]/.."
# 搜索框任务来源
TASK_SOURCE_IN_SEARCH_BOX = "//input[@placeholder='请选择任务来源']"
# 搜索框输入关键字
ENTER_KEYWORDS_IN_SEARCH_BOX = "//input[@placeholder='请输入任务名称、仓库名称搜索']"
# 搜索框制品类型
PRODUCT_TYPE_IN_SEARCH_BOX = "//input[@placeholder='请选择制品类型']"
# 点击执行扫描任务
EXECUTE_SCAN_TASK = "(//span[contains(text(),'执行')])[3]/.."
# 点击编辑扫描任务
EDIT_SCAN_TASK = "(//span[contains(text(),'编辑')])[3]/.."
# 点击删除扫描任务
DELETE_SCAN_TASK = "(//span[contains(text(),'删除')])[3]/.."
# 代码扫描定位---------------------------------------
# 代码扫描下子目录
CODE_SACN_TASK = "(//p[contains(text(),'代码扫描')]/../../../../div/div/div/div/div/button)[1]"
CODE_SACN_PLAN = "(//p[contains(text(),'代码扫描')]/../../../../div/div/div/div/div/button)[2]"
CODE_SACN_UNIT = "(//p[contains(text(),'代码扫描')]/../../../../div/div/div/div/div/button)[3]"
FIlTER_CONFIGURATION = "(//p[contains(text(),'代码扫描')]/../../../../div/div/div/div/div/button)[4]"
# 新建按钮
# CODE_SCAN_PLAN_CREATE = "//*[@id='app']/div/section/div/main/div/div[1]/div[1]/button"
# 方案名称
CODE_SCAN_PLAN_NAME = "//input[@placeholder='请输入方案名称']"
# 方案描述
CODE_SCAN_PLAN_DESCRIPTION = "//input[@placeholder='请输入方案描述']"
# 设为默认
CODE_PLAN_STE_DEFAULT = "//label[contains(text(),'设为默认')]/../div/div"
# 确定按钮
CODE_PLAN_CONFIRM_BUTTON = "//span[contains(text(),'确 定')]/.."
# 搜索方案名称
CODE_SCAN_PLAN_SEARCH_ELE = "//input[@placeholder='搜索方案名称']"
# 方案列表第一个
CODE_SCAN_PLAN_FIRST = "//*[@id='app']/div/section/div/main/div/div[1]/div[2]/ul/li[1]"
# 编译/过滤配置tab
CODE_SCAN_PLAN_FILTER_CONFIG_TAB = "//div[contains(text(),'编译 / 过滤配置')]"
# 删除方案
DELETE_SCAN_PLAN = "//*[@id='app']/div/section/div/main/div/div[1]/div[2]/ul/li/div[2]/div[1]/div[2]/i"
# 扫描任务
# 扫描任务方案名称
CODE_SCAN_TASK_PLAN_NAME = "//label[contains(text(),'方案名称')]/../div/div/div/input"
# 扫描任务名称
CODE_SCAN_TASK_NAME = "//label[contains(text(),'任务名称')]/../div/div/input"
# 扫描任务关联应用
CODE_SCAN_TASK_APP = "//label[contains(text(),'应用名称')]/../div/div/div/input"
# 扫描应用选择分支
CODE_SCAN_TASK_BRANCH = "//label[contains(text(),'分支')]/../div/div/div/input"
# 扫描模式
SCAN_MODE_FULL = "//span[contains(text(),'全量')]/.."
SCAN_MODE_INCREMENTAL = "//span[contains(text(),'增量')]/.."
# 任务过滤路径
CODE_SCAN_TASK_FILTER_PATH = "(//*[@id='app']/div/section/div/main/div/div[2]/div/div/section/div/div[2]/div[1]/form/div/div/div/div[1]/div/div[3]/table/tbody/tr/td[2]/div/div/div/div/div/input)"
# 扫描任务
CODE_SCAN_TASK_SEARCH = "//input[@placeholder='请输入关键字搜索']"
# 扫描应用点击时间范围
CODE_SCAN_TASK_TIME = "(//input[@placeholder='开始日期'])[2]"
CODE_SCAN_TASK_TIME_RANGE = "//button[contains(text(),'最近三个月')]"
# 扫描应用点击基线版本
CODE_SCAN_TASK_BASIC_VERSION_BUTTON = "//label[contains(text(),'基线版本')]/../div/div/div/input"
CODE_SCAN_TASK_BASIC_VERSION = "(//div[@class='v-modal']/../div/div/div/ul/li[2]/div/div/span[contains(text(),'提交')]/../../..)"
# 扫描应用点击比较版本
CODE_SCAN_TASK_COMPARE_VERSION_BUTTON = "//label[contains(text(),'比较版本')]/../div/div/div/input"
CODE_SCAN_TASK_COMPARE_VERSION = "(//div[@class='v-modal']/../div/div/div/ul/li[1]/div/div/span[contains(text(),'提交')]/../../..)[2]"
# 质量门禁按钮
CODE_SCAN_TASK_QUALITY_BUTTON = "//label[contains(text(),'质量门禁')]/../div/div"
# 质量门禁阻塞等级
QUALITY_GATES_BLOCKING = "//span[contains(text(),'阻塞')]/../../../../../td[3]/div/div/div/div/div/input"
QUALITY_GATES_SERIOUS = "//span[contains(text(),'严重')]/../../../../../td[3]/div/div/div/div/div/input"
QUALITY_GATES_PRIMARY = "//span[contains(text(),'主要')]/../../../../../td[3]/div/div/div/div/div/input"
QUALITY_GATES_SECONDARY = "//span[contains(text(),'次要')]/../../../../../td[3]/div/div/div/div/div/input"
# 过滤配置
VIEEW_FILTER_CONFIG = "//span[contains(text(),'查看所有过滤配置')]/.."
CLOSE_FILTER_CONFIG = "//span[contains(text(),'过滤配置')]/../button"
# pdf设置
GENERATE_PDF = "//label[contains(text(),'生成PDF报告')]/../div/div"
# 过滤配置
FILTER_CONFIG_CREATE = "//*[@id='app']/div/section/div/main/div/div[1]/div[1]/div/button"
# 配置描述
FILTER_DESCRIPTION = "//textarea[@placeholder='请输入描述']"
# 应用选择框
CHOOSE_APP = "(//input[@placeholder='请选择'])[1]"
# 静态扫描tab
STATIC_SCAN_TAB = "//div[contains(text(),'静态扫描')]"
# 单元测试tab
UNIT_TEST_TAB = "//div[contains(text(),'单元测试')]"
# 单元测试添加按钮
UNIT_TEST_ADD = "(//span[contains(text(),'添加')]/..)[2]"
# 过滤路径base
FILTER_PATH_BASE = "(//div[contains(text(),'排除')]/../../../../../../td[2]/div/div/div/div/div/input)"
# 保存配置
SAVE_FILETR = "//span[contains(text(),'保存配置')]/.."
# 应用配置存在提示校验
APPLICATION_CONFIG_EXIST = "//p[contains(text(),'该应用的配置已存在！')]"
# 查询配置
QUERY_FILETR = "//*[@id='app']/div/section/div/main/div/div[1]/div[1]/div[1]/div/div[1]/input"
# 删除配置
DELETE_FILETR = "//*[@id='app']/div/section/div/main/div/div[1]/div[1]/div[2]/ul/li/div[2]/div[1]/div[2]/i"
# 项目管理定位---------------------------------------
PROJECT_INPUT = "//input[@placeholder='请输入名称/编号']"
PROJECT_QUERY = ""
PROJECT_OVERVIEW = "(//div[@class='simplebar-content'])[2]/nav/div/div[1]"
