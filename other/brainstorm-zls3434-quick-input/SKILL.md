---
name: brainstorm
description: "产品概念创意构思。通过情感锚点、品味画像、约束识别，生成多个产品概念并验证范围与可行性，产出 product-concept.md。"
license: MIT
metadata:
  model: sonnet
  argument-hint: ""
  user-invocable: true
  allowed-tools:
    - Read
    - Glob
    - Grep
    - Write
    - WebSearch
    - Task
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /brainstorm}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# brainstorm — 产品概念创意构思

## 技能目的

在项目最早期阶段引导用户进行产品创意构思，从情感锚点出发，结合品味画像与约束条件，生成多个候选概念，设计核心流程，定义产品支柱与反支柱，验证用户类型，最终评估范围与可行性，产出 `product-concept.md`。

## 参数说明

本技能无参数。通过交互式问答收集创意输入。

## 分阶段工作流

### 阶段 1：创意发现

- **输入**：用户交互
- **处理**：
  1. 通过 AskUserQuestion 询问情感锚点：希望用户使用后产生什么感受
  2. 询问品味画像：目标用户的美学与体验偏好
  3. 询问约束条件：预算、时间、技术、团队能力
  4. 可选使用 WebSearch 调研同类产品与市场趋势
- **输出**：创意发现清单

### 阶段 2：概念生成

- **输入**：创意发现清单
- **处理**：生成 3 个候选概念，每个概念采用不同策略：
  1. 动词优先 — 以核心动作驱动
  2. 混搭 — 跨领域组合
  3. 体验优先 — 以情感体验驱动
  通过 AskUserQuestion 请用户选择或组合
- **输出**：3 个候选概念 + 用户选择

### 阶段 3：核心流程设计

- **输入**：选定的概念
- **处理**：设计用户从首次接触到完成核心目标的端到端流程，标注关键触点
- **输出**：核心流程描述

### 阶段 4：产品支柱与反支柱

- **输入**：核心流程
- **处理**：
  1. 定义 3-5 个产品支柱（必须做到极致的方面）
  2. 定义反支柱（明确不做的方面，防止范围蔓延）
- **输出**：支柱与反支柱清单

### 阶段 5：用户类型验证

- **输入**：支柱清单
- **处理**：识别 2-3 种用户类型，验证每种类型是否有足够大的受众与明确需求
- **输出**：用户类型验证结果

### 阶段 6：范围与可行性

- **输入**：以上所有产出
- **处理**：评估 MVP 范围、技术可行性、资源可行性，使用 Write 写入 `docs/product-concept.md`
- **输出**：product-concept.md 文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 概念文档规范
- 参考 `.claude/docs/templates/product-concept.md` 模板

## 推荐下一步

使用 `/setup-stack` 配置技术栈，或使用 `/map-modules` 将概念分解为模块。