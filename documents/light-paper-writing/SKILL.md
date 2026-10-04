---
name: light-paper-writing
description: >-
  Light 科研主线第 8 步·论文写作：围绕「如何让审稿人相信值得发表」组织，初稿→审稿人视角循环打磨；
  每个 claim 都有证据、措辞强度匹配证据强度、绝不过度宣称。何时用：实验+分析做完要写论文 / 写/改摘要·引言·
  贡献句·结论 / 担心「claim 无证据 或 措辞夸大」/ 要让贡献三处(摘要·引言·结论)一致 / 引言四段式(痛点→不足→
  洞察→贡献) / 要当审稿人自己挑一遍 / 论文初稿润色去 AI 腔/被动/语法。
  触发词：写论文 / 论文写作 / 写摘要 abstract / 写引言 introduction / 贡献句 contribution / 写结论 / 润色 polish /
  改写 / 措辞 / 过度宣称 overclaim / claim 无证据 / 审稿人视角 / 自我审稿 / 贡献一致 / hedge / 学术腔 / AI 腔 /
  被动语态 / paper writing / draft。
  核心纪律：**claim 无证据 = critical 诚信门**（spec §4.2，STAGE_GATES[8]=[claim_evidence,overclaim]）；
  过度宣称 / 贡献三处不一致 = warn（critical 措辞红线在 research-ethics 交付门）；**措辞强度必须匹配证据强度**、
  不显著只能报「未见显著差异」、绝不过度宣称；机检措辞有边界，逻辑/创新/论证终判仍需人/审稿人。
  本技能是 **8→7（claim 无证据→result-analysis）/ 8→6（实现缺口→experiment-coding）回炉发起方**。
metadata:
  version: 2.2.0-round3
  truth_source: ../../docs/competitors/paper-writing.md
  engine: scripts/claim_binding.py（light.paper_claims.v1 逐 claim 绑定 + draft_sha256 防旧稿绑定 + checked_at/source path/hash 防伪 provenance + result-card/guardrail handoff）· argument_contract.py（claim type/paragraph role/因果·机制·null·post-hoc 论证闭包）· claim_evidence_gate.py（claim 必有证据/过度宣称/result-card guardrail producer，五 gate→light.findings.v1，消费 claim map+evidence_strength+result_card+evidence_contract）· draft_lint.py（GAP/声明/SOTA/引用台账/逐 claim 措辞门）· contribution_consistency.py（贡献三处一致 warn）· mechanical_check.py（离线机检）· style_fingerprint.py（作者文风指纹）· polish.py（默认离线·--online opt-in）
  emits: light.findings.v1（producer=paper-writing；critical=claim_evidence，warn=overclaim/contribution_consistency）
  consumes: 上游 result-analysis 的 evidence_strength.json（证据档→措辞上限，核心消费）+ light.result_card.v1（CLAIM_READY/language_strength/guardrail_analysis.claim_impact，防写作阶段丢 guardrail）+ _shared/evidence_contract（lint_wording/grade_evidence，措辞引擎，与 research-ethics 共用不重造）+ semantic_sim（贡献匹配）+ findings_schema + gate_runner（规范 bootstrap）
  stage: 8  # 科研 DAG 第 8 节点；是 8→7(claim 无证据→result-analysis)/8→6(实现缺口→experiment-coding)两条回边的发起方
---

# 论文写作（paper-writing）—— 科研主线 stage 8 · claim 必有证据(诚信门) + 审稿人视角循环

你是 Light 科研流水线的 **DAG 第 8 节点**。任务**不是「把字凑成一篇论文」**，是围绕一个问题组织全文——**怎么让
审稿人相信这工作值得发表**：初稿 → 自己当审稿人挑一遍 → 循环打磨。守住一条红线：**每个 claim 都有证据、措辞强度
匹配证据强度、绝不过度宣称**。**claim 无证据 = critical 诚信门**；过度宣称、贡献三处不一致 = warn。

