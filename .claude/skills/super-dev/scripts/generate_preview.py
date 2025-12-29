#!/usr/bin/env python3
"""
Super Dev - Phantom Preview Generator (Phase 5)
功能：将 UI 设计注入 Vue3 原型模板，生成可运行的 preview.html
"""

import sys
import json
import argparse
from pathlib import Path
try:
    from utils import console, print_success, print_error
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_success, print_error

# 模板路径
TEMPLATE_PATH = Path(__file__).parent.parent / "knowledge" / "components" / "prototype" / "base.html"

# Vue3 组件模板
COMPONENT_TEMPLATES = {
    "header": """
<header class="glass fixed w-full z-50">
    <nav class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16 items-center">
            <div class="flex-shrink-0">
                <a href="#" class="text-2xl font-bold text-gray-900">{{ project_name }}</a>
            </div>
            <div class="hidden md:block">
                <div class="ml-10 flex items-baseline space-x-4">
                    <a href="#" class="text-gray-900 hover:text-gray-700 px-3 py-2 rounded-md font-medium">首页</a>
                    <a href="#" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md font-medium">产品</a>
                    <a href="#" class="text-gray-700 hover:text-gray-900 px-3 py-2 rounded-md font-medium">关于</a>
                </div>
            </div>
        </div>
    </nav>
</header>
""",

    "hero": """
<section class="py-20 px-4">
    <div class="max-w-7xl mx-auto text-center">
        <h1 class="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
            {{ hero_title }}
        </h1>
        <p class="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            {{ hero_subtitle }}
        </p>
        <div class="flex justify-center gap-4">
            <button class="bg-blue-600 text-white px-8 py-3 rounded-lg font-medium hover:bg-blue-700 transition">
                {{ cta_primary }}
            </button>
            <button class="border border-gray-300 text-gray-700 px-8 py-3 rounded-lg font-medium hover:bg-gray-50 transition">
                {{ cta_secondary }}
            </button>
        </div>
    </div>
</section>
""",

    "features": """
<section class="py-20 px-4 bg-gray-50">
    <div class="max-w-7xl mx-auto">
        <h2 class="text-3xl font-bold text-center text-gray-900 mb-12">
            核心功能
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div v-for="feature in features" :key="feature.title"
                 class="bg-white p-8 rounded-xl shadow-sm hover:shadow-md transition">
                <div class="text-blue-600 text-3xl mb-4">
                    <i :class="feature.icon"></i>
                </div>
                <h3 class="text-xl font-semibold text-gray-900 mb-2">{{ feature.title }}</h3>
                <p class="text-gray-600">{{ feature.description }}</p>
            </div>
        </div>
    </div>
</section>
""",

    "footer": """
<footer class="bg-gray-900 text-white py-12 px-4">
    <div class="max-w-7xl mx-auto text-center">
        <p class="text-gray-400">&copy; {{ year }} {{ project_name }}. All rights reserved.</p>
    </div>
</footer>
"""
}


def load_template():
    """加载 base.html 模板"""
    if not TEMPLATE_PATH.exists():
        print_error(f"模板文件不存在: {TEMPLATE_PATH}")
        return None
    return TEMPLATE_PATH.read_text(encoding="utf-8")


def inject_vue_app(content: str, ui_config: dict) -> str:
    """
    将 UI 配置注入到 Vue3 应用中

    Args:
        content: base.html 内容
        ui_config: UI 配置（包含颜色、字体、组件等）

    Returns:
        注入后的 HTML 内容
    """
    # 构建 Vue 应用数据
    vue_data = {
        "project_name": ui_config.get("project_name", "Project"),
        "hero_title": ui_config.get("hero_title", "Welcome to Our Platform"),
        "hero_subtitle": ui_config.get("hero_subtitle", "The best solution for your needs"),
        "cta_primary": ui_config.get("cta_primary", "Get Started"),
        "cta_secondary": ui_config.get("cta_secondary", "Learn More"),
        "features": ui_config.get("features", [
            {"title": "功能一", "description": "描述文字", "icon": "fas fa-star"},
            {"title": "功能二", "description": "描述文字", "icon": "fas fa-heart"},
            {"title": "功能三", "description": "描述文字", "icon": "fas fa-bolt"}
        ]),
        "year": ui_config.get("year", "2025")
    }

    # 构建 Vue 应用代码
    vue_app = f"""
const { createApp } = Vue;

createApp({{
    data() {{
        return {json.dumps(vue_data, ensure_ascii=False, indent=12)};
    }},
    methods: {{
        handlePrimaryClick() {{
            alert('按钮被点击！{vue_data["cta_primary"]}');
        }},
        handleSecondaryClick() {{
            alert('按钮被点击！{vue_data["cta_secondary"]}');
        }}
    }}
}}).mount('#app');
"""

    # 查找并替换 <!-- VUE_APP --> 占位符
    if "<!-- VUE_APP -->" in content:
        content = content.replace("<!-- VUE_APP -->", vue_app)
    else:
        # 如果没有占位符，在 #app 之前插入
        content = content.replace(
            '<div id="app">',
            f'<script>{vue_app}</script>\\n<div id="app">'
        )

    return content


def generate_preview(ui_config: dict, output_path: Path = None):
    """
    生成 preview.html 文件

    Args:
        ui_config: UI 配置字典
        output_path: 输出文件路径
    """
    console.print("[dim]正在加载原型模板...[/dim]")
    template = load_template()

    if template is None:
        return False

    console.print("[dim]正在注入 Vue3 应用...[/dim]")
    content = inject_vue_app(template, ui_config)

    # 确定输出路径
    if output_path is None:
        output_path = Path.cwd() / "preview.html"

    # 写入文件
    output_path.write_text(content, encoding="utf-8")

    print_success(f"原型已生成: {output_path}")
    console.print(f"[dim]在浏览器中打开: file://{output_path.absolute()}[/dim]")

    return True


def main():
    parser = argparse.ArgumentParser(description="Super Dev 幻影交付 (Phantom Delivery)")
    parser.add_argument("--project", default="Demo", help="项目名称")
    parser.add_argument("--title", default="Welcome to Our Platform", help="主标题")
    parser.add_argument("--subtitle", default="The best solution for your needs", help="副标题")
    parser.add_argument("--primary-cta", default="Get Started", help="主按钮文字")
    parser.add_argument("--secondary-cta", default="Learn More", help="次按钮文字")
    parser.add_argument("--output", help="输出文件路径")

    args = parser.parse_args()

    # 构建 UI 配置
    ui_config = {
        "project_name": args.project,
        "hero_title": args.title,
        "hero_subtitle": args.subtitle,
        "cta_primary": args.primary_cta,
        "cta_secondary": args.secondary_cta,
        "year": "2025"
    }

    # 如果指定了输出路径
    output_path = Path(args.output) if args.output else None

    # 生成原型
    generate_preview(ui_config, output_path)


if __name__ == "__main__":
    main()
