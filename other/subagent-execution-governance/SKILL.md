---
name: subagent-execution-governance
description: 把子代理派发从"监督型治理"升级为"契约型治理"：探查/实现/验证角色分离、契约快照（含负空间）、三级有界读取、单写者文件所有权、行动门槛替代轮次门槛、结构化 BLOCKED、token/工具/轮次预算、结构化结果回收与 repair-contract 恢复。用于派发实现型子代理（写代码/写文件类任务）、设计"谁读什么/谁写什么/何时算阻塞"的执行协议、审计子代理空转（反复探查不产出、并行写冲突、上下文膨胀）、或复盘"子代理烧了大量 token 却没产出"的会话。不用于纯问答、单轮小修改、或已有成熟任务流程的普通委派。
version: 0.2.0
triggers:
  - "派发实现型子代理（需要写文件/写代码的任务）"
  - "设计或评审子代理执行协议（读边界/写所有权/退出条件）"
  - "子代理反复探查不产出、空转、静默超时"
  - "多个子代理并行写同一批文件导致冲突"
  - "子代理会话 token 消耗异常膨胀（如输入数十万 token 无产出）"
  - "复盘长会话：审计子代理模型、token 消耗与纪律执行"
not_for:
  - "纯问答或单轮小修改"
  - "已有成熟流程的普通委派（无需重设计）"
  - "只查子代理用了什么模型（直接用会话日志 request/header 事件即可）"
depends_on:
  - task-mode-router
  - execution-discipline
  - minimal-implementation
---

# 子代理执行治理（Subagent Execution Governance）

> 本 skill 由一次真实实现会话审计（session-33b69ec9-1abf-454d-9555-f2d4031a9453）提炼而成。那次会话 3 小时、17 个子代理、执行层消耗 309 万输入 token（主会话 4 倍），`b21b9211` 一个子代理读了 65 个文件后仍被催"直接实现"，主会话被迫 28 次 `send_message` 催促 + 8 次 `interrupt_agent`，最终目标未 complete、会话中途悬死。**根因不是"监督不够凶"，而是子代理的工作边界、信息边界、写权限和退出条件没有工程化。**

## 核心原则

> 不要从"自由探索"直接走向"实现代理完全失去自主权"；正确形态是 **契约驱动 + 有界自治 + 结构化升级**。
>
> 目标不是"主代理不断管子代理"，而是 **系统规则让正常子代理根本不需要被管**。

失败因果链（本 skill 要打断的）：

```text
任务设计错误（探查/实现不分）
  → 执行边界过宽（无限读取授权）
  → 监督不得不频繁介入（催促/中断/重派）
  → send_message / interrupt 注入上下文
  → 上下文继续膨胀 → 缓存命中率恶化 → token 爆炸
```

## 一、角色分离（Discovery → Contract → Implementation → Validation）

禁止让一个子代理同时承担"先研究、再实现、再测试"四种认知模式：

| 角色 | 读 | 写 | 产出 |
|------|----|----|------|
| **Discovery**（探查） | 自由只读 | 禁止 | 契约快照草案（≤15 条 file:line 事实） |
| **Contract Builder**（主会话） | 验证契约 | 写契约文件 | 最终契约快照（含负空间） |
| **Implementation**（实现） | 有界读取（三级） | 只写自有文件 | 代码 + 变更清单 + 状态 |
| **Validation**（验证） | 只读目标文件/测试 | 禁止（或只改测试） | 测试结果 + 差异报告 |

**主会话承担 Contract Builder 与 Orchestrator**：探查结果必须经主会话验证、确认文件无冲突、写入契约快照后，才能派实现子代理。**禁止**探查子代理直接产出实现任务。

## 二、契约快照（Implementation Contract）

每个实现子代理派发前必须有一份契约快照，包含**正空间和负空间**：

