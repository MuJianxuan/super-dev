# {{ project_name }} - 部署运维手册

## 1. 环境依赖 (Prerequisites)

| 组件 | 版本 | 说明 |
|:---|:---|:---|
| Docker | 20.10+ | 容器运行时 |
| K8s | 1.25+ | 容器编排 (生产环境) |
| PostgreSQL | 15.0+ | 主数据库 |

## 2. 部署流程 (Deployment)

### 2.1 容器构建
```bash
# 构建镜像
docker build -t {{ project_name }}:latest .
```

### 2.2 环境变量 (.env)
> **注意**: 严禁将 .env 提交到 git。

```bash
DB_HOST=127.0.0.1
DB_PASS=S3cr3t!  # 生产环境请使用 KMS
REDIS_URL=redis://localhost:6379
```

### 2.3 启动服务
```bash
docker-compose up -d
```

## 3. 监控与告警
- **健康检查**: `GET /health` 返回 200 OK。
- **日志路径**: `/var/log/{{ project_name }}/app.log`。
- **Prometheus 指标**: `GET /metrics`。

## 4. 故障排查 (Troubleshooting)
- **Error 1001 (DB Conn Fail)**: 检查防火墙端口 5432 是否开放。
- **Error 5002 (Redis Timeout)**: 检查 Redis 内存水位。
