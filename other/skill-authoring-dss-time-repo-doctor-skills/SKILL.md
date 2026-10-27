---
name: skill-authoring
description: "Engineer one new or updated AI Skill in this Skills repository from concrete use cases through canonical source, minimal resources, bilingual metadata, UI integration, activation contracts, validation, and cross-platform build inspection. Use when a maintainer explicitly wants a reusable Skill artifact, not for a one-off prompt, using an existing business Skill, empty plugin scaffolding, ordinary code changes, or silently creating multiple Skills. 在当前 Skills 仓库中，根据具体用例工程化创建或更新一个 AI Skill，覆盖 canonical 源、最少资源、双语元数据、UI 集成、activation 契约、验证和跨平台构建检查。维护者明确需要可复用 Skill 产物时使用；不用于一次性 Prompt、调用现有业务 Skill、只创建空插件、普通代码修改或未经确认批量创建多个 Skill。"
---

# Skill Authoring（Skill 工程化创建）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

# Skill Authoring

Read `references/skill-maintenance-boundaries.md` and `references/authoring-checklist.md`. Use `assets/skill-design-brief.md` to record the design before editing.

1. Inspect repository instructions, canonical packs, existing Skills, schemas, scaffolds, sync/build adapters, activation contracts, manifests, and the dirty worktree. Preserve user changes.
2. Derive two to five distinct realistic intents for positive requests, explicit-invocation and automatic-activation cases, negative requests, and adjacent Skills. Do not manufacture trigger coverage by piling synonyms. Ask only when a blocking choice would change scope, permissions, public/private placement, or the number of Skills.
3. Decide whether the repeated workflow deserves a Skill. Require meaningful reusable procedure, output contract, safety boundary, specialist reference, reusable template, or deterministic logic. Reject a simple one-off prompt.
4. Search globally for duplicate slug, ID, semantics, and triggers. Prefer extending an existing Skill when it owns the same intent. Do not broaden the request into several Skills without authorization.
5. Select the canonical Pack, plugin distribution, visibility, target platforms, permissions, and handoffs. Keep private or restricted implementation outside this public repository.
6. Plan the minimum files. Keep in canonical instructions only the procedure every branch needs; progressively load branch-only detail from first-level `references/`, use `assets/` for copied material, and add deterministic tested `scripts/` only when justified. Establish one authoritative source per rule. Never create empty resource directories or Skill-local README/CHANGELOG files.
7. Check filesystem, shell, and scaffold availability, then run the existing `npm run create:skill -- --pack ... --name ... --id ... --category ...` scaffold. If any required capability is unavailable, stop before writing, return the completed design brief and exact pending commands, and mark implementation and validation as not performed. Never claim files were generated. If the scaffold is missing or incomplete, enhance only the existing script within the user's authorization and add tests; never create a competing structure or overwrite an existing Skill.
8. Replace placeholders with bilingual metadata, imperative workflows, output contracts, examples, and tests. Put what/when/not-when semantics in descriptions; do not hard-code platform invocation syntax into canonical instructions. Give every phase inspectable completion criteria plus explicit failure and exit conditions; remove ineffective, duplicated, stale, or unbounded instructions.
9. Update Pack indexes, the relevant plugin sync configuration, UI metadata, manifests, marketplace only when required, activation cases, and repository documentation. Let adapters generate platform copies.
10. Apply the shared Repo Doctor Skill Quality Model: check premature completion, bilingual behavior/permission/risk parity, output/example/test consistency, overlap with existing owners, and router references to missing or deprecated Skills. Run the repository's deterministic quality checker, validation, activation tests, maintainer-tool tests, and build. Inspect every targeted output and repeat the build to verify stable hashes. Fix failures without hiding unknowns.
11. Report requirement understanding, suitability, triggers, counterexamples, resources, files, validation, and limitations. Do not commit, push, publish, or install unless explicitly authorized.

