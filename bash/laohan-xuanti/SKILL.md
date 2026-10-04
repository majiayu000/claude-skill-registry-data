---
name: laohan-xuanti
version: 3.3.0
description: 真人口播①选题决策主写者；按老韩选题五步法（扫爆款→剔假爆款→看重复→定角度→验收藏）执行：扫描数据层达人库与自频道异常倍数，过滤假阳性，判定单期/系列，提炼冲突角度并验证收藏价值后AI自主定题（Jeffrey保留否决权），核对小白受众承诺、抖音语义对齐和 PRIMARY 原始来源。Use when 用户说"抓热点""AI热点""找选题""选题""今天做什么""redian"，或 bianpai 路由到①；单独搜抖音时改用 laohan-douyinsousuo。
argument-hint: [可选：--episode episodes/<slug>；或关键词]
allowed-tools: Bash(*), Read, Write, Glob, Grep
---

# ①选题决策

热点只用于发现，最终结果是一个可审计的生产决策：为什么现在做、给谁看、论点凭什么成立、抖音上有哪些重复角度、为什么淘汰其他候选，以及发布后如何按固定窗口复盘。

## 边界

- 本 skill 是①唯一主写者，写 signals、candidates、source-health 和 `00-选题.*`。
- `laohan-douyinsousuo` 只写 `00-抖音搜索证据.{json,md}`；同一 Agent 宿主按 bianpai 路由执行，不做 programmatic skill-to-skill 调用。
- ②才写口播稿；①不生成正文、大纲段落或封面。
- ⑤才做完整事实核验；①仍须给最终事实前提找到至少一条 PRIMARY 原始来源。
- 不安装新浏览器、爬虫、Python runtime 或第三方 skill。抖音平台访问只用已安装 OpenCLI。
- 同一事件可以形成观点候选和教程候选；受众任务、标题承诺和内容路径真正不同时可分别参加比较。②—④沿用选中 lane，不混写。

## 输入

Episode 模式必须读取：

1. 本期 `episode-config.json` 与 `00-编排/` 冻结产物。
2. 本期已显式登记的反馈快照；没有就记录 `NOT_AVAILABLE`，不得扫描旧 episode 猜经验。
3. 本轮真实 signals 与抖音搜索证据。

标准 Episode 为 `AUTO_SELECT`：AI按五步法完成发现、过滤与定题， Jeffrey 保留事后否决权（`00-选题-Jeffrey否决.json`，否决原因必填，否决后按原因重新扫描）。Jeffrey 明确给题时走 `USER_SEED`，仍须给出至少一个真实替代候选、抖音取证、PRIMARY 证据和测量合同。

Jeffrey给出的是软件、方法或系列方向时，先走`USER_DIRECTION_RESEARCH`：读取项目`docs/系列选题研究与分期规格.md`，完成四平台定向搜索、内容级拆解、需求判断、系列分期和单期资料包。它不运行与方向无关的9账号泛扫描来凑热度。只有`DEMAND_VALIDATED`可进入三期以上系列，`EXPERIMENTAL_ONE_OFF`只进入单期，`DIRECTION_REJECTED`停止。正式episode仍须提供替代候选。

## 工作流

### 1. 采集当前信号

先写`00-选题-signals.json.discovery_mode`：无方向为`AUTONOMOUS_SCAN`；Jeffrey已给方向为`USER_DIRECTION_RESEARCH`。后者把已通过`node scripts/check-series-research.mjs`的`series_research_path`与SHA写入`direction_research`，并把哔哩哔哩、小红书、抖音、知乎四路结果分别登记为signals来源。`DEMAND_VALIDATED`至少两个平台有真实需求信号；`EXPERIMENTAL_ONE_OFF`只按研究包内已验证的官方新事件、Jeffrey亲历或小众任务依据进入单期，不强制伪造两个平台热度。

Episode 模式执行唯一确定性入口：

```bash
node ~/Documents/laohan-skills/laohan-xuanti/scripts/collect-topic-signals.mjs \
  --episode episodes/<slug>
```

