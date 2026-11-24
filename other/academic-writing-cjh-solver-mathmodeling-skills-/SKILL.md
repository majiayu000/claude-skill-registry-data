---
name: academic-writing
description: |
  数学建模论文的学术表达与结构质量控制主入口。调用本地化论文审阅规则，
  只允许修改普通正文，并在交付前保护公式、引用、数字、三线表、图表编号和模型逻辑。
  不负责模型建立、数据计算或竞赛交付门禁。
allowed-tools:
  - Read
  - Write
  - Edit
  - AskUserQuestion
metadata:
  mode: local-adapter
  upstream: youngze0016/thesis-polish-agent
  guard: scripts/mathmodel_patch_guard.py
---

# 数学建模论文写作适配层

本技能是本地维护的稳定入口。上游 `thesis-polish-agent` 只作为 `modules/` 下的规则和审阅资源，不能直接接管数学建模论文，也不能绕过本地差异门禁。

## Contest-Orchestrator Adapter

Harness 启用 `visual_workflow: chapter_parallel` 时，先读取 `contest-orchestrator/references/harness_chapter_parallel.md`。H6 获批后，同一固定论文角色提交一个把最终 `chapter_order` 与实际 `writing_order` 分开的全篇计划；建模与求解章节依赖优先，摘要只在正式 H8 最后完成。每次只写一章完整、证据绑定的正文，经质量审查与用户 `H7_CHAPTER:<chapter_id>` 批准后才开始下一章。批准后才生成自包含图表提示词，由用户亲自转交图表会话；H7 图件可与下一章并行。图件返修只出新版本提示词，不撤销章节批准或阻塞后续写作。最终 H8 按最终目录整合选定图件、做必要局部编辑并写摘要，不从头重写已批准正文；H9 仍是完整交付门。章节记录声明 `visuals_required: false` 时无需生成提示词或制图。`writer_first_draft` 仍读取 `contest-orchestrator/references/harness_writer_preparation.md`。

本技能在主控中的固定位置是“论证中心编辑”：接收当前任务卡、论文快照、冻结的模型/结果/引用证据，输出普通正文补丁和可回流节点包。`contest-orchestrator` 负责范围、模型、数字、图表、引用和交付裁决；本技能不得越权修改这些内容。

- 节点包包含 `status`、`active_mode`、`task_card`、`artifacts`、`evidence`、`checks`、`blockers`、`next_node`，所有路径均为项目工作区相对路径。
- 每个新符号必须在正文首用处给出含义、单位/量纲、取值域和变量类型；缺少定义时报告 `FAIL`，不通过补写猜测修复。
- 建模问题章节只设置一次全局“符号说明”；每个问题标题后先写不编号的问题引入与建模思路段，默认使用“模型建立”和“模型求解与结果分析”两个编号小节。模型建立小节末尾保留当前模式求解节点与独立验证节点核验的唯一“最终求解模型”框，模型求解与结果分析小节必须解释算法、结果意义和适用范围。执行前读取 `contest-orchestrator/references/model_summary_protocol.md`。
- 不把“决策变量、目标函数、约束条件、算法、结果分析”等内部导航词扩展成碎片化编号标题；灵敏度或稳健性只有在存在独立证据时单独成节。
- 交付文本只保留面向读者的最终论证，不得出现元话语、内部交流、评审过程、修改轮次、agent、提示词、调试或旧内容等负回响。
- 非绘图论文任务的视觉检查默认关闭；文本层、公式、引用、数字和结构检查照常执行，只有用户明确要求时才启用视觉检查。
- active_mode: full-contest-mathorcup 时，写作任务接收已批准的 paper_argument_blueprint.yaml、paper_language_profile.yaml、独立核验的 paper_material_readiness.yaml、paper_claim_coverage.yaml、当前写作卡和冻结证据。chapter_parallel 按实际 writing_order 逐章写作和批准，正文与附录批准后单独讨论摘要框架，摘要最后写，最终统一接图与全文终审。仅历史四批流程按批次边界暂停并使用 B1–B4。标题、篇幅、AI 使用说明与提交格式只取当前 competition_profile.yaml 中已核实的官方要求；不得套用国赛 B 题模板、页数或附录口径。
- paper_language_profile.yaml 是项目级术语与文风配置，必须在写作计划批准时冻结并随每批任务卡传入。对“题目”“题干”等候选用词先做语境归类，再记录用户确认的词形和适用场景；不得全局查找替换。仅对普通正文应用已确认规则，保护公式、符号、数值、引用、图表、标题、直接引文和模型逻辑。
- 符号首用定义、主张—证据绑定、元话语与负向回响检查，在当前写作单元局部收尾及最终全文终审执行；chapter_parallel 每章只作局部审阅，不对每章重复启动整篇质检。历史四批流程保持批次检查。
- 仅国赛 2026 论文：正文不设目录；正文从正文主体起计（摘要不计入），包含正文主体、参考文献前的 AI 工具使用声明和参考文献，最多 30 页，附录不计入；提交论文文件总页数（含摘要、正文、参考文献和附录）硬上限 51 页，推荐区间 35–51 页；论文提交为含文本层的非图片 PDF，文件不超过 20 MB。
- AI 声明只写实际使用范围的必要信息，但必须真实；不得隐瞒已使用工具或填写未使用。国赛 2026 使用 AI 时，支撑材料提供 `AI工具使用详情.pdf`，说明工具版本、用途环节、关键交互摘要、采纳、人工修改和核验，突出参赛队主导核心建模与分析；其他赛事的说明形式以已核实官方规则为准。