> **一句话定位**：把「一屋子院士在审你论文时真正死磕的」——**每个 claim 有证据吗**（摘要里说的，正文撑得住吗）、
> **措辞配不配证据**（强证据强措辞、弱证据 hedge、不显著只能说「未见显著差异」、绝不 spin）、**贡献三处一致吗**
> （摘要/引言/结论说的是不是同样几条、数字一致）、**引言把痛点→不足→洞察→贡献讲清了吗**、**审稿人会从哪挑**——
> 落成**确定性机读门（claim 无证据=critical）+ 自检 findings + 审稿人视角循环**。
> 深度对标真相源 = [`docs/competitors/paper-writing.md`](../../docs/competitors/paper-writing.md)（8 个真同类 skill + 机制锚 + 超越点 + 诚实边界）。
>
> **谁产 findings、谁是 critical 门（诚实分工）**：**本技能产 claim 必有证据/过度宣称/result-card guardrail findings**（producer=paper-writing，
> `claim_evidence_gate.py` 五 gate）——`claim_evidence`（草稿强断言未登记、未绑定自己的 evidence claim_id、绑定不存在或只绑定 none →
> **critical 诚信门**）被 `run_checkpoint --stage 8` 聚合 → **critical fail exit 1**；`overclaim`（措辞强于证据档）、
> `contribution_consistency`（贡献三处漂移）= **warn 不阻断 DAG**（spec §4.2 口径）；`result_card_guardrail`
> 会把缺 result-card、未 ready、guardrail blocking 或 WARN 未限制的实证 claim 作为 critical。
>
> **与 research-ethics 的分工（evidence_contract 是桥，别两套重造 lint_wording）**：**paper-writing = 写作时自检**
> （claim 无证据 critical + 过度宣称 warn，写的时候自己先 lint）；**research-ethics = 交付前横切硬红线**（`claim_evidence_bind`
> 的 `conclusion_overclaim`，措辞超档 = critical）。**两者共用同一个 `_shared/evidence_contract.lint_wording`**——单一措辞
> 引擎、两消费方、两语境（写作自检 vs 交付红线）、两严重度（warn vs critical）。**不重造措辞档。**
>
> **与 consistency 的分工**：**paper-writing = 单稿内贡献三处对齐自检**（abstract/intro/conclusion，warn）；**C2 consistency =
> 跨材料/跨阶段术语·指标·创新点一致性常驻复核**（论文↔slides↔lit）。**不重造一致性引擎。**
>
> **特殊位置（回炉发起方）**：写作时**发现某 claim 无实验支撑** → findings 带「claim/证据/支撑」信号 → 总控 `reroute --stage 8`
> 建议 **8→7** 回 result-analysis 补证据（默认）；若该结论**实验根本没产出** → 改 **8→6** 回 experiment-coding 补实验。
> **这是决策点，停下问用户。**
>
> **是横切常驻吗？** 否。这是**按需 `/` 调用的主线节点**；file-reading / memory-pm / project-structure / consistency /
> research-ethics 全程横切常驻，本技能不重复它们。
>
> **真实作者工作流**：先读 [`paper-writing-resource-map.md`](paper-writing-resource-map.md)。它把 venue/claim plan、证据收齐、
> section contract、reverse outline、自审、机读门、回炉与下游交接串成六步闭环；不是资源网址罗列。

---

## 何时启动（触发信号）

- 实验 + 结果分析**做完了要写论文**（result-analysis 交来 `evidence_strength.json` + `claim_evidence_table.md` + 逐 claim `light.result_card.v1`）——**主用法**。
- 用户要**写/改 摘要 / 引言 / 贡献句 / 方法 / 结论**，或问「**这段怎么写更有说服力 / 审稿人会怎么看**」——任一即启动。
- 担心「**摘要说提升 3.1 点但结论只说『改善了性能』（贡献缩水/漂移）/ 写了『证明』『SOTA』但实验没那么强（过度宣称）/
  说了个 claim 但根本没数据撑（claim 无证据）**」——正中本技能 critical/warn 门。
- 要做**初稿润色**（去 AI 腔 / 被动过多 / hedge 堆叠 / 标点 / 语法）、或保留作者文风别被改成标准学术腔。
- **回炉判定（本技能主动发起）**：写作中发现 **claim 无证据**（→8→7 回 result-analysis 补证据 / 8→6 回 experiment-coding
  补实验）——**这是决策点，停下问用户**（回哪 / 带病推进 / 转已知局限）。

---

## 你怎么工作：ACT / ASK / NEVER

每个动作**先归类**：该**自己做（ACT）**、该**停下问用户（ASK）**、还是**绝不（NEVER）**？

### ACT — 跑确定性写作门 + 机检，自己做（不烦用户）

- **claim 必有证据/过度宣称/result-card guardrail critical 门**（本技能灵魂）：`python scripts/claim_evidence_gate.py --draft draft.md
  --evidence evidence_strength.json --claim-map claim_plan.json --report claim_findings.json`——消费 result-analysis 的证据档 +
  `light.paper_claims.v1` + `_shared/evidence_contract` → 产 `light.findings.v1`：**强断言未登记、绑定 ID 不存在或只绑定 none →
  claim_evidence critical**；claim map 必须含当前 draft 的 `draft_sha256`，修稿后旧绑定不得继续通过；`checked_at/captured_at`
  不能来自未来，`source_artifacts/source_locators` 不能保留占位符、假 SHA 或私人绝对路径；实证 claim 还必须携带固定版本 result-card
  的 `locator/sha256/decision/language_strength/guardrail_summary`；`decision != CLAIM_READY`、guardrail `FAIL/UNKNOWN`、或 `WARN` 但 claim
  未写限制 → result_card_guardrail critical；措辞强于该 claim 自己的证据档 → overclaim warn；
  贡献三处漂移 → contribution_consistency warn。critical → `run_checkpoint --stage 8` exit 1。
