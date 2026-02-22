#!/bin/bash

# Atom IP Insights - 一键发布脚本
PROJECT_DIR="/Users/atom1983/.openclaw/workspace/core/atom_ip_platform"

echo "🚀 准备发布最新内容到 www.atom-ip.com..."

cd $PROJECT_DIR

# 检查是否有更改
if [[ -n $(git status -s) ]]; then
    echo "📦 发现新更改，正在打包..."
    git add .
    git commit -m "Update insights: $(date +'%Y-%m-%d %H:%M')"
    
    echo "📤 正在上传到 GitHub..."
    git push origin main
    
    echo "✅ 发布成功！请等待 1-2 分钟查看线上更新。"
else
    echo "✨ 内容已经是最新，无需发布。"
fi
