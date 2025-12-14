from config.contants import ADD_VULN_IDS


class XPathBuilder:
    """XPath表达式构建工具类"""
    
    @staticmethod
    def build_app_option_xpath(index):
        """构建应用选项的XPath表达式"""
        return f"//div[@class='v-modal']/../div/div/div/ul/li/span[contains(text(),'{index}')]/.."

    @staticmethod
    def build_vuln_id_xpath(index):
        """构建漏洞编号输入框XPath表达式"""
        return f"{ADD_VULN_IDS}[{index}]"

    @staticmethod
    def build_choose_language_xpath(index):
        """构建选择语言的XPath表达式"""
        return f"//div[contains(text(),'{index}')]/../div[2]/div[1]/input"

    @staticmethod
    def build_choose_sonar_way_xpath(index):
        """构建选择Sonar way的XPath表达式"""
        return f"(//span[contains(text(),'Sonar way')]/..)[{index}]"

    @staticmethod
    def build_delete_filter_xpath(index):
        """构建删除过滤路径的XPath表达式"""
        return f"//*[@id='pane-filterSetting']/form/div/div[1]/div/div[3]/table/tbody/tr[{index}]/td[3]/div/div/div/a"

    @staticmethod
    def build_choose_filter_xpath(index):
        """构建选择应用的过滤配置的XPath表达式"""
        return f"//div[@id='root']/../div/div/div/ul/li/span[contains(text(),'{index}')]/.."

    @staticmethod
    def build_static_delete_filter_xpath(index):
        """构建静态扫描删除过滤路径的XPath表达式"""
        return f"//div[@id='pane-staticScan']/div/div/div/div[3]/table/tbody/tr[{index}]/td[3]/div/div/div/a"

    @staticmethod
    def build_unit_delete_filter_xpath(index):
        """构建单元测试删除过滤路径的XPath表达式"""
        return f"//div[@id='pane-unitTest']/div/div/div/div[3]/table/tbody/tr[{index}]/td[3]/div/div/div/a"

    @staticmethod
    def build_plan_option_xpath(index):
        """构建方案选项的XPath表达式"""
        return f"//li/span[contains(text(),'{index}')]/.."

    # @staticmethod
    # def build_app_option_xpath(index):
    #     """构建应用选项的XPath表达式"""
    #     return f"//span[contains(text(),'{index}')]/.."