---
name: agent-switchboard-ops
description: |
  以"管理者—执行者"模式运维 agent-switchboard MCP：受管 Claude supervisor 生命周期、跨模型委派（Codex/Claude/Gemini）、验收纪律与已知陷阱对策。
  用于存在任一可用委派通道（mcp__agent-switchboard__* 工具或宿主原生 subagent），且用户要求委派执行、监督长任务、跨模型审查、回收多 agent 会话成果，或询问"怎么让 Codex/Claude 帮我做"的场景。
  不用于单会话即可完成的普通修改；未安装 agent-switchboard 时仍可经原生 subagent 通道触发，但不要猜测工具名。
---

# Agent Switchboard 运维手册

本 Skill 是使用 `agent-switchboard` MCP（本地跨 agent 协作桥）的操作契约，全部经验来自真实生产使用的事故与验收记录。只负责编排规则；任务本身的修改纪律交给 `minimal-implementation`，范围澄清交给 `clarify-before-change`。

## 适用范围与触发边界

触发边界：存在任一可用委派通道即可触发；随后按任务类型进入相应路由：

1. 存在任一可用委派通道：`mcp__agent-switchboard__*` 工具，或宿主原生委派机制（如后台 subagent）；
2. 任务属于以下之一：跨模型委派（审查/实现/辩论）、受管长任务执行、监督或收取其他 agent 会话的成果、多窗口并行编排。

## 不适用场景

- 单会话可直接完成的小型或中型修改：不要为普通任务起 supervisor。
- 环境未安装 agent-switchboard 且也无原生委派通道：不要猜测工具名或要求用户临时安装，安装属于高风险操作，需用户明确授权。
- 纯只读问答：直接回答，不经 broker 绕道。

## 核心模式：管理者—执行者边界

- 会话管理者（你自己）只负责：定目标与阶段顺序、写完整派工提示词、审阅执行者证据、下返修指令、判定阶段是否通过、向用户汇报。
- 任务规模一律由 `task-mode-router` 判级，不由"我已经在做了"反推：判为中型及以上的动手操作（调查、读大量文件、编码、改配置、跑构建/测试/数据扫描、Git 提交）委派给受管执行者；判为小型的单会话修改可直接最小修改并验证。执行前记录所选路由与理由（写入派工单或 broker 记录）。
- 管理者允许做**有界、只读的独立验收**：复跑只读校验脚本、`git show`/`git diff --check`、读文件核对哈希/行号/输出。禁止实现、提交、扩大调查范围。
- 执行者自报的 PASS 不是验收依据；验收以独立证据为准（上述只读核验的结果）。
- 互不冲突的任务应主动并行多个受管窗口，无需用户提醒；存在同一文件或同一数据冲突风险的任务在同一窗口排队。
- 执行者窗口验收完成或确认不再需要后立即 `close_supervisor` / `stop_managed_claude_supervisor`，不得长期悬挂闲置窗口。

## 路由规则：确定性选择委派通道

按以下顺序判定，命中即停；执行前记录所选路由与理由：

1. **小型任务直接执行**：经 `task-mode-router` 判级为小型的单会话修改，不走任何委派，直接最小修改并验证。
2. **同厂劳动 native subagent 优先**：与当前会话同厂（同厂商/同宿主）的执行类劳动，优先使用宿主原生委派机制（如后台 subagent）。这不是"switchboard 失败后的降级"，而是 broker 自身要求的默认路由。
3. **异厂咨询/审查走 switchboard**：跨厂商模型的审查、评审、辩论、咨询，经 `route_agent_task` / `consult_*` / `queue_*_request` 走 broker。
4. **受管 Claude 长任务走 supervisor**：需要跨多轮、可归档续接的 Claude 长任务，用 `start_managed_claude_supervisor` 受管执行。
5. **逐级降级**：所需路由的真实调用失败时，才降级到下一可用通道（switchboard → 原生 subagent → 直接执行），并记录降级原因。可用性以**真实调用**为准：工具未出现在会话声明目录里不等于不可用（热重载可能迟注册），禁止凭目录清单下"无法使用"的结论。
6. **无可用执行者报 BLOCKED**：所有通道均不可用时，在验收报告中报 BLOCKED，说明已试通道与失败原因，不硬撑执行。

