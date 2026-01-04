# Super Dev

<div align="center">


# 顶级 AI 开发战队
### God-Tier AI Development Team

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![Code Style](https://img.shields.io/badge/code%20style-black-2024%20informational)](https://github.com/psf/black)
[![Type Checks](https://img.shields.io/badge/type%20checks-mypy-success)](https://mypy-lang.org/)
[![Tests](https://img.shields.io/badge/tests-59%20passing-brightgreen)](tests/)
[![CI](https://img.shields.io/badge/CI-GitHub%20Actions-success)](.github/workflows/ci.yml)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blue)](https://code.claude.com)

[English](README_EN.md) | 简体中文

[功能特性](#-功能特性) • [快速开始](#-快速开始) • [命令参考](#-命令参考) • [文档](#-文档) • [示例](#-示例)

</div>

---

## 什么是 Super Dev?

**Super Dev** 是一个商业级 AI 辅助开发工具，专注于 **规范驱动开发 (SDD)**。它从一句话需求出发，自动生成完整的项目文档、规范说明，直至 CI/CD 配置和数据库迁移脚本。

```
想法 → 文档 → 规范 → 审查 → AI 实现 → 部署
```

### 核心价值

| 能力 | 说明 |
|:---|:-----|
| **规范驱动开发** | 类似 OpenSpec 的工作流，在编码前达成规范共识 |
| **8 阶段流水线** | 文档 → Spec → 红队审查 → 质量门禁 → 代码审查 → AI 提示 → CI/CD → 数据库迁移 |
| **10 位专家系统** | PM/架构/UI/UX/安全/代码/DBA/QA/DevOps/RCA 协作 |
| **设计智能引擎** | 超越 UI UX Pro Max：100+ UI 风格、150+ 配色、80+ 字体组合、BM25+ 语义搜索 |
| **知识库注入** | 6 个业务领域 + 4 个平台的专业知识自动注入 |
| **质量门禁** | 80+ 分质量标准，确保交付物达到商业级 |
| **开箱即用** | CLI 工具，一键生成完整项目资产 |

---

## 功能特性

### 1. 完整开发流水线

Super Dev 提供从想法到部署的 8 阶段自动化流水线：

```
┌──────────────────────────────────────────────────────────────┐
│                    Super Dev 完整流水线                       │
├──────────────────────────────────────────────────────────────┤
│  第 1 阶段  │  生成专业文档 (PRD + 架构 + UI/UX)              │
│  第 2 阶段  │  创建 Spec 规范 (OpenSpec 风格)                  │
│  第 3 阶段  │  红队审查 (安全 + 性能 + 架构)                   │
│  第 4 阶段  │  质量门禁 (自动评分 80+ 分通过)                  │
│  第 5 阶段  │  代码审查指南                                   │
│  第 6 阶段  │  AI 提示词生成                                  │
│  第 7 阶段  │  CI/CD 配置 (5 大平台)                          │
│  第 8 阶段  │  数据库迁移脚本 (6 种 ORM)                      │
└──────────────────────────────────────────────────────────────┘
```

### 2. CLI 工具集

```bash
# ===== 核心命令 =====
super-dev pipeline "功能描述"    # 运行完整 8 阶段流水线
super-dev create "功能描述"      # 一键创建项目 (文档 + Spec + AI 提示)
super-dev spec <subcommand>      # Spec-Driven Development 管理
super-dev design <subcommand>    # 设计智能引擎 (超越 UI UX Pro Max)

# ===== 设计智能 =====
super-dev design search "glass"       # 搜索设计资产
super-dev design generate --product SaaS --industry Fintech  # 生成完整设计系统
super-dev design tokens --primary #3B82F6  # 生成 design tokens

# ===== 项目管理 =====
super-dev init <name>            # 初始化新项目
super-dev analyze [path]         # 分析现有项目结构
super-dev config <cmd>           # 配置管理

# ===== 专家系统 =====
super-dev expert --list          # 列出所有可用专家
super-dev expert PM "提示词"     # 调用产品经理专家
super-dev expert ARCHITECT       # 调用架构师专家

# ===== 质量与部署 =====
super-dev quality --type all     # 运行质量检查
super-dev deploy --cicd github   # 生成 CI/CD 配置
super-dev preview -o output.html # 生成 UI 原型

# ===== 工作流 =====
super-dev workflow               # 运行交互式工作流
```

### 3. Spec-Driven Development (SDD)

Super Dev 内置了类似 [OpenSpec](https://github.com/Fission-AI/OpenSpec) 的规范驱动开发工作流：

```
┌────────────────────┐
│ Draft Change       │
│ Proposal           │
└────────┬───────────┘
         │ share intent with your AI
         ▼
┌────────────────────┐
│ Review & Align     │
│ (edit specs/tasks) │◀──── feedback loop ──────┐
└────────┬───────────┘                          │
         │ approved plan                        │
         ▼                                      │
┌────────────────────┐                          │
│ Implement Tasks    │──────────────────────────┘
│ (AI writes code)   │
└────────┬───────────┘
         │ ship the change
         ▼
┌────────────────────┐
│ Archive & Update   │
│ Specs (source)     │
└────────────────────┘
```

**目录结构：**
```
.super-dev/
├── specs/          # 当前规范 (单一事实源)
│   └── auth/
│       └── spec.md
├── changes/        # 提议的变更
│   └── add-2fa/
│       ├── proposal.md
│       ├── tasks.md
│       ├── design.md
│       └── specs/
│           └── auth/
│               └── spec.md  # Delta (ADDED/MODIFIED/REMOVED)
└── archive/        # 已归档的变更
```

### 4. 专家团队

| 专家 | 专长 | 适用场景 |
|:---|:-----|:---------|
| **PM** | 需求分析、PRD 编写、用户故事 | 产品规划、功能定义 |
| **ARCHITECT** | 系统设计、技术选型、架构文档 | 架构设计、技术决策 |
| **UI** | 视觉设计、设计规范、组件库 | 界面设计、视觉规范 |
| **UX** | 交互设计、用户体验、信息架构 | 交互流程、用户体验 |
| **SECURITY** | 安全审查、漏洞检测、威胁建模 | 安全审查、渗透测试 |
| **CODE** | 代码实现、最佳实践、代码审查 | 代码实现、代码审查 |
| **DBA** | 数据库设计、SQL 优化、数据建模 | 数据库设计、性能优化 |
| **QA** | 质量保证、测试策略、自动化测试 | 测试计划、质量保证 |
| **DEVOPS** | 部署、CI/CD、容器化、监控 | 部署配置、流水线 |
| **RCA** | 根因分析、故障复盘、改进建议 | 故障分析、复盘总结 |

### 5. 知识库

#### 业务领域
- **金融科技** (fintech) - 支付、借贷、理财、保险
- **电子商务** (ecommerce) - B2C/B2B/C2C、跨境、社交电商
- **医疗健康** (medical) - 医疗信息化、健康管理
- **社交媒体** (social) - Feed 流、即时通讯、内容审核
- **物联网** (iot) - 设备管理、MQTT/CoAP、边缘计算
- **在线教育** (education) - 直播课堂、题库系统、学习分析
- **认证授权** (auth) - JWT、OAuth2、RBAC
- **内容管理** (content) - CMS、内容推荐、搜索

#### 技术平台
- **Web** - React/Vue/Angular + Node/Python/Go
- **Mobile** - React Native/Flutter
- **WeChat** - 微信小程序
- **Desktop** - Electron/Tauri

### 6. 支持的技术栈

#### 前端框架
- React, Vue, Angular, Svelte

#### 后端框架
- Node.js, Python, Go, Java

#### 数据库 ORM
- Prisma, TypeORM, Sequelize, SQLAlchemy, Django, Mongoose

#### CI/CD 平台
- GitHub Actions, GitLab CI, Jenkins, Azure DevOps, Bitbucket Pipelines

### 7. 设计智能引擎 (超越 UI UX Pro Max)

Super Dev 内置强大的设计智能引擎，提供从设计搜索到完整设计系统生成的端到端能力：

#### 核心能力

| 能力 | 说明 |
|:---|:-----|
| **BM25+ 语义搜索** | 增强版 BM25 算法，支持字段权重、短语匹配、IDF 平滑、模糊搜索 |
| **多域搜索** | style, color, typography, component, layout, animation, ux, chart, product, stack |
| **美学方向生成** | 26+ 种独特美学方向（cyberpunk, brutalist_minimal, vaporwave, etc.） |
| **Design Tokens** | 自动生成色彩、间距、阴影、圆角等设计令牌 |
| **设计系统生成** | 完整设计系统（CSS 变量、Tailwind 配置、设计文档） |
| **AI 驱动推荐** | 基于产品类型、行业、关键词智能推荐设计系统 |

#### 设计资产库

```
100+ UI 风格    # Glassmorphism, Neumorphism, Brutalism, Bento Grid, etc.
150+ 配色方案   # 预设调色板 + 自动生成单色/类比/互补/三色配色
80+ 字体组合    # Display + Body + Accent + Mono 组合
200+ 组件库     # Button, Input, Card, Navigation, etc.
50+ 布局模式    # Grid, Masonry, Bento, Split Screen, etc.
60+ 动画效果    # Easing, Stagger, Parallax, Morphing, etc.
```

#### 美学方向 (26+ 种)

```
极简方向: brutalist_minimal, japanese_zen, scandinavian, swiss_international
极繁方向: maximalist_chaos, memphis_group, pop_art, vaporwave
复古未来: retro_futurism, cyberpunk, art_deco, steampunk
自然有机: organic_natural, biophilic, earthy, botanical
奢华精致: luxury_refined, french_elegance, italian_sophistication, artisanal
俏皮趣味: playful_toy, kawaii, whimsical, neon_pop
编辑杂志: editorial_magazine, typography_centric, grid_breaking
原始工业: raw_industrial, utilitarian, grunge, post_apocalyptic
柔和梦幻: soft_pastel, dreamy, ethereal, glass_morphism
```

#### 使用示例

```bash
# 搜索设计资产（支持多域搜索）
super-dev design search "glass" --domain style -n 5
super-dev design search "blue" --domain color -n 10
super-dev design search "minimal" --domain layout -n 3

# 生成完整设计系统
super-dev design generate \
  --product SaaS \
  --industry Fintech \
  --keywords "professional,trust,secure" \
  --platform web

# 生成 design tokens
super-dev design tokens \
  --primary #3B82F6 \
  --type monochromatic \
  --format css
```

#### 输出示例

**设计系统生成** (CSS 变量):
```css
:root {
  /* Colors */
  --color-primary: #3B82F6;
  --color-secondary: #1E40AF;
  --color-accent: #F59E0B;
  --color-background: #FFFFFF;
  --color-surface: #F9FAFB;
  --color-text: #111827;
  --color-text-secondary: #6B7280;

  /* Typography */
  --font-display: 'Space Grotesk';
  --font-body: 'Plus Jakarta Sans';

  /* Spacing (8pt grid) */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
  --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
}
```

**Tailwind 配置**:
```json
{
  "theme": {
    "extend": {
      "colors": {
        "primary": "#3B82F6",
        "secondary": "#1E40AF",
        "accent": "#F59E0B"
      },
      "fontFamily": {
        "display": ["Space Grotesk", "sans-serif"],
        "body": ["Plus Jakarta Sans", "sans-serif"]
      }
    }
  }
}
```

---

## 快速开始

### 安装

```bash
# 从 GitHub 克隆源码
git clone https://github.com/shangyankeji/super-dev.git
cd super-dev

# 安装依赖
pip install -e .
```

### 环境要求

- Python 3.10+
- 现代终端 (支持 ANSI 颜色)

### 核心使用：从想法到部署

#### 方式 1: 完整流水线 (推荐)

```bash
# 一句话 → 完整项目资产 (8 阶段)
super-dev pipeline "用户认证系统" \
  --platform web \
  --frontend react \
  --backend node \
  --cicd github \
  --quality-threshold 80
```

**自动生成**:
```
output/
├── 用户认证系统-prd.md                    # PRD 文档
├── 用户认证系统-architecture.md          # 架构设计
├── 用户认证系统-uiux.md                  # UI/UX 设计
├── 用户认证系统-redteam.md               # 红队审查报告
├── 用户认证系统-quality-gate.md          # 质量门禁报告
├── 用户认证系统-code-review.md           # 代码审查指南
├── 用户认证系统-ai-prompt.md             # AI 提示词
└── ...
.super-dev/changes/用户认证系统/
├── proposal.md                            # 变更提案
├── tasks.md                               # 任务清单
└── specs/                                 # 规范定义
.github/workflows/
├── ci.yml                                 # CI 配置
└── cd.yml                                 # CD 配置
prisma/
├── schema.prisma                          # 数据库模型
└── migrations/                            # 迁移脚本
```

#### 方式 2: 一键创建项目

```bash
# 生成文档 + Spec + AI 提示词
super-dev create "用户认证系统" \
  --platform web \
  --frontend react \
  --backend node \
  --domain auth
```

#### 方式 3: 分步创建

```bash
# 1. 初始化项目
super-dev init todo-app \
  --platform web \
  --frontend react \
  --backend node

# 2. 编辑配置
vim super-dev.yaml

# 3. 运行工作流
super-dev workflow
```

### Claude Code Skill 集成

```bash
# 安装到 Claude Code
./install.sh

# 在 Claude Code 中使用
直接告诉 Claude："帮我用 Super Dev 分析这个项目"
```

---

## 命令参考

### pipeline - 完整流水线

```bash
super-dev pipeline "功能描述" [选项]

选项:
  -p, --platform {web,mobile,wechat,desktop}
                        目标平台 (默认: web)
  -f, --frontend {react,vue,angular,svelte,none}
                        前端框架 (默认: react)
  -b, --backend {node,python,go,java,none}
                        后端框架 (默认: node)
  -d, --domain {fintech,ecommerce,medical,social,iot,education,auth,content}
                        业务领域
  --name NAME           项目名称 (默认根据描述生成)
  --cicd {github,gitlab,jenkins,azure,bitbucket}
                        CI/CD 平台 (默认: github)
  --skip-redteam        跳过红队审查
  --quality-threshold N 质量门禁阈值 (默认: 80)

示例:
  super-dev pipeline "电商购物车"
  super-dev pipeline "用户登录" --platform wechat --cicd gitlab
```

### create - 一键创建项目

```bash
super-dev create "功能描述" [选项]

选项:
  -p, --platform       目标平台
  -f, --frontend       前端框架
  -b, --backend        后端框架
  -d, --domain         业务领域
  --name NAME          项目名称
  --skip-docs          跳过文档生成，只创建 Spec
```

### spec - Spec 管理

```bash
# 初始化 SDD 目录结构
super-dev spec init

# 列出所有变更
super-dev spec list

# 显示变更详情
super-dev spec show <change-id>

# 创建变更提案
super-dev spec propose <change-id> --title "标题" --description "描述"

# 添加需求
super-dev spec add-req <change-id> <component> <requirement-id> "需求描述"

# 验证规格格式
super-dev spec validate              # 验证所有变更
super-dev spec validate <change-id>  # 验证单个变更
super-dev spec validate -v           # 显示详细信息

# 交互式仪表板
super-dev spec view                  # 显示所有规范和变更的仪表板

# 归档变更
super-dev spec archive <change-id>
```

### design - 设计智能引擎

```bash
# ===== 搜索设计资产 =====
super-dev design search "查询词" [选项]

选项:
  -d, --domain {style,color,typography,component,layout,animation,ux,chart,product,stack}
                        搜索域 (默认: 自动检测)
  -n, --max-results N   最大结果数 (默认: 5)
  --fuzzy               启用模糊匹配
  --format {table,json,detailed}
                        输出格式 (默认: table)

示例:
  super-dev design search "glass"              # 搜索 glassmorphism 风格
  super-dev design search "blue" --domain color # 搜索蓝色配色
  super-dev design search "minimal" -n 10       # 获取 10 个结果

# ===== 生成完整设计系统 =====
super-dev design generate [选项]

选项:
  --product {SaaS,Mobile,E-commerce,Dashboard,Portfolio,Landing,Blog,Marketplace}
                        产品类型 (必需)
  --industry {Fintech,Healthcare,Education,E-commerce,Social,Media,Travel,RealEstate}
                        行业领域 (必需)
  --keywords KEYWORDS   关键词 (逗号分隔)
  --platform {web,mobile,wechat,desktop}
                        目标平台 (默认: web)
  --aesthetic AESTHETIC 美学方向 (见下方列表)
  -o, --output DIR      输出目录 (默认: ./design-system)

示例:
  super-dev design generate --product SaaS --industry Fintech
  super-dev design generate --product E-commerce --industry Retail --keywords "vibrant,energetic"
  super-dev design generate --product Dashboard --industry Healthcare --aesthetic brutalist_minimal

# ===== 生成 Design Tokens =====
super-dev design tokens [选项]

选项:
  --primary COLOR       主色调 (必需，格式: #RRGGBB)
  --type {monochromatic,analogous,complementary,triadic,split_complementary,tetradic}
                        配色类型 (默认: monochromatic)
  --format {css,json,tailwind}
                        输出格式 (默认: css)
  -o, --output FILE     输出文件 (默认: stdout)

示例:
  super-dev design tokens --primary #3B82F6
  super-dev design tokens --primary #10B981 --type analogous --format tailwind
  super-dev design tokens --primary #FF6B6B --type complementary -o tokens.json

# ===== 美学方向列表 =====
可用美学方向 (26+ 种):

极简方向:
  brutalist_minimal    - 原始极简主义
  japanese_zen         - 日式禅意
  scandinavian         - 北欧风格
  swiss_international  - 瑞士国际主义

极繁方向:
  maximalist_chaos     - 极繁混乱
  memphis_group        - 孟菲斯集团
  pop_art              - 波普艺术
  vaporwave            - 蒸汽波

复古未来:
  retro_futurism       - 复古未来主义
  cyberpunk            - 赛博朋克
  art_deco             - 装饰艺术
  steampunk            - 蒸汽朋克

自然有机:
  organic_natural      - 有机自然
  biophilic            - 亲生物设计
  earthy               - 大土色调
  botanical            - 植物学

奢华精致:
  luxury_refined       - 奢华精致
  french_elegance      - 法式优雅
  italian_sophistication - 意式精致
  artisanal            - 手工艺

俏皮趣味:
  playful_toy          - 俏皮玩具
  kawaii               - 卡哇伊
  whimsical            - 异想天开
  neon_pop             - 霓虹流行

编辑杂志:
  editorial_magazine   - 编辑杂志
  typography_centric   - 排版中心
  grid_breaking        - 打破网格

原始工业:
  raw_industrial       - 原始工业
  utilitarian          - 实用主义
  grunge               - 垃圾摇滚
  post_apocalyptic     - 末日后

柔和梦幻:
  soft_pastel          - 柔和粉彩
  dreamy               - 梦幻
  ethereal             - 空灵
  glass_morphism       - 玻璃态
```

### expert - 调用专家

```bash
# 列出所有可用专家
super-dev expert --list

# 调用特定专家
super-dev expert PM "帮我写一个电商平台的 PRD"
super-dev expert ARCHITECT "设计高并发架构"
super-dev expert SECURITY "审查安全方案"
```

### 其他命令

```bash
# 初始化项目
super-dev init <name> [选项]

# 分析现有项目
super-dev analyze [path] [选项]

# 质量检查
super-dev quality --type {prd,architecture,ui,ux,code,all}

# 生成部署配置
super-dev deploy --docker --cicd {github,gitlab,jenkins,azure,bitbucket}

# 生成 UI 原型
super-dev preview -o output.html

# 运行交互式工作流
super-dev workflow [--phase ...]

# 配置管理
super-dev config {get,set,list} [key] [value]
```

---

## 示例

### 示例 1: 用户认证系统

```bash
super-dev pipeline "用户认证系统" \
  --platform web \
  --frontend react \
  --backend node \
  --cicd github
```

### 示例 2: 电商平台

```bash
super-dev pipeline "电商平台购物车" \
  --platform web \
  --frontend vue \
  --backend python \
  --domain ecommerce \
  --cicd gitlab
```

### 示例 3: 微信小程序

```bash
super-dev create "点餐小程序" \
  --platform wechat \
  --domain auth
```

### 示例 4: Spec-Driven Development

```bash
# 1. 初始化 SDD
super-dev spec init

# 2. 创建变更提案
super-dev spec propose add-user-auth \
  --title "Add User Authentication" \
  --description "Implement JWT-based user authentication"

# 3. 添加需求
super-dev spec add-req add-user-auth auth user-registration \
  "The system SHALL allow user registration with email and password"

# 4. 查看变更
super-dev spec show add-user-auth

# 5. 完成后归档
super-dev spec archive add-user-auth
```

### 示例 5: 设计智能引擎

```bash
# 搜索 Glassmorphism 风格
super-dev design search "glass" --domain style -n 5

# 生成 SaaS Fintech 设计系统
super-dev design generate \
  --product SaaS \
  --industry Fintech \
  --keywords "professional,trust,secure" \
  --platform web

# 生成单色配色 tokens
super-dev design tokens --primary #3B82F6 --type monochromatic

# 生成赛博朋克风格设计系统
super-dev design generate \
  --product Dashboard \
  --industry Gaming \
  --aesthetic cyberpunk \
  -o ./design-system
```

---


## 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 联系方式

- **GitHub**: https://github.com/shangyankeji/super-dev
- **Issues**: https://github.com/shangyankeji/super-dev/issues
- **Email**: 11964948@qq.com

---

<div align="center">

**如果这个项目对你有帮助，请给一个 Star！**

Made with passion by [Excellent](https://github.com/shangyankeji)

</div>
