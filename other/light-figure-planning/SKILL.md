---
name: light-figure-planning
description: 根据论文内容规划应该做哪些图、哪些表、插在哪里、各起什么作用。当用户需要论文图表规划时使用。图表不限于统计图，也包括数据集真实效果图、模型输出示例、案例展示、可解释性可视化等。规划框架图、技术路线图、数据集示意图、模型结构图、算法流程图、结果对比/消融/敏感性图、真实效果图、统计表/对比表等，以审稿人标准判断哪些必做、哪些冗余。
---

# 论文图表设计规划

## 定位
图表服务论点，不是装饰。每个图表先回答：**它支撑哪个 claim？删掉它论文会不会缺一块？**

## 规划流程
1. 通读论文(或大纲) + m06 结果，列出全部 claim。
2. 给每个 claim 匹配最有说服力的呈现形式。**可跑 `scripts/recommend_chart.py --task <比较/分布/关系/构成/趋势/排序/占比/不确定性> --fields <定类/定序/定量/时间...> --n-series N`** 拿启发式候选图型排序（依据 Cleveland-McGill 感知精度+任务族先验，输出理由/注意）——是**可解释建议非真值**，最终结合 claim 重要性/领域惯例/期刊偏好人工定夺。
3. 标注优先级：**必做**(支撑核心贡献) / **可做**(增强) / **可删**(冗余或弱)。
4. 排版位置：哪张进正文、哪张进附录、组图怎么组。
5. **display item 预算核查**：统计正文 F#+T# 总数，对照目标 venue 上限（顶刊/顶会常 **6–8 件**，以目标刊作者指南为准）。**超预算强制取舍**，砍序固定：先砍"可删" → "可做"降到附录 → "必做"不动（删了就没核心论证的不许砍）。合并同质图、把次要分析移附录也是减件手段。把总数核查写进交付（见自检清单数量项）。完整示例见 [examples/worked_example.md](examples/worked_example.md) 的 claim→图表清单全景。

## 图表类型清单（按需选，附建议工具）
- **概念/方法**：框架图、技术路线图、模型结构图、算法流程图、数据流图。→ 精排可编辑源用 diagrams.net/Draw.io(XML，有官方 MCP，diagram-as-code)；与 LaTeX 同源用 TikZ；关系/依赖自动布局用 Graphviz(dot)；文档内嵌草图用 Mermaid；3D 结构/分子/科学可视化用 Blender(+Molecular Nodes/SciBlend 插件)。
- **数据**：数据集示意图、样本分布、标注示例。→ 统计分布用 seaborn/matplotlib；示意排版用 draw.io/TikZ。
- **定量结果**：主结果对比图/表、消融图、参数敏感性曲线、收敛曲线、ROC/PR、混淆矩阵、雷达图。→ matplotlib(精排)+seaborn(统计便捷)；R 用 ggplot2；交互补充材料用 Plotly/Altair。
- **定性结果**：真实效果图、模型输出示例、case study、失败案例、可解释性可视化(注意力/SHAP/特征图)。
- **表**：指标汇总表、对比表、消融表、数据集统计表、复杂度表。

## 论文三类核心图 · 范式速查（借 figure-designer 的范式库思路，规划产出落到具体范式而非"放一张图"）
规划这三类图时，直接挂一个范式 + 布局骨架，而非泛泛"建议放方法图"：
- **动机/问题图（intro）**：范式 = "痛点对比"（左现状缺陷 vs 右本文改善）或"概念示意"（抽象问题具象化）。布局：左右并置或单幅大示意；放 §1 末。常见错误：塞太多细节、过早展示方法。
- **方法总览图（method）**：范式 = "管线流（pipeline）"（输入→模块→输出，箭头标数据流）或"架构图"（模块堆叠+连接）。布局：横向流水线（窄高比，适合双栏顶部）或纵向；创新模块用强调色/虚线框圈出。工具 Draw.io/TikZ，非 AI 生图。放 §3 开头。
- **结果图（results）**：范式 = "分组柱+误差棒"（多方法多数据集比较）/"折线+置信带"（趋势/收敛/敏感性）/"散点+回归"（相关）/"热力图"（矩阵/消融网格）。布局：主结果单图大、次要进组图。必带误差棒+显著性+n。`recommend_chart.py` 可按 claim 数据形态推荐具体范式。
> 范式只是起点骨架，最终按 claim 与数据定。参考样例池：可挂高质量同类图链接（如 dair-ai/ml-visuals 模板、awesome-scientific-figure）作规划参照，但**论文数据图必须用真实数据程序化绘制，不照搬不 AI 生成**。

