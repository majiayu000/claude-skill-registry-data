---
name: safe-code-review
description: "Review a concrete diff or PR through three independent axes: repository conformance, change-intent fidelity, and operational safety, then deduplicate evidence-backed findings. Use automatically for broad change review, not specialist-only security, performance, API, or migration assessment. Read-only: never implement fixes without a separate explicit request and write authorization. 通过仓库符合度、变更意图忠实度和运行安全三个独立轴审查具体 Diff 或 PR，再对有证据的问题去重。适合自动承接广泛变更审查，不吸收单一安全、性能、API 或迁移专项。本 Skill 只读；没有独立明确请求和写权限时绝不实施修复。"
---

# Safe Code Review（安全代码审查）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `fast`; bounded natural-language invocation is allowed.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Safe Code Review

Independent review axes prevent a clean result in one concern from hiding a failure in another.

Default output is `fast`; use `standard` or `audit` for detailed evidence, following the output contract.

## Boundary and Evidence

- Read repository instructions, the original request, relevant specification and acceptance criteria, diff, surrounding code, interfaces, and tests before judging.
- Do not modify files or implement fixes. Do not invent behavior, requirements, or passing validation.
- Prioritize correctness and material risk over style. Search references before recommending deletion and require compatibility evidence before public-interface changes.
- Use P0/P1/P2/P3. Every finding requires file, tight location, evidence, severity, impact, recommendation, and validation method.
- Do not create findings to fill a list. Record findings and evidence gaps per axis; show the breakdown in detailed output rather than guessing.

## Axis A: Repository Conformance

Evaluate only compliance with repository instructions, documented architecture constraints, naming, test conventions, relevant ADRs, and language/framework conventions. Distinguish documented violations from judgment calls. Do not use the requested feature as evidence on this axis.

## Axis B: Change Intent Fidelity

Evaluate only whether the change implements the original request, specification, and acceptance criteria. Check missing behavior, partial criteria, scope drift, unauthorized behavior, and implementation that looks reasonable but solves a different problem. If intent evidence is unavailable, mark this axis `insufficient evidence`; do not infer the requirement from the code.

## Axis C: Operational Safety

Evaluate only operational consequences: data migration and integrity, compatibility, authorization and security, rollback capability, runtime behavior, resource use, observability, release sequencing, and release blockers. Do not turn style or unmet product scope into an operational finding unless it independently creates runtime risk.

## Synthesis

1. Pin the reviewed diff or file set and record the evidence sources available to each axis.
2. Run all three axes separately, even without subagents. Do not pass conclusions, assumptions, or severity rankings from one axis into another.
3. Complete each axis independently, then report at the requested output depth.
4. Aggregate only after all axes finish. Merge duplicates by root problem while retaining every contributing axis and the strongest direct evidence.
5. Rank by user impact and likelihood. Do not inflate severity because multiple axes observed the same root problem.
6. Report commands/tests actually run, skipped validation, residual risks, and a bounded next action. Review-only authority never permits a fix.

# Output Contract

Default `fast`: conclusion, scope and evidence-backed P0/P1/P2 findings. Each finding includes severity, file/location, problem and impact, decisive evidence and an actionable recommendation without duplicate fields.
State no findings briefly; add material evidence gaps only when present. Omit empty risks, blockers and forced next steps.
`standard` adds the three axis results, validation advice and useful P3 findings.
`audit` adds sources, commands, skipped checks and permissions.
Complete all three checks; never invent findings or implement fixes.

---

## 执行契约

默认使用 `fast`；允许边界明确的自然语言隐式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 安全代码审查

独立审查轴可以防止一个维度的干净结论掩盖另一个维度的失败。

输出默认 `fast`；需要详细证据时使用 `standard` 或 `audit`，字段以输出契约为准。

## 边界与证据

- 判断前读取仓库指令、用户原始需求、相关规格与验收标准、diff、周边代码、接口和测试。
- 不修改文件或实施修复，不编造行为、需求或验证通过结果。
- 正确性和实质风险优先于风格；建议删除前搜索引用，建议修改公共接口前需要兼容性证据。
- 使用 P0/P1/P2/P3。每个问题都需要文件、精确位置、证据、严重度、影响、建议和验证方式。
- 不为了凑数输出问题。各轴记录发现和证据缺口，详细输出时再展示；不猜测。

## 轴 A：Repository Conformance（仓库符合度）

只检查仓库指令、已记录架构约束、命名、测试约定、相关 ADR，以及语言/框架惯例。区分文档明确违规与判断性建议；不得用功能需求作为本轴证据。

## 轴 B：Change Intent Fidelity（变更意图忠实度）

只检查改动是否实现用户原始需求、规格和验收条件；查找遗漏行为、不完整验收、范围漂移、未授权行为，以及“代码看似合理但解决了另一个问题”的实现。意图证据不可用时，本轴标为“证据不足（`insufficient evidence`）”，不得从代码反推需求。

## 轴 C：Operational Safety（运行安全）

只检查运行后果：数据迁移与完整性、兼容性、权限与安全、回滚能力、运行时行为、资源使用、可观察性、发布顺序和发布阻塞。风格问题或未满足产品范围只有在独立造成运行风险时才属于本轴。

## 汇总

1. 固定被审查的 Diff 或文件集合，并记录各轴可用的证据来源。
2. 即使平台没有子代理，也分别运行三个轴；一个轴的结论、假设和严重度不得污染另一个轴。
3. 独立完成各轴检查，再按输出模式报告结果。
4. 三轴完成后再聚合；按根问题合并重复项，同时保留所有贡献轴和最强直接证据。
5. 按用户影响和发生可能性排序；同一根问题被多轴发现不得自动抬高严重度。
6. 报告实际运行的命令/测试、跳过验证、剩余风险和有边界的下一动作。只审查权限永远不包含修复权限。

# 输出契约

默认 `fast`：整体结论、范围和有证据的 P0/P1/P2 问题。每项包含严重度、文件位置、问题及影响、关键证据和可操作建议，避免重复字段。
没有发现时简短说明；有实质证据缺口时才补充。不输出空风险、空阻塞或强制下一步。
`standard` 增加三个审查轴的结果、验证建议以及有价值的 P3 项。
`audit` 增加来源、命令、跳过检查与权限记录。
三轴检查仍须完成；不得编造问题或实施修复。
