#!/usr/bin/env python3
"""
Super Dev - CI/CD Configuration Generator (Phase 6: DevOps)
功能：生成 GitHub Actions / GitLab CI 配置文件
"""

import sys
import argparse
from pathlib import Path
try:
    from utils import console, print_success, print_error
except ImportError:
    sys.path.append(str(Path(__file__).parent))
    from utils import console, print_success, print_error


# GitHub Actions 模板
GITHUB_ACTIONS_TEMPLATES = {
    "node": """
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '20'
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  # ============================================
  # 代码质量检查
  # ============================================
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run Type Check
        run: npm run type-check

  # ============================================
  # 单元测试
  # ============================================
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage/lcov.info

  # ============================================
  # 构建镜像
  # ============================================
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=ref,event=pr
            type=semver,pattern={{version}}
            type=semver,pattern={{major}}.{{minor}}
            type=sha,prefix={{branch}}-
            type=raw,value=latest,enable={{is_default_branch}}

      - name: Build and push Docker image
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ============================================
  # 部署 (仅 main 分支)
  # ============================================
  deploy:
    name: Deploy to Production
    runs-on: ubuntu-latest
    needs: build
    if: github.ref == 'refs/heads/main' && github.event_name == 'push'
    environment: production
    steps:
      - name: Deploy
        run: |
          echo "部署到生产环境"
          # 添加你的部署命令，例如:
          # kubectl set image deployment/app app=${{ needs.build.outputs.image-tag }}
          # 或
          # ssh user@server "docker pull ${{ needs.build.outputs.image-tag }} && docker-compose up -d"
""",

    "python": """
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  PYTHON_VERSION: '3.12'

jobs:
  # ============================================
  # 代码质量检查
  # ============================================
  lint:
    name: Lint & Format Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install ruff mypy pytest
          pip install -r requirements.txt

      - name: Run Ruff
        run: ruff check .

      - name: Run MyPy
        run: mypy .

  # ============================================
  # 单元测试
  # ============================================
  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ env.PYTHON_VERSION }}
          cache: 'pip'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install pytest pytest-cov
          pip install -r requirements.txt

      - name: Run tests
        run: pytest --cov=./ --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3

  # ============================================
  # 安全扫描
  # ============================================
  security:
    name: Security Scan
    runs-on: ubuntu-latest
    needs: test
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'

      - name: Upload Trivy results to GitHub Security tab
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'

  # ============================================
  # 构建镜像
  # ============================================
  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: [test, security]
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
      image-digest: ${{ steps.build.outputs.digest }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=semver,pattern={{version}}
            type=sha,prefix={{branch}}-

      - name: Build and push
        id: build
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
""",

    "nextjs": """
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

env:
  NODE_VERSION: '20'

jobs:
  lint:
    name: Lint & Type Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run ESLint
        run: npm run lint

      - name: Run TypeScript Check
        run: npm run type-check

  test:
    name: Unit Tests
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: ${{ env.NODE_VERSION }}
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Run tests
        run: npm test

      - name: Build Next.js
        run: npm run build

  build:
    name: Build Docker Image
    runs-on: ubuntu-latest
    needs: test
    permissions:
      contents: read
      packages: write
    outputs:
      image-tag: ${{ steps.meta.outputs.tags }}
    steps:
      - uses: actions/checkout@v4

      - name: Set up Docker Buildx
        uses: docker/setup-buildx-action@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ghcr.io/${{ github.repository }}
          tags: |
            type=ref,event=branch
            type=sha

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
"""
}

