---
name: paper-workflow
description: >
  经管 / 社科实证论文全流程 meta-orchestrator：把选题、设计、数据、估计、方法闸门、
  表图、写作、去 AI 味、质量门、修订、投稿与复盘编排成 Stage 0–9 可断点续跑流水线。
  本 skill 不重复实现子能力，而是按阶段调用既有 skill 或并行 subagent，并在 Stage 3–4
  路由 Python/StatsPAI、Stata、R 三种分析后端。触发：/paper-workflow、帮我写一篇实证论文、
  从选题到投稿、端到端 empirical paper、已有 proposal/数据/初稿要推进到投稿，或明确要求
  用 Stata / R/fixest / Python-StatsPAI 完整复现。
allowed-tools: Skill, Agent, Read, Write, Edit, Glob, Grep, Bash, AskUserQuestion, WebSearch, WebFetch, NotebookEdit
argument-hint: "[研究方向 | proposal.md | 数据路径 | main.tex 目录] [目标期刊(可选)]"
---

# Paper-WorkFlow — 经管 / 社科实证论文全流程总编排器

## Overview

本 skill 只做总编排：把一篇实证论文拆成 **Stage 0–9 + Method Gate + Draft Quality Gate**，
用 `Skill` 调既有 skill、用 `Agent` 派并行 subagent；主代理只管规划、路由、状态、审阅和交付。

两条纪律贯穿全程：① 子代理写盘，只回 ≤10 行状态摘要，主代理不吞大文件；② 用
`workflow_state.json`、stage passport、handoff 和快照保证固定顺序、断点续跑与交互档位。

> **能调用就不要重写。** `skills/67-econfin-workflow-toolkit/` 已覆盖全流程；本编排器只负责把
> 47 个 skill 按正确顺序、上下文和人类决策点串起来。调用表与逐阶段手册按需读
> [`references/skill-map.md`](references/skill-map.md) 与 [`references/stage-playbook.md`](references/stage-playbook.md)。

---

## 这条流水线（固定主线，可按入口跳入）

| Stage | 阶段 | 主要调用的 skill（位于 `67-econfin-workflow-toolkit/`，除非另注） | 产出落盘 |
|---|---|---|---|
| **0** | Intake & Setup | *(编排器本体)* | 工作区、`workflow_state.json`、入口路由 |
| **1** | 选题与设计 | `econfin-idea-finder` → `novelty-check` → `significance-search` → `journal-digest` → `econfin-proposal` | `01_proposal/proposal.md` |
| **2** | 数据 | `data-fetcher` → `data-cleaning` + sample/estimand audit | `02_data/clean.parquet` + `codebook.md` + `sample_audit.md` |
| **3** | 计量识别、估计与方法闸门 | **分析后端路由**：默认 Python/StatsPAI（MCP 优先：`detect_design→preflight→recommend→fit(as_handle)→audit_result→sensitivity_from_result→bibtex`），也可按用户/复现要求切到 Stata（`00.2` `.do` pipeline）或 R（`00.3` tidyverse/fixest/Quarto pipeline）；再按设计配 `did-analysis` / `iv-estimation` / `rdd-analysis` / `synthetic-control` / `panel-data` / `ols-regression` / `time-series` / `ml-causal` + empirical audit + research-grade methods pack + design gate cards | `03_analysis/` 代码 + `design_register.md` + `method_gate.md` + `00_meta/evidence_ledger.md` |
| **4** | 表与图 | 按同一分析后端生成出版级表图：Python/StatsPAI `regtable`/`paper_tables`/`collect`，Stata `esttab`/`outreg2`/`collect`，R `modelsummary`/`etable`/Quarto；均需 Word/Excel/LaTeX 同出 + PDF/PNG 图 | `04_results/*.{tex,docx,xlsx}` + `*.pdf/png` |
| **5** | 写作初稿 | `paper-writer` | `05_draft/main.tex` + `ref.bib` |
| **6** | 全流程打磨 | `paper-pipeline`（内部跑 polish→self-revise→style→polish→reference-verify） | 打磨后的 `main.tex` |
| **7** | 语言与去 AI 味 | `readability` / `fix-chinese` + （`44`/`47`/`48`/`49` 去 AIGC 集合） | 去味后的稿件 |
| **8** | 模拟评审与修订 | `referee-report` → `paper-referee-revise`（或 `paper-self-revise`） | 修订稿 + response letter |
| **9** | 选刊与投稿 | `paper-submission` + `reference-verify`（终审） | 期刊清单 + cover letter |
| **—** | 复盘与交付 | *(编排器本体)* | `FINAL_REPORT.md` + 打包交付物 |