**用户成本偏好**：计费 token 与订阅额度并存时，在任务适配、真实可用性和授权边界均满足的前提下优先 MCP 路由（省钱）；不得以此绕过最小权限、认证失败停机或破坏性操作上报规则。

降级通道的能力差异要如实告知用户：宿主 subagent 没有 broker 的事件流、归档和跨会话续接能力；长任务可建议用户安装 agent-switchboard（安装属高风险操作，需明确授权）。

## 统一监督协议（2026-08-26 沉淀，业界对照联网验证）

> 受管 supervisor 与 DSH 会话（goal 模式）是**两套执行引擎，但应共用一套监督协议**——
> 业界共识（Langfuse/LangSmith/OTel/Temporal）：观测平台只负责记录，"每个执行器都必须
> 适配同一组事件与状态字段"，而不是为每个执行器发明一套监督方式。
> 来源：<https://langfuse.com/docs/observability/data-model>、
> <https://docs.langchain.com/langsmith/annotate-code>、
> <https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/gen-ai-agent-spans.md>、
> <https://github.com/temporalio/documentation/blob/main/docs/develop/go/activities/timeouts.mdx>

**三要素监督协议**（对任何执行者都检查这三项，不区分 executor_type）：

| 要素 | 受管 supervisor | DSH 会话（session-supervisor 插件） |
|---|---|---|
| ① 事件 | `wait_supervisor_event`（turn_completed/stall/error） | 会话事件流（turn/end、tool/call）+ 摘要注入 |
| ② 摘要 | broker `agent_events`（executor_type 区分来源） | 回合摘要注入（含思考行，deepseek 系） |
| ③ 超时兜底 | `stall_timeout_seconds` → stall 事件 | 插件回合内超时看门狗（turnTimeoutMinutes） |

**执行规则**：
- 监督任何执行者时，按 ①②③ 三项核对，缺哪项用对应机制补（supervisor 缺摘要→查 agent_events；DSH 会话缺超时→看门狗警告）；
- 事件统一落点：broker `agent_events` 表（`executor_type` 列：`cli`/`supervisor`/`session`/`subagent`）；
- 任务路由（execution 引擎二选一）：交互式/需要思考可见 → DSH 会话；重后台/需要独立进程硬兜底 → 受管 supervisor；监督接口两者一致。

## 工作流程：受管执行者生命周期

1. **启动**：`start_managed_claude_supervisor`，提供具体 `objective`、明确 `policy`（里程碑、安全红线、验收规则）、稳定 `supervisor_id`。默认 `decision_mode=record_only`，除非用户要求 Codex 决策。
2. **派工**：`send_to_managed_claude_session` 发送有界任务切片（一次一个可验收的增量），不发开放式大目标。
   - **验收口径开工前回显（2026-08-26 沉淀）**：凡任务涉及外部对照目标（如"对照某基准榜/公认值/参考实现"），派工提示词必须写明该目标**允许怎么用**（仅验收对照 vs 可作调参目标；可调参时注明约束：不要求一一对应、偏差上限、禁止照抄）并要求执行者在步骤 0 回显口径；**先开工后改口径 = 返工**。来源实证：2026-08-26 论文会话国际公认榜口径 16:14"仅验收"→16:18"可调参"翻转，中间按旧口径下发的任务需返工。
3. **追踪**：用 `wait_supervisor_event` 长轮询等待材料事件；进度可见性来自 wait 本身。禁止自建 cron 或轮询循环做监控。
4. **验收**：对照 objective 与 policy 独立核验证据，不接受执行者自述。
5. **关闭归档**：`close_supervisor` 写入归档摘要（做了什么、证据、风险、下一步），供跨会话续接。

### 生命周期强制收尾（看门狗兜底）

> **根因**：2026-08-24 会话 9 个 supervisor 在验收完成后仍悬挂（leaderboard-reground、impact-gold-rootcause-audit、taskflow-dashboard-update 等全部 `attention_required`、daemon+claude 存活）。"及时关闭"规则早已存在，缺的是执行拦截——人工"记得 close"不可靠。

