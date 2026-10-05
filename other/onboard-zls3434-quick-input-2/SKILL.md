---
name: onboard
description: "为指定角色生成入职文档，读取相关 Agent 定义和技能列表，生成该角色的入职指南。"
license: MIT
metadata:
  model: haiku
  argument-hint: "[角色名]"
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /onboard}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# onboard — 角色入职文档生成

## 技能目的

为团队成员（或 AI Agent）生成针对特定角色的入职文档，帮助其快速理解职责、可用技能、协作协议与产物规范。

## 参数说明

- `[角色名]`：目标角色名称，例如 `frontend-architect`、`test-engineer`、`release-manager` 等。

## 分阶段工作流

### 阶段 1：读取角色定义

- **输入**：角色名参数
- **处理**：
  1. 使用 Glob 在 `.claude/agents/` 下查找匹配的 Agent 定义文件
  2. 使用 Read 读取该 Agent 的定义文件，提取职责、权限、协作关系
  3. 使用 Grep 在技能目录中搜索引用了该角色的技能
- **输出**：角色定义对象 + 关联技能列表

### 阶段 2：汇总可用技能

- **输入**：关联技能列表
- **处理**：读取每个技能的 SKILL.md frontmatter，提取 name、description、argument-hint
- **输出**：技能摘要表

### 阶段 3：读取协作协议

- **输入**：角色名
- **处理**：使用 Glob 查找 `.claude/docs/templates/collaborative-protocols/` 下与该角色相关的协议文件，使用 Read 读取
- **输出**：适用协议清单

### 阶段 4：生成入职文档

- **输入**：角色定义 + 技能摘要 + 协议清单
- **处理**：使用 Write 将入职文档写入 `.claude/docs/onboarding/{角色名}.md`，包含：角色概述、核心职责、可用技能清单、协作协议、产物规范、常见问题
- **输出**：入职文档文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 中的角色定义规范

## 推荐下一步

阅读生成的入职文档，然后使用 `/help` 查看当前可执行的第一项任务。