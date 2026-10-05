---
name: execution-discipline
description: 在 DSH 长程/多工具会话中强制九条执行纪律，防止高频反模式重演：禁止无 wait 轮询、禁止把门禁拒绝当交付物抛回决策、外部研究先探测通道再极窄探针、探查派子代理不肉身 Read、子代理派发带进度回报协议、回合结束零悬挂收尾、上下文预算（回合合并+结果落盘）。用于接手长任务、等待子代理/后台任务、发起外部研究、收到 INVALID/FAIL/PARTIAL 门禁结果、收到"重复工具调用"系统警告、需要读取多个源码文件或大文件，以及任何需要"执行层不空转、不惊群、不绕门禁"的执行场景。不用于单轮小修改或无需持久化的临时问答。
version: 0.3.0
triggers:
  - "接手/恢复长任务（.taskflow、goal、跨轮委派）"
  - "接手/交接项目（先跑接手一致性门禁，见下文专用节）"
  - "等待 subagent / 后台任务 / CLI 请求返回"
  - "发起外部研究、文献调研、跨模型长推理"
  - "收到门禁拒绝（INVALID / FAIL / PARTIAL）"
  - "收到重复工具调用系统警告"
  - "需要读取 ≥2 个源码文件或 >300 行大文件"
not_for:
  - "单轮小修改"
  - "无需持久化的临时问答"
depends_on:
  - task-mode-router
  - minimal-implementation
---

# 执行纪律（Execution Discipline）

> 本 skill 由一次真实长程会话审计（session-`<id>`）提炼而成。那次会话 13 小时、72 轮、12 次压缩、30 次无 wait 轮询、外部研究惊群空转约 90 分钟、多次把决策抛回用户，最终在 goal 8/8 耗尽时仍未完成。**这些错误全部有现成规则可依，缺的是执行时把它们当硬门禁。** 本 skill 把十条铁律固化为"执行点自查"，任何新会话在匹配场景下加载后必须逐条对照。

## 十条铁律

### 铁律一：等通知，不轮询（零轮询）

- 子代理 / 后台任务 / CLI 请求完成时，系统会**主动推送完成通知**，无需查询。
- 派发后本轮立即收尾结束，等通知进入下一轮。
- 确需确认请求存在时，`list_agents` / `job_list` / `request_status` / `get_cli_requests` **只允许调用一次**；确认后转入单次长轮询：`job_output(job_id, wait=true, timeout_ms=60000)`、`request_result(request_id, wait_seconds=60~120)`、`wait_task_receipt(receipt_path, wait_seconds=60~120)`、`wait_supervisor_event(...)`。
- **长轮询超时返回 ≠ 有事件**：`wait_supervisor_event` 180s 超时后直接再次 wait（`since_seq` 推进），**禁止**在两次 wait 之间夹 `get_managed_claude_supervisor` / `list_managed_claude_supervisors` 查询——WAIT→GET 夹用就是轮询变体（2026-08-24 曾连续 44 分钟）。
- **收到"重复相同工具调用"系统警告 = 必须立即改变策略**：先读上次结果，换参数/换工具/换方案，绝不在同一调用上再试。
- **等待期必须并行推进，禁止纯等（2026-08-26 沉淀）**：长轮询/等 CLI 结果期间，先列出"不依赖该结果的待办"并逐个执行（读产物、查未闭合项、推进其他 todo），再回到轮询；**同一回合内连续 ≥2 次 request_result/job_output 之间没有其他工具调用 = 空转信号**。来源实证：2026-08-26 论文会话 Turn 7 的 16 次调用中 9 次输出 <200 tokens 的纯轮询，38 分钟内 Top1000 归属等可并行项未推进。

### 铁律二：门禁结果是诊断信号，不是交付物（自主闭环）

- INVALID / FAIL / PARTIAL 意味着"继续修"，不是"可以交差了"。
- 收到门禁拒绝后先回答三个问题再决定下一步：**根因在哪（数据/构造/门禁本身）？修哪里能过？需要什么证据证明修好了？**
- **禁止**向用户输出"是否继续？/你怎么看 A/B/C？/待决策"这类抛回；只有存在确实不可自行裁决的方向分歧时才问，且一次问完。
- 措辞从"待决策"改为"我将继续做 X，因为 Y"。
- 用户写死的门禁（如"B/C 失败则停止"）**不允许**在执行端悄悄重定义语义；确需调整，必须显式向用户说明理由并获批。

### 遇阻自救三连（检查设计 → 联网搜索 → 真正推进）

