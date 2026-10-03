---
name: briefbound-project-memory
description: Use when the user or project rules request project-local memory/dashboard initialization or updates, or an existing `.docs/project-memory/` or resolved external `activePaths.memory` root is needed for cross-session recovery, durable decisions, blockers, parallel coordination, or formal handoff; never auto-initialize or sync for ordinary development.
license: MIT
---

# Briefbound Project Memory

## 目标

按需维护 `.docs/project-memory/`（未迁移）或 `activePaths.memory` 解析的外部 memory root（已迁移）与 HTML 总览，为同项目 Agent 提供不入 Git 的 live coordination registry。memory 只存改变未来行动的事实；普通开发不自动初始化。

## Briefbound task contract

- Context Boundary: 目标仓库、现有 memory、live registry、项目规则、需持久化事实。
- Output Contract: READ/INIT/SYNC 结果、持久 delta、渲染/registry 验证和 Route Out。
- Allowed Action: 只操作 memory/dashboard 与协调工具；不改业务代码、不伪造 claim/进度/验证。
- Success Evidence: 来源可溯，delta 落正确 lane，索引/HTML/registry 一致、不覆盖并行改动。
- Stop Condition: 未被要求、事实源不明、ownership 冲突、脚本缺失、渲染失败或覆盖他人写入。
- Route Out: 原任务 owner、`briefbound-autonomous-collaboration-loop`、`briefbound-thread-coordination`、`briefbound-development-cleanup`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配回 `briefbound-router` 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文、保留技术字面量；只报产出、证据与风险；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 激活与模式

激活（任一）：用户/规则明确要求；memory 是恢复所需事实源；跨会话决定/blocker/handoff 需持久化；真实多 Agent 并行需 registry。

- `READ`：只读 `INDEX.md`、`profile.json` 与改变判断的 lane，不载全部历史。
- `INIT`：用户/规则要求且目录缺失时初始化。
- `SYNC`：只写 durable delta，不记对话或测试日志。

现有 `.docs/project-memory` 先读规则和索引；无目录且未触发 INIT 时返回原 owner。

## 已迁移仓库（外部 memory root）

已迁移仓库解析 `activePaths.memory` 得外部 memory 根，把 `--memory-root <根>` 传给 sync/render/capture/init 脚本；只读写根内文件，绝不写 `.docs/project-memory` 或根级 `PROJECT_MEMORY.html`；根缺失或未初始化（缺 memory.json/profile.json/lanes/）即失败，不创建目录。projects home 下存在 status=completed 的 `project-memory-migration.json` 时，resolver `resolve_and_lock_memory_dir()` 定位活跃根：无 `--memory-root` 的 legacy 写入会被拒。

示例：`sync_project_memory.py --memory-root <activePaths.memory> --lane <lane> --update "<delta>"`

legacy 模式仅限未迁移仓库：不传 `--memory-root`，行为向后兼容。`sync_project_memory.py` 另支持 `--summary-phase/--summary-focus/--summary-health` 更新全局 summary，及 `--resolve-issue <精确标题>`（可选 `--resolve-note`）解决 lane 内恰好一条未解决 issue；零或多条匹配拒绝写入。

Memory 不接管执行循环：自动闭环由 `briefbound-autonomous-collaboration-loop` 持有，memory 只作可恢复状态载体。只写已确认决定、跨会话 blocker、正式 handoff 或改变未来行动的验证结论；不为单个 task、测试或 checkpoint 重写渲染。

## 事实与结构

- 代码/Git/运行结果是事实源；memory 是恢复与决策投影，不能覆盖源事实。
- `lanes/*.json` 按职责存状态、决定、问题、next step；`memory.json` 只存全局事实。
- `INDEX.md`/`overview.html` 是投影，不是 claim 或运行状态权威。
- 绝对 worktree、thread id、secret、敏感日志不入 tracked dashboard。

首次初始化才读 `references/setup.md` 并跑 `init_project_memory.py`；已有结构用 sync/capture/render，参数以 `--help` 为准；capture 只存待查的高价值线索。

## 并行协作

真实并行或 registry 已存在时用 `agent_coordination.py <project-root> status/join/update/claim/open/respond/resolve/pause/resume/complete`。

live registry 位于 `<git-common-dir>/briefbound/coordination/registry.json`；非 Git 项目回退 `~/.codex/project-coordination/<project-id>/registry.json`。跨 worktree 共享、不入 Git，用文件锁、revision、原子替换。

只 claim 最小 scope。pause 让出 claim，resolve 形成 `resumePendingAgentIds`；owner 失活由 `takeover` 接管，恢复重查重叠，取消/归档须 `cancel-resume --confirmed-by-user`。目标已 stale 且有 fresh list/read 证据时，`expire-resume --evidence <fact>` 只清本地债务并释放 yielded claim，不标对方任务完成。open coordination 或恢复债务阻止 complete。`agent_work_guard.py` 仅为兼容入口。

并行 worker 不直接同步 tracked memory；coordinator 在决定解决后用 `--lane <lane> --coordination-id <id>` 写一次。

## 验证

写入后确认：delta 落正确 lane；`INDEX.md` 计数/链接一致；HTML 可打开且脱敏；不覆盖无关 lane 与并行改动。结构/渲染异常才读 `references/troubleshooting.md`，视觉调整才读 `references/html-design.md`。

事实或工具不足即 BLOCKED，不手改 JSON/HTML 伪造状态。
