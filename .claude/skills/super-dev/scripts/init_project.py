#!/usr/bin/env python3
"""
Super Dev - 项目初始化工具
创建标准输出目录结构
"""

import sys
from datetime import datetime
from pathlib import Path


def init_project(project_name: str, output_base: Path = None):
    """初始化项目输出目录"""
    
    if output_base is None:
        output_base = Path.cwd()
    
    output_dir = output_base / "docs"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    readme_content = f"""# {project_name} - 文档目录

创建时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 文件说明

- PRD.md - 产品需求文档
- ARCHITECTURE.md - 架构设计文档
- UI_SPEC.md - UI 设计规格
- INTERACTION.md - 交互设计文档
- CODE_REVIEW.md - 代码审查报告
"""
    
    readme_path = output_dir / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    
    return output_dir


def main():
    if len(sys.argv) < 2:
        print("Super Dev 项目初始化工具")
        print()
        print("用法: python init_project.py <项目名称>")
        print()
        print("示例: python init_project.py online-education")
        sys.exit(0)
    
    project_name = sys.argv[1]
    
    print(f"初始化项目: {project_name}")
    output_dir = init_project(project_name)
    print(f"输出目录已创建: {output_dir}")


if __name__ == "__main__":
    main()