**收尾不是靠记忆，是靠看门狗兜底**：

- **验收后立即 close**：验收通过或确认不再需要 → `close_supervisor` 归档摘要，这是验收流程第 5 步的自然延续。
- **启动时设 stall 兜底**：`start_managed_claude_supervisor` 必填 `stall_timeout_seconds`（300~600），超时无 token 自动产出 stall 事件供处置。
- **看门狗必须对用户可见**：启动长监督/跨轮等待时，必须在回复中报告「下一次检查触发时间」（精确到时分秒，含时区），不能黑箱等待；超时无事件则由 stall 事件接管，管理者不得静默循环。
- **回合结束自查一次**：每个 goal round / 长等待结束时，`list_managed_claude_supervisors` 检查本项目存活 supervisor；任务已完成但仍存活的立即 close；`attention_required` 的先收集最终结果再关闭。
- **stale 记录识别**：`daemon_alive=false` 但状态非终态（`stopped`/`failed`）的 supervisor 会带 `stale_uncollected: true`——daemon 已死无法回收，状态残留；出现时在 checkpoint 登记后清理状态记录，不让它永久残留。
- **返修轮次预算（防套娃，broker 强制）**：同一 artifact 的 review→repair 循环最多 **2 轮**（第 3 轮起被 broker 拒绝）。**实现方式**：每次 `route_agent_task` / `queue_cli_request` 派发同一 artifact 的返修时，必须传 `chain_key=<artifact 稳定 id>`（同一链同 key）；broker 对同一 chain_key 计数 ≥3 时直接拒绝（`chain_budget_exceeded`）。若收到该错误：停止该链，重新设计合同（或升级决策），并在验收报告记录 `repair_rounds`。参照 GitLab `retry:max`/Jenkins `retry(N)` 的收敛上限思想。
- **悬挂即处置，不留过夜**：任何 supervisor 若已无待处理命令且事件流停滞，即使本回合没有它的结果，也 `stop_managed_claude_supervisor` 并在 checkpoint 记录，由下一会话续接，而不是长期悬挂。

### 等待纪律：WAIT 与 GET 不得夹用（防轮询变体）

> **反模式**：2026-08-24 会话 `wait_supervisor_event`（180s）每次超时返回后立即夹一次 `get_managed_claude_supervisor`，形成 WAIT→GET 轮询循环，连续 44 分钟无看门狗、无用户可见检查时间。

- `wait_supervisor_event` 超时返回 ≠ 有事件：直接再次 wait（`since_seq` 推进到最新已知 seq），**禁止**在两次 wait 之间夹 `get_managed_claude_supervisor` / `list_managed_claude_supervisors` 查询；
- 只有 wait 返回了 material 事件（turn_completed / stall / failed / exited），才去 GET 详情或收结果；
- 长等待依赖 `stall_timeout_seconds` 的事件驱动兜底，而不是人工每 3 分钟查一次。

### 跨通道等待纪律总纲（防轻量状态查询轮询）

> **反模式**：2026-08-22 监督会话 pollCount=305（`request_status`×96、`list_agents`×265、`job_list`×15、`get_goal`×25）——监督者反复调用轻量状态查询工具"看进度"，而非转入单次长轮询。AGENTS.md 模块七/八已确立纪律，这是**规则确立后的执行回归**（见 evolution-inbox 提案 #1）。业界共识（AWS SQS Long Polling / LangGraph event streaming / Claude SDK streaming 等）：等待应靠"任务句柄 + 单次阻塞等待/事件流 + 超时恢复"，polling 仅限调试。

