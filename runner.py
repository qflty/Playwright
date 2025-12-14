import argparse
import subprocess
import pytest
import os
import sys
from api.core.test_runner import TestRunner
from utils.logger import logger
from pathlib import Path
from config.config import config


def run_ui_tests(args):
    """运行UI测试"""
    logger.info("运行UI测试...")
    
    # 获取项目根目录（脚本所在目录）
    project_root = Path(__file__).resolve().parent
    # 测试报告目录
    report_dir = project_root / "reports/ui_reports"
    if not os.path.exists(report_dir):
        os.makedirs(report_dir)

    test_case_path = config.ui.test_case_path
    if not os.path.exists(test_case_path):
        logger.error(f"未找到测试用例路径: {test_case_path}")
        sys.exit(1)
    else:
        # 构建pytest参数
        pytest_args = [
            test_case_path,
            "-s",  # 显示标准输出
            "-v",  # 详细输出
            "--alluredir", str(report_dir),  # Allure报告输出目录
            "--clean-alluredir"  # 清理旧报告
        ]
    
    # 添加测试用例路径
    if args.file:
        pytest_args.insert(0, args.file)
    else:
        # 默认运行所有UI测试
        pytest_args.insert(0, "ui/test_cases")
        
    # 添加标签过滤
    if args.mark:
        pytest_args.extend(["-m", args.mark])
        
    # 添加关键字过滤
    if args.keyword:
        pytest_args.extend(["-k", args.keyword])
    
    logger.info(f"运行测试命令: pytest {' '.join(pytest_args)}")
    exit_code = pytest.main(pytest_args)
    logger.info(f"UI测试执行完毕，退出码: {exit_code}")

    # 生成Allure HTML报告
    allure_path = config.allure_path
    if not os.path.exists(allure_path):
        logger.error(f"未找到Allure命令行工具: {allure_path}")
        sys.exit(1)
    try:
        result = subprocess.run([
            allure_path, 
            "generate", 
            str(report_dir), 
            "-o", 
            str(report_dir / "html"), 
            "--clean"
        ], check=True,
        cwd=os.path.dirname(os.path.abspath(__file__)),  # 指定工作目录
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        logger.info(f"Allure命令成功执行")
        report_path = os.path.abspath(f'{report_dir}/html/index.html')
        logger.info(f"Allure HTML报告已生成: {report_path}")
        return report_path
    except subprocess.CalledProcessError as e:
        logger.error(f"Allure命令执行失败: {e.stderr}")
        logger.info(f"返回码: {e.returncode}")
        logger.info(f"可以手动执行: allure generate {report_dir} -o {report_dir}/html --clean")
    except FileNotFoundError:
        logger.error("未找到Allure命令行工具，请确保已安装并添加到PATH")
        logger.info("安装指南: https://docs.qameta.io/allure/#_installing_a_commandline")
    return None


def run_api_tests(args):
    """运行API测试"""
    logger.info("运行API测试...")
    
    # 确定测试用例文件
    if args.file:
        test_file = args.file
        if not os.path.exists(test_file):
            logger.error(f"指定的测试用例文件不存在: {test_file}")
            return
    else:
        test_cases_dir = config.api.test_cases_dir
        # 默认查找测试用例目录下的Excel文件
        excel_files = [f for f in os.listdir(test_cases_dir) if f.endswith(('.xlsx', '.xls'))]
        if not excel_files:
            logger.error(f"在 {test_cases_dir} 目录下未找到任何Excel测试用例文件")
            return
        test_file = os.path.join(test_cases_dir, excel_files[0])
        logger.info(f"未指定测试用例文件，使用默认文件: {test_file}")

    # 执行测试
    try:
        test_runner = TestRunner(test_file)
        result_summary = test_runner.run_all_tests(module=args.module)
        test_runner.close()
        # 输出测试 summary
        logger.info("\n" + "="*50)
        logger.info("API测试执行完毕")
        logger.info("="*50)
        logger.info(f"总用例数: {result_summary['total']}")
        logger.info(f"通过用例: {result_summary['passed']}")
        logger.info(f"失败用例: {result_summary['failed']}")
        logger.info(f"总耗时: {result_summary['total_time']}ms")
        logger.info(f"测试报告: {result_summary['report_path']}")
        logger.info("="*50)
        return result_summary['report_path']
    except Exception as e:
        logger.error(f"执行测试时发生错误: {str(e)}", exc_info=True)
        return None


def parse_args():
    """解析命令行参数"""
    parser = argparse.ArgumentParser(description='自动化测试框架')
    parser.add_argument('type', choices=['ui', 'api', 'both'], help='测试类型: ui/api/both')
    parser.add_argument('--env', default='test', help='测试环境: dev/test/prod (默认: test)')
    parser.add_argument('--file', help='测试用例文件路径')
    parser.add_argument('--module', help='指定测试模块 (仅API测试)')
    parser.add_argument('--mark', help='运行指定标签的测试用例 (仅UI测试)')
    parser.add_argument('--keyword', help='通过关键字过滤测试用例 (仅UI测试)')
    return parser.parse_args()


def main():
    """主函数"""
    # 打印配置值，验证是否正确加载
    logger.info("当前使用的配置:")
    for key, value in config.get_dict().items():
        logger.info(f"{key}: {value}")
    
    logger.info("开始执行测试...")
    
    # 解析命令行参数
    args = parse_args()
    
    # 根据测试类型运行对应测试
    report_paths = []  # 定义列表来存储多个报告路径
    if args.type == "both":
        # 同时运行UI和API测试
        ui_report_path = run_ui_tests(args)
        api_report_path = run_api_tests(args)
        report_paths.extend([ui_report_path, api_report_path])
    elif args.type == "ui":
        report_paths.append(run_ui_tests(args))
    elif args.type == "api":
        report_paths.append(run_api_tests(args))
    else:
        logger.error(f"无效的测试类型: {args.type}")
        sys.exit(1)

    # 打印所有报告路径
    for report_path in report_paths:
        if report_path:
            logger.info(f"测试报告已生成: {report_path}")
        else:
            logger.warning("测试报告生成失败")


if __name__ == "__main__":
    main()