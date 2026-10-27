---
name: requirements-to-spec
description: "Convert requirements whose material product, data, security, permission, compatibility, and acceptance decisions are already closed into a structured, implementable, testable specification. Use when a clarification summary or settled discussion is ready for specification and only non-blocking assumptions remain; stop and route material open decisions to requirements-clarification. Do not use for task decomposition, implementation planning, code explanation, bug fixing, or direct edits. 将产品、数据、安全、权限、兼容性和验收等重大决策已经闭合的需求整理为结构化、可实施、可验证的规格。用于已有澄清摘要或讨论已定稿、只剩非阻塞假设时；发现重大未决决策必须停止并转交 requirements-clarification。不用于拆工作项、制定实施计划、解释代码、修 Bug 或直接修改。"
---

# English

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Requirements to Spec

Convert requirements whose material decisions are already closed into an implementable and testable specification. Do not reopen settled choices, modify files, or produce a file-by-file implementation plan.

## Boundary

- Require a clarification summary, settled discussion, or other evidence that material product, behavior, data, security, permission, compatibility, migration, and acceptance decisions are closed.
- Use repository evidence before labeling any current behavior or constraint.
- Continue with explicit assumptions only for non-blocking details that cannot materially change the specification.
- If a material decision remains open or reopens, stop specification work and hand the decision ledger to `requirements-clarification`; do not hide it under an assumption.
- Do not use this skill when the user supplied a complete formal specification, only wants existing code explained, wants a bug fixed, requests direct edits, or needs work-item decomposition.
- Route impact discovery to `change-impact-analysis`, implementation planning to `safe-change-plan`, settled feature delivery to `feature-implementation`, and diagnosed local repairs to `safe-fix-implementation`.
- Match the user's language. Preserve code identifiers, paths, API names, commands, and error messages.

## Workflow

1. Cite the clarification summary or settled source and confirm that no material decision remains open.
2. Restate the requirement and identify target users, business goal, current state, desired behavior, and measurable success.
3. Inspect relevant repository docs, code, configuration, APIs, tests, and conventions. Cite paths or commands for every repository-derived claim.
4. Separate in-scope behavior, out-of-scope behavior, constraints, dependencies, non-blocking assumptions, deferred items, and unknown evidence.
5. Describe normal flows, failure flows, boundary cases, permissions, compatibility, and migration expectations.
6. Mark unsupported details as unknown. Give each non-blocking assumption a confidence level and verification method.
7. Write testable acceptance criteria in Given/When/Then or an equivalent observable form.
8. Recheck the specification for material decisions. If one remains, stop and route it to `requirements-clarification`.
9. Recommend `spec-to-work-items` for multi-step delivery or `change-impact-analysis` for a concrete code change; do not prescribe edits.

# Output Contract

1. Requirements summary
2. Users and goals
3. Current behavior, with evidence or `Unknown`
4. Target behavior
5. In scope
6. Out of scope
7. Constraints and dependencies
8. Assumptions, confidence, and verification
9. Non-blocking assumptions, deferred items, and unknown evidence
10. Acceptance criteria covering normal, failure, boundary, and compatibility behavior
11. Risks
12. Recommended next step

If a blocking decision exists, stop and return a handoff to `requirements-clarification` instead of presenting a completed specification. Do not include a file-by-file implementation plan or edits.

# 简体中文

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# Requirements Specification（需求规格化）

将重大决策已经闭合的需求转换成可实施、可测试的规格。不要重新打开已确认选择、修改文件或输出逐文件实施计划。

## 职责边界

- 必须已有澄清摘要、已定稿讨论或其他证据，证明产品、行为、数据、安全、权限、兼容、迁移和验收等重大决策已闭合。
- 先使用仓库证据，再描述当前行为或约束。
- 只有不会实质改变规格的细节才能作为显式假设继续。
- 发现重大决策仍未闭合或重新出现时，停止规格化并把决策台账交给 `requirements-clarification`，不得把它伪装成假设。
- 用户已提供完整正式规格、只要求解释代码、要求修 Bug、直接修改或需要拆工作项时，不使用本 Skill。
- 影响发现交给 `change-impact-analysis`，实施规划交给 `safe-change-plan`，已确认功能交付交给 `feature-implementation`，已诊断局部修复交给 `safe-fix-implementation`。
- 输出语言跟随用户输入；代码标识符、路径、API 名称、命令和错误信息保持原样。

## 工作流程

1. 引用澄清摘要或已定稿来源，确认不存在重大开放决策。
2. 复述需求，识别目标用户、业务目标、当前状态、期望行为和可衡量成功标准。
3. 检查相关文档、代码、配置、API、测试和约定，每条仓库结论引用路径或命令。
4. 区分范围内、范围外、约束、依赖、非阻塞假设、延期事项和未知证据。
5. 描述正常流程、异常流程、边界条件、权限、兼容和迁移要求。
6. 无证据细节标为未知；每个非阻塞假设附置信度和验证方式。
7. 使用 Given/When/Then 或等价可观察结构编写可测试验收标准。
8. 再次检查重大决策；仍有开放项时停止并转交 `requirements-clarification`。
9. 多步骤交付推荐 `spec-to-work-items`，具体代码变更推荐 `change-impact-analysis`；不要规定实际修改。

# 输出契约

1. 需求摘要
2. 用户与目标
3. 当前行为，附证据或标记“未知”
4. 目标行为
5. 范围内
6. 范围外
7. 约束与依赖
8. 假设、置信度与验证方式
9. 非阻塞假设、延期事项和未知证据
10. 验收标准，覆盖正常、异常、边界和兼容性行为
11. 风险
12. 建议下一步

存在阻塞决策时，必须停止并输出给 `requirements-clarification` 的交接，不得声称规格已完成。不得包含逐文件实施计划或实际修改。