> 完整阶段细节、每阶段的 plan→execute→review→revise 微循环、subagent 派发模板，全部在
> [`references/stage-playbook.md`](references/stage-playbook.md)。**主代理在进入某阶段时才去读
> 对应章节**（渐进式加载，省上下文）。

> **双硬闸门 = 方法闸门 + 初稿质量门。** Stage 3 结束必须先过
> [`research-grade-methods.md`](references/research-grade-methods.md) 的 **Method Gate**：设计注册、
> 最低诊断证据、稳健性矩阵与复现脚本齐了，且
> [`design-risk-ledger.md`](references/design-risk-ledger.md) 把适用识别威胁、选择性报告、外部效度、SUTVA/溢出
> 和 attrition 风险逐项关掉或降级，才能把结果送进表图和写作。Stage 7 跑完再过
> **Draft Quality Gate**：结构完整、识别可信、表图齐备、语言无 AI 味的初稿，必须由独立 critic
> 按 7 维 rubric 打分达标，才算「可投稿级初稿」。**任何闸门未达标都按回退指令重做**，绝不把
> 「流程跑完」当成「研究可信」。

---

## Phase 0：Setup（调用任何子 skill 前完成）

1. **取北京时间**：`TZ='Asia/Shanghai' date '+%Y-%m-%d %H:%M'`，记为 `NOW`。
2. **判定入口**，不要一律从 Stage 1 开始：想法→1；成形 proposal→2；已清洗数据+设计→3；
   已有结果/表图→5；`main.tex`→6；初稿+审稿意见→8；成稿投稿→9。能从 `$ARGUMENTS`
   后缀和内容推断就别问；否则一次 `AskUserQuestion` 问清。
3. **建工作区**：在用户目录或当前目录创建 `paper_workspace/{研究短名}_{NOW紧凑时间戳}/`，
   运行 `assets/init_workspace.sh`。同名目录另建，不覆盖。目录、`00_meta/` 状态文件、entry routing、
   passport、pipeline status、handoff、analysis backend、evidence/claim/citation 台账见
   [`references/workspace-and-state.md`](references/workspace-and-state.md)；交付物优先用 [`templates/`](templates/)。
4. **写 Stage 0 账本**：`00_meta/entry_routing.md` 记录入口、材料、假设、人类决策分支；
   `00_meta/stage_passport.md` 和 `workflow_state.json.orchestration` 记录 handoff / 断点恢复指针。
5. **一次问清四件套**：交互档位（`全自动` / `阶段确认` 推荐 / `全程交互`）、目标期刊、
   语言、分析后端（`python-statspai` 推荐 / `stata` / `r`；规则见
   [`references/analysis-backends.md`](references/analysis-backends.md)）。若用户要求无人值守或参数足够，
   自动填保守缺省并写入 `00_meta/intake.md`、`00_meta/analysis_backend.md`、`workflow_state.json.decisions`。
6. **初始化状态**：`workflow_state.json` 从 [`assets/workflow_state.template.json`](assets/workflow_state.template.json)
   复制，填 `project` / `orchestration` / `analysis_backend`；Stage 状态用
   `pending|in_progress|done|skipped`；`empirical_audit`、`method_gate`、`evidence_governance`、
   `integrity_audit`、`design_risk`、`quality_gate`、`replication_pack` 起始为 `pending`。
   每阶段开始置 `in_progress`，完成置 `done` 并刷新 `last_updated_beijing`。
7. **续跑先刷新事实**：已有工作区时先读 passport 和 latest handoff，再查 `git status`、当前产物与 gate 证据；
   handoff 只是指针，缺 fresh evidence 不得宣称完成。
8. **Setup 后直接执行**：不要为“计划”单独求批准；阶段确认/全程交互只在阶段闸门处暂停。

---

## 多代理 + 上下文保护协议（贯穿所有阶段）

主代理上下文是**最稀缺资源**：任何"重读大文件、跑长代码、扫一堆文献"的脏活都**派给 subagent（`Agent`）或子 skill**，主代理只持有指针与状态。硬规则：

