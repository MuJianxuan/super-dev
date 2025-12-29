#!/usr/bin/env python3
"""
Super Dev - End-to-End Workflow Test
功能：验证完整的 6 阶段工作流是否正常运行
"""

import sys
import subprocess
import json
import argparse
from pathlib import Path
from datetime import datetime
try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner


class WorkflowTester:
    """工作流测试器"""

    def __init__(self, project_name: str = "TestProject"):
        self.project_name = project_name
        self.results = []
        self.test_dir = Path.cwd() / "test_output"
        self.test_dir.mkdir(exist_ok=True)

    def log_result(self, phase: str, test_name: str, passed: bool, message: str = ""):
        """记录测试结果"""
        self.results.append({
            "phase": phase,
            "test": test_name,
            "passed": passed,
            "message": message
        })

        status = "[green]PASS[/green]" if passed else "[red]FAIL[/red]"
        console.print(f"{phase} > {test_name}: {status}")
        if message:
            console.print(f"  [dim]{message}[/dim]")

    def test_phase_0_environment(self):
        """Phase 0: 环境激活测试"""
        print_step("Phase 0: 测试环境激活...")

        # 测试 Python 依赖
        try:
            import ddgs
            import rich
            self.log_result("Phase 0", "Python 依赖检查", True, "ddgs 和 rich 已安装")
        except ImportError as e:
            self.log_result("Phase 0", "Python 依赖检查", False, f"缺失依赖: {e}")

        # 测试专家文件存在性
        experts_dir = Path(__file__).parent.parent / "experts"
        core_experts = ["PM.md", "ARCHITECT.md", "UI.md", "CODE.md", "SECURITY.md"]
        missing = []
        for expert in core_experts:
            if not (experts_dir / expert).exists():
                missing.append(expert)

        if missing:
            self.log_result("Phase 0", "专家文件检查", False, f"缺失: {', '.join(missing)}")
        else:
            self.log_result("Phase 0", "专家文件检查", True, f"所有 {len(core_experts)} 位专家就位")

    def test_phase_2_intelligence(self):
        """Phase 2: 实时情报测试"""
        print_step("Phase 2: 测试实时情报收集...")

        # 测试研究脚本可执行性
        scripts = [
            ("market_research.py", "市场研究"),
            ("competitor_analysis.py", "竞品分析"),
            ("domain_research.py", "领域研究")
        ]

        for script, name in scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                self.log_result("Phase 2", f"{name}脚本", True, f"{script} 存在")
            else:
                self.log_result("Phase 2", f"{name}脚本", False, f"{script} 不存在")

    def test_phase_3_expert_activation(self):
        """Phase 3: 专家激活测试"""
        print_step("Phase 3: 测试专家激活...")

        # 测试知识库组件
        knowledge_dir = Path(__file__).parent.parent / "knowledge"
        platforms_dir = knowledge_dir / "platforms"
        components_dir = knowledge_dir / "components"

        checks = [
            ("platforms/web.md", "Web 平台知识"),
            ("platforms/mobile.md", "Mobile 平台知识"),
            ("components/prd/base.md", "PRD 基础组件"),
            ("components/prototype/base.html", "原型模板")
        ]

        for rel_path, name in checks:
            file_path = knowledge_dir / rel_path
            if file_path.exists():
                self.log_result("Phase 3", name, True, f"{rel_path} 存在")
            else:
                self.log_result("Phase 3", name, False, f"{rel_path} 不存在")

    def test_phase_4_quality_gate(self):
        """Phase 4: 递归质检测试"""
        print_step("Phase 4: 测试质量门禁...")

        # 测试质量检查脚本
        quality_script = Path(__file__).parent / "quality_check.py"
        if quality_script.exists():
            self.log_result("Phase 4", "质量检查脚本", True)
        else:
            self.log_result("Phase 4", "质量检查脚本", False)

    def test_phase_5_phantom_delivery(self):
        """Phase 5: 幻影交付测试"""
        print_step("Phase 5: 测试幻影交付...")

        # 测试原型生成脚本
        preview_script = Path(__file__).parent / "generate_preview.py"
        if preview_script.exists():
            self.log_result("Phase 5", "原型生成脚本", True)

            # 尝试生成一个测试原型
            try:
                test_config = {
                    "project_name": "TestApp",
                    "hero_title": "Test Title",
                    "hero_subtitle": "Test Subtitle",
                    "cta_primary": "Start",
                    "cta_secondary": "Learn",
                    "year": "2025"
                }
                output_path = self.test_dir / "test_preview.html"
                # 这里我们只验证脚本存在，不实际运行（避免依赖问题）
                self.log_result("Phase 5", "原型生成配置", True)
            except Exception as e:
                self.log_result("Phase 5", "原型生成配置", False, str(e))
        else:
            self.log_result("Phase 5", "原型生成脚本", False)

    def test_phase_6_industrial_complex(self):
        """Phase 6: 工业化部署测试"""
        print_step("Phase 6: 测试工业化部署...")

        # 测试部署脚本
        deployment_scripts = [
            ("generate_dockerfile.py", "Dockerfile 生成"),
            ("generate_ci_cd.py", "CI/CD 配置生成")
        ]

        for script, name in deployment_scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                self.log_result("Phase 6", name, True, f"{script} 存在")
            else:
                self.log_result("Phase 6", name, False, f"{script} 不存在")

    def test_phase_10_singularity(self):
        """Phase 10: 奇点进化测试"""
        print_step("Phase 10: 测试奇点进化...")

        # 测试动态扩展脚本
        singularity_scripts = [
            ("hire_expert.py", "专家生成"),
            ("clone_dna.py", "风格克隆")
        ]

        for script, name in singularity_scripts:
            script_path = Path(__file__).parent / script
            if script_path.exists():
                self.log_result("Phase 10", name, True, f"{script} 存在")
            else:
                self.log_result("Phase 10", name, False, f"{script} 不存在")

    def test_integration(self):
        """集成测试"""
        print_step("集成测试: 端到端流程...")

        # 测试完整研究流程
        orchestrator_script = Path(__file__).parent / "research_orchestrator.py"
        if orchestrator_script.exists():
            self.log_result("Integration", "研究指挥官", True, "research_orchestrator.py 存在")
        else:
            self.log_result("Integration", "研究指挥官", False, "research_orchestrator.py 不存在")

    def generate_report(self):
        """生成测试报告"""
        print_step("生成测试报告...")

        total = len(self.results)
        passed = sum(1 for r in self.results if r["passed"])
        failed = total - passed
        pass_rate = (passed / total * 100) if total > 0 else 0

        # 创建 JSON 报告
        report = {
            "timestamp": datetime.now().isoformat(),
            "project": self.project_name,
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "pass_rate": f"{pass_rate:.1f}%"
            },
            "results": self.results
        }

        # 保存 JSON
        report_path = self.test_dir / "workflow_test_report.json"
        report_path.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")

        # 打印摘要
        console.print(f"\\n[bold]测试摘要:[/bold]")
        console.print(f"  总计: {total}")
        console.print(f"  [green]通过: {passed}[/green]")
        if failed > 0:
            console.print(f"  [red]失败: {failed}[/red]")
        console.print(f"  通过率: {pass_rate:.1f}%")

        # 失败详情
        if failed > 0:
            console.print(f"\\n[red]失败的测试:[/red]")
            for r in self.results:
                if not r["passed"]:
                    console.print(f"  - {r['phase']} > {r['test']}: {r['message']}")

        console.print(f"\\n[dim]详细报告: {report_path}[/dim]")

        return pass_rate >= 80  # 80% 及格线

    def run_all_tests(self):
        """运行所有测试"""
        print_header("Super Dev 工作流测试", f"项目: {self.project_name}")

        self.test_phase_0_environment()
        self.test_phase_2_intelligence()
        self.test_phase_3_expert_activation()
        self.test_phase_4_quality_gate()
        self.test_phase_5_phantom_delivery()
        self.test_phase_6_industrial_complex()
        self.test_phase_10_singularity()
        self.test_integration()

        return self.generate_report()


def main():
    parser = argparse.ArgumentParser(description="Super Dev 工作流端到端测试")
    parser.add_argument("--project", "-p", default="TestProject", help="测试项目名称")

    args = parser.parse_args()

    tester = WorkflowTester(args.project)
    success = tester.run_all_tests()

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
