---
name: laohan-bianpai
version: "1.23.0"
description: 真人口播工作流编排器。根据 episode 已落盘产物识别当前步骤、验证前置 gate，并给出唯一下一步与对应 skill；不替代创作、剪辑、发布或复盘。Use when 用户说工作流下一步、检查本期进度、编排这期视频、当前做到哪、验证 episode、开始下一环节。
---

# 真人口播编排器

编排器只根据 episode 里的真实文件路由。它不把聊天结论当完成，也不在脚本内 programmatic 调用其他 skill；宿主 Agent 读取唯一路由后执行对应 skill，再重跑 bianpai。

①额外验证 `screening_summary` 的 signals→longlist→短名单链路。抖音平台数据真实尝试后仍不可用时允许 `UNAVAILABLE`，不单独阻塞；discovery、PRIMARY 和其余①合同仍必须通过。

## 命令

```bash
# 从 laohanAI视频创作 根目录运行；不要从 skill 目录运行

# 当前状态、缺失产物、唯一下一步
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs status --episode episodes/<slug>

# 先检查 dbskill / Cheat 上游；只在新 episode 前或独立维护窗口同步
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs vendors --episode episodes/<slug>
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs vendors --episode episodes/<slug> --sync

# 只输出下一步的输入、产物、gate 与 skill
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs next --episode episodes/<slug>

# 运行已实现的机械契约检查
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs check --episode episodes/<slug>

# 阶段验收；未完成时退出非 0
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs check --episode episodes/<slug> --require production
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs check --episode episodes/<slug> --require full

# 要求成片已经接受；供⑫发布前调用
node ~/Documents/laohan-skills/laohan-bianpai/scripts/bianpai.mjs check --episode episodes/<slug> --require final
```

## 工作流

1. 恢复工作先运行 `vendors`。它把当时可用 vendor 的状态和完整 HEAD SHA 写入 schema 3 `FROZEN_ON_RESUME`；进行中 episode 只能在两方 HEAD 与原冻结值一致时续用，旧 schema 2 因缺 commit 证据必须 BLOCKED，不能从当前 HEAD 猜填。`--sync` 只会在新 episode 前或独立维护窗口、Cheat 工作树干净、活动 lane 没有 schema migration 时更新。新 episode 只能从 `UP_TO_DATE` 或审计过的 `READY_LOCAL_AHEAD` 状态创建；更新可用/待安装不得写成 READY。schema 2 episode 还必须通过 `00-编排/executor-lock.json`；registry/runtime lock 漂移时不得刷新 preflight 掩盖执行器变化。
   已存在且通过机械核验的 `00-编排/supersession-record.json` 必须优先返回 `SUPERSEDED`，不得继续 vendors/status/next/check，也不得用新 lock 覆盖旧 lock。
2. 读取 `episode-config.json`，先运行 config gate。失败时停在①之前，不路由任何内容或生产步骤。
3. 按①—⑭检查标准产物，并在⑥与⑦之间检查V5.1导演初稿`D1`和最终复审`D2`。新episode默认 `CODEX_DIRECT + Remotion`，媒体窗口归属固定如下：

   ```text
   06-原片剪辑与制作准备：同一Codex Desktop任务连续完成⑧和⑨，只冻结clean/SRT、direct-brief与source-manifest。
   07-网络素材：仅在source-manifest存在网络请求时创建独立任务；无请求为NOT_NEEDED。
   08-本机录屏：仅在source-manifest存在LOCAL_CAPTURE请求时创建独立任务；无请求为NOT_NEEDED。
   09-成片candidate制作：独立任务，只消费已复核或NOT_NEEDED的⑩状态后执行⑪。
   ```