1. **子代理自己写盘，只回传状态摘要**：给每个 subagent 显式指定**输入 / 输出文件**，要求它处理完立即写盘、只回传 ≤10 行摘要（做了什么 / 写到哪 / 关键数字 / 是否通过 / 下一步）。**严禁把完整产出回传主代理。**
2. **为子代理放行 Read + Write + Bash**（必要时含 Skill），让它独立闭环。
3. **能并行就并行**：同阶段内彼此独立的任务（多个稳健性、多个候选期刊、多份机制检验）一次性并行派发（每批 ≤10；选题漏斗沿用 `idea-finder` 的 `PARALLEL_BATCH_SIZE=5`）；有依赖的串行。
4. **每阶段是一个微循环** `plan → execute → review → revise`；重活阶段（1 选题、3 估计、6 打磨、8 评审）尤其要派**独立 critic subagent** 做对抗式审阅再修订。
5. **子 skill 调用**：轻量且需主线上下文的（如 `paper-style` 顺着同一份 `main.tex`）直接在主代理调；重量可隔离的（多路文献扫描、批量稳健性）派 subagent，并在其 prompt 里**强制按下节「子 skill 调用协议」加载**，绝不许凭记忆脑补（参考 `idea-finder` 强制每个 subagent 加载 `econfin-proposal`+`novelty-check`）。
6. **日志**：每阶段把「调用了哪些 skill / 派了哪些 agent / 产出哪些文件 / 关键决策」追加到 `logs/stage_<N>.md`，并同步 `00_meta/stage_passport.md` 与 `00_meta/pipeline_status.md`。
7. **交接**：阶段切换 / 长暂停 / 上下文变薄 / 并行 agent 接手前，在 `00_meta/handoff/` 写 handoff card 并把路径写入 `workflow_state.json.orchestration.latest_handoff`；下一位 agent 先刷新现实再继续。

---

## 子 skill 调用协议（怎么把被编排的 skill 真正跑起来）

子 skill 是**仓库内的文件夹**，不保证在运行时注册为可被 `Skill` 工具直接触发。**权威细节（注册名
对照表、输出路径重定向）见 [`references/skill-map.md`](references/skill-map.md) §0**；每次调用按此优先级：

1. **优先 `Skill` 工具**：`Skill(skill="<注册名>", args=...)`。**注册名 = 子 skill `SKILL.md` 的 `name:`
   字段，不一定等于文件夹名**（大小写/改名差异表见 skill-map §0.1）——用注册名，别用文件夹名猜。
2. **报「not found」立刻退回 `Read` 内联执行**（稳路径，永远可用）：`Read` 该 SKILL.md 正文当本步操作
   手册逐步执行；重量步骤把「`Read` 这个 SKILL.md 并按它执行」写进 subagent 的 prompt。**不要反复重试，
   也不要凭记忆脑补子 skill 的逻辑**（这正是 `idea-finder` 反复警告的劣化）。
3. **两个子 skill（`econfin-idea-finder`、`journal-digest`）在其 SKILL.md 里硬编码了仓库外 Windows 输出
   路径，调用时必须改写**到工作区内（候选→`01_proposal/candidates/`、期刊摘要→`01_proposal/journal_digest.md`）；
   细节见 skill-map §0.2，模板见 [`references/subagent-templates.md`](references/subagent-templates.md)。

> **派 subagent 调子 skill 时，SKILL.md 路径必须是仓库内完整路径**——subagent 的工作目录可能与主
> 代理不同，给错路径它就找不到文件、转而脑补，产出不可复现的劣化结果。

---

## 阶段执行协议（每个 Stage 都按这个走）

进入任一阶段按固定四步（细节在 playbook 对应章节）：

1. **打横幅**，让用户始终知道流水线在哪：

   ```
   ════════════════════════════════════════
     Stage N/9 · <阶段名>  —  <一句话目的>
     调用：<本阶段要用的 skill 列表>
   ════════════════════════════════════════
   ```

