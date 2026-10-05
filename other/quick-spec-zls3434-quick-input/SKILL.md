---
name: quick-spec
description: "轻量级变更规范，适用于小型变更、配置调优、微调，产出精简的变更说明。"
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
    windsurf: {enabled: true, trigger: /quick-spec}
    trae: {enabled: true}
    hermes: {enabled: true, platforms: [macos, linux, windows]}
    workbuddy: {enabled: true}
---

# quick-spec — 轻量级变更规范

## 技能目的

为小型变更、配置调优、微调等不需要完整 SRS 流程的场景，产出精简的变更说明文档，确保变更可追溯但不增加不必要的文档负担。

## 参数说明

本技能无参数。通过交互式问答收集变更信息。

## 分阶段工作流

### 阶段 1：评估变更范围

- **输入**：用户交互
- **处理**：
  1. 通过 AskUserQuestion 询问变更目标与影响范围
  2. 评估是否确实属于轻量级变更（单模块、无架构影响、无数据迁移）
  3. 若超出轻量级范围，建议改用 `/requirement-spec`
- **输出**：变更范围评估结果

### 阶段 2：收集变更细节

- **输入**：变更范围
- **处理**：
  1. 询问变更原因、预期效果、涉及文件
  2. 使用 Grep 搜索可能受影响的现有代码或配置
- **输出**：变更细节清单

### 阶段 3：生成变更说明

- **输入**：变更细节清单
- **处理**：使用 Write 生成 `docs/changes/{变更名}.md`，包含：变更摘要、原因、影响范围、验收标准、回滚方案
- **输出**：变更说明文件

## 协作协议引用

- 遵循 `.claude/docs/templates/collaborative-protocols/design-agent-protocol.md` 轻量级变更规范

## 推荐下一步

直接进入开发阶段实现变更，或使用 `/create-stories` 将变更分解为用户故事。