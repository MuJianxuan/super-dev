#!/usr/bin/env python3
"""
Super Dev - Research Orchestrator
功能：并行执行市场研究和竞品分析，生成由于专家使用的"任务简报" (Mission Brief)。
"""

import sys
import json
import argparse
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
    from market_research import search_market_data
    from competitor_analysis import get_competitor_info
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner
    from market_research import search_market_data
    from competitor_analysis import get_competitor_info

def run_research_suite(topic: str, neighbors: list):
    """
    Run all research tools in parallel.
    """
    results = {}
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Task 1: Market Research
        future_market = executor.submit(search_market_data, topic, "Global")
        
        # Task 2: Competitor Analysis (Parallel for each competitor)
        future_competitors = [executor.submit(get_competitor_info, comp, topic) for comp in neighbors]
        
        results["market"] = future_market.result()
        results["competitors"] = [f.result() for f in future_competitors]
        
    return results

def generate_mission_brief(project_name: str, data: dict):
    """
    Generate a JSON Brief for the Agent Experts.
    """
    brief = {
        "meta": {
            "project": project_name,
            "timestamp": datetime.now().isoformat(),
            "generator": "Super Dev 指挥官 v2.0"
        },
        "intelligence": {
            "market_size_signals": [x['body'] for x in data['market'].get('market_size', [])],
            "trends": [x['body'] for x in data['market'].get('trends', [])],
            "pain_points": [x['body'] for x in data['market'].get('pain_points', [])],
            "competitor_matrix": data['competitors']
        },
        "directives": {
            "pm_focus": "利用痛点 (pain_points) 推导特性优先级 (MoSCoW)。",
            "architect_focus": "根据市场规模信号 (market_size) 扩展架构设计。",
            "ui_focus": "与竞品视觉风格 (competitor_matrix) 形成差异化。"
        }
    }
    return brief

def main():
    parser = argparse.ArgumentParser(description="Super Dev 研究指挥官")
    parser.add_argument("project_name", help="项目名称")
    parser.add_argument("topic", help="核心领域 (如 'AI Code Tool')")
    parser.add_argument("competitors", nargs="+", help="竞品列表")
    
    args = parser.parse_args()
    
    print_header("研究指挥官", f"项目: {args.project_name}")
    
    print_step("正在部署自动化研究无人机...")
    results = {}
    with spinner("正在抓取市场与竞品情报..."):
        results = run_research_suite(args.topic, args.competitors)
        
    print_step("正在编译任务简报 (Mission Brief)...")
    brief = generate_mission_brief(args.project_name, results)
    
    output_path = Path.cwd() / "docs" / "mission_brief.json"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(json.dumps(brief, indent=2, ensure_ascii=False), encoding="utf-8")
    
    print_success(f"任务简报已就绪: {output_path}")
    console.print_json(data=brief)

if __name__ == "__main__":
    main()
