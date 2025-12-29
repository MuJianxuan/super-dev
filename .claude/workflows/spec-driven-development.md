# Spec-Driven Development Workflow

使用 Super Dev 进行规范驱动开发 (SDD)，类似 OpenSpec 工作流。

## 工作流程

```
Draft Change → Review & Align → Implement → Archive
```

## 步骤说明

### 1. Draft Change (起草变更)

使用 CLI 创建变更提案：

```bash
# 初始化 SDD 项目结构（首次使用）
super-dev spec init

# 创建新的变更提案
super-dev spec propose add-user-auth \
  --title "Add User Authentication" \
  --description "Implement JWT-based user authentication with OAuth2"
```

这会创建以下结构：
```
.super-dev/changes/add-user-auth/
├── proposal.md      # 变更提案
├── tasks.md         # 任务清单
├── design.md        # 设计文档（可选）
└── specs/           # 规范增量
    └── auth/
        └── spec.md  # Delta 格式 (ADDED/MODIFIED/REMOVED)
```

### 2. Review & Align (审查与对齐)

与 AI 协作完善规范：

```bash
# 查看变更详情
super-dev spec show add-user-auth

# 添加需求到规范
super-dev spec add-req add-user-auth auth user-registration \
  "The system SHALL allow user registration with email and password"
```

**Delta 格式示例** (specs/auth/spec.md)：

```markdown
## ADDED

### Requirement: User Registration

The system SHALL allow user registration with the following constraints:

- Email MUST be unique across all users
- Password MUST be at least 12 characters with complexity requirements
- Email verification MUST be completed before account activation

#### Scenario: Successful Registration

Given a user provides valid email and password
When the user submits registration
Then the system SHOULD create a pending account
And send a verification email

## MODIFIED

### Requirement: Session Management

Updated to support JWT tokens with 15-minute expiration...
```

### 3. 验证规范

```bash
# 验证单个变更
super-dev spec validate add-user-auth

# 验证所有变更
super-dev spec validate

# 查看仪表板
super-dev spec view
```

### 4. Implement (实现)

告诉 AI 实现规范：

**提示词模板：**
```
请实现以下规范变更：

```bash
super-dev spec show add-user-auth --full
```

请按照规范中的需求 (SHALL/MUST/SHOULD/MAY) 和场景 (Scenario) 实现功能。
```

### 5. Archive (归档)

实现完成后：

```bash
# 归档变更，更新源规范
super-dev spec archive add-user-auth
```

## 关键关键词

| 关键词 | 含义 | 用法 |
|--------|------|------|
| SHALL | 强制要求 | 必须实现的功能 |
| MUST | 强制约束 | 技术或安全约束 |
| SHOULD | 推荐做法 | 强烈建议但可有例外 |
| MAY | 可选功能 | 可选实现 |

## AI 集成命令

### Claude Code 使用

```
# 列出所有变更
请运行：super-dev spec list

# 查看变更详情
请运行：super-dev spec show <change-id>

# 验证规范格式
请运行：super-dev spec validate

# 显示仪表板
请运行：super-dev spec view
```

### 最佳实践

1. **先写规范，后写代码** - 确保在编码前达成共识
2. **使用标准关键词** - SHALL/MUST/SHOULD/MAY 明确需求级别
3. **包含场景** - 使用 Given-When-Then 格式描述行为
4. **验证格式** - 每次修改后运行 validate 命令
5. **归档已完成** - 及时归档已实现的变更

## 目录结构

```
.super-dev/
├── specs/          # 当前规范（单一事实源）
│   └── auth/
│       └── spec.md
├── changes/        # 提议的变更
│   └── add-user-auth/
│       ├── proposal.md
│       ├── tasks.md
│       ├── design.md
│       └── specs/
│           └── auth/
│               └── spec.md  # Delta
└── archive/        # 已归档的变更
```

## 故障排除

### 问题：验证失败

```bash
# 查看详细错误信息
super-dev spec validate <change-id> -v
```

### 问题：找不到变更

```bash
# 列出所有变更
super-dev spec list
```

### 问题：规范格式错误

检查以下内容：
- 一级标题是否存在
- Purpose 部分是否存在
- Requirements 部分是否存在
- 需求格式: `### Requirement: <名称>`
- 场景格式: `#### Scenario: <描述>`
- 使用 SHALL/MUST/SHOULD/MAY 关键词
