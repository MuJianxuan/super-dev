#!/usr/bin/env python3
"""
Super Dev - The Spawner (hire_expert.py)
功能：虚空造人。根据职位名称，联网搜索 JD 和最佳实践，基于 TEMPLATE.md 生成新的专家人格。
"""

import sys
import argparse
from pathlib import Path
from string import Template
from ddgs import DDGS
from rich.panel import Panel
from rich.markdown import Markdown

try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner

TEMPLATE_PATH = Path(__file__).parent.parent / "experts" / "TEMPLATE.md"
OUTPUT_DIR = Path(__file__).parent.parent / "experts"

def search_role_intel(role: str):
    """
    Search for Job Description, Mindset, and Best Practices for a role.
    """
    intel = {
        "description": "",
        "mindset": "",
        "focus": "",
        "deliverables": []
    }
    
    queries = [
        f"{role} job description responsibilities senior",
        f"{role} mindset philosophy best practices",
        f"{role} deliverables artifacts output",
        f"{role} interview questions senior"
    ]
    
    with DDGS() as ddgs:
        # 1. Mindset & Motto
        try:
            res = list(ddgs.text(queries[1], max_results=2))
            if res:
                intel["mindset"] = res[0]['body'][:100] + "..."
        except:
            intel["mindset"] = "Professional and Detail-Oriented"

        # 2. Responsibilities (Focus)
        try:
            res = list(ddgs.text(queries[0], max_results=2))
            if res:
                intel["focus"] = res[0]['body'][:150] + "..."
        except:
            intel["focus"] = "Efficiency, Quality, Reliability"

        # 3. Deliverables
        try:
            res = list(ddgs.text(queries[2], max_results=3))
            if res:
                for r in res:
                    intel["deliverables"].append(r['title'])
        except:
             intel["deliverables"] = ["Technical Report", "Strategy Doc"]

    return intel

def generate_expert(role: str, intel: dict):
    """
    Fill the TEMPLATE.md with gathered intelligence.
    """
    if not TEMPLATE_PATH.exists():
        print_error("TEMPLATE.md not found!")
        sys.exit(1)
        
    template_content = TEMPLATE_PATH.read_text(encoding="utf-8")
    
    # Simple substitution (Not using string.Template due to likely collisions with Markdown ${})
    # We will use manual replace for {{ key }} style to be safe with Markdown
    
    content = template_content
    
    replacements = {
        "{{ role_name }}": role,
        "{{ role_alias }}": "Specialist",
        "{{ mindset }}": intel["mindset"],
        "{{ motto }}": f"As a {role}, I strive for perfection.",
        "{{ focus_areas }}": intel["focus"],
        "{{ core_question }}": "How does this align with industry standards?",
        "{{ behavior_1_title }}": "Research First",
        "{{ behavior_1_desc }}": "Always verify assumptions with data.",
        "{{ behavior_2_title }}": "Best Practices",
        "{{ behavior_2_desc }}": "Adhere to the latest industry standards.",
        "{{ deliverable_1 }}": "Expert Analysis",
    }
    
    for k, v in replacements.items():
        content = content.replace(k, str(v))
        
    # Generate filename
    filename = role.upper().replace(" ", "_") + ".md"
    output_path = OUTPUT_DIR / filename
    output_path.write_text(content, encoding="utf-8")
    
    return output_path

def main():
    parser = argparse.ArgumentParser(description="Super Dev 虚空造人 (The Spawner)")
    parser.add_argument("role", help="想要招聘的角色 (如 'Blockchain Expert')")
    
    args = parser.parse_args()
    
    print_header("虚空造人 (The Spawner)", f"目标角色: {args.role}")
    
    intel = {}
    with spinner(f"正在猎聘顶级 {args.role}..."):
        intel = search_role_intel(args.role)
        
    print_step("正在进行入职培训 (Generating Persona)...")
    file_path = generate_expert(args.role, intel)
    
    print_success(f"新专家已入职! 定义文件: {file_path}")
    console.print(f"[dim]思维逻辑: {intel['mindset']}[/dim]")

if __name__ == "__main__":
    main()
