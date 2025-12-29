# Super Dev 完整流水线工作流

使用 Super Dev 的 8 阶段流水线从想法到部署。

## 快速开始

```bash
# 一句话生成完整项目资产
super-dev pipeline "用户认证系统" \
  --platform web \
  --frontend react \
  --backend node \
  --cicd github \
  --quality-threshold 80
```

## 8 阶段流水线

```
想法 → 文档 → Spec → 红队 → 质量门 → 审查 → AI 提示 → CI/CD
```

### 阶段 1: 文档生成

自动生成 PRD、架构设计、UI/UX 设计：

```bash
super-dev pipeline "功能描述"
```

**输出：**
- `<name>-prd.md` - 产品需求文档
- `<name>-architecture.md` - 架构设计文档
- `<name>-uiux.md` - UI/UX 设计文档

### 阶段 2: Spec 规范

创建 OpenSpec 风格的规范：

```bash
super-dev spec init
super-dev spec propose <change-id>
```

### 阶段 3: 红队审查

安全、性能、架构审查：

```bash
# 红队审查已自动生成
# 查看 <name>-redteam.md
```

### 阶段 4: 质量门禁

自动评分，80+ 分通过：

```bash
# 质量报告已自动生成
# 查看 <name>-quality-gate.md
```

### 阶段 5: 代码审查指南

生成代码审查检查清单：

```bash
# 审查指南已自动生成
# 查看 <name>-code-review.md
```

### 阶段 6: AI 提示词

生成 AI 实现提示词：

```bash
# AI 提示词已自动生成
# 查看 <name>-ai-prompt.md
```

### 阶段 7: CI/CD 配置

生成 CI/CD 配置文件：

```bash
super-dev deploy --cicd github
```

**支持的平台：**
- GitHub Actions
- GitLab CI
- Jenkins
- Azure DevOps
- Bitbucket Pipelines

### 阶段 8: 数据库迁移

生成 ORM 迁移脚本：

```bash
# 支持 6 种 ORM
--orm prisma     # Prisma
--orm typeorm    # TypeORM
--orm sequelize  # Sequelize
--orm sqlalchemy # SQLAlchemy
--orm django     # Django ORM
--orm mongoose   # Mongoose
```

## 专家系统集成

调用 11 位专家协助：

```bash
# 列出所有专家
super-dev expert --list

# 调用产品经理
super-dev expert PM "帮我写一个电商平台的 PRD"

# 调用架构师
super-dev expert ARCHITECT "设计高并发架构"

# 调用安全专家
super-dev expert SECURITY "审查安全方案"
```

## AI 工具使用

### 在 Claude Code 中

```bash
# 1. 安装 Super Dev
pip install super-dev

# 2. 生成项目资产
super-dev create "功能描述" --platform web --frontend react

# 3. 告诉 Claude
"请查看 output/ 目录中的文档和规范，然后实现这个功能"
```

### 直接命令

```bash
# 分析现有项目
super-dev analyze

# 运行交互式工作流
super-dev workflow

# 查看仪表板
super-dev spec view
```

## 配置文件

项目配置：`super-dev.yaml`

```yaml
project:
  name: my-app
  platform: web
  frontend: react
  backend: node

domain: ecommerce

quality:
  threshold: 80

cicd:
  platform: github

database:
  orm: prisma
```

## 输出目录结构

```
output/
├── <name>-prd.md
├── <name>-architecture.md
├── <name>-uiux.md
├── <name>-redteam.md
├── <name>-quality-gate.md
├── <name>-code-review.md
└── <name>-ai-prompt.md

.super-dev/
├── specs/
├── changes/
└── archive/

.github/workflows/
├── ci.yml
└── cd.yml

prisma/
├── schema.prisma
└── migrations/
```
