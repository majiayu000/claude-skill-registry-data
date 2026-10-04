---
name: light-slides
description: 制作精美 PPT。当用户需要为论文、项目、竞赛、答辩、汇报、路演做幻灯片时使用。设计封面/目录/过渡/内容/图表/流程/时间线/对比/团队/结论/致谢等页。逻辑清晰、排版高级、审美统一、重点突出，按主题选风格（学术/科技/农业/医学/商务/极简/浅色/深色/数据可视化/竞赛路演）。不仅生成内容，还规划整套叙事逻辑、视觉风格、页面层次与演讲节奏。
---

# 精美 PPT 制作

## 路线（python-pptx 程序化）
- python-pptx 程序化出可编辑 pptx（`assets/themes.py`/`patterns.md`/`examples/build_deck.py`），数据密集、批量出页、表格密集均走这条。需要更强设计感时，可借 PptxGenJS/Marp/reveal.js/Beamer（见下「实现工具」），但 Light 自带可运行资产以 python-pptx 为首选路线。
- **三条硬边界**（与 m11/a10 互引，红线）：①数据图一律走 m11/m06 真数据出图，绝不让生成式模型画数据图（会编造数值）②论文图链路严禁任何 AI 生成图像（出版商禁令，见 m11 `light-figure-drawing/references/figure_integrity.md`「AI 生成图像政策」节）③文本一律落原生文本框，不烤进图片（否则"可编辑"是假的）。

## 先定三件事
1. **场景与受众**：答辩(评委/导师) vs 路演(投资人/评审) vs 汇报 —— 决定内容深度与节奏。
2. **叙事逻辑**：选骨架(问题-方法-结果-价值 / 痛点-方案-市场-团队 / 背景-工作-贡献-展望)，先列大纲(每页一个核心信息)。
3. **视觉风格**：按主题从 db06 选风格(学术/科技/农业/医学/商务/极简/浅/深/数据可视化/路演)，定调色板+字体配对+图标风格，全程统一。**项目有 `databases/db09-projects/projects/<project_name>/palette.json` 则必用其取色**（与论文图 m11/前端 a05 共享的视觉 SSOT 实例；schema 见 db09 README），保证 PPT 与论文图/前端同色，不另起一套。版式/叙事方法(action-title/一页一观点/data-ink/控时公式)以 db06 卡为 SSOT,本 SKILL 不另写一份;工具星标/许可/链接不信本地快照,跑 `databases/db06-ppt-styles/scripts/resource_signal.py` 实时核(GitHub stars+spdx/PyPI license/URL 存活),冲突信在线、无网用快照标 stale、不阻断出稿。

## 页面类型与排版
封面(标题/作者/单位/日期)、目录、过渡页、内容页(一页一观点+留白)、图表页(图大字少)、流程页、时间线页、对比页、团队页、结论页、致谢/QA 页。
排版原则：对齐、对比、重复、亲密性；视觉层次(标题>要点>细节)；每页信息密度受控；高亮一个重点。
具体尺度(借 Anthropic PPTX skill)：一主色占视觉权重 60–70% + 1–2 辅色 + 1 个尖锐强调色；深色用于封面/结论、浅色用于内容(三明治结构)；锁定一个重复视觉母题(圆角图框/色环图标/单边粗边)并贯穿全篇。字号 标题 36–44pt、节标题 20–24pt、正文 14–16pt、注释 10–12pt；页边距≥0.5"，块间距统一取 0.3" 或 0.5"。正文一律左对齐、仅标题居中。每页必须有视觉元素，禁纯文字页。
明确禁忌：标题下不要加装饰下划线(AI 味标志，用留白代替)；不要每页重复同一版式；不默认蓝色(按主题选色)；文本框要与形状对齐时设 margin=0。

