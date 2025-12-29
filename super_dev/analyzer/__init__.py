# -*- coding: utf-8 -*-
"""
Super Dev 项目分析器
用于自动检测和分析项目结构
"""

from .analyzer import ProjectAnalyzer, ArchitectureReport
from .detectors import detect_project_type, detect_tech_stack
from .models import (
    Dependency,
    DesignPattern,
    PatternType,
    TechStack,
    ProjectCategory,
    ProjectType,
    FrameworkType,
    ArchitecturePattern,
)

__all__ = [
    "ProjectAnalyzer",
    "ProjectCategory",
    "ProjectType",
    "ArchitectureReport",
    "Dependency",
    "DesignPattern",
    "PatternType",
    "TechStack",
    "FrameworkType",
    "ArchitecturePattern",
    "detect_project_type",
    "detect_tech_stack",
]