```text
GOAL:           一句话目标（可验收）
OWN:            本子代理独占写入的文件（单写者）
MAY READ:       自动允许读取的文件/目录白名单
REFERENCE:      参考实现文件（读但不改）
IN SCOPE:       允许做的事
OUT OF SCOPE:   禁止做的事（防 scope creep）
MUST PRESERVE:  必须保持不变的现有行为/API
MUST NOT:       禁止触碰的模块/文件/顺手重构/兜底路径
EXIT:           完成条件（确定性可判）
BLOCKED:        允许升级阻塞的场景（仅限契约外信息缺失）
```

负空间（OUT OF SCOPE / MUST NOT）是防"模型顺手优化"最有效的手段，**必须有，且比正空间更具体**。

## 三、读取策略：三级有界读取（不是"只写不读"）

实现子代理不自由探索仓库，但保留必要自治——**三级读取权限**：

```text
Level 0 — 自动允许（无预算消耗）
  目标文件、契约快照、指定参考实现、直接测试文件

Level 1 — 有预算的自主读取（最多 N 个额外文件，需带 reason code）
  API_SIGNATURE_UNKNOWN       类型/签名未知
  TEST_EXPECTATION_UNKNOWN    测试预期未知
  TYPE_DEFINITION_REQUIRED    需要类型定义

Level 2 — 需要升级（禁止自主执行）
  跨模块架构探索、repo-wide grep、超过预算、发现契约错误
  → 走结构化 BLOCKED，不自行扩大范围
```

**不要把读的决策权全部收归主会话**（会变成"主代理当 I/O 调度器"的 ping-pong）；也不要完全放开（会回到无限探索）。Level 1 的 reason code 让升级可观测、可审计。

## 四、写入所有权：单写者文件所有权

```text
一个文件在同一时刻只有一个 writer owner。
```

- 共享文件：禁止两个子代理同时写；由主会话（或专门的 integration agent）最后统一修改。
- 派发前主会话必须做**文件级冲突检查**：把每个实现子代理的 OWN 集合求交，交集为空才并行。
- 并行写冲突（"目标文件已被父代理并行更新"）是调度错误，不是模型错误——重派前先改派发拓扑。

## 五、进度状态机（替代"催促"）

实现子代理**只允许**处于以下状态：

```text
IMPLEMENTING    工作中（每阶段报告当前状态与产出物）
MUTATED         已完成首次有效写入（重点信号）
BLOCKED         结构化阻塞（见下）
DONE            完成，附验证证据
FAILED          失败，附原因
```

**没有 `STILL_EXPLORING` 状态，也不存在无限期的 `STILL_RESEARCHING`。** 正常协议里几乎不存在"催促"——orchestrator 不靠"你做好了吗/赶紧实现/不要再读了"判断执行状态，而是看状态机与资源观测。

**探查充分即停（EVIDENCE_SUFFICIENT）**：证据已足以安全选择下一动作时必须停止读取、进入 MUTATE 或结构化 BLOCKED；"还能再查更多"不是继续探查的理由。每个报告周期必须带 Progress Delta（DONE_CRITERION_CLOSED / MEANINGFUL_MUTATION / BLOCKER_REMOVED / DECISION_RESOLVED / NEW_ACTION_CHANGING_EVIDENCE，见 execution-discipline）；无 delta 的重复读取/重复测试不算进展。

空转判定（替代"催两次就判空转"）：连续 K 个有效动作窗口内 `mutation_count = 0` 且 `discovery_budget` 耗尽 → 自动判定 `STALLED`，由 watchdog（观测通道）触发，不是人工催促。

## 六、行动门槛（替代"第 N 轮必须建文件"）

轮次门槛会产生 Goodhart（先 touch 一个空文件满足 KPI 再继续探索）。改用**行动门槛**：

```text
在 exploration budget 耗尽之前，必须发生以下之一：
  A. 第一处有效代码修改（mutation）
  B. 返回 BLOCKED(reason, exact_missing_information)

禁止第三种状态："继续研究。"
```

实现子代理在首次 mutation 前，允许读取目标文件、契约参考文件、最多 K 次 Level-1 额外查询；预算耗尽而未 mutation 即 STALLED。

## 七、结构化 BLOCKED（防止"无限问主代理"）