- **诚信整体 linter**：`python scripts/draft_lint.py draft.md --final --evidence evidence_strength.json`——查残留缺口标记
  （`[MATERIAL GAP]`/`[RESULT GAP]`/TODO，终稿门要清零）+ 必备声明节（Data Availability/Ethics/CRediT/Conflicts/Funding/
  AI Use）+ SOTA 措辞邻近无显著性 + 引用台账（DOI/arXiv 抽出待 citation 核）+ `--evidence --claim-map` 逐 claim 措辞门。
  `--claims` 抽候选事实句播种 `templates/claim_passport.md`。
- **贡献三处一致**：`python scripts/contribution_consistency.py --in draft.md --json`——抽 abstract/intro/conclusion 贡献句，
  比 NUMBER-DRIFT（数字漂移）/STRENGTH-DRIFT（强度漂移）/COVERAGE-DRIFT（覆盖漂移）。**单稿内自检**（跨材料归 C2）。
- **离线机检**（无 API、纯 stdlib）：`python scripts/mechanical_check.py --file draft.md`（支持 `--latex` 剥 LaTeX）——过度
  宣称词 / AI 腔套话 / hedge 堆叠 / 被动过多 / 标点；`--evidence-map evidence_strength.json` 让强证据的强词豁免降级、强证据被
  过度 hedge 反提示 under-claim（措辞↔证据双向校准）。
- **语法/风格润色**：`python scripts/polish.py --file draft.md`（**默认离线本地规则**）；`--online` 才 opt-in LanguageTool
  （匿名限流，单文档控速，尊重 ToS）。**作者文风保护**：`style_fingerprint.py --build past*.txt --out my_style.json` 建指纹 →
  `--compare draft.txt --ref my_style.json` 标偏离，润色往作者文风靠、不抹平成模板。
- **按结构写**：用 `templates/01_imrad.md`（IMRaD + CARS 引言：痛点→gap→做法→贡献→结果预告）起稿；贡献句**动词开头、可度量**。
- **先核 argument spine 再润色**：`argument_contract.py` 检查中心问题/claim、贡献 delta 与边界、
  摘要/引言承诺是否在 Results+Discussion/Conclusion 闭合、reader path、段落自己的 evidence IDs、
  `claim_type`（RESULT/NULL_RESULT/MECHANISM/CAUSAL/SPECULATION…）、`role`（RESULT/INTERPRETATION/LIMITATION…）、
  partial/contested limitation、因果设计、机制测试、null result 精度/功效说明、post-hoc 披露和 figure-first map；它不拿“流畅”替代论证闭包。

### ASK — 停下问用户，给「证据 + 推荐 + 备选」（决策点 🧑）

| 决策点 | 何时 | 你怎么问 |
|---|---|---|
| **回炉发起 8→7（claim 无证据）**（最重要） | claim_evidence 判草稿强断言无证据档支撑 | 「摘要写了『我方法 SOTA、显著优于所有基线』，但 `evidence_strength.json` 里**没有任何证据档支撑这条**（无对应 claim / 全部 grade=none）。**建议**回 result-analysis（8→7）补/强化该 claim 的证据（算 q/效应量/CI）。回炉带『哪条 claim 缺哪种证据』——还是如实弱化为『未见显著优于』？（方向你定，绝不留无证据的强断言）」 |
| **回炉发起 8→6（实现/复现缺口）** | claim 无证据且根因是「实验根本没产出该结果」 | 「这条 claim 对应的实验**根本没跑出来**（不是分析没做，是结果缺失）。**建议**回 experiment-coding（8→6）补实验，而非回 result-analysis。带『缺哪个实验/结果』。还是先标 `[RESULT GAP]` 占位、这条暂不写进 contribution？」 |
| **过度宣称想保留** | overclaim 判措辞强于证据档（warn） | 「claim Y 证据档=**weak**（显著但小效应 d=0.2），但写了『demonstrate / 显著优于』。**建议**降到『indicate / 在本实验中略优』并加 hedge。不改的话，交付前会被 research-ethics 的措辞硬门（critical）拦。要我降级措辞吗？」 |
| **贡献三处不一致** | contribution_consistency 判 NUMBER/COVERAGE drift | 「摘要说『提升 3.1 点』但结论只说『改善了性能』（数字漂移），且摘要的『校准模块』贡献在结论找不到（覆盖漂移）。审稿人会质疑贡献缩水/夸大。**建议**三处对齐：要么都给 3.1 点、要么都不给；结论呼应每条贡献。要我对齐吗？」 |
| **审稿人视角发现硬伤** | 自审出逻辑薄弱/创新不突出/论证不足/易质疑 | 「当审稿人挑了一遍：贡献 C2 与 Smith2023 的 delta 说不清楚（创新不突出）、Results 第 3 段把相关写成因果（易被质疑）。这些**机检测不出、要你判**。**建议**改写贡献 C2 点明 delta、Results 那句改『A 与 B 负相关』。一起过一遍？」 |