接上一条：遇到任何问题、失败、门禁拒绝或"似乎无法继续"时，**不要记录阻塞或抛回用户**，默认按以下顺序自动推进，不添加人工环节：

1. **先检查设计**：追调用链、查门槛/终态，用证据判定是"实现问题"还是"机制缺口"（grep 入口、读源码、跑最小复现）。
2. **再联网搜索**：内置 `web_search` 不可用则走 CLI worker（`queue_cli_request`，显式 `target_model`+`effort`，极窄探针，结构化回收），对照业界做法。
3. **然后真正推进**：把诊断变成系统层改动（代码/门禁/机制）+ 回归测试 + 验证生效，而不是写报告或加文档规则。

三连做完前**禁止**记 blocked/BLOCKED；只有无可用工具、无替代路径、无新增证据且达到预算才算确认阻塞。难度/不确定性不是阻塞理由。

> 三连是 Recovery Ladder 的快速版；完整恢复路径、失败分类与停止裁决见下方「Recovery Ladder 与合法停止策略」（canonical，其他 Skill 的停止/恢复规则不得比它更宽松）。

## 自主执行契约（Autonomy Execution Contract，canonical）

所有执行类 Skill 共享同一运行语义。字段复用既有 artifact，**不新增第二套任务管理 SSOT**：

```text
INTENT                → goal objective / anchor.md Intent / 子代理契约 GOAL
DONE-WHEN             → anchor Done-when / 契约 EXIT / 验收标准
CRITICAL CONSTRAINTS  → anchor Critical Constraints / 契约 MUST PRESERVE·MUST NOT
NON-GOALS             → anchor Scope.Exclude / 契约 OUT OF SCOPE
AUTONOMY BOUNDARY     → clarify-before-change「意图解析策略」（什么必须问、什么自己定）
CURRENT STATE         → checkpoint.md / task-state.json / work_memory
NEXT BEST ACTION      → checkpoint 下一步（任何时刻有且仅有一个最优下一步）
VALID STOP CONDITIONS → 本节「合法停止策略」
```

**规则优先级（EXECUTION_RULE_PRECEDENCE，冲突时按此裁决）**：

```text
Safety / 不可逆授权
> 用户显式目标与约束
> 合法停止策略（Valid Stop Policy）
> 自主续接（"继续"= 已授权推进）
> 流程便利（任何流程规则不得成为提前停止或反复澄清的理由）
```

## Progress Delta 与 No-Progress Governor（canonical）

每个执行周期必须至少产生一种 **PROGRESS_DELTA**：

```text
DONE_CRITERION_CLOSED        闭合了一条 Done-when
MEANINGFUL_MUTATION          有实质内容的写入/修改（空 touch、无效改动不算）
BLOCKER_REMOVED              消除了一个通往 Done 的阻塞
DECISION_RESOLVED            一个影响后续动作的决策被拍定
NEW_ACTION_CHANGING_EVIDENCE 产生了改变下一动作的证据
```

以下**本身不算 progress**：重复读取、重复测试、再次总结、再次审计、生成没有决策作用的报告、同一搜索换措辞重复查询、再派一个 Agent 得到相同结论——除非它真正改变 next action 或 done state。

**NO_PROGRESS_STREAK**：连续动作无 Progress Delta 时，不得继续同类动作。必须：①重读 original objective；②判断当前动作是否缩短 Distance-to-Done；③改变策略；④优先执行可逆的具体动作。

**Retry 必须声明 WHAT_CHANGED**（query / tool / assumption / environment / implementation 至少一项变化）；没有任何变量变化 = 禁止 retry。不拿固定魔法轮次当唯一判定。

**Distance-to-Done Guard**：任何新增工作项必须满足至少一条——A. 闭合 Done Criterion；B. 移除通往 Done 的阻塞；C. 是 A/B 的必要前置。否则归类 OUT_OF_PATH，默认不执行。特别拦截：顺手重构、顺手 benchmark、顺手补文档、顺手研究相关技术、顺手优化非阻塞组件、顺手扩展架构——除非它成为真实 blocker。

## 证据充分即执行（EVIDENCE_SUFFICIENT，canonical）

调查和规划只服务于下一步执行。当已具备 objective / current state / target location / 可逆下一步 时，**必须进入 EXEC**。PREP 的退出条件不是"研究完整"，而是 `enough evidence to safely choose next action`。"还能再查更多资料"不是继续研究的理由。验证动作遵循 decision-gates 的 VERIFICATION_PURPOSE 预算。

## Recovery Ladder 与合法停止策略（canonical）

**Recovery Ladder**（任何失败按此爬升，最后一步强制）：

