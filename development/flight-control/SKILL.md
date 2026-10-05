---
name: flight-control
description: 使用状态绑定的最小 Tool Surface、exact Action Gateway、来源可追踪的 MissionSpec 与 Verification Manifest、宿主无关 Flight Progression Engine、可选且无权威的 App Server continuation、顺序持久 Wave、一层原生 Agent、困难后强制战术指导、证据型 Capability Profile、显式 Manual Verification、不可变宿主 Evidence、恢复检查点和仅本地 Git，治理复杂 Codex 开发。用户要求飞控接管、继续、自主开发、修复或完成多步骤软件项目，需要有界并行子代理，或实现前必须建立文档工程时使用。
---

# Codex 编程飞控

在不把模型置信度当作证据的前提下自主开发。模型负责规划、实现和纠错；项目记忆、Wave
边界、权限与完成状态由可检查合同控制。

规划 Wave、分发写入 Agent 或解释 reconciliation 前，必须阅读
[控制协议](references/control-protocol.md)。

## 一、执行确定性预检

1. MCP 可用时，第一步调用 `flight_status`。
2. SessionStart 已注入 exact Project、Host Session、thread runtime domain 与 Lead
   credential 时，调用 `flight_state_status` 读取 Project 全局完整性和当前根线程摘要；
   禁止省略、猜测或跨会话复用 credential。聚合 `BLOCKED` 不能被解释为当前线程的
   控制状态；`CORRUPT` 才是 Project 全局阻断，当前 Run/Discovery 的阻断只服从其
   exact 状态与门禁。
3. 随后调用 `flight_surface_status`。生产连接必须从 `BOOTSTRAP` 启动，只显示 8 项
   Bootstrap 工具，同时报告 81 项 sealed 注册表；Surface 只减少选择，不授予权限。
   普通受治理开发使用当前 SessionStart 注入的 exact Project、Host Session 和 Lead
   credential 调用一次 `flight_surface_select` 选择 `RUN`。禁止请求 `FULL_COMPAT`。
4. 无效显式配置、不受支持 runtime、Surface 注册数/allowlist hash 漂移或选择失败都是
   阻断条件。禁止静默继承、猜测默认值、直接调用隐藏工具或继续写入。
5. Product Discovery 活动时，`RUN` Surface 会以 `DISCOVERY_RUN_CONFLICT` 失败关闭。
   此时只选择 `DISCOVERY`，读取 `flight_discovery_status`，停止 Run 创建。禁止绕过
   或替换 Session。已完成 Discovery 需要 handoff 时，只能消费本轮显式
   `$flight-control` 注入的 `discovery_handoff_token`；禁止代替用户调用
   `$flight-brainstorm`。
6. 编辑业务代码前调用 `flight_documentation_prepare`。`baseline` 只能包含用户本轮
   目标或权威项目来源已经证明的事实；无法证明时省略，禁止填入猜测。
7. assessment 为 `BLOCKED` 时，只按冲突项和 Document Debt 修复文档。仅对精确
   文档路径申请 `flight_documentation_write_gate`；修复后用新幂等键创建新的不可变
   assessment 记录。
8. 阅读仓库规则、当前路线图、相关架构、需求追踪、已接受 ADR 和质量门禁。
9. 新 Run 前，从 exact current `READY` assessment 调用
   `flight_mission_spec_compile`。目标、范围、非目标、验收条件、安全不变量、用户决策
   域和风险都必须有已接受来源；`unresolved_assumptions` 必须为空，
   change budget 必须显式。
10. 调用 `flight_verification_manifest_compile`，完整覆盖每个 acceptance obligation
   和 Mission risk。WRITE Mission 必须有来源已验证 COMMAND；非 `CUSTOM` obligation
   必须使用 COMMAND evidence；只有声明为用户决策域的事项才可使用 `MANUAL`。
11. 创建或找回一个持久 Run。新 Run 只能绑定 exact MissionSpec ID/hash、Verification
   Manifest ID/hash 和 current `READY map_hash`。禁止向 `flight_run_create` 传入原始
   objective、scope、non-goals 或 completion JSON。
12. Lead 自己写入业务代码前，针对实际路径取得新的
    `flight_documentation_write_gate` 回执。Controlled Wave 会对 Slice WRITE claim
    union 单独执行当前 Gate。只有 `ALLOWED` 授权业务写入；
    `REMEDIATION_ONLY` 只授权文档修复。
13. 确认 SessionStart/持久状态预检已经建立或验证本地 `main` 基线。已有 main 永不
    移动；缺失时只允许本地创建 ref 或空 bootstrap commit，不 checkout、不 stage 用户
    文件、不修改 dirty 主工作区，也不执行任何远端 Git。