## 职责边界

### MathorCup reader-facing results

MathorCup 控制记录启用 `nodes.M4.visual_workflow: chapter_parallel` 时，先基于冻结科学证据提出全篇写作蓝图；不要求正式图或视觉计划先完成。蓝图区分最终目录顺序与实际写作顺序，建模与求解章节依赖优先，摘要最后完成。每次只执行一章 `draft`，提交完整、证据绑定正文和局部质量审查；用户批准 `M4_CHAPTER:<chapter_id>` 后才写下一章。批准后，writer 才可用 `figure_prompt` 从这份确切正文选择图、表或文字并形成自包含提示词。用户亲自转交 figure；只有另有明确授权时主控才代发。图表返修只形成提示词新版本，不撤销未变正文批准或阻塞后续章节。最终 `write` 统一接图、调整解释、图注与排版，并在摘要章和全文审阅完成后交付。具体字段与门禁读取 `contest-orchestrator/references/mathorcup_chapter_parallel.md`；历史 `writer_first_batches` 仍读取 execution protocol 的兼容段。

MathorCup 正文以读者问题、比较结果和具体发现组织：先回答发现了什么，再用必要的方法、数字和证据解释为什么、意味着什么。证据完整与正文可读性分别审阅，不把审查字段、派发顺序或“做法—数字—免责声明”循环写成段落模板。必要的代理定义、不可认证条件和预测边界保留在首次定义、表注或集中局限中；不逐段重复免责，也不为了消除负向句删去科学事实。

章节标题按“问题一／二／三＋具体任务或方法”保持可检索性；三级标题随真实论证形成，不在素材不全时冻结。先呈现公平比较，再解释最终采用方案及理由。摘要仍在正文与附录完成后写，先通读全文检查读者路径、章节递进和贡献收束，再突出方法、具体发现及意义，不能只列算法名称。写作发现题意缺口时回流现有 requirement coverage，不能以改写措辞替代缺失计算。

- `contest-orchestrator`：题目解析、模型建立、代码求解、结果、图表、引用和正式交付。
- `academic-writing`：章节结构、学术表达、术语统一、审阅报告和 LaTeX 编译建议。
- `humanizer-zh`：最后的语言去痕，只处理普通正文。
- `mathmodel_patch_guard.py`：检查润色前后的数学内容是否发生未授权变化。

## 论证中心编辑

当用户要求“论证中心编辑”“按主张—证据—结论审阅”“防御性写作清理”或等价处理时，必须先读取 [claim-centered-editing](modules/claim-centered-editing/MODULE.md)。该模块只负责普通正文的主张组织、证据绑定和结论范围；不建立模型、不重算结果、不改变引用和图表。

当 Harness H8 或 MathorCup M4 阶段要求“论证蓝图”“写前论证架构”或等价处理时，必须先读取 [argument-blueprint](modules/argument-blueprint/MODULE.md)。该模块在写作开始前把冻结叙事、结果解释卡、图表和证据组织为读者问题—章节回答—论证—证据的蓝图；不撰写论文正文，不建立模型，不重算结果。

当 Harness H8 阶段要求“论文作者简报”“章节写作卡”或等价处理时，必须在论证蓝图获批准后读取 [author-brief](modules/author-brief/MODULE.md)。该模块把蓝图转换为论文作者的紧凑输入；不把质量门禁或交付清单混入作者任务，不撰写论文正文。

Harness H8C 或 MathorCup M4 全文通读阶段必须先读取 `contest-orchestrator` 的 `references/h8_writer_first_protocol.md`，沿读者路径检查章节递进、段落衔接、主张回收和结论意义，再进行局部证据与表达编辑。Harness `chapter_parallel` 的 H8C 只接入最终选定图件、修订图前图后文字、图注、排版和必要局部衔接，不从头改写已批准章节。章节卡和检查项只能作为内部导航，不能成为正文的组织形式。

