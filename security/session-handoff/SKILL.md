---
name: session-handoff
description: "Explicit-invocation Skill that creates a sanitized continuation brief tailored to the next-session goal, referencing specifications, ADRs, issues, commits, and diffs instead of copying them. Save to an operating-system temporary directory by default; project-directory writes require authorization. Never modify business files, Git state, or external systems. 仅显式调用：创建面向下一会话目标的脱敏续接摘要，通过路径、ADR、Issue、Commit 和 Diff 引用既有产物而不重复全文。默认保存到操作系统临时目录；写入项目目录必须授权。绝不修改业务文件、Git 状态或外部系统。"
---

# Session Handoff（会话交接）

Use the section matching the user's language. 使用与用户输入语言一致的章节。

## Execution Contract

Default to `standard`; explicit invocation is required.
Complete one primary task by default. Continue an authorized end-to-end workflow within each Skill's permissions; Router remains recommendation-only. Pause for new material decisions or scope, not authorization already given.
For a human-only blocker, give location, action, success signal and resume step; never request secret values or assume completion.
Validate according to actual risk; security, production, migrations, releases and other high-risk work use `audit`. Read `references/execution-modes.en.md` only when mode selection is unclear.

# Session Handoff

A good handoff transfers verified state and the smallest next action, not the conversation's bulk.

## Output modes

- `fast`: current goal, status, confirmed facts, blockers, critical paths, next Skill, and one copyable start instruction.
- `standard` (default): the complete continuation brief described below.
- `audit`: `standard` plus source provenance, command/exit ledger, sanitization categories, permission decisions, and evidence gaps.

Tailor every mode to a user-provided next-session goal. If none is provided, optimize for resuming the current unfinished objective.

## Boundary

- Stay read-only by default. Do not modify business code, tests, configuration, documentation, Git state, commits, branches, external tasks, or releases.
- Do not claim the next session will automatically discover or read the brief.
- Reference long specifications, ADRs, work-item plans, diffs, logs, and documentation by path or identifier rather than copying them.
- Redact authentication material, password values, identity numbers, private addresses, and other sensitive personal or customer data. Preserve only the minimum non-sensitive context needed to continue.
- Automatically remove credentials, passwords, private keys, connection strings, identifying personal values, and other sensitive values. Use non-reversible category markers such as `[REDACTED_CREDENTIAL]`.
- Save the brief to a unique file in the operating system temporary directory by default. Confirm the path is outside the project and do not overwrite an existing file. Writing inside the repository or another user directory requires explicit path-scoped authorization.
- Also summarize the saved path and key next action in the response. If no safe temporary location is writable, return the complete brief in the response and mark file creation `Blocked`.

## Workflow

1. Determine the next-session goal and current objective. Reconstruct original intent from the conversation and repository artifacts; mark unavailable source context `Unverified`.
2. Separate current status, confirmed facts, explicit decisions, unverified information, reasonable inferences, unresolved questions, risks, and blockers.
3. Record completed changes, unfinished tasks, current repository state, key files, actual commands, exit results, tests, and validation. Never claim a command ran when it did not.
4. Reference existing specifications, ADRs, issues, commits, diffs, logs, and documentation by path, identifier, commit, issue, or URL. Do not duplicate their full content.
5. Identify permission constraints, generated files, user-owned changes, conflict zones, and actions that must not be repeated.
6. Order the next steps for the stated next-session goal. Recommend the narrowest existing Repo Doctor Skill and state the minimum required input and stop condition.
7. Sanitize the entire brief before saving. Report categories removed, never original values.
8. Save to a unique OS temporary path by default, then provide that path and a minimum copyable start instruction that tells the new session to read the brief and verify current state.

## Completion and Failure Conditions

Complete when the brief is sufficient to choose and verify the next action without repeating completed work. Mark unavailable repository state, command results, or intent `Unverified`. Return `Blocked` only for required missing context, an unsafe target path, or unavailable temporary storage; never fall back to the project directory without authorization.

# Output Contract

Lead with `status`, next-session goal, saved path, and recommended first action.

- `fast`: current goal/status, confirmed facts, blockers, key files, next Skill, and minimum start instruction.
- `standard`: current goal, original intent, confirmed facts, unverified information, decisions, completed changes, unfinished tasks, repository state, risks/blockers, key files, artifact references, validation commands/results, next steps, recommended Skill, minimum start instruction, sanitization summary, and file-write status.
- `audit`: add source provenance, exact command/working-directory/exit ledger, permission decisions, evidence gaps, and redaction categories.

