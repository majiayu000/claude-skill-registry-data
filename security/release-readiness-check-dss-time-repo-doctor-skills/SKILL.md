---
name: release-readiness-check
description: "Explicit-invocation, evidence-backed, read-only release gate for a specific candidate version, returning GO, GO WITH CONDITIONS, or NO-GO after full release checks. Do not trigger for ordinary validation or project health, and never execute release, commit, tag, push, or version changes. 仅显式调用：针对具体候选版本执行有证据的只读发布门禁，完成发布检查后给出 GO、GO WITH CONDITIONS 或 NO-GO。不得因普通验证或项目体检而触发，也不执行发布、提交、tag、push 或版本修改。"
---

# English

## Execution Contract

Default to `standard`; explicit invocation is required.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Release Readiness Check

Evaluate a specific release candidate and return an evidence-backed `GO`, `GO WITH CONDITIONS`, or `NO-GO`. Keep the check read-only.
When the request explicitly names local gates to run, resolve their repository commands from the nearest manifest, preflight and execute that finite gate list before broader audit work, capture every status, and then continue the read-only assessment.
If the request says to run the full local test, typecheck, or build gates, executing the corresponding full package-manager scripts is mandatory. Before execution, inspect the scripts, package-manager lifecycle hooks and transitively invoked commands for side effects. Run the full requested scripts only after confirming they stay within the authorized local validation scope; reading a script, running a narrower command, or predicting its result never satisfies the gate. If a command includes deployment, publishing, migration, unsafe deletion, production access, or unknown side effects, mark that gate `Blocked` and explain the boundary; continue independent safe gates. Do not silently replace or edit the blocked script.

## Boundary

- Cleanup is allowed only for disposable artifacts created by this run in an isolated temporary directory, with ownership and resolved paths verified and no symlink escape. Preserve pre-existing files, user data and unknown paths; otherwise block cleanup. This exception does not authorize general deletion.

- Require a release object such as a version, branch, commit, tag candidate, build artifact, or explicit change range. Route broad repository diagnosis to `project-health-check`.
- Do not publish, deploy, commit, tag, push, change versions, edit files, or approve despite unresolved blockers.
- Shell permission covers only user-authorized, preflighted repository-local validation and its disposable outputs. Source/configuration edits, network access, arbitrary commands and release actions remain forbidden.
- Use only repository-provided validation commands and actual results. Mark checks not run and explain why.
- When the user authorizes a finite list of independent local gates, run every listed gate even if an earlier gate fails; stop only when a later gate depends on the failed one or would be unsafe.
- Do not expose credential values or private data when scanning evidence.
- A checklist without reproducible evidence is insufficient.

## Workflow

1. Define the release object, target environment, change range, included artifacts, and comparison baseline.
2. Inspect workspace status, version consistency, change scope, dependency lockfiles, generated outputs, and untracked or temporary files.
3. Identify repository-provided test, build, lint, typecheck, schema, package, and release verification commands. Execute every gate the user explicitly requested and authorized; inspecting its script is not a substitute. Record actual results or `not run`.
4. Check API, database, configuration, permission, runtime, and platform compatibility; migration ordering; rollback feasibility; and forward/backward compatibility where applicable.
5. Check documentation, CHANGELOG, release notes, deprecations, migration guidance, and operator/user communication against the actual change.
6. Scan for credential-like material, private data, debug code, disabled checks, temporary files, absolute machine paths, and unexpected generated artifacts without revealing sensitive values.
7. Classify findings as blockers, pre-release conditions, recommendations, or post-release observations. Attach evidence and an owner/action when available.
8. Evaluate rollback readiness, observability, monitoring signals, and stop or rollback thresholds.
9. Return exactly one decision: `GO`, `GO WITH CONDITIONS`, or `NO-GO`, with conditions and next steps tied to evidence.

# Output Contract