当控制文件启用 `reader_evidence_protocol: "1.0"` 时，H8A/H8B 必须同时读取 `contest-orchestrator/references/paper_author_evidence_protocol.md`。将 H5/H6 的技术卡片转写为论文作者可用的论证输入，而不是把字段名或检查项复制进正文：每章建立“开篇张力—证据序列—解释动作—过渡问题”的 `authoring_arc`；结果段按“观察模式—比较基准—决策含义—边界或例外”展开；代码和算法材料转写为变量、关系、输入输出、迭代条件和可复现参数的数学叙述。若模型卡、结果解释卡或视觉槽位缺少必要证据，返回 `evidence_gap` 并指出应回补的 H5/H6/H7 材料，不以泛化背景、重复数字或形式化段落补足篇幅。该协议只约束写作准备和审阅，不改变模型、结果、引用、图表语义或排版命令。

### 视觉论证槽位的写作转写

Harness H8 和 MathorCup M4 只读取已批准的 `visual_argument_plan.yaml` 和已登记图表。Harness 按 `figure_intent`，MathorCup 按已批准图位的读者问题、证据、正文落位和图注主张安排图前引入与图后解释；若图位含 `figure_intent`，其 `body_anchor`、`pre_text_function`、`post_text_function`、`must_show` 和 `must_not_show` 同样约束正文。不得在论文中直接输出这些控制字段名或把它们改写成清单。

上述“只读取已批准图表”的限制适用于正式接图与完成稿。MathorCup 的 `chapter_parallel` 章节初稿可含内部图位占位，并在章节批准后由 writer 生成有冻结证据的提示词，不能因此虚构成图内容、数据趋势或 QA 通过。提示词在用户转交后才约束正式成图；不得为配合初稿而扭曲真实结果。历史 `writer_first_batches` 保留其批次需求解释。

论文 agent 不得因为版面、图数或模板要求新增图表，不得替换已批准路由，不得给流程图/技术路线图补写无必要公式或数据，也不得给机制/几何图补写未登记的关系。若图位缺少可解释的证据、正文落位冲突，或图内实际内容无法支撑 `reader_takeaway`，返回 `evidence_gap` 或图表位置缺口，由主控回流当前模式的图表节点补齐；不得靠泛泛图后评价掩盖缺口。

## 强制输入

执行修改前必须有：

1. 论文项目根目录和明确的目标章节；
2. 明确的比赛类型及当前官方规则配置；`active_mode: full-contest-mathorcup` 必须读取项目 `competition_profile.yaml`，不得按中文论文默认判为国赛；
3. 已冻结的模型、代码、结果和图表；MathorCup `chapter_parallel` 的章节初稿只要求冻结科学证据，正式图在用户批准该章并转交其提示词后制作，完成稿仍须接入选定图表；历史 `writer_first_batches` 保留批次需求解释；
4. 当前 `.tex`、`.bib` 及其来源文件；
5. 修改前快照目录，或由本技能先创建隔离快照。

缺少模型结果来源、引用数据库或修改前快照时，只能输出审阅意见，不得直接改写文件。

## 允许与禁止

允许修改：普通正文中的句式、段落衔接、冗余表达、术语一致性和章节组织建议。

默认禁止修改：

- 公式、公式编号、公式标签、变量、单位和约束；
- `\cite`、`\ref`、`\label`、参考文献数据库及引用顺序；
- 数字、误差、成本、厚度、百分比和结果值；
- `table`、`tabular`、三线表命令、图表编号和图片路径；
- 代码、数据、模型参数、目标函数和算法实现。

如确实需要改动上述内容，必须退出普通润色模式，交回 `contest-orchestrator` 的模型/结果一致性流程，并由用户明确授权。

## 固定执行流程

