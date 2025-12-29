#!/usr/bin/env python3
"""
Super Dev - 文档生成工具
基于模板生成标准化文档
"""

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class DocumentGenerator:
    """文档生成器"""
    
    def __init__(self, skill_dir: Optional[Path] = None):
        if skill_dir is None:
            current = Path.cwd()
            skill_dir = current / ".claude" / "skills" / "super-dev"
            if not skill_dir.exists():
                skill_dir = Path(__file__).parent.parent
        
        self.skill_dir = skill_dir
        self.templates_dir = skill_dir / "templates"
        self.output_dir = Path.cwd() / "docs"
    
    def ensure_output_dir(self):
        """确保输出目录存在"""
        self.output_dir.mkdir(parents=True, exist_ok=True)
        return self.output_dir
    
    def load_template(self, template_name: str) -> str:
        """加载模板文件"""
        template_path = self.templates_dir / f"{template_name}.md"
        if not template_path.exists():
            raise FileNotFoundError(f"模板不存在: {template_path}")
        return template_path.read_text(encoding="utf-8")
    
    def fill_template(self, template: str, data: Dict) -> str:
        """填充模板变量"""
        result = template
        result = result.replace("[产品名]", data.get("product_name", "[产品名]"))
        result = result.replace("[系统名]", data.get("product_name", "[系统名]"))
        result = result.replace("[日期]", datetime.now().strftime("%Y-%m-%d"))
        return result
    
    def generate(self, doc_type: str, data: Dict) -> Path:
        """生成文档"""
        template_map = {
            "prd": "PRD",
            "architecture": "ARCHITECTURE",
            "arch": "ARCHITECTURE",
            "ui": "UI_SPEC",
            "ux": "INTERACTION",
            "interaction": "INTERACTION",
            "code-review": "CODE_REVIEW",
            "code": "CODE_REVIEW"
        }
        
        template_name = template_map.get(doc_type.lower())
        if not template_name:
            raise ValueError(f"未知文档类型: {doc_type}")
        
        template = self.load_template(template_name)
        content = self.fill_template(template, data)
        
        self.ensure_output_dir()
        output_path = self.output_dir / f"{template_name}.md"
        output_path.write_text(content, encoding="utf-8")
        return output_path


def main():
    if len(sys.argv) < 2:
        print("Super Dev 文档生成工具")
        print()
        print("用法: python generate_doc.py <文档类型> [产品名称]")
        print()
        print("文档类型: prd, architecture, ui, ux, code-review")
        print()
        print("示例: python generate_doc.py prd '在线教育平台'")
        sys.exit(0)
    
    doc_type = sys.argv[1]
    product_name = sys.argv[2] if len(sys.argv) > 2 else "MyProduct"
    
    generator = DocumentGenerator()
    data = {"product_name": product_name}
    
    try:
        output_path = generator.generate(doc_type, data)
        print(f"文档已生成: {output_path}")
    except Exception as e:
        print(f"错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