## 工具选型速查（写进规划卡的"建议工具"字段）
- **统计/定量图**：matplotlib（控制最细）、seaborn（自动 CI/分面）、ggplot2（R 的 grammar of graphics）、Plotly/Altair（交互+静态导出）。
- **信号/控制/数值仿真类图**（频谱/FFT、Bode/根轨迹、Simulink 仿真输出）：MATLAB（信号/控制工具箱原生，`exportgraphics` 出矢量）——尤其项目本就在 MATLAB 生态时；有官方 MATLAB MCP Core Server（跑本地 MATLAB，配置见 README 推荐 MCP 表），执行端 m11 figure-drawing 已支持，规划卡"建议工具"字段对这类图填 MATLAB 即闭环。
- **出版级矢量、公式标签多**：TikZ/PGFPlots，与 LaTeX 同源，字体公式无缝。
- **框架/系统图，要可编辑矢量源**：diagrams.net/Draw.io（`.drawio` 即 mxGraph XML，可程序化批量改、纳 Git 版本控制；有**官方 MCP** jgraph/drawio-mcp 与社区 lgazo/drawio-mcp-server，可让 AI 生成/编辑 .drawio；CLI `drawio --export --format pdf/png/svg` 批量出图，脚本化注意锁版本，详见 references）。
- **关系/依赖/自动布局**：Graphviz（dot 分层；neato/fdp 弹簧；sfdp 大图）。
- **文档内嵌草图/流程**：Mermaid（GitHub/Notion 原生渲染，diagram-as-code）。
- **3D 科学可视化/结构/分子**：Blender（开源免费，程序化建模渲染**非 AI 生图**；有社区 ahujasid/blender-mcp 与 Blender 基金会官方 Lab MCP）。**成熟科研路子是直接用专用插件**：Molecular Nodes（蛋白/PDB/轨迹）、SciBlend（科研数据可视化）、AstroBlend（天文）；**用 MCP 让 AI 自然语言驱动这些科研可视化目前实践尚少**，属探索方向。3D 渲染作论文图须保证数据真实可复现（标清渲染参数/数据来源），否则更适合路演/展示（→ m16 slides）。生命科学通路/机制示意图若需专业图标库，BioRender 等 SaaS 可手工做（其官方 MCP 仅查询不能作图，故不列为程序化路径）。
- **最终多-panel 拼版/对已导出图手工精修矢量**：Inkscape（免费，CLI `inkscape in.svg --export-type=pdf,svg`，转曲 `--export-text-to-path`）或 Adobe Illustrator（行业标准，`.ai` 私有非开放格式，跨工具存 PDF/SVG）。把异源面板（mpl 导出 PDF + 位图 + 文字标签）自由对齐组装成单张投稿图。