## 学术报告专项（论文/答辩/会议）
- **行动式标题(action title)**：每页标题写成陈述结论的完整句子，不是话题标签(写"三个队列处理效应均显著"而非"Results")。
- **幽灵 deck 测试**：只读所有标题连起来要能讲完整个论证；不行先改大纲再做页。
- 叙事骨架三选一：SCR(情境-冲突-解决) / 漏斗+答案(背景→缺口→方法→发现→意义) / 答案先行(时间紧的评委)。
- 一份报告只讲一个论点，其余进附录；每页一个职责、一个 exhibit。结果页：图放左、解读 bullet 放右；在图上直接标注关键发现(箭头/高亮区/"↑23%"/焦点序列变色)；正文≤~40 词/页；以 Conclusions 收尾而非"Thank You"。
- 学术配色更克制：白底、单一无衬线字体、最多三色(主 `1F4E79`+辅 `2E75B6`+强调)、无装饰图标/渐变。

## 实现工具（按需，见 a09）
按"是否需可编辑 PPTX / 文本化版本控制 / 设计强度"选型：
- **python-pptx**(Python，**本 skill 自带可运行资产的首选路线**)：`Presentation()` → `slides.add_slide(slide_layouts[i])` → 占位符/`add_textbox`/`add_picture`/`add_table`/`add_chart` → `save()`；单位 `Inches/Pt`、色 `RGBColor`。强在数据驱动批量出页、表格密集、衔接 m06/m11 的 Python 分析链路；无渐变(用渐变图当背景)、不能自渲 PDF(走 LibreOffice)。
- **PptxGenJS**(Node)：`new pptxgen()` → `addSlide()` → `addText/addShape/addImage/addTable/addChart` → `writeFile()`，坐标=英寸。列表项用 `bullet:true`+`breakLine:true`(忌 Unicode `•`)；与形状对齐设 `margin:0`；阴影 offset 必须≥0、color 用 6 位 hex 无 `#`；无渐变(用渐变图当背景)。Anthropic 通用 deck「从零创建」首选；**JS 路线本 skill 不带可运行资产，直接走 a09 → anthropics/skills 的 pptxgenjs.md**。
- **Marp**(Markdown)：front-matter 设 `theme/paginate/headingDivider/style`，`---` 分页，`<!-- -->` 写备注；`npx @marp-team/marp-cli deck.md --pdf|--pptx`(走无头浏览器)。`--pptx` 默认每页栅格化成图不可再编辑，需可编辑文本加 `--pptx --pptx-editable`(样式可能复现不全)。
- **reveal.js**(HTML)：`Reveal.initialize({plugins:[Markdown,Notes,Math]})`；`section` 分页、嵌套=纵向；`?print-pdf` 导 PDF；交互/动画强但分发不如 PPTX。
- **Beamer**(LaTeX，学术)：`\documentclass{beamer}`+`\usetheme{}`；`frame`/`columns`/`block`/`alertblock`；overlay 用 `\item<1->` 或 `\pause`；公式/BibTeX 强、视觉迭代慢。
- **海报**：LaTeX `beamerposter`(`\usepackage[orientation=portrait,size=a0,scale=1.4]{beamerposter}`) 或 `tikzposter`(`\block{}{}`)；或 PPTX 海报(把 slide 尺寸设成 A0 单页，python-pptx 设 `slide_width/height`)。A0=841×1189mm，照片≥150–300 DPI、嵌字体防错位。
- **设计/AI 向**(可借工作流，闭源)：Canva Connect API(`POST /autofills` 品牌模板批量填充，需 Enterprise)、Gamma Generations API(`POST /v1.0/generations` prompt→deck，可 `exportAs:pptx/pdf`)、Beautiful.ai(规则驱动自适应版式理念)、Slidesgo(模板灵感按行业/风格/色筛)。
- **3D 渲染配图(路演/展示用)**：Blender（开源免费，程序化建模渲染**非 AI 生图**；有社区 ahujasid/blender-mcp ~22.7k★ 与 Blender 基金会官方 Lab MCP，需本地装 Blender）可出 3D 产品/装置/结构示意渲染图，给创业路演/挑战杯现场感。**严守三条硬边界**：3D 渲染图只作**装饰/展示配图**，不作数据图（数据图走 m11 真数据）、不进论文图链路、文字仍落原生文本框。科研数据/结构的 3D 可视化见 m09(figure-planning) 的 Blender 节。
- **流程/架构/路线图**：用 **Draw.io MCP**（diagram-as-code，官方 jgraph/drawio-mcp）出流程图/系统架构图/技术路线图，导出 PNG/SVG 嵌入 PPT——比手摆 python-pptx 形状整齐、可编辑可复用，契合"图大字少"原则。仍守红线：图里文字若是关键标题/要点，落 PPT 原生文本框；数据图走 m11。
- **从论文一键转稿**：两条路线择一——图像渲染路线（Paper2Slides/HKUDS，RAG→分析→规划→渲染，分阶段 checkpoint）适合图文均衡稿；LaTeX/Beamer 路线（takashiishida/paper2slides，flatten 源→LLM 出 Beamer→chktex lint→编译）适合公式重的硬核论文。两条的完整 CLI/参数/实测教训见 `references.md`（paper2slides 两节）。
图表复用论文图(m11)并适配投影：从论文重画而非直接贴 PDF 图，放大轴标≥16pt、增强对比。
- **生图边界（与 m11 figure_integrity 互相指认的硬红线）**：上述 AI 生图/渲染路线（Gamma、Paper2Slides 等外部工具的产物）**只用于 PPT/路演/前端灵感图，严禁任何产物进入论文图链路**。论文图一律走 m11(light-figure-drawing)数据驱动绘制——Nature/Science/Elsevier 三家头部出版商明令禁止 AI 生成论文图像（见 light-figure-drawing `light-figure-drawing/references/figure_integrity.md`「AI 生成图像政策」节）。PPT 里若要放实验数据图，从 m11 成品重画适配投影，不要用生成式模型造数据图。