`AUTONOMOUS_SCAN`按五步法第1步扫爆款：`数据层/tracked-creators.json`全池逐账号扫描（ACTIVE必扫且失败阻断；PENDING一并扫描供交叉印证，失败如实记录不阻断）、`数据层/self-channel.json`自频道异常倍数（自己异常倍数高的方向优先深挖）、全面热点（辅助输入）与`script-pool/Jeffrey个人表达池.md`（素材来源）。扫描同时执行**时间分层**（近30天异常=当下需求优先做；3个月前异常=常青题，需再验证当下热度）与**异常分级**（3倍=值得注意，10倍以上=大机会优先深挖），并消费每条异常的`top_comments`高赞评论——高赞评论是观众没被满足的问题，直接作为候选线索。默认发现与展示优先级为`BENCHMARK_CREATOR(1) > SELF_CHANNEL(2) > BROAD_HOTSPOT(3) > PERSONAL_EXPRESSION(4)`。全面热点默认 route 为 AIHOT、Hacker News、知乎、微博、36kr、B站、抖音热榜、头条、贴吧和虎扑；某一路失败如实记录，其他热点路继续。需要缩小热点route时才传 `--sources`，不能借此跳过达人库和自频道。

脚本只写：

- `00-选题-signals.json`
- 初始 `00-选题-source-health.json`

脚本不选题、不访问旧 episode、不调用 `douyin-ai.js`。

### 2. 标准化、去重、形成候选

读取 signals，按稳定 signal id 聚类同一事实事件；排除同 URL/同承诺/同路径的重复表达。对标账号只提炼母题、公众需求和异常信号，不复制标题、文案、案例或结论。同一事件只有在“帮观众作判断”和“带观众完成任务”分别成立时才生成两个形态。写 schema 4 `00-选题-candidates.json`，先用顶层 `screening_summary` 留下筛选链路，再写至少两个真正不同的短名单候选。`screening_summary` 只包含：

- `raw_signal_count`：signals 中实际结果总数；`event_cluster_count`：去重后的事件簇总数。
- `longlist`：有效事件足够时记8—12条，不足8条时全部记录。每条含唯一 `event_cluster_id`、`working_title`、非空 `signal_ids`、正整数 `source_count`、`disposition: SHORTLISTED|REJECTED` 和具体 `reason`。
- 每个最终候选的 `event_cluster_id` 都必须在 longlist 中标 `SHORTLISTED`。不新增中间文件、额外节点或第二套打分器。

同一事件的观点/教程变体在受众任务、标题承诺和内容路径不同时可分别计数。每项必须有：

定角度前置动作：**先读原视频**——必须读过原爆款的转录或完整内容才允许写tension（反驳/补深/亲历替代都建立在实际内容上，没读过就是猜）。对标视频转录复用项目既有转录工具链（large-v3），产物放`数据层/scans/<日期>/`或episode临时目录。想不出差异时用兴趣市场工具：两个高兴趣题材组合=受众叠加，并评估母题受众池大小（工具教程类通常大于纯观点类，同质量优先池大的）。

形成候选前恢复原版分析：以“AI/GPT/Claude/大模型/机器人/自动化/编程/副业”等直接词和“教育/职业/消费/创业/职场”等间接词标注相关度，但保留可能产生新角度的边缘信号；统计安装教程/进阶技巧/方法论/对比评测/实战/资源推荐等内容类型；标出多平台共振、单平台独有、已拥挤角度和竞品未覆盖机会。它们用于扩大候选，不替代后面的 PRIMARY 与抖音关键词核验。