BLOCKED 必须是结构化异常，不是自然语言求助。**有效性门禁：缺任一关键字段 = `BLOCKED_INVALID`，orchestrator 不接受停止**：

```text
BLOCKED:
  blocked_reason:                一句话阻塞原因
  why_it_blocks_done:            为什么它阻止 Done Criterion 闭合
  evidence:                      已收集的证据（含已查文件/命令/输出）
  recovery_steps_attempted:      已尝试的恢复步骤（Diagnose/Reproduce/Local/Search/...）
  alternative_routes_attempted:  已尝试的替代路径（换工具/换通道/换假设）
  what_external_fact_is_missing: 缺失的外部事实（精确到签名/字段/配置项）
  why_agent_cannot_obtain_it:    为什么自己无法获得（所有可用通道均已排除的证据）

# 兼容简写：missing_fact≈what_external_fact_is_missing，why_required≈why_it_blocks_done，
# already_checked≈evidence，requested_context≈希望 orchestrator 补充的上下文
```

orchestrator 收到 BLOCKED 后，**先按五级阶梯自行解决，不得直接转发用户**：

```text
1. 自己补 context（把缺失信息补进契约 / 直接回答）
2. 派 narrow discovery probe（极窄只读查询）
3. 换 alternate tool / channel / model
4. 创建 repair contract（只处理失败点）
5. 修订本地执行计划（任务设计错误 → 终止并重设计）
```

五级阶梯走完且符合 execution-discipline「合法停止策略」五类之一，才可向用户报告；否则继续推进。**禁止**随手回 `send_message("继续看看")`。

## 八、资源预算（必须存在且可观测）

"不要无限探索"必须转成机器可判断的资源约束：

```text
Discovery：    ≤ 12 次 repo read/search，≤ 2 个 agent turns
Implementation：首次写入前 ≤ 6 次工具调用；额外探索 ≤ 4 次
Validation：   只允许 test / lint / targeted read
```

具体数字按任务调整，关键是：**预算必须存在、写入派发 prompt、并在会话纪律体检时可见**。

## 九、上下文回收：结构化结果 only

**工作历史不进入 orchestrator 的活动上下文。** 子代理完成/报告时只回：

```text
Agent A DONE
Changed:    [foo.ts, foo.test.ts]
Validation: 17/17 passed
Deviations: none
Blocker:    none
Details:    artifact://agent-A/report
```

**报告体积硬约束（≤500 词，业界 LangChain Deep Agents 值）**：最终报告正文 ≤500 词；原始数据（完整日志、表格、证据）一律写文件，Details 只给路径。超长报告不得 splice 回主上下文——体积保护层配合前缀缓存保护，结构性防炸（实测：大量 inbox/spliced 注入与单步 204,869 输入 token / cache=0 高度相关）。

**派发类别标注（[PREP]/[EXEC]，准备-执行平衡）**：每次 subagent 派发的 `description` 必须以 `[PREP]`（调查/审计/验证/合同）或 `[EXEC]`（实现/构建/运行/修复）开头；同一轮次内 `[PREP]` subagent 数量达到 6 个且 `[EXEC]` 为 0 时，必须停止派发调查类 subagent，先派一个 `[EXEC]` 动作（准备压倒执行是复发反模式，2026-08-25 实测：单日 19 个 subagent 全部为调查类、codex 派工 0 个 implementation，用户两次发火）。此约束为流程层，系统层插件版（自动计数拦截）待开发。

禁止把子代理的完整工作过程（大量探查日志、多轮内部推理）splice 回主上下文。这是缓存保护的**结构性**方案，不是"少发几次消息"。多次大规模 splice 会杀死前缀缓存（实测单步 204,869 输入 token 且 cache=0 与大量 inbox/spliced 高度相关）。

## 十、恢复：checkpoint + repair contract（失败不重派全新 agent）