## 出版级硬规格（规划卡里据此约束执行）
- **分辨率/格式**：线稿矢量(PDF/EPS/SVG)或 600–1200 DPI；位图 300–600 DPI、TIFF/PNG，**绝不用 JPEG 存科研数据**。matplotlib 设 `pdf.fonttype=42` 避免 Type-3 字体被拒。
- **配色**：离散用 Okabe-Ito（`#E69F00 #56B4E9 #009E73 #F0E442 #0072B2 #D55E00 #CC79A7`），连续量用 viridis/plasma/cividis；颜色之外加冗余编码(线型/marker)；**灰度+色盲双测**。
- **字体**：无衬线(Arial/Helvetica)，标签 sentence case，单位入括号。**最小字号按刊定，别一刀切**：Nature 官方实测下限 **5 pt**（仅 Nature，✅ curl www.nature.com 逐字命中 5–7 pt），但**多数刊与通用稳妥下限是 6–7 pt**（不少绘图工具默认建议 6–8 pt）——除非确认目标刊允许，**别低于 6 pt**，5 pt 只在确认是 Nature 时用。最终印刷尺寸下判读。
- **列宽**（按目标期刊设图宽，mm；**下列数字仅为快照，运行时唯一真相源是 light-figure-drawing `figure_export.py` 的 `JOURNAL_SPECS`——出图前以脚本动态读到的为准，本表数字若与之不符以脚本为准**；最后同步 2026-06-11。下值仅 Nature 经 curl 实测，其余出版商官网对 curl/WebFetch 返回 403 付费墙，为公开作者指南通行值，投稿前务必以目标刊官网为准）：
  - **Nature**（✅ curl 实测 www.nature.com/nature/for-authors/final-submission，HTTP 200）：单栏 **89**、双栏 **183**，最大高 **170**（留题注空间）。
  - **Science (AAAS)**（栏宽数字以 light-figure-drawing `figure_export.py` JOURNAL_SPECS 为唯一真相源；三档制经联网多源核实 2026-06-11）：单栏 **55**(5.5 cm)、双栏 **120**(12 cm)、整页 **183**(18.3 cm)。注意 Science 无"175"这一档。
  - **Cell Press**（⚠️付费墙未实测）：单栏 **85**、1.5 栏 **114**、整页 **174**。注意整页是 174 非 178。
  - **PLOS**（✅ curl 实测 journals.plos.org/plosone/s/figures，HTTP 200）：单栏 **83**、1.5 栏 **140**、整页 **190**；仅收 TIFF/EPS，789–2250px@300dpi、高 ≤2625px、字 Arial/Times/Symbol 8–12pt、单文件 <10MB。栏宽数字以 `figure_export.py`（light-figure-drawing）`JOURNAL_SPECS` 的 `plos` 键为唯一真相源。
  - **Elsevier**（⚠️付费墙未实测，含 db01 的 Computers and Electronics in Agriculture 等）：最小 **30**、单栏 **90**、1.5 栏 **140**、双栏/整页 **190**。
  - **IEEE**（⚠️付费墙未实测，IEEEtran 双栏版式）：单栏 ≈**88.9**(3.5 in)、双栏/整页文本宽 ≈**181.9**(7.16 in)。
  - **MDPI**（⚠️付费墙未实测，含 db01 的 Animals）：单列版式正文宽 ≈**170**，图按此宽或其整数分数排；线稿/组合图建议 1000 DPI、照片 ≥300 DPI。
  - **中文刊**（✅ 2026-06-11 从发表 PDF 实测，pdfplumber 词边聚类，已落 db01 risk_note）：**农业工程学报** 单栏≈**86**、整页≈**180**（A4 双栏）；**中国农业科学**、**作物学报** 单栏≈**81**、整页≈**170**（A4 双栏）；**农业机械学报** PDF 入口被反爬拦截，标**待核查**。中文刊不在 `JOURNAL_SPECS`，用 `journal="custom", custom_width_mm=<db01实测值>` 逃生通道出图。
  - 导出按 mm 设尺寸（如 ggplot2 `ggsave(w,h,units='mm',dpi=300)`、mpl `figsize` 换算）。
- **统计严谨**：必带误差棒(SD/SEM/CI，caption 注明)、样本量 n、显著性标记，尽量画散点。
- **多 panel**：matplotlib GridSpec / subplots；加粗大写 A/B/C 标号；跨 panel 风格、尺度一致。
  - **反冗余（组图的核心检验）**：每个 panel 必须回答一个**唯一的科学问题**——遮住任意一个 panel，应造成无法从其它 panel 补回的信息缺口。两个 panel 用不同图形回答同一问题，就是冗余。常见冗余陷阱：① 同一数据画了"绝对值 bar"又画"绝对值表"；② 一个 panel 是另一个的子集/父集；③ 两个排序图传递相同次序信息。发现冗余→合并、删除，或换成能回答新问题的视角（如把第二个绝对值图改成"相对基线的偏差"）。
  - 多 panel 推荐信息递进：overview（全景）→ deviation（偏差/对比）→ relationship（变量关系），层层补充而非重复。

