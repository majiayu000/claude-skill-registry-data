---
name: light-competition
description: 竞赛与项目申报材料辅助。当用户做统计建模、数学建模、互联网+、挑战杯、大创、创新创业、科研训练等项目时使用。辅助写申报书、项目计划书、商业计划书、路演 PPT、答辩稿、项目摘要、技术路线、创新点、可行性分析、市场分析、研究基础、预期成果、经费预算、团队分工。用于非论文投稿场景，可与论文/软著/专利/PPT 联动。
---

# 竞赛与项目申报材料

## 先定位赛事/项目类型（流程第一步，必产 rules_checklist 工件）
不同赛事评审重点差异极大，先确认是哪个赛事/组别，并**对齐当届官方规则**——规则逐年改，先下当届评审规则压缩包，按 `references/competition_rules_cn.md` 的 rules_checklist 逐项勾选，**落盘 `material_checklist.md` 后再动笔**（口头确认不算数；套旧届组别名/漏当届重点领域是高频出局点 anti_patterns D2/E1）。各赛事一句话定位：
- **数学建模国赛 CUMCM**：摘要（单独一页、决定初筛）最重；须含灵敏度分析 + 附录可复现代码；有 AI 使用声明规定。
- **数学建模美赛 MCM/ICM**：英文 Summary Sheet 第一页、权重极高；**全篇 25 页硬上限**（含附录代码，仅 AI 报告不计页）；99 小时三人队。
- **统计建模大赛**：重真实数据 + 统计推断严谨 ＞ 算法炫技。
- **中国国际大学生创新大赛（原互联网+）**：本科/研究生组 × 创意组/创业组（旧"初创/成长组"已淘汰）；提交 BP + 路演 PPT + 答辩。
- **挑战杯**：先分清"大挑"（课外学术，重研究深度）还是"小挑"（创业计划，重商业可行）。
- **大创/科研训练**：创新/创业训练/创业实践三类；重学生主体与培养价值；走申报→中期检查→结题验收。

> 六大赛事的组别细分、页数上限、当届重点领域、评分维度、AI 规定等**逐年易变的硬规则细节**全部下沉到 [`references/competition_rules_cn.md`](references/competition_rules_cn.md)（含 rules_checklist 模板与 last_checked）；后端高分骨架与评审维度见 `databases/db08-ip-materials/case_skeletons.md`。

## 材料模块（按需）
申报书、项目计划书、商业计划书、路演 PPT(交 m16)、答辩稿、项目摘要、技术路线、创新点、可行性分析、市场分析(规模/竞品/痛点/壁垒)、研究基础、预期成果、经费预算(分类合理)、团队分工。

**通用申报书骨架**(大创/挑战杯/科研训练/基金同构、可互借)：立项依据与意义 → 国内外现状 → 研究内容与目标 → 技术路线/方案 → 可行性分析 → 创新点 → 进度安排(里程碑) → 预期成果 → 经费预算 → 团队分工与基础。对标 NSF/NIH 范式则为 Specific Aims→Significance→Innovation→Approach→Preliminary Data→Timeline→Budget→Broader Impacts。借 Research Grants skill 的硬要点：
- **Specific Aims 一页结构**：知识缺口开场 → 长期+近期目标 → 中心假设 → 2–4 个 aims（各含 rationale/工作假设/方法概要/预期产出，彼此独立但互补、时间预算内可完成）→ 收尾 payoff 段。
- **Innovation 按五维写**：概念/方法/整合/转化/规模，并说明如何克服现有方案局限。
- **Approach 每条 aim 配**：设计 · 样本量/数据量 · 分析计划 · 质控 · **备选方案(contingency)**。
- **全篇说服线**：Hook→Problem→Solution→Evidence→Impact→Team，保证 预算↔活动↔时间线↔人员 内部一致。

**商业计划书前先填精益画布(Lean Canvas 九格)自检逻辑闭环**：Problem(前3痛点)·Customer Segments·Unique Value Proposition·Solution·Channels·Revenue Streams·Cost Structure·Key Metrics·Unfair Advantage(难复制壁垒)。注意"先发/团队/资源"常被误当壁垒；UVP 与 Unfair Advantage 最关键最难填。