1. 读取 [references/mathmodel_rules.md](references/mathmodel_rules.md) 和 [references/upstream_map.md](references/upstream_map.md)。
    2. 国赛任务额外读取 [references/cumcm_content_redlines.md](references/cumcm_content_redlines.md)，编辑前先扫描目标章节，命中红线时输出【国赛内容红线：xxx】标记，不自行修复内容层问题；目标章节包含摘要时，额外读取 [references/cumcm_abstract_check.md](references/cumcm_abstract_check.md) 执行摘要专项检查，并读取 [references/abstract-writing.md](references/abstract-writing.md) 的实例写法（含信贷/ RGV 等非机理题型示范）；**仅国赛 B 题（优化决策类）任务读取其中的"B 题专属摘要模板"章节**；**仅国赛 B 题的建模求解章节必须读取 [references/b_chapter_templates/README.md](references/b_chapter_templates/README.md)，按问题编号和形态读取对应模板文件并使用骨架结构与必选项清单**；**所有论文写作任务必须读取 [references/anti-defensive-writing.md](references/anti-defensive-writing.md)（防防御性写作指南，数学建模竞赛版），只围绕有证据的结果组织叙事**；**Harness H8 任务必须读取 `contest-orchestrator/references/paper_author_evidence_protocol.md`，按读者问题、证据序列、解释动作和过渡问题组织作者简报与章节卡**；目标章节含图表时，额外读取 [references/figure-placement-rules.md](references/figure-placement-rules.md) 执行图表位置纪律扫描（连续浮动体、图前后缺文字、[H] 强制位置、图前后解释和布局入口），命中输出【图表位置：xxx】标记，不自动改变图表语义、路径、编号或尺寸；正文只能调用登记中已有的 `layout_mode` 和排版技能提供的布局宏。
3. 需要论证中心编辑时，再读取 [modules/claim-centered-editing/MODULE.md](modules/claim-centered-editing/MODULE.md)。
4. 只读运行审阅模块，选择 `review-chapter`、`style-check`、`terminology`、`consistency` 等必要角色；不自动并行调用全部子模块。
5. 在隔离副本中生成正文修改，保留原项目不变。
6. 运行：

   ```text
   python scripts/mathmodel_patch_guard.py <before_dir> <after_dir> --strict --out patch_guard.json
   ```

7. 只有保护器 PASS，才允许将普通正文补丁合并回论文项目；随后运行 LaTeX 编译、引用检查和 `contest-orchestrator` 的交付门禁。
8. 写作风格客观检查：读取 [references/style_guide.md](references/style_guide.md)（写作风格规范，含句长变化、段落长度变化、避免列表堆砌、自然过渡、避免套话、跨章节差异化），并运行 `python scripts/style_check.py <paper.tex> --out style_report.json` 进行六项客观指标检查（句长均匀度、段落长度均匀度、列表堆砌、机械过渡词、跨章节短语重复、套话密度），WARN 项需要针对性修改。
9. 最后按需执行自然化去痕：读取 [modules/humanizer/MODULE.md](modules/humanizer/MODULE.md)（humanizer-zh 能力本地模块，作为本技能固定后编辑器），并再次运行保护器。

## 写作素材（按需加载）

- 常用表达与句式库（正文写作/润色参考）：[references/common-phrases.md](references/common-phrases.md)
- 题型策略（按题面类型选表达与结构策略）：[references/problem-type-strategies.md](references/problem-type-strategies.md)
- 去 AI 味完整清单（8 类痕迹 + 数模禁用词/结果铁律，与 modules/deai 互补）：[references/de-ai-writing.md](references/de-ai-writing.md)
- 摘要写作实例（3 个完整示范，覆盖机理/数据/优化三类）：[references/abstract-writing.md](references/abstract-writing.md)
- 图表位置纪律（防浮动/防连图/防错位，写作阶段与编译后扫描规则）：[references/figure-placement-rules.md](references/figure-placement-rules.md)
- 写作风格规范（降低AI生成感：句长变化、段落长度变化、避免列表堆砌、自然过渡、避免套话）：[references/style_guide.md](references/style_guide.md)
- **国赛 B 题建模求解章节模板库**（五层结构：题型判定+骨架+必选项+写作要点+特色空间，覆盖问题一至四共8种形态，含反机械硬约束和自查清单）：[references/b_chapter_templates/README.md](references/b_chapter_templates/README.md)，仅国赛 B 题建模求解章节读取并使用
- **防防御性写作指南**（数学建模竞赛版，核心原则：论文是学术发布会不是项目总结，只围绕优势组织叙事，不写工作汇报，禁用自我削弱表达，每个结果必须有论证职责，结论只强化记忆点，不给评委递刀子）：[references/anti-defensive-writing.md](references/anti-defensive-writing.md)，所有论文写作任务必须读取并使用

## 上游更新

上游版本由 [UPSTREAM_LOCK.yaml](UPSTREAM_LOCK.yaml) 锁定。禁止自动拉取上游更新；升级必须在隔离目录中进行，并通过技能结构检查、保护器负面测试和至少一次数学建模论文 replay。

## 交付物

- 修改前后差异报告；
- `patch_guard.json`；
- 学术表达问题清单；
- 编译和一致性检查结果。

没有差异报告或保护器结果时，不得声称论文已完成润色。