14. 明确当前 Mission，并且只选择一个 active Wave。

MCP 报告某项 capability 不可用时，禁止模拟该能力。尤其禁止把聊天文本冒充持久状态、
把普通文件冒充 Evidence、把手工 Agent prompt 冒充分发 permit。

## 二、只通过 Flight Progression Engine 推进

当 `progression_engine: true` 时，`flight_engine_advance` 是受治理 Run 的唯一首选推进
入口。Flight Control 拥有 Mission 推进权；Codex Goal 不属于本协议。

1. 使用当前 attested Lead credential、稳定 Driver ID、受限 retry budget、30–300 秒
   TTL 和新的 operation idempotency key 调用 `flight_engine_advance`。
2. 返回 `EXECUTE_ACTION` 时，只调用一次 `flight_action_execute`。原样传递响应中的
   Action/Controller version、fence、claim token、Host/Lead identity 和 Action
   `idempotency_key`；`required_inputs` 只能包含 Action contract 中除 Gateway 管理字段
   之外的业务字段。底层 `target.tool` 和 `fixed_arguments` 只用于核对，禁止直接调用、
   回传、替换或覆盖。
3. Gateway 返回非空 `host_followup=collaboration.spawn_agent` 时，只执行这一个宿主
   后续动作，并原样使用 `target_result` 中的不可变 `spawn_envelope`。禁止自行补字段、
   改写 prompt、换模型、创建第二个 Agent 或建立嵌套 Agent。完成 Host binding 后才能
   继续；Gateway 未返回该字段时禁止 spawn。
4. 下一次 `flight_engine_advance` 报告 Gateway 和可选 Host follow-up 的真实结果。
   必须携带 exact Action/Controller
   version、fence 和 claim bearer。长任务在租约到期前使用 `HEARTBEAT`。
   `SUCCEEDED` 只是请求服务端验证后置条件；失败必须如实使用 `FAILED_RETRYABLE`、
   `FAILED_TERMINAL` 或 `ABANDONED`。
5. `ACTION_IN_PROGRESS` 仅允许原调用方继续其已经持有 bearer 的 exact Action。
   `RECLAIM_REQUIRED` 表示响应不能重新暴露一次性 credential；禁止猜 token、重放副
   作用或新建 Action。等待过期或 Host Session recovery，再用新幂等键推进。
6. `WAITING_FOR_AGENT` 或 `WAITING_FOR_GUIDANCE` 时，禁止重复 spawn、重复交付或忙
   轮询。`HUMAN_DECISION_REQUIRED`、`PAUSED` 或 `BLOCKED` 时，停止自主项目修改。
   `AWAITING_HOST_TURN` 时，不依赖 transcript 保存状态，等待宿主提供新 turn 后从
   服务端恢复。`COMPLETED`、`FAILED` 或 `CANCELLED` 时停止。
7. 用户要求 `PAUSE`、`RESUME` 或 `CANCEL` 时停止本 Skill，不得代替用户执行。
   只展示服务端当前 Run、Controller 和 version，并要求用户在新的 turn 精确调用
   `$flight-control-run <run_id> <controller_id> <expected_version> <PAUSE|RESUME|CANCEL>`。
   控制完成后必须从新的 canonical state 继续，不能复活旧 Action 合同。

每次成功 advance 都会持久化无 secret 的 Progress Receipt。根 Stop Hook 返回一次
continuation 时，只执行已经签发的 Action，再次 advance；固定 continuation 文本没有
任何额外 authority。waiting、human、paused、blocked、terminal、stale、re-entry 或
no-progress budget 耗尽时必须允许停止。

低层 Controller 工具只保留给服务端、诊断和兼容 Driver。模型禁止在同一 active
Action 上混用 Engine facade 与手工编排。

默认 Host continuation 为 `POLL_ONLY`，原因必须精确区分
`HOST_CONTINUATION_DISABLED`、Sandbox 未证明、adapter 不可用或恢复阻断。只有用户在
独立 prompt 显式调用 `$flight-connect-host <run_id> <thread_id> ENABLE`，并且 App
Server、本地 Host Bridge、新鲜 exact Sandbox Attestation 与 delivery receipt 全部由
服务端验证后，才能报告 `APP_SERVER`。该 transport 只创建后续 turn，不规划 Action、
不携带 bearer，也不能替代 Mission/Gate。禁止把持久化或普通 Hook 描述为无人值守唤醒；
禁止启用、镜像或依赖 Codex Goal。Computer Use 不属于本插件。

## 三、每次只推进一个 Wave

