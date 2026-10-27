---
name: architecture-deepening-analysis
description: "Explicit-invocation, read-only analysis of evidence-backed architecture friction and migratable, reversible deepening options after concrete caller or change evidence exists. Do not trigger for a simple refactor, judge by file size, create speculative abstractions, or write files. 仅显式调用：在已有具体调用方或变更证据后，只读分析架构摩擦并比较可迁移、可回滚的深化方案。不得因简单重构而触发、按文件大小下结论、创建推测性抽象或写入文件。"
---

# Architecture Deepening Analysis（架构深化分析）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `standard`; explicit invocation is required.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Architecture Deepening Analysis

Architecture friction is credible when callers, changes, or tests repeatedly pay for knowledge a module should contain.

## Output modes

- `fast`: top candidate, evidence, risk, recommendation, and next Skill.
- `standard` (default): all qualified candidates with two or more options, migration, testing, and rollback.
- `audit`: `standard` plus complete scope, command ledger, rejected candidates, ADR evidence, uncertainty, and option scoring rationale.

Read `references/architecture-friction-checklist.en.md` only when evaluating candidates or producing audit evidence.

## Boundary and evidence

- This Skill analyzes and plans. It never performs a broad refactor, edits files, creates an ADR, or changes tests.
- Read repository instructions, domain terminology, relevant ADRs, callers, implementations, tests, and change history available within scope.
- Shell access permits only preflighted, non-destructive read-only discovery such as search, status, diff, log, and existing analysis commands with known side effects. Never install, migrate, deploy, publish, delete, switch branches, or mutate the working tree.
- Do not infer architecture quality from file size, directory shape, naming preference, or aesthetic neatness.
- Require concrete caller, change, duplication, defect, or test evidence. Do not create an abstraction for a hypothetical future caller.
- Treat personal style as a preference, not a defect. Existing ADRs constrain options until evidence justifies reopening them.
- If the user asks to directly rewrite a large area, stop and route through `requirements-clarification`, `change-impact-analysis`, `safe-change-plan`, and an explicitly authorized implementation workflow.

## Analysis dimensions

Examine interface size and required caller knowledge; how much complexity the implementation actually hides; responsibility leakage; domain-boundary clarity; repeated adaptation; scattered change; test-seam stability; whether deleting the module removes or merely transfers complexity; unnecessary abstractions; real use-case support; and relevant ADR constraints.

## Workflow

1. Define the architecture scope, decision need, and evidence threshold. Identify the callers or change history that motivated the analysis.
2. Read the minimum repository and domain context needed to understand responsibilities and constraints.
3. Map each candidate's interface, callers, implementation responsibility, adapters, test seams, recent change paths, and ADR constraints.
4. Record observed friction with file/line or commit evidence. Reject candidates supported only by size, taste, or one hypothetical use case.
5. Test the causal explanation: determine whether the interface exports knowledge that belongs behind it, whether repeated adaptations express the same rule, and whether deleting the abstraction removes or redistributes complexity.
6. Estimate impact across callers, compatibility, data, runtime, operations, tests, and ownership.
7. Develop at least two materially different design directions, including a conservative option when plausible. For each, describe what knowledge moves, what remains public, migration cost, testing approach, rollback, and risk.
8. Recommend one direction and explain why the alternatives are not selected. Do not conceal uncertainty or ADR conflict.
9. Provide an ordered migration that preserves runnable checkpoints, a test strategy at stable observable seams, and a rollback point for each material step.
10. Decide whether an ADR is required and recommend the next Skill. Do not write the ADR or execute the migration.

## Candidate completeness and stop conditions

Each reported candidate must include observed friction, code evidence, root cause, impact scope, at least two options, recommendation, rejection reasons, migration order, test strategy, rollback strategy, risk, ADR need, and next Skill.

Return `Blocked` when scope is undefined, callers cannot be inspected, essential ADRs are unavailable, or command safety is uncertain. Return `no qualified candidates` when evidence does not support a recommendation; do not manufacture one.

# Output Contract

Lead with `status`, top recommendation or `no qualified candidates`, risk, and next Skill.

For every candidate include:

1. Observed friction
2. Code/commit/ADR evidence with tight locations
3. Root cause and confidence
4. Impact scope and affected callers
5. At least two materially different design options
6. Recommended option
7. Why other options are not selected
8. Ordered migration with runnable checkpoints
9. Test strategy at observable seams
10. Rollback strategy
11. Risk level
12. ADR requirement
13. Recommended next Skill

