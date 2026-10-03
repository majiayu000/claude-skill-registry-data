---
name: briefbound-multi-agent-orchestration
description: "Use when two or more existing independent Codex App threads in the same project can benefit from bounded peer coordination through BRT trusted relay, while each thread retains its original task, permissions, branch, and completion responsibility."
license: MIT
---

# Briefbound Peer-Agent Collaboration

## 目标

让同项目的平级会话 Agent 各自完成原任务，同时通过最少必要协商减少重复劳动、修改冲突、过期结论和集成返工。编排对象是协作过程，不是其他 Agent。

## Briefbound task contract

- Context Boundary: 已对齐意图、现有独立 thread、各自任务/scope/branch、共享契约、依赖、冲突和集成目标。
- Output Contract: peer agreement、责任边界、共享决定、依赖交付、集成证据和各自任务状态。
- Allowed Action: 读取 thread/Git 证据；在 `BRT_TRUSTED_RELAY_V1` 门禁通过后发送协议消息、维护 agreement/claim，并执行已授权的本地集成。不得替对方改任务状态；新建会话、远程 Git、发布和破坏性动作需授权。
- Success Evidence: 每个 Agent 的原任务保持 owner；agreement、共享边界、Git/测试集成证据和恢复债务闭环。
- Stop Condition: 意图未对齐、不是同项目、缺少有效 thread、协作成本不低于收益、责任争议、高风险取舍或权限不足。
- Route Out: 各 Agent 原 owner、`briefbound-autonomous-collaboration-loop`、`briefbound-thread-coordination`、`briefbound-pr-review`、`briefbound-development-cleanup`、`briefbound-router` 或 BLOCKED。

## 统一调用契约

- 所有 Agent 平级且保留原任务、写入许可、branch 和完成责任；没有主从、派发或隐式任务转移。
- 用户可见内容默认中文，只报改变行动的共同决定、依赖、风险和集成证据。Route Out 仅以 Briefbound task contract 为准；有自然闸门时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。
- 协作必须改善至少一个本地任务且不损害其他任务，或降低共享项目的冲突/回归；否则静默返回各自工作。

## 进入闸门

Briefbound Router 已对齐意图并有界发现；至少两个现有独立 Codex task 通过 `BRT_TRUSTED_RELAY_V1` 身份门禁，存在真实互补、依赖、重叠或共同集成面。非空相同 `projectId` 可证明同项目；managed Worktree 缺失该字段时必须解析到相同 `gitCommonDir`。原生子 agent 不是平级会话，不能加入 discovery、agreement、outbox 或 relay。需平级多会话原语；缺失时不触发，按 scope 串行降级（见 harness 矩阵）。

首次 proposal 只投递给 idle 目标。双方 fresh 校验平台注入的源 thread ID；接收只表示愿意在自身原始任务/权限内协调，不从 relay 获得新写入、删除、建任务、发布或远程 Git 权限。通过后交接为 `PEER_COLLABORATION_READY`。

简单任务、仅目录相似、无共享决定、同一小文件无法并行，或消息/合并成本高于预期收益时不进入。一次建议、状态交换或单一冲突只用 `briefbound-thread-coordination`。

本 skill 维护平级协作协议，不负责持续驱动。用户已确认自动推进所有 peer、恢复冲突并合入本地 `main` 时，以 `briefbound-autonomous-collaboration-loop` 为 primary，本 skill 只提供 agreement 支持。

## 平级协作循环

### 1. 建立各自与共同事实

读取每个候选的 `Task / Desired Outcome / Scope / Branch or Worktree / Checkpoint / Blocker / Success Evidence`。区分：各自独占面、共享契约、依赖交付和集成面。代码、Git 和运行证据优先于消息或 registry。

### 2. 提出协作而非派发

任何 Agent 都可提出 `COLLABORATION_PROPOSAL`，但不能改变对方任务。对方以 `PEER_ACCEPT / PEER_ADAPT / PEER_DECLINE` 自主决定。只有接受后才形成 agreement；需要消息结构时读取 `references/team-protocol.md`。

agreement 只记录 `Peer Tasks / Shared Surface / Each Scope / Dependency / Integration Target / Current Integration Claim / Evidence / Exit Condition`。`Coordination Owner` 仅维护共同决定，`Integration Owner` 仅负责合入验证，均不拥有其他 Agent。开始协作时可以没有 Integration Owner。

使用一次 registry claim 原子占用 `lane=collaboration/<topic-key>`，并加入相关 `thread/<thread-id>`、`host/<host-id>` 与共享 surface，防止重复提议；拒绝、过期或结束后释放。每个 Agent 继续自己的非冲突工作，不等待可选协作。

### 3. 动态认领集成责任

首个交付进入 integration queue 时，相关 Agent 只检查一次 `lane=integration/<target-key>`。无有效 claim 时可原子保留队列；目标不干净则标记 `WAITING_FOR_CLEAN_TARGET`，不得 rebase、应用或合并。已有 claim 时，其余 Agent只发 `MERGE_READY`，不重复 gate/merge。用户指定优先；负责人无法维护队列才交接释放。细节交 `briefbound-thread-coordination`。

### 4. 用信息价值降低熵

只在共享契约变化、依赖就绪、可行动新证据、结论纠正、真实 blocker 或 `MERGE_READY` 时通信。消息必须说明发送者、原任务、证据、对双方行动的影响和期望回复。

不发送无变化进度、逐步思考、重复边界、可自行读取的信息或非阻塞催促。相同事实只保留最新结论；矛盾结论用 `CORRECTION` 明确替代关系。没有新增决策价值时继续各自任务。

### 5. 协商冲突与依赖

共享接口或实现顺序有分歧时，由 `briefbound-thread-coordination` 维护 discussion，各方提交立场与证据后形成共同决定。先调整 scope、顺序或接口；只有继续写会立即覆盖/回归且无法拆分时才暂停。暂停方让出 claim，解决后必须恢复，不能因另一方结束而遗留。

### 6. 协同集成而非收编结果

每个 Agent 独立报告 `Base / Head or Artifact / Changed Scope / Tests / Assumptions / Risks`。当前有效 integration claim 的 owner 用 Git 与测试重验，不把消息当事实源；队列已有交付但 claim 为空时，先完成动态认领，不把合并义务留给用户。

- 同一 checkout 的不重叠修改无需制造 merge；独立 branch/worktree 才进入 integration queue。
- 有依赖或共享契约时串行集成；冲突由相关 Agent 共同决定，机械冲突才由 Integration Owner 处理。
- 每项运行窄验证，全部合入后运行一次集成 gate；失败只通知责任 Agent 和受影响依赖方。
- 不得在未授权时 push、创建/合并远程 PR、发布或直接改受保护 `main`。

## 完成与降熵门

协作完成不等于替任何 Agent 完成任务。只有各自交付达到原验收、共享决定一致、必要集成验证通过、integration claim 已释放、open coordination 和 `resumePendingAgentIds` 恢复债务清零时，才结束共同 agreement。

收口前检查：是否减少了重复实现、冲突修改、过期消息和多余 worktree；协作日志是否只保留会改变后续行动的事实。存在真实残留才路由 `briefbound-development-cleanup`。