1. Wave 创建、Dispatch permit 与 reconciliation 都是服务端派生的 Gateway target。
   Lead 只能执行 Engine 返回的当前 Action，禁止绕过 Gateway 直接创建 Wave、签发
   permit、改变 reconciliation 决定或调用隐藏目标工具。
2. 服务端冻结每个 Wave 的范围、依赖、exact/tree path claim、逻辑资源、允许工具、
   允许命令、禁止动作、预期产物、验证命令、文档影响、容量和复杂度。Lead 只能核对
   `flight_engine_advance`/`flight_action_execute` 返回的冻结合同，不得补猜或改写。
3. 默认使用 `DEFAULT_CONSERVATIVE` 与 `FINE`。只有
   `flight_capability_profile_build` 或 `flight_capability_profile_get` 返回基于终态、已报告 Attempt 且 BOUND
   `OVERRIDE` model receipt 的 exact immutable profile，才能使用
   `RECORDED_BEHAVIOR`。Profile ID/hash、建议粒度、角色/任务类别和 Run 的 exact
   model/reasoning override 必须完全匹配。`USER_SELECTED` 尚未获得
   独立授权合同，禁止使用。至少保留一个 control slot。
4. Slice 必须小到轻量模型无需猜测也能完成。对全部冲突 WRITE claim 建立有序 DAG，
   每个 Slice 在 `integration_order` 中恰好出现一次。需要战术指导时，最多增加一个
   read-only `tactical_advisor` control Slice，并至少保留一个 business Slice。
5. `flight_wave_status` 仅用于读取状态，不授予分发权。只有 Gateway 明确返回
   `host_followup=collaboration.spawn_agent` 时，才可原样使用该 Action 的
   `spawn_envelope` 创建一个原生 Agent。permit 丢失、重放要求换发或 envelope 不完整
   时必须回到 Engine；禁止自行重建 nonce、version、prompt、model 或 reasoning。
6. 所有 child 都必须是 Lead 的直接子节点。绑定 child 禁止再次调用 Agent、扩大路径
   或命令，也禁止把 capability token 写入文件、输出或消息。
7. child 必须运行全部冻结 `verification_command`，并在停止前调用
   `flight_attempt_report`。必须使用注入的 `agent_id`、`attempt_id`、lineage fence
   和一次性 capability。成功报告必须对每条命令恰好提供一次 exit code 0 和 output
   SHA-256。Guidance successor 必须先 ACK exact Directive，再记录 Guidance Outcome。
   MissionSpec 对 Wave 数、Slice 文件数、successor Attempt 和 no-progress
   continuation 的预算不可绕过；禁止通过重命名或拆标签规避。
8. Agent 停止后重新调用 `flight_engine_advance`，让服务端观察 Attempt、依赖和容量，
   再通过 Gateway 派生下一项 dispatch、reconciliation 或 completion Action。禁止
   根据 `flight_wave_status` 的只读结果自行推进。
9. `WAITING`、`BLOCKED`、`PARTIAL` 和 `REPLAN_REQUIRED` 都是需要证据处理的控制
   决定。`READY_FOR_COMPLETION_GATE` 只允许进入确定性完成链，不表示完成。

Agent 运行期间可以执行有价值的本地工作，但禁止仅为“看起来在编排”而创建 Agent。

## 四、在边界内保持自主性

Agent 可以在 Work Order 内调查、选择实现细节、编辑、测试和纠错。Hook 是受支持工具
调用的宿主护栏，不是操作系统 sandbox。Lead 必须检查 Evidence；发生 drift、合同不
充分、安全不变量受威胁或重试不产生新信息时必须介入。

business child 缺少关键事实时，只能提交一个有界、脱敏 Problem Capsule 到
`flight_guidance_submit`，然后停止。提交成功会原子冻结 FINAL snapshot 和 Guidance
Handoff，使旧 Attempt/Slice yield，并撤销 capability、binding 和 lease。旧 turn
禁止继续调用任何工具。

`PostToolUse` 会记录脱敏 Difficulty Signal。进入 `STUCK` 或 `STRATEGIC_BLOCK` 后，
下一次 `PreToolUse` 只允许角色合同已允许的 Guidance 工具或
`flight_attempt_report`；普通 read、shell、patch 和 business MCP 全部拒绝。禁止换
工具名继续猜测。只能求助或如实提交终态 blocker。

Tactical Advisor 只能领取 `OPEN` 信件，使用短 lease 和单调 fence。它可以读取冻结
合同、文档、Evidence 和 mailbox，但禁止写 workspace、调用 Agent、创建 Skill 或扩大
authority。它可以 heartbeat、请求补充证据、回复或把战略决定升级给 Lead。