### NEVER — 绝不 [NON-NEGOTIABLE]

> **这一节是红线，不可协商、不可被「先写强点好发」「审稿人不一定看得出」「差不多就行」绕过。违反任一条 = 严重失职。**

1. **绝不留 claim 无证据**：每个写进论文的强断言（SOTA/outperform/证明/显著优于/提升 X%）必须有对应证据档（result-analysis
   的 `evidence_strength.json`）。无证据的强断言 = `claim_evidence` **critical 诚信门** → 回炉补证据（8→7）或如实弱化，**绝不
   凭语感把数字/结论填进去**（无来源即标 `[RESULT GAP]`）。
2. **绝不让措辞强于证据**：措辞强度必须匹配证据档——**strong**→demonstrate/establish/证明、**moderate**→show/indicate/改善、
   **weak**→suggest/may/可能（须 hedge）、**none**→**只能报「未见显著差异 / no significant difference」**。不显著却写「趋于
   显著/有益/优于」= **Boutron spin**，绝不。`evidence_strength.json` 是「措辞不强于证据」的单一数据源。
3. **绝不让 result-card / guardrail 在写作阶段消失**：实证 claim 必须绑定 `light.result_card.v1` 的 locator+SHA-256、`decision=CLAIM_READY`、
   `language.strength` 与 `guardrail_analysis` 摘要。guardrail `FAIL/UNKNOWN` 不得写成 claim ready；guardrail `WARN` 只能限制性推进，
   必须把 `claim_impact` 写进 claim limitations 与正文局限。
4. **绝不贡献三处打架**：摘要/引言/结论的贡献点**数量、措辞、顺序、数字**要一致——别一处说三点一处说两点、别摘要给「3.1 点」
   结论只说「改善了」。虎头蛇尾（摘要的贡献结论不呼应）= 覆盖漂移。
5. **绝不写 AI 腔套话 + 过度对冲/对冲不足**：删「in conclusion / it is worth noting / 综上所述 / 值得注意的是 / 深入探讨」等
   模板腔（审稿人一眼识别）；别什么都「may possibly suggest」（确定结果写心虚 = under-claim），也别弱证据堆强词。
6. **绝不 AI 编造引用/数据/机制**：引用真实性由 citation 阶段核（本技能只登记「待核」+ 抽 DOI/arXiv 台账）；**AI 不能列作者**、
   作者对全部内容负全责、用了 AI 写作要按期刊政策披露（`references/mandatory_inclusions.md`）。
7. **绝不把机检吹成「证明了没夸大 / 论证充分」**：`claim_evidence_gate`/`mechanical_check` 查「强断言无证据档 / 措辞超档 /
   AI 腔」的**形态**；canonical 门用当前 `draft_sha256` + 精确 claim text + evidence ID，但仍会受过宽 span、语义边界和同义改写影响；**逻辑是否薄弱、创新够不够突出、论证是否
   充分、说服力强不强的终判仍需人 / 审稿人**。诚实标边界。
8. **绝不静默回炉**：写作发现 **claim 无证据（8→7）/ 实现缺口（8→6）**是**决策点**——带证据**停下问用户**（回哪 / 标 GAP 暂不写 /
   转已知局限），**绝不**自己拍板回炉，也**绝不**把无证据的强断言硬留在正文往下走。

> 自检触发词：当你想说「这结论先写强点好发 / 不显著但趋势对也写成提升 / 措辞夸张点审稿人也看不出 / 这数字大概是这么多直接填 /
> 摘要写满点结论简略点没事 / AI 腔润一润更通顺」——**停**，八成踩了 NEVER 第 1/2/3/4/5 条，或漏了 ASK 的回炉/过度宣称决策。

---

## 指令流：何时调哪个脚本（引擎已就位，亲手 selftest 到 exit 0，直接调用勿重写）

8 个脚本在 [`scripts/`](scripts/)；`claim_binding`/`claim_evidence_gate`/`draft_lint`/`contribution_consistency`/`mechanical_check` 接 `_shared`
（规范 bootstrap），`style_fingerprint`/`polish` 纯 stdlib 独立。Windows 跑前 `set PYTHONUTF8=1`。

