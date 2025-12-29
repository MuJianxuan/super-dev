# -*- coding: utf-8 -*-
"""
红队审查器 - 安全、性能、架构审查

开发：Excellent（11964948@qq.com）
功能：模拟红队视角，全面审查项目安全性、性能和架构
作用：在开发前发现问题，确保质量
创建时间：2025-12-30
"""

from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class SecurityIssue:
    """安全问题"""
    severity: str  # critical, high, medium, low
    category: str  # injection, auth, xss, csrf, etc.
    description: str
    recommendation: str
    cwe: Optional[str] = None


@dataclass
class PerformanceIssue:
    """性能问题"""
    severity: str  # critical, high, medium, low
    category: str  # database, api, frontend, infrastructure
    description: str
    recommendation: str
    impact: str = ""


@dataclass
class ArchitectureIssue:
    """架构问题"""
    severity: str  # critical, high, medium, low
    category: str  # scalability, maintainability, reliability
    description: str
    recommendation: str
    adr_needed: bool = False


@dataclass
class RedTeamReport:
    """红队审查报告"""
    project_name: str
    security_issues: list[SecurityIssue] = field(default_factory=list)
    performance_issues: list[PerformanceIssue] = field(default_factory=list)
    architecture_issues: list[ArchitectureIssue] = field(default_factory=list)

    @property
    def critical_count(self) -> int:
        return (
            sum(1 for i in self.security_issues if i.severity == "critical") +
            sum(1 for i in self.performance_issues if i.severity == "critical") +
            sum(1 for i in self.architecture_issues if i.severity == "critical")
        )

    @property
    def high_count(self) -> int:
        return (
            sum(1 for i in self.security_issues if i.severity == "high") +
            sum(1 for i in self.performance_issues if i.severity == "high") +
            sum(1 for i in self.architecture_issues if i.severity == "high")
        )

    @property
    def total_score(self) -> int:
        """计算总分 (0-100)"""
        base_score = 100

        # 扣分标准
        for issue in self.security_issues:
            if issue.severity == "critical":
                base_score -= 20
            elif issue.severity == "high":
                base_score -= 10
            elif issue.severity == "medium":
                base_score -= 5
            else:
                base_score -= 2

        for issue in self.performance_issues:
            if issue.severity == "critical":
                base_score -= 15
            elif issue.severity == "high":
                base_score -= 8
            elif issue.severity == "medium":
                base_score -= 4
            else:
                base_score -= 1

        for issue in self.architecture_issues:
            if issue.severity == "critical":
                base_score -= 15
            elif issue.severity == "high":
                base_score -= 8
            elif issue.severity == "medium":
                base_score -= 4
            else:
                base_score -= 1

        return max(0, base_score)

    def to_markdown(self) -> str:
        """生成 Markdown 报告"""
        lines = [
            f"# {self.project_name} - 红队审查报告",
            "",
            f"> **审查时间**: 自动生成",
            f"> **总分**: {self.total_score}/100",
            "",
            "---",
            "",
            "## 执行摘要",
            "",
            f"- **Critical 问题**: {self.critical_count}",
            f"- **High 问题**: {self.high_count}",
            f"- **总分**: {self.total_score}/100",
            "",
        ]

        if self.total_score < 60:
            lines.append("**状态**: 未通过质量门禁 - 需要修复关键问题后重新审查")
        elif self.total_score < 80:
            lines.append("**状态**: 有条件通过 - 建议修复 High 级别问题")
        else:
            lines.append("**状态**: 通过 - 质量良好")

        lines.extend(["", "---", ""])

        # 安全审查
        lines.extend([
            "## 1. 安全审查",
            "",
        ])

        if not self.security_issues:
            lines.append("未发现明显的安全问题。")
        else:
            lines.append("| 严重性 | 类别 | 描述 | 建议 |")
            lines.append("|:---|:---|:---|:---|")
            for issue in self.security_issues:
                cwe_ref = f" ({issue.cwe})" if issue.cwe else ""
                lines.append(
                    f"| {issue.severity} | {issue.category}{cwe_ref} | {issue.description} | {issue.recommendation} |"
                )

        lines.extend(["", "---", ""])

        # 性能审查
        lines.extend([
            "## 2. 性能审查",
            "",
        ])

        if not self.performance_issues:
            lines.append("未发现明显的性能问题。")
        else:
            lines.append("| 严重性 | 类别 | 描述 | 影响 | 建议 |")
            lines.append("|:---|:---|:---|:---|:---|")
            for issue in self.performance_issues:
                lines.append(
                    f"| {issue.severity} | {issue.category} | {issue.description} | {issue.impact} | {issue.recommendation} |"
                )

        lines.extend(["", "---", ""])

        # 架构审查
        lines.extend([
            "## 3. 架构审查",
            "",
        ])

        if not self.architecture_issues:
            lines.append("未发现明显的架构问题。")
        else:
            lines.append("| 严重性 | 类别 | 描述 | 需要 ADR | 建议 |")
            lines.append("|:---|:---|:---|:---:|:---|")
            for issue in self.architecture_issues:
                adr = "是" if issue.adr_needed else "否"
                lines.append(
                    f"| {issue.severity} | {issue.category} | {issue.description} | {adr} | {issue.recommendation} |"
                )

        lines.extend(["", "---", ""])

        # 改进建议
        lines.extend([
            "## 4. 改进建议",
            "",
            "### 优先级 P0 (立即修复)",
            "",
        ])

        p0_issues = [
            i for i in self.security_issues + self.performance_issues + self.architecture_issues
            if i.severity in ("critical", "high")
        ]

        if not p0_issues:
            lines.append("无 P0 级别问题。")
        else:
            for idx, issue in enumerate(p0_issues, 1):
                issue_type = "安全" if issue in self.security_issues else "性能" if issue in self.performance_issues else "架构"
                lines.append(f"{idx}. [{issue_type}] {issue.description}")
                lines.append(f"   - 建议: {issue.recommendation}")
                lines.append("")

        lines.extend([
            "### 优先级 P1 (尽快修复)",
            "",
        ])

        p1_issues = [
            i for i in self.security_issues + self.performance_issues + self.architecture_issues
            if i.severity == "medium"
        ]

        if not p1_issues:
            lines.append("无 P1 级别问题。")
        else:
            for idx, issue in enumerate(p1_issues, 1):
                issue_type = "安全" if issue in self.security_issues else "性能" if issue in self.performance_issues else "架构"
                lines.append(f"{idx}. [{issue_type}] {issue.description}")
                lines.append(f"   - 建议: {issue.recommendation}")
                lines.append("")

        return "\n".join(lines)


