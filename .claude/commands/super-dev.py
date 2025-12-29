#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Super Dev Slash Command Handler for Claude Code

开发：Excellent（11964948@qq.com）
功能：在 Claude Code 中通过 /super-dev 调用
作用：解析用户输入并执行 super-dev create
创建时间：2025-12-30
"""

import sys
import subprocess
import re
from pathlib import Path


def parse_input(user_input: str) -> dict:
    """解析用户输入"""
    parts = user_input.strip().split()

    if not parts:
        return {"error": "请提供功能描述"}

    result = {
        "description": "",
        "platform": "web",
        "frontend": "react",
        "backend": "node",
        "domain": ""
    }

    # 提取功能描述（直到遇到 -- 参数）
    desc_parts = []
    for i, part in enumerate(parts):
        if part.startswith("--"):
            break
        desc_parts.append(part)

    result["description"] = " ".join(desc_parts)

    # 解析参数
    for i, part in enumerate(parts):
        if part == "--platform" and i + 1 < len(parts):
            result["platform"] = parts[i + 1]
        elif part == "--frontend" and i + 1 < len(parts):
            result["frontend"] = parts[i + 1]
        elif part == "--backend" and i + 1 < len(parts):
            result["backend"] = parts[i + 1]
        elif part == "--domain" and i + 1 < len(parts):
            result["domain"] = parts[i + 1]

    return result


def run_super_dev_create(params: dict) -> int:
    """执行 super-dev create 命令"""
    cmd = [
        sys.executable, "-m", "super_dev.cli", "create",
        params["description"],
        "--platform", params["platform"],
        "--frontend", params["frontend"],
        "--backend", params["backend"]
    ]

    if params.get("domain"):
        cmd.extend(["--domain", params["domain"]])

    print(f"🚀 正在创建项目: {params['description']}")
    print(f"   平台: {params['platform']} | 前端: {params['frontend']} | 后端: {params['backend']}")
    print()

    result = subprocess.run(cmd, cwd=Path.cwd())
    return result.returncode


def main():
    """主入口"""
    # 从命令行参数获取用户输入
    if len(sys.argv) > 1:
        user_input = " ".join(sys.argv[1:])
    else:
        # 从标准输入读取（Claude Code 调用时）
        user_input = sys.stdin.read().strip()

    if not user_input:
        print("❌ 请提供功能描述")
        print()
        print("使用方法:")
        print("  /super-dev 用户认证系统")
        print("  /super-dev 用户认证系统 --platform web --frontend react")
        return 1

    # 解析输入
    params = parse_input(user_input)

    if "error" in params:
        print(f"❌ {params['error']}")
        return 1

    # 执行命令
    return run_super_dev_create(params)


if __name__ == "__main__":
    sys.exit(main())