## db07 查找纪律与规划卡边界
- **先查 db07 canonical**：通用图表模式查 `databases/db07-figures/resources_real.md`；高级/领域规范图查 `databases/db07-figures/figure_advanced_cards.md`；`figure_cards.md` 只保留模板 + canonical 索引，**不得再写实体卡**。
- **按 research_field 过滤偏科卡**：先读项目方向(db09 项目卡 domain),按 db07 README 的 research_field 受控取值表只在 `通用` + 命中的领域专属图型(如 GWAS→Manhattan、生存分析→KM、方法学比较→Bland-Altman)两个集合里选卡,不给非该方向用户推 volcano/CONSORT 等偏科卡;项目方向缺失时降级为不过滤、全集候选。
- **replication_notes 引用铁律编号**：规划卡的 color_scheme/replication_notes 直接引用 db07 README『制图方法论铁律 R1-R9』编号(如"遵 R1/R8"),不再各卡复述通用诚实性规则,保持单一真相源。
- **db07 是可复用图表模式库**：只沉淀跨项目通用的 `figure_card`。某个具体论文的 F1/F2、caption、目标期刊、导出文件路径属于项目级产物，写入仓库根目录下的 `databases/db09-projects/projects/<project_name>/version_history.md` 与 `projects/<project_name>/figures/manifest.md`，不直接塞回 db07。
- **选型顺序**：先把每个 claim 映射到已有 canonical `figure_type`；如果确实没有匹配，再规划新增一张可复用 figure_card 到 `resources_real.md` 或 `databases/db07-figures/figure_advanced_cards.md`，并保持 `figure_type` 全库唯一。

## 每个图表的规划卡（交 m11 执行）
单张图/表填一张**规划卡**（图用 [templates/figure_plan_card.md](templates/figure_plan_card.md)，**表用专用的 [templates/table_plan_card.md](templates/table_plan_card.md)**——表有自己的行列结构/表头分组/对齐/有效位数/booktabs 三线表字段，图卡的 color_scheme/layout/GridSpec 对表无意义，别共用）。规划卡分两层，避免把项目执行字段误写成 db07 schema：
1. **db07 基础字段（可沉淀为 figure_card）**：`figure_type, paper_source, research_field, purpose, data_required, layout, color_scheme, annotation_style, caption_style, possible_code_tool, replication_notes, where_to_place_in_paper`。
2. **项目执行辅助字段（只进规划交付/manifest，不作为 db07 必填 schema）**：`figure_id, priority, target_journal, column, caption_draft, output_formats, source_card`。

- **figure_id**：固定 `F#` 命名图、`T#` 命名表（F=Figure、T=Table，如 F1/F2/T1），与 m07 论文模板的 `[图位 F1]`/`[表位 T1]` 占位对齐，作为图↔图号↔caption 的锚点。
- **source_card（必填）**：记录命中的 db07 canonical 来源，如 `databases/db07-figures/resources_real.md::跨数据集主结果对比(分组柱+误差棒)`，便于 m11 照卡执行、后续追溯；只有确认为全新图表模式时，才标注 `source_card: new_canonical_candidate -> databases/db07-figures/resources_real.md`（或 `databases/db07-figures/figure_advanced_cards.md`）并后续回写 db07。
- **target_journal**：目标期刊键，取 `figure_export.py`（light-figure-drawing）的 `JOURNAL_SPECS` 键之一：`nature`/`science`/`cell`/`plos`/`ieee`/`elsevier`/`mdpi`。决定物理栏宽 mm、最小字号、首选格式，执行技能据此直接传 `save_for_journal`，避免栏宽臆测导致整张图物理尺寸作废。表外刊（如中文刊）填 `target_journal: custom` 并在规划卡补 `custom_width_mm: <mm>`（数据须有来源：db01 卡或实测记录，**禁止臆测**），执行端走 `save_for_journal(..., journal="custom", custom_width_mm=...)` 逃生通道。
- **column**：栏宽档位，取 `single`/`double`/`full`/`onehalf`（须为该刊在 `JOURNAL_SPECS` 里实有的键：`full` 仅 science/mdpi；`onehalf` 仅 plos/elsevier）。`target_journal: custom` 时 column 省略，直接以 `custom_width_mm` 为准。
**建议工具二选一判定**：异源面板组合（代码图 + 位图 + 文字标签）/ 需逐像素对齐与自由精修 → 手工矢量编辑（Inkscape/Illustrator）；同源同类数据图、追求复现性 → 代码生成（GridSpec/subplots）。
概念/示意类可先出 **ASCII 线框 + 文案 + 配色 + 图标/图表类型建议**（content-first 蓝图），把信息架构定死再交执行。