2. **置 `in_progress`** → 读 [`references/stage-playbook.md`](references/stage-playbook.md) 对应章节 → 按其 plan→execute→review→revise 跑（该用 `Skill` 用 `Skill`、该派 `Agent` 派 `Agent`，全程守上面的上下文保护协议）。
3. **冲突 / 退化检查**（沿用 `paper-pipeline`）：每阶段前后 `Glob` 一次 `*冲突副本*` / `*conflicted copy*`，发现就停下让用户定夺哪份为准；每阶段末把关键产物快照进 `backups/after_stage<N>/` 作为回滚路径。若 `Skill` / `Agent` / 网络 / MCP / Stata/R/Python/Zotero 不可用，按 [`references/runtime-fallbacks.md`](references/runtime-fallbacks.md) 选 fallback，影响写入日志、`decisions` 与对应闸门，不可把工具缺失伪装成已验证。
4. **阶段闸门**：置 `done` → 按交互档位决定是否暂停——`全自动` 直接进下一阶段；`阶段确认`（缺省）输出**摘要卡**（产出清单 + 关键数字 + 红旗 + 下阶段计划）等放行；`全程交互` 再做一次阶段级确认。遇**硬阻断**（平行趋势不过、IV 弱工具、查新撞车、数据取不到）不要硬往下走——按 playbook「失败回退」分支处理（换识别策略 / 换样本 / 退回 Stage 1 改设计），并在摘要卡里**显著标红**说明发生了什么、采取了什么回退。

---

## 研究级方法闸门（Method Gate）—— Stage 3 之后、Stage 4 之前强制执行

Stage 3 的目标不是「跑出显著系数」，而是把识别设计、估计量、诊断证据、设计风险与稳健性矩阵落成**可审计产物**。
进入前加载本闸门 references——[`research-grade-methods.md`](references/research-grade-methods.md)（最低证据包）·
[`design-gate-cards.md`](references/design-gate-cards.md)（设计卡 / hard fail / claim 降级）·
[`empirical-audit.md`](references/empirical-audit.md)（样本对齐）· [`inference-and-uncertainty.md`](references/inference-and-uncertainty.md)（推断口径）·
[`mechanism-and-channels.md`](references/mechanism-and-channels.md)（机制三分类）· [`design-risk-ledger.md`](references/design-risk-ledger.md)（风险台账）·
[`analysis-backends.md`](references/analysis-backends.md)（后端选择，主后端为 python-statspai 再加 [`statspai-analysis.md`](references/statspai-analysis.md)）——逐项完成并落盘：

1. **设计注册** `03_analysis/design_register.md`：estimand、处理定义、比较组、识别假设、主 / 替代估计量、失败回退。
2. **样本审计** `02_data/sample_audit.md`：estimation sample、treated/control 数、treatment timing、missingness/balance/overlap、cluster level 与变量构造对齐 estimand。
3. **最低证据包**：按设计分支补齐必需 artifact（交错 DiD→CS/SA/BJS group-time 或事件研究稳健估计；RDD→bandwidth+robust bias-corrected CI+density/covariate continuity；DML/HTE→cross-fitting+nuisance diagnostics+overlap+seed stability；其余见 methods pack）。推断口径按 `inference-and-uncertainty.md` 把聚类层级 / few-cluster / 多重检验 / 弱工具区间定死并写 `03_analysis/inference_report.md`；有机制主张按 `mechanism-and-channels.md` 分类、把中介移出主设定、证据落 `03_analysis/mechanism/`。
4. **方法闸门报告** `03_analysis/method_gate.md`：逐项列必需证据是否齐、路径、是否 `PASS`，填 **Design Gate Card** 与最强允许 claim 等级。`NOT PASS` 不得进入 Stage 4，须回 Stage 1/2/3 修设计 / 数据 / 估计。
5. **Design risk ledger** `03_analysis/design_risk_ledger.md`：逐项审计 OVB、反向因果、选择、测量误差、spillover/SUTVA、坏控制、specification search、外部效度、attrition、选择性报告。任何 blocking threat 未关 → `workflow_state.json.design_risk.status=not_pass`、Method Gate 不得 `PASS`；若风险只限外推，把 claim consequence 写进 ledger 与 evidence ledger。
6. **Evidence ledger** `00_meta/evidence_ledger.md`：每个 manuscript claim 连到 estimand、样本审计、结果文件、稳健性、表图、脚本与允许措辞；摘要 / 引言 / 结果 / 结论 / cover letter 的 claim 不得强于 ledger 的 `Strength`。
7. **治理与透明度 hard flags**：按 [`data-governance.md`](references/data-governance.md)（受限数据 / PII / IRB/DUA / 存档边界）与 [`design-transparency.md`](references/design-transparency.md)（预分析 / MDE / 研究者自由度）检查；关键材料缺失时方法闸门不得静默放行。
8. **写入状态**：更新 `workflow_state.json` 的 `analysis_backend` / `empirical_audit` / `method_gate` / `evidence_governance` / `design_risk` / `decisions`（分析后端、主设计、主估计量、适用威胁、blocking threats、缺失 artifact、最强 claim 等级、open discrepancies、是否放行）。
9. **机械闸门自检**：跑 `python3 scripts/check_workspace_gates.py <workspace>`，机械校验「某闸门标了 `pass`/`ready` 但 artifact 不在盘上、或上游闸门未过（质量门不得松于方法闸门）」及 Stage 0 route / stage passport / latest handoff 路径一致性；返回非零必须补齐再放行。这是对 critic 主观判定的机械兜底，不替代它。

