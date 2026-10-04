---
name: light-paper-drafting
description: 撰写论文初稿与单章节起草、重写、自检。当用户要写论文、写某个章节（标题/摘要/引言/相关工作/方法/实验/结果/讨论/结论/局限/未来工作）、重写某章节、或对草稿做失败模式自检时使用。五种模式 full/outline-only/abstract-only/section-redraft/self-review；以顶刊/顶会审稿人标准打磨，逻辑严谨、创新点突出、结论不夸大、claim 有引用支撑。
---

# 论文初稿撰写

## 总原则
围绕一个问题组织全文：**如何让审稿人相信这篇论文值得发表**。每写一段就自问"审稿人读到这里会信吗、会问什么"。

**先研究后落笔**：每个 claim 落笔前要有可核查来源；没有来源支撑的句子一律标 `[MATERIAL GAP]`，绝不凭空填充（anti-leakage 协议）。**brief 驱动**：平庸写手 + 好 brief 胜过好写手无方向——每节先写明"要论证什么/用哪些证据/对标哪篇"再写。

## 操作模式（先选档位，别每次都走全流程）
`full`（完整初稿）/ `outline-only`（只给大纲+论证图）/ `abstract-only`（只写摘要）/ `section-redraft`（重写某节）/ `self-review`（只做自检）。各模式的触发/输入/步骤/产出/诚信门档位见 `references/operational_modes.md`。