- **等待阶段唯一合法动作是单次长轮询**：派发 subagent / CLI 请求 / supervisor 后，等待结果只能用 `wait_supervisor_event` / `request_result(wait_seconds=60~120)` / `job_output(wait=true)` 单次挂起；
- **轻量状态查询仅限"首次确认请求存在"调用一次**：`request_status` / `job_list` / `list_agents` / `get_goal` / `get_topic_status` / `get_cli_requests` / `get_codex_requests` 等，仅在派发后第一次确认"请求已入队/已存在"时可调用一次；确认后必须转入对应的长轮询工具；
- **禁止把反复无 wait 状态查询当作等待策略**：连续 ≥2 次无 wait 的轻量查询即构成轮询反模式，会被 `scripts/evolution_scan.js` 检测并写入 evolution-inbox；
- **超时接管而非重查**：长轮询超时返回 ≠ 通道死亡——直接再次长轮询（推进 since_seq / 同一 request_id），或先查一次在途队列确认存在后继续长轮询；禁止切回短周期查询循环。

## 跨模型委派规则

- **模型档位与执行层解耦（统一 Provider 优先）**：
  - **禁止死板按厂商猜工具**：不要将 Gemini 绑定到 Antigravity，也不要将 OpenAI 模型绑定到 Codex CLI。任何注册在 Provider（如 CPA）或 CLI 中的模型均可通过 `route_agent_task(target_model=...)` 直接分发。
  - **执行层默认使用廉价工作马**：默认首选廉价档（如 `gpt-5.6-luna`、`gemini-3.7-flash`），两者互为热备；除非用户显式要求前沿档（sol/fable），否则禁止使用昂贵模型。
  - **网络检索/开放调研委托执行层**：凡需最新资料、论文检索或外网调研，禁止主会话直接调用 `web_search` 灌入脏网页，优先委托带搜索能力的执行层 Worker（如 `gemini-3.7-flash` via CPA）处理并回收提炼摘要。
  - **web_search 不可用时的标准通道（CLI worker 搜索）**：内置 `web_search` 工具（`web-search-deepseek` provider）需要 DeepSeek 官方 API key；未配置或调用失败时**不阻塞**，改用已登录的 CLI worker 联网搜索：`queue_cli_request(backend=codex_cli, target_model=gpt-5.6-luna, effort=medium, prompt="联网搜索…返回URL")` → 单次 `request_result(wait_seconds=120)` 回收。零新增成本、复用已有订阅额度；代价是 1~3 分钟延迟与结构化提示词约束。完整可复制模板见 `examples/web-search-via-cli-worker.md`。
- 审查/评审/辩论类任务优先派给当前最强模型（如 Codex 的 `gpt-5.6-sol` max 档），`mode=read-only`；评审意见作为返修指令来源。
- Gemini 路由：经 `consult_gemini` / `route_agent_task(target_agent="gemini")` 走 Gemini CLI 或 Gemini API；适用咨询类任务，与 Codex/Claude 同属异厂咨询通道。
- **权限默认最小**：broker 默认的受管权限模式是 `acceptEdits`，实现类委派先以默认最小权限启动；`bypassPermissions` 仅在用户明确授权且目标范围受控（有界目录、红线已写入 policy）时才升级使用。
- worker 拒绝执行有两类成因，分别处理：会话模式受限（落在"仅提供建议"的只读会话）→ 检查权限模式与路由，不要盲目升级权限；提示词缺少授权声明 → 在派工提示词开头补显式授权声明，模板见 `examples/delegate-implementation.md`。
- **遇到认证失败（凭据缺失/过期/配额鉴权错误）或被要求执行破坏性操作（删除数据、重置历史、覆盖未知产物）时，必须停止并上报用户**，不得自行升级权限或重试绕过。
- **调研派工必须极窄探针切片**：严禁向外部委派“大而全的宏大文献综述课题”；必须切片为 2~3 个生成耗时 <10 秒的极窄探针（单次 <100 字，结构化事实），5~10 秒极速回收。
- **多路结果共识直接锁定（Diff-Only）**：回收多路结果时，重合度 ≥80% 的共识事实直接采纳入库；严禁因次要格式差异全量重新调研，仅对单一实质冲突点发起微探针核查。
- 大证据用 `store_shared_context` 压缩传递，接收方按需 `retrieve_shared_context`，不要把完整转录粘贴进提示词。
- 排队类请求（`queue_codex_request` 等）用 `request_result` 长轮询收取，并在汇报中区分"请求的模型"与"实际应答的模型"。