- 唯一 `id`、稳定非空 `event_cluster_id`、非空 `why_now`、`title`、`content_form: opinion-video|tutorial-video`、`audience_level: BEGINNER|INTERMEDIATE|ADVANCED`、`audience_problem`、`audience_promise`、`thesis`。
- `candidate_origin` 必须登记 `primary_lane`、对应的 `priority_rank`、非空 `origin_signal_ids` 与 `corroborating_lanes`。交叉印证可以提高可信度，但不能把个人表达来源伪装成对标爆款来源。
- `tension` 必须登记 `type: CONFLICT|MISCONCEPTION|COUNTERINTUITIVE|TRADEOFF`、`common_assumption`、`jeffrey_position` 和一句可由正文兑现的 `conflict_statement`。只写领域名、产品发布或“值得关注”不算候选。
- `creator_fit` 必须写清 `basis: FIRSTHAND_EXPERIENCE|BUILT_OR_TESTED|OWNED_EVIDENCE|LONG_TERM_PRACTICE|RESEARCHED_JUDGMENT|NOT_ESTABLISHED`、`why_jeffrey` 与 `distinctive_judgment`。它回答“为什么由 Jeffrey 讲、他的依据是什么、相比通用复述多了什么判断”。SELECTED 不允许 `NOT_ESTABLISHED`；没有亲历时可以使用 `RESEARCHED_JUDGMENT`，但必须形成有证据边界的独立判断，不能把“我也关注了”冒充个人优势。
- `assumed_prerequisites` 与 `jargon_to_explain` 字符串数组。BEGINNER 候选必须把标题和论点里的关键工具、命令、迁移/导入概念列入解释清单，不能只提高 `audience_fit` 分。
- 非空 `signal_ids` 和 `evidence_ids`。
- 非空 `platform_query_intent`；`platform_alignment` 含 `status: ALIGNED|ADJACENT|CONTRADICTED|UNRESOLVED|UNAVAILABLE`、非空 `rationale` 和 `evidence_ids`。有平台结果时 evidence ids 必须真实；平台访问失败时写 `UNAVAILABLE` 和空数组。
- `content_gap` 含 `status: CONFIRMED|NOT_CONFIRMED|UNAVAILABLE`、非空 `rationale` 和 `evidence_ids`。只有平台直接提供搜索量、供给或缺口证据时才能写前两种；搜索结果条数、互动字段缺失或模型判断一律不能冒充内容缺口。`UNAVAILABLE` 合法且不参与机械淘汰。
- 非空 `claim_evidence_map`；每条含唯一 `claim_id`、非空 `claim`、`evidence_ids`。它要把技术事实绑定 PRIMARY；平台证据可用时，把“平台有人关心什么”绑定 PLATFORM_SIGNAL，不能让相邻关键词替另一个论点背书。平台 `UNAVAILABLE` 时不虚构 PLATFORM_SIGNAL claim。
- `scorecard` 七维整数 1—5：`audience_fit`、`evidence_strength`、`platform_relevance`、`differentiation`、`creator_fit`、`production_feasibility`、`learning_value`。
- 非空 `rationale`。未定题时候选为 `disposition: SHORTLISTED`或`REJECTED`；五步法全部通过的最优候选由AI标记`AUTO_SELECTED`（同时其余候选给`REJECTED`加具体理由）。
- `false_positive_filter`（第2步剔假爆款）：`status: PASSED|REJECTED`、`checks`四项布尔（`celebrity_event`/`controversy`/`off_niche`/`pure_news`）、非空`rationale`。四类假信号命中的候选保持REJECTED，不得入选。
- `topic_kind`（第3步看重复）：`SERIES_CANDIDATE|ONE_OFF`。前者必须绑定`topic_corroboration.signal_ids`——两个不同账号的同母题异常即可成系列，三个以上账号=强信号降风险。系列优先采用可追更形式（"挑战30天XX""10天教会XX"式进度感系列，直接吃到复访率权重），形式写入`topic_corroboration.series_format_hint`（可空）。
- `packaging_assessment`（第5步验收藏）：非空`title_direction`与`cover_concept`（一句话，不做图）、三问布尔`worth_collecting`/`evergreen_half_year`/`title_clickable`、非空`rationale`。AUTO_SELECTED候选三问必须全true；不达标回第4步换角度或换题。