```text
真实状态 ≠ chat history

任务状态存盘：
  task-state.json          # 当前阶段、状态机、预算消耗
  implementation-contract.md
  completed-work.json      # 已完成文件与验证
  validation-report.json

失败路径：
  FAIL → 创建 repair contract（只处理失败点）→ 派实现
  而不是：重派全新 agent 重新理解仓库
```

主会话即使中断，新的 orchestrator 也能凭存盘状态继续，不从零重放。

## 十一、模型路由（排最后，且不是省钱主杠杆）

模型选择是最后一道配置，不是治理手段：

- Discovery/Validation：便宜高速档（如 `gpt-5.6-luna-max`）
- Implementation：工作马档（如 `gpt-5.6-terra`）
- Orchestrator/决策：前沿档（如 `gpt-5.6-sol-xhigh`）

**经验证据：设计不良的任务，用再便宜的模型也能烧掉 300 万 tokens。** 任务设计正确优先于模型省钱。

## 十二、派发协议清单（每次派实现子代理前过一遍）

1. 契约快照存在？含负空间（OUT OF SCOPE / MUST NOT）？
2. OWN 文件与并行子代理无交集？（单写者）
3. 读取白名单 + 三级权限写清楚了？
4. 预算（工具调用/探索次数/token）数值化并写入 prompt？
5. 行动门槛（mutation 或 BLOCKED，二选一）？
6. 状态机字段（IMPLEMENTING/MUTATED/BLOCKED/DONE/FAILED）要求回报？
7. 结果回收契约（只回结构化摘要，不回工作过程）？

## 与相邻 skill 的分工

- `execution-discipline`：执行层五条铁律（零轮询、不惊群、不肉身读、派发带进度回报）——管"执行纪律"，本 skill 是其**实现型任务的深化协议**。
- `decision-gates`：决策层不跑偏（checkpoint 证据锚、成本比对）——管"决策正确性"。
- 本 skill：**契约型治理**——管"子代理工作边界、信息边界、写权限和退出条件的工程化"。三者可叠加：先按 execution-discipline 自查执行姿势，再按本 skill 出契约，最后按 decision-gates 落 checkpoint。

## 反面案例速查（本 skill 来源）

| 场景 | 当时的错误 | 现在该怎么做 |
|------|-----------|-------------|
| 实现子代理空转 | `b21b9211` 2 轮读 65 文件、grep 30 次、941K tokens 后仍被催"直接实现" | 契约快照 + 三级读取 + 行动门槛：首次写入前 ≤6 次工具调用，无 mutation 即 STALLED |
| 并行写冲突 | 多个子代理并行写同一文件包，`b21b9211` 报告"目标文件已被父代理并行更新" | 派发前文件级冲突检查：OWN 集合求交为空才并行 |
| 催收式管理 | 主会话 28 次 send_message + 8 次 interrupt_agent，双方 token 叠加膨胀 | 状态机 + 结构化 BLOCKED + watchdog 判定，正常路径无催促 |
| 上下文撑爆缓存 | 169 次 inbox/spliced 注入，单步 204,869 输入 token 且 cache=0 | 结构化结果回收：只回 status/changed/validation/blocker/artifact ref |
| 目标中途悬死 | 第三个 goal 未 complete，会话停在 open step | checkpoint 存盘 + repair contract 恢复，不从零重放 |
| 便宜模型不等于省钱 | 执行层 309 万输入 token（luna-max），是主会话 4 倍 | 任务设计正确优先于模型省钱；模型路由排最后 |
| Workflow 全量返回 null / 秒崩 | 凭直觉硬编码未准入模型 `model: 'gpt-5.6-luna'`，缺少 pre-flight 与结构化捕获 | 采用逻辑角色映射 + Pre-flight 验证 + 结构化返回 + 受控 Fallback 政策 |

## 十三、Workflow 批量子代理编排与模型路由契约

在使用 `workflow` 工具（基于 JavaScript 沙箱的多子代理并发/流水线编排）时，必须遵守以下四层防崩契约：

