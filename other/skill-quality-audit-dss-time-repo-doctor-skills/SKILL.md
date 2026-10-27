---
name: skill-quality-audit
description: "Perform a strictly read-only, pre-release quality audit of one AI Skill, a Pack, a plugin, or a Skills repository across structure, triggering, workflow, progressive resources, bilingual cross-platform output, safety, and publishing integration. Use when maintainers want findings, severity, evidence, and a release recommendation; do not audit ordinary application code or PRs, run a broad project health check, gate a product release candidate, or automatically fix files. 对一个 AI Skill、Pack、插件或 Skills 仓库执行严格只读的发布前质量审计，覆盖结构、触发、工作流、渐进资源、双语跨平台产物、安全和发布集成。维护者需要发现、严重度、证据和发布建议时使用；不用于普通应用代码或 PR 审查、广泛项目体检、产品候选版本门禁，也不自动修复文件。"
---

# Skill Quality Audit（Skill 质量审计）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

# Skill Quality Audit

Read `references/skill-maintenance-boundaries.md` and `references/audit-rubric.md`. Use `assets/skill-audit-report.md` for the report.

1. Define the audit object, release target, canonical source, generated outputs, intended platforms, neighboring Skills, and evidence available. Keep the workspace strictly read-only.
2. Inspect repository instructions, schemas, Pack/plugin/marketplace manifests, scaffold, validator, activation contracts, adapters, build scripts, and git status before judging the target.
3. Run only commands proven not to modify the workspace, such as the deterministic quality checker, validator, and tests. Do not run build/sync commands that rewrite outputs unless the user separately authorizes an isolated or generated-output check; otherwise mark reproducibility unverified.
4. Audit structure and format: folder/name consistency, frontmatter, required files, direct resource links, depth, orphaned files, line length, redundant documentation, UI metadata, and Pack/plugin references.
5. Audit triggering: explicit user invocation and automatic model activation, distinct realistic intents rather than synonym piles, what/when/not-when semantics, bilingual phrasing, breadth, adjacent routing, positive/negative/boundary/conflict/tool-unavailable cases, and gaps where no Skill owns the intent.
6. Audit workflow and output: executable order, inspectable completion criteria for every phase, premature-termination risk, evidence use, permissions, analysis/edit/validation/release separation, stopping conditions, failures, exits, unknowns, actual platform capability, and acceptance-ready output.
7. Audit progressive loading and authority: keep only all-branch procedure in instructions, branch-specific rules in first-level references, copied templates in assets, deterministic repeated logic in tested scripts, and reject multiple authorities, ineffective instructions, duplicated, stale, unreachable, or unbounded content.
8. Audit canonical uniqueness, adapter output, platform syntax leakage, English/Chinese behavior-permission-risk parity, output/schema/example/test agreement, generated coverage, and available repeat-build evidence.
9. Resolve every router reference against the active inventory and report missing or deprecated targets. Compare task state, inputs, outputs, permissions, and failure conditions to detect responsibility overlap with existing Skills.
10. Audit safety and publishing: credential/private-path/customer/restricted-content patterns, destructive or production actions, unauthorized publishing, manifest/version/CHANGELOG consistency, and public/private placement.
11. Report only evidence-backed findings. Assign P0/P1/P2 using the rubric; do not elevate style preferences. Include location, evidence, impact, recommendation, validation, unknowns, and one release recommendation. Do not edit files.

# Output Contract

1. Overall conclusion and audit scope
2. Scorecard by structure, explicit/automatic activation, workflow completion and exit, progressive resources and authority, cross-platform/bilingual parity, schema/example/test agreement, routing/overlap, and safety/release
3. P0 findings
4. P1 findings
5. P2 findings
6. Evidence locations, impact, repair recommendations, and validation suggestions
7. Unknowns and checks not performed
8. Release recommendation: READY, READY WITH CONDITIONS, or NOT READY

---

# Skill 质量审计

读取 `references/skill-maintenance-boundaries.md` 和 `references/audit-rubric.md`。使用 `assets/skill-audit-report.md` 输出报告。

1. 明确审计对象、发布目标、canonical 源、生成物、目标平台、相邻 Skill 和可用证据，保持工作区严格只读。
2. 判断目标前检查仓库指令、schemas、Pack/plugin/marketplace manifests、脚手架、验证器、activation 契约、adapters、构建脚本和 git 状态。
3. 只运行已证明不会修改工作区的命令，例如确定性质量检查、validator 和 tests。未经用户另行授权，不运行会重写产物的 build/sync；无法隔离验证时将可重复构建标为未验证。
4. 审计结构与格式：目录/name、frontmatter、必需文件、直接资源引用、层级、孤立文件、行数、冗余文档、UI 元数据和 Pack/plugin 引用。
5. 审计触发：用户主动调用与模型自动调用、不同真实意图而非同义词堆叠、做什么/何时/不何时语义、中英文真实说法、宽窄、相邻路由、正向/反向/边界/冲突/工具不可用用例，以及无人承接的意图。
6. 审计工作流与输出：可执行顺序、每阶段可检查完成条件、提前结束风险、证据、权限、分析/修改/验证/发布分离、停止条件、失败、退出、未知项、真实平台能力和可验收输出。
7. 审计渐进加载与权威来源：instructions 只保留所有分支都需要的流程，分支细则放一级 references，复制模板放 assets，重复确定性逻辑放有测试 scripts；拒绝多权威来源、无效、重复、过期、不可达或无边界内容。
8. 审计 canonical 唯一性、adapter 产物、平台语法泄漏、中英文行为/权限/风险一致、输出 Schema/示例/测试一致、生成覆盖和可用的重复构建证据。
9. 将 Router 的每个引用与 active 清单核对，报告不存在或已弃用目标；比较任务状态、输入、输出、权限和失败条件，识别与现有 Skill 的职责重叠。
10. 审计安全与发布：凭据、私有路径、客户或受限内容模式，破坏性/生产操作、未授权发布，以及 manifest、版本、CHANGELOG 和公开/私有归属一致性。
11. 只报告有证据的问题，按 rubric 使用 P0/P1/P2，不把风格偏好升为高风险；包含位置、证据、影响、建议、验证、未知项和一个发布建议，不修改文件。

# 输出契约

1. 总体结论与审计范围
2. 结构、主动/自动调用、工作流完成与退出、渐进资源与权威来源、跨平台/双语一致、Schema/示例/测试一致、路由/重叠、安全/发布评分卡
3. P0 发现
4. P1 发现
5. P2 发现
6. 证据位置、影响、修复建议和验证建议
7. 未知项与未执行检查
8. 发布建议：READY、READY WITH CONDITIONS 或 NOT READY