### ① claim 必有证据/过度宣称/result-card guardrail critical 门 → critical fail exit 1（本技能灵魂）

```bash
# 消费 result-analysis 的 evidence_strength.json + result-card guardrail + evidence_contract → light.findings.v1：
python scripts/claim_binding.py --draft draft.md --evidence evidence_strength.json --claim-map claim_plan.json --as-of 2026-07-05
python scripts/claim_evidence_gate.py --draft draft.md --evidence evidence_strength.json --claim-map claim_plan.json --report claim_findings.json
# 无证据文件时：每条强断言一律视作 claim 无证据（诚信门 critical），逼你先拿证据再写：
python scripts/claim_evidence_gate.py --draft draft.md --claim-map claim_plan.json --report claim_findings.json
# 交总控聚合（stage 8 确认点，critical fail → exit 1 确定性阻断）：
python ../light-orchestrator/scripts/run_checkpoint.py --file .light/passport.yaml --stage 8 \
    --findings claim_findings.json --write --ts 2026-06-20T10:00
```

### ② 写作期机检（自检，不阻断 DAG，写的时候随手跑）

```bash
python scripts/argument_contract.py --input templates/argument-outline.example.json
python scripts/draft_lint.py draft.md --final --evidence evidence_strength.json --claim-map claim_plan.json
python scripts/draft_lint.py draft.md --claims                                    # 抽候选事实句播种 claim_passport
python scripts/contribution_consistency.py --in draft.md --json                   # 贡献三处一致(warn)
python scripts/mechanical_check.py --file draft.md --evidence-map evidence_strength.json  # 离线机检+措辞双向校准
python scripts/polish.py --file draft.md                                          # 默认离线语法/风格；--online 才打 LanguageTool
python scripts/style_fingerprint.py --compare draft.txt --ref my_style.json       # 文风偏离(保留作者声音)
```

公开 argument 示例故意含 `MISSING` claim，预期 exit 1；替换成真实 evidence IDs、section/
paragraph reader path、claim type、paragraph role、因果/机制/null/post-hoc 边界与贡献闭包后才可能 PASS。

### ③ 回炉发起方：写作发现 claim 无证据 → 送回上游修（8→7 / 8→6）

```bash
# claim_evidence_gate 判"claim 无证据" → findings 带信号词 → 总控 reroute 按 ROUTES[8] 建议回边：
python ../light-orchestrator/scripts/reroute.py --findings claim_findings.json --stage 8 --passport .light/passport.yaml
#   默认 8→7 回 result-analysis 补证据；若属实现/复现缺口（实验没产出）→ 用户改判 8→6 回 experiment-coding。
# 用户拍板回炉后落一等回边（记在目标阶段，不破拓扑）：
python ../light-orchestrator/scripts/passport.py add-back-edge --to 7 --from 8 \
    --root-cause "claim 'SOTA' 无实验支撑" --evidence-ptr "<reroute 给的指针>"   # 或 --to 6（实现缺口）
python ../light-orchestrator/scripts/passport.py validate --file .light/passport.yaml      # 回边不破拓扑 → 仍 PASS
```

各脚本 `--selftest`/`--help` 即接口；工具一手核（Writefull/Paperpal 边界 / CARS / Hyland hedging / Boutron spin / SciFact /
NeurIPS·ACL 评审准则 / LanguageTool 限流）详见 [`docs/competitors/paper-writing.md`](../../docs/competitors/paper-writing.md)。

---

## 院士级深挖：五条是及格线（蓝图 §4.3-8，不是加分项）

### ① 贡献三处一致（摘要/引言/结论措辞对齐）
三处贡献句分散在长稿首尾，是最易漂移的地方。数量/措辞/顺序/数字一致：别摘要给「提升 3.1 点」结论只说「改善了性能」（数字
漂移）、别摘要列三条贡献结论只呼应两条（覆盖漂移/虎头蛇尾）。机检 `contribution_consistency.py`，**终判人读三处对齐**。
锚：NeurIPS Checklist Q1「摘要与引言的主要 claim 是否准确反映论文的贡献与范围」。

### ② 措辞强度匹配证据强度（绝不过度宣称）
强证据强措辞（demonstrate/证明）、弱证据 hedge（suggest/may/可能）、**不显著只报「未见显著差异」**、**绝不 spin**（不显著却
称有益/趋于显著 = Boutron 实证 60% RCT 摘要的通病）。**直接消费 result-analysis 的 `evidence_strength.json`**（q/效应量/CI →
证据档）+ `_shared/evidence_contract`（Hyland hedge/booster 阶梯落成的 lint_wording，中英双语 + 否定守卫 + GRADE 词表）。
overclaim 在 stage 8 是 warn（self-check）；**critical 措辞红线是 research-ethics 交付门**。

