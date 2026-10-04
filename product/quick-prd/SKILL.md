---
name: quick-prd
description: '在一个工作流中生成包含竞品分析的完整 PRD。当用户需要带竞品上下文的 PRD、想要快速记录功能、说"写一个带竞品对比的 PRD"、或需要综合的产品需求文档时使用。当用户提到创建 PRD 并附带竞品研究，或说"分析竞品并写需求"、"快速为 X 写 PRD"时激活。支持 HTML 原型输出格式。 Also triggers on: write a PRD with competitive analysis, analyze competitors and write requirements, quick PRD for X.'
layer: workflow
input-from: user
output-to: feature-launch
---

# Quick PRD Workflow

本工作流是 **full-pm-cycle 的 `mode: quick` 预设**。阶段定义、质量门控与状态管理的唯一权威在 `skills/full-pm-cycle/SKILL.md`（见其中 `## Execution Modes` 与 `## Workflow Stages`），本文件只定义预设参数与阶段裁剪概览。

## 参数映射

| 输入参数 | 映射到 | 说明 |
|:---------|:-------|:-----|
| `<feature description>` | 需求描述 | 作为 PRD 的功能需求输入 |
| `[competitors...]` | S1 竞品分析名单 | 提供时直接按名单运行 competitive-analysis |

## 阶段裁剪概览

| Stage | 内容 | 说明 |
|:------|:-----|:-----|
| S0 | 状态初始化 | 创建 `.ompm/` 状态目录与 `current-workflow.json` |
| S1 | 竞品分析 | 只跑 competitive-analysis（market-research 可选） |
| S2 | 轻量策略 | product-strategy 轻量（定位 + 优先级） |
| S2.5 | 硬门控 | Strategy Confirmation Gate，未确认不得进入 S3 |
| S3 | PRD + 原型 | prd-gen + prototype-design（HTML 原型） |
| S4 / S5 | 可选 | 仅当用户明确要求时执行 |

## 执行说明

- 激活后按 full-pm-cycle 的 `mode: quick` 执行，遵循其阶段定义与质量门控
- 工作流状态仍写入 `docs/product/.ompm/current-workflow.json`，快照写入 `docs/product/.ompm/workflow-state/{{workflow_id}}.json`
- 产出位置（`docs/product/prd/`、`docs/product/prototypes/`、`docs/product/.ompm/competitive-analysis.json` 等）均以 full-pm-cycle 定义为准
