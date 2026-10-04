---
name: scipilot-writing-skill
description: >-
  SciPilot Skills 家族的学术论文写作与润色技能。用于中英互译润色、proofread、缩写/扩写、
  英文或中文学术表达润色、逻辑检查、去 AI 味/humanize、Title/Abstract/Introduction/
  Methods/Results/Discussion/Conclusion/Limitations 起草或改写、图表标题、实验结果分析、
  reviewer 视角自检、cover letter、rebuttal/response to reviewers。触发词包括：润色、
  polish、proofread、改写、帮我改这段、translate and polish、中译英、英译中、condense、
  expand、去AI、降AI、humanize、caption、results 分析、投稿信、审稿回复，或用户上传论文/
  段落并要求改善表达、语言、可读性、学术性。核心规则：先确认任务类型、文本载体、目标期刊、
  语言方向、学科领域和修改保守度；只动表达，不改数值、方向、结论或引用；不编造数据或文献；
  交付前按需运行 scripts/writing_lint.py 做 AI 指纹、LaTeX/Word 格式、中文标点、被动比例
  和句长节奏检查，并报告残留问题。
---

# SciPilot-writing-skill — 高水平 SCI 论文写作与润色副驾驶

> SciPilot Skills 家族成员 | 把"顶刊编辑 + 严苛审稿人"装进你的写作流程

## 概述

`scipilot-writing-skill` 处理科研写作的"最后一公里"：从一句中文想法、一段粗糙草稿、
一个章节，到一篇投稿级的英文（或中文）论文文本。它覆盖翻译、缩写、扩写、润色、去 AI 味、
逻辑检查、逐章节起草、图表标题、实验分析、审稿自检、投稿信与审稿回复。

它与"prompt 食谱"最大的不同在于：**写作质量在这里是可机检的契约，不是凭感觉。**
每一次改写都要穿过两道闸：先用 `scripts/writing_lint.py` 抓确定性的语言指纹（AI 味词、
破折号滥用、LaTeX 未转义、Word 端 Markdown 残留……），再用 AI 读稿、以审稿人视角复核
逻辑与夸大。这条"机器 + AI 读稿"的自检闭环，与 `scipilot-figure-skill` 的视觉自检闭环、
`scipilot-cite-skill` 的幻觉门控同源，是 SciPilot 家族的统一签名。

**一句话定位：先判断后下笔，宁缺毋滥，改完必自检。**

## IRON RULES（不可违反的铁律）

1. **诚信铁律**：润色只动表达，**绝不**改动任何数据、数值、方向、结论或实验事实；
   **绝不**编造或臆造文献、结果、引用（需要找文献请转 `scipilot-cite-skill`）。
   翻译/改写不得悄悄"修正"原意——若发现疑似事实错误，只提示用户，不擅自改。
2. **宁缺毋滥铁律**：保守修改。原文若已清晰、准确、规范，**保留原样并明确肯定**，
   不为追求形式变化而强行换同义词、重组句式、刷存在感。修改阈值高于改写冲动。
3. **透明可溯铁律**：**绝不静默重写**。每次改写都产出三段式——
   `Part 1 改后文本` + `Part 2 直译/回译（供核对未走样）` + `Part 3 修改日志（改了什么、为什么）`。
   用户永远能看见你动了哪里。
4. **去 AI 味但留人味铁律**：删除 AI 指纹（堆砌高级词、机械连接词、悬垂 -ing、三点式滥用、
   破折号泛滥、空泛归因、promotional 夸张），但**不为换词而换词**；保留作者的观点、
   节奏与领域术语。高质量输入应判"检测通过"。
5. **格式纯净随载体铁律**：按文本载体切换规范——
   **LaTeX**：源码纯净，禁止擅自加粗/斜体，特殊字符转义（`%→\%`、`_→\_`、`&→\&`、`#→\#`），
   数学公式保留 `$`，保留 `\cite{}`/`\ref{}`/`\label{}` 等命令；
   **Word/中文**：纯文本输出，禁止任何 Markdown 标记（`**`、`#`、`*`），中文全角标点；
   **拒绝列表化**：把 `\item` / `1. 2. 3.` 还原为连贯段落（除非列举本身逻辑更清晰）。
6. **断言=证据铁律**：hedging（may/suggest/likely）与 boosting（demonstrate/establish）
   的强度必须匹配证据强度。有强数据才能 boost，超出数据的推断必须 hedge；
   **绝不 overclaim**，绝不把相关说成因果，绝不把单一研究上升为普适。
