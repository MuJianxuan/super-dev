#!/usr/bin/env python3
"""
Super Dev - 文档质量检查工具
验证文档是否符合质量标准
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple


class QualityChecker:
    """文档质量检查器"""
    
    def check_structure(self, content: str) -> List[Tuple[str, bool, str]]:
        """检查文档结构"""
        checks = []
        
        if re.search(r'^# .+', content, re.MULTILINE):
            checks.append(("有一级标题", True, ""))
        else:
            checks.append(("有一级标题", False, "文档应该有一级标题"))
        
        h2_count = len(re.findall(r'^## .+', content, re.MULTILINE))
        if h2_count >= 3:
            checks.append(("有足够章节", True, f"共 {h2_count} 个章节"))
        else:
            checks.append(("有足够章节", False, f"只有 {h2_count} 个章节"))
        
        if re.search(r'\|.+\|', content):
            checks.append(("包含表格", True, ""))
        else:
            checks.append(("包含表格", False, "建议使用表格"))
        
        return checks
    
    def run_checks(self, content: str) -> dict:
        """执行所有检查"""
        all_checks = self.check_structure(content)
        
        passed = [c for c in all_checks if c[1]]
        failed = [c for c in all_checks if not c[1]]
        
        total = len(all_checks)
        pass_rate = len(passed) / total * 100 if total > 0 else 0
        
        return {
            "total_checks": total,
            "passed": len(passed),
            "failed": len(failed),
            "pass_rate": round(pass_rate, 1),
            "status": "PASS" if pass_rate >= 80 else "FAIL",
            "details": {
                "passed": [(c[0], c[2]) for c in passed],
                "failed": [(c[0], c[2]) for c in failed]
            }
        }


def main():
    parser = argparse.ArgumentParser(
        description="Super Dev 文档质量检查工具 - 验证文档是否符合质量标准",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python quality_check.py ./docs/PRD.md
  python quality_check.py ./output/architecture.md --threshold 90
        """
    )
    parser.add_argument(
        "file",
        help="要检查的文档路径"
    )
    parser.add_argument(
        "-t", "--threshold",
        type=int,
        default=80,
        help="通过阈值 (默认: 80)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="显示详细信息"
    )

    args = parser.parse_args()

    try:
        content = Path(args.file).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"文件不存在: {args.file}", file=sys.stderr)
        sys.exit(1)

    checker = QualityChecker()
    result = checker.run_checks(content)

    # 使用自定义阈值
    status = "PASS" if result["pass_rate"] >= args.threshold else "FAIL"

    print(f"文档质量检查: {args.file}")
    print(f"通过率: {result['pass_rate']}%")
    print(f"状态: {status}")

    if args.verbose:
        print(f"\n总检查项: {result['total_checks']}")
        print(f"通过: {result['passed']}")
        print(f"失败: {result['failed']}")

    if result["details"]["failed"]:
        print("\n未通过项:")
        for name, reason in result["details"]["failed"]:
            print(f"  - {name}: {reason}")

    if args.verbose and result["details"]["passed"]:
        print("\n通过项:")
        for name, reason in result["details"]["passed"]:
            print(f"  [通过] {name}")

    sys.exit(0 if status == "PASS" else 1)


if __name__ == "__main__":
    main()
