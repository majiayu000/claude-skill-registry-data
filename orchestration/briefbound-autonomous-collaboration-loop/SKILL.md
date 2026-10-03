---
name: briefbound-autonomous-collaboration-loop
description: "Use when the user explicitly enables an automated same-project multi-thread development loop that keeps peer Codex tasks progressing, recovers conflicts or stale coordination, integrates verified work into local main, and closes cleanup without repeated gates; do not use before opt-in, for one-off coordination, remote publication without permission, or subagent creation."
license: MIT
---

# Briefbound 自动协作开发闭环

## 目标

一次确认后，驱动同项目平级会话完成、验证、合入 `main`；不建主从或接管任务。

## Briefbound task contract

- Context Boundary: 已对齐目标、授权的现有同项目 thread、各自 scope/branch/worktree、共享契约、目标 `main`/验证门。
- Output Contract: agreement、交付证据、integration queue、本地 `main` 验证和恢复清理。
- Allowed Action: 在授权范围内读取 thread 状态、维护本任务 registry、执行本地写入/提交/合入 `main`、验证和安全清理；当前 `BRT_TRANSPORT_DISABLED`，不得发送 thread 消息。新建会话、远程 push/PR merge/发布、破坏性或高风险动作仍需单独授权。
- Success Evidence: 每个原任务达到验收，目标 `main` 包含预期交付，集成门通过，open coordination、恢复债务和已知开发残留清零。
- Stop Condition: 未获开启确认、共同目标或 target 不明、产品/安全/数据迁移取舍未决、需要远程授权、破坏性动作，或自动恢复连续失败。
- Route Out: 各 Agent 原 owner、`briefbound-multi-agent-orchestration`、`briefbound-thread-coordination`、`briefbound-pr-review`、`briefbound-development-cleanup`、`briefbound-project-memory`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 用户可见内容默认中文；只报行动决定、blocker 和最终证据。Route Out 仅以 Briefbound task contract 为准；有自然闸门（需用户裁决、批准或被外部阻塞）时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。
- 各 Agent 仍负责自己的任务、scope、branch；Loop Owner 只维护闭环。
- 开启后不在每个阶段、task、普通冲突或恢复动作后询问是否继续。

## 开启与授权

Briefbound Router 仅在非简单目标确有多会话协作价值时，询问一次明确列出项目、既有参与会话、integration target 和本地集成范围的授权。确认后才可联系这些现有会话、协商、安全开发、验证和限定目标的本地集成，直到完成、取消或自然闸门；泛化“继续/确认”不扩大到创建会话或新的 integration target。

没有合适会话时，只询问一次是否创建。远程 push、PR 或破坏性操作不继承授权。自动循环还必须具备已验证的 `BRT_DIRECT_USER_TURN_V1`，且运行环境提供平级多会话原语（见 harness 能力矩阵）；任一不满足保持 `BLOCKED_TRANSPORT`，不启动跨任务循环或 outbox。

## 角色与持久状态

- `Loop Owner`：维护状态、租约、outbox、恢复债务和完成门，不代写 peer 结论。
- `Peer Owner`：完成任务，提供 scope、依赖和 `MERGE_READY`。
- `Integration Owner`：由任一合格 peer 在首个 `MERGE_READY` 出现后可原子认领，维护当前队列；只有目标干净、授权范围匹配且重验通过时才合入 `main`。claim 有效期间不启动新的无关实现任务，变忙时先转交队列。
- `Recovery Dispatcher`：任何活跃参与者在 Loop Owner 租约过期时可 `takeover`，继承 outbox、恢复和集成义务，但不能继承或伪造 peer 的完成声明。

状态为 `DISCOVER -> AGREEMENT -> RUNNING/NEGOTIATING -> MERGE_READY -> INTEGRATING -> INTEGRATED -> CLOSED`。每个 peer 只记 `Task / Scope / Branch or Worktree / Dependency / Checkpoint / Tests / Blocker / Resume Debt`；优先 registry，跨会话恢复才用 memory。

## 自动循环

### 1. 发现与约定

只读最多 3 个相关 thread，确认收益、边界、契约、依赖和 Integration Target，用 `briefbound-multi-agent-orchestration` 建 agreement。Integration Owner 可等首个交付入队后认领；无收益则返回原 owner。

### 2. 并行推进

各 peer 继续非冲突任务。`BRT_TRANSPORT_DISABLED` 期间不得通信、轮询、入队或催促；`MERGE_READY` 只由原任务交付或用户直接传达。未来恢复后，消息默认只发差量：`From/Task / Changed Fact / Action Impact / Evidence Pointer / Reply Needed`；背景、方案和测试用指针，首次契约或安全语义才展开。