**核心页优先**(借 NIH Specific Aims，CN 改造)：评委时间有限，**第一页/开篇 300–500 字**决定他是否带着兴趣读完。按以下顺序写：
- Hook（具体数字钩子）→ Gap（现有方案为何不够）→ 长期目标/本项目目标 → 中心假设（创业向=UVP 一句话）。
- 立论依据：把一句前期证据前移，降低风险感知。
- 2–4 子目标：各含 理由/假设/方法/产出，互不依赖、周期内可完成。
- Payoff：价值收尾。

大创/挑战杯的"立项依据+研究内容目标+创新点"、互联网+路演开场 30 秒、数模摘要都是事实上的核心页。完整八段骨架+逐段中文范例+自检清单见 `assets/aims_zh_guide.md`。

## 写作要点
- **创新点**：与现有方案差异化，可量化、可展示（复用 m03/m04 的判断）。
- **可行性**：技术(有基础)、资源(算力/数据/经费)、时间(里程碑)、团队(分工匹配)。
- **进度/技术路线**(借 writing-plans 思路)：把阶段拆成可验证小步，每步有交付物，避免笼统"第一阶段调研"。里程碑 JSON→甘特图(阶段条+交付物+go/no-go 菱形节点)/技术路线图(阶段块+箭头流向)用 `scripts/roadmap_gen.py`(无参跑合成自测，`--emit-sample` 导样例 JSON；matplotlib 自动挂中文字体；图为可再生产物，材料用完即删)。**系统架构图/商业模式流程图/技术方案框图**(评审常反复改稿)可用 **Draw.io MCP**(diagram-as-code，`.drawio` XML 可编辑可版本控制，导出矢量)，比甘特脚本更适合结构类图(配置见 README 推荐 MCP 表)。
- **评委视角**：突出亮点、社会/经济/学术价值，逻辑闭环，数据支撑。
- **市场分析**(创业类，借 Market Research Reports skill 与 7 步法)：
  - **三级测算**：TAM→SAM→SOM，**每层假设进"假设登记表"让评委能直接质疑输入**，配敏感性分析；无现成报告用第一性原理（人口基数×转化过滤×现实 ARPU），再用竞品营收/公开财报**交叉校验**，杜绝自上而下虚高。
  - **竞品四透镜**：波特五力逐力 H/M/L 评级+rationale、Top 份额、定位 2×2 矩阵、战略群组；5–7 家统一模板，提炼 table stakes/普遍空白/未被服务细分。
  - **数据纪律**：须标出处且≤2 年；客户画像基于评论与论坛真实语言而非臆想；用真实可核查数据，不臆造市场规模。
  - **市场数据图**（TAM/SAM/SOM 分层同心圆、竞品 2×2 定位矩阵、波特五力分级、风险概率×影响热图）用 `scripts/market_charts.py`（无参跑合成自测，`--emit-sample` 导样例 JSON；其 TAM/SAM/SOM 三值与 db08 预算/财务预测共用同一套数，a07 一致性把关；matplotlib 自动挂中文字体、色盲安全语义色；图为可再生产物，材料用完即删）。

## 路演 PPT 与答辩
- **路演 deck 走 m16(light-slides)程序化路线**：python-pptx 出可编辑 pptx，按 db06 主题统一视觉，适合创业/挑战杯路演现场；数据图走 m11 真数据出图后嵌入，不用生成式模型造图。需**更快出有设计感的路演物料/海报**时，可用 **Canva MCP**（自然语言生成+品牌模板批量填充、导出 PPTX/PDF/PNG；核心功能免费，autofill/品牌模板需 Enterprise）做创业/挑战杯现场 deck 与海报——数据图仍从 m11 真数据出图后嵌入，不用 AI 生成数据图。
- **学术/答辩幻灯用断言-证据法(assertion-evidence, Michael Alley)**：每页标题写一句完整结论句，正文用图表/示意图作证据，少用 bullet 堆砌；一页一信息。内容密度设上下界(借 beamer-skill：每页≤7 bullet/2 公式/5 符号，且每页都要值得存在)；先 Why 后 What。公式密集场景可用 Beamer(block/alertblock 装重点)，但讲义/打印慎用 overlay——beamer-skill 索性弃用 `\pause/\onslide`，改多页+色盲安全语义色(对比≥4.5:1)逐步强调。
- **PPT 出稿后走视觉 QA 闭环**(借 PPTX skill / beamer-skill)：转 PDF→逐页转图(`pdftoppm -jpeg -r 150`)→用"新眼睛"检查重叠/对比度/溢出/残留占位符(grep 查 xxxx/lorem/未替换字样)→修→只重验受影响页→直到无新问题。Beamer 在 block 内会吞溢出警告，必须靠视觉 audit 抓。**审改分离**：先只读出"位置/现状/建议/严重度"结构化报告，再在另一步动手改；可加 devil's-advocate 对抗轮专挑设计毛病。

