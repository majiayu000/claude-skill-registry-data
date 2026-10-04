---
name: cc-status
description: 结构化 Codex 配置与任务状态检查工作流，适用于显式 status、配置诊断、同步结果核对或任务盘点场景；聚焦 Codex 配置与项目内 .codex 任务状态。
---

# CC Status

当用户明确要求 status、查看 Codex 配置状态，或排查 sync 后的生效情况时，使用本技能。

不要用于：

- Claude 或 Gemini 的状态诊断
- 正式 code review
- 变更项目代码实现

## 核心方式

1. 同时看项目内 `.codex/` 权威源和用户级 `~/.codex/`、`~/.agents/skills/` 部署产物。
2. 检查全局入口是否齐全：`AGENTS.md`、`rules/`、`instructions/`、`skills/`、`*.config.toml` profiles。
3. 检查 `AGENTS.md` 是否包含受管区块，`rules/`、`instructions/`、`skills/` 与 profiles 是否保留 manifest。
4. 检查 `codex` CLI 是否可用，并报告版本。
5. 若 `codex execpolicy check` 可用，抽样验证当前 rules 的 `allow/prompt/forbidden` 是否符合预期。
6. 补查当前项目是否具备 `new-feature` 任务持久化前置条件：项目内 `.codex/tasks/`、`.codex/tasks/archived/`、`.codex/templates/` 是否存在。
7. 补查 `.codex/tasks/` 根目录中的活动任务：当前主任务、候选任务、被打断点、最近更新时间，以及是否出现多个任务同时标成 `进行中` 的冲突。
8. 补查当前项目根目录 `AGENTS.md` 是否存在、是否包含 `AUTO:*` 自动区块，以及项目级上下文是否明显缺失。
9. 如果项目内与用户级数量不一致，优先判断是不是还没执行同步脚本。
10. 若项目内骨架齐全但仍无法持久化任务，优先判断是不是当前 Codex 会话的 sandbox / workspace scope 只覆盖了受限目录，而不是项目根目录本身可写。
11. 输出状态、缺口和下一步，不做泛泛而谈的环境描述。

## 输出要求

- 明确区分“项目权威源”和“用户级生效配置”
- 明确区分“文件已同步”与“规则已生效”
- 明确区分“配置状态”与“任务状态”
- 报告缺失项、数量差异、受管区块异常和明显异常
- 若当前项目缺少 `.codex/tasks/` 或 `.codex/templates/`，明确提示这会影响 `new-feature` 持久化，并建议先执行 `$project-init` 或 `$project-scan`
- 若当前项目缺少根目录 `AGENTS.md`，或 `AGENTS.md` 明显缺少项目全貌/自动区块，明确建议执行 `$project-scan`
- 若存在活动任务，报告当前主线、候选任务、阻塞或打断状态，以及建议先恢复哪一项
- 若发现多个任务同时处于 `进行中`，明确指出这是状态冲突，建议先用 `cc-task-state` 收敛
- 若检测不到问题，要直接说明状态正常
- 若怀疑未同步，明确建议执行 `tools/sync-config.sh`
- 若骨架已齐全但任务写入仍失败，必须明确区分“项目根目录确实不可写”和“当前会话仍在受限 sandbox / workspace scope 中执行”

## 按需展开

- 检查项：`references/status-checks.md`
