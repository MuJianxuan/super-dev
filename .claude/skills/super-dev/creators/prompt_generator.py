# -*- coding: utf-8 -*-
"""
AI 提示词生成器 - 生成可直接给 AI 的提示词

开发：Excellent（11964948@qq.com）
功能：将 Spec 转换为 AI 可理解的提示词
作用：用户复制给 AI 即可开始开发
创建时间：2025-12-30
"""

from pathlib import Path
from typing import Optional


class AIPromptGenerator:
    """AI 提示词生成器"""

    def __init__(self, project_dir: Path, name: str):
        """初始化提示词生成器"""
        self.project_dir = Path(project_dir).resolve()
        self.name = name

    def generate(self) -> str:
        """生成 AI 提示词"""
        # 读取项目配置
        import yaml
        config_path = self.project_dir / "super-dev.yaml"
        project_config = {}
        if config_path.exists():
            with open(config_path, 'r') as f:
                project_config = yaml.safe_load(f)

        # 读取生成的文档
        prd_content = self._read_document('prd')
        arch_content = self._read_document('architecture')
        uiux_content = self._read_document('uiux')

        # 读取 Spec 变更
        change_content = self._read_change_spec()

        # 组装提示词
        prompt = f"""# {self.name} - AI 开发提示词

> 由 Super Dev 自动生成
> 生成时间: {self._get_timestamp()}

---

## 📋 项目概述

**项目名称**: {self.name}
**项目描述**: {project_config.get('description', '见 PRD 文档')}
**目标平台**: {project_config.get('platform', 'web').upper()}
**技术栈**:
- 前端: {project_config.get('frontend', 'react')}
- 后端: {project_config.get('backend', 'node')}

---

## 🎯 你的任务

请根据以下规范和文档，实现 {self.name} 的所有功能。

**重要**:
1. **严格按照任务列表顺序实现**
2. **每完成一个任务，标记为 [x]**
3. **遵循规范中的所有要求**
4. **参考架构文档中的技术选型**

---

## 📄 核心文档

### 1. PRD (产品需求文档)

{prd_content[:1000] if prd_content else '请查看 output/{self.name}-prd.md'}
...

### 2. 架构设计文档

{arch_content[:1000] if arch_content else '请查看 output/{self.name}-architecture.md'}
...

### 3. UI/UX 设计文档

{uiux_content[:1000] if uiux_content else '请查看 output/{self.name}-uiux.md'}
...

---

## ✅ 任务列表

{change_content}

---

## 🔧 开发规范

### 代码规范

1. **遵循项目代码风格**
   - 使用 Prettier 格式化
   - 使用 ESLint 检查
   - 遵循现有命名规范

2. **提交规范**
   - Conventional Commits
   - 一个功能一个 commit
   - Commit message 清晰描述变更

3. **测试规范**
   - 单元测试覆盖率 > 80%
   - 每个功能点都有测试
   - 使用 pytest / jest

### 安全规范

1. **输入验证**: 所有用户输入必须验证
2. **SQL 注入**: 使用参数化查询
3. **XSS**: 输出转义
4. **认证**: JWT Token 认证

---

## 📂 文件结构

请按照以下结构组织代码：

```
project-root/
├── frontend/          # 前端代码
│   ├── src/
│   │   ├── components/  # 组件
│   │   ├── pages/       # 页面
│   │   ├── services/    # API 服务
│   │   └── utils/       # 工具函数
│   ├── package.json
│   └── vite.config.js
│
├── backend/           # 后端代码
│   ├── src/
│   │   ├── controllers/ # 控制器
│   │   ├── models/      # 数据模型
│   │   ├── services/    # 业务逻辑
│   │   ├── routes/      # 路由
│   │   └── utils/       # 工具函数
│   ├── package.json
│   └── tsconfig.json
│
└── shared/            # 共享代码
    ├── types/         # 类型定义
    └── constants/     # 常量
```

---

## 🚀 开始实现

请从任务 1.1 开始，按顺序实现所有任务。

**每完成一个任务**:
1. 更新 `.super-dev/changes/{self.name}/tasks.md`
2. 将任务标记为 [x] 完成状态
3. 提交代码 (可选)
4. 继续下一个任务

---

## ❓ 遇到问题？

如果遇到不清楚的地方：
1. 优先查看架构文档
2. 参考 PRD 中的需求说明
3. 查看 UI/UX 文档中的设计规范

---

## ✨ 完成标准

所有任务完成后：
- [ ] 所有功能正常运行
- [ ] 所有测试通过
- [ ] 代码符合规范
- [ ] 文档已更新

**祝开发顺利！🚀**
"""

        return prompt

    def _read_document(self, doc_type: str) -> Optional[str]:
        """读取生成的文档"""
        doc_path = self.project_dir / "output" / f"{self.name}-{doc_type}.md"
        if doc_path.exists():
            return doc_path.read_text(encoding="utf-8")
        return None

    def _read_change_spec(self) -> str:
        """读取 Spec 变更内容"""
        from ..specs import ChangeManager

        change_manager = ChangeManager(self.project_dir)
        changes = change_manager.list_changes()

        if not changes:
            return "暂无 Spec，请先运行 super-dev spec init"

        change = changes[0]  # 获取最新的变更

        content = f"""
### 变更: {change.id}

**描述**: {change.title}

**状态**: {change.status.value}

#### 任务列表
"""

        for task in change.tasks:
            checkbox = "[x]" if task.status == TaskStatus.COMPLETED else "[ ]"
            content += f"\n{checkbox} **{task.id}: {task.title}**\n"
            if task.description:
                content += f"  - {task.description}\n"
            if task.spec_refs:
                content += f"  - 规范引用: {', '.join(task.spec_refs)}\n"

        if change.spec_deltas:
            content += "\n#### 规范要求\n"
            for delta in change.spec_deltas:
                content += f"\n**{delta.spec_name}** ({delta.delta_type.value})\n"
                for req in delta.requirements:
                    content += f"- {req.name}: {req.description}\n"
                    for scenario in req.scenarios:
                        content += f"  - {scenario.when}: {scenario.then}\n"

        return content

    def _get_timestamp(self) -> str:
        """获取时间戳"""
        from datetime import datetime
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
