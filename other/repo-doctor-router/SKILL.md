---
name: repo-doctor-router
description: "Explicit routing entrypoint that recommends one verified Repo Doctor Skill and fast, standard, or audit mode from the current repository state, or returns a registered workflow when detailed routing is requested. Use only when the user explicitly invokes the Router or asks for Repo Doctor routing. Do not execute the recommendation, route ordinary factual questions, invent aliases, or bypass permission gates. 显式路由入口：根据当前仓库状态推荐一个已核验 Repo Doctor Skill 及 fast、standard 或 audit 模式；用户要求详细路由时再返回注册工作流。仅在用户显式调用 Router 或明确要求 Repo Doctor 路由时使用。不得执行推荐、路由普通知识问答、编造别名或绕过权限门禁。"
---

# Repo Doctor Router（工作流路由）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `fast`; explicit invocation is required.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Repo Doctor Router

The best route is the smallest verified next capability that matches the current artifact and permission state.

Default to one `fast` recommendation; expand to `standard` or `audit` only for requested routing detail. Fields belong to the output contract.

Use [execution modes](references/execution-modes.en.md) when detailed mode selection is needed.

## Boundary

- Stay read-only. Do not edit files, run commands, access the network, or perform release actions.
- Read `references/workflows.yaml` relative to this Skill document. In a distribution this is a bundled read-only projection of the unique canonical registry; no source-repository checkout is required. Do not invent or silently extend workflows.
- Do not claim the host recursively invokes Skills. A recommendation is guidance for the user or a later turn.
- Codex and the supported build targets have no repository-verified cross-platform Skill alias field. Do not emit alias frontmatter, duplicate a Skill, or claim `$doctor` exists. Use the stable canonical Skill name.
- Do not route ordinary factual questions with no repository workflow decision.
- Recommend only active verified Skill IDs. Mark unavailable inventory or registry evidence `unverified` and provide a bounded natural-language fallback.
- Never collapse clarification, specification, planning, permission gates, implementation, verification, and release.

## Routing Workflow

1. Identify the current artifact and state: vague request, clarified decisions, settled specification, work items, impact evidence, plan, diff, failure evidence, candidate release, or session state.
2. Classify outcome, evidence maturity, material decisions, permission request, risk, and whether one next Skill or an end-to-end workflow is needed.
3. Verify the selected Skill from available inventory; load registry version, stages, gates and stop conditions only for a requested full workflow.
4. Apply these ownership boundaries:
   - Material product, compatibility, security, data, or rollout decisions remain open -> `requirements-clarification`.
   - Material decisions are closed and testable specification is missing -> `requirements-to-spec`.
   - A settled large specification needs vertical delivery slices -> `spec-to-work-items`.
   - Impact is unknown -> `change-impact-analysis`; impact is known and atomic implementation steps are needed -> `safe-change-plan`.
   - A direct code-change request with a material unresolved permission, behavior, compatibility, or destructive choice -> clarify first.
   - A clear, scoped direct code-change request with explicit write authority -> recommend the matching registered workflow gate and implementation owner below; never treat clarity as permission.
   - Settled new-feature specification/work items with write authority -> `feature-implementation`; a diagnosed local defect remains `safe-fix-implementation`.
   - Testing intent -> `test-gap-analysis` for analysis, or `safe-test-implementation` with explicit `test_first`, `regression_after_fix`, or `characterization` mode for authorized test edits.
   - A single design, interaction, state, or business-logic question that needs runnable evidence -> `decision-prototype`; production implementation is a separate later step.
   - Broad diff review -> `safe-code-review`; pre-change blast-radius analysis -> `change-impact-analysis`.
   - CI-specific failure -> `ci-failure-diagnosis`; complex non-CI runtime failure -> `bug-root-cause-analysis`.
   - Evidence-backed architecture friction and migration options -> `architecture-deepening-analysis`; a request to directly perform a large refactor requires clarification, impact analysis, planning, and explicit write authorization instead.
   - Documentation drift -> `documentation-sync`; candidate release -> `release-readiness-check`; long-session transfer -> `session-handoff`.
   - Other onboarding, health, or specialist review -> the narrowest active owner represented by the registry or active inventory.
5. If a registered workflow fits, return its exact `workflow_id` and ordered applicable stages. Preserve approval gates, forbidden transitions, alternatives, and stop conditions. Do not create a bespoke duplicate.
6. If no workflow fits, recommend one verified Skill and say why registry routing is not applicable.
7. Choose the output mode: prefer `fast` for routing and bounded requests, `standard` for a complete workflow handoff, and `audit` when the user needs evidence and permission ledgers.
8. Return the recommendation using the output contract. Invocation syntax is an adapter example, not canonical workflow data.

## Completion

Return one verified recommendation and never execute it. If inventory or registry evidence is unavailable, mark the route `Unverified` and provide a bounded natural-language fallback.

# Output Contract

Default `fast` output:

```text
Recommend: $<skill-name>
Reason: <one sentence>
Mode: fast | standard | audit
Needs: <minimum input>
Try: <copyable invocation preserving the user’s problem and scope>
```

Keep `fast` to these fields. Give one host-supported invocation or natural-language request, preserving scope and permissions; use placeholders for missing inputs.

