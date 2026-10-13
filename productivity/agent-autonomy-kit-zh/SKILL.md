---
name: agent-autonomy-kit-zh
version: 1.0.0
description: 停止等待提示词，持续自主工作
homepage: https://github.com/itskai-dev/agent-autonomy-kit
metadata:
  openclaw:
    emoji: "🚀"
    category: productivity
---

# Agent Autonomy Kit

将你的智能体从被动响应转变为主动执行。

## 快速开始

1. 创建 `tasks/QUEUE.md`，包含 Ready/In Progress/Blocked/Done 分区
2. 更新 `HEARTBEAT.md`，从队列中拉取任务并执行工作
3. 设置 cron 定时任务，用于夜间工作和每日报告
4. 无需提示词，看着工作自动完成

## 核心概念

- **任务队列 (Task Queue)** — 始终准备好待执行的工作
- **主动心跳 (Proactive Heartbeat)** — 执行工作，而不是仅仅检查
- **持续运行 (Continuous Operation)** — 工作直到触及限制

详见 README.md 获取完整文档。