1. Release object and baseline
2. Check scope and evidence sources
3. Passed checks with commands or file evidence
4. Blocking items
5. Conditional items and pre-release actions
6. Risks and post-release observations
7. Rollback readiness and thresholds
8. Final decision: GO, GO WITH CONDITIONS, or NO-GO
9. Next steps

List unrun checks explicitly. Do not perform release actions.

# 简体中文

## 执行契约

默认使用 `standard`；仅允许用户显式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# 发布就绪检查

评估具体候选版本，并给出有证据的 `GO`、`GO WITH CONDITIONS` 或 `NO-GO`。保持只读。
请求明确列出要运行的本地门禁时，先从最近的清单解析仓库命令，在扩展审计前预检并执行这组有限门禁并记录每项状态，然后继续只读评估。
请求要求运行完整本地测试、类型检查或构建门禁时，必须执行清单中对应的完整包管理器脚本。执行前检查脚本实现、包管理器生命周期钩子及间接调用命令的副作用。确认属于已授权的本地验证范围后，完整执行所要求的脚本；只读取脚本、运行更窄命令或推测结果都不算完成门禁。命令包含部署、发布、迁移、不安全删除、生产访问或未知副作用时，将该门禁标为 `Blocked` 并说明边界，继续其他独立且安全的门禁。不得静默替换或修改被阻塞的脚本。

## 职责边界

- 仅允许清理本次运行在隔离临时目录创建、归属和解析后路径均已核验且不存在符号链接越界的可丢弃产物。保留已有文件、用户数据和不明路径；无法确认时阻塞清理。本例外不授权一般删除。

- 需要版本、分支、commit、候选 tag、构建产物或明确变更范围等发布对象；广泛仓库诊断交给 `project-health-check`。
- 不发布、不部署、不提交、不打 tag、不 push、不修改版本或文件，也不得在阻塞项未解决时批准发布。
- Shell 权限仅用于用户已授权、经预检的仓库本地验证及其可丢弃生成物；仍禁止修改源文件/配置、联网、任意命令和发布动作。
- 只使用仓库提供的验证命令和真实结果；未运行项必须标明并解释原因。
- 用户明确授权一组有限且相互独立的本地门禁时，即使前一项失败，也要执行全部列明门禁；只有后续门禁依赖失败项或继续执行不安全时才停止。
- 扫描证据时不得暴露密钥或私有数据。
- 没有可复现证据的笼统 checklist 不足以支持结论。

## 工作流程

1. 明确发布对象、目标环境、变更范围、包含产物和比较基线。
2. 检查工作区状态、版本一致性、变更范围、依赖锁文件、生成物、未跟踪或临时文件。
3. 识别仓库提供的测试、构建、lint、typecheck、schema、打包和发布验证命令；执行用户明确要求并授权的每一项门禁，读取脚本不能替代执行；记录真实结果或“未运行”。
4. 检查 API、数据库、配置、权限、运行时和平台兼容性，以及迁移顺序、回滚可行性和适用的前后向兼容。
5. 根据实际变更检查文档、CHANGELOG、发布说明、弃用、迁移指南和用户/运维通知。
6. 扫描疑似密钥、私有数据、调试代码、禁用检查、临时文件、机器绝对路径和异常生成物，但不展示敏感值。
7. 将发现分类为阻塞项、发布前条件、建议或发布后观察项；附证据及可用的负责人/动作。
8. 评估回滚准备、可观察性、监控信号以及停止或回滚阈值。
9. 只给一个结论：`GO`、`GO WITH CONDITIONS` 或 `NO-GO`，条件和下一步必须关联证据。

# 输出契约

1. 发布对象与基线
2. 检查范围与证据来源
3. 通过项及命令或文件证据
4. 阻塞项
5. 条件项与发布前动作
6. 风险与发布后观察项
7. 回滚准备与阈值
8. 最终结论：GO、GO WITH CONDITIONS 或 NO-GO
9. 下一步

明确列出未运行检查，不执行发布动作。