For `standard` or requested detail, add classification, workflow ID, current stage, prerequisites, permission gate, stop condition, next Skill, and one alternative. For `audit`, add registry/version verification, active-inventory evidence, rejected candidates, platform alias capability, and unresolved uncertainty.

---

## 执行契约

默认使用 `fast`；仅允许用户显式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# Repo Doctor Router（工作流路由）

最佳路由是与当前产物和权限状态匹配的最小已核验下一能力。

默认 `fast` 推荐一个 Skill；`standard` 或 `audit` 仅在要求详细路由时展开。输出字段以输出契约为准。

需要详细选择模式时，参阅[执行模式](references/execution-modes.zh-CN.md)。

## 职责边界

- 保持只读，不修改文件、不运行命令、不联网，也不执行发布动作。
- 相对于本 Skill 文档读取 `references/workflows.yaml`。分发包内附带唯一 canonical 注册表的只读投影，无需克隆源仓库。不得编造或静默扩展工作流。
- 不声称宿主会递归调用 Skill。推荐只是给用户或后续轮次的指引。
- Codex 与本仓库支持目标没有经仓库核验的跨平台 Skill alias 字段。不得输出 alias frontmatter、复制 Skill 或声称 `$doctor` 已存在；始终使用稳定 canonical Skill 名。
- 普通知识问答不涉及仓库工作流决策时不要路由。
- 只推荐已核验为 active 的 Skill；清单或注册表无法核实时标为 `unverified`，并给出边界明确的自然语言后备指令。
- 不把澄清、规格、计划、权限门禁、实施、验证和发布合并成一个动作。

## 路由流程

1. 识别当前产物和状态：模糊需求、已澄清决策、已闭合规格、工作项、影响证据、计划、diff、失败证据、候选版本或会话状态。
2. 按目标、证据成熟度、重大决策、权限请求、风险，以及需要单一步骤还是端到端工作流进行分类。
3. 从可用清单核验推荐 Skill；只有请求完整工作流时才读取注册表版本、阶段、门禁和停止条件。
4. 应用职责边界：
   - 产品、兼容性、安全、数据或发布方式仍有重大未决选择 -> `requirements-clarification`。
   - 重大决策已闭合但缺少可测试规格 -> `requirements-to-spec`。
   - 大型已闭合规格需要垂直交付切片 -> `spec-to-work-items`。
   - 影响未知 -> `change-impact-analysis`；影响已知且需要原子实施步骤 -> `safe-change-plan`。
   - 直接改代码请求仍有重大权限、行为、兼容性或破坏性选择 -> 先澄清。
   - 范围明确且有显式写授权的直接改代码请求 -> 推荐匹配的注册工作流门禁和下述实施承接者；清晰不等于授权。
   - 已确认新功能规格/工作项且已有写授权 -> `feature-implementation`；已诊断局部缺陷仍交给 `safe-fix-implementation`。
   - 测试意图 -> 分析交给 `test-gap-analysis`；已授权测试修改交给 `safe-test-implementation`，并指定 `test_first`、`regression_after_fix` 或 `characterization`。
   - 单一设计、交互、状态或业务逻辑问题需要可运行证据 -> `decision-prototype`；生产实施属于后续独立步骤。
   - 广泛 diff 审查 -> `safe-code-review`；修改前影响范围分析 -> `change-impact-analysis`。
   - CI 特有失败 -> `ci-failure-diagnosis`；复杂非 CI 运行故障 -> `bug-root-cause-analysis`。
   - 有证据的架构摩擦与迁移方案 -> `architecture-deepening-analysis`；要求直接进行大规模重构时，应先澄清、影响分析、计划和明确写授权。
   - 文档漂移 -> `documentation-sync`；候选版本 -> `release-readiness-check`；长会话交接 -> `session-handoff`。
   - 其他上手、体检或专项审查 -> 选择注册表或 active 清单中职责最窄的承接者。
5. 若注册工作流匹配，返回准确 `workflow_id` 和适用阶段顺序；保留审批门禁、禁止跃迁、替代路径和停止条件，不另造重复流程。
6. 若没有工作流匹配，只推荐一个已核验 Skill，并说明为何不适用注册工作流。
7. 选择输出模式：路由和有边界请求优先 `fast`，完整工作流交接使用 `standard`，需要证据与权限账本时使用 `audit`。
8. 按输出契约返回推荐。调用语法属于 adapter 示例，不是 canonical 工作流数据。

## 完成条件

只返回一个已核验推荐，绝不执行。清单或注册表无法核实时，将路由标为 `Unverified` 并给出边界明确的自然语言后备指令。

# 输出契约

默认 `fast` 输出：

```text
推荐：$<skill-name>
原因：<一句话>
模式：fast | standard | audit
需要：<最小输入>
下一步：<保留用户问题和范围的可复制调用>
```

`fast` 只输出上述字段。给一个宿主支持的调用或自然语言请求，保留范围和权限；缺失输入用占位符。

`standard` 或用户要求详细信息时，增加分类、workflow ID、当前阶段、前置条件、权限门禁、停止条件、后续 Skill 和一个替代路径。`audit` 再增加注册表/版本核验、active 清单证据、被拒绝候选、平台 alias 能力和未解决不确定性。