# GitLab CI 模板
GITLAB_CI_TEMPLATES = {
    "node": """
stages:
  - lint
  - test
  - build
  - deploy

variables:
  NODE_VERSION: "20"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# ============================================
# 代码质量检查
# ============================================
lint:
  stage: lint
  image: node:$NODE_VERSION-alpine
  cache:
    paths:
      - node_modules/
  script:
    - npm ci
    - npm run lint
    - npm run type-check
  only:
    - merge_requests
    - main
    - develop

# ============================================
# 单元测试
# ============================================
test:
  stage: test
  image: node:$NODE_VERSION-alpine
  cache:
    paths:
      - node_modules/
  script:
    - npm ci
    - npm test
  coverage: '/All files[^|]*\\|[^|]*\\|[^|]*\\|/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage/cobertura.xml
  only:
    - merge_requests
    - main
    - develop

# ============================================
# 构建镜像
# ============================================
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop

# ============================================
# 部署
# ============================================
deploy:staging:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE_STAGING
  environment:
    name: staging
  only:
    - develop

deploy:production:
  stage: deploy
  image: bitnami/kubectl:latest
  script:
    - kubectl set image deployment/app app=$IMAGE_TAG -n $KUBE_NAMESPACE_PRODUCTION
  environment:
    name: production
  when: manual
  only:
    - main
""",

    "python": """
stages:
  - lint
  - test
  - build
  - deploy

variables:
  PYTHON_VERSION: "3.12"
  IMAGE_TAG: $CI_REGISTRY_IMAGE:$CI_COMMIT_SHORT_SHA

# ============================================
# 代码质量检查
# ============================================
lint:
  stage: lint
  image: python:$PYTHON_VERSION-slim
  cache:
    paths:
      - .cache/pip
  before_script:
    - pip install ruff mypy
  script:
    - ruff check .
    - mypy .
  only:
    - merge_requests
    - main
    - develop

# ============================================
# 单元测试
# ============================================
test:
  stage: test
  image: python:$PYTHON_VERSION-slim
  cache:
    paths:
      - .cache/pip
  before_script:
    - pip install pytest pytest-cov
    - pip install -r requirements.txt
  script:
    - pytest --cov=./ --cov-report=xml --cov-report=term
  coverage: '/(?i)total.*? (100(?:\\.0+)?%|[1-9]?\\d?\\d%)/'
  artifacts:
    reports:
      coverage_report:
        coverage_format: cobertura
        path: coverage.xml
  only:
    - merge_requests
    - main
    - develop

# ============================================
# 安全扫描
# ============================================
security:
  stage: test
  image: aquasec/trivy:latest
  script:
    - trivy fs --format sarif --output trivy-results.sarif .
  artifacts:
    reports:
      sast: trivy-results.sarif
  only:
    - merge_requests
    - main
    - develop

# ============================================
# 构建镜像
# ============================================
build:
  stage: build
  image: docker:24
  services:
    - docker:24-dind
  script:
    - docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY
    - docker build -t $IMAGE_TAG .
    - docker push $IMAGE_TAG
  only:
    - main
    - develop
"""
}


def generate_ci_cd(platform: str, stack: str, output_path: Path = None) -> bool:
    """
    生成 CI/CD 配置文件

    Args:
        platform: 平台 (github, gitlab)
        stack: 技术栈 (node, python, nextjs)
        output_path: 输出文件路径

    Returns:
        是否成功
    """
    platform = platform.lower().strip()
    stack = stack.lower().strip()

    # 确定模板来源
    if platform == "github":
        templates = GITHUB_ACTIONS_TEMPLATES
        default_filename = ".github/workflows/ci.yml"
    elif platform == "gitlab":
        templates = GITLAB_CI_TEMPLATES
        default_filename = ".gitlab-ci.yml"
    else:
        print_error(f"不支持的平台: {platform}")
        console.print("[dim]支持的平台: github, gitlab[/dim]")
        return False

    # 检查技术栈
    if stack not in templates:
        print_error(f"技术栈 '{stack}' 在 {platform} 模板中不存在")
        available = list(templates.keys())
        if stack in ["react", "django", "go"]:
            # 映射到相似的技术栈
            if stack == "react":
                stack = "node"
            elif stack == "django":
                stack = "python"
            console.print(f"[dim]使用 '{stack}' 模板代替[/dim]")
        else:
            console.print(f"[dim]支持的技术栈: {', '.join(available)}[/dim]")
            return False

    # 获取模板内容
    content = templates[stack].strip()

    # 确定输出路径
    if output_path is None:
        output_path = Path.cwd() / default_filename

    # 创建目录
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 写入文件
    output_path.write_text(content, encoding="utf-8")

    print_success(f"CI/CD 配置已生成: {output_path}")
    console.print(f"[dim]平台: {platform} | 技术栈: {stack}[/dim]")

    return True


def main():
    parser = argparse.ArgumentParser(description="Super Dev CI/CD 生成器 (Phase 6)")
    parser.add_argument("platform",
                       choices=["github", "gitlab"],
                       help="CI/CD 平台")
    parser.add_argument("stack",
                       help="技术栈 (node, python, nextjs, react, django, go)")
    parser.add_argument("--output", "-o",
                       help="输出文件路径")

    args = parser.parse_args()

    output_path = Path(args.output) if args.output else None

    generate_ci_cd(args.platform, args.stack, output_path)


if __name__ == "__main__":
    main()
