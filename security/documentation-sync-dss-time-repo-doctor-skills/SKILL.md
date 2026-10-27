---
name: documentation-sync
description: "Synchronize documentation with a confirmed code, configuration, API, or behavior change by updating only evidence-backed README, API, configuration, example, migration, and changelog content while preserving style and language. Use for documentation-only edits; do not modify production behavior, invent undocumented facts, or use as a general code fix. 根据已确认的代码、配置、API 或行为变更，只更新有证据支持的 README、API、配置、示例、迁移和 CHANGELOG 内容，并保留原有风格与语言。用于仅文档修改；不得改变生产行为、编造未证实内容，也不作为通用代码修复。"
---

# English

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Documentation Sync

Synchronize affected documentation with confirmed implementation, configuration, API, or behavior changes. Modify documentation only.

## Boundary

- Require confirmed implementation evidence, configuration, specification, or diff. Do not document planned behavior as shipped behavior.
- For a user-identified typo in one named document, the visible text and exact correction are sufficient evidence: edit only that file, run at most one targeted check, and stop without a broader documentation inventory.
- Modify only documentation and documentation-owned examples by default. Do not change production code, tests, configuration, dependencies, or behavior.
- If implementation appears wrong or contradicts the confirmed specification, report a blocker instead of changing business code.
- Preserve each document's language, structure, terminology, links, formatting, and local style.
- Do not rewrite unrelated sections or invent commands, parameters, return values, versions, compatibility claims, or migration steps.

## Workflow

1. Establish the documentation basis from the confirmed diff, code, configuration, API contracts, tests, and release scope.
2. Search references to changed names, commands, parameters, outputs, configuration keys, versions, deprecations, and examples.
3. Classify affected README, API docs, configuration guides, examples, migration guides, CHANGELOG entries, and release notes as update, verify-only, or not affected.
4. For every update, map the statement to repository evidence and preserve the surrounding document's language and style.
5. Synchronize commands, parameters, return values, compatibility, deprecation, migration sequence, and examples only when evidence confirms them.
6. Make the smallest documentation-only edits. Keep unrelated prose and formatting unchanged.
7. Run repository-provided documentation, link, formatting, or example checks when available. Do not invent missing check commands.
8. Check links, code fences, versions, terminology, and cross-document consistency manually when no tool exists.
9. Report updated files, evidence, validation, intentionally unchanged files, blockers, and documentation that may still be stale.

# Output Contract

1. Change basis and evidence
2. Updated documentation files
3. Content synchronized in each file
4. Files not updated and reasons
5. Implementation contradictions or blockers
6. Validation commands and results
7. Documentation that may still be stale

Separate confirmed documentation changes from assumptions. List only commands actually run.

# 简体中文

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 文档同步维护

根据已确认的实现、配置、API 或行为变更同步受影响文档。只修改文档。

## 职责边界

- 需要已确认实现证据、配置、规格或 diff；不得把计划行为写成已发布行为。
- 用户已指出单个命名文档中的 typo 时，可见文本和精确更正就是充分证据：只修改该文件，最多运行一个定向检查，不做更广的文档盘点并立即停止。
- 默认只修改文档和归属文档的示例，不改生产代码、测试、配置、依赖或行为。
- 发现实现错误或与已确认规格冲突时，报告阻塞项，不修改业务代码。
- 保留各文档原有语言、结构、术语、链接、格式和局部风格。
- 不重写无关章节，也不编造命令、参数、返回值、版本、兼容性或迁移步骤。

## 工作流程

1. 从已确认 diff、代码、配置、API 契约、测试和发布范围建立文档变更依据。
2. 搜索已变更名称、命令、参数、输出、配置键、版本、弃用和示例的引用。
3. 将受影响 README、API 文档、配置指南、示例、迁移指南、CHANGELOG 和发布说明分类为更新、仅验证或不受影响。
4. 每项更新都映射到仓库证据，并保持周边文档语言和风格。
5. 只有证据确认时才同步命令、参数、返回值、兼容性、弃用、迁移顺序和示例。
6. 做最小文档修改，保持无关文字和格式不变。
7. 存在仓库提供的文档、链接、格式或示例检查时运行；不得编造不存在的命令。
8. 没有工具时人工检查链接、代码围栏、版本、术语和跨文档一致性。
9. 报告更新文件、证据、验证、明确未修改文件、阻塞项和仍可能过期的文档。

# 输出契约

1. 变更依据与证据
2. 更新的文档文件
3. 各文件同步内容
4. 未更新文件及原因
5. 实现冲突或阻塞项
6. 验证命令与结果
7. 仍可能过期的文档

区分已确认文档变更和假设，只列出实际运行的命令。
