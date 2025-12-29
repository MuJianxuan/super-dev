#!/bin/bash
#
# Super Dev - 一键安装脚本
# 将 Super Dev Agent Skill 安装到你的项目中
#

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的消息
info() { echo -e "${BLUE}${NC} $1"; }
success() { echo -e "${GREEN}${NC} $1"; }
warning() { echo -e "${YELLOW}${NC} $1"; }
error() { echo -e "${RED}${NC} $1"; }

# 欢迎信息
echo ""
echo -e "${GREEN} Super Dev 安装程序${NC}"
echo "=================================="
echo ""

# 检查目标目录
TARGET_DIR="${1:-.}"

if [ "$TARGET_DIR" == "." ]; then
    info "将安装到当前目录"
else
    info "将安装到: $TARGET_DIR"
fi

# 检查源目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_SOURCE="$SCRIPT_DIR/.claude/skills/super-dev"

if [ ! -d "$SKILL_SOURCE" ]; then
    # 如果脚本在仓库根目录运行
    if [ -d "$SCRIPT_DIR/.claude/skills/super-dev" ]; then
        SKILL_SOURCE="$SCRIPT_DIR/.claude/skills/super-dev"
    else
        error "找不到 Super Dev Skill 源文件"
        error "请确保从 super-dev 仓库目录运行此脚本"
        exit 1
    fi
fi

# 创建目标目录
TARGET_SKILL_DIR="$TARGET_DIR/.claude/skills/super-dev"

if [ -d "$TARGET_SKILL_DIR" ]; then
    warning "目标目录已存在: $TARGET_SKILL_DIR"
    read -p "是否覆盖? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        info "安装已取消"
        exit 0
    fi
    rm -rf "$TARGET_SKILL_DIR"
fi

# 创建目录结构
info "创建目录结构..."
mkdir -p "$TARGET_DIR/.claude/skills"

# 复制文件
info "复制 Skill 文件..."
cp -r "$SKILL_SOURCE" "$TARGET_SKILL_DIR"

# 统计文件
FILE_COUNT=$(find "$TARGET_SKILL_DIR" -type f | wc -l | tr -d ' ')
success "已复制 $FILE_COUNT 个文件"

# 安装 Python 依赖 (可选)
echo ""
read -p "是否安装 Python 依赖? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    info "安装 Python 依赖..."
    if command -v pip &> /dev/null; then
        pip install -r "$TARGET_SKILL_DIR/scripts/requirements.txt"
        success "Python 依赖安装完成"
    else
        warning "未找到 pip，请手动安装依赖"
        echo "  pip install -r .claude/skills/super-dev/scripts/requirements.txt"
    fi
fi

# 完成
echo ""
echo -e "${GREEN}=================================="
echo " Super Dev 安装成功!"
echo "==================================${NC}"
echo ""
echo " 安装位置: $TARGET_SKILL_DIR"
echo ""
echo " 使用方法:"
echo "   在 Claude Code 中输入："
echo "   \"帮我设计一个在线教育平台的 PRD\""
echo ""
echo " Python 工具:"
echo "   python $TARGET_SKILL_DIR/scripts/init_project.py \"my-project\""
echo ""
echo " 更多信息请查看 README.md"
echo ""