claim 后调用 `flight_guidance_route`。只能使用 Wave frozen snapshot 返回的有界 Skill
Frame。`NO_MATCH`、`ABSTAIN` 或 `CONFLICT` 必须使用 model fallback 或升级 Lead；
禁止强制匹配。`MATCHED` Reply 必须绑定 exact Route 和不可变版本，禁止读取 ambient
Registry 或注入整个 Skill。

Lead 只有在当前 documentation、epoch、lineage、yielded state、workspace snapshot、
capacity 和 lease 全部通过时，才能 drain `ANSWERED` outbox。stale reply 变为
`REJECTED_STALE` 并要求 replan，禁止创建 successor。

successor 必须先用 exact Directive digest 调用 `flight_guidance_acknowledge`，再调用
`flight_guidance_report_outcome`，最后才能提交终态 `flight_attempt_report`。

Private Skill 是战术记忆，不是常驻 prompt。只有用户明确调用
`$flight-forge-github`、`$flight-forge-local-skill` 或 `$flight-forge-session`
后才能创建。普通 `$flight-control` 禁止代替用户触发 Forge。

角色配置同样只能显式修改。普通流程只能读取 effective policy，禁止调用
`$flight-configure-roles`、写 override 或代替用户选择 model。新 Run 会把十个角色的
解析结果冻结为不可变 policy snapshot；配置变化只影响未来 Run。

## 五、只用 Evidence 完成

接受 Slice handoff 或 reconciliation 前：

- 执行风险要求的 format、lint、type、unit、integration、recovery 和 security 检查；
- 检查 diff 和 allowed path；
- 拒绝弱化测试或与证据矛盾的完成声明；
- 同步 canonical documentation、ADR、contract、migration 和 traceability；
- 明确记录未解决风险；
- 只有项目策略授权时才创建本地 Git commit；
- 禁止仅凭 `READY_FOR_COMPLETION_GATE` 宣称 Wave 完成。

WRITE Wave reconciliation 后严格执行：

1. 用 `flight_completion_status` 读取 compiled Verification Manifest 投影出的冻结
   Slice/Wave/Mission 义务、命令名称和 blocker；该只读结果不授予执行权限。
2. 继续固定的 Engine → Gateway → 可选 Host follow-up → Engine report 循环。命令
   Verification、Slice/Wave/Mission evaluation 和本地 commit 都只能由当前
   `flight_action_execute` 根据冻结 Action Registry 调用；Lead 禁止直接调用这些隐藏
   target，也禁止传入 shell、任意 argv、commit message 或自行选择评估 scope。
3. Gateway 执行 Verification 时，宿主必须在受支持的 sandbox provider 中运行冻结
   argv，并重新验证 command source、cwd、网络和写入边界。sandbox unavailable、
   timeout、非零退出、输出截断或来源漂移都必须如实报告失败，不能回落到 Lead shell。
4. 有变更的 Wave 必须由服务端先派生 `READY_FOR_LOCAL_COMMIT` Action；本地 commit
   后还要通过新 Action 重新评估 Wave。只有服务端 Mission Gate 返回 `ALLOWED` 才能
   报告完成。
5. 存在 pending `MANUAL` 时，在 `HUMAN_DECISION_REQUIRED` 停止，并向
   用户显示精确
   `$flight-approve-verification <run_id> <entry_id> <APPROVE|REJECT>`。禁止代替用户
   调用、改写决定或伪造授权。用户后续显式调用对应 Skill 后，重新从 canonical
   Controller state 恢复；`APPROVE` 只满足该 entry，`REJECT` 是不可变 blocker。

只有绑定当前 contract、environment、Documentation 和 workspace 的
`HOST_EXECUTED` Evidence 能满足 Gate。Agent report 只用于诊断。Local commit 只留在
托管 `codex/flight-*` branch；禁止 stage 用户 main worktree、merge、删除 worktree、
push、建 PR、tag、release 或 publish。

## 六、只在真实边界停止

修复尝试和剩余 `READY` Slice 仍在预算内时继续。只有以下条件之一成立才返回用户：

- Mission 已满足全部可用确定性 Completion Gate；
- 产品决定会实质改变结果；
- 缺少必要 authority、credential 或范围外访问；
- 已验证安全边界阻断；
- 证据驱动修复达到文档规定的 retry/escalation 上限。

`completion_gate: false` 时，明确报告当前 Host 无法生成 Flight Control 完成判决。
需要支持证据时使用 `$flight-diagnose`；诊断不能替代 Completion Gate。

始终禁止远端写、自动发布、无界嵌套 Agent 和 Computer Use。
