---
name: estimate
description: "产出结构化工作量估算，使用 estimate.md 模板按Story维度分解估算。"
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
    windsurf: {enabled: true, trigger: /estimate}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# estimate — 工作量估算

## 技能目的

为 Story 或 Epic 产出结构化工作量估算，使用模板按维度分解（开发、测试、文档、集成），标注不确定性与风险，支持 Sprint 容量规划。

## 参数说明

本技能无参数。自动扫描待估算的 Story。

## 分阶段工作流

### 阶段 1：加载待估算 Story

- **输入**：项目目录
- **处理**：
  1. 使用 Glob 查找 `.claude/docs/templates/estimate.md` 模板
  2. 使用 Glob 扫描 `docs/stories/**/*.md` 获取待估算 Story
  3. 使用 Read 读取每个 Story 的描述、验收标准、任务清单
  4. 使用 Read 读取 `docs/architecture/control-manifest.md` 获取约束
- **输出**：Story 集合 + 模板

### 阶段 2：维度分解估算

- **输入**：Story 集合
- **处理**：
  1. 为每个 Story 按维度分解：前端开发、后端开发、数据库、测试、文档、集成
  2. 使用故事点（Story Points）或理想人时（Ideal Hours）估算
  3. 通过 AskUserQuestion 与用户确认估算方法
  4. 参考历史数据或类似 Story 的实际耗时
- **输出**：维度估算表

### 阶段 3：标注不确定性与风险

- **输入**：维度估算表
- **处理**：
  1. 为每个估算标注不确定性等级（低/中/高）
  2. 识别导致不确定性的因素（技术未知、依赖未确认、需求模糊）
  3. 为高风险项添加缓冲系数
  4. 列出需要原型验证的技术点
- **输出**：风险标注表

### 阶段 4：汇总与写入

- **输入**：维度估算 + 风险标注
- **处理**：
  1. 汇总每个 Story 的总估算
  2. 汇总 Epic 级别总估算
  3. 基于模板填充各章节
  4. 向用户展示估算摘要
  5. 批准后使用 Write 写入 `docs/estimates/{epic-or-sprint}.md`
- **输出**：估算文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 估算规范
- 参考 `.claude/docs/templates/estimate.md` 模板
- 估算需标注不确定性，避免过度精确

## 推荐下一步

估算完成后使用 `/sprint-plan` 将 Story 纳入 Sprint。高不确定性项使用 `/prototype` 验证后重新估算。开发阶段使用 `/dev-story` 实现 Story。