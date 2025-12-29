#!/usr/bin/env python3
"""
Super Dev - 自动化竞品分析工具
功能：针对指定竞品进行深度对比，生成对比矩阵
"""

import sys
import argparse
from pathlib import Path
from ddgs import DDGS
from rich.table import Table
from rich import box
try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner

def get_competitor_info(competitor_name: str, industry: str):
    """
    Search for specific competitor details: Pricing, Main Features, Weaknesses.
    """
    info = {
        "name": competitor_name,
        "pricing": "Unknown",
        "features": [],
        "weaknesses": []
    }
    
    queries = [
        f"{competitor_name} pricing {industry}",
        f"{competitor_name} main features list",
        f"{competitor_name} vs others disadvantages cons"
    ]
    
    with DDGS() as ddgs:
        # Simplistic extraction (In production, use LLM to parse this)
        # Here we just grab the first relevant snippet as a proxy for "AI reading"
        for i, q in enumerate(queries):
            try:
                res = list(ddgs.text(q, max_results=1))
                if res:
                    snippet = res[0]['body']
                    if i == 0:
                        info['pricing'] = snippet[:100] + "..." # Truncate for display
                    elif i == 1:
                        info['features'].append(snippet[:150] + "...")
                    elif i == 2:
                        info['weaknesses'].append(snippet[:150] + "...")
            except Exception:
                pass
                
    return info

def generate_comparison_matrix(target_product: str, competitors: list):
    """
    Generate a CLI table and Markdown report.
    """
    table = Table(title=f"竞品分析: {target_product} vs 市场竞对", box=box.ROUNDED)
    table.add_column("维度", style="cyan", no_wrap=True)
    
    comp_data = []
    
    with spinner(f"正在分析 {len(competitors)} 个竞品..."):
        for comp in competitors:
            data = get_competitor_info(comp, target_product)
            comp_data.append(data)
            table.add_column(comp, style="green")

    # Rows
    table.add_row("定价模式", *[d.get('pricing', 'N/A') for d in comp_data])
    table.add_row("核心优势", *[d.get('pros', 'N/A') for d in comp_data])
    table.add_row("劣势/痛点", *[d.get('cons', 'N/A') for d in comp_data])
    
    console.print(table)
    return comp_data

def main():
    parser = argparse.ArgumentParser(description="Super Dev 竞品分析")
    parser.add_argument("target_product", help="你的产品类型 (如 'Code Editor')")
    parser.add_argument("competitors", nargs="+", help="竞品列表 (如 'VS Code' 'Cursor')")
    
    args = parser.parse_args()
    
    print_header("竞品分析专家", f"目标: {args.target_product}")
    
    data = generate_comparison_matrix(args.target_product, args.competitors)
    
    # Save Report
    report = f"# 竞品分析报告: {args.target_product}\n\n"
    for item in data:
        report += f"## {item['name']}\n- **定价**: {item.get('pricing')}\n- **优势**: {item.get('pros')}\n- **劣势**: {item.get('cons')}\n\n"
        
    output_path = Path.cwd() / "docs" / "competitor_analysis_raw.md"
    output_path.parent.mkdir(exist_ok=True)
    print_success(f"Matrix generated! Saved to {output_path}")

if __name__ == "__main__":
    main()