# Output Contract

1. Requirement understanding
2. Skill suitability decision and rationale
3. Explicit-invocation and automatic-activation intents, counterexamples, and adjacent Skills
4. Canonical placement, permissions, and resource plan
5. Implemented files and integrations
6. Validation and generated-output results
7. Phase completion, failure, exit, premature-termination, and single-authority review
8. Bilingual behavior/permission/risk and output/example/test parity
9. Router-reference and responsibility-overlap checks
10. Known limitations and unperformed release actions

---

# Skill 工程化创建

读取 `references/skill-maintenance-boundaries.md` 和 `references/authoring-checklist.md`。编辑前使用 `assets/skill-design-brief.md` 记录设计。

1. 检查仓库指令、canonical Packs、现有 Skills、schemas、脚手架、同步/构建适配器、activation 契约、manifests 和脏工作区，保护用户已有改动。
2. 推导 2–5 个覆盖不同真实意图的正向请求、用户主动调用与模型自动调用用例、明确反例和相邻 Skill；不得靠堆同义词制造 trigger 覆盖。只有会改变范围、权限、公开/私有归属或 Skill 数量的阻塞选择才询问。
3. 判断重复工作是否值得成为 Skill。至少应存在可复用流程、输出契约、安全边界、专业资料、模板或确定性逻辑；简单一次性 Prompt 应拒绝创建。
4. 全局搜索重复 slug、ID、语义和触发。意图相同时优先增强现有 Skill；未经授权不得扩展为多个 Skill。
5. 确定 canonical Pack、插件分发、可见性、目标平台、权限和转交关系；私有或受限实现不得进入本公开仓库。
6. 规划最少文件。canonical instructions 只保留所有分支都需要的流程，分支专用细节通过一级 `references/` 渐进加载；复制材料使用 `assets/`，只有确有需要才增加有测试的确定性 `scripts/`。每条规则只有一个权威来源。不得创建空资源目录或 Skill 内 README/CHANGELOG。
7. 先检查文件系统、shell 和脚手架能力，再运行现有 `npm run create:skill -- --pack ... --name ... --id ... --category ...`。如果所需能力不可用，必须在写入前停止，输出已完成的设计 brief 和待执行的准确命令，并明确“尚未实现、尚未验证”，不得声称已生成文件。若脚手架缺失或不完整，只能在用户授权范围内增强现有脚本并补测试，不得手建竞争结构或覆盖现有 Skill。
8. 用双语元数据、命令式流程、输出契约、示例和测试替换占位内容；description 写清做什么、何时触发、何时不触发；canonical 正文不写死平台调用语法。每个阶段需要可检查完成条件，并明确失败与退出条件；删除无效、重复、过期或无边界扩张的指令。
9. 更新 Pack 索引、相关插件同步配置、UI 元数据、必要 manifests/marketplace、activation cases 和仓库文档，由 adapters 生成平台副本。
10. 应用共享 Repo Doctor Skill 质量模型，检查提前结束、中英文行为/权限/风险一致、输出/示例/测试一致、与现有职责重叠，以及 Router 是否引用不存在或已弃用 Skill。运行确定性质量检查、validate、activation、维护工具测试和 build；抽查所有目标产物并重复构建比较哈希。修复失败，不隐藏未知项。
11. 报告需求理解、适合度、触发、反例、资源、文件、验证和限制。未经明确授权不 commit、push、发布或安装。

# 输出契约

1. 需求理解
2. 是否适合 Skill 及理由
3. 用户主动调用与模型自动调用意图、反例和相邻 Skill
4. canonical 归属、权限和资源规划
5. 实现文件与集成
6. 验证和生成物结果
7. 阶段完成、失败、退出、提前结束和单一权威来源检查
8. 中英文行为/权限/风险及输出/示例/测试一致性
9. Router 引用与职责重叠检查
10. 已知限制与未执行的发布操作