## 演讲节奏
为每页配 speaker notes 与时长建议；标出"必讲/可略"；控制总页数匹配时长(答辩常 8–12 min ≈ 10–15 页)。

## 审美自检（出稿前）
□ 风格统一(色/字/图标) □ 每页一个重点 □ 无大段文字 □ 图表清晰可投影 □ 对齐整齐 □ 逻辑连贯 □ 重点突出 □ 页数匹配时长。
学术加测：□ 每页有行动式标题 □ 幽灵 deck 测试通过 □ 每结果页一图且有"so what"标注 □ 借用图/数据有页内引用 □ 末尾有 References 页 □ 以 Conclusions 收尾 □ 正文≥20pt。

## 本 skill 自带可运行资产（直接用，别重造）
- `assets/themes.py`：db06 十大主题的 `COLORS/FONTS` 常量块（学术/科技/农业/医学/商务/极简/浅色高级/深色高对比/数据可视化/竞赛路演），统一 8 字段色板(bg/surface/primary/secondary/accent/text/muted/line)+字体配对。`from themes import get_theme; t=get_theme("academic")`。dataviz 额外带 Okabe-Ito 色盲友好序列。`python themes.py` 自测打印全表。
- `patterns.md`：python-pptx 可直接跑的版式片段——封面/目录/过渡/内容/结果(左图右解读)/对比(高亮列表格)/时间线/结论/References，含 `fill_bg`(无原生页背景的全幅矩形法)、`add_text`(margin=0)、`rect` 等共用工具函数。**`add_text` 走 `_set_run_fonts` 同设拉丁+东亚字体(中文不回退默认黑体)**、`style_chart` 给原生图表套主题色(不沿用 Office 默认蓝橙灰)、`add_figure_with_caption` 导入 m11 成品图+caption(数据图不在 PPT 重画)。
- `examples/build_deck.py`：端到端生成 6 页学术 pptx(封面+内容+结果+对比+**结论收尾**+References，对齐"Conclusions 收尾不写 Thank You"规则)，每页配 speaker notes，`add_text` 同设拉丁+CJK 字体，自带幽灵 deck 测试。`python build_deck.py --theme tech -o tech_demo.pptx`，无需外部数据即可跑。
- `scripts/thumbnail.py`：pptx→缩略图网格做视觉 QA。优先 LibreOffice 像素渲染(需 soffice + PyMuPDF/pdftoppm)；无 soffice 时自动回退纯 python(读 python-pptx 几何用 PIL 画版式示意图)，足以抓重叠/溢出/空页/对齐/版式重复。`python scripts/thumbnail.py deck.pptx --cols 4`。
- `scripts/pptx_eval.py`：**PPT 可量化评测**(借 PPTAgent/PPTEval 思路)。把视觉 QA 从肉眼查升级为可打分、可回归——内容密度/设计一致/连贯性三维扣分制(对照本节硬尺度：每页≤7 要点、字号区间、配色数、禁纯文字页/同版式)，逐页给分+扣分理由。`python scripts/pptx_eval.py deck.pptx`。**只算结构性指标，配色品味/叙事质量/图是否真数据仍须人工 + thumbnail 肉眼复核**。与 thumbnail 互补：thumbnail 给人看、pptx_eval 给分。
- `scripts/to_pdf.py`：pptx→pdf 的 soffice 无头封装。本环境未装 LibreOffice，脚本会明确报 unavailable 并给安装指引+备选(不静默假成功)。`python scripts/to_pdf.py deck.pptx`，`--check` 只探测引擎。
- `scripts/pacing.py`：**答辩/路演时长估算**。读每页 speaker notes 的时长标记(`40s`/`1.5min`/`[90s]`)累加估总时长，对照 `--limit` 给 OK/超时 + 标出时长偏重的页(分配失衡)；无标记页按字数×语速兜底。`python scripts/pacing.py deck.pptx --limit 12`。时长是估算，务必真人计时彩排——脚本只抓明显超时/失衡。