Use references for specifications, ADRs, issues, commits, and diffs. Do not include raw sensitive values, repeat long artifacts, or claim automatic discovery.

---

## 执行契约

默认使用 `standard`；仅允许用户显式调用。
默认完成一个主任务。用户已授权完整流程时，在各 Skill 权限内连续完成；Router 仍只推荐。新重大决策或超出授权时暂停，不重复索取已有授权。
必须由用户完成的阻塞步骤：给出操作位置、具体动作、成功标志、恢复步骤；不要求粘贴秘密值，不代替用户确认完成。
按实际风险选择验证；安全、生产、迁移、发布等高风险工作使用 `audit`。模式不明确时才读取 `references/execution-modes.zh-CN.md`。

# Session Handoff（会话交接）

好的交接传递已验证状态和最小下一动作，而不是搬运整段对话。

## 输出模式

- `fast`：当前目标、状态、已确认事实、阻塞、关键路径、下一 Skill 和一条可复制启动指令。
- `standard`（默认）：输出下述完整续接摘要。
- `audit`：在 `standard` 基础上增加来源追踪、命令/退出账本、脱敏类别、权限判断和证据缺口。

所有模式都应围绕用户提供的下一会话目标调整重点；未提供时，以继续当前未完成目标为准。

## 职责边界

- 默认只读，不修改业务代码、测试、配置、文档、Git 状态、commit、分支、外部任务或发布。
- 不声称下一会话会自动发现或读取交接内容。
- 已存在的长规格、ADR、工作项、diff、日志和文档只引用路径或标识，不重复全文。
- 清理认证材料、密码值、身份证号、私人地址和其他敏感个人或客户数据，只保留继续任务所需的最少非敏感上下文。
- 自动移除访问凭据、密码、私钥、连接串、可识别个人值和其他敏感原值，使用 `[REDACTED_CREDENTIAL]` 等不可逆类别标记。
- 默认保存为操作系统临时目录中的唯一文件；确认路径位于项目外且不覆盖已有文件。写入仓库或其他用户目录必须获得精确到路径的明确授权。
- 在响应中同时给出保存路径和关键下一动作。没有可写安全临时目录时，在响应中输出完整交接，并把文件创建标为 `Blocked`。

## 工作流程

1. 确认下一会话目标和当前目标；从对话与仓库产物重建用户原始意图，无法取得的来源上下文标为 `Unverified`。
2. 区分当前状态、已确认事实、明确决策、未验证信息、合理推断、未决问题、风险和阻塞。
3. 记录已完成修改、未完成任务、当前仓库状态、关键文件、实际命令、退出结果、测试和验证；未运行的命令不得声称已运行。
4. 通过路径、标识、commit、issue 或 URL 引用相关规格、ADR、Issue、Commit、Diff、日志和文档，不复制全文。
5. 标识权限限制、生成文件、用户已有改动、冲突区域和不应重复执行的动作。
6. 围绕下一会话目标排列后续步骤，推荐职责最窄的现有 Repo Doctor Skill，并说明最小输入和停止条件。
7. 保存前对完整摘要脱敏；只报告被移除的类别，不报告原值。
8. 默认保存到唯一系统临时路径，再给出该路径和最小可复制启动指令，要求新会话先读摘要并核对当前状态。

## 完成与失败条件

摘要足以让下一会话不重复已完成工作并选择、验证下一动作时完成。仓库状态、命令结果或原始意图无法核实时标为 `Unverified`。只有必要上下文缺失、目标路径不安全或系统临时存储不可用时返回 `Blocked`；不得在未授权时改写到项目目录。

# 输出契约

先给 `status`、下一会话目标、保存路径和推荐第一动作。

- `fast`：当前目标/状态、已确认事实、阻塞、关键文件、下一 Skill 和最小启动指令。
- `standard`：当前目标、原始意图、已确认事实、未验证信息、决策、已完成修改、未完成任务、仓库状态、风险/阻塞、关键文件、产物引用、验证命令/结果、下一步、推荐 Skill、最小启动指令、脱敏摘要和文件写入状态。
- `audit`：增加来源追踪、准确命令/工作目录/退出码账本、权限判断、证据缺口和脱敏类别。

规格、ADR、Issue、Commit 和 Diff 使用引用。不得包含敏感原值、复制长产物或声称下一会话会自动发现交接内容。
