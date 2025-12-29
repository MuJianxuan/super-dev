#!/usr/bin/env python3
"""
Super Dev - Dynamic Template Engine
Function: Generates context-aware documents by assembling components from the Knowledge Matrix.
Language: English (Strict)
"""

import sys
import argparse
from pathlib import Path
from datetime import datetime

# Configuration
KNOWLEDGE_BASE = Path(__file__).parent.parent / "knowledge"
COMPONENTS = KNOWLEDGE_BASE / "components"

def load_component(category: str, name: str) -> str:
    """Load a specific markdown component."""
    path = COMPONENTS / category / f"{name}.md"
    if not path.exists():
        return f"<!-- Missing Component: {category}/{name} -->"
    return path.read_text(encoding="utf-8")

def assemble_prd(platform: str, domain: str, project_name: str, lang: str = "cn") -> str:
    """Assemble a PRD based on platform and domain."""
    
    # 1. Load Base
    content = load_component("prd", "base")
    
    # 2. Inject Platform Specifics
    platform_section = load_component("prd", platform) if platform in ["mobile", "web", "wechat"] else ""
    
    # Language Pack
    LANG_PACK = {
        "cn": {
            "web": "Web端", "mobile": "移动端 (App)", "wechat": "微信小程序", "desktop": "桌面端",
            "vision": "(待填充项目愿景)", "audience": "(待填充目标用户)", "problem": "(待填充核心痛点)"
        },
        "en": {
            "web": "Web Application", "mobile": "Mobile App", "wechat": "WeChat Mini Program", "desktop": "Desktop App",
            "vision": "(Vision TBD)", "audience": "(Target Audience TBD)", "problem": "(Core Pain Points TBD)"
        }
    }
    
    current_pack = LANG_PACK.get(lang, LANG_PACK["cn"])
    
    # 3. Inject Domain Specifics (Placeholder for Phase 3)
    domain_section = "" 
    # if domain == "saas": domain_section = load_component("prd", "saas")
    
    # 4. Assembly
    full_doc = f"{content}\n\n{platform_section}\n\n{domain_section}"
    
    # 5. Variable Replacement
    replacements = {
        "{{ project_name }}": project_name,
        "{{ year }}": datetime.now().strftime("%Y"),
        "{{ month }}": datetime.now().strftime("%m"),
        "{{ date }}": datetime.now().strftime("%Y-%m-%d"),
        "{{ platform }}": current_pack.get(platform, platform),
        "{{ section_number }}": "3", 
        "{{ vision }}": current_pack["vision"],
        "{{ target_audience }}": current_pack["audience"],
        "{{ problem_statement }}": current_pack["problem"],
    }
    
    for key, val in replacements.items():
        full_doc = full_doc.replace(key, val)
        
    return full_doc

def main():
    parser = argparse.ArgumentParser(description="Super Dev 模版引擎")
    parser.add_argument("type", choices=["PRD", "ARCH", "UI"], help="文档类型")
    parser.add_argument("--platform", required=True, choices=["web", "mobile", "wechat", "desktop"], help="Target Platform")
    parser.add_argument("--domain", default="general", help="Domain (e.g. saas, ecommerce)")
    parser.add_argument("--project", default="Project", help="Project Name")
    parser.add_argument("--lang", default="cn", choices=["cn", "en"], help="Output Language (cn/en)")
    
    args = parser.parse_args()
    
    output = ""
    if args.type == "PRD":
        output = assemble_prd(args.platform, args.domain, args.project, args.lang)
    else:
        output = f"# {args.type} doc for {args.platform} (WIP)"
        
    # Output to stdout for redirection or pipe
    print(output)

if __name__ == "__main__":
    main()
