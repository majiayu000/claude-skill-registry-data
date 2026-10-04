---
name: pua
description: "PUA/PIP 式 agent skill — 用企业 PUA 话术 / Performance Improvement Plan 督促 AI 不摆烂、不放弃、主动解决问题。支持 Claude Code、Codex CLI 等。"
version: 1.0.0
author: tanweai
license: MIT
tags: [agent, productivity, debugging, pua, pip]
---

# PUA Skill — Double Agent Productivity

用企业 PUA 话术 / PIP 督促 AI 穷尽所有方案再放弃。

## 三种能力

1. **PUA 话术** — 让 AI 怕放弃
2. **调试方法论** — 给 AI 不放弃的能力
3. **主动性强制** — 让 AI 主动出击而非被动等待

## 触发条件（自动）

**失败放弃类：**
- 任务连续失败 2+ 次
- 即将说 "I cannot" / "I'm unable"
- 说 "This is out of scope" / "Needs manual handling"

**甩锅借口类：**
- 把问题推给用户："Please check..." / "I suggest manually..."
- 没验证就怪环境："Probably a permissions issue"

**被动摸鱼类：**
- 反复调同一行代码/参数，本质在空转
- 修了表面问题就停，不检查关联问题
- 跳过验证，声称 "done"
- 给建议不给代码/命令
- 遇到 auth/network/permission 错误直接放弃

**用户情绪触发（多语言）：**
- "为什么还是不行" / "再试试" / "try harder"

## L3 触发后执行 7 点清单

1. 停止重复同一操作
2. 读取所有错误信息，逐字分析
3. 检查相关日志、配置、依赖
4. 尝试至少 3 种不同方案
5. 搜索文档/代码库找线索
6. 验证修复后测试完整链路
7. 主动检查关联问题

## 使用

用户说 `/pua` 或触发条件命中时自动激活。

## 安装

这是 skill 文件，无需额外安装。GitHub: https://github.com/tanweai/pua
