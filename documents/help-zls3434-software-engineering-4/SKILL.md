---
name: help
description: "上下文感知的\"下一步该做什么\"助手。读取工作流目录与已有产物，判断当前阶段并推荐下一步动作。"
license: MIT
metadata:
  model: haiku
  argument-hint: ""
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /help}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# help — 上下文感知下一步助手

## 技能目的

根据当前项目状态、已有产物与工作流目录，智能判断项目所处阶段，并向用户推荐下一步应执行的动作或技能。

## 参数说明

本技能无参数。

## 分阶段工作流

### 阶段 1：读取工作流目录

- **输入**：`.claude/workflow-catalog.yaml`
- **处理**：解析工作流目录，获取所有阶段定义、必需产物列表、阶段间依赖关系
- **输出**：工作流定义对象

### 阶段 2：检测已有产物

- **输入**：工作流定义 + 项目目录
- **处理**：
  1. 使用 Glob 扫描各阶段期望产物（product-concept.md、systems-index.md、SRS、architecture-doc.md 等）
  2. 使用 Grep 检查产物内容的完整度（是否仅占位、是否有实际内容）
  3. 对照工作流目录标记每个阶段的完成度：未开始/进行中/已完成
- **输出**：阶段完成度矩阵

### 阶段 3：定位当前阶段

- **输入**：阶段完成度矩阵
- **处理**：找到第一个未完成阶段作为当前阶段，识别该阶段缺失的关键产物
- **输出**：当前阶段名称 + 缺失产物清单

### 阶段 4：推荐下一步

- **输入**：当前阶段 + 缺失产物
- **处理**：匹配当前阶段对应的技能，生成推荐动作列表（按优先级排序）
- **输出**：推荐下一步消息，包含技能名、简要说明、建议参数

## 协作协议引用

- 参考 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 中的阶段流转规则

## 推荐下一步

直接执行推荐的首选技能。若用户对推荐有异议，可使用 `/project-stage-detect` 获取更详细的阶段诊断报告。