---
name: bug-triage
description: "Bug 重新优先排序技能。读取所有未解决 Bug，按严重度、影响面、紧急度重新排序，输出分流建议与处理路径分配。"
license: MIT
metadata:
  model: sonnet
  argument-hint: "[可选: Sprint-id 或 Bug 列表路径]"
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
    windsurf: {enabled: true, trigger: /bug-triage}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# bug-triage —— Bug 重新优先排序技能

## 技能目的

读取项目内所有未解决 Bug，依据严重度、影响面、业务紧急度与修复成本重新排序，
给出分流建议（立即修复 / 本 Sprint / 下 Sprint / 暂缓），并分配处理路径，
帮助团队在有限资源下优先解决高价值缺陷。

## 参数说明

- `[可选: Sprint-id 或 Bug 列表路径]`：
  - 省略时默认读取 `docs/bugs/BUG-LIST.md` 全量未解决 Bug。
  - 提供 Sprint-id 时仅排序该 Sprint 范围内发现的 Bug。
  - 提供列表路径时读取该自定义列表。

## 分阶段工作流

### 阶段 1：收集未解决 Bug

- **输入**：用户参数或默认列表路径。
- **处理**：使用 Read 读取 `docs/bugs/BUG-LIST.md`；使用 Glob 枚举 `docs/bugs/BUG-*.md` 逐个读取详情。
- **输出**：未解决 Bug 全量清单，含编号、标题、严重度、状态。

### 阶段 2：评估维度

- **输入**：阶段 1 的 Bug 清单。
- **处理**：对每个 Bug 评估：
  1. 严重度（阻断 / 严重 / 一般 / 轻微）
  2. 影响面（全用户 / 部分角色 / 个别场景）
  3. 业务紧急度（是否阻塞发布或关键流程）
  4. 修复成本线索（涉及模块数、是否需架构改动）
- **输出**：每个 Bug 的评估卡片，含四维评分。

### 阶段 3：排序与分流

- **输入**：阶段 2 的评估卡片。
- **处理**：按综合优先级排序，分配到四个分流桶：
  - `hotfix-now`：立即修复
  - `this-sprint`：本 Sprint 内修复
  - `next-sprint`：下 Sprint 规划
  - `defer`：暂缓并记录理由
- **输出**：分流建议表，含处理路径与负责 Agent 建议。

### 阶段 4：确认与落盘

- **输入**：阶段 3 的分流建议表。
- **处理**：使用 AskUserQuestion 向用户确认分流决策；获批准后使用 Write 更新 `docs/bugs/BUG-LIST.md` 的优先级与分流字段。
- **输出**：更新后的列表路径与本次分流摘要。

## 协作协议引用

- 分流决策需用户确认，不得自主改写优先级。
- 写入列表前必须询问："我可以将分流结果更新到 [路径] 吗？"
- 热修复候选由用户最终拍板，本技能仅提供建议。

## 推荐下一步

- 标记为 `hotfix-now` 的 Bug 运行 `/hotfix [Bug 编号]` 启动紧急修复。
- 标记为 `this-sprint` 的 Bug 可创建修复 Story 后运行 `/dev-story`。
- 全量分流完成后运行 `/sprint-status` 查看进度影响。