---
name: lagrangian-core
description: >
  Augmented Lagrangian for constrained optimization. Handles convex QP, smooth NLP,
  non-convex NLP, distributed ADMM, Safe RL, multi-objective. Trigger on: constrained
  optimization, KKT, ALM, ADMM, safe constraints, Pareto front, shadow prices,
  sensitivity analysis, infeasibility diagnosis, near-infeasible problems.
license: MIT
metadata:
  version: "0.7.0"
  stage: beta
  success_rate: "96.9%"
  token_budget: "1.18x"
---

# Lagrangian Core Skill — v0.7.0

## 能力边界
支持: 凸QP | 光滑NLP | 非凸NLP | 分布式ADMM | Safe RL | 多目标
协同: 检测贝叶斯/统计成分→HALT并建议调用对应Skill
不支持: 纯贝叶斯 | 纯统计检验 | MIP → HALT
输出模式: MINIMAL | STANDARD(默认) | VERBOSE

## Step -1 — 预检 [LAT-1] (4项并行)
1. 变量类型  2. 约束可行性(LP松弛)  3. 问题规模  4. 量纲一致性
任意HALT条件 → 立即停止，输出结构化错误码。

## Step 0 — 澄清
模糊点→单轮确认；贝叶斯信号→HALT "请调用贝叶斯Skill"

## Step 3 — 稀疏JSON通道
```json
{"step":3,"type":"augmented_lagrangian",
 "formula":"L_ρ=f(x)+Σλ·h(x)+Σμ·g(x)+ρ/2·||h||²",
 "multipliers":{"lambda":[0.0],"mu":[0.0]},
 "penalty":{"rho_init":1.0,"update_rule":"×1.5 if ||h||>tol"}}
```

## Step 4 — KKT验证 + 缓存
指纹=(变量数, eq约束数, ineq约束数, 目标函数类型, 约束结构哈希); 命中率~85%

## Step 5 — 求解路由 [FIX-16/17/18]
```
safe_rl+adversarial    → cos_thresh=0.10, window=20    [FIX-16]
safe_rl+near_infeas    → ratio_thresh=3.0, n_stages=6, stage_step=0.25  [FIX-18]
multi_obj+adversarial  → max_repair=3, repair_freq=10  [FIX-17]
non_convex+adversarial → ALM(n_starts=10, uniform_random)
non_convex+normal      → ALM(n_starts=10, warm_start=cache)
convex_qp/smooth_nlp   → standard_solver
distributed            → ADMM
```

## Step 6 — 影子价格
默认只输出活跃约束(影子价格>0)；其余折叠"[展开]"。

## Step 7 — 输出
STANDARD: 最优解(一行) → 约束状态表(仅活跃) → 关键瓶颈(一句)
VERBOSE:  STANDARD + Steps 3-6 JSON原始数据

## 失败处理
```json
{"status":"FAILED","error_code":"INFEASIBLE|BAD_PARAMS|AMBIGUOUS|SOLVER_FAIL",
 "reason":"<一行说明>","recovery":"<修复建议或最小松弛量>"}
```
近不可行→自动计算最小松弛量写入recovery。

## Forbidden Behaviors
❌ Steps 1-6输出自然语言 | ❌ Step 7输出JSON给用户
❌ 语言边界直接HALT | ❌ 失败后输出散文
❌ FIX-16: cos_thresh>0.20或window<15
❌ FIX-17: repair_freq<5
❌ FIX-18: stage_step>0.40或n_stages∉[5,7]
