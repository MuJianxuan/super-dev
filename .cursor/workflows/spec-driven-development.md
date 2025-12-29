# Spec-Driven Development Workflow for Cursor

使用 Super Dev 在 Cursor 中进行规范驱动开发 (SDD)。

## 快速开始

1. 安装 Super Dev：
```bash
pip install super-dev
```

2. 初始化项目：
```bash
super-dev spec init
```

3. 在 Cursor 中使用 `.cursor` 指令调用工作流

## 工作流步骤

### Step 1: Create Proposal

在 Cursor 终端：
```bash
super-dev spec propose add-feature --title "Add Feature" --description "Description"
```

### Step 2: Edit Specs

在 Cursor 编辑器中打开：
```
.super-dev/changes/add-feature/specs/*/spec.md
```

使用 Delta 格式编辑：

```markdown
## ADDED

### Requirement: Feature Name

The system SHALL provide feature X.

#### Scenario: Success Case

Given condition A
When action B
Then result C
```

### Step 3: Validate

在 Cursor 中运行：
```bash
super-dev spec validate add-feature
```

### Step 4: View Dashboard

```bash
super-dev spec view
```

### Step 5: Implement

在 Cursor Chat 中：
```
请实现以下规范：

```bash
super-dev spec show add-feature --full
```

请按照规范中的 SHALL/MUST/SHOULD/MAY 要求实现。
```

### Step 6: Archive

```bash
super-dev spec archive add-feature
```

## Cursor 指令

在 Cursor Chat 中使用这些指令：

### 查看规范
```
.spec 请列出当前所有变更
```

### 验证规范
```
.spec 请验证 add-feature 变更的格式
```

### 实现需求
```
.spec 请实现 add-feature 中定义的需求
```

### 检查代码符合性
```
.spec 请检查当前代码是否符合 add-feature 规范
```

## Super Dev 命令参考

```bash
# Spec 管理
super-dev spec init              # 初始化
super-dev spec list              # 列出变更
super-dev spec show <id>         # 显示详情
super-dev spec validate [id]     # 验证格式
super-dev spec view              # 仪表板
super-dev spec archive <id>      # 归档变更

# 项目管理
super-dev create "描述"          # 创建项目
super-dev pipeline "描述"        # 完整流水线
super-dev analyze                # 分析项目

# 专家系统
super-dev expert --list          # 列出专家
super-dev expert PM "提示词"     # 调用专家
```

## 关键词指南

规范中使用标准关键词：

| 关键词 | 用途 | 示例 |
|--------|------|------|
| SHALL | 强制要求 | The system SHALL authenticate users |
| MUST | 技术约束 | Password MUST be 12+ characters |
| SHOULD | 推荐做法 | Response time SHOULD be < 200ms |
| MAY | 可选功能 | The system MAY cache results |

## 项目结构

```
.super-dev/
├── specs/              # 当前规范
│   └── component/
│       └── spec.md
├── changes/            # 工作变更
│   └── change-id/
│       ├── proposal.md
│       ├── tasks.md
│       ├── design.md
│       └── specs/      # Delta 规格
│           └── component/
│               └── spec.md
└── archive/            # 已完成变更
```

## Delta 格式

spec.md 使用 Delta 格式描述变更：

```markdown
## ADDED

### Requirement: New Requirement

The system SHALL do X.

## MODIFIED

### Requirement: Existing Requirement

Updated to also do Y.

## REMOVED

### Requirement: Old Requirement

This requirement is removed.
```

## 最佳实践

1. **规范先行** - 在编写代码前先写好规范
2. **使用标准关键词** - 确保需求级别清晰
3. **包含场景** - 使用 Given-When-Then 格式
4. **验证格式** - 每次修改后运行 validate
5. **及时归档** - 完成后归档变更

## 与 Cursor Composer 集成

在 Cursor Composer 中：

1. 创建规范：
```bash
super-dev spec propose my-feature --title "My Feature"
```

2. 编辑规范文件，让 Composer 读取：
```
请阅读 .super-dev/changes/my-feature/ 中的规范文件
```

3. 实现代码：
```
请按照规范实现功能，确保满足所有 SHALL/MUST 要求
```

4. 验证：
```bash
super-dev spec validate my-feature
```

## 故障排除

### 验证失败
```bash
super-dev spec validate <id> -v  # 详细输出
```

### 找不到变更
```bash
super-dev spec list
```

### 格式问题
检查规范包含：
- 一级标题
- Purpose 部分
- Requirements 部分
- `### Requirement:` 格式
- SHALL/MUST/SHOULD/MAY 关键词