4. ④先记录带原始隔离 JSON 的 score；编排器只验证绑定、无污染和证据级别，不替评分器判断内容质量。此时状态为 PARTIAL，再进入⑤；⑤报告与 `04-事实主张.json` 匹配当前稿后，④必须写最终盲预测并成为 COMPLETE，才可进入⑥或任何 production/final gate。
5. 输出唯一下一步的 skill、必要输入、应落盘产物与不能跨越的 gate。`AUTONOMOUS_RUN` 在标准①—⑥全程输出 `AUTO_CONTINUE_REQUIRED`（2026-09-17起①按五步法AI自主定题、②直接写稿，无询问门槛）。Jeffrey否决选题（`00-选题-Jeffrey否决.json`）或五步法信号不足时输出`TOPIC_RESCAN_REQUIRED`，作为同一01任务内的计划内回退，不进入②，也不算BLOCKED；新候选携带否决历史。D1导演初稿与D2最终复审分别继续对应固定任务，D2完成后才路由⑦。标准入口到⑦输出 `WAITING_FOR_JEFFREY_SHOOTING` 并停下。`USER_PROVIDED_FINAL_SCRIPT_AND_RAW`不补造内容门槛；具备完整`FULL_PIPELINE_TO_PUBLISH`授权时，已提供最终稿入口仍不得增加新的Jeffrey确认卡点。
6. Jeffrey明确提供最终口播稿和真人原片时，只接受`episode_entry_contract.mode=USER_PROVIDED_FINAL_SCRIPT_AND_RAW`和`00-编排/user-provided-inputs.json`的SHA闭合记录。登记器同步生成绑定当前稿与raw的`shooting-record.json`；①—⑤显示`~`用户输入替代态，不伪造完成证据，也不再错误路由回①；D1、D2及后续生产按本期授权自动继续。
7. 如果旧V5 episode已经生成待验收candidate，再升级V5.1时只接受`FROZEN_PENDING_CANDIDATE_PREDATES_V5_1_STATE_FIELDS`受控迁移。迁移必须冻结原candidate和director-state SHA；编排器把D1/D2视为本期已完成的兼容事实，不得倒退重写导演稿或重新生产。默认停在`JEFFREY_REVIEW`；仅完整自动化授权改走`AGENT_PROXY`。
8. 唯一下一步始终是最早失效节点。④已评分、⑤已完成或⑥曾有产物都不能覆盖破损的①—③；下游文件可以保留为历史证据，但在前缀恢复前不算可继续状态。

## 硬规则

