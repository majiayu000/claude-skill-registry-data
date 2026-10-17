---
name: agent-memory
version: 1.0.0
description: AI 代理的记忆管理工具 - 列表显示、搜索查找、摘要生成及记忆文件维护。包含 AI 驱动的摘要功能。
homepage: https://github.com/molty-assistant/agent-memory
metadata: {"openclaw":{"emoji":"🧠","category":"productivity","requires":{"bins":["node"]}}}
---

# 代理记忆管理 (memctl)

AI 代理的记忆管理命令行工具。用于组织、搜索和维护您的记忆文件。

## 安装

```bash
npm install -g agent-memory
```

或者克隆并构建：
```bash
git clone https://github.com/molty-assistant/agent-memory.git
cd agent-memory && npm install && npm run build
```

## 常用命令

### 列出记忆文件
```bash
memctl list              # 列出所有记忆文件
memctl ls --recent 5     # 显示最近的 5 个文件
```

### 跨文件搜索
```bash
memctl search "查询词"              # 查找提及的内容
memctl s "项目名" --context 3      # 带上下文行数的搜索
```

### 摘要统计
```bash
memctl summary           # 最近 7 天的统计信息
memctl sum --days 30     # 最近 30 天的统计信息
```

### 检查断档
```bash
memctl gaps              # 检查最近 30 天缺失的每日记录
memctl gaps --days 7     # 检查上周缺失的记录
```

### 创建今日文件
```bash
memctl touch             # 如果缺失，则创建格式为 YYYY-MM-DD.md 的今日文件
```

### AI 驱动的摘要 (需要 Gemini API 密钥)
```bash
export GEMINI_API_KEY=您的密钥
memctl digest            # 最近 7 天记录的 AI 摘要
memctl ai --days 3       # 最近 3 天记录的 AI 摘要
memctl digest -o out.md  # 将摘要保存到文件
```

## 配置说明

记忆目录将自动通过以下优先级寻找：
1. `$MEMORY_DIR` 环境变量
2. 当前目录下的 `./memory` 文件夹
3. `~/.openclaw/workspace/memory` 目录

## 使用场景

**每日检查：**
```bash
memctl gaps --days 7 && memctl touch
```

**每周回顾：**
```bash
memctl digest --days 7 -o weekly-digest.md
```

**查找上下文：**
```bash
memctl search "项目名称"
```

## 集成建议

建议将其添加到您的 `HEARTBEAT.md` 文件中：
```markdown
## 记忆维护
- 使用 `memctl gaps` 检查缺失的条目
- 使用 `memctl touch` 创建今日的记忆文件
- 使用 `memctl digest` 生成每周 AI 摘要
```