**质量门可严于但不得松于方法闸门**：`method_gate.md` 未过 → 初稿质量门「识别可信度」不得达标；`evidence_ledger.md` 有影响主结论的 open discrepancy → 质量门与投稿包不得标 ready。这把现代实证的 reviewer 标准前置到写作之前，避免事后用语言包装弥补方法硬伤。

---

## 初稿质量门（Draft Quality Gate）—— 把「高质量」从口号变成可验收的闸门

Stage 7 结束、Stage 8 开始前**强制插入**：不靠主代理自我感觉，而是派一个独立「顶刊 AE」critic subagent，按
[`references/quality-rubric.md`](references/quality-rubric.md) 的 7 维评分卡给当前初稿打分（派发模板见
[`subagent-templates.md`](references/subagent-templates.md) §QG）：

1. critic 读 `07_dehumanize/main.tex`（含表图、`ref.bib`）+ `01_proposal/proposal.md`（对照贡献承诺）+ `03_analysis/results/summary.md`（对照真实结果），逐维打分写入 `00_meta/quality_scorecard.md`，只回传总分 / 各维分 / 是否达标 / 最关键 3 条短板。
2. **7 维**（各满分 10，细则见 rubric）：① 选题与贡献锋利度 ② 识别可信度 ③ 稳健性完整度 ④ 结果与解读克制度 ⑤ 写作与结构 ⑥ 引用真实性与文献定位 ⑦ 可复现性。
3. **达标线**：每维 ≥7 **且**总分 ≥56/70 **且**第②③⑥维（识别 / 稳健 / 引用）无致命红旗，**且** `00_meta/claim_integrity_audit.md` 的 `pre-review` 无 blocking finding → 标 `quality_gate=pass`、`draft_milestone=done`，进入可选 Stage 8–9。
4. **未达标**按 rubric「短板 → 回退阶段」映射重做（识别→Stage 3、贡献单薄→Stage 1、写作→Stage 5/6、AI 味→Stage 7、引用→reference-verify），**最多回退 2 轮**；2 轮仍卡某维则记「已知短板」标红交用户裁决是否带病投稿。
5. 每轮打分追加进 `logs/quality_gate.md`，让用户看到分数随修订上升（审计轨迹）。

> 质量门**不是**重跑 Stage 6 打磨、也不替代 Stage 8 评审——它只做一件事：按统一 rubric 量化「这份初稿够不够格」并决定放行还是回炉。

**Claim Integrity Audit（配套引用 / 数字 / claim 忠实度检查）**：Stage 7→8 加载
[`integrity-and-claim-audit.md`](references/integrity-and-claim-audit.md)，用 [`templates/claim_integrity_audit.md`](templates/claim_integrity_audit.md)
写 / 刷新 `00_meta/claim_integrity_audit.md`。**pre-review**：审计摘要、引言贡献段、结果主题句、结论、cover letter 的所有数值与因果 claim，每条定位到 evidence ledger row、结果文件 / 脚本、表图或可核引用；`major_distortion` / `unsupported` / `constraint_violation` 及影响主结论的 `retrieval_failed` → `workflow_state.json.integrity_audit.status=not_pass`、质量门不得 `pass`。**final-check**（Stage 9 投稿前）中央 claim 不许抽样，`replication_pack.status=ready` 要求 `integrity_audit.status=pass` 且 `blocking_findings=[]`。把 `checked_claims` / `unsupported_claims` / `unverified_citations` / `blocking_findings` / `last_audit` 写入 `workflow_state.json.integrity_audit`，跑 `python3 scripts/check_workspace_gates.py <workspace>` 抓状态矛盾。

