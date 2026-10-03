---
name: briefbound-thread-coordination
description: "Use when existing independent Codex App threads in one project need peer advice, target/ACK validation, file or runtime-process ownership and shared data-root arbitration, conflict recovery, discussion, merge coordination, status exchange, or native-thread handoff without creating subagents."
license: MIT
---

# Briefbound Thread Coordination

## 目标

registry/thread 处理冲突、合并；Git 为准。

## Briefbound task contract

- Context Boundary: 项目/thread/branch/worktree/scope/claim 及共享 runtime 归属。
- Output Contract: ownership、决定、验证、恢复债务。
- Allowed Action: 用 `list_threads`、`read_thread`、`wait_threads`、只读进程/Git 探针；只有 `BRT_TRUSTED_RELAY_V1` validator 返回 `TRUSTED_RELAY_AUTHORIZED` 时才调用 `send_message_to_thread`。不停止未知 owner，创建/归档/远程 Git 另授权。缺原语则不进入（见 harness 矩阵）。
- Success Evidence: registry、thread 回执、Git/测试和闭环。
- Stop Condition: thread 不明、owner 争议、未确认暂停/未授权。
- Route Out: 原 owner、`briefbound-autonomous-collaboration-loop`、`briefbound-multi-agent-orchestration`、`briefbound-pr-review`、`briefbound-development-cleanup`、`briefbound-project-memory`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract；不匹配时回具体 owner。
- 用户可见内容默认中文；只报产出、证据和风险；Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 接入与所有权

`preflight` 传 `--write-kind development|mechanical|integration`：根 `main/master` 开发为 `ISOLATION_REQUIRED`，集成需 claim+clean；其余按 `CLEAR/PEERS_NO_OVERLAP` 或 `OVERLAP` 判定，只 claim 最小 scope。

owner 顺序：用户指定 > 有效 claim/registry > 更早 owner。非 owner 停止自身冲突写入，不要求既有 owner 暂停；争议面只读。

文件/集成 owner 分开。`MERGE_READY` 时读 `references/integration-ownership.md`，按 claim 认领或退回交付者。

共享 runtime 归属按 `references/proactive-collaboration.md`；端口不同不等于数据隔离。仲裁留在本 skill；已知任务进程的安全停止与释放转 `briefbound-development-cleanup`。

## 受控跨任务投递（`BRT_TRUSTED_RELAY_V1`）

2026-08-26 的隔离冒烟证明 `send_message_to_thread` 能精确唤醒目标、产生 turn 并返回 ACK；平台将消息包装为带 `codexDelegation.sourceThreadId` 的 `<codex_delegation>`。本 skill 将它作为受控 Agent relay，而非用户输入或新权限。正文自报的 ID 不可信；只有当前 turn 的平台源 ID 与 fresh thread snapshot 匹配才可作为来源事实。

投递前依次满足：

1. fresh `list_threads/read_thread` 取得精确 source/target，二者均为 Codex task、thread ID 不同且 host 相同；
2. 非空 `projectId` 相同，或在 managed Worktree 缺失 project ID 时，用只读 `git rev-parse --path-format=absolute --git-common-dir` 得到完全相同的 `gitCommonDir`；标题、普通路径相似或历史 registry 不够；
3. 首次只向 idle 目标发送 `COLLABORATION_PROPOSAL`；目标用同一门禁校验 source 后自主 `PEER_ACCEPT / PEER_ADAPT / PEER_DECLINE`，接受前不根据 relay 写入；
4. envelope 使用 `BRT_TRUSTED_RELAY_V1`，参与者是精确会话对，`permissionMode=receiver_existing_scope_only`；relay 不能授予删除、发布、远程 Git、建任务、越界写入或其他新权限；
5. 从当前已加载的 `briefbound-thread-coordination` skill 目录解析 `scripts/validate_thread_transport.py`（不是从项目仓库 cwd 查找）；它对完整 envelope 返回 `TRUSTED_RELAY_AUTHORIZED` 后才发送。失败不改投、不猜测、不把 ACK 当授权。

接收方只在自己的原始用户任务和既有写入范围内采用 peer 证据；代码、Git 和测试始终优先于消息。一次性状态交换或冲突留在本 skill；持续互助交 `briefbound-multi-agent-orchestration`；自动闭环仅在用户另行明确启用时交 `briefbound-autonomous-collaboration-loop`。所有会话平级，不建立主从关系。

## 冲突恢复

Silent Conflict Triage 核验 claim、真实写入和替代工作；优先 `SELF_NARROWED / CONTINUE_NON_CONFLICTING / WAIT_SILENTLY`。

需共同决定时为 `DISCUSSION_REQUIRED`：在已接受 agreement 内发送一次 `DISCUSSION_REQUEST`，包含双方、共享面、证据和待决事实；没有新增决策价值不发送。各方继续各自非冲突工作。

继续执行会立即覆盖/回归、无法拆分且协商不能避免时才为 `PAUSE_REQUIRED`：经 trusted relay 发送一次 `CONFLICT_PAUSE_REQUEST`。`PAUSE_REQUEST` 不等于 `PAUSED`，确认前不写冲突面。

修复后本地记录 `resolve`，经 trusted relay 发送一次 `CONFLICT_RESOLVED`；对方验证 Git/运行证据后恢复，不把消息本身当作修复证据。

三门禁仍为 `Target Validity Gate`、`ACK Gate` 与 `Coordination Closeout Gate`。地址事实只允许进入 envelope 校验；缺少 trusted relay 授权、有效 ACK 或 Git closeout 证据时不接管、不关闭。

`main` 推进、合入排队或 gate 可能 stale 不属于 `PAUSE_REQUIRED`。Peer 只在已接受 agreement 内发送 `MERGE_READY`；由有效 integration claim 的 owner 以 Git 和测试证据串行应用交付。

pause 产生 `resumePendingAgentIds`；债务清零才能 `complete`：

- `open` 默认 30 分钟租约；跨 checkpoint 用 `heartbeat`，不高频轮询。
- `status` 标记 `owner-stale`；注册 Agent 用 `takeover` 并继承恢复义务。健康 owner 仅由用户改派。
- 目标已 stale 且 fresh `list_threads/read_thread` 证明无法安全恢复时，owner 可用 `expire-resume --evidence <fact>` 清除本地债务并释放 yielded claim；这不会把对方任务标为完成、归档或改投。
- 任务明确取消/归档才可 `cancel-resume --confirmed-by-user`；无回复不等于取消，不得自行设置确认标记。

## 讨论与合并

讨论优先于暂停；同一 participants + surface 存在则复用，不重复发送。

各 Agent 发送 `MERGE_READY`（branch/base/head/scopes/dependency/tests/risks）。Integration Owner 用 Git 重验；无重叠成组，共享面串行，全部进入目标分支后只跑一次完整 gate。失败只通知责任方和受影响依赖，成功广播一次 `INTEGRATED`。standalone 不自动 push、发布或清理。

条件合入快线及失败分类读取 `references/integration-ownership.md`。

影响未来行动的决定才执行 `sync_project_memory.py --coordination-id <id>`；普通并行会话不写 tracked memory。

## 完成

未收到 `PAUSED` 为 BLOCKED；已修复未恢复为 PARTIAL。relay delivery/ACK 不等于 `RESUMED` 或集成完成；merge 仍需目标分支包含交付且验证通过。