```text
Diagnose → Narrow Reproduce → Inspect Local Evidence → Search External Evidence
→ Alternate Route → Repair → Verify → RESUME ORIGINAL GOAL
```

修复子问题后**必须恢复** original objective 与被中断的 next action；禁止在子问题中无限优化（RECOVERY_WITHOUT_RESUME 是失败模式）。

**网络/外部信息失败**不自动等于 BLOCKED。先分类：`SEARCH_ZERO_RESULT / PAGE_UNAVAILABLE / AUTH_REQUIRED / RATE_LIMIT / TOOL_FAILURE / SOURCE_CONFLICT / UNKNOWN_TERM`，依次自救：改 query → 官方/primary source → GitHub → docs → 替代检索通道 → CLI worker → 更窄探针 → 缓存/本地源。仅当确需信息经所有可用通道仍无法获得、且缺失会阻止下一步，才可升级阻塞。

**工具失败一次不是 blocker**。先分类：transient / bad args / wrong tool / permission / auth / unsupported operation / environment / real system defect，选对应恢复路径。禁止同参数同工具反复调用。

**合法停止策略（Valid Stop Policy）**——主任务只能因以下五类停止，定义必须机器/流程可审计：

```text
DONE                                              所有 DONE-WHEN 闭合且有验证证据
TRUE_HUMAN_JUDGMENT_REQUIRED                      答案实质改变 objective/业务语义/互斥价值偏好，且无可自取证据通道
IRREVERSIBLE_OR_HIGH_RISK_AUTHORIZATION_REQUIRED  删除/全局写入/凭据/权限/外部系统且无显式授权
EXTERNAL_CAPABILITY_BLOCKER                       确需能力/信息经全部可用通道（替代工具/模型/本地缓存）确认不可得且阻止下一步
VERIFIED_EXHAUSTION                               Recovery Ladder 全程走完且预算耗尽，附尝试清单
```

**以下不是合法停止（Invalid Stop Reasons）**：complex / uncertain / test failed / tool failed once / source not found once / library unfamiliar / another agent failed / context getting long / PARTIAL / gate failed / 模型一时解不出 / "建议后续继续" / "需要进一步研究"。这些只能触发 Recovery / Replan / Continue。

**上下文逼近上限（CONTEXT_ANXIETY）不是停止理由**：必须 checkpoint → 持久化 current state → compact/reset → resume（利用 Project State / checkpoint / Memory / repair contract 恢复）。禁止因上下文变长主动降低目标、提前交付 partial、把剩余任务抛回用户。

### 铁律三：外部研究：先探测 → 极窄探针 → 单次接管（防惊群）

按顺序执行，缺一不可：
1. **先探测通道可用性**：`list_providers`（模型接口层：中转/登录态，如 CPA）与 `list_cli_backends`（前端 CLI 壳层，如 codex_cli/claude_code）**是两个不同抽象层，不是同级通道**：CLI 壳可任意匹配任意 provider 上的任意模型。探测时先确认"用哪个模型接口"，再确认"用哪个 CLI 壳去跑"，不要把它们并列成候选。确认目标通道真实存在且已配置，**再**发起请求。
2. **通道必须对照 `routing_preferences` 选**：按任务类型查偏好表（research/coding → cpa、codex_cli；fast/general → cpa），从偏好列表内选通道；选偏好之外的通道必须说明理由。**禁止**只凭"可用"就选。
3. **每次派发必须显式指定模型档位**：`queue_cli_request` / `route_agent_task` / `consult_*` 调用必须传 `target_model`（或 `model_policy`）与 `effort`，禁止只传 token_budget；省略档位 = broker 默认前沿档（最贵）。默认工作马档（`gpt-5.6-luna`），中档/前沿档须向用户说明理由。
2. **任务拆成极窄探针**：单次生成 <10 秒、Prompt ≤100 字、要求结构化输出事实；严禁"大而全的宏大综述命题"。
3. **异步提交**：`queue_cli_request` / `queue_codex_request` 拿 `request_id`，然后**单次** `request_result(wait_seconds=60~120)` 阻塞收取。
4. **超时不惊群**：MCP 超时（-32001）≠ 通道挂掉，Worker 仍在跑——先 `get_cli_requests` 查在途，再 `request_result` 接管；**严禁**同一时间并发切换 4~5 个通道。
5. **拿到足够证据立即收敛**：多路结果重合 ≥80% 部分直接锁定，只对单一差异点做一次定向核实，然后拍板；**严禁**证据已足仍反复核验。

### 铁律四：探查交给子代理，主会话只收摘要（Read-as-Execution）

