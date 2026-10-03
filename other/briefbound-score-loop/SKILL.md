---
name: briefbound-score-loop
description: "Use when repeated work is governed by an explicit metric, active baseline, candidate search, promotion rule, leaderboard feedback, or submission iteration; do not use for a one-off research check that its current owner can execute directly, or for non-competition performance optimization and profiling."
license: MIT
---

# Briefbound Score Loop

## 目标

围绕一个明确指标主动寻找候选，用可比较证据决定是否替换当前最好方案。它负责一条量化优化 lane，不负责整个研究方向或竞赛生命周期。

## Briefbound task contract

- Context Boundary: 主指标、硬约束、当前最好方案、搜索空间、评价协议、预算和允许写入面。
- Output Contract: 下一候选、可比结果、决定、可复用证据和停止/转向信号。
- Allowed Action: 在已确认范围内提出并评估候选；不静默改变指标、数据、基线、预算或提交目标。
- Success Evidence: 精确 baseline/candidate、参数或 diff、命令、数据/seed、主副指标、运行产物和可比性判断。
- Stop Condition: 协议漂移、指标无法解析、候选重复、预算耗尽、连续结果不再提供新信息、写入冲突或安全边界变化。
- Route Out: 继续当前 loop、返回 `briefbound-ai-research-loop`、`briefbound-bug-review`、`briefbound-development-cleanup`（验证后的真实残留）、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract；复合任务不吞其他 owner；Route Out 仅以 Briefbound task contract 为准。
- 用户可见内容默认中文，先说结论，再给比较依据。默认使用“替换、淘汰、继续观察、暂时无法比较”等通俗说法；必须保留枚举时写成中文结论加括号，例如“替换当前最好方案（`PROMOTE`）”。
- 复杂指标、代理测试或搜索策略会影响判断时，用一句话解释；不展示内部 trial 账本。有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 实验 owner 独占

只有主要未知量是“怎样持续改善一个明确指标”时进入。AI Research 中一次低成本比较由原 owner 直接执行。

分数下降、candidate reject 和 online neutral/worse 是实验结果，不是 TDD RED。metric/parser/schema/seed/shape/NaN/打包出现确定性错误时，临时路由 `briefbound-bug-review`，修复后回到原 lane。

## Protocol Freeze

比较前冻结以下协议；任何一项变化都先建立新 baseline，不能把前后结果直接相减：

- 主指标、越大/越小更好和最小有效提升；
- 硬约束与副指标，不能用主指标掩盖合法性、正确性或资源超限；
- baseline 的 commit/hash/config；
- 数据、case、seed、运行环境和评价命令；
- 单候选预算、总预算和停止条件。

若目标确实有多个指标，先指定主指标与硬约束；只有用户明确接受综合规则时才做加权，不临时拼一个总分。

## Search Policy

每轮先选择一种搜索意图，再生成候选：

- `EXPLOIT`：已有稳定正向信号时，在当前最好方案附近做小步改动。
- `EXPLORE`：结果停滞或局部空间已重复时，尝试机制不同的方向。
- `DIAGNOSE`：噪声、代理指标或失败原因不清时，先设计能区分原因的检查。

把变量写成可判断的搜索空间：类别、顺序、数值或结构变化。候选必须有一个主要因果机制和唯一指纹；已做过的同机制、同方向、同边界候选直接跳过。随机变化若不能回答问题，也不进入队列。

## ASK -> FILTER -> TELL

1. `ASK`：根据当前证据提出一个候选，写清机制、预期信号、`smallestDecisiveEvaluation` 和 kill condition。
2. `FILTER`：先做构建、合法性、成本和最小决定性检查。即使最乐观也过不了替换标准时，立即 `PRUNE`；诊断候选则按是否回答问题判断。
3. 通过初筛后跑代表性评价；昂贵完整评价只留给仍可能晋升的候选。
4. `TELL`：记录结果、可比性、机制判断和副作用，再更新下一轮的 `EXPLOIT / EXPLORE / DIAGNOSE` 选择。
5. 没有新变量、新证据或校准价值时停止，不用更多试验掩盖平台期。

内部 trial 可标记 `ASKED / RUNNING / PRUNED / COMPLETE / FAILED`；用户通常只需要知道结果和原因。

## 决定规则

- `PROMOTE`：可比较，主指标超过有效提升线，硬约束通过，代表性结果支持替换 baseline。
- `REJECT`：可比较但未过线，或副作用越过已确认边界。
- `HOLD`：方向有信息价值，但样本、稳定性或代表性不足，下一项验证明确。
- `BLOCKED`：协议漂移、证据缺失或结果不可解析，当前无法安全比较。

代理测试只用于筛选；不能证明目标指标提升。线上分数是稀疏外部证据，应与本地可复现结果分别记录。

## 自适应重量与并行

- `QUICK`：已有协议，直接完成一个 `ASK -> FILTER -> TELL`，不创建 profile、ledger、worker 或独立 artifact。
- `STANDARD`：反复候选或跨会话，维护最小 trial 历史与重复指纹。
- `FULL`：昂贵评价、线上反馈、提交包或真正独立的并行候选，使用项目已有事实源。

默认不创建 worker。只有写入面、资源和验证互相独立时才并行；worker 不能自行替换共享 baseline，只返回 diff、命令、指标和产物。

## 输出

```text
结论: 替换 / 淘汰 / 继续观察 / 暂时无法比较（必要时附内部枚举）
比较: <baseline、candidate、主指标变化和硬约束>
原因: <机制判断、关键副作用或证据缺口>
记录: <仅跨会话、线上反馈或可复用教训需要时>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```

## 方法来源

搜索循环参考 [Optuna](https://github.com/optuna/optuna) 的 Ask-and-Tell 与 pruning 思路，证据记录参考 [MLflow](https://github.com/mlflow/mlflow) 的 run/metric/artifact 模型；这里只重写为无新增依赖的 skill 契约。