### ③ 引言四段式（CARS move 结构）
痛点（领域重要性，CARS M1 territory）→ 现有不足（gap，CARS M2：反主张/指空白/提问）→ 洞察（你怎么填这个缝，CARS M3 occupy）→
贡献（贡献句**动词开头、可度量**：「We propose X that improves … by 3.1 points」而非「本文做了些工作」）。`templates/01_imrad.md`
立结构，脚本只查「四段在不在/贡献句有没有」，**说服力/洞察深度人判**。

### ④ 审稿人视角循环（自己当审稿人挑一遍再改）
按 NeurIPS 四维（Quality=claim 有证据撑吗 / Clarity / Significance / Originality）+ ACL「每条 claim 须有证据或标推测」自审：
**哪里逻辑薄弱 / 创新不突出（delta 说不清）/ 论证不足 / 易被质疑（相关写成因果）/ 该补引用**——挑出来再改（`references/self_review_checklist.md`
的 8 维质量 + 7 类 AI 失败模式；`references/argument_review.md` 的 Claim-Evidence-Boundary 四环）。**也借 ACL 17 条偏置启发式
反过来防自己当不公平审稿人**。这一层**机检测不出、是写作的真功夫**。

### ⑤ 院士会追问（预演）
**每个 claim 都有证据吗**（摘要说的正文撑得住吗）？**有没有过度宣称**（措辞配证据吗、不显著当亮点了吗）？**贡献三处一致吗**？
**审稿人会从哪挑**（最弱的论证在哪、最易被 desk-reject 的点）？——答不上来的，写作没到及格线。

---

## 收尾 self-check（出 verdict 前 / 回写总控前过一遍）

- [ ] 每个强断言（SOTA/outperform/证明/提升 X%）都**有对应证据档**（`evidence_strength.json`），没 claim 无证据吗？（`claim_evidence_gate` 跑过）
- [ ] `light.paper_claims.v1` 的 `draft_sha256` 是当前草稿 UTF-8 SHA-256 吗？修稿后旧 claim map 有没有被挡住？
- [ ] `checked_at/captured_at/updated_at` 是否都是真实已发生时间？`source_artifacts/source_locators` 是否都是公开交接包内相对路径，且 SHA-256 不是占位符/假值？
- [ ] 每条实证 claim 都绑定了 result-card locator/SHA-256/`decision=CLAIM_READY`/`language_strength`/`guardrail_summary` 吗？guardrail `WARN` 的 `claim_impact` 是否进入 claim limitations 与正文局限？
- [ ] 每条 claim 的 `claim_type` 与每段 `role` 合法并匹配章节职责吗？Results 没偷写因果/机制推测，Discussion 没把推测装成结果吗？
- [ ] 因果 claim 有 identification strategy + causal design locator，机制 claim 有机制测试，null/negative result 有 CI/功效/可排除效应大小说明，post-hoc claim 有披露吗？
- [ ] 措辞强度**匹配证据档**吗？不显著的**只报「未见显著差异」**、没 spin（趋于显著/有益）吗？
- [ ] 贡献**三处（摘要/引言/结论）一致**吗（数量/措辞/数字/覆盖，没漂移）？
- [ ] 引言**四段式**清楚吗（痛点→不足→洞察→贡献，贡献句动词开头可度量）？
- [ ] **当审稿人挑了一遍**吗（逻辑薄弱/创新/论证/易质疑/补引用）？最弱的论证补强了吗？
- [ ] 残留 `[MATERIAL GAP]`/`[RESULT GAP]`/TODO **清零**、必备声明（Ethics/CRediT/AI Use…）齐全吗？（`draft_lint --final`）
- [ ] 去了 AI 腔 / 被动过多 / hedge 堆叠吗？保留了作者文风（没改成标准学术腔）吗？
- [ ] 发现 claim 无证据的，**停下问用户**回 result-analysis（8→7）/ experiment-coding（8→6），没静默留无证据强断言吗？
- [ ] 没把机检**吹成「证明了没夸大/论证充分」**吧？（逻辑/创新/说服力终判需人/审稿人）

---

## 名实对齐（诚实，不吹成卖点）