- 需研读 ≥2 个源码文件 / 摸排调用链 / 排查旧实现 → 派探查 subagent（`subagent(run_in_background: true)`，轻量 Brief），主会话只回收 ≤5 行接入点摘要。
- 大文件（>300 行）先用 `grep` 锁定行号，再 `read(offset, limit)` 窗口读取；禁止全量。
- **禁止**用 `pwsh` 把大 JSON / 大表全量打印回主会话上下文（会引发压缩风暴、上下文丢失）。
- 一旦判定/声明为 `large` 任务，立即阻断本地文件探测/阅读/修改，下一动作只能是结构化 Brief + 委派。

**read 预算（2026-08-24 新增，防重复读取膨胀）**：同一会话对同一文件的**第 2 次读取**起，禁止再次全文 `read`——改用 `grep` 定位 + `read(offset, limit)` 窗口，或直接引用上下文已有内容（compaction 前读过的内容若仍需要，先确认是否已被压缩丢弃，再决定窗口读取而非全文重读）。单个 goal round / 任务回合内 `read` 调用 ≤5 次；超限的探查必须转交 subagent 做带结果摘要的只读扫描。来源实证：2026-08-24 daily_stock 会话同一 records.jsonl 全文重读 5 次、validation 脚本重读 3-4 次，55 分钟消耗 375 万输入 token、16 次压缩（含一次 15 连发）——重复读取是上下文膨胀与压缩风暴的第一来源。

**重复命令检测（2026-08-25 新增，可执行门禁）**：同一 `read` 目标 ≥3 次 / 同一 `pwsh`/`grep` 命令 ≥3 次 = 重复执行信号，必须先读上次结果再换参数/换方案。回合结束把本会话工具调用记录导出为 JSONL（每行 `{"tool": ..., "args": {...}}`），跑 `python <本skill>/scripts/flow_check.py --check-session <记录.jsonl>` 自检；FAIL 时禁止原样重跑同一调用。来源实证：inbox 审计 347 条 repeat/read-repeat 异常（read 39 / pwsh 34 / grep 26 / edit 24），为最大无质量代价浪费。

### 铁律五：派发带进度回报协议（防静默卡死）

- 派发 subagent 时要求：**步骤 0 先回报工作目录与沙箱探针**，之后每文件/每阶段回报，静默超 5 分钟必须主动报告。
- 同一任务重派前，先派一个最小 smoke test 验证通道真实可用；不要第二次派给同一个可能卡死的通道。
- 注意 subagent 有自己的沙箱临时目录（`$env:TEMP` 与 `%TEMP%\dsh-xxx` 不同），验证产物路径以 subagent 报告为准。

### 铁律六：回合结束零悬挂收尾（防执行者泄漏）

- 每个 goal round / 长等待结束时，**一次** `list_managed_claude_supervisors` 自查本项目存活执行者；任务已完成即 `close_supervisor` 归档，`attention_required` 的先收结果再关闭，事件流停滞无命令的直接 `stop_managed_claude_supervisor` 并在 checkpoint 登记续接。
- 队列类请求同理：本轮派出的 `request_id` 在结算前不得离开会话；结算后状态必须进入 completed / error / cancelled。
- **紧急打断必须登记恢复方向**：任何 interrupt / 停写 / 中止，先在 todo 保留 pending 项并写入 checkpoint"待恢复方向"清单，下一轮先处理该清单，不允许方向蒸发。
- **长监督必须挂可见看门狗**：启动跨轮等待时向用户报告「下一次检查触发时间」（精确到时分秒含时区）；等待期间依赖 stall 事件兜底，禁止静默 WAIT→GET 轮询循环。
- **微观纠偏上限 2 次**：同一执行者 interrupt 纠偏 2 次仍无效（工具误用、路径猜错、反复踩同一坑）→ 停用该执行者，改走另一通道或重写派工提示词（陷阱一次性写死：`mcp="none"`、`allowed_tools`、OWN 绝对路径），不允许第 3 次救火。
- 规则来源：2026-08-24 会话一次悬挂 9 个 supervisor（含 2 个已产出报告未归档、2 个失败态仍挂着）；"及时关闭"规则早已存在但无执行拦截。

### 铁律七：上下文预算——回合合并 + 结果落盘（防重载空耗）

> **根因**：2026-08-24 论文会话短回合模式（每 5-10 分钟一个 goal 回合）每小时消耗 166 万输入 token，其中大头是**每回合全量重载上下文**（系统提示 + skill 目录 + 历史），不是干活本身。省 token 的正确途径是降低单位工作的固定成本，不是少干活。