Audit mode also lists command evidence, rejected candidates, unknowns, and permission decisions. Do not include implementation edits.

---

## 执行契约

默认使用 `standard`；仅允许用户显式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# Architecture Deepening Analysis（架构深化分析）

当调用方、修改或测试反复承担本应由模块内部消化的知识时，架构摩擦才有可信依据。

## 输出模式

- `fast`：首要候选、证据、风险、建议和下一 Skill。
- `standard`（默认）：全部合格候选，每项包含至少两个方案、迁移、测试和回滚。
- `audit`：在 `standard` 基础上增加完整范围、命令账本、被拒绝候选、ADR 证据、不确定性和方案评分理由。

评估候选或准备 audit 证据时，才读取 `references/architecture-friction-checklist.zh-CN.md`。

## 边界与证据

- 本 Skill 只分析和规划，绝不执行大范围重构、编辑文件、创建 ADR 或修改测试。
- 阅读仓库指令、领域术语、相关 ADR、调用方、实现、测试和范围内可用变更历史。
- Shell 权限只允许经过预检的非破坏性只读发现，例如搜索、status、diff、log 和副作用已知的现有分析命令；不得安装、迁移、部署、发布、删除、切换分支或改变工作区。
- 不得仅凭文件大小、目录形态、命名偏好或“更干净”判断架构质量。
- 必须具备具体调用方、变更、重复、缺陷或测试证据；不得为假想未来调用方创建抽象。
- 个人风格属于偏好，不是缺陷。现有 ADR 在证据足以重新讨论前约束方案。
- 用户要求直接重写大范围代码时停止，转给 `requirements-clarification`、`change-impact-analysis`、`safe-change-plan` 和获得明确授权的实施流程。

## 分析维度

检查接口大小和调用方必需知识、实现实际隐藏的复杂度、职责泄漏、领域边界、重复适配、修改分散、测试接缝稳定性、删除模块后复杂度是消失还是转移、不必要抽象、真实用例支持和 ADR 约束。

## 工作流程

1. 定义架构范围、决策需求和证据门槛，识别触发分析的调用方或变更历史。
2. 阅读理解职责与约束所需的最小仓库和领域上下文。
3. 映射每个候选的接口、调用方、实现职责、适配逻辑、测试接缝、近期修改路径和 ADR 约束。
4. 用文件/行或 commit 证据记录观察到的摩擦；仅由大小、风格或单个假想用例支持的候选直接拒绝。
5. 验证因果解释：接口是否向外暴露本应隐藏的知识、重复适配是否表达同一规则，以及删除抽象后复杂度是消失还是重新分散。
6. 估计对调用方、兼容性、数据、运行时、运维、测试和归属的影响。
7. 提出至少两个有实质差异的设计方向；可行时包含保守方案。每项说明知识如何移动、哪些仍公开、迁移成本、测试方式、回滚和风险。
8. 推荐一个方向并解释不选择其他方案的理由；不得隐瞒不确定性或 ADR 冲突。
9. 给出保持可运行检查点的迁移顺序、基于稳定外部接缝的测试策略，以及每个重大步骤的回滚点。
10. 判断是否需要 ADR，并推荐下一 Skill；不编写 ADR，也不执行迁移。

## 候选完整性与停止条件

每个报告候选必须包含：观察到的摩擦、代码证据、根本原因、影响范围、至少两个方案、推荐方案、其他方案不采用理由、迁移顺序、测试策略、回滚策略、风险、是否需要 ADR 和下一 Skill。

范围未定义、调用方无法检查、关键 ADR 不可用或命令安全不确定时返回 `Blocked`。证据不足时返回“无合格候选”，不得制造建议。

# 输出契约

先给 `status`、首要建议或“无合格候选”、风险和下一 Skill。

每个候选必须包含：

1. 观察到的摩擦
2. 具有精确位置的代码/commit/ADR 证据
3. 根本原因和置信度
4. 影响范围和受影响调用方
5. 至少两个有实质差异的设计方案
6. 推荐方案
7. 不采用其他方案的理由
8. 包含可运行检查点的迁移顺序
9. 基于外部可观察接缝的测试策略
10. 回滚策略
11. 风险等级
12. 是否需要 ADR
13. 推荐下一 Skill

audit 模式还要列出命令证据、被拒绝候选、未知项和权限判断。不得包含实施修改。