分数是可挑战的候选比较，不是流量预测。热度不能替代受众价值、证据强度、差异化或可拍性。SELECTED 可为 `ALIGNED`、有明确差异化解释的 `ADJACENT`，也可在 discovery 与 PRIMARY 充分时为如实说明缺失范围的 `UNAVAILABLE`；平台缺失降低 `platform_relevance` 置信度，但不能单独淘汰候选。`CONTRADICTED|UNRESOLVED` 不得入选。教程候选写成确定步骤前仍必须在 `tutorial_proof` 登记 `status: VERIFIED`、本期内 `evidence_path`、`evidence_sha256`、非空 `version_boundary` 和 `recovery`。

### 3. 对短名单做抖音关键词验证

为 1—3 个短名单各设计一个具体查询，交同一宿主执行 `laohan-douyinsousuo` episode 模式。必须得到 `00-抖音搜索证据.json` 与 `.md` 后才继续。

- `OK`：引用真实结果 id，写清查询实际证明的观众意图。直接支持候选标题承诺、受众任务和 `why_now` 时标 `ALIGNED`；只支持同一产品、迁移热度或相邻概念时标 `ADJACENT`。优先补充更直接查询，但不因缺少完全同标题内容自动淘汰差异化新角度。
- `EMPTY_OR_FIELD_UNAVAILABLE`：只写“平台证据未决”，不得写“无人做/蓝海”。
- OpenCLI 登录或 adapter 全部失败：保留真实 FAILED 证据，把 `platform_alignment` 与 `content_gap` 标 `UNAVAILABLE`；只要 discovery 与 PRIMARY 足够，继续比较，不把平台缺失当卡点。

### 4. 回到 PRIMARY 原始来源

对最终候选的事实前提查找官网、官方公告、论文、产品文档或原始公开记录。平台热榜、搜索结果、媒体转述只能是 `PLATFORM_SIGNAL` 或 `SECONDARY`。

把 PRIMARY 与 PLATFORM_SIGNAL evidence 写入候选文件；每条有稳定 `id`、`source`、`source_type`、`url`、`retrieved_at`。缺 PRIMARY 时缩窄论点为可证范围；仍无法成立就换候选或 BLOCKED。

### 5. AI自主定题（Jeffrey保留否决权）

五步法全部通过后直接定题，不等待Jeffrey：

- 按`异常倍数 > 收藏价值 > 定位重合度`排序，取最优候选标记`AUTO_SELECTED`，其余改`REJECTED`并写具体理由；并列时优先`SELF_CHANNEL`异常方向（自己已被验证的赛道）。
- 写 schema 4 `00-选题.json`（含`auto_selection_rationale`）与`00-选题.md`后直接进入②。
- Jeffrey否决：任何时候可写 schema 1 `00-选题-Jeffrey否决.json`（`vetoed_by/vetoed_at/candidates_sha256/selected_candidate_id/veto_reason`必填）。否决后进入`TOPIC_RESCAN_REQUIRED`：按否决原因重新扫描，删除AUTO_SELECTED与最终选题；新候选必须把否决记录（四项+旧候选SHA）原样写入`screening_summary.rejection_history[]`，不得重复推被否决的候选。
- 信号不足以支撑任何候选通过五步法时进入`TOPIC_RESCAN_REQUIRED`扩大扫描（新登记达人候选、补抖音搜索），不勉强定题。

### 6. 写最终决策与 source health

更新 `00-选题-source-health.json`，每路记录：

- 唯一 `source_id` 与 `source_role: DISCOVERY|BENCHMARK_CREATOR|PERSONAL_EXPRESSION|DOUYIN_SEARCH|PRIMARY_PROOF`。schema 3必须保留后两条本地发现角色；个人表达池允许`EMPTY`，对标账号只允许完整扫描后的`OK|EMPTY`。
- 实际 `command_or_url`、`attempted_at`、`status`、`result_count`。
- 本期相对 `result_file` 与真实 `result_sha256`。
- FAILED 写 `error`；SKIPPED 写 `reason`。

