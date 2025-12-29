# -*- coding: utf-8 -*-
"""
开发：Excellent（11964948@qq.com）
功能：工作流编排引擎 - 协调 6 阶段工作流
作用：管理任务执行、专家调度、质量门禁
创建时间：2025-12-30
最后修改：2025-12-30
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import Any, Callable, Optional
from dataclasses import dataclass, field
from enum import Enum

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeElapsedColumn
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from ..config.manager import ConfigManager, get_config_manager


class Phase(Enum):
    """工作流阶段"""
    DISCOVERY = "discovery"
    INTELLIGENCE = "intelligence"
    DRAFTING = "drafting"
    REDTEAM = "redteam"
    QA = "qa"
    DELIVERY = "delivery"
    DEPLOYMENT = "deployment"


@dataclass
class PhaseResult:
    """阶段执行结果"""
    phase: Phase
    success: bool
    duration: float
    output: Any = None
    errors: list = field(default_factory=list)
    quality_score: float = 0.0


@dataclass
class WorkflowContext:
    """工作流上下文"""
    project_dir: Path
    config: ConfigManager
    results: dict = field(default_factory=dict)
    metadata: dict = field(default_factory=dict)

    # 共享数据
    user_input: dict = field(default_factory=dict)
    research_data: dict = field(default_factory=dict)
    documents: dict = field(default_factory=dict)
    quality_reports: dict = field(default_factory=dict)


class WorkflowEngine:
    """工作流编排引擎"""

    def __init__(self, project_dir: Optional[Path] = None):
        """
        初始化工作流引擎

        Args:
            project_dir: 项目目录
        """
        self.project_dir = Path.cwd() if project_dir is None else project_dir
        self.config_manager = get_config_manager(self.project_dir)
        self.console = Console() if RICH_AVAILABLE else None

        # 阶段注册表
        self._phase_handlers: dict[Phase, Callable] = {}

        # 注册默认阶段处理器
        self._register_default_handlers()

    def _register_default_handlers(self) -> None:
        """注册默认阶段处理器"""
        # 这些方法将在后续实现中连接到实际的 Python 脚本
        self._phase_handlers[Phase.DISCOVERY] = self._phase_discovery
        self._phase_handlers[Phase.INTELLIGENCE] = self._phase_intelligence
        self._phase_handlers[Phase.DRAFTING] = self._phase_drafting
        self._phase_handlers[Phase.REDTEAM] = self._phase_redteam
        self._phase_handlers[Phase.QA] = self._phase_qa
        self._phase_handlers[Phase.DELIVERY] = self._phase_delivery
        self._phase_handlers[Phase.DEPLOYMENT] = self._phase_deployment

    def register_phase_handler(self, phase: Phase, handler: Callable) -> None:
        """
        注册自定义阶段处理器

        Args:
            phase: 阶段
            handler: 处理函数
        """
        self._phase_handlers[phase] = handler

    async def run(
        self,
        phases: Optional[list[Phase]] = None,
        context: Optional[WorkflowContext] = None
    ) -> dict[Phase, PhaseResult]:
        """
        运行工作流

        Args:
            phases: 要执行的阶段列表，默认执行全部
            context: 工作流上下文

        Returns:
            各阶段执行结果
        """
        # 初始化上下文
        if context is None:
            context = WorkflowContext(
                project_dir=self.project_dir,
                config=self.config_manager
            )

        # 确定要执行的阶段
        if phases is None:
            phases = self._get_phases_from_config()

        results = {}

        # 打印工作流开始
        self._print_workflow_start(phases)

        # 执行各阶段
        for phase in phases:
            result = await self._run_phase(phase, context)
            results[phase] = result

            # 质量门禁检查
            if not result.success:
                self._print_phase_failed(phase, result)
                break

            if result.quality_score < self.config_manager.config.quality_gate:
                self._print_quality_gate_failed(phase, result)
                break

            self._print_phase_complete(phase, result)

        # 打印工作流完成
        self._print_workflow_complete(results)

        # 保存执行报告
        self._save_report(results)

        return results

    def _get_phases_from_config(self) -> list[Phase]:
        """从配置获取要执行的阶段"""
        config_phases = self.config_manager.config.phases
        phases = []
        phase_map = {
            "discovery": Phase.DISCOVERY,
            "intelligence": Phase.INTELLIGENCE,
            "drafting": Phase.DRAFTING,
            "redteam": Phase.REDTEAM,
            "qa": Phase.QA,
            "delivery": Phase.DELIVERY,
            "deployment": Phase.DEPLOYMENT,
        }
        for p in config_phases:
            if p in phase_map:
                phases.append(phase_map[p])
        return phases

    async def _run_phase(self, phase: Phase, context: WorkflowContext) -> PhaseResult:
        """
        执行单个阶段

        Args:
            phase: 阶段
            context: 上下文

        Returns:
            阶段执行结果
        """
        start_time = datetime.now()

        try:
            # 获取阶段处理器
            handler = self._phase_handlers.get(phase)
            if handler is None:
                raise ValueError(f"No handler registered for phase: {phase}")

            # 执行阶段
            output = await self._execute_handler(handler, context)

            duration = (datetime.now() - start_time).total_seconds()

            return PhaseResult(
                phase=phase,
                success=True,
                duration=duration,
                output=output,
                quality_score=self._calculate_quality_score(phase, context)
            )

        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            return PhaseResult(
                phase=phase,
                success=False,
                duration=duration,
                errors=[str(e)]
            )

    async def _execute_handler(self, handler: Callable, context: WorkflowContext) -> Any:
        """执行处理器（支持同步和异步）"""
        if asyncio.iscoroutinefunction(handler):
            return await handler(context)
        else:
            return handler(context)

    def _calculate_quality_score(self, phase: Phase, context: WorkflowContext) -> float:
        """计算质量分数"""
        # 这里应该调用质量检查脚本
        # 暂时返回默认分数
        return 85.0

    # ==================== 阶段处理器 ====================

    async def _phase_discovery(self, context: WorkflowContext) -> Any:
        """Phase 0: 发现阶段 - 需求 intake"""
        from ...skills.super_dev.scripts.init_project import initialize_project
        # 这里会调用 init_project.py
        return {"status": "requirements_collected"}

    async def _phase_intelligence(self, context: WorkflowContext) -> Any:
        """Phase 2: 情报阶段 - 市场研究、竞品分析"""
        # 这里会调用 market_research.py, competitor_analysis.py, domain_research.py
        return {"status": "intelligence_collected"}

    async def _phase_drafting(self, context: WorkflowContext) -> Any:
        """Phase 3: 起草阶段 - 专家协作生成文档"""
        # 这里会调用专家系统生成 PRD、架构、UI 等
        return {"status": "documents_generated"}

    async def _phase_redteam(self, context: WorkflowContext) -> Any:
        """Phase 4: 红队阶段 - 质量检查"""
        # 这里会调用 quality_check.py
        return {"status": "review_complete"}

    async def _phase_qa(self, context: WorkflowContext) -> Any:
        """Phase 5: QA 阶段 - 质量门禁"""
        # 这里会进行最终质量检查
        return {"status": "qa_passed"}

    async def _phase_delivery(self, context: WorkflowContext) -> Any:
        """Phase 6: 交付阶段 - 幻影交付"""
        # 这里会调用 generate_preview.py
        return {"status": "preview_generated"}

    async def _phase_deployment(self, context: WorkflowContext) -> Any:
        """Phase 7: 部署阶段 - 工业化部署"""
        # 这里会调用 generate_dockerfile.py, generate_ci_cd.py
        return {"status": "deployment_ready"}

    # ==================== 打印方法 ====================

    def _print_workflow_start(self, phases: list[Phase]) -> None:
        """打印工作流开始"""
        if self.console:
            self.console.print(Panel.fit(
                f"[bold cyan]Super Dev 工作流引擎[/bold cyan]\n\n"
                f"项目: {self.config_manager.config.name}\n"
                f"阶段: {len(phases)} 个",
                title="启动"
            ))

    def _print_phase_complete(self, phase: Phase, result: PhaseResult) -> None:
        """打印阶段完成"""
        if self.console:
            self.console.print(
                f"[green]✓[/green] {phase.value}: "
                f"完成 ({result.duration:.1f}s, 质量分: {result.quality_score:.0f})"
            )

    def _print_phase_failed(self, phase: Phase, result: PhaseResult) -> None:
        """打印阶段失败"""
        if self.console:
            self.console.print(
                f"[red]✗[/red] {phase.value}: "
                f"失败 ({', '.join(result.errors)})"
            )

    def _print_quality_gate_failed(self, phase: Phase, result: PhaseResult) -> None:
        """打印质量门禁失败"""
        if self.console:
            gate = self.config_manager.config.quality_gate
            self.console.print(
                f"[yellow]⚠[/yellow] {phase.value}: "
                f"质量分 ({result.quality_score:.0f}) 低于门禁 ({gate})"
            )

    def _print_workflow_complete(self, results: dict[Phase, PhaseResult]) -> None:
        """打印工作流完成"""
        if self.console:
            # 创建结果表格
            table = Table(title="工作流执行结果")
            table.add_column("阶段", style="cyan")
            table.add_column("状态", style="green")
            table.add_column("耗时", style="yellow")
            table.add_column("质量分", style="magenta")

            total_duration = 0
            success_count = 0

            for phase, result in results.items():
                status = "[green]成功[/green]" if result.success else "[red]失败[/red]"
                duration = f"{result.duration:.1f}s"
                quality = f"{result.quality_score:.0f}"

                table.add_row(phase.value, status, duration, quality)

                total_duration += result.duration
                if result.success:
                    success_count += 1

            self.console.print(table)
            self.console.print(
                f"\n总计: {success_count}/{len(results)} 成功, "
                f"总耗时: {total_duration:.1f}s"
            )

    def _save_report(self, results: dict[Phase, PhaseResult]) -> None:
        """保存执行报告"""
        output_dir = self.project_dir / self.config_manager.config.output_dir
        output_dir.mkdir(exist_ok=True)

        report_path = output_dir / f"workflow_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        report_data = {
            "timestamp": datetime.now().isoformat(),
            "project": self.config_manager.config.name,
            "results": {
                phase.value: {
                    "success": result.success,
                    "duration": result.duration,
                    "quality_score": result.quality_score,
                    "errors": result.errors
                }
                for phase, result in results.items()
            }
        }

        with open(report_path, "w", encoding="utf-8") as f:
            json.dump(report_data, f, indent=2, ensure_ascii=False)