## 已知陷阱与对策

| 陷阱 | 症状 | 对策 | 来源 |
|---|---|---|---|
| 权限模式误配 | 受管会话读项目根外文件时空转，等不到人工批准；或 worker 落在只读会话拒绝执行 | 默认用 broker 的保守默认 `acceptEdits` 启动；仅当用户明确授权且目标范围受控时才升级 `bypassPermissions`（受管窗口无人可点批准）；遇到认证类失败停止上报，不得自行升级绕过 | broker 实现依据（默认 `acceptEdits`）+ 来自 2026-08-18 生产复盘，本仓库无可复核测试 |
| git 写操作无人批准卡死 | acceptEdits 下 `git add/commit/tag` 触发人工批准请求，受管窗口无人可批 → 只能被迫升级 bypassPermissions | 优先用 `allowed_tools` 命令级白名单（如 `["Bash(git add:*)","Bash(git commit:*)","Bash(git tag:*)","Read"]`），引擎强制拒绝白名单外命令且无需人工批准；`bypassPermissions` 仅作最后手段 | 2026-08-24 生产复盘（leaderboard-source-freeze 卡死）；实现有单测覆盖 |
| memory 等无关 MCP 反复调用 | policy 文字禁止无效，模型仍尝试调用 `mcp__memory_server__*` | 只读/文件类任务启动时用 `mcp="none"` 硬禁用全部 MCP（`--strict-mcp-config` 空配置），工具不存在即不可能被调用；需要特定 MCP 时再显式放开 | 2026-08-24 生产复盘（两次 supervisor 均撞 memory）；实现有单测覆盖 |
| 客户端超时假死 | 大上下文请求被客户端掐断，但上游实际健康 | 为执行者客户端配置长超时（如 Claude 的 `API_TIMEOUT_MS=600000`），注意只对新进程生效 | 来自 2026-08-18 生产复盘，本仓库无可复核测试 |
| MCP超时与惊群重试 | 同步调用长任务触发 MCP 32001，误判通道死亡，连发多个新请求打瘫队列 | 耗时任务强制改用异步队列（`queue_*` 拿 ID）+ 单次 `request_result(wait_seconds=60~120)` 挂起；遇超时先查在途队列接管 ID，严禁重发或并发切换通道 | 2026-08 生产复盘与治理闭环 |
| 微小差异套娃核验 | 回收两路结果后因次要格式或模型标识微差推翻一切，再次拉 Subagent 全量重查 | 实行 Diff-Only 收敛门禁：共识部分直接锁定，仅对有实质冲突的单一事实/公式发微探针，禁止全盘重推 | 2026-08 生产复盘与治理闭环 |
| 上游配额耗尽 | 事件流反复 `api_retry` / `api_retry_exhausted` 且含 `rate_limit` | 报告用户并暂停，切换上游/接口后重试；禁止无限重试 | broker 实现/测试依据（supervision 事件流含 `api_retry_exhausted`） |
| 多窗口消息串线 | 中断一条消息时它可能已送达另一窗口 | 中断前确认目标窗口；返修时先核对提交归属再决定 reset | 来自 2026-08-18 生产复盘，本仓库无可复核测试 |
| 闲置窗口悬挂 | supervisor 完成但长期不关闭（2026-08-24 一次 9 个悬挂） | 验收通过即 `close_supervisor`，摘要归档进 topic memory；回合结束自查存活列表，悬挂即处置，见上文「生命周期强制收尾（看门狗兜底）」 | broker 实现依据 + 2026-08-24 生产复盘（9 supervisor 悬挂） |
| WAIT→GET 轮询变体 | `wait_supervisor_event` 每次超时后立即夹 `get_managed_claude_supervisor`，形成 3 分钟一次的轮询循环（2026-08-24 连续 44 分钟） | wait 超时直接再次 wait（推进 since_seq）；只有 material 事件返回才 GET 详情；长等待靠 `stall_timeout_seconds` 事件兜底 | 2026-08-24 生产复盘（10:08-10:52 无看门狗 Deep diving 段） |
| 管理者微观纠偏循环 | 同一执行者 2 次以上 interrupt 纠偏仍无效（memory MCP、Grep 参数、路径猜错），管理者反复救火 | 派工提示词一次性写死陷阱（`mcp="none"`、`allowed_tools`、OWN 绝对路径）；同一执行者第 2 次纠偏无效即停用，改走 Codex worker 或重写派工，不继续第 3、4、5 次 | 2026-08-24 生产复盘（8+ 次 interrupt） |
| 工具可用性臆断 | 声明目录里没有某工具就断言"物理上无法使用" | 先做一次真实调用，失败再降级；目录清单不是可用性证据（热重载可能迟注册） | 来自 2026-08-18 生产复盘（热重载迟注册），本仓库无可复核测试 |
| 省略模型档位 | 省略 `model_policy`/`effort` 的派工被路由到前沿档，悄悄烧额度 | 派工单必填显式档位；环境默认值（如 `set_model_default`）只是局部补丁，不作约束 | 2026-08-18 生产复盘，本仓库无可复核测试 |
| worker 越权改 git 状态 | 受管 worker 切换分支或动暂存区，管理者的提交落到非预期分支 | 派工红线显式禁止一切 git 写操作（含 checkout/switch）；提交前必查 `git branch --show-current` 与 `git status`；提交后核对远端实际落点 | 2026-08-18 生产复盘，本仓库无可复核测试 |