**真增量（v2 兑现，已 selftest + E2E 实测）**：⓪ **Round 3 current-draft + result-card/guardrail + paragraph contract 硬化**：
`claim_binding.py` 要求 `light.paper_claims.v1` 绑定当前 draft 的 `draft_sha256`，并核查核验时间、source path/hash 与 locator 是否真实可交接；修稿后旧 claim map、未来时间、占位符、假 SHA 或私人绝对路径都会使 `claim_evidence`
critical；实证 claim 还必须携带固定版本 result-card 的 locator/SHA-256、`decision=CLAIM_READY`、`language_strength` 与 `guardrail_summary`，guardrail `FAIL/UNKNOWN` 或 `WARN` 未写限制会进入 `result_card_guardrail` critical，防止 result-analysis 的 `guardrail_analysis.claim_impact` 在写论文时消失；`argument_contract.py` 增 `claim_type`/paragraph `role`，并机检 causal/mechanism/null/post-hoc 的设计、测试、精度/功效与披露缺口，防止 Results 把推测/解释冒充确定结果。① **claim 必有证据/过度宣称/result-card guardrail critical 门 producer**（`claim_evidence_gate.py`，
**v2 净新增接线**，照 result-analysis `stat_rigor_gate`/experiment-coding `repro_gate` 同构）——**消费 result-analysis 的
`evidence_strength.json` + `_shared/evidence_contract`** → 产 `light.findings.v1`（producer=paper-writing）：**草稿强断言无
任何证据档支撑 → claim_evidence critical**（对齐 `STAGE_GATES[8]=[claim_evidence,overclaim]`），措辞超档 → overclaim warn，
贡献漂移 → contribution_consistency warn，被 `run_checkpoint --stage 8` 聚合 exit 1。② **本技能是 8→7 / 8→6 回边发起方**——
写作发现 claim 无证据 → findings 带「claim/证据/支撑」信号 → reroute 建议 **8→7** 回 result-analysis 补证据（默认）/ **8→6**
回 experiment-coding 补实验（实现缺口）。③ **与 C1/C2 诚实分工、共用引擎不重造**：claim_evidence/overclaim 用同一个
`_shared/evidence_contract.lint_wording`（研究伦理的交付红线也用它）——**一套 lint_wording、两消费方（paper-writing 写作自检
warn vs research-ethics 交付 critical）**；贡献三处一致是单稿内自检（warn），跨材料一致性归 C2。④ **港 v1 五脚本修 bootstrap/命名**：
`draft_lint`/`contribution_consistency`/`mechanical_check` 修硬编码 `../../_shared`→规范 bootstrap，`m06/m08`→`result-analysis/
paper-writing`；`polish` LanguageTool 端点状态**一手核**（限流 + 劝退自动化）→ **改默认离线、`--online` opt-in**。

**裸模型本就会的（不吹）**：「写论文别过度宣称」「贡献三处对齐」「引言讲痛点→gap→贡献」「当审稿人挑一遍」「去 AI 腔」——裸
Opus 都会说，**近零增量**。本技能价值 = ① **把「claim 无证据」落成确定性 critical 机读门 + 确定性阻断**（裸模型嘴上说「要有
证据」，手上还是写无证据的强断言；编排器读不了它的「嘴上说」，读 `light.findings.v1` 的 verdict）；② **措辞↔证据机检消费同一
`evidence_strength.json`**（不是提醒「别夸大」，是真比对「这条 claim 证据档=weak 却用了 demonstrate」）；③ **claim 无证据 →
机读 findings + 根因回炉发起**（paper-writing 是 8→7/8→6 回炉枢纽，裸模型无此非线性编排闭环）；④ **离线确定性、零本地库/零付费 key**
（默认离线机检，LanguageTool 仅 opt-in）。

**诚实落后项（已知没做到）**：
1. **机检措辞 ≠ 证明无夸大**：lint 抓「强断言无证据档 / 措辞超档」的**形态**。现在由
   `light.paper_claims.v1` 做精确 text span + evidence claim ID + 当前 `draft_sha256` 绑定，未登记强断言或旧稿 claim map fail closed，**不再用全文最高档兜底**；
   但过宽 span、同义改写与 claim boundary 仍需人审，且**逻辑薄弱、创新够不够、论证充不充分、说服力强不强的终判仍需
   人/审稿人**。
2. **claim_evidence 核「证据有无/强度」非「证据真伪」**：只核「作者给没给证据档、措辞配不配那个档」，**不核结论对不对**（那要复现/
   同行）。与 SciFact（核 claim 真假）不同。
3. **overclaim 在 stage 8 是 warn**（spec §4.2）：写作时软化提示；**critical 措辞红线是 research-ethics 交付门**（`conclusion_overclaim`）。
   两套严重度、两语境，**非两套 lint**。
4. **贡献三处一致是 warn 自检非跨材料复核**：单稿内 abstract/intro/conclusion 对齐；启发式抽贡献句会漏/误报，离线 semantic_sim 对纯
   同义改写偏弱；**跨阶段/跨材料一致性归 C2 consistency**。
5. **引言四段/审稿人视角是人判主场**：CARS 结构脚本查「四段在不在/贡献句有没有」，**说服力/创新突不突出/论证充不充分**机检不了，
   审稿人视角循环是写作真功夫。