- **回合合并**：goal 回合之间"验证完就收回合"是浪费——把 2-3 个可独立推进的待办合并到同一回合处理，回合数降 60-70%，重载成本同比例下降，工作量不变。业界对照：OpenAI Batch API 批量提交思路。
- **结果落盘 + 摘要引用**：任何 worker/subagent/CLI 请求的结果，收取后**全文写 checkpoint/artifact 文件**，上下文只保留路径 + ≤5 行摘要；后续需要细节时窗口读取该文件，绝不把全文注入上下文。业界对照：Claude Code MEMORY.md（启动只加载摘要、按需读文件）。
- **禁止把大结果留在上下文**：收到大响应（>2KB）后，本轮用完立即落盘并删除上下文中的原文（通过后续只引用路径实现），防止膨胀到压缩阈值。
- **每回合自查**：回合开始前估算"本回合必须重载什么"——历史摘要够用就不要带全文；上一回合的临时结果本回合还要用 → 先落盘再引用。
- 规则来源：2026-08-24 论文会话 166 万/小时（回合重载为主因）+ 业界调研（LangGraph checkpoint / Claude Code memory / OpenAI Batch）。

## 铁律八：接手/交接先跑一致性门禁（防隐性不一致）

> **根因**：接手项目时，"基线数字漂移、状态登记失联、残留缓存失效、隐私红线突破、大文件入 git" 五类问题靠人翻文档核对必然漏检，靠文档约定必然复发。**根因是缺约束（无强制校验机制），不是人不够小心。**
> **来源案例**：novel-main 接手分析检出 AGENTS.md 基线 2940 vs 实测 3018 冲突、.taskflow/index.json 未登记活跃任务、pytest lastfailed 2 个失效 nodeid、工作区 12 条未跟踪研究产物。单仓手写脚本是临时方案（其他项目照样重犯），故沉淀为本 skill 通用门禁。

- **接手/交接/恢复长任务的项目，第一步先跑通用门禁**：`python <本skill>/scripts/takeover_check.py --root <项目根> [--config <项目配置>]`（纯标准库，只读，不改任何文件）。
- 门禁六项检查：**baseline-lock**（测试收集数 vs 合同锁）、**registry-consistency**（active 目录 vs 登记表 index）、**cache-stale**（lastfailed 失效 nodeid）、**privacy-tracked**（隐私红线路径入 git）、**oversized-tracked**（大文件入 git）、**workspace-hygiene**（未跟踪/分支，INFO）。
- 复制模板到目标项目 `scripts/` 并按项目配置隐私前缀/基线常量后，纳入该项目的"必跑检查"（AGENTS.md/README）——**流程层，观察执行**；同一问题复发即升级为 pre-commit hook（系统层）。
- **门禁报 FAIL = 诊断信号，不是交付物**：定位根因（数据/构造/门禁本身）→ 修机制 → 复跑至绿；既有实际问题（悬挂任务、残留清理、未提交产物）记录后留给处置，不混入机制修复。
- 门禁自身必须可自检：`takeover_check.py --selftest` exit 0 才可交付给项目（防门禁腐化）。

## 铁律九：检查时间声明必须绑定执行载体（防口头承诺）

> **根因**：目标会话自述"犯了一个执行错误：只在文字里报了'17:43:36检查'，但没有真正创建定时器或后台看门狗任务"。模型把偏好里的"报告下次检查时间"（可见性要求）当成了"完成监督"（机制要求）——报时是文本输出（零成本），创建定时器是执行动作（有成本），模型默认选了前者。**且该会话工具集根本没有 schedule 工具**——报时成了无载体承诺。

- **任何"将在 X 时间检查/监督"的声明必须绑定执行载体**，三选一：
  - 有在途任务 → 绑定 **`job id`**（`job_output(job_id, wait=true)` 阻塞等待）；
  - 有定时器工具（`dsh-schedule`）→ 绑定 **`schedule id`**（创建后回读确认）；
  - 无上述工具 → 绑定 **`goal round 自动触发`**（声明"下一轮 goal 唤醒时检查"——goal 轮次本身就是定时兜底）。
