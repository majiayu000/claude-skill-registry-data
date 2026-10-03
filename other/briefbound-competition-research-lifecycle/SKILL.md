---
name: briefbound-competition-research-lifecycle
description: Use when coordinating an end-to-end research competition or benchmark program across multiple lifecycle stages such as rules, data, baseline, experiments, claims, and submission; use a stage owner directly for isolated work.
license: MIT
---

# Briefbound 竞赛科研全流程

## 目标

维护竞赛/benchmark 项目的阶段边界、事实源和跨阶段依赖，让当前最具体 owner 连续推进。它是全项目协调层，不重复执行研究、score、写作或工程流程。

## Briefbound task contract

- Context Boundary: 竞赛规则、数据/metric、active baseline/evidence、当前阶段、关键 artifact、提交约束和截止时间。
- Output Contract: 当前阶段判断、跨阶段风险、一个 primary owner、阶段完成证据和下一阶段动作。
- Allowed Action: 读取项目事实源并协调当前阶段；具体实验、工程、审查和写作由最具体 owner 执行。
- Success Evidence: 规则/数据版本、baseline/实验记录、claim 来源、submission checklist 或外部反馈中的阶段必要证据。
- Stop Condition: 规则/metric/数据漂移、active evidence 冲突、关键提交要求未知、claim 无来源或继续会污染有效证据。
- Route Out: 当前阶段 owner、`briefbound-ai-research-loop`、`briefbound-score-loop`、`briefbound-research-rigor-review`、工程 owner、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配时回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文，完成只报状态、产出、证据和剩余风险；代码、命令、路径、错误原文、API/协议、skill 名和枚举保留原样；Route Out 仅以 Briefbound task contract 为准，末行 `下一步建议: <一个具体动作>`，且限于决策类建议（推荐方向、优先级或需用户拍板的选项），不把可自行完成的执行步骤包装成建议交回。

## 激活闸门

只有请求跨越至少两个阶段，或规则、数据、baseline、claim、submission 之间的依赖需要统一治理时进入。单次论文复现/消融用 AI Research，反复 metric 晋升用 Score Loop，关键 claim 审查用 Rigor Review，具体工程故障用对应工程 owner。

## 阶段地图

按项目实际情况映射，不强制创建八套 artifact：`规则与目标 -> 数据/协议 -> baseline -> 研究实验 -> 证据综合/claim -> 提交或发布`。

每次只维护：当前阶段、active truth、阻塞下一阶段的最小缺口、primary owner、完成证据。已有项目工件优先；缺少模板但不影响当前决策时继续，不为形式补文档。

## 协调规则

1. 先读取最相关的规则、metric、数据版本、baseline、实验结果、claim map 或提交清单，不扫描所有阶段。
2. 识别当前阶段及最早失效的上游证据；上游漂移时标记受影响下游为 stale 并回退修复。
3. 选择一个能直接产生下一阶段必要证据的 primary owner。当前 owner 完成后，若下一阶段明确且已授权，连续路由，不逐阶段询问。
4. AI Research 可以内部完成简单实验；只有反复晋升/榜单 lane 才下沉 Score Loop。普通 candidate gate 不经过 Rigor Review。
5. 只有论文/对外 claim、方向转向、重要 best-known 结果或高成本投入才进入 Rigor Review。
6. 并行只用于真正独立的 artifact 和写入面；不默认创建 3-6 lanes、worktree 或多 Agent。

Smoke/proxy 只用于可运行性、淘汰和排序，不替代正式目标评估。外部 leaderboard 是重要校准证据，但不能静默改变本地 protocol 或 claim 范围。

## 输出

```text
阶段: <当前阶段>
- Active truth: <规则/数据/baseline/evidence>
- 关键缺口或漂移: <仅真实项>
- Primary owner 与产出:
- 阶段完成证据:
下一步建议: <决策类动作：方向、优先级或需用户拍板的选项>
```

跨会话或正式交接时才读取 `references/lifecycle-reference.md` 和 `references/templates.md`；需要校准典型阶段切换时读取 `references/examples.md`。普通推进不输出完整 lifecycle 表、Briefbound gate 或阶段菜单。
