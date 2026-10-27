---
name: performance-regression-analysis
description: "Explicit-invocation analysis of one measured performance regression against a defined baseline and workload using profiles, benchmarks, traces, logs, or reproducible experiments. Do not trigger for ordinary slowness guesses, replace general code review, or optimize code. 仅显式调用：针对明确基线和工作负载，使用 profile、benchmark、trace、日志或可复现实验分析一个已测量的性能回归。不得因普通性能猜测而触发，不替代代码审查，也不优化代码。"
---

# Performance Regression Analysis（性能回归分析）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `standard`; explicit invocation is required.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Performance Regression Analysis

Analyze one specific performance regression. Keep production code and configuration unchanged.

## Boundary
- Require a baseline, workload, metric, or explicit plan to obtain them. Do not claim regression from code appearance alone.
- Route broad code review to `safe-code-review`, general health to `project-health-check`, test implementation to `safe-test-implementation`, and optimization implementation to `safe-fix-implementation`.
- Do not run unsafe load against production or infer causality from one noisy sample.

## Workflow
1. Define baseline and candidate versions, environment, workload, dataset, warmup, concurrency, metric, percentile, budget, and measurement method.
2. Inspect supplied profiles, benchmarks, traces, logs, query plans, browser traces, or reproducible experiments; record missing controls.
3. Compare algorithms, repeated I/O, N+1 behavior, caches, allocation and memory, concurrency and contention, network, database, serialization, and frontend rendering as applicable.
4. Separate measured regression, correlated observation, code-based hypothesis, and unknown.
5. Check variance, sample size, cold/warm effects, environment drift, and measurement bias before attributing cause.
6. Rank hypotheses by impact, evidence, confidence, and experiment cost; propose falsifiable validation experiments and optimization priorities.
7. Do not optimize code; report exact evidence, locations, impact, severity/priority, confidence, validation, and unknowns.

# Output Contract
1. Scope, baseline, workload, and metrics
2. Evidence and measurement quality
3. Findings with measured/inferred status, severity, impact, and confidence
4. Ranked hypotheses and affected locations
5. Validation experiments and expected signals
6. Optimization priorities without implementation
7. Unknowns

---

## 执行契约

默认使用 `standard`；仅允许用户显式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 性能回归分析

分析一个具体性能回归，保持生产代码和配置不变。

## 职责边界
- 需要基线、工作负载、指标或获取它们的明确方案；不得仅凭代码外观声称回归。
- 广泛代码审查交给 `safe-code-review`，一般体检交给 `project-health-check`，测试实施交给 `safe-test-implementation`，优化实施交给 `safe-fix-implementation`。
- 不对生产执行不安全压力，也不从单个噪声样本推断因果。

## 工作流程
1. 明确基线与候选版本、环境、工作负载、数据集、预热、并发、指标、分位数、预算和测量方法。
2. 检查用户提供的 profile、benchmark、trace、日志、查询计划、浏览器 trace 或可复现实验，记录缺失控制变量。
3. 按适用情况比较算法、重复 I/O、N+1、缓存、分配与内存、并发与争用、网络、数据库、序列化和前端渲染。
4. 分离已测量回归、相关观察、代码假设和未知。
5. 归因前检查方差、样本量、冷热效应、环境漂移和测量偏差。
6. 按影响、证据、置信度和实验成本排序假设，提出可证伪实验和优化优先级。
7. 不优化代码，报告准确证据、位置、影响、严重度/优先级、置信度、验证和未知项。

# 输出契约
1. 范围、基线、工作负载和指标
2. 证据与测量质量
3. 发现、测量/推断状态、严重度、影响和置信度
4. 排序假设与受影响位置
5. 验证实验与预期信号
6. 不含实施的优化优先级
7. 未知项
