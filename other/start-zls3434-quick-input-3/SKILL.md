---
name: start
description: "首次上手引导技能。检测项目状态、询问用户所处阶段、根据答案路由到对应工作流，并设置审查模式，完成交接。"
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
    - AskUserQuestion
  platforms:
    claude-code: {enabled: true}
    cursor: {enabled: true}
    codex: {enabled: true}
    windsurf: {enabled: true, trigger: /start}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# start — 首次上手引导

## 技能目的

为首次使用本框架的用户提供一站式引导：检测当前项目状态、询问用户所处阶段、根据回答路由到合适的工作流起点，并设置审查模式（full / lean / solo），最后将控制权交接给对应技能或 Agent。

## 参数说明

本技能无参数。启动后会主动询问用户当前位置与期望。

## 分阶段工作流

### 阶段 1：检测项目状态

- **输入**：当前工作目录
- **处理**：
  1. 使用 Glob 扫描是否存在 `.claude/`、`.agent/`、`docs/`、`agent-docs/` 等目录
  2. 使用 Read 读取 `workflow-catalog.yaml`（若存在）
  3. 使用 Grep 检查是否已有 product-concept.md、systems-index.md 等产物
  4. 判断项目属于"绿地"（无产物）还是"棕地"（已有产物）
- **输出**：项目状态摘要（绿地/棕地、已有阶段、缺失产物）

### 阶段 2：询问用户位置

- **输入**：项目状态摘要
- **处理**：通过 AskUserQuestion 向用户呈现 4 个选项：
  1. 没有想法 — 尚未想好要做什么
  2. 模糊想法 — 有大致方向但未成型
  3. 清晰概念 — 已有明确产品概念
  4. 已有项目 — 已有代码或文档，希望接入框架
- **输出**：用户位置答案

### 阶段 3：根据答案路由

- **输入**：用户位置答案 + 项目状态
- **处理**：
  - 没有想法 → 路由到 `brainstorm`
  - 模糊想法 → 路由到 `product-concept`
  - 清晰概念 → 路由到 `map-modules`
  - 已有项目 → 路由到 `adopt`
- **输出**：路由目标技能名与交接说明

### 阶段 4：设置审查模式

- **输入**：用户位置答案
- **处理**：通过 AskUserQuestion 询问审查模式：
  1. full — 完整多角色审查（推荐团队）
  2. lean — 精简审查（推荐小团队）
  3. solo — 单人模式（推荐个人开发）
  将选择写入 `.claude/docs/review-mode.md`
- **输出**：审查模式配置文件

### 阶段 5：交接

- **输入**：路由目标 + 审查模式
- **处理**：生成交接说明，包含：目标技能名、下一步命令、推荐初始参数
- **输出**：交接提示消息

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 中的交接规范
- 参考 `workflow-catalog.yaml` 获取阶段定义

## 推荐下一步

根据路由结果执行对应技能。例如选择"没有想法"后，推荐运行 `/brainstorm` 开始创意构思。