## QA（当 bug 猎，别当确认）
出稿后默认有问题。① 内容 QA：`python -m markitdown out.pptx` 查缺漏/错字/顺序，并 `grep -iE "xxxx|lorem|ipsum"` 抓残留占位符。② 视觉 QA：优先 `python scripts/thumbnail.py out.pptx` 出缩略图网格逐页扫(无 soffice 也能出版式示意)；有 LibreOffice 时 `python scripts/to_pdf.py out.pptx` 转 PDF 再 `pdftoppm -jpeg -r 150 out.pdf slide` 出高保真图，逐图找重叠/文字溢出/低对比/对齐错位/边距不足/装饰线压两行标题；有子代理就交给它(新鲜眼睛)。③ 改完只重渲受影响页，循环到整轮无新问题才收。

## 衔接
内容来自 m07(论文正文)/m06(结果)，图表来自 m11，竞赛路演来自 m17；视觉风格与 a05/m11 协调(由 a07 统一术语与指标)；文件解析借 a01；版本与风格登记 db06/db09。交付前过 a08(light-self-review)自检闸门。

## 产出
完整 PPT(源文件 + 导出) + 叙事大纲 + 每页 speaker notes + 风格说明(登记 db06/db09)。

落盘工件名（CONVENTIONS §6.1，下游 orchestrator/a08 按名调度）：`slides/`（源 pptx + 导出）+ `slide_outline.md`。

## 合规
商用模板只学版式不直接复制(CONVENTIONS §5)；最终原创化。内容与论文/项目一致(a07)。Canva/Gamma/Slidesgo 等闭源/模板源借工作流与版式灵感，授权条款须先确认；Anthropic/academic-pptx 等专有 skill 只学方法不照搬脚本。

工具逐项硬核笔记(真实端点/参数/坑)见 references.md。