class RedTeamReviewer:
    """红队审查器"""

    def __init__(self, project_dir: Path, name: str, tech_stack: dict):
        self.project_dir = Path(project_dir).resolve()
        self.name = name
        self.tech_stack = tech_stack
        self.platform = tech_stack.get("platform", "web")
        self.frontend = tech_stack.get("frontend", "react")
        self.backend = tech_stack.get("backend", "node")
        self.domain = tech_stack.get("domain", "")

    def review(self) -> RedTeamReport:
        """执行完整红队审查"""
        report = RedTeamReport(project_name=self.name)

        # 安全审查
        report.security_issues = self._review_security()

        # 性能审查
        report.performance_issues = self._review_performance()

        # 架构审查
        report.architecture_issues = self._review_architecture()

        return report

    def _review_security(self) -> list[SecurityIssue]:
        """安全审查"""
        issues = []

        # 认证安全
        if self.backend != "none":
            issues.extend([
                SecurityIssue(
                    severity="high",
                    category="认证",
                    description="确保使用 JWT 或 Session 进行身份验证",
                    recommendation="实施基于 Token 的认证，使用 RS256 算法签名",
                    cwe="CWE-287"
                ),
                SecurityIssue(
                    severity="critical",
                    category="密码存储",
                    description="密码必须使用强哈希算法存储",
                    recommendation="使用 bcrypt (cost>=10) 或 Argon2 存储密码",
                    cwe="CWE-256"
                ),
                SecurityIssue(
                    severity="high",
                    category="密码策略",
                    description="实施强密码策略",
                    recommendation="最小长度 8 位，包含大小写字母、数字和特殊字符",
                    cwe="CWE-521"
                ),
            ])

        # 输入验证
        issues.extend([
            SecurityIssue(
                severity="critical",
                category="注入",
                description="防止 SQL 注入攻击",
                recommendation="使用参数化查询或 ORM，禁止字符串拼接 SQL",
                cwe="CWE-89"
            ),
            SecurityIssue(
                severity="high",
                category="注入",
                description="防止 XSS 攻击",
                recommendation="对所有用户输入进行转义，使用 CSP 头",
                cwe="CWE-79"
            ),
            SecurityIssue(
                severity="high",
                category="CSRF",
                description="防止 CSRF 攻击",
                recommendation="实施 CSRF Token 验证，使用 SameSite Cookie",
                cwe="CWE-352"
            ),
        ])

        # API 安全
        if self.backend != "none":
            issues.extend([
                SecurityIssue(
                    severity="high",
                    category="速率限制",
                    description="实施 API 速率限制",
                    recommendation="使用 Redis 实现令牌桶算法，限制每 IP 每分钟请求次数",
                    cwe="CWE-770"
                ),
                SecurityIssue(
                    severity="medium",
                    category="敏感数据",
                    description="敏感数据不得记录到日志",
                    recommendation="实施日志脱敏，过滤密码、Token 等敏感字段",
                    cwe="CWE-532"
                ),
            ])

        # HTTPS
        issues.append(
            SecurityIssue(
                severity="critical",
                category="传输安全",
                description="强制使用 HTTPS",
                recommendation="配置 TLS 1.3，启用 HSTS，使用有效证书",
                cwe="CWE-319"
            )
        )

        # 领域特定安全
        if self.domain == "fintech":
            issues.extend([
                SecurityIssue(
                    severity="critical",
                    category="PCI-DSS",
                    description="金融数据必须符合 PCI-DSS 标准",
                    recommendation="实施端到端加密，使用 PCI 认证的服务商",
                    cwe="CWE-320"
                ),
                SecurityIssue(
                    severity="critical",
                    category="审计",
                    description="所有金融操作必须有审计日志",
                    recommendation="实施完整的审计追踪，日志不可篡改",
                    cwe="CWE-778"
                ),
            ])
        elif self.domain == "medical":
            issues.extend([
                SecurityIssue(
                    severity="critical",
                    category="HIPAA",
                    description="医疗数据必须符合 HIPAA 标准",
                    recommendation="实施数据加密、访问控制、审计日志",
                    cwe="CWE-200"
                ),
            ])

        return issues

    def _review_performance(self) -> list[PerformanceIssue]:
        """性能审查"""
        issues = []

        # 数据库性能
        if self.backend != "none":
            issues.extend([
                PerformanceIssue(
                    severity="high",
                    category="数据库",
                    description="确保数据库查询使用索引",
                    recommendation="为所有 WHERE、JOIN、ORDER BY 字段添加索引",
                    impact="查询速度可提升 10-1000 倍"
                ),
                PerformanceIssue(
                    severity="high",
                    category="数据库",
                    description="防止 N+1 查询问题",
                    recommendation="使用 Eager Loading 或 JOIN 查询，避免循环查询",
                    impact="减少数据库往返次数，显著提升响应速度"
                ),
                PerformanceIssue(
                    severity="medium",
                    category="数据库",
                    description="实施数据库连接池",
                    recommendation="配置连接池 (max_connections=100)，避免频繁创建连接",
                    impact="降低连接开销，提升并发能力"
                ),
            ])

        # API 性能
        issues.extend([
            PerformanceIssue(
                severity="high",
                category="API",
                description="实施响应缓存",
                recommendation="使用 Redis 缓存热点数据，设置合理的过期时间",
                impact="缓存命中时响应时间 < 10ms"
            ),
            PerformanceIssue(
                severity="medium",
                category="API",
                description="实施响应压缩",
                recommendation="启用 gzip 或 brotli 压缩，减少传输数据量",
                impact="传输数据量减少 60-80%"
            ),
            PerformanceIssue(
                severity="medium",
                category="API",
                description="实施分页和限制",
                recommendation="所有列表接口实施分页，限制每页最大数量",
                impact="防止大数据量查询导致性能问题"
            ),
        ])

        # 前端性能
        if self.frontend != "none":
            issues.extend([
                PerformanceIssue(
                    severity="high",
                    category="前端",
                    description="实施代码分割和懒加载",
                    recommendation="使用动态 import() 和 React.lazy() 按需加载代码",
                    impact="初始加载体积减少 40-60%"
                ),
                PerformanceIssue(
                    severity="medium",
                    category="前端",
                    description="优化图片加载",
                    recommendation="使用 WebP 格式，实施懒加载和响应式图片",
                    impact="图片体积减少 50-70%"
                ),
                PerformanceIssue(
                    severity="medium",
                    category="前端",
                    description="使用 CDN 加速静态资源",
                    recommendation="将 JS/CSS/图片等静态资源部署到 CDN",
                    impact="全球访问速度提升 50-80%"
                ),
            ])

        return issues

    def _review_architecture(self) -> list[ArchitectureIssue]:
        """架构审查"""
        issues = []

        # 可扩展性
        issues.extend([
            ArchitectureIssue(
                severity="high",
                category="可扩展性",
                description="设计无状态架构",
                recommendation="避免 Session 粘滞，使用 JWT 或外部 Session 存储",
                adr_needed=True
            ),
            ArchitectureIssue(
                severity="medium",
                category="可扩展性",
                description="实施水平扩展能力",
                recommendation="使用负载均衡，支持动态增减实例",
                adr_needed=True
            ),
        ])

        # 可维护性
        issues.extend([
            ArchitectureIssue(
                severity="high",
                category="可维护性",
                description="遵循单一职责原则",
                recommendation="每个模块/类只负责一个功能，保持高内聚低耦合",
                adr_needed=False
            ),
            ArchitectureIssue(
                severity="medium",
                category="可维护性",
                description="实施依赖注入",
                recommendation="使用 DI 容器，降低模块间耦合",
                adr_needed=True
            ),
            ArchitectureIssue(
                severity="medium",
                category="可维护性",
                description="统一错误处理",
                recommendation="实施全局错误处理中间件，统一错误响应格式",
                adr_needed=True
            ),
        ])

        # 可靠性
        if self.backend != "none":
            issues.extend([
                ArchitectureIssue(
                    severity="high",
                    category="可靠性",
                    description="实施健康检查端点",
                    recommendation="提供 /health 和 /ready 端点，支持 K8s 健康检查",
                    adr_needed=False
                ),
                ArchitectureIssue(
                    severity="high",
                    category="可靠性",
                    description="实施熔断机制",
                    recommendation="使用熔断器模式，防止级联故障",
                    adr_needed=True
                ),
                ArchitectureIssue(
                    severity="medium",
                    category="可靠性",
                    description="实施重试机制",
                    recommendation="对外部调用实施指数退避重试",
                    adr_needed=False
                ),
            ])

        # 可观测性
        issues.extend([
            ArchitectureIssue(
                severity="high",
                category="可观测性",
                description="实施结构化日志",
                recommendation="使用 JSON 格式日志，包含请求 ID、用户 ID 等上下文",
                adr_needed=True
            ),
            ArchitectureIssue(
                severity="medium",
                category="可观测性",
                description="实施分布式追踪",
                recommendation="使用 OpenTelemetry 追踪跨服务调用链",
                adr_needed=True
            ),
            ArchitectureIssue(
                severity="medium",
                category="可观测性",
                description="实施指标监控",
                recommendation="收集和展示关键业务和技术指标",
                adr_needed=True
            ),
        ])

        return issues