### 3. 冲突协商

普通重叠先缩 scope、调顺序或交换接口，由 `briefbound-thread-coordination` 复用 discussion。仅无法拆分且继续写会立即覆盖/回归时暂停冲突 surface，记录 `resumePendingAgentIds`；解决后发 `CONFLICT_RESOLVED` 并确认恢复。

`main` 变化、排队或 gate stale 不暂停。Peer 聚焦验证并提交 `MERGE_READY` 后结束执行，由 Integration Owner 集成；不等待 stable main，不反复 closeout。

### 4. 故障与接管

每次收发在未来恢复后均先通过 `briefbound-thread-coordination` 的 `BRT_DIRECT_USER_TURN_V1` 验收门：只允许同项目、fresh `read_thread` 返回精确 `threadId` 的平级顶层 thread；原生子 agent 不得加入 outbox 或 relay。当前不得调用 `send_message_to_thread`，不得保存 outbox，也不得依据 `/root`、agent 标签或旧 registry 重新寻址。Loop Owner 失活时只记录交接事实，不自动唤醒其他任务。

自动恢复先分类为任务、依赖、集成或环境失败；证据发给 owner，其他 peer 继续。只有高风险取舍或同一 blocker 经两轮不同恢复策略仍失败才询问用户。

接管者只继承推进义务，不能继承证据所有权。失活 peer 没有正式 `MERGE_READY` 时：

- Git commit/artifact、scope 和新鲜验证足以独立重验：接管者可标记 `MERGE_READY_RECOVERED`，必须注明原 owner 未确认及重验证据。
- 只有聊天中的采纳、计划、进度或草稿：标记 `RECOVERY_PENDING_EVIDENCE`；接管者自行完成缺口或恢复原 owner，不能代其宣告完成。
- 无法安全完成且两轮恢复失败：保持明确 owner/blocker 后再询问用户，不把缺证据项目合入。

### 5. 集成队列

每个 peer 用 `MERGE_READY` 入队，完整证据字段规范见 `briefbound-multi-agent-orchestration` 的 `team-protocol.md`。`MERGE_READY_RECOVERED` 也必须满足相同证据门。Integration Owner 以 Git 和新鲜测试为事实源：

首个交付入队时检查一次 `lane=integration/<target-key>`：无 claim 则认领队列并发 `INTEGRATION_CLAIMED`。baseline/dirty main 时进入 `WAITING_FOR_CLEAN_TARGET`，保留证据但不应用、变基或合并；已有负责人则其他 peer 停止合并。Loop Owner 对空缺自行认领或只联系一个合适 peer，不轮询或询问用户。细节交 `briefbound-thread-coordination`。

1. 无依赖且不重叠的交付可成组；共享契约或依赖项串行。
2. Peer 只需聚焦验证；Integration Owner 对过期 base 变基或应用提交，重验受影响窄面。机械冲突可处理，语义冲突才回相关 peer。
3. 全部预期交付合入本地 `main` 后只运行一次完整集成 gate；失败才重开责任任务和受影响依赖。
4. 不用远程 CI 替代本地证据，也不在未授权时 push 或操作远程 PR。

gate 期间若无关任务推进 `main`，不冻结全项目：比较新增提交与本轮 scope；无重叠则在最终 HEAD 补受影响的窄验证，有语义重叠才重跑对应 gate。不得因无关漂移重跑整套门禁。

可重建的 ignored/untracked 测试缓存不阻塞 `MERGE_READY`，统一留给 final cleanup；删除受阻且不影响 tracked 交付时保留，不更换多种命令追查。

### 6. 收尾

验收和集成 gate 通过后，广播一次 `INTEGRATED`，释放 integration claim 并关闭 merge coordination；债务清零后用 `briefbound-development-cleanup` 清理安全残留，最后只做一次整体汇报。

## 完成门

以下条件必须同时成立：

- 每个 peer 的原任务已完成或由用户明确取消；“消息已发送”“已采纳”“接近完成”和恢复生成的总结都不能代替交付证据；
- 本地 `main` 包含所有预期交付且集成验证通过；
- 没有有效或遗留 integration claim、未处理 outbox、open coordination、stale owner 或 `resumePendingAgentIds`；每个 `TRANSPORT_EXPIRED` 都有 fresh list/read 证据；
- 清理没有删除未合并工作，远程动作仍保持未执行；
- 失败和 Deferred 项有明确 owner、证据和触发条件。

未满足时由当前 Loop Owner 或接管者继续闭环，不把普通协调债务抛回用户。