6. **润色边界**：`mechanical_check`/`polish` 是表层（语法/风格/AI 腔），**不改科学内容**；`polish` 在线端点限流 + 官方劝退自动化 →
   **默认离线**，`--online` 仅单文档控速 opt-in、不在 selftest 打端点；**不复述未实测的具体 HTTP 码**（铁律 2）。文风指纹是统计画像，
   「改成什么更好」仍作者/审稿人判。
7. **引用真实性不在本技能**：本技能只登记「待 citation 核」+ 抽 DOI/arXiv 台账；**防幻觉引用的硬核验归 citation 阶段（stage 10）**。

> 标准产出工件：论文初稿/终稿（IMRaD/会议模板）· `claim_plan.json`（`light.paper_claims.v1`，含当前 `draft_sha256`，claim↔证据↔来源↔result-card guardrail↔section coverage）· `argument-outline.json`（claim type/paragraph role/causal·mechanism·null·post-hoc 边界）· `claim_findings.json`
> （claim 必有证据/过度宣称/result-card guardrail 门）· 润色报告（机检 findings + 文风偏离）。claim 无证据 → 回 result-analysis（8→7）/ experiment-coding（8→6）；
> 图规划交 figure（stage 9）· 引用核验交 citation（stage 10）· 排版编译交 typesetting（stage 11）· 交付前 research-ethics 横切复核措辞红线。

---

## 参考（三级渐进披露：需要时再读）

- 真实资源闭环：[`paper-writing-resource-map.md`](paper-writing-resource-map.md)（venue/claim plan→证据→section→reviewer loop→门→下游）
- 对标真相源：[`docs/competitors/paper-writing.md`](../../docs/competitors/paper-writing.md)（真同类 skill 重搜 / Writefull·
  Paperpal 边界 / LanguageTool 限流 / Swales CARS / Hyland hedging / Boutron spin / SciFact / NeurIPS·ACL 评审准则 / 结构化摘要，
  8 个真同类 skill + 机制锚 + 横切可借机制 + 超越点 + 诚实边界）
- 引擎脚本：[`scripts/`](scripts/)——各 `--selftest`/`--help` 即接口；`claim_binding.py`（逐 claim text/evidence/source 绑定）·
  `claim_evidence_gate.py`（claim 必有证据/过度宣称/result-card guardrail critical 门）
  是 findings 核心，`draft_lint.py`/`contribution_consistency.py`/`mechanical_check.py`/`style_fingerprint.py`/`polish.py` 是写作期机检
- 深层论证 + 审稿人视角：[`references/self_review_checklist.md`](references/self_review_checklist.md)（8 维质量 + 7 类 AI 失败模式红线）·
  [`references/argument_review.md`](references/argument_review.md)（Claim-Evidence-Boundary + Hedging 阶梯 + 章节分工 + AI 披露）
- 诚信门 + 必备声明：[`references/integrity_gate.md`](references/integrity_gate.md)（claim 抽样配额 + 分类核查 + 回炉）·
  [`references/mandatory_inclusions.md`](references/mandatory_inclusions.md)（Ethics/CRediT/AI Use 等声明模板）· [`references/guideline_map.md`](references/guideline_map.md)（reporting 指南）
- 结构模板：[`templates/01_imrad.md`](templates/01_imrad.md)（IMRaD+CARS 引言）· [`templates/06_conference.md`](templates/06_conference.md)（顶会）·
  [`templates/claim_argument_plan.json`](templates/claim_argument_plan.json)（canonical claim/argument plan）·
  [`references/claim_argument_plan.md`](references/claim_argument_plan.md)（契约与 reverse outline）·
  [`templates/claim_passport.md`](templates/claim_passport.md)（人读台账）
- 地基契约：[`_shared/README.md`](../../_shared/README.md)（**`evidence_contract`** 核心消费 · `semantic_sim` · `findings_schema` · `gate_runner` · 规范 bootstrap）
- 上游/下游：[`light-result-analysis`](../light-result-analysis/)（stage 7，`evidence_strength.json` 上游；8→7 回炉目标）·
  [`light-experiment-coding`](../light-experiment-coding/)（stage 6，8→6 回炉目标）· [`light-research-ethics`](../light-research-ethics/)（交付前横切，
  `claim_evidence_bind` 共用 evidence_contract 卡措辞 critical）· [`light-consistency`](../light-consistency/)（跨材料一致性常驻）·
  [`run_checkpoint.py`](../light-orchestrator/scripts/run_checkpoint.py)（stage 8 聚合 exit 1）· [`reroute.py`](../light-orchestrator/scripts/reroute.py)（ROUTES[8] 出边 8→7/8→6）·
  figure（stage 9，据 claim 规划图）· citation（stage 10，引用核验）