- schema 2在①前必须有distribution contract与executor lock；⑥开始前distribution必须锁定。⑦前必须有shooting_contract；⑦通过后交接任一已注册生产宿主（Codex Desktop或ZCode，铁柱）的06窗口完成⑧和⑨——HANDOFF_TO_CODEX语义见主项目AGENTS第7条，纯会话型Claude Code只能返回交接token不能生成媒体产物，再按source-manifest分别路由07、08和09。⑨前必须有绑定当前raw/稿件的raw-transcript、edit-candidates、schema 2 edit-decision、edit-render、clean、large-v3 clean-transcript/SRT provenance、spoken-script-variance、Codex edit-review与schema 5 edit-manifest；候选必须逐项裁决，不确定KEEP，不路由人工审批。
- schema 2 的①必须同时有 signals、至少两个真正不同的 candidates、source health、抖音 JSON+Markdown 与最终选题；同一事件的观点/教程变体只要受众任务、标题承诺和内容路径不同即可分别计数。每个候选都必须登记 `creator_fit`，唯一 SELECTED 还必须锁定可成立的 Jeffrey 个人依据、独特判断、why-now、lane、小白合同、PRIMARY+PLATFORM_SIGNAL claim map，以及 `ALIGNED` 或有差异化解释的 `ADJACENT` 平台语义。教程型 lane 的 SELECTED 候选还必须绑定 `tutorial_proof`：`status: VERIFIED`、本机真实执行产物的 `evidence_path` 与 `evidence_sha256`、`version_boundary` 与 `recovery` 方法，对应 CLAUDE.md 第13条“教程写成确定步骤前仍须本机真实执行、版本边界和恢复方法”。编排器只验证这些字段存在和来源一致，不根据创意风格、模板或分数淘汰候选。③只对明确未解决高风险阻断；ruleset 过期只要求在报告中警告并安排复核。
- 标准新期①必须通过`laohan-xuanti` schema 4 validator（3.3.0+五步法合同），证明数据层达人库全池与自频道已扫描、候选通过假阳性过滤、`topic_kind`、tension与`packaging_assessment`收藏三问，AI自主定题（AUTO_SELECTED）；Jeffrey否决必须退回扫描。新期②必须使用 `laohan-chuangzuo` schema 4，并实际通过其 `scripts/check-script-contract.mjs`，证明选题SHA与个人表达池取材绑定、钩子兑现包装承诺；原有内容单位、原创增量、可视化锚点、逐段SHA、人味、自然稿长和本机TTS合同继续有效。旧episode按其 executor lock 继续验证冻结合同，不静默迁移。
- ⑤必须同时验证 `04-事实主张.json`；直接来源支持写 `SUPPORTED`，实现推导写 `INFERRED + inference_note`，后者不能充当 PROOF beat。`PASS` 只表示机械合同通过，不代表编排器独立确认内容优秀。
- ⑥固定读取项目 `assets/identity/jeffrey-cover-reference.jpg`，并使用新期自动复制的 `05-封面/reference/jeffrey-reference.jpg`。`reference_mode` 只允许 `REQUIRED`；项目真源、本期副本与 config SHA 必须一致。完成合同为：绑定当前稿和本期 reference 的 `cover-prompts.md`、01/02/03三张真实9:16排序候选，以及默认01同一视觉主张分别重新构图生成的3张共享真实尺寸封面：3:4复用到抖音竖版、视频号个人主页和小红书，4:3复用到抖音横版、视频号分享和B站首页推荐，16:9用于B站个人空间，共映射7个发布入口。任何一张缺失、比例错误、不可解码或由简单裁切冒充都不通过；provider request、review和 `selected-cover.json` 不是硬门槛。
- 封面延后仅用于提示词、三张候选或三张共享发布封面尚未完成时的临时时序调整。`--require production` 可接受有效的本期延后授权；补齐完整合同后 `--require final|full` 才通过⑥。
- V5.1制作前必须在同一个`09-导演/director-state.md`同时满足`director_draft: COMPLETED`和两处`director_review: COMPLETED`。初稿的`PENDING`只能路由最终复审，不能进入⑧。
- 已存在pending candidate的V5.1兼容迁移是一次性历史例外：只承认迁移记录冻结的candidate与director-state，不允许借兼容字段跳过新episode的D1/D2。默认状态是`JEFFREY_REVIEW`；只有当前episode完整绑定`FULL_PIPELINE_TO_PUBLISH + AGENT_PROXY`时，Codex完成全片QA后才可代理选择并继续。Jeffrey无需掌握Remotion技术。
- CODEX_DIRECT 的 direct brief 必须绑定当前 clean/SRT、柱子哥 production learning profile、3—5 个当前样本和 2—4 个本期学习目标，且不能包含 renderer 实现细节。
- ⑩不能因 stock 无结果放行；⑪不能因 candidate 存在写 final.mp4，必须有完整观看 QA。默认由 Jeffrey 看过并接受；仅当前 episode 预先记录 Jeffrey 本人、ISO时间和原话的 `final_selection_contract.mode=AGENT_PROXY` 时，Codex可在完整QA后代为选择，并写 `selection_mode=AGENT_PROXY` 的审阅记录。
- ⑫默认不自动发布。只有当前episode用输入记录SHA绑定Jeffrey本人、ISO时间和原话的`FULL_PIPELINE_TO_PUBLISH`授权，并同时覆盖`DEFAULT_COVER_RANK_01`、`AGENT_PROXY_FINAL_SELECTION`、`FOUR_PLATFORM_AUTO_PUBLISH`和`SCHEDULE_T_PLUS_N_RETRO`四项scope时，才可从最终口播稿与真人原片继续到四平台发布回执；封面默认使用rank 01的3张共享尺寸成品，热点失败按非阻断策略继续。评论回复与方法论升级仍不自动执行。
- 有产物但未满足 gate 时，报告 BLOCKED，不算完成；JSON 损坏也必须报告 BLOCKED，不输出 stack trace。
- 普通 `check` 只检查已有输入并明确输出 INCOMPLETE；只有 `--require production|final|full` 可作为阶段验收。
- ⑫—⑭由 `laohan-yunying` 处理；默认发布、评论回复和数据纠正都必须有对应的人工确认或来源证据。当前episode具备完整`FULL_PIPELINE_TO_PUBLISH`授权时，四平台发布可由该本期授权替代逐次人工确认，但仍必须取得平台真实回执；不能把预留目录当完成。

## 不适用

- 写口播稿、发布 → 使用对应专业skill。06与09使用 `codex-direct-production` executor；07、08各自独立且条件式创建。⑧不路由人工候选审批：不确定KEEP，事实冲突回上游。
- 只有一个独立文案、没有 episode 目录 → 先创建 episode，不猜文件位置。

## 反模式

❌ 看见 `01-口播稿.md` 就认为整期可拍。  
✅ 先检查 config、事实核验、封面最小合同和拍摄契约。

❌ 自动跳过 no_result 或技术失败。  
✅ 保留 BLOCKED，并返回产生该决策的上游步骤。
