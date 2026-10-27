---
name: spec-to-work-items
description: "Decompose a confirmed specification, implementation plan, or settled conversation into independently executable and verifiable vertical work items with dependencies, safe parallelism, conflict areas, tests, risks, and rollback notes. Use for delivery planning of a multi-behavior scope; return copyable Markdown in the current response only and never write files, invoke Shell, or create external tasks even with user authorization. Do not use for unresolved requirements, a single small fix, or a file-by-file technical-layer checklist. 将已确认规格、实施计划或已闭合对话拆成可独立执行和验证的垂直工作项，明确依赖、安全并行、冲突区域、测试、风险和回滚。用于包含多个可交付行为的交付规划；只在当前响应返回可复制 Markdown；即使用户授权也不写文件、不调用 Shell、不创建外部任务。需求未闭合、单个小修复或按文件与技术层罗列清单时不使用。"
---

# English

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Spec to Work Items

Convert settled scope into delivery slices that can be executed and verified independently. Prefer observable behavior over technical layers.

## Boundary

- Require a confirmed specification, implementation plan, or sufficiently settled conversation. Route material open decisions to `requirements-clarification` or `requirements-to-spec`.
- Stay read-only. Return copyable Markdown only in the response. Never write a local file, use Shell to write indirectly, create GitHub Issues or Linear tickets, or call an external task system, even when the user asks; this Skill's metadata does not grant those capabilities.
- Do not substitute for the code-level atomic steps of `safe-change-plan`; this Skill owns delivery slicing, dependencies, and parallel coordination.
- Include migrations, compatibility, rollback, documentation, and tests within the behavior slice they support.

## Workflow

1. Establish the source specification, user-visible outcomes, acceptance criteria, exclusions, constraints, and unresolved assumptions.
2. Identify independently observable behaviors. Slice vertically so each item delivers one coherent outcome across the necessary layers.
3. For each item, define scope and out-of-scope boundaries, affected areas, acceptance criteria, the smallest credible verification, risks, rollback notes, and recommended Repo Doctor Skills.
4. Model prerequisites and blockers as a dependency graph. Name items that can run in parallel only when their dependencies, shared state, and integration sequence permit it.
5. Identify shared files, schemas, interfaces, fixtures, generated artifacts, and other conflict zones. Explain coordination when parallel items touch the same core area.
6. Keep tests close to each behavior. Do not defer all testing to a final item unless a genuinely cross-cutting verification cannot run earlier.
7. Validate the plan against the quality gates below; revise or reject it when a gate fails.
8. Return the ordered Markdown plan, parallel groups, integration checkpoints, and remaining planning unknowns.

## Quality Rejection Gates

Reject and explain a decomposition that:

- consists only of database, backend, frontend, documentation, or test layers;
- cannot verify an item independently;
- uses acceptance criteria such as only “development complete”;
- leaves dependencies unspecified;
- assigns broad edits to the same core files without declaring conflicts;
- postpones all tests to the end; or
- combines unrelated outcomes in one item.

## Completion Conditions

Complete only when every item has all required fields, dependencies are acyclic or explicitly blocked, parallel claims are justified, conflicts are visible, and every acceptance criterion is observable and verifiable.

If the user needs persistence, state that the plan was not saved and ask them to save the Markdown manually or use an existing Skill whose metadata explicitly permits the requested documentation write.

# Output Contract

Start with source scope, dependency overview, parallel groups, conflict zones, and integration checkpoints. Then provide every work item with:

- `id`
- `title`
- `goal`
- `user_visible_outcome`
- `scope`
- `out_of_scope`
- `affected_areas`
- `dependencies`
- `parallelizable_with`
- `acceptance_criteria`
- `verification`
- `risks`
- `rollback_notes`
- `recommended_skills`
- `status`

End with rejected decomposition patterns, unresolved assumptions, and confirmation that no file, Shell workaround, external issue, or task was created.

# 简体中文

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# Spec to Work Items（规格拆分工作项）

把已闭合范围转成可独立执行和验证的交付切片，优先按可观察行为拆分，不按技术层机械切割。

## 职责边界

- 需要已确认规格、实施计划或足够闭合的对话；仍有关键决策时转给 `requirements-clarification` 或 `requirements-to-spec`。
- 保持只读，只在当前响应中输出 Markdown 工作项计划。即使用户明确授权，也不得写入本地文件、调用 Shell、创建 GitHub Issue、Linear 任务或任何外部对象。
- 不替代 `safe-change-plan` 的代码级原子步骤；本 Skill 负责交付切片、依赖和并行协调。
- 迁移、兼容、回滚、文档和测试应进入其所支持的行为切片。

## 工作流程

1. 明确来源规格、用户可见结果、验收标准、排除项、约束和未解决假设。
2. 识别可独立观察的行为，按垂直切片拆分，使每项跨越必要技术层并交付一个完整结果。
3. 每项写明范围、范围外、影响区域、验收标准、最小可信验证、风险、回滚说明和推荐 Repo Doctor Skills。
4. 将前置条件和阻塞建成依赖图。只有依赖、共享状态和集成顺序允许时才声明可以并行。
5. 标识共享文件、Schema、接口、fixture、生成物等冲突区域；并行项触碰同一核心区域时说明协调方式。
6. 测试跟随对应行为，不得把所有测试推迟到最后；只有真正跨切片验证无法提前运行时才单列最终验证。
7. 使用下述质量门禁检查计划，不通过时修改或拒绝该拆分。
8. 输出有序 Markdown 计划、并行组、集成检查点和剩余规划未知项。

若用户要求持久化工作项，请输出可复制的 Markdown，并让用户自行保存，或明确转交给已有且获得写权限的专用工具；不得用 Shell、临时脚本或其他变通方式绕过 `write_files: false`。

## 低质量拒绝门禁

出现以下情况应拒绝并解释：

- 只按数据库、后端、前端、文档或测试层拆分；
- 工作项无法独立验证；
- 验收标准只有“完成开发”；
- 缺少依赖关系；
- 多项大范围修改相同核心文件却未声明冲突；
- 所有测试都推迟到最后；
- 一个工作项混入多个无关目标。

## 完成条件

只有每项必需字段齐全、依赖无环或明确阻塞、并行声明有依据、冲突可见，且每条验收标准都可观察和验证时才完成。

# 输出契约

先给出来源范围、依赖概览、并行组、冲突区域和集成检查点。随后每个工作项必须包含：

- `id`
- `title`
- `goal`
- `user_visible_outcome`
- `scope`
- `out_of_scope`
- `affected_areas`
- `dependencies`
- `parallelizable_with`
- `acceptance_criteria`
- `verification`
- `risks`
- `rollback_notes`
- `recommended_skills`
- `status`

最后列出被拒绝的低质量拆分模式、未解决假设，并确认没有写入文件、使用 Shell 变通或创建任何外部 Issue 与任务。
