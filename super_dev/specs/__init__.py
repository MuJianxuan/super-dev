# -*- coding: utf-8 -*-
"""
Super Dev Spec-Driven Development (SDD) 模块

开发：Excellent（11964948@qq.com）
功能：规范驱动开发工具，类似 OpenSpec
作用：在开发前达成规范共识，让 AI 遵循规范而非随意发挥
创建时间：2025-12-30
最后修改：2025-12-30
"""

from .models import (
    Spec,
    Requirement,
    Scenario,
    Change,
    ChangeStatus,
    Proposal,
    Task,
    TaskStatus,
    DeltaType,
    SpecDelta,
)
from .manager import SpecManager, ChangeManager
from .generator import SpecGenerator
from .validator import SpecValidator, ValidationResult, ValidationError

__all__ = [
    "Spec",
    "Requirement",
    "Scenario",
    "Change",
    "ChangeStatus",
    "Proposal",
    "Task",
    "TaskStatus",
    "DeltaType",
    "SpecDelta",
    "SpecManager",
    "ChangeManager",
    "SpecGenerator",
    "SpecValidator",
    "ValidationResult",
    "ValidationError",
]
