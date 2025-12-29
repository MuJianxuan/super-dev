#!/usr/bin/env python3
"""
Super Dev - Auto Quality Gate
功能：自动化检查文档质量，执行商业级标准审计
"""

import sys
import re
import argparse
from pathlib import Path
from rich.table import Table
from rich.panel import Panel
try:
    from utils import console, print_header, print_step, print_success, print_error
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error

RULES = {
    "No TODOs": r"(?i)\bTODO\b|\[Insert .*\]",
    "No Placeholders": r"\[.*?\]",  # Brackets generally mean unfilled template
    "Commercial Header": r"Document Control|文档信息",
    "Legal Section": r"Legal & Compliance|法律与合规",
}

def check_file(file_path: Path):
    content = file_path.read_text(encoding="utf-8")
    
    score = 100
    findings = []
    
    # 1. Structure Checks
    if len(content) < 500:
        score -= 20
        findings.append(("CRITICAL", "文档内容过少 (<500 字符)。可能是空文档。"))
        
    # 2. Rule Checks
    for rule_name, pattern in RULES.items():
        if rule_name in ["Commercial Header", "Legal Section"]:
            # Critical Sections MUST exist
            if not re.search(pattern, content):
                score -= 15
                findings.append(("HIGH", f"缺失关键章节: {rule_name}"))
        else:
            # Forbidden patterns MUST NOT exist
            matches = re.findall(pattern, content)
            if matches:
                penalty = len(matches) * 5
                score -= penalty
                findings.append(("MEDIUM", f"发现 {len(matches)} 处违规内容 '{rule_name}' (例如 '{matches[0]}')"))

    # 3. Density Check (Simple Heuristic: Link/List density)
    list_count = len(re.findall(r"^(\s*[-*]|\s*\d+\.)", content, re.MULTILINE))
    if list_count < 5:
        score -= 10
        findings.append(("LOW", "信息密度低 (列表过少)。商业文档应包含结构化列表。"))

    return score, findings

def main():
    parser = argparse.ArgumentParser(description="Super Dev 质量门禁")
    parser.add_argument("files", nargs="+", help="Documents to check")
    
    args = parser.parse_args()
    
    print_header("质量门禁", "商业标准审计")
    
    all_passed = True
    
    for f_str in args.files:
        f_path = Path(f_str)
        if not f_path.exists():
            print_error(f"文件未找到: {f_path}")
            continue
            
        print_step(f"正在审计 {f_path.name}...")
        score, findings = check_file(f_path)
        
        # Display Results
        table = Table(title=f"审计报告: {f_path.name}", border_style="bold white")
        table.add_column("严重级", style="bold")
        table.add_column("发现问题")
        
        for severity, msg in findings:
            color = "red" if severity == "CRITICAL" else "yellow" if severity == "HIGH" else "blue"
            table.add_row(f"[{color}]{severity}[/{color}]", msg)
            
        console.print(table)
        
        color_score = "green" if score >= 80 else "red"
        console.print(Panel(f"[bold {color_score}]最终得分: {score}/100[/bold {color_score}]", title="裁决"))
        
        if score < 80:
            console.print(f"[bold red]不通过[/bold red]: 文档未达商业标准 (80分)。已拒绝。")
            all_passed = False
        else:
            console.print(f"[bold green]通过[/bold green]: 商业级认证 (Commercial Grade Certified)。")
            
    if not all_passed:
        sys.exit(1)

if __name__ == "__main__":
    main()