状态必须一致：OK 条数大于 0，EMPTY/FAILED/SKIPPED 条数为 0。至少一条 DISCOVERY 为 OK、一条 DOUYIN_SEARCH 有真实尝试记录、一条 PRIMARY_PROOF 为 OK；DOUYIN_SEARCH 可以 FAILED，但必须绑定本期抖音证据文件与原始错误。

写 schema 4 `00-选题.json`，绑定AUTO_SELECTED候选与`auto_selection_rationale`。最后执行：

```bash
node ~/Documents/laohan-skills/laohan-xuanti/scripts/check-topic-contract.mjs --episode episodes/<slug>
```

只有输出`PASS redian topic contract schema=4`才算①完成。

- `schema_version: 4`、`selected_candidate_id`、非空 `rejected_candidate_ids`、非空 `auto_selection_rationale`。
- 原样复制选中项的 `content_form`、`audience_level`、`audience_promise`、`creator_fit`、`assumed_prerequisites`、`jargon_to_explain`、`platform_query_intent`、`platform_alignment`、`content_gap` 和 `claim_evidence_map`。
- `audience`、`thesis`、`evidence`、`selection_rationale`、`not_do_reason`。
- evidence 全部属于选中候选，且至少一条 PRIMARY；平台可用时至少一条 PLATFORM_SIGNAL，`platform_alignment.status=UNAVAILABLE` 时可没有。
- experiment 含唯一主要 intervention、合法 `metric_keys`、正整数 `T+N`、`observation_window_unit: DAY` 和逐键 `metric_targets`。

每条 metric target：

```json
{
  "key": "avg_duration_sec",
  "direction": "INCREASE",
  "baseline_ref": "recent_5_median",
  "measurement_source": "douyin_creator_center"
}
```

最后写 `00-选题.md`，只解释机器合同里的真实决策，不新增未登记事实。

## 失败处理

| 触发条件 | 处理 |
|---|---|
| 单一 discovery source 失败 | 记录 FAILED；其他来源满足角色合同可继续 |
| 所有 discovery source 无结果 | BLOCKED，不凭模型记忆选题 |
| 抖音返回合法空数组 | 记录 EMPTY；不得推断没有竞争 |
| OpenCLI 登录/adapter 全路径失败 | 平台证据记 `UNAVAILABLE` 并继续；不安装替代爬虫，不推断蓝海 |
| 最终候选无 PRIMARY | 缩窄论点或换候选；仍无则 BLOCKED |
| Jeffrey否决当前选题 | 进入`TOPIC_RESCAN_REQUIRED`；按否决原因重新扫描，否决历史带入新候选，不进入② |
| 平台结果只支持相邻话题 | 标 `ADJACENT`，补充查询；仍相邻时如实说明差异化与风险，可参加最终比较，不得冒充直接对齐 |
| 教程候选没有本机真实执行证据 | 保持 REJECTED；可保留为待验证候选，不能写成教程已可交付 |
| 候选不可在既有⑬指标测量 | 换 intervention/metric 或换候选 |

## 反模式

❌ “三个平台都热，所以就做这个。”

✅ “候选 C02 同时解决目标受众问题，PRIMARY 支持事实前提，抖音证据显示现有内容集中在功能介绍，本期以真实工作流代价形成差异；C01/C03 因证据弱或不可拍被淘汰。”

❌ “抖音有人搜 Claude Code 迁移，所以能证明‘验证闭环’是当前平台需求。”

✅ “该结果只证明迁移/导入需求，标 ADJACENT；继续搜索验证失败、上线回归等直接意图。若仍无直接结果，可把‘验证闭环’作为差异化观点参加比较，但明确平台证据只支持相邻需求。”

❌ “搜索 0 条，所以这是蓝海。”

✅ “搜索执行成功但返回 0 条，记为平台证据未决，不据此判断竞争度。”

## 非 Episode 模式

用户只要热点简报时，可以执行同一采集脚本到临时目录后返回当前信号摘要；不写 episode 真源。用户只要搜抖音时直接路由 `laohan-douyinsousuo`。