```text
┌────────────────────────────────────────────────────────┐
│ 1. 逻辑角色先行（Logical Roles First）                  │
│    - 默认使用逻辑角色：                                  │
│      * subagent_default   -> cpa/gemini-3.7-flash-high │
│      * cheap_executor     -> cpa/gpt-5.6-luna-max      │
│      * strong_reviewer    -> cpa/claude-sonnet-4-6     │
│      * frontier_architect -> cpa/gpt-5.6-sol-xhigh     │
│    - 禁止凭自然语言猜测未经验证的具体模型 Slug           │
├────────────────────────────────────────────────────────┤
│ 2. Pre-flight 预检（Fast Failure Before Spawning）     │
│    - 在启动并发子代理前，核对模型是否在 DSH settings 声明 │
│    - 确定性配置错误必须在启动前一次性拦截，禁止生成一批 null│
├────────────────────────────────────────────────────────┤
│ 3. 显式受控 Fallback 政策（禁止静默换模型）              │
│    - 仅允许 routing-policy 明确声明的 Alias 映射       │
│    - 每次 Fallback 必须记录原请求、实际模型、reason_code│
│    - 无声明规则时必须 Fail Closed 阻断                 │
├────────────────────────────────────────────────────────┤
│ 4. 聚合层校验与自愈（Aggregator Guard & Self-Healing） │
│    - 校验结果数量、至少一个成功、必填字段非空             │
│    - 全失败时自动诊断根因并重析重试，不把修改工作甩给用户  │
└────────────────────────────────────────────────────────┘
```

## 工具化支撑（P1/P2 落地物）

本 skill 附两套运行时工具，让治理从"靠 prompt 自觉"变成"可观测、可执行"：

### P1 用量观测插件（subagent-usage-observer）

动态 Cordis 插件（Host 端），注册两个工具：

- **`subagent_usage`**：输入子代理 session id → 输出 tokens(input/output/cacheRead)、models、preset、toolCallsCount、mutationsCount、turns、steps。数据源 `sessionQuery.readSession`，只读。
- **`subagent_stalled_check`**：基于预算约束（mutationBudget 默认 1 / toolBudget 默认 6 / turnBudget 默认 3）保守判定：成功的 edit/write 结果达到预算 → `MUTATED`；检测到四字段结构化报告 → `BLOCKED`；工具行动预算或轮次兜底预算任一耗尽且无 mutation/BLOCKED/潜在写入工具 → `STALLED`；命令或委派可能写入但日志无法证明时保持 `IMPLEMENTING`，避免假阳性。

用途：替代"催 2 次判空转"的轮次拍脑袋。watchdog 用工具调用数与 mutation 事实判定，不靠催促。

### P2 splice 摘要化插件（subagent-splice-summarizer）

动态 Cordis 插件（Host 端），监听 `agent/pre-step` waterfall：

- 对进入步骤的 `source.kind === 'subagent-report'` 消息，若文本超 8000 字符，替换为结构化摘要（保留 status/changed/validation/deviations/blocker/artifact 各节前几行，其余截断；无结构字段的走首尾截断）。
- 目的：阻断超长子代理报告全文 splice 回主上下文，保护前缀缓存。非 subagent-report 消息与短报告不动。

注意：**这是体积保护层，不是缓存银弹**。A/B 实验（`scripts/splice-ab-experiment.js`）实测：审计会话 117 条注入共 ~55K tokens（仅占总输入 7%），摘要化仅省 2.6%——真正的大头是每步前缀重复（169 次注入/单步 204K 输入/cache=0）。所以 P2 的价值是"结构性防炸"（极长报告不会一次塞爆），缓存命中率仍需 A/B 重放实测。

### 体检脚本（scripts/）

- `session-discipline-audit.js <session id|zstd 路径>`：完整纪律体检（模型路由、每轮 token、子代理清单、催收成本、cache=0 异常、短轮询、全量读风险）。
- `splice-ab-experiment.js <session id|zstd 路径>`：A/B 体积对比（全量注入 vs 摘要化的字符/token 节省，按轮聚合，top 条目前 5）。

两个脚本均 Node ≥22（`node:zlib` 内置 zstd），支持直接传会话 ID 自动定位。