---

## 收尾：复盘与交付

所有目标阶段 `done`（**且初稿质量门已 `pass`**）后，主代理在工作区根目录产出 **`FINAL_REPORT.md`**
（用 [`templates/FINAL_REPORT.md`](templates/FINAL_REPORT.md) 实例化），含：① 一页流水线复盘表（每 Stage 调用 / 产出 /
关键数字 / 回退分支）· ② 方法闸门报告（链接 `03_analysis/design_register.md`+`method_gate.md`：主设计 / 主估计量 /
最低证据包 / 缺失与回退史）· ③ 初稿质量门评分卡（链接 `00_meta/quality_scorecard.md`：7 维终评分 + 达标判定 + 回退史）·
④ 交付物清单（带相对路径：proposal / 清洗数据+codebook / 分析代码 / 出版级表图 / `main.tex`+`ref.bib` /
response letter / 期刊清单+cover letter）· ⑤ 可复现说明（`REPLICATION.md`、环境依赖、一键重跑命令、来源与版权、
DAS、存档计划、重跑耗时、数据治理红旗）并更新 `workflow_state.json.replication_pack` · ⑥ 下一步建议（还差哪些稳健性 +
投稿前检查清单）。最后把打包路径告知用户。**全程无需人工干预即可从 Setup 跑到交付**（`全自动` 档位）；
其余档位只在阶段闸门处征求放行。

---

## 关键约束（务必遵守）

- **绝不替子 skill 重新发明轮子**：识别策略、表格规范、查新、审稿口吻都在既有 skill 里，本编排器只在对的时点把对的 skill 喂对的输入。
- **绝不伪造数据 / 结果 / 文献**：引用核验交给 `reference-verify` / StatsPAI `bibtex`（`paper.bib` 唯一真源），数据交给 `data-fetcher`，计量结论以真实运行为准；后端选择见 [`analysis-backends.md`](references/analysis-backends.md)、默认路径见 [`statspai-analysis.md`](references/statspai-analysis.md)。
- **绝不贴空方法标签**：DiD/IV/RDD/SDID/DML/causal forest 等必须对应 [`research-grade-methods.md`](references/research-grade-methods.md) 与 [`design-gate-cards.md`](references/design-gate-cards.md) 的证据包；缺 `method_gate.md`、闸门未过或 ledger 不允许该强度，就不得写成主因果发现。
- **绝不让估计样本漂移**：`sample_audit.md` 未说明 raw→clean→estimation 的 N、drop 原因、treated/control 数、missingness/balance/overlap 与聚类层级时，不得宣称已过方法闸门。
- **绝不让不确定性量化错位**：聚类层级 ≥ 处理分配层级；G≲30–50 用 wild bootstrap / CR2 / 随机化推断；多 outcome / 子样本要预指定或族内校正；弱工具用 AR/tF 区间——口径写进 `inference_report.md`，缺则按 [`inference-and-uncertainty.md`](references/inference-and-uncertainty.md) 在质量门封顶。
- **绝不把机制当主回归的赠品**：按 [`mechanism-and-channels.md`](references/mechanism-and-channels.md) 分清描述性分解 / 因果中介 / 异质性，中介绝不进主设定，措辞退到证据支持的档位。
- **绝不把识别威胁留在散文里**：OVB、反向因果、选择、坏控制、spillover/SUTVA、外部效度、attrition、specification search、选择性报告必须进 [`design-risk-ledger.md`](references/design-risk-ledger.md) 与 `03_analysis/design_risk_ledger.md`；有 blocking threat 时 Method Gate 不能 `PASS`。
- **人类决策点不可跳过**（除非 `全自动` 档位且已显式授权）：定标题、定目标期刊、识别策略拍板、投稿终审——在阶段闸门处守住。
- **数据治理不可绕过**：受限数据、PII、IRB/DUA、许可证、archive boundary 按 [`data-governance.md`](references/data-governance.md) 记录；公共复现包不得含不可公开材料。
- **运行时退化必须披露**：工具 / 网络 / MCP / 统计软件缺失时按 [`runtime-fallbacks.md`](references/runtime-fallbacks.md) 退化执行；影响最低证据包或复现的必须降低闸门状态/分数，不得把工具缺失伪装成已验证。
- **claim 忠实度必须单独验**：citation 存在 ≠ claim 忠实。Stage 7→8 与 Stage 9 按 [`integrity-and-claim-audit.md`](references/integrity-and-claim-audit.md) 审计数字、引用、因果措辞与 forbidden wording；有 blocking finding 时质量门与投稿包都不得 ready。
- **引用存在性与时序完整性也必须单独验**：先确认引用真实存在且引对（DOI 解析 / 撤稿筛查 / 版本 / 无 citation laundering）与无时序穿越（look-ahead / real-time vs final vintage / 训练-测试切分 / 样本期 vs 论断期），按 [`citation-and-temporal-integrity.md`](references/citation-and-temporal-integrity.md) 逐项落 `00_meta/citation_integrity_log.md`，终审跑 `python3 scripts/check_citation_integrity.py <workspace> --final`；未排除的 look-ahead 把相关结论封顶到 `descriptive`。
- **上下文保护优先于一切**：任何会把大段文本灌回主代理的操作，一律改成"写盘 + 回传摘要"。
- **断点交接必须可恢复**：阶段完成必须更新 `00_meta/stage_passport.md`；长暂停 / 阶段切换 / 接手前写 `00_meta/handoff/`，续跑时用 fresh evidence 重核当前事实。
- **自我改进不靠训练集幻觉**：维护本 skill 时按 [`skillopt-improvement-loop.md`](references/skillopt-improvement-loop.md) 收 rollout、拆 train / held-out、提有界 patch、过 selection gate；并守 [`evals/check_complexity_budget.py`](evals/check_complexity_budget.py) 体积棘轮，不让常驻层只增不减。
- **自检不靠感觉**：维护后先跑 `python3 validate_skill.py` 与仓库级验证，再跑 [`evals/score_skill.py`](evals/score_skill.py) `--selftest`；有 SkillOpt 改进包还要跑 `python3 scripts/check_skillopt_packet.py <packet>`。自检失败必须修到通过再宣称可交付。

