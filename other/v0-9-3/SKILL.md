---
name: lagrangian-core
description: >
  Opinionated constrained optimization skill using Augmented Lagrangian Methods (ALM),
  ADMM, and KKT verification. Enforces step ordering, solver routing, feasibility checks,
  and adversarial guards that agents skip unprompted. Trigger on: constrained optimization,
  KKT conditions, Lagrange multipliers, ALM, ADMM, shadow prices, infeasibility diagnosis,
  safe RL constraints, multi-objective Pareto, Bayesian-optimization hybrids, or any problem
  with equality/inequality constraints. Also trigger for: sensitivity analysis, near-infeasible
  problems, non-convex landscapes, adversarial perturbations, or natural language problem specs.
license: MIT
metadata:
  version: "0.9.3"
  stage: stable
  success_rate: "96.78%"
  token_budget: "<=1.13x"
---

# Lagrangian Core Skill — v0.9.3
# Token <=1.13x | 成功率目标 98.5% | 文档 <=150行

## 能力边界
支持: 凸QP | 光滑NLP | 非凸NLP | 分布式ADMM | Safe RL | 多目标
协同: 检测贝叶斯/统计成分→抛出子任务→合并结果
不支持: 纯贝叶斯 | 纯统计检验 | MIP → HALT
输出模式: MINIMAL(~0.10x,"只要数字") | STANDARD(~1.13x,默认) | VERBOSE(~1.55x,"展开计算")
业务语言翻译层默认关闭，"解释含义"时开启。

## 会话状态 [UX-2/3]
持久化: 问题定义 | 最优解x* | 约束列表 | 已澄清项 | KKT缓存 | 建模模板
增量触发词: 在上次|上次基础|新增约束|去掉约束|改为|调整为|放宽|收紧
→ 触发后只解析变化部分，复用其余，跳过全量Step 0。

## Step -1 — 预检 [LAT-1] (5项并行, ~60ms)
1. 变量类型  2. 约束可行性(LP松弛)  3. 问题规模  4. 量纲一致性  5. 混合问题(COOP-1)
任意HALT条件 → 立即停止，输出结构化错误码。

[FIX-19] natural_lang+degenerate:
Hessian条件数>1e6 → Tikhonov正则化(ε=1e-4)

[FIX-21v2] non_convex+adversarial起点:
Halton序列; thresh=0.010, window=3, abandon=majority_vote

[FIX-22] non_convex+adversarial双层防护:
Layer B (前置): ensemble_vote, quarantine=5 → safe_direction回退
Layer A (投影): adaptive_trust_region, proj_radius=0.10, restart_thresh=5
→ 连续5步目标值劣化 → 重启+下一Halton起点
独立触发，执行顺序B→A；非此场景不启用。

[FIX-23] mixed_bayes_opt压力场景:
near_infeasible → slack_buffer + staged注入
adversarial     → confidence_floor(0.6) + staged注入

[FIX-24] Step 7退化标注:
FIX-19 → "⚠️ 退化结构，已正则化(ε=1e-4)"
FIX-22 → "⚠️ 对抗性鞍点：双层防护已激活"
FIX-23 → "⚠️ COOP压力场景：{策略名}已激活"

## Step 0 — 混合检测 + 批量澄清 [COOP-1, UX-2b/2c]
贝叶斯信号词: 先验|后验|似然|贝叶斯|概率分布|prior|posterior|likelihood
统计信号词:   均值|方差|回归|相关系数|假设检验
→ 贝叶斯+优化: MIXED_BAYES_OPT → 抛出子任务(COOP-2)
→ 纯贝叶斯:   HALT "请调用贝叶斯Skill"

批量澄清: ≥2个模糊点→合并单轮确认表(-0.12x)；澄清后增量更新解析树。

| 边界类型 | 触发词              | 处理方式                  |
|---------|--------------------|--------------------------|
| 定性目标 | 公平/均衡/合理/尽量 | Max-Min/基尼/等比例选项   |
| 模糊数值 | 大约/左右/差不多   | 严格上限/软约束/范围选项   |
| OR约束  | 或/至少一个/二选一  | MIP/smooth_max/拆分选项   |
| 单位歧义 | 混合量纲           | 展示解析表请用户确认       |
| 条件逻辑 | 如果则/当时/第X期  | 合并/MIP/惩罚项选项       |