7. **机检门控铁律**：交付前**必须**运行 `scripts/writing_lint.py`。命中 FAIL 项必须修复
   或如实向用户报告，**不得**假装通过、不得伪造检查结果。这条把"写得好"从口号变成
   机器可检查的契约（与 cite 的 Gate 8、figure 的视觉自检同构）。

## 触发条件

当用户意图涉及以下任一场景时激活：

- 润色 / 改写 / proofread 一段或整篇论文文本（中或英）
- 中译英并润色、英译中、缩写、扩写
- "去 AI 味" / humanize / 降低 AI 痕迹 / "这段太像 AI 写的"
- 逻辑检查 / 一致性核对 / 投稿前语言终检
- 起草或改写某个章节（Title / Abstract / Introduction / Methods / Results / Discussion / Conclusion / Limitations）
- 生成图标题、表标题；把实验数据写成分析段落
- 以审稿人视角自检论文；写 cover letter；写 rebuttal / response to reviewers
- 用户上传 `.tex` / `.docx` / `.md` 并要求改善表达、语言、可读性、学术性
- 用户提到 "scipilot" 且涉及写作 / 文字 / 润色

## 工作流程（Stage 0–7，按序执行）

### Stage 0：信息收集（必做 — 主动逐项询问，禁止默默假设）

这是交互的核心。缺任一必问项就开工是错误的；对有默认值的项也要告知默认值再确认。

**A. 任务类型（最先问）** — 见下方《任务清单》，确定走哪条路由。常见：润色 / 翻译润色 /
缩写 / 扩写 / 去 AI 味 / 逻辑检查 / 写某章节 / 图表标题 / 实验分析 / 审稿自检 / cover letter / rebuttal。

**B. 文本载体（必问，决定格式规范）**：
- `.tex`（LaTeX，英文论文常见）→ 走 LaTeX 纯净 + 转义规则，调 `scripts/latex_clean.py`
- `.docx` / Word（中文论文常见）→ 纯文本 + 全角标点 + 零 Markdown
- `.md` / 纯文本 → 按用户后续用途定
- 直接粘贴的片段 → 问清最终落到 LaTeX 还是 Word

**C. 目标期刊 / 会议（必问，告知影响）**：决定结构、篇幅、风格与报告规范。
没有明确目标时给默认（英文顶会/顶刊通用学术风），并说明。详见 `references/journal_styles.md`。

**D. 语言方向（翻译/润色类必问）**：中→英 / 英→中 / 英→英 / 中→中。

**E. 学科领域（必问，软性影响风格）**：CS/AI、自然科学（生物/化学/物理）、医学、工程、
社科、中文核心期刊……不同领域时态、语态、hedging、报告规范有别。

**F. 修改保守度（必问，告知默认）**：默认"中等—宁缺毋滥"。可选"仅纠错（最保守）"/
"中等润色"/"深度重写"。深度重写也绝不触碰 IRON RULE 1/6。

**G. 参数复述确认（必做）**：收齐后口头复述全部参数并等待"开始"信号，例：

> 我将润色 **paper.tex** 的 **Discussion 第 2 段**（载体 LaTeX，中→英不涉及，**英→英深度润色**），
> 目标 **NeurIPS**，领域 **ML**，保守度 **中等**。输出三段式 + 机检报告。开始？

未获明确"开始"前，**不进入 Stage 1**。

### Stage 1：解析载体与范围

- `.tex`：读源码，定位要处理的片段/章节，记录其中的 LaTeX 命令（`\cite`/`\ref`/`\textbf` 等）
  与数学公式跨度，确保改写时原样保留。
- `.docx`：用 `scripts/docx_text.py`（或 python-docx）读段落与 Heading 样式，提取纯文本。
- 片段：直接载入。明确"要改的边界"，不越界动用户没让动的部分。

### Stage 2：选路由

按 Stage 0 的任务类型 + 目标刊 + 章节，加载对应参考：
- 任务怎么做 → `references/prompt_library.md`（18 个升级版任务剧本）
- 句段怎么写好 → `references/sci_writing_principles.md`（时态/语态/hedging/衔接/简洁/数字规范）
- 章节怎么搭 → `references/section_playbooks.md`（逐章节 + CARS 模型）
- 目标刊要什么 → `references/journal_styles.md`（Nature/Science/Cell/PNAS/IEEE/医学/中文核心 + 报告规范）
- 去 AI 味怎么改 → `references/de_ai_humanize.md`（AI 指纹清单 + 中英词表 + humanize 原则）
- 投稿信/审稿回复 → `references/cover_letter_and_rebuttal.md`

