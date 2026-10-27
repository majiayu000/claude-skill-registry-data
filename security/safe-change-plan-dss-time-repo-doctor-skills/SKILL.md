---
name: safe-change-plan
description: "Turn a confirmed specification, root-cause finding, or impact analysis into an atomic, verifiable, reversible implementation plan with explicit scope and risk controls. Use only when material decisions are closed and blast radius is sufficiently known; route open decisions to requirements-clarification, settled requirements needing a specification to requirements-to-spec, unknown impact to change-impact-analysis, architecture rationale or decision documentation to architecture-decision-record, and execution to safe-fix-implementation. 将已确认规格、根因结论或影响分析转为原子化、可验证、可回滚且范围明确的实施计划。仅在重大决策已闭合且影响范围足够明确时使用；未决需求交给 requirements-clarification，已闭合但尚需规格化的需求交给 requirements-to-spec，影响未知交给 change-impact-analysis，架构理由或决策文档交给 architecture-decision-record，执行交给 safe-fix-implementation。"
---

# English

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Safe Change Plan

Convert confirmed analysis into a safe, atomic, verifiable, and reversible implementation plan. Do not execute the plan.

## Boundary

- Confirm that the requirement, desired behavior, and blast radius are sufficiently known.
- If material decisions remain open, recommend `requirements-clarification`; if decisions are settled but a testable specification is missing, recommend `requirements-to-spec`. If dependencies or compatibility impact are unknown, recommend `change-impact-analysis`.
- Do not modify code, tests, configuration, dependencies, or documentation.
- Route settled feature delivery to `feature-implementation` and diagnosed local repairs to `safe-fix-implementation`.
- Reject opportunistic refactors and unrelated cleanup.

## Workflow

1. Cite the confirmed specification, root-cause report, impact analysis, diff, or repository evidence that forms the plan basis.
2. Rate input sufficiency. Stop and ask only when a missing decision changes architecture, contracts, data safety, permissions, or rollback feasibility.
3. List `will change`, `may change`, and `will not change` scopes.
4. Identify prerequisites and API, database, configuration, permission, concurrency, compatibility, deployment, and release risks.
5. Split work into single-purpose steps ordered by dependency. Keep required work separate from recommended work and later optimization.
6. For every step state the goal, files or modules, intended change, dependency, validation method, failure signal, and rollback action.
7. Prefer compatibility layers, feature flags, additive migrations, and reversible sequencing when risk warrants them.
8. Define incremental validation, the complete test strategy, stop conditions, rollback plan, and definition of done.
9. Mark inferred paths or commands as assumptions; never invent repository commands.

# Output Contract

1. Plan basis and evidence
2. Input sufficiency
3. Scope: will change, may change, will not change
4. Preconditions
5. Atomic steps, each with goal, location, change, dependency, validation, failure signal, and rollback
6. Stepwise validation
7. Test strategy
8. Compatibility and release risks
9. Rollback plan
10. Stop conditions
11. Definition of done

Label every item as required, recommended, or later optimization. Do not execute any step.

# 简体中文

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 安全变更计划

把已确认分析转为安全、原子、可验证、可回滚的实施计划。不要执行计划。

## 职责边界

- 确认需求、目标行为和影响范围已经足够清楚。
- 重大决策仍开放时使用 `requirements-clarification`；决策已闭合但缺少可测试规格时使用 `requirements-to-spec`；依赖或兼容性影响未知时建议使用 `change-impact-analysis`。
- 不得修改代码、测试、配置、依赖或文档。
- 已确认功能交付交给 `feature-implementation`，已诊断局部修复交给 `safe-fix-implementation`。
- 拒绝顺手重构和无关清理。

## 工作流程

1. 引用作为计划依据的已确认规格、根因报告、影响分析、diff 或仓库证据。
2. 评估输入充分性；只有缺失选择会改变架构、契约、数据安全、权限或回滚可行性时才停止询问。
3. 分别列出“将修改”“可能修改”和“明确不修改”的范围。
4. 识别前置条件，以及 API、数据库、配置、权限、并发、兼容性、部署和发布风险。
5. 按依赖顺序拆成单一目的的小步骤；区分必须完成、建议完成和后续优化。
6. 每一步说明目标、文件或模块、修改内容、依赖关系、验证方法、失败信号和回滚动作。
7. 风险需要时优先采用兼容层、功能开关、增量迁移和可逆顺序。
8. 定义逐步验证、完整测试策略、停止条件、回滚方案和完成定义。
9. 推断出的路径或命令必须标记为假设，不得编造仓库命令。

# 输出契约

1. 计划依据与证据
2. 输入充分性
3. 范围：将修改、可能修改、明确不修改
4. 前置条件
5. 原子步骤；每步包含目标、位置、改动、依赖、验证、失败信号和回滚
6. 逐步验证
7. 测试策略
8. 兼容性与发布风险
9. 回滚方案
10. 停止条件
11. 完成定义

每项标记为必须完成、建议完成或后续优化。不得执行任何步骤。