## 输出契约

派工时输出派工单；验收时输出验收报告：

```text
派工单：目标 / 边界与红线 / 授权范围 / 所选路由与理由 / 产物落点 / 验收标准 / 回报方式
验收报告：结论（PASS | PARTIAL | BLOCKED）/ 执行机制 / 收据 / 状态 / 独立核验证据 / 偏差与风险 / 下一步
```

- **执行机制**：实际使用的路由（switchboard supervisor / switchboard 队列 / 原生 subagent / 直接执行）。
- **收据**：该路由的产物标识——supervisor 为 `supervisor_id` 与归档摘要；队列为 `request_id` 与终态；原生 subagent 为其返回的最终报告；直接执行为改动文件清单。
- **状态**：该路由的终态（closed/stopped、completed/error/cancelled、子代理已结算、验证已通过）。

向用户汇报时按路由分支给出状态，不凭空估计进度：

- switchboard supervisor 路径：活跃 supervisor 列表及其状态（来自 `list_managed_claude_supervisors` 或 wait 返回）。
- switchboard 队列路径：排队请求终态（`request_result` 收取结果）。
- 原生 subagent / 直接执行路径：supervisor=N/A、队列=N/A，汇报子代理结算结果或直接执行的验证输出，**不要编造 broker 侧对象**。

## 安全边界与非目标

- 不修改用户级或全局 MCP/模型配置，除非用户明确要求。
- 不使用 `send_to_claude_session` 前台控制他人终端，除非用户明确要求驱动人工会话。
- 不抓取私人会话内容；快照走 `request_context_snapshot` 的本地授权通道。
- 不代替执行者写项目代码；管理者的写入仅限 broker 记录（`record_work_memory` / `record_agent_event`）。

## 验证方式

交接或收尾前完成以下可观察检查，按实际路由选择适用项：

**通用（所有路由）**：

1. 验收报告中的每条证据都可复核（路径、行号、哈希、命令输出）。
2. 所选路由与理由已记录；发生降级时降级原因已记录。
3. 无悬挂执行者、无未收取的结果、无管理者越权写入项目文件。

**switchboard supervisor 路径**：

4. `initialize` + `tools/list` 能连上 broker（新环境先冒烟）。
5. 每个启动过的 supervisor 都有终态：closed / stopped，且有归档摘要。

**switchboard 队列路径**：

6. 每个排队请求都有终态：completed / error / cancelled，结果已用 `request_result` 收取。

**原生 subagent / 直接执行路径**：

7. supervisor=N/A、队列=N/A；核验子代理最终报告或直接执行的测试/校验输出，不要求 broker 侧对象。

相关示例见 `examples/`。