## 评审模拟
出稿后用评委视角自审(类比 m14)：创新够不够、可行不可行、商业逻辑通不通、预算合不合理、答辩可能被问什么。
1. **先用 `references/anti_patterns.md` 五类反模式逐条排雷**(概念/写作/技术/格式/策略，每条 症状→为何被扣→怎么改 + 一页速查表)。
2. **再用 `scripts/scorecard.py` 出可机检自审评分卡**：填一份逐维度自评 JSON(每维 1–10)，按所选赛事(innovation/dachuang/dating/mcm)评审维度加权，输出总分 + 薄弱维度 + 对照 anti_patterns 的红旗 + 放行判定(`--emit-sample` 看格式，`--list` 看维度)。⚠ 权重是**经验相对参考、非官方分值**(中国赛事确切权重多不公开)，只用于排序"哪一维拖后腿"，以当届《评审规则》为准、可传 `weights_override` 覆盖。
3. **赛事专项回看**：基金/学术类按 NIH 五项(Significance/Investigator/Innovation/Approach/Environment)或 NSF 两项(Intellectual Merit + Broader Impacts)逐项过；幻灯按 beamer-skill 扣分制 + devil's-advocate 对抗轮；数模回看摘要/灵敏度、MCM 25 页与 AI 说明(细则见 `references/competition_rules_cn.md`)；创业类回看 UVP/壁垒/市场测算是否经得起追问。
4. 多个卖点用 content-strategy 加权打分(客户影响40%+契合30%+潜力20%+资源10%)排序，路演先讲最强的一两个(anti_patterns E2)。
5. 最后做 `templates/defense_qa.md` 答辩 QA 预演，软肋备诚实兜底话术。

## 与其他成果联动
技术内容←m05/a03/a04；论文成果←m07；软著专利←m15；PPT←m16；图表←m11；一致性由 a07 保证(同一项目跨材料说法统一)。

## 产出
**落盘工件名**(CONVENTIONS §6.1 单一真相源，下游 orchestrator 按名调度、a07 跨材料核查、a08 自检)：按所选材料模块取用 `competition/application_draft.md`(申报书) ∣ `business_plan.md`(商业计划书) ∣ `pitch_deck_outline.md`(路演纲，交 m16 出 pptx) ∣ `defense_qa.md`(答辩 QA 预演) ∣ `budget_table.md`(经费预算表)，并恒产出 `material_checklist.md`(材料清单核对 + 当届规则确认)。可填模板见 `templates/`(申报书八段骨架/商业计划书/答辩QA预演/项目摘要)，端到端走查见 `examples/worked_example.md`。

**配套指南与资产**：申报核心页指南(NIH Specific Aims→CN 大创/挑战杯核心页，八段骨架+中文范例+自检)见 `assets/aims_zh_guide.md`；跨赛事反模式手册(五类，症状→为何被扣→怎么改)见 `references/anti_patterns.md`；各届赛事硬规则与确认清单见 `references/competition_rules_cn.md`；评委视角自审评分卡(逐维度加权+薄弱项红旗，经验权重非官方分值)见 `scripts/scorecard.py`；进度图生成器(里程碑 JSON→甘特图/技术路线图，支持 `--granularity week|month`)见 `scripts/roadmap_gen.py`；市场数据图生成器(TAM/SAM/SOM 同心圆/竞品2×2/波特五力/风险热图)见 `scripts/market_charts.py`(JSON 与预算/财务预测共用同一套 TAM/SAM/SOM)。

**后端知识库(db08-ip-materials)**：经费预算表模板(科研支出预算/创业财务预测+假设登记表+自审清单)见 `databases/db08-ip-materials/budget_template.md`；各赛事高分结构骨架(互联网+/挑战杯大挑/大创/数模+评审维度+常见出局点)见 `databases/db08-ip-materials/case_skeletons.md`；竞赛/软著/专利材料细分卡见 `databases/db08-ip-materials/material_extended_cards.md`(`material_cards.md` 为模板与 canonical 索引壳，实体卡已迁至 extended)。逐工具研究笔记(真实端点/方法/链接)见 references.md。

## 衔接
全过程入 db09；商业/数据真实性风险上报 a10（不夸大、不虚构）。交付前过 a08(light-self-review)自检闸门。