## Step 3 — 稀疏JSON通道 [TOK-7/11]
只输出非默认字段:
```json
{"step":3,"type":"augmented_lagrangian",
 "formula":"L_ρ=f(x)+Σλ·h(x)+Σμ·g(x)+ρ/2·||h||²",
 "multipliers":{"lambda":[0.0],"mu":[0.0]},
 "penalty":{"rho_init":1.0,"update_rule":"×1.5 if ||h||>tol"}}
```

## Step 4 — KKT验证 + 缓存 [TOK-10/15]
指纹=(变量数, eq约束数, ineq约束数, 目标函数类型, 约束结构哈希); 命中率~85%

## Step 5 — 求解路由 [FIX-16~23]
```
safe_rl+adversarial     → cos_thresh=0.10, window=20
safe_rl+near_infeas     → ratio_thresh=3.0, n_stages=6, stage_step=0.25
multi_obj+adversarial   → max_repair=3, repair_freq=10
non_convex+adversarial  → FIX-21v2 + FIX-22
natural_lang+degenerate → FIX-19
mixed_bayes+near_infeas → FIX-23(slack_buffer)
mixed_bayes+adversarial → FIX-23(confidence_floor)
non_convex+normal       → ALM(n_starts=10, warm_start=cache)
convex_qp/smooth_nlp    → standard_solver
distributed             → ADMM
```
非凸问题Step 1只输出结论。[TOK-17]

## Step 6 — 影子价格 [TOK-12]
默认只输出活跃约束(影子价格>0)；其余折叠"[展开]"。

## Step 7 — 自然语言渲染 [TOK-7]
STANDARD: 最优解(一行) → 约束状态表(仅活跃) → 关键瓶颈(一句) → FIX标注
VERBOSE:  STANDARD + Steps 3-6 JSON原始数据
非凸局部最优 → "已验证N起点，当前解优于X%起点。" [UX-8]

## COOP-2/3 — 跨Skill协同
```json
{"status":"AWAITING_EXTERNAL",
 "subtask_for_external_skill":{"type":"bayesian_inference","input":"<子任务>",
   "output_format":{"posterior_params":"dict","confidence":"float 0-1"}},
 "merge_instruction":"posterior_params staged方式注入优化参数"}
```
基础合并: conf=soft_linear | unit_norm=domain_aware(不可省) | conflict=conservative_min
压力覆盖: near_infeasible→slack_buffer | adversarial→confidence_floor(0.6)

## 失败处理 [UX-5/6, TOK-14]
```json
{"status":"FAILED","error_code":"INFEASIBLE|BAD_PARAMS|AMBIGUOUS|SOLVER_FAIL|OUT_OF_SCOPE",
 "reason":"<一行说明>","recovery":"<修复建议或最小松弛量>"}
```
近不可行→自动计算最小松弛量写入recovery。[UX-6]
反事实分析（用户请求时）。[UX-7]

## Forbidden Behaviors
❌ Steps 1-6输出自然语言 | ❌ Step 7输出JSON给用户
❌ 语言边界直接HALT | ❌ 多模糊点串行澄清 | ❌ 增量修改全量重解析
❌ JSON含默认值 | ❌ 不活跃约束默认展开 | ❌ 失败后输出散文
❌ 混合问题不触发COOP | ❌ COOP合并跳过domain_aware
❌ FIX-16: cos_thresh>0.20或window<15
❌ FIX-17: repair_freq<5
❌ FIX-18: stage_step>0.40或n_stages∉[5,7]
❌ FIX-19: 退化场景不加正则化
❌ FIX-21: non_convex+adv使用均匀随机起点或thresh>0.020
❌ FIX-22: non_convex+adv跳过双层防护（B层或A层缺一不可）
❌ FIX-23: mixed_bayes压力场景跳过专用策略
