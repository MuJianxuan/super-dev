#!/usr/bin/env python3
"""
Super Dev - 领域知识扩展器 (Infinite Domain Expansion)
功能：针对特定行业 (如医疗、金融) 抓取合规、标准与设计规范，生成知识库文件。
"""

import sys
import argparse
from pathlib import Path
from ddgs import DDGS
from rich.markdown import Markdown
from rich.panel import Panel

try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner

def search_domain_knowledge(domain: str):
    """
    Search for domain-specific technical standards, compliance, and patterns.
    """
    results = {
        "compliance": [],
        "standards": [],
        "design": [],
        "security": []
    }
    
    # 针对性搜索 Query
    queries = {
        "compliance": f"{domain} software application compliance regulations China Global",
        "standards": f"{domain} software industry data standards protocols",
        "design": f"{domain} application UI UX design best practices patterns",
        "security": f"{domain} software security standards requirements"
    }
    
    with DDGS() as ddgs:
        for category, query in queries.items():
            try:
                console.print(f"[dim]正在搜索 {category}: {query}...[/dim]")
                search_res = list(ddgs.text(query, max_results=3))
                results[category].extend(search_res)
            except Exception as e:
                console.print(f"[warning]搜索失败 '{query}': {e}[/warning]")
                
    return results

def generate_domain_knowledge_file(domain: str, data: dict):
    """
    Generate the structured markdown knowledge file.
    """
    content = f"# 领域知识库: {domain}\n\n"
    content += "> **自动生成**: 由 Super Dev 领域扩展器生成。\n"
    content += "> **用途**: 专家 (Experts) 在处理该领域任务时**必须**读取此文件。\n\n"
    
    content += "## 1. 合规与法规 (Compliance)\n"
    if not data["compliance"]:
        content += "- *未检索到特定合规信息，请人工核查。*\n"
    else:
        for item in data["compliance"]:
            content += f"- **{item['title']}**: {item['body']} ([Source]({item['href']}))\n"
            
    content += "\n## 2. 行业标准与协议 (Standards)\n"
    if not data["standards"]:
        content += "- *未检索到特定技术标准。*\n"
    else:
        for item in data["standards"]:
            content += f"- {item['body']} ([Source]({item['href']}))\n"
            
    content += "\n## 3. 设计最佳实践 (UI/UX)\n"
    if not data["design"]:
        content += "- *未检索到特定设计模式。*\n"
    else:
        for item in data["design"]:
            content += f"- {item['body']}\n"

    content += "\n## 4. 安全红线 (Security)\n"
    if not data["security"]:
        content += "- *未检索到特定安全标准。*\n"
    else:
        for item in data["security"]:
            content += f"- {item['body']}\n"
            
    return content

def main():
    parser = argparse.ArgumentParser(description="Super Dev 领域知识扩展器")
    parser.add_argument("domain", help="目标领域 (如 'Medical', 'Fintech', 'Ecommerce')")
    
    args = parser.parse_args()
    
    print_header("无限领域扩展器", f"目标领域: {args.domain}")
    
    data = {}
    with spinner(f"正在挖掘 {args.domain} 行业内幕..."):
        data = search_domain_knowledge(args.domain)
        
    print_step("正在编译领域知识矩阵...")
    markdown_content = generate_domain_knowledge_file(args.domain, data)
    
    # Save to knowledge/domains/
    output_dir = Path.cwd().parent / "knowledge" / "domains"
    # Fix path if running from root or scripts dir
    if Path("knowledge").exists():
         output_dir = Path("knowledge") / "domains"
    elif Path(".claude/skills/super-dev/knowledge").exists():
         output_dir = Path(".claude/skills/super-dev/knowledge") / "domains"
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{args.domain.lower()}.md"
    
    output_file.write_text(markdown_content, encoding="utf-8")
    
    print_success(f"知识库已扩展! 文件保存在: {output_file}")
    console.print(Panel(Markdown(markdown_content[:800] + "\n\n*(预览已截断)*"), title=f"{args.domain} 知识库预览"))

if __name__ == "__main__":
    main()