### Stage 3：起草 / 改写

应用 `sci_writing_principles` + `de_ai_humanize` + 对应任务剧本，产出**三段式**
（IRON RULE 3）。深度重写也保留作者观点与领域术语；LaTeX/Word 按载体守纯净。

### Stage 4：机器自检（强制 — Gate）

把改后文本写入工作文件，运行：

```bash
python scripts/writing_lint.py <改后文本文件> --mode {latex|word|markdown|plain} --lang {en|zh} \
       --report lint_report.json
```

- exit `0` → PASS（无 FAIL/WARN），继续
- exit `1` → 有 WARN（如破折号偏多、被动比例偏高），评估后决定是否回 Stage 3
- exit `2` → 有 FAIL（如 Word 端残留 Markdown、LaTeX 未转义、命中重 AI 指纹），**必须回 Stage 3 修复**

LaTeX 专项再跑 `scripts/latex_clean.py` 核转义与 `$` 配平；需要量化节奏/被动可跑 `scripts/text_stats.py`。

### Stage 5：AI 读稿自审闭环（机器查不出的，靠读）

以**审稿人视角重读改后文本**，对照清单自检（程序抓不到的感知/逻辑问题）：
1. 逻辑是否连贯、有无跳跃或自相矛盾
2. 是否 overclaim、是否把相关说成因果（IRON RULE 6）
3. 是否仍有"读着像 AI"的段落（节奏均匀、空洞、悬垂 -ing）
4. 术语/缩写/时态是否前后一致
5. 是否偏离了原意或动了不该动的事实（IRON RULE 1）

发现问题 → 回 Stage 3 改 → 重跑 Stage 4 机检。**最多 3 轮**；3 轮仍有残留则如实标注为
"建议人工确认项"交付，不假装完美。

### Stage 6：一致性与诚信复核

- 术语表一致（同一概念不无故换名）、缩写首次定义后统一、时态符合各章节惯例
- US/UK 拼写全文统一；数字/单位/统计量格式统一（详见 `sci_writing_principles.md`）
- **diff 比对**：确认未改动任何数值、公式、引用键、原意（IRON RULE 1）
- 若涉及文献真实性，提示转 `scipilot-cite-skill` 核验，本技能不臆造引用

### Stage 7：交付报告（SciPilot 写作报告）

- 本次做了什么任务、处理了哪些片段
- `lint_report.json` 的 PASS/WARN/FAIL 摘要与已处理项
- 修改日志要点（Part 3 汇总）
- 残留的"建议人工确认项"（如有）
- 与家族协作建议（配图 → figure；补文献 → cite；模拟审稿 → review[规划中]）

## 任务清单（覆盖同类"写作 prompt 清单"的全部能力 + 更多）

| # | 任务 | 触发例 | 载体 | 参考 |
|---|---|---|---|---|
| 1 | 中译英 + 润色 | "把这段中文翻成英文论文语言" | LaTeX/纯文本 | prompt_library §中译英 |
| 2 | 英译中（直译核对） | "帮我把这段英文读懂" | 纯文本 | prompt_library §英译中 |
| 3 | 中文重写（Word 场景） | "把零散要点写成中文论文段落" | Word | prompt_library §中文重写 |
| 4 | 缩写 | "这段压缩 10 个词" | LaTeX | prompt_library §缩写 |
| 5 | 扩写 | "这句太单薄，扩充一下" | LaTeX | prompt_library §扩写 |
| 6 | 英文润色 | "润色到顶会投稿水准" | LaTeX | prompt_library §英文润色 |
| 7 | 中文润色 | "润色这段中文，保守一点" | Word | prompt_library §中文润色 |
| 8 | 逻辑检查 | "终稿做个红线审查" | LaTeX | prompt_library §逻辑检查 |
| 9 | 去 AI 味（英） | "这段去一下 AI 味" | LaTeX | de_ai_humanize + prompt_library |
| 10 | 去 AI 味（中） | "中文去 AI 味" | Word | de_ai_humanize + prompt_library |
| 11 | 写/改 Title | "帮我起 5 个标题" | 任意 | section_playbooks §Title |
| 12 | 写/改 Abstract | "根据这些结果写摘要" | 任意 | section_playbooks §Abstract |
| 13 | 写 Introduction | "按 CARS 写引言" | 任意 | section_playbooks §Introduction |
| 14 | 写 Methods/Results/Discussion | "起草 Discussion" | 任意 | section_playbooks |
| 15 | 图标题 / 表标题 | "给 Figure 1 写英文 caption" | 任意 | prompt_library §图表标题 |
| 16 | 实验结果分析 | "把这张结果表写成分析段" | LaTeX | prompt_library §实验分析 |
| 17 | 审稿人视角自检 | "用 reviewer 视角审一遍" | PDF/文本 | prompt_library §审稿自检 |
| 18 | Cover letter | "写投稿信" | 纯文本 | cover_letter_and_rebuttal |
| 19 | Rebuttal / 审稿回复 | "帮我逐条回复审稿意见" | 纯文本 | cover_letter_and_rebuttal |

