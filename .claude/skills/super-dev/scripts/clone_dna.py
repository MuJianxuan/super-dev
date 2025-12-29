#!/usr/bin/env python3
"""
Super Dev - The Mirror (clone_dna.py)
功能：基因克隆。分析目标品牌/网站的视觉风格，重写 UI 专家的设计系统参数。
"""

import sys
import argparse
import re
from pathlib import Path
from ddgs import DDGS

try:
    from utils import console, print_header, print_step, print_success, print_error, spinner
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_header, print_step, print_success, print_error, spinner

UI_EXPERT_PATH = Path(__file__).parent.parent / "experts" / "UI.md"

def fetch_design_dna(brand: str):
    """
    Search for brand colors and fonts.
    """
    dna = {
        "primary_color": "#000000",
        "secondary_color": "#ffffff",
        "font": "Inter",
        "style": "Modern"
    }
    
    queries = [
        f"{brand} brand color palette hex codes",
        f"{brand} brand typography font family",
        f"{brand} ui design style guide"
    ]
    
    with DDGS() as ddgs:
        # Colors
        try:
            res = list(ddgs.text(queries[0], max_results=3))
            text = " ".join([r['body'] for r in res])
            # Find Hex codes
            hexes = re.findall(r'#[0-9a-fA-F]{6}', text)
            if hexes:
                dna["primary_color"] = hexes[0]
                if len(hexes) > 1:
                    dna["secondary_color"] = hexes[1]
        except:
            pass
            
        # Fonts
        try:
            res = list(ddgs.text(queries[1], max_results=2))
            if res:
                if "Helvetica" in res[0]['body']: dna["font"] = "Helvetica Neue"
                elif "Roboto" in res[0]['body']: dna["font"] = "Roboto"
                elif "San Francisco" in res[0]['body']: dna["font"] = "San Francisco"
        except:
            pass

    return dna

def inject_dna(dna: dict):
    """
    Update UI.md with new DNA.
    """
    if not UI_EXPERT_PATH.exists():
        print_error("UI.md not found!")
        return

    content = UI_EXPERT_PATH.read_text(encoding="utf-8")
    
    # APPEND the Cloned DNA to the context injection or behavior section
    # Since updating the whole file is complex without a strict template, 
    # we will append a "Current DNA Override" section at the top.
    
    dna_block = f"""
> [!IMPORTANT]
> **CLONED DNA ACTIVE**: 当前正处于 [DNA Clone Mode]
> - **Primary Color**: `{dna['primary_color']}`
> - **Secondary Color**: `{dna['secondary_color']}`
> - **Typography**: `{dna['font']}`
> - **Style Directive**: 请严格模仿此配色与排版风格。
"""
    
    # Check if we already injected
    if "CLONED DNA ACTIVE" in content:
        # Regex replace existing block
        content = re.sub(r"> \[!IMPORTANT\]\n> \*\*CLONED DNA ACTIVE\*\*.*?\n", dna_block.strip() + "\n", content, flags=re.DOTALL)
    else:
        # Insert after frontmatter or title
        lines = content.splitlines()
        insert_idx = 5 
        for i, line in enumerate(lines):
            if line.startswith("#"):
                insert_idx = i + 2
                break
        lines.insert(insert_idx, dna_block)
        content = "\n".join(lines)
        
    UI_EXPERT_PATH.write_text(content, encoding="utf-8")

def main():
    parser = argparse.ArgumentParser(description="Super Dev 基因克隆 (The Mirror)")
    parser.add_argument("brand", help="目标品牌 (如 'Airbnb', 'Spotify')")
    
    args = parser.parse_args()
    
    print_header("基因克隆 (The Mirror)", f"目标: {args.brand}")
    
    dna = {}
    with spinner(f"正在窃取 {args.brand} 的设计基因..."):
        dna = fetch_design_dna(args.brand)
        
    print_step(f"捕获 DNA: {dna}")
    
    inject_dna(dna)
    
    print_success(f"UI 专家已变异! 现在的设计风格模仿: {args.brand}")

if __name__ == "__main__":
    main()
