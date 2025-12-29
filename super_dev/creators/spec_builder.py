# -*- coding: utf-8 -*-
"""
Spec 构建器 - 自动创建 Spec 规范

开发：Excellent（11964948@qq.com）
功能：从需求自动创建完整的 Spec 变更提案
作用：参考 OpenSpec，自动分解任务、定义场景
创建时间：2025-12-30
"""

from pathlib import Path
from typing import Optional
from datetime import datetime

from ..specs import SpecGenerator, ChangeManager, SpecManager
from ..specs.models import ChangeStatus, TaskStatus, DeltaType, Task


class SpecBuilder:
    """Spec 构建器 - 自动创建 Spec 规范"""

    def __init__(self, project_dir: Path, name: str, description: str):
        """初始化 Spec 构建器"""
        self.project_dir = Path(project_dir).resolve()
        self.name = name
        self.description = description

        self.spec_generator = SpecGenerator(self.project_dir)
        self.change_manager = ChangeManager(self.project_dir)
        self.spec_manager = SpecManager(self.project_dir)

    def create_change(self, requirements: list, tech_stack: dict) -> str:
        """创建 Spec 变更提案"""
        # 初始化 SDD 目录
        self.spec_generator.init_sdd()

        # 生成变更 ID (从项目名称转换)
        change_id = self.name.replace('_', '-').lower()

        # 1. 创建变更提案
        change = self.spec_generator.create_change(
            change_id=change_id,
            title=self.name.replace('-', ' ').title(),
            description=self.description,
            motivation="用户需求驱动的功能开发",
            impact=f"涉及 {len(requirements)} 个主要功能模块"
        )

        # 2. 添加需求到变更
        for req in requirements:
            self.spec_generator.add_requirement_to_change(
                change_id=change_id,
                spec_name=req['spec_name'],
                requirement_name=req['req_name'],
                description=req['description'],
                scenarios=req.get('scenarios', []),
                delta_type=DeltaType.ADDED
            )

        # 3. 自动生成任务
        self._generate_tasks_for_change(change_id, tech_stack)

        return change_id

    def _generate_tasks_for_change(self, change_id: str, tech_stack: dict):
        """为变更自动生成任务"""
        change = self.change_manager.load_change(change_id)
        if not change:
            return

        tasks = []
        task_counter = [1, 0]  # [major, minor]

        # 根据技术栈生成任务
        backend = tech_stack.get('backend', 'node')
        frontend = tech_stack.get('frontend', 'react')

        # 为每个规范增量生成任务
        for delta in change.spec_deltas:
            # 数据库任务 (如果有后端)
            if backend != 'none':
                task_counter[1] += 1
                tasks.append(Task(
                    id=f"{task_counter[0]}.{task_counter[1]}",
                    title=f"设计 {delta.spec_name} 数据库表",
                    description=f"设计并创建 {delta.spec_name} 相关的数据表",
                    status=TaskStatus.PENDING,
                    spec_refs=[f"{delta.spec_name}::*"]
                ))

            # 后端 API 任务
            if backend != 'none':
                task_counter[1] += 1
                tasks.append(Task(
                    id=f"{task_counter[0]}.{task_counter[1]}",
                    title=f"实现 {delta.spec_name} API",
                    description=f"实现 {delta.spec_name} 相关的 API 端点",
                    status=TaskStatus.PENDING,
                    spec_refs=[f"{delta.spec_name}::*"]
                ))

            # 前端 UI 任务
            if frontend != 'none':
                task_counter[1] += 1
                tasks.append(Task(
                    id=f"{task_counter[0]}.{task_counter[1]}",
                    title=f"实现 {delta.spec_name} 前端页面",
                    description=f"实现 {delta.spec_name} 相关的前端组件和页面",
                    status=TaskStatus.PENDING,
                    spec_refs=[f"{delta.spec_name}::*"]
                ))

        # 测试任务
        task_counter[0] += 1
        task_counter[1] = 0

        for delta in change.spec_deltas:
            task_counter[1] += 1
            tasks.append(Task(
                id=f"{task_counter[0]}.{task_counter[1]}",
                title=f"测试 {delta.spec_name} 功能",
                description=f"编写 {delta.spec_name} 的单元测试和集成测试",
                status=TaskStatus.PENDING,
                spec_refs=[f"{delta.spec_name}::*"]
            ))

        # 更新变更
        change.tasks = tasks
        self.change_manager.save_change(change)