## 资产导航
- **结构模板**：`templates/` 六类骨架——`01_imrad.md`(IMRaD 实证) / `02_review_survey.md`(综述/系统综述) / `03_theory.md`(理论方法) / `04_case_study.md`(案例) / `05_policy_brief.md`(政策简报) / `06_conference.md`(会议)。每个含节序+每节字数上限+[图位/表位]+必备声明位。
- **端到端范例**：`examples/worked_example.md`——brief→配置→贡献清单→大纲→论证图→Introduction 初稿的真实"前/后"对照（前=踩满幻觉红线，后=合规并显式标 `[MATERIAL GAP]`/`[RESULT GAP]`）。
- **自检清单**：`references/self_review_checklist.md`——8 维质量 + 7 类失败模式，可勾选，每项"看什么/什么触发改写"两栏。
- **诚信门**：`references/integrity_gate.md`——claim 抽样配额（初稿≥30%、终稿100%）+ 引用核查动作（curl DOI/Crossref/arXiv/OpenAlex，端点已实测记 HTTP 码）+ **无 DOI 中文文献核对协议**（知网/万方/维普题录三字段比对法，中文文献不得因无 DOI 跳过诚信门；写作时本技能是拦截方，核验执行方是 m10 citation 的中文核验兜底清单，两方口径一致）。**claim 台账落地：用 `templates/claim_passport.md`** 逐条登记 claim（ID/类型①②③④/来源指针/核查状态 已验证·待核·GAP/HTTP码），这是诚信门 load-bearing 工件；可跑 `draft_lint.py --claims` 抽候选事实句来播种。
- **reporting 指南映射**：`references/guideline_map.md`——实验/观察/系统综述/诊断/预测/动物/个案/定性 → CONSORT/STROBE/PRISMA/STARD/TRIPOD/ARRIVE/CARE/SRQR。
- **必备声明**：`references/mandatory_inclusions.md`——Data Availability/Ethics/CRediT/COI/Funding + 按 venue 的 AI 使用声明模板。
- **机检器**：`scripts/draft_lint.py`——查残留 GAP、缺失声明、无显著性的 SOTA 句、抽取待核引用。**已重写降误报**：SOTA 措辞与显著性按**同句/相邻句窗口**共现判定（非严格同行）、**跳过 ``` 代码围栏**、必备声明按**行首 markdown 标题**校验（非全文子串）；`--claims` 抽候选事实句播种 claim 台账、`--json` 出机读结果供 orchestrator 判过门。`python scripts/draft_lint.py <draft.md> [--final] [--claims] [--json]`；自测 `--selftest`。人判优先，机检兜底。

## 写作前
确认创新点(m03/m04)、结果与亮点(m06)、目标 venue 风格(db01/db02)。动笔顺序参考成熟流水线(ARS)：
1. **Paper Configuration**：定结构类型(IMRaD / 综述 / 理论分析 / 案例 / 政策简报 / 会议论文)与目标 venue。
2. **贡献清单(3 条左右)**：作为全文 pillar，每节都要服务于它。
3. **大纲 + 论证图(Argument Map)**：先把"论点→证据→反驳"链条画出来再落笔。
4. 从 db02 抽取该类论文的**结构套路**（节序、字数/页数上限、图表规范），不照抄内容。venue 模板务必取**目标年份当年版本**（NeurIPS/ACL/IEEE 模板逐年改；注意双盲匿名规则）。
   - 分层取用:结构套路(title_pattern/节序/摘要五段)取自方法论层(patterns_library + 各卡结构拆解),领域中立直接用;但取**可信度背书**时按目标 venue 方向用 `domain_scope=` 过滤样本卡——非 cs.* 方向(统计/医学/农业/社科)禁用竞赛排名/SOTA/开源 social proof,改用通用背书(理论保证/第三方基准/真实部署),详见 samples_real 文末 D 表。
   - 若引用任何卡内被引数作论据,须经 `databases/db02-paper-writing/scripts/paper_signal.py --doi <DOI>` 实时刷新,不信本地 snapshot。
读外部 PDF/DOCX/PPTX 资料时，可用 MarkItDown 转 Markdown 再喂模型（`markitdown paper.pdf -o paper.md`）。

## 分模块要点
- **标题**：准确 + 有信息量 + 体现创新，避免夸大。
- **摘要**：背景→问题→方法→关键结果(带数字)→意义，150–250 词。
- **引言**：problem → gap → 本文做法 → 贡献清单 → 结果预告。gap 要有文献支撑（每个 gap 用 3–5 篇引用佐证）。
- **相关工作**：按 taxonomy 组织，每类末尾点明"与本文的差异"，不流水账。这是审稿胜负手，舍得投入综述合成。**可操作微流程**：① **选 taxonomy 轴**——按"方法族/问题设定/数据模态/解决的核心痛点"之一选 1 个主轴分 2–4 类（别按时间线流水账）；② 每类写 **delta 句**骨架："`<这类工作>` 做到 `<X>`，但 `<未解决的 Y>`；本文通过 `<机制>` 补上 `<Y>`"——必须落到实质差异（非"我们也做了 X"）；③ **锁定强 baseline**：列每类里**最强/最新/最像**的代表作（非最好打的弱 baseline），实验对比必含它们，否则审稿人问"为什么不比 X"；④ 每条引用挂 claim 台账①类核查元数据。宁可少引而准，不堆砌（堆砌易引幻觉，违 M2）。
- **方法**：从直觉到形式化，公式定义清晰，配框架图(m09)，可复现。
- **实验**：先讲 setup(数据/baseline/指标/实现细节)，再主结果、消融、敏感性、泛化、鲁棒性，对应 m05 设计。结果段用"数据驱动占位"：显式写出关键数字 + 显著性(如 p<0.001) + 与文献基线对比。
- **结果分析**：解释为什么，引用 m06 的洞察，承认不利结果。
- **讨论**：意义、适用边界、与已有工作对话。
- **结论**：呼应贡献，不引入新内容。
- **局限性 + 未来工作**：诚实，体现 reviewer 友好。

## 当论文"差点意思"时：诚实地讲好故事
不是每篇论文都有顶会级的创新。当 m04 评出来只是"增量"、核心撞了前作、或主方法失败时，**讲好故事 ≠ 夸大造假**——是在严守诚信门的前提下，把真实贡献用最有说服力的框架呈现。这是写作技巧，不是学术不端的遮羞布。两条铁律先立：**(1) 绝不把②增量谎报成①创新**（m04 已查核心撞车，谎报会被抓）；**(2) 绝不把失败/负结果藏起来**。在此之上：

- **重新定位贡献，而非夸大贡献**。核心被前人做过 → 别假装首创，改打"广度/严谨/统一对比/可复现"牌：明确承认前作（专设"Closest prior work"段，逐句讲清 delta），把卖点转成"首次在统一协议下系统对比 X/Y/Z"或"首个多种子+配对统计+效应量的扎实证据"。审稿人厌恶的是"假装没看见前作"，不是"增量但诚实"。
- **把负结果/失败变成卖点**。主方法没work，但"我们试了看似显然的捷径、证明它不行、并解释为什么"本身有科学价值——它阻止后人重蹈覆辙，还能反向强化主结论（如"没有免数据捷径，所以数据驱动校准是必需的"）。给负结果单设一节，讲清机理、给出可证伪的解释。
- **缩小 framing 到能站住的范围**。够不着"我们解决了 X"，就老实写"我们刻画了 X 在 Y 条件下的边界/代价"。小而真的 claim 比大而虚的 claim 更难被拒。标题、摘要、贡献清单同步收缩到证据撑得住的尺度。
- **用故事弧组织，但每个转折都挂证据**。好故事 = 张力(一个被忽视的代价/矛盾) → 升级(它有多普遍、多严重，带数字) → 转折(能不能修、修的代价) → 落点(可操作建议)。每一环都用真实验数字兜底，不靠形容词。
- **诚实换信任，信任换接收**。主动写足 limitation、承认不利结果、点名比自己强的前作——reviewer 友好度直接影响评分。藏短板被识破一次，整篇可信度归零。
- **选对场子也是讲故事**。增量扎实的工作投 workshop / 应用 track / 短文，比硬投顶会主会更可能中；交 m13 venue-matching 时如实报"这是增量"，让它匹配现实层次，别为面子投注定被拒的场。
每个模块写完，立即用 m08(润色) + m14(模拟审稿) 视角自检一轮。完整可勾选清单见 `references/self_review_checklist.md`（8 维 + 7 模式，每项含"什么触发改写"）。

**模拟审稿 8 维自评清单**（ScholarEval 维度，逐项指出可改处，相对自检比打绝对分更可靠）：
创新性 / 意义影响 / 方法严谨性 / 清晰度 / 可复现性 / 实验证据支撑 / 与已有工作定位 / 伦理与局限诚实度。

**7 类 AI 失败模式红线自查**（源自 The AI Scientist 的失败模式分析，写草稿时逐条排雷）：
M1 把实现 bug 当通过；M2 幻觉引用(编造参考文献)；M3 幻觉实验结果；M4 走捷径；M5 把 bug 包装成"新洞察"；M6 方法学造假；M7 早期框架锁死(frame-lock)。
引用核查：citation key/DOI/arXiv ID 只是溯源字段，不等于该文真支撑你的论点——存疑的点开看。核查配额与 curl 动作见 `references/integrity_gate.md`。
**正文引用占位统一用机读 citekey**：写成 `\cite{authorYearWord}`——**第一作者姓 + 年份 + 标题首个实词，全部小写**（如 `\cite{zhang2024deep}`），不要用 `[Zhang 2019]` 这类自由文本占位（排版到 m10 会对不上 .bib 键、报 undefined citation）。该公式与 m10 citation 生成 .bib 时 pin 的 citekey 同源。
改完再交付。修订时逐维度追踪分数，警惕"改了 A 坏了 B"的回退。

## 产出
分模块 Markdown/LaTeX 草稿 + 贡献清单 + 待补内容标记(`[MATERIAL GAP]`/`[RESULT GAP]`/TODO，如缺图缺实验)。提交前过 `references/mandatory_inclusions.md` 的声明清单与 `references/integrity_gate.md` 的终稿门(100% claim/引用核查)。术语与 db09 术语表对齐(a07)。输出建议归到带时间戳的目录便于版本管理。

落盘工件名（CONVENTIONS §6.1，下游 m08/m09/m10/m12 消费）：`draft.md`（分模块草稿，m08 润色在同稿迭代）+ `claim_passport.md`（claim 台账）。

## 衔接
图表交 m09/m11，引用交 m10（正文 `\cite{}` 占位用 `authorYearWord` 公式，与 m10 pin 的 citekey 同源），排版交 m12，润色交 m08，模拟审稿交 m14。交付前过 a08(light-self-review)自检闸门。版本入 db09。

---
工具调研笔记（真实端点/方法/局限）见 `references.md`。