- **无载体声明 = 未执行**：检查时间写入回复前，必须先确认载体存在（job id / schedule id / goal 活跃）；只有文字没有载体的时间声明不得写入回复。
- **载体回读**：创建定时器/任务后，用 Describe/List/status 回读确认真实存在（Temporal Schedule 语义），不凭创建调用的成功返回自证。
- **看门狗三原则（2026-08-25 调研落地）**：
  1. **agent 内 sleep / 后台自睡 job 不算看门狗**（业界：LangGraph Cron/Temporal Timer/Step Functions Wait 的定时器都在**持久化状态机/服务端**，不是睡在 agent 进程里；"不要让 agent 自己 sleep 充当唯一调度器"）；
  2. **唤醒必须来自外部机制**：goal round 自动轮次（DSH 的 scheduler 等效）或 dsh-schedule 定时器——job 完成通知**不唤醒已结束会话**（Claude Code 结论：通知本身不启动 agent，需显式 `--resume`）；
  3. **分工分离**：job 负责"检查并产出结果"（如 Test-Path receipt → READY/PENDING），**goal round 负责"唤醒并消费"**（唤醒后 `job_output(job_id)` 取结果）——只有两者闭环才算看门狗。
- 反模式实证（2026-08-25）：目标会话派 9 个 `Start-Sleep 600` 后台 job（含检查逻辑），job 按时完成但会话 1.8h 后才回来——"为什么没有触发"= job 完成通知无法唤醒会话。
- 业界对照：OpenAI Structured Output（声明必须带 `status/resource_id/evidence`，缺证据拒绝 `scheduled=true`）；Temporal Schedule（create 后 Describe 回读）；"把承诺视为无效，只有可查询的资源 ID 与审计记录才算成立"。

## 铁律十：长任务结构化分阶段（防单会话无限膨胀）

> **根因**：超长任务单会话硬扛到底——inbox 审计显示 18 个会话单会话 input 超 500 万 tokens（最高 1623 万、701 steps），压缩后继续累积。业界实证（FastContext 实验）：探查/实现分阶段后 SWE-QA token 418k→210k（**-50%**），质量反而 **+0.7pp**——分阶段不降智，单会话硬扛才降智（上下文逼近窗口上限时注意力稀释）。

- **硬触发阈值**：单会话 >300 steps 或累计 input >500 万 tokens 时，**必须**分阶段或结构化交接，禁止继续累积。
- **结构化交接格式**（不复制完整轨迹——OpenAI Agents SDK / Handoff Debt 模式）：目标与约束 / 已确认事实（含文件路径与行号）/ 文件变更清单 / 测试结果 / 待办事项。交接只传这五类，禁止把父会话全文轨迹粘过去。
- **探查与实现分离**：仓库探索/调研类任务优先派探查子代理（轻量 Brief），只向主会话交接结构化定位结果；主会话直接做实现/决策。
- **压缩质量抽检**：每次自动压缩后，抽查摘要是否保留「任务目标 / 已做决策 / 未完成事项 / 关键证据」四类信息（Anthropic compaction 保留标准）；发现遗漏立即补记 checkpoint，防止压缩丢关键上下文后重做。

## 流程完整执行（防跳步，2026-08-24 复盘沉淀 + 升级为可执行门禁）

> **根因**：加载了方法论 skill 却跳过其步骤（尤其"有约束不执行"）是最高频复发模式。纯文字规则（流程层）已实证复发；按业界结论（Anthropic Building effective agents / OpenAI Harness engineering）升级为**可执行门禁（系统层）**：多步流程由程序化门禁强制执行，不靠提示词。
> **来源**：novel-main 接手分析跳第 4-6 步直接实施；复盘本身又跳"借鉴→决策门"；借鉴凭记忆编造出处（已联网核验 NASA AAR / Scrum.org / PMI / Agent Skills 官方机制后沉淀）。

- **可执行门禁（强制，不靠自觉）**：
  - `python <本skill>/scripts/flow_check.py --check-flow <流程记录.json>` —— 校验九步全、决策门已确认、借鉴含真实 URL；**FAIL 则禁止实施**（exit 1）。
  - `python <本skill>/scripts/flow_check.py --check-review <复盘.md>` —— 校验复盘含 NASA AAR 六段（预期→事实→差异→经验→行动→**验证闭环**）；缺闭环=复盘未完成。
  - `--selftest` exit 0 才可交付（防门禁腐化）。
- **流程记录契约**（`--check-flow` 输入）：九步 stage 名固定为 baseline→problems→root-cause→borrow→tradeoff→decision-gate→implement→verify→measure；`decision-gate.status` 必须 `confirmed` 且位于 implement 之前；`borrow.evidence` 必须含 http(s) URL（**编造来源比不借鉴更糟**，门禁直接拦截）。
- **落点三问**（任何"修根因"动作前，由流程记录 `root-cause`/`tradeoff` 证据承载）：①是否跨项目/跨对话？（→ 沉淀到 skill 层，不写单仓脚本）②现有 skill 是否已覆盖？（→ 复用/优化，不新建）③改动面积是否最小？（→ 落点正确优先于改动少）。
- **借鉴必须有真实来源**：外部机制一律先探测通道→极窄探针→回收带 URL 的结论（铁律三），然后写入流程记录 `borrow` 证据；**禁止凭记忆写"出处"**。
- **复盘本身也走完整流程**：产出复盘文件后必须过 `--check-review` 门禁，六段齐全（含验证闭环）才算复盘完成。

