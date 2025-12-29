#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
开发：Excellent（11964948@qq.com）
功能：Super Dev Web API - FastAPI 后端
作用：提供 REST API 服务，支持项目管理和工作流执行
创建时间：2025-12-30
最后修改：2025-12-30
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from pathlib import Path
from typing import Optional, List
import uvicorn

from super_dev.config import ConfigManager, get_config_manager, ProjectConfig
from super_dev.orchestrator import WorkflowEngine, Phase, WorkflowContext


# ==================== 数据模型 ====================

class ProjectInitRequest(BaseModel):
    """项目初始化请求"""
    name: str
    description: str = ""
    platform: str = "web"
    frontend: str = "react"
    backend: str = "node"
    domain: str = ""
    quality_gate: int = 80


class ProjectConfigResponse(BaseModel):
    """项目配置响应"""
    name: str
    description: str
    version: str
    platform: str
    frontend: str
    backend: str
    domain: str
    quality_gate: int
    phases: List[str]
    experts: List[str]


class WorkflowRunRequest(BaseModel):
    """工作流运行请求"""
    phases: Optional[List[str]] = None
    quality_gate: Optional[int] = None


class WorkflowRunResponse(BaseModel):
    """工作流运行响应"""
    status: str
    message: str
    run_id: Optional[str] = None


# ==================== FastAPI 应用 ====================

app = FastAPI(
    title="Super Dev API",
    description="顶级 AI 开发战队 - Web API",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 静态文件服务 (前端)
frontend_path = Path(__file__).parent / "frontend" / "dist"
if frontend_path.exists():
    app.mount("/", StaticFiles(directory=str(frontend_path), html=True), name="frontend")


# ==================== API 路由 ====================

@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy", "version": "1.0.0"}


@app.get("/api/config")
async def get_config(project_dir: str = ".") -> dict:
    """获取项目配置"""
    try:
        manager = ConfigManager(Path(project_dir))
        if not manager.exists():
            raise HTTPException(status_code=404, detail="项目未初始化")

        config = manager.config
        return {
            "name": config.name,
            "description": config.description,
            "version": config.version,
            "platform": config.platform,
            "frontend": config.frontend,
            "backend": config.backend,
            "database": config.database,
            "domain": config.domain,
            "quality_gate": config.quality_gate,
            "phases": config.phases,
            "experts": config.experts,
            "output_dir": config.output_dir,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/init")
async def init_project(request: ProjectInitRequest, project_dir: str = ".") -> dict:
    """初始化项目"""
    try:
        manager = ConfigManager(Path(project_dir))
        if manager.exists():
            raise HTTPException(status_code=400, detail="项目已初始化")

        config = manager.create(
            name=request.name,
            description=request.description,
            platform=request.platform,
            frontend=request.frontend,
            backend=request.backend,
            domain=request.domain,
            quality_gate=request.quality_gate
        )

        return {
            "status": "success",
            "message": "项目已初始化",
            "config": {
                "name": config.name,
                "platform": config.platform,
                "frontend": config.frontend,
                "backend": config.backend,
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.put("/api/config")
async def update_config(
    updates: dict,
    project_dir: str = "."
) -> dict:
    """更新项目配置"""
    try:
        manager = ConfigManager(Path(project_dir))
        if not manager.exists():
            raise HTTPException(status_code=404, detail="项目未初始化")

        config = manager.update(**updates)
        return {"status": "success", "config": config.__dict__}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/workflow/run")
async def run_workflow(
    request: WorkflowRunRequest,
    background_tasks: BackgroundTasks,
    project_dir: str = "."
) -> WorkflowRunResponse:
    """运行工作流"""
    try:
        manager = ConfigManager(Path(project_dir))
        if not manager.exists():
            raise HTTPException(status_code=404, detail="项目未初始化")

        # 更新质量门禁
        if request.quality_gate is not None:
            manager.update(quality_gate=request.quality_gate)

        # 解析阶段
        phases = None
        if request.phases:
            phase_map = {
                "discovery": Phase.DISCOVERY,
                "intelligence": Phase.INTELLIGENCE,
                "drafting": Phase.DRAFTING,
                "redteam": Phase.REDTEAM,
                "qa": Phase.QA,
                "delivery": Phase.DELIVERY,
                "deployment": Phase.DEPLOYMENT,
            }
            phases = [phase_map[p] for p in request.phases if p in phase_map]

        # 生成运行 ID
        import uuid
        run_id = str(uuid.uuid4())[:8]

        # 后台运行工作流
        async def run_workflow_background():
            engine = WorkflowEngine(Path(project_dir))
            await engine.run(phases=phases)

        background_tasks.add_task(run_workflow_background)

        return WorkflowRunResponse(
            status="started",
            message=f"工作流已启动 (ID: {run_id})",
            run_id=run_id
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/workflow/status/{run_id}")
async def get_workflow_status(run_id: str, project_dir: str = ".") -> dict:
    """获取工作流状态"""
    # TODO: 实现工作流状态跟踪
    return {
        "run_id": run_id,
        "status": "running",
        "progress": 0
    }


@app.get("/api/experts")
async def list_experts() -> dict:
    """列出可用专家"""
    experts = [
        {"id": "PM", "name": "产品经理", "description": "需求分析、PRD编写"},
        {"id": "ARCHITECT", "name": "架构师", "description": "系统设计、技术选型"},
        {"id": "UI", "name": "UI设计师", "description": "视觉设计、设计规范"},
        {"id": "UX", "name": "UX设计师", "description": "交互设计、用户体验"},
        {"id": "SECURITY", "name": "安全专家", "description": "安全审查、漏洞检测"},
        {"id": "CODE", "name": "开发专家", "description": "代码实现、最佳实践"},
        {"id": "DBA", "name": "数据库专家", "description": "数据库设计、优化"},
        {"id": "QA", "name": "测试专家", "description": "质量保证、测试策略"},
        {"id": "DEVOPS", "name": "运维专家", "description": "部署、CI/CD"},
    ]
    return {"experts": experts}


@app.get("/api/phases")
async def list_phases() -> dict:
    """列出工作流阶段"""
    phases = [
        {"id": "discovery", "name": "需求发现", "description": "收集和分析用户需求"},
        {"id": "intelligence", "name": "情报收集", "description": "市场研究、竞品分析"},
        {"id": "drafting", "name": "专家起草", "description": "专家协作生成文档"},
        {"id": "redteam", "name": "红队审查", "description": "安全、性能审查"},
        {"id": "qa", "name": "质量门禁", "description": "质量检查和验证"},
        {"id": "delivery", "name": "幻影交付", "description": "生成原型预览"},
        {"id": "deployment", "name": "工业化部署", "description": "生成部署配置"},
    ]
    return {"phases": phases}


# ==================== 主函数 ====================

def main():
    """启动 API 服务器"""
    uvicorn.run(
        "super_dev.web.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )


if __name__ == "__main__":
    main()
