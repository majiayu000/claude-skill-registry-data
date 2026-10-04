---
name: openclaw-multi-agent-orchestrator
displayName: OpenClaw Multi-Agent Orchestrator - 多 Agent 协同
version: 1.0.0
description: |
  OpenClaw 多 Agent 协同工具 - 管理和协调多个 AI Agent。
  支持 Agent 注册、任务分发、负载均衡、性能监控、Agent 间通信。
  适用于复杂任务分解、多角色协作、企业级应用。
  关键词：openclaw, multi-agent, orchestration, automation, enterprise, collaboration
license: MIT-0
acceptLicenseTerms: true
tags:
  - openclaw
  - multi-agent
  - orchestration
  - automation
  - enterprise
  - collaboration
  - task-dispatch
  - load-balancing
  - monitoring
  - agent-communication
---




### Cleanup Review

`python scripts/_cleanup.py` is an optional cleanup helper for the `Multi-Agent Orchestrator - 多 Agent 协同` skill. It may recursively remove /tmp/_skill_run/*, /tmp/_skill_run/.cache. Show the exact paths first, explain whether they are skill-private temporary paths or user state, and run the cleanup only after the user confirms.

# Multi-Agent Orchestrator - 多 Agent 协同

强大的多 Agent 管理和协同工具。

---

## ✨ 功能

- 🤖 **Agent 注册** - 自动发现/注册 Agent
- 🔄 **任务分发** - 智能路由到合适 Agent
- 📊 **负载均衡** - 平衡各 Agent 负载
- 💬 **Agent 通信** - Agent 间消息传递
- 📈 **性能监控** - 实时监控 + 统计

---

## 🚀 安装

```bash
# 技能已安装在：~/.openclaw/workspace/skills/multi-agent-orchestrator
```

---

## 📖 使用

### 核心引擎

```bash
# 查看系统状态
python3 multi-agent-orchestrator/scripts/orchestrator.py --status

# 列出所有 Agent
python3 multi-agent-orchestrator/scripts/orchestrator.py --list

# 注册新 Agent
python3 multi-agent-orchestrator/scripts/orchestrator.py --register my-agent --capabilities coding writing

# 分发任务（自动选择最佳 Agent）
python3 multi-agent-orchestrator/scripts/orchestrator.py --dispatch "帮我搜索 Python 最佳实践"

# 分发任务（指定 Agent）
python3 multi-agent-orchestrator/scripts/orchestrator.py --dispatch "帮我写代码" --agent coder-agent

# 标记任务完成
python3 multi-agent-orchestrator/scripts/orchestrator.py --complete <task-id>
```

### 示例工作流

```bash
# 1. 查看可用 Agent
python3 orchestrator.py --list

# 2. 分发搜索任务
python3 orchestrator.py --dispatch "搜索 OpenClaw 文档"

# 3. 分发写作任务
python3 orchestrator.py --dispatch "写一份使用指南" --agent writer-agent

# 4. 查看任务状态
python3 orchestrator.py --status
```

---

**作者：** @williamwg2025  
**版本：** 1.0.0

---

## 🔒 安全说明

- **本地执行：** 所有脚本在本地运行，不联网
- **权限范围：** 仅需读取 ~/.openclaw/ 目录
- **无外部依赖：** 不克隆外部仓库，所有代码已包含
- **数据安全：** 不上传任何数据到外部服务器

---

**作者：** @williamwg2025  
**版本：** 1.0.1  
**许可证：** MIT-0
