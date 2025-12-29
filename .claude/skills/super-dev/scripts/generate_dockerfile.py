#!/usr/bin/env python3
"""
Super Dev - Dockerfile Generator (Phase 6: DevOps)
功能：根据技术栈自动生成优化的 Dockerfile
"""

import sys
import argparse
from pathlib import Path
try:
    from utils import console, print_success, print_error
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_success, print_error


# Dockerfile 模板
DOCKERFILE_TEMPLATES = {
    "node": """
# ============================================
# 多阶段构建 - Node.js 应用
# ============================================

# 阶段 1: 依赖安装
FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --only=production && npm cache clean --force

# 阶段 2: 构建
FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
# 如果需要构建
# RUN npm run build

# 阶段 3: 生产运行
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production

# 创建非 root 用户
RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

# 复制必要文件
COPY --from=builder /app/public ./public
# COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
# COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

COPY --from=builder /app/package.json ./package.json
COPY --from=deps /app/node_modules ./node_modules

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \\
    CMD node healthcheck.js

CMD ["node", "server.js"]
""",

    "python": """
# ============================================
# 多阶段构建 - Python 应用
# ============================================

# 阶段 1: 基础镜像
FROM python:3.12-slim AS builder

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    --no-install-recommends \\
    gcc \\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 阶段 2: 生产运行
FROM python:3.12-slim

WORKDIR /app

# 复制已安装的包
COPY --from=builder /root/.local /root/.local

# 确保脚本在 PATH 中
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 创建非 root 用户
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
""",

    "nextjs": """
# ============================================
# 多阶段构建 - Next.js 应用
# ============================================

FROM node:20-alpine AS deps
RUN apk add --no-cache libc6-compat
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci

FROM node:20-alpine AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
ENV NEXT_TELEMETRY_DISABLED 1
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV production
ENV NEXT_TELEMETRY_DISABLED 1

RUN addgroup --system --gid 1001 nodejs
RUN adduser --system --uid 1001 nextjs

COPY --from=builder /app/public ./public
COPY --from=builder --chown=nextjs:nodejs /app/.next/standalone ./
COPY --from=builder --chown=nextjs:nodejs /app/.next/static ./.next/static

USER nextjs

EXPOSE 3000

ENV PORT 3000
ENV HOSTNAME "0.0.0.0"

CMD ["node", "server.js"]
""",

    "react": """
# ============================================
# 多阶段构建 - React 应用 (Nginx)
# ============================================

# 构建阶段
FROM node:20-alpine AS builder
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

# 生产阶段 - Nginx
FROM nginx:alpine

# 复制构建产物到 Nginx
COPY --from=builder /app/build /usr/share/nginx/html

# 复制 Nginx 配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --quiet --tries=1 --spider http://localhost/ || exit 1

CMD ["nginx", "-g", "daemon off;"]
""",

    "django": """
# ============================================
# 多阶段构建 - Django 应用
# ============================================

FROM python:3.12-slim AS builder

WORKDIR /app

# 安装系统依赖
RUN apt-get update && apt-get install -y \\
    gcc \\
    postgresql-client \\
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# 生产运行
FROM python:3.12-slim

WORKDIR /app

# 复制已安装的包
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# 复制应用代码
COPY . .

# 收集静态文件
RUN python manage.py collectstatic --noinput

# 创建非 root 用户
RUN useradd --create-home django
USER django

EXPOSE 8000

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s --retries=3 \\
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health/')"

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
""",

    "go": """
# ============================================
# 多阶段构建 - Go 应用
# ============================================

# 构建阶段
FROM golang:1.21-alpine AS builder

WORKDIR /app

# 安装依赖
COPY go.* ./
RUN go mod download

# 复制源码并构建
COPY . .
RUN CGO_ENABLED=0 go build -o /app/main .

# 运行阶段
FROM alpine:latest

RUN apk --no-cache add ca-certificates

WORKDIR /root/

# 复制构建的二进制文件
COPY --from=builder /app/main .

# 创建非 root 用户
RUN addgroup -S app && adduser -S app -G app
USER app

EXPOSE 8080

# 健康检查
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \\
    CMD wget --quiet --tries=1 --spider http://localhost:8080/health || exit 1

CMD ["./main"]
"""
}

# Nginx 配置模板（用于 React）
NGINX_CONF = """
server {{
    listen 80;
    server_name localhost;
    root /usr/share/nginx/html;
    index index.html;

    # Gzip 压缩
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;

    # SPA 路由支持
    location / {{
        try_files $uri $uri/ /index.html;
    }}

    # 静态资源缓存
    location ~* \\.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {{
        expires 1y;
        add_header Cache-Control "public, immutable";
    }}

    # 安全头部
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
}}
"""


def generate_dockerfile(stack: str, output_path: Path = None) -> bool:
    """
    生成 Dockerfile

    Args:
        stack: 技术栈 (node, python, nextjs, react, django, go)
        output_path: 输出文件路径

    Returns:
        是否成功
    """
    stack = stack.lower().strip()

    if stack not in DOCKERFILE_TEMPLATES:
        print_error(f"不支持的技术栈: {stack}")
        console.print(f"[dim]支持的技术栈: {', '.join(DOCKERFILE_TEMPLATES.keys())}[/dim]")
        return False

    # 获取模板
    dockerfile_content = DOCKERFILE_TEMPLATES[stack].strip()

    # 确定输出路径
    if output_path is None:
        output_path = Path.cwd() / "Dockerfile"

    # 写入 Dockerfile
    output_path.write_text(dockerfile_content, encoding="utf-8")

    # 如果是 React，同时生成 nginx.conf
    if stack == "react":
        nginx_conf_path = output_path.parent / "nginx.conf"
        nginx_conf_path.write_text(NGINX_CONF.strip(), encoding="utf-8")
        print_success(f"Dockerfile 和 nginx.conf 已生成")
        console.print(f"[dim]- Dockerfile: {output_path}[/dim]")
        console.print(f"[dim]- nginx.conf: {nginx_conf_path}[/dim]")
    else:
        print_success(f"Dockerfile 已生成: {output_path}")

    return True


def main():
    parser = argparse.ArgumentParser(description="Super Dev Dockerfile 生成器 (Phase 6)")
    parser.add_argument("stack",
                       choices=list(DOCKERFILE_TEMPLATES.keys()),
                       help="技术栈类型")
    parser.add_argument("--output", "-o", help="输出文件路径 (默认: ./Dockerfile)")

    args = parser.parse_args()

    output_path = Path(args.output) if args.output else None

    console.print(f"[dim]正在生成 {args.stack} Dockerfile...[/dim]")
    generate_dockerfile(args.stack, output_path)


if __name__ == "__main__":
    main()