## 回合开始前自查（每次新 goal round / 长等待 / 大研究前，10 秒过一遍）

1. 我是不是在轮询？（→ 应等通知，最多查一次）
2. 我是不是又要问用户"要不要继续"？（→ 应自己定下一步）
3. 我要发的任务，通道查过吗？探针够窄吗？
4. 我读的文件是不是该交给子代理？（→ 同一文件第 2 次读？>300 行？本回合已 read ≥5 次？）
5. 我派出去的活儿，有进度回报协议吗？
6. 我是不是在重复调用同一工具？（→ 先读上次结果再换策略）
7. 上一轮派出的执行者/请求都收尾了吗？（→ 无悬挂、无未收结果；打断的方向已登记）
8. 本回合的重载成本算过吗？（→ 待办能合并到这一轮吗？要用的结果落盘了吗？上下文里还有大结果原文吗？）
9. 本会话超 300 steps / 500 万 input 了吗？（→ 必须分阶段结构化交接，见铁律九）

## 反面案例速查（本 skill 来源，遇到同类情况直接对照）

| 场景 | 当时的错误 | 现在该怎么做 |
|------|-----------|-------------|
| 等两个审计子代理 | 22 次 `list_agents` 无 wait，被系统警告后仍继续 | 派发后结束本轮等通知；至多查一次 |
| 4 作者 pilot 得 INVALID | 输出"门禁正确拒绝"+"待决策：是否继续？"，用户批评"你不是来拒绝的，你是来解决问题的" | 定位根因（碎情境键→数据现实→作者选择）自主迭代 |
| 外部研究两轮 | 未探测通道就把请求发给未安装的 Antigravity CLI / 未配置的 Gemini，MCP 超时后并发换 4~5 个通道，证据足够仍重复核验 | 先 `list_providers`；极窄探针；单次 `request_result` 接管；共识直接收敛 |
| 通道选型错误 | research 任务硬选 `claude_code`（偏好是 cpa/codex_cli），且未传档位触发前沿档 | 派发前先查 `routing_preferences` 按任务类型选通道，再显式指定 `target_model`+`effort` |
| 省略档位派发 | `queue_cli_request` 只传 token_budget 没传 target_model/effort，broker 默认路由到前沿档（最贵） | 每次派发必填 target_model（或 model_policy）与 effort；禁止只传 token_budget |
| 内置工具失败误当通道问题 | `web_search` 报 "Insufficient Balance" 被说成"通道余额不足"，与 switchboard 通道混淆 | `web_search` 是 DSH 内置工具，余额独立于 switchboard；失败就写"内置 web_search 余额耗尽"，另走已实测可用的 `queue_cli_request`（codex_cli/cpa）通道 |
| Phase 1C 子代理返回乱码 | 未重新派发、未报告，直接重定义门禁语义继续 | 结果不可读 = 未完成 = 重新派发或主会话直接核查 |
| v8 实施子代理 | 5 小时静默无产出，三次重派仍失败，goal 8/8 耗尽 | 派发时带进度回报协议；重派前 smoke test 通道 |
| 主会话读 3 个源码文件 + 260KB JSON | 肉身全量 Read，触发 12 次上下文压缩 | 派探查子代理；grep + offset/limit 窗口 |
| 2026-08-24 九 supervisor 悬挂 | 验收完成后未 close：9 个 `attention_required` 存活（2 个已出报告未归档、2 个失败态仍挂），管理者全程无回合级自查 | 铁律六：回合结束一次 `list_managed_claude_supervisors`，任务完成即 close、attention 先收结果、停滞即 stop 并登记续接 |
| 2026-08-24 44 分钟无看门狗 Deep diving | WAIT→GET 轮询循环（10:08-10:52），连续 44 分钟未向用户报告检查时间，依赖 180s 人工长轮询而非 stall 事件兜底 | 铁律一：wait 超时直接再次 wait，禁止夹 GET；铁律六：长监督必须报告下次检查时间，依赖 stall 事件兜底 |
| 2026-08-24 微观纠偏超限 | 同一执行者 8+ 次 interrupt 纠偏（memory、Grep、路径），但管理者未停用，持续救火 | 铁律六：2 次纠偏无效即停用，换通道或重写派工（陷阱一次性写死） |
| 2026-08-24 派工陷阱未模板化 | 执行者反复误用 memory MCP、Grep 非法参数、OWN 路径误写 `.taskflow/`、reference 路径猜错，管理者 8+ 次 interrupt 纠偏 | 派工模板固化：`mcp="none"` 硬禁用、OWN 绝对路径写前 glob 确认、reference 以 receipt 登记字段为准、BLOCKED 结构化 |
| 2026-08-24 打断方向丢失 | 320 合同设计被 provenance 紧急事件打断后未恢复，方向蒸发 | 紧急打断必须登记"待恢复方向"到 todo+checkpoint，下一轮先处理 |
| 2026-08-24 三步连跳（novel-main 接手） | 跳第 4 步（借鉴）、第 5 步（取舍）、第 6 步（决策门）直接实施单仓脚本；"借鉴"凭记忆编造来源 | 第 6 步未确认不进实施；落点三问：跨项目→skill 层；借鉴先联网搜索拿真实 URL |
| 2026-08-24 复盘又跳步 | 复盘走到"错误清单→根因"后，跳"借鉴→决策门"直接到"机制化修复"，且方案是约定层（"下次注意"） | 复盘走完六段（NASA AAR 标准），借鉴必须真实来源，决策门必须展示确认，最后一环"后续验证闭环"不可跳 |
| 2026-08-24 约束层标注错误 | 把 SKILL.md 文字规则标注为"系统层"（实际是流程层，触发时注入非常驻） | 引用 Anthropic Agent Skills 官方文档确认加载机制后，正确标注约束层：可执行脚本=系统层，SKILL.md=流程层 |
| 2026-08-25 单会话硬扛到底 | inbox 审计 18 个 token 热点会话（最高 input 1623 万 / 701 steps），压缩后仍累积，不做分阶段 | 铁律九：>300 steps / >500 万 input 必须结构化分阶段交接（FastContext 实证 -50% token 且质量 +0.7pp） |
| 2026-08-25 重复工具调用堆积 | 347 条 repeat/read-repeat 异常（read 39 / pwsh 34 / grep 26），同一文件反复读、同一命令反复跑 | 铁律四重复命令检测：同目标/同命令 ≥3 次跑 `flow_check.py --check-session` 自检，先读结果再换策略 |
| 2026-08-26 纯轮询空转 | 论文会话 Turn 7 的 16 次调用 9 次输出 <200 tokens（request_result 反复轮询 38 分钟），Top1000 归属等可并行项未推进 | 铁律一等待期并行：轮询间隙必做不依赖该结果的待办；连续 2 次轮询无其他调用即空转 |