> 第 11–14、18、19 是同类 prompt 清单通常没有、而高水平 SCI 写作高频需要的能力——本技能的"只多"。

## 自检闭环（机器 + AI 读稿）—— 家族签名

```
改写 → writing_lint.py 机器自检（AI 指纹/转义/全角/被动/节奏）
        + AI 读稿审稿人自审（逻辑/夸大/AI味/一致性）
                  ↓ 发现问题
        回 Stage 3 改 → 重检，最多 3 轮，残留如实标注
```

三层防线：
1. **机器抓确定性指纹**：`writing_lint.py` 命中即报（词表、正则、转义、Markdown 残留、全角标点）。
2. **AI 读稿抓感知/逻辑问题**：节奏是否均匀机械、是否 overclaim、悬垂 -ing、术语漂移——这些程序查不出。
3. **诚信/一致性复核**：diff 确认未动事实，缩写/时态/拼写统一。

## 脚本与参考

| 脚本 | 作用 |
|---|---|
| `scripts/writing_lint.py` | **核心**。确定性写作质量 linter：AI 指纹词（中英）、机械连接词、悬垂 -ing、否定式平行、破折号密度、空泛归因、模型名所有格、LaTeX 未转义、Word 端 Markdown 残留、中文全角标点、被动比例、句长节奏；输出 PASS/WARN/FAIL + JSON 报告 |
| `scripts/latex_clean.py` | LaTeX 专项：转义 `%/_/&/#`（跳过数学与已转义）、检查 `$` 配平、检测擅自的 `\textbf`/Markdown 污染 |
| `scripts/text_stats.py` | 量化指标：句长分布与节奏（burstiness）、被动语态比例、名词化密度、hedge/booster 计数 |
| `scripts/docx_text.py` | 读/写 `.docx`：提取纯文本段落、纯文本写回（零 Markdown）、可选 tracked-changes 提示 |

| 参考文档 | 内容 |
|---|---|
| `references/workflow.md` | 完整工作流与边界情况处理 |
| `references/prompt_library.md` | 18 个升级版任务剧本（覆盖并超过同类 prompt 清单） |
| `references/sci_writing_principles.md` | 句段技法：时态/语态/hedging-boosting/给-新衔接/简洁/数字单位统计规范 |
| `references/section_playbooks.md` | 逐章节写法：Title/Abstract/Introduction(CARS)/Methods/Results/Discussion/Conclusion/Limitations |
| `references/journal_styles.md` | Nature/Science/Cell/PNAS/IEEE/医学/中文核心风格 + CONSORT/PRISMA/ARRIVE/STROBE/ICMJE 路由 |
| `references/de_ai_humanize.md` | AI 指纹语言学清单 + 中英 AI 味词表 + humanize 原则 |
| `references/cover_letter_and_rebuttal.md` | 投稿信结构 + 审稿回复（point-by-point）策略 |

## 与 SciPilot Skills 家族协作

- 文字配图 / 图表 → **scipilot-figure-skill**
- 补充或核验文献引用 → **scipilot-cite-skill**（本技能绝不臆造引用）
- 全面模拟审稿 → **scipilot-review-skill**（规划中）
- 投稿格式适配 → **scipilot-submit-skill**（规划中）

## 依赖

```
pip install python-docx     # 仅 .docx 读写需要；纯文本/LaTeX 无需任何依赖
```

`writing_lint.py` / `latex_clean.py` / `text_stats.py` 仅用 Python 标准库，开箱即用。

## 工作目录产物（写作质量证据链）

| 文件 | 由谁生成 | 用途 |
|---|---|---|
| `lint_report.json` | `writing_lint.py` | Stage 4 机检凭证：逐项命中、严重度、PASS/WARN/FAIL |
| `change_log.md` | LLM 在 Stage 3 累积写出 | 透明修改日志（Part 3 汇总），对应 IRON RULE 3 |

这两个文件让"我把文字改好了"从一句口头承诺，变成可核对的机器记录。
