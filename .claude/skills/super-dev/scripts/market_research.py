#!/usr/bin/env python3
"""
Super Dev - 自动化市场研究工具
功能：联网搜索市场规模、增长趋势、用户痛点
"""

import sys
import json
import argparse
from pathlib import Path
from ddgs import DDGS
from rich.markdown import Markdown
from rich.panel import Panel
try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
except ImportError:
    # Fallback if running from a different directory context
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner

def search_market_data(topic: str, region: str = "Global"):
    """
    Perform deep web search for market data.
    """
    results = {
        "market_size": [],
        "trends": [],
        "pain_points": [],
        "competitors": []
    }
    
    queries = [
        f"{topic} market size {region} 2024 2025 report",
        f"{topic} industry key trends 2025",
        f"{topic} user pain points and complaints",
        f"top {topic} competitors {region}"
    ]
    
    with DDGS() as ddgs:
        for q in queries:
            try:
                # Get top 3 results for each query
                search_res = list(ddgs.text(q, max_results=3))
                
                if "market size" in q:
                    results["market_size"].extend(search_res)
                elif "trends" in q:
                    results["trends"].extend(search_res)
                elif "pain points" in q:
                    results["pain_points"].extend(search_res)
                elif "competitors" in q:
                    results["competitors"].extend(search_res)
                    
            except Exception as e:
                console.print(f"[warning]Search failed for query '{q}': {e}[/warning]")

    return results

def generate_report(topic: str, data: dict):
    """
    Synthesize check data into a Markdown report.
    (In a real production system, this would use an LLM to summarize specific numbers.
     Here we structure the raw search snippets for the Agent to consume.)
    """
    
    report = f"""# Market Research Report: {topic}

## 1. Market Size & Growth
"""
    if not data["market_size"]:
        report += "- *No specific market size data found.*"
    else:
        for item in data["market_size"]:
            report += f"- **{item['title']}**: {item['body']} ([Source]({item['href']}))\n"

    report += "\n## 2. Key Trends\n"
    if not data["trends"]:
        report += "- *No specific trend data found.*"
    else:
        for item in data["trends"]:
            report += f"- {item['body']} ([Source]({item['href']}))\n"

    report += "\n## 3. User Pain Points\n"
    if not data["pain_points"]:
        report += "- *No specific pain point data found.*"
    else:
        for item in data["pain_points"]:
            report += f"- {item['body']}\n"
            
    return report

def main():
    parser = argparse.ArgumentParser(description="由 Super Dev 执行的市场研究工具")
    parser.add_argument("topic", help="研究主题 (如 'Online Education')")
    parser.add_argument("region", help="目标市场区域 (如 'China' 或 'Global')", default="Global")
    
    args = parser.parse_args()
    
    print_header("市场调研专家", f"主题: {args.topic} | 区域: {args.region}")
    
    data = {}
    
    with spinner(f"正在深网检索 '{args.topic}' 市场数据..."):
        data = search_market_data(args.topic, args.region)
        
    print_step("正在综合洞察...")
    report = generate_report(args.topic, data)
    
    # Output to stdout for the Agent to read, or save to file
    output_path = Path.cwd() / "docs" / "market_research_raw.md"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    
    print_success(f"调研完成! 数据已保存至 {output_path}")
    console.print(Panel(Markdown(report[:1000] + "\n\n*(预览已截断)*"), title="报告预览"))

if __name__ == "__main__":
    main()