---

## 进一步阅读（按需加载，别一次性全读进上下文）

主代理进入某环节时才加载对应文档，用完即弃（路径见正文各处链接）。

**编排核心** — [`stage-playbook.md`](references/stage-playbook.md)（10 阶段逐阶段手册：skill 调用·subagent 模板·失败回退）·
[`skill-map.md`](references/skill-map.md)（§0 子 skill 调用机制+注册名对照+输出路径重定向；其余为「任务→skill」全量路由）·
[`orchestration-and-handoff.md`](references/orchestration-and-handoff.md)（Stage 0 路由·stage passport·pipeline status·fresh evidence·handoff·schema v10 字段）·
[`workspace-and-state.md`](references/workspace-and-state.md)（目录布局·`workflow_state.json` 字段·subagent 输入/输出约定）·
[`subagent-templates.md`](references/subagent-templates.md)（可复制派发模板，内置上下文保护契约与输出重定向）。

**Stage 3–4 后端与方法** — [`analysis-backends.md`](references/analysis-backends.md)（python-statspai/stata/r 后端路由·输出合同·环境记录·fallback）·
[`statspai-analysis.md`](references/statspai-analysis.md)（StatsPAI 估计+出版级出表·8 段流水线·七块稳健性闸门）·
[`research-grade-methods.md`](references/research-grade-methods.md)（各设计分支最低证据包）·
[`design-gate-cards.md`](references/design-gate-cards.md)（设计分支证据卡：required artifacts·hard fail·claim 降级）·
[`empirical-audit.md`](references/empirical-audit.md)（样本/变量/estimand 对齐）·
[`dataset-cards.md`](references/dataset-cards.md)（Stage 2 数据源目录+触发的设计风险；配 [`templates/dataset_card.md`](templates/dataset_card.md)）。

**Stage 2 数据源（按地区/性质分流）** — [`china-data-sources.md`](references/china-data-sources.md)（**中国实证数据源总表**：CSMAR/WIND/CNINFO/CHARLS/CFPS/CHFS/CGSS/统计年鉴/工业企业/海关/专利/土地/文本/政策，含字段映射、申请流程、清洗陷阱、GB/T 7714 引用规范、DAS 模板；中文学位论文/中国期刊论文专属）·
配合 [`data-governance.md`](references/data-governance.md) 的全球合规框架使用（本文是「中国语境」特有补充）。

