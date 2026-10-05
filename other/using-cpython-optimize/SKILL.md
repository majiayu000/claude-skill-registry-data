---
name: using-cpython-optimize
description: Use when CPython/CinderX 任务需要跨环境、跑分、crash 或 JIT 分析选择工作流；单项操作直接用对应技能。
---

# CPython/CinderX Optimize Router

根据用户目标选择所需 Skill 或 Workflow。已指定技能、只读结果、局部代码审查和文档修改可直接完成，不必经过 Orchestrator → Workflow → Agent 全链路。

## 单项任务

| 当前需要 | 技能 |
|----------|------|
| 审计 / 初始化 / 清理 lab | `cinderx-env-validate` / `cinderx-env-bootstrap` / `cinderx-env-clean` |
| 远程操作或卡顿诊断 | `cinderx-remote-lab-ops` |
| A/B 资源隔离 | `cinderx-ab-run-slot` |
| 功能或集成测试 / 最小 JIT | `cpython-runtime-test-run` / `cinderx-smoke-check` |
| 单 worker / 正式 suite / 并行队列 | `pyperformance-worker-run` / `pyperformance-suite-run` / `cinderx-parallel-pyperformance` |
| 已有结果比较 / 统计图表 / 实验报告 | `pyperformance-result-compare` / `pyperformance-stat-report` / `cinderx-optimization-report` |
| native crash / HIR dump | `cinderx-gdb-core-triage` / `cinderx-hir-dump` |
| JIT 进入判定 / HIR-LIR / 解释执行分析 | `cinderx-jit-entry-check` / `cinderx-hir-lir-analyze` / `cinderx-interpreter-case-analyze` |
| 平台归因 / 单用例证据表 | `cinderx-isa-microarch-compare` / `cinderx-evidence-table` |
| 指令规格 / 编译器理论 | `isa-instruction-lookup` / `compiler-optimization-theory` |
| 验证范围或成本取舍 | `validation-strategy` |

## 多阶段任务

- 已有双平台差距：`workflow-cross-platform-delta-triage`
- 实施已知优化：`workflow-feature-driven-optimization`
- 尚未选定用例的系统扫描：`workflow-platform-differential-discovery`
- 深钻已选用例：`workflow-platform-differential-discovery-deepdive`
- 远程环境准备：`workflow-remote-cinderx-lab-setup`
- crash 复现到报告：`workflow-cinderx-crash-triage`
- 正式 A/B 回归：`workflow-pyperformance-regression`
- 单 benchmark 路径与优化分析：`workflow-jit-optimization-analysis`

只读取当前阶段需要的材料。已有环境和实验指纹未变时复用证据；源码、解释器、安装、flags 或 CPU 分配变化后重查受影响项。环境三态由 `cinderx-env-validate` 定义；正式 A/B 还需独立证明 baseline source 可信。

Workflow 的 Agent 列表示阶段职责，不要求创建子代理。需要角色交接或宿主允许委派时，查 [角色索引](references/agent-routing.md) 并只读选定角色；否则主 Agent 顺序执行相同职责。

## 决策与完成

用户当前要求和已有授权优先于技能中的默认流程。自行选择可从证据确定的路线、子集、日志目录和可逆隔离方案；不要让用户替你选择内部 Workflow 或验证等级。

只有目标/实验轴确实不明、将删除用户产物、影响其他任务或超出已知预算时，才询问阻塞部分，并继续独立的只读分析。需要提问格式时查 [澄清模板](references/clarifying-question-templates.md)，遵循当前宿主工具约束。

按请求完成实现、适当验证和结果交付；测试通过后仅因新改动、失败或未解风险扩大验证。证据门禁限制结论，不要求停下所有工作：baseline 不可信不能跑正式 A/B，缺 native 栈不能声称 crash 根因，未证明 benchmark 进入 JIT 不能给 HIR 优化结论。说明缺口并推进可验证部分。

指令集规格（编码、汇编语法、伪代码、`FEAT_xxx` 依赖、跨平台等价候选）使用 `isa-instruction-lookup` 查证，不凭记忆回答；引用带 `source_doc` 和页码。编译器理论使用 `compiler-optimization-theory` 的相关分支，落到具体指令时仍需查库。