## 业界对照验证（2026-08-22 web 研究回收，与十条铁律一致）

| 铁律 | 业界做法 | 来源 |
|------|---------|------|
| 一 等通知不轮询 | Anthropic Agent Teams mailbox：子代理 `SendMessage` 主动投递，主代理无需轮询 | <https://code.claude.com/docs/en/agent-teams> |
| 三 防惊群 | 指数退避：LangGraph `RetryPolicy` / CrewAI `max_retries`；在途接管：LangGraph Durable Execution | <https://docs.langchain.com/oss/python/langgraph/use-graph-api#add-retry-policies> / <https://docs.langchain.com/oss/python/langgraph/durable-execution> |
| 三 熔断 | Circuit Breaker 模式：连续 N 次失败后快速失败、冷却后重试（框架多需外置） | <https://learn.microsoft.com/azure/architecture/patterns/circuit-breaker> |
| 四 上下文 | auto-compact（Claude Code）/ LangGraph checkpoint（按 thread_id 恢复）/ Mem0·Zep 结构化记忆 | <https://code.claude.com/docs/en/how-claude-code-works> / <https://langchain-ai.github.io/langgraph/concepts/persistence/> / <https://docs.mem0.ai/migration/platform-v2-to-v3> / <https://help.getzep.com/v2/memory> |

**熔断补充（业界有、本 skill 此前缺）**：同一工具/通道**连续失败 3 次**即熔断——停止重试、记入 checkpoint、切换方案或等待冷却后再试；严禁在同一通道上无限退避重试。与铁律一"收到重复调用警告立即换策略"联动。

## 与相邻 skill 的分工

- `decision-gates`：决策层不跑偏（checkpoint 证据锚、对抗审计、成本比对）——管"决策正确性"。
- 本 skill：执行层不空转（零轮询、不惊群、不绕门禁、不肉身读、不静默派发）——管"执行纪律"。
- 两者可叠加使用：长任务先按本 skill 自查执行姿势，再按 decision-gates 落 checkpoint。