**Stage 5/8/9 中国期刊投稿（按地区/性质分流）** — [`chinese-journals.md`](references/chinese-journals.md)（**中国期刊投稿总册**：5 大顶刊详细规范 + 第二梯队 + 细分领域 + 学位论文场景 + GB/T 7714-2015 详解 + cover letter / response letter 模板 + 选刊决策树 + "中国故事"写作要点；中国期刊/中文学位论文投稿专属）·
配合 [`peer-review-and-submission.md`](references/peer-review-and-submission.md)（英文期刊投稿策略）使用（本文是「中国期刊」特有补充）。

**研究深化层（按阶段加载）** — [`inference-and-uncertainty.md`](references/inference-and-uncertainty.md)（标准误/聚类·few-cluster·随机化推断·多重检验·弱工具区间 · Stage 3/4/5/8）·
[`mechanism-and-channels.md`](references/mechanism-and-channels.md)（X→M→Y 三分类·Gelbach·因果中介+敏感性·坏控制 · Stage 1/3/5/8）·
[`threats-to-validity.md`](references/threats-to-validity.md)（识别威胁×审稿异议预案 · Stage 3/5/8）·
[`design-risk-ledger.md`](references/design-risk-ledger.md)（识别威胁/选择性报告/外部效度/SUTVA/attrition 逐项状态表 · Stage 1/3/5/8）·
[`design-transparency.md`](references/design-transparency.md)（预分析·功效/MDE·设定曲线·研究者自由度 · Stage 3）·
[`literature-and-positioning.md`](references/literature-and-positioning.md)（结构化检索·文献矩阵·贡献定位 · Stage 1/5）。

**写作·质量·完整性** — [`quality-rubric.md`](references/quality-rubric.md)（质量门 7 维评分卡+致命红旗+「短板→回退」映射）·
[`writing-craft.md`](references/writing-craft.md)（写作与结构规范）·
[`integrity-and-claim-audit.md`](references/integrity-and-claim-audit.md)（claim/citation/number 忠实度审计：pre-review/final-check）·
[`citation-and-temporal-integrity.md`](references/citation-and-temporal-integrity.md)（引用存在性+时序完整性；配 [`templates/citation_integrity_log.md`](templates/citation_integrity_log.md) 与 `scripts/check_citation_integrity.py --final`）·
[`peer-review-and-submission.md`](references/peer-review-and-submission.md)（模拟评审与投稿）·
[`worked-example.md`](references/worked-example.md)（端到端黄金路径 trace，数字示意）。

**运行·治理·维护** — [`runtime-fallbacks.md`](references/runtime-fallbacks.md)（工具/网络/MCP/统计软件缺失时的退化与质量封顶）·
[`data-governance.md`](references/data-governance.md)（敏感数据·PII·IRB/DUA·复现包边界）·
[`skillopt-improvement-loop.md`](references/skillopt-improvement-loop.md)（维护本 skill 的 SkillOpt-style 优化协议：rollout/held-out/有界 patch/selection gate）·
[`evals/`](evals/)（维护期评测：[`score_skill.py`](evals/score_skill.py) held-out 打分+packet 行、[`check_complexity_budget.py`](evals/check_complexity_budget.py) 体积棘轮、[`complexity_audit.md`](evals/complexity_audit.md) 漂移诊断）·
[`templates/`](templates/)（关键 artifact 模板）。

**本地自检** — [`validate_skill.py`](validate_skill.py)（模板 schema·工作区初始化·链接·资产·契约·smoke·Notebook）·
[`scripts/smoke_workspace.py`](scripts/smoke_workspace.py)（最小工作区+模板契约）·
[`scripts/check_workspace_gates.py`](scripts/check_workspace_gates.py)（运行期闸门校验，`--reconcile`/`--selftest`）·
[`scripts/check_skillopt_packet.py`](scripts/check_skillopt_packet.py)（维护期改进包校验）。
演示物料：README 已整合 8 阶段教学主线、47 个技能地图与 DiD 自检清单；另保留一个可一键运行的 DiD 演示 Notebook 供讲解配合。