## 审稿人视角自检
- 核心贡献是否每条都有图/表支撑？
- 有没有"好看但不传递信息"的图？删。
- 表格能不能图示化得更直观？
- 组图逻辑是否清晰（同类对齐、尺度一致）？**每个 panel 回答唯一科学问题、无冗余**（遮住一个 panel 会丢失独有信息）？
- caption 能否脱离正文独立读懂？
- 示意图按 5 维评分（各 0–2，合 10）：**科学准确性 / 清晰可读 / 标签质量 / 布局构图 / 专业度**；journal 级目标 ≥8.5。**适用范围：仅限示意图/概念图/框架图这类构图主观的图**（评分源自社区 AI 生图技能）；**代码矢量数据图（柱/线/散点/热力图）改用客观 QA 项**（矢量格式、字号达栏宽下限、色盲安全、坐标轴诚实不截断、误差棒+n、caption 自洽——见下方投稿前 13 点核查），别把构图美学评分套到数据图上。
- 投稿前 14 点核查：分辨率·格式·尺寸·可读性·色盲安全·灰度兼容·坐标轴标签(含单位)·误差棒·panel 标号·显著性标记·图例清晰·字体一致·去装饰元素·**display item 总数 ≤ 目标 venue 上限**（F#+T# 计数，超则按"可删→可做降附录"取舍）。

## 交 m11 前：契约校验（可机检，前移打回）
规划卡交 m11 执行**前**，跑 `scripts/validate_plan_card.py <卡.md>...` 做契约校验，把 m11 会打回的问题拦在规划阶段：
- 校验 `target_journal` 命中 figure_export.py `JOURNAL_SPECS` 键（或 custom 带 `custom_width_mm`）、`column` 是该刊实有档位、`figure_id` 形如 F#/T# 且批量唯一（与 m07 占位对齐）、`source_card` 必填。
- 脚本**动态从 m11 的 figure_export.py 读 JOURNAL_SPECS**（单一真相源，杜绝栏宽键漂移）；导入不到回退内置快照并标 `[SNAPSHOT]`。
- 全部通过（exit 0）再交 m11；有 ✗ 先按提示补卡。这只校验可机检的契约（键存在/字段齐全/唯一），不替代图本身的质量判断。

## 衔接
规划卡交 m11 绘制；与 m07/m08 同步确保图文一致。项目级风格、图号、caption 与导出路径登记到仓库根目录下的 `databases/db09-projects/projects/<project_name>/version_history.md` 与 `projects/<project_name>/figures/manifest.md`；只有跨项目可复用的新图表模式才回写 db07 canonical 文件。全文图表风格由 a07 维护。

### 代号图例（脱离 Light 全家桶时速查本表）
| 代号 | 是什么 | 与本技能的接口 |
|---|---|---|
| m02 | data-engineering | 供数据；派生数据集回它构建 |
| m06 | result-analysis | 供结果/claim/claim_evidence_table（图的数值源） |
| m07 / m08 | paper-drafting / polishing | 供 `[图位 F1]`/`[表位 T1]` 占位，保图文一致 |
| m11 | figure-drawing | **下游执行端**：照规划卡画图；其 figure_export.py JOURNAL_SPECS 是栏宽/字号唯一真相源 |
| m12 | typesetting | 表的 booktabs 排版执行 |
| a07 | consistency | 维护全文图表风格统一 |
| db01 | 期刊库 | 目标刊与实测栏宽 |
| db07 | 图表库 | 可复用 figure_card 模式库 |
| db09 | 项目库 | 登记项目级图号/caption/导出路径/version_history |

---
工具真实端点、API 参数、各绘图库用法与已知坑见 `references.md`。
