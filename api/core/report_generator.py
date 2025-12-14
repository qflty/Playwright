import os
from datetime import datetime
from utils.file_utils import FileUtils
from utils.logger import logger
from config.config import config

class ReportGenerator:
    """测试报告生成器"""

    def __init__(self):
        # 确保报告目录存在
        FileUtils.ensure_dir_exists(config.api.report_dir)

    def generate_html_report(self, results, total, passed, failed, total_time):
        """
        生成HTML格式的测试报告
        :param results: 测试结果列表
        :param total: 总用例数
        :param passed: 通过用例数
        :param failed: 失败用例数
        :param total_time: 总耗时(ms)
        :return: 报告文件路径
        """
        try:
            # 生成报告文件名
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            report_filename = f"report_{timestamp}.html"
            report_title = config.api.report_title
            report_path = os.path.join(config.api.report_dir, report_filename)

            # 计算通过率
            pass_rate = round(passed / total * 100, 2) if total > 0 else 0

            # 生成HTML内容
            html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{report_title}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 20px; background-color: #f5f5f5; }}
        .report-container {{ max-width: 1200px; margin: 0 auto; background-color: white; padding: 20px; border-radius: 5px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }}
        .report-header {{ text-align: center; margin-bottom: 30px; }}
        .summary {{ display: flex; justify-content: space-around; margin-bottom: 30px; text-align: center; }}
        .summary-item {{ padding: 15px; border-radius: 5px; flex: 1; margin: 0 10px; }}
        .total {{ background-color: #e3f2fd; }}
        .passed {{ background-color: #e8f5e9; }}
        .failed {{ background-color: #ffebee; }}
        .time {{ background-color: #fff8e1; }}
        .results-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        .results-table th, .results-table td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        .results-table th {{ background-color: #f2f2f2; }}
        .results-table tr:nth-child(even) {{ background-color: #f9f9f9; }}
        .results-table tr:hover {{ background-color: #f5f5f5; }}
        .status-passed {{ color: green; font-weight: bold; }}
        .status-failed {{ color: red; font-weight: bold; }}
        .details {{ white-space: pre-wrap; word-wrap: break-word; }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-header">
            <h1>{report_title}</h1>
            <p>生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>

        <div class="summary">
            <div class="summary-item total">
                <h3>总用例数</h3>
                <p style="font-size: 24px;">{total}</p>
            </div>
            <div class="summary-item passed">
                <h3>通过用例</h3>
                <p style="font-size: 24px; color: green;">{passed}</p>
            </div>
            <div class="summary-item failed">
                <h3>失败用例</h3>
                <p style="font-size: 24px; color: red;">{failed}</p>
            </div>
            <div class="summary-item time">
                <h3>通过率</h3>
                <p style="font-size: 24px;">{pass_rate}%</p>
            </div>
            <div class="summary-item time">
                <h3>总耗时</h3>
                <p style="font-size: 24px;">{total_time}ms</p>
            </div>
        </div>

        <h2>测试结果详情</h2>
        <table class="results-table">
            <tr>
                <th>用例ID</th>
                <th>用例名称</th>
                <th>接口ID</th>
                <th>开始时间</th>
                <th>结束时间</th>
                <th>响应时间(ms)</th>
                <th>状态码</th>
                <th>测试结果</th>
                <th>错误信息</th>
                <th>断言结果</th>
            </tr>
        """

            # 添加测试结果行
            for result in results:
                status_class = "status-passed" if result['测试结果'] == '通过' else "status-failed"
                # 添加依赖用例标识
                case_type = " (依赖用例)" if result.get('是否依赖用例', False) else ""
                html_content += f"""
            <tr>
                <td>{result['用例ID']}{case_type}</td>
                <td>{result['用例名称']}</td>
                <td>{result['接口ID']}</td>
                <td>{result['开始时间']}</td>
                <td>{result['结束时间']}</td>
                <td>{result['响应时间(ms)']}</td>
                <td>{result['状态码']}</td>
                <td class="{status_class}">{result['测试结果']}</td>
                <td class="details">{result['错误信息']}</td>
                <td class="details">{result['断言结果']}</td>
            </tr>
                """

            # 结束HTML内容
            html_content += """
        </table>
    </div>
</body>
</html>
            """

            # 写入文件
            with open(report_path, 'w', encoding='utf-8') as f:
                f.write(html_content)

            logger.info(f"HTML测试报告已生成: {report_path}")
            return report_path

        except Exception as e:
            logger.error(f"生成HTML报告失败: {str(e)}")
            return None