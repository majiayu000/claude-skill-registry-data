---
name: light-figure-drawing
description: 从顶会大牛角度进行专业绘图与组图。当用户需要把规划好的图实际画出来时使用。按情况用 Python(matplotlib/seaborn/plotly/altair)、R(ggplot2)、MATLAB、Visio、Origin、LaTeX/TikZ、Illustrator、PowerPoint 等。审美统一、专业清晰、配色合理、字体规范、线条清楚、高分辨率，适合直接投稿。不仅画图，还从论文表达角度判断怎么排、怎么组、怎么标注、怎么突出重点。
---

# 专业绘图与组图

## 工具选择（按图类型，附核心调用）
- 统计图/可复现图（首选）：
  - **matplotlib**：最可控。组图 `plt.subplots(figsize=(7,5), constrained_layout=True)`，不规则布局用 `GridSpec`（跨格 `gs[0,:]`）。
  - **seaborn**：统计/分布/分类图。`sns.set_theme(style="ticks", context="paper", palette="colorblind")` + `sns.despine()`；分面拼图用 figure-level（`relplot/catplot` 的 `col=/row=`），手动拼图用 axes-level（`scatterplot(ax=...)`）。
  - **plotly**：交互/3D，静态投稿 `fig.write_image("f.pdf", scale=3)`（需 `kaleido`），`template="simple_white"`。
  - **altair**：声明式、可复现强。`chart.save("f.svg", scale_factor=3)`（需 `vl-convert-python`），拼图用 `c1 | c2` / `c1 & c2`。
  - **ggplot2(R)**：`+ theme_classic() + scale_color_viridis_d()`，拼图用 `patchwork`（`p1+p2` 且 `plot_annotation(tag_levels="a")` 自动标号）。
- 框架图/流程图/结构图：
  - **Graphviz**（自动布局）：`digraph{rankdir=LR; node[shape=box,style=rounded]; A->B}`，选对引擎 `dot`(分层)/`neato`(无向)/`fdp`(大图)，`rank=same` 对齐同层。
  - **TikZ/PGFPlots**（字体与正文统一）：`\begin{axis}...\addplot table{data.dat};`，导言区 `\pgfplotsset{compat=1.18}` 统一样式，大图用 `external` 库缓存。
  - **Mermaid**（文档/初稿）：`graph TD; A[框]-->|标签|B{判断}`，`mmdc -i in.mmd -o out.svg` 导出。
  - **Draw.io**（要可编辑矢量源 + 可版本控制的系统/架构图）：`.drawio` 即 mxGraph XML，可程序化生成；有官方 jgraph/drawio-mcp（diagram-as-code，AI 可生成/改图），CLI `drawio --export --format pdf/svg` 出图。比 Graphviz 自动布局更可控、比 Mermaid 表达力强（与 m09 figure-planning 列的首选对齐；配置见 README 推荐 MCP 表）。
  - 精修拼版：Illustrator / Inkscape。
- 精细科学图/期刊曲线：
  - **Origin**：Export Graphs 按出版商精确设 Width/Height+DPI（TIFF 600dpi），可 `Export as AI` 转 Illustrator；.otp 模板固化风格。
  - **MATLAB**：`exportgraphics(ax,"f.pdf","ContentType","vector")` 出矢量、`"Resolution",600` 出位图；组图用 `tiledlayout` + `nexttile`（`TileSpacing="compact"`）。
- 示意/机制图/graphical abstract：生命科学图标库可用 **BioRender** 手工做（注意导出授权与分辨率；其官方 MCP 仅查询不能作图，故只手工用、非程序化路径）。
- 3D 结构/分子/科学可视化：**Blender**（开源，程序化建模渲染**非 AI 生图**；成熟路子用 Molecular Nodes/SciBlend 等插件，有社区/官方 MCP 但驱动科研可视化尚属探索）；3D 渲染作论文图须数据真实可复现并标渲染参数，详见 m09 figure-planning references「Blender」节。
- 组图/排版：matplotlib subplots/GridSpec、Illustrator（图层+画板对齐）、python-pptx（`add_picture(..., width=Inches(3))`，layout[6] 空白页）。
优先可复现(代码)方案，便于改数据重出；最终精修/拼大图再进 Illustrator/Inkscape。具体决策同 a09。

## 一行套刊样式与导出脚本（本技能自带资产）
- **样式**：`plt.style.use("assets/publication.mplstyle")` 是通用底；按刊叠加 `plt.style.use(["assets/publication.mplstyle","assets/nature.mplstyle"])`（或 `science.mplstyle`）。三者均为 Okabe-Ito 色盲安全色环 + 无衬线 + 矢量文字可编辑（pdf/ps fonttype42、svg 不转曲）。
- **导出**：`scripts/figure_export.py`
  - `save_publication_figure(fig, basename, formats=("pdf","png","svg"), dpi=600)` 多格式 + DPI，自动建目录、强制文字可编辑。
  - `save_for_journal(fig, basename, journal, column)` 按刊规格设物理尺寸（mm→in）再导出，返回 `(paths, info)`。
  - `check_figure_size(fig, journal=, column=)` 校验栏宽（mm）与最小字号（pt），`measured=True,path=` 还能读回落盘文件实测宽度复核 bbox tight 静默裁剪。
  - `check_scaled_fonts(fig, journal=, column=)` 校验「大尺寸画再缩小到栏宽」后的**有效字号**——**仅对"先大画布作图再缩到栏宽"工作流有意义**；若已用 `save_for_journal` 设精确栏宽(scale≈1)，它必报"无风险"，是预期空操作不是 bug，standard 流程无需再跑。
  - `check_export_compliance(path, journal, column=)` 消费此前闲置的规格字段：实测 dpi≥min_dpi、文件体积≤max_file_mb、高度≤max_height_px、格式∈preferred_formats（位图读 Pillow，矢量/无 Pillow 跳过不臆断）。
  - `save_for_journal` 导出前检字体落空：rcParams 首选 Arial/Helvetica 在 Linux/CI 不可用会静默回退 DejaVu，回退即打 WARNING 并入 info["font"]，让"字体与正文一致"可验证。
  - `JOURNAL_SPECS` 内置逐刊规格字典（含 `verified` 标记）。
- **配色**：`scripts/color_palettes.py`
  - `OKABE_ITO` / `OKABE_ITO_LIST` 8 色常量；`sequential_cmap()` / `diverging_cmap()` / `discrete_cmap()`；`apply_palette()` 设当前色环。
  - `to_grayscale()`、`simulate_cvd(kind=deuteranomaly/protanomaly/tritanomaly)`、`preview_palette()` 出原色/灰度/三种色盲对照图。有 `colorspacious` 走精确算法，缺则自动降级线性近似（`cvd_backend()` 可查）。
- **诚实性 lint**：`scripts/figure_integrity_lint.py` —— 静态扫绘图代码，提示常见误导：y 轴偷偷截断（含 `set_ylim(bottom=)` 关键字形式）、双 y 轴伪相关、bar/`sns.barplot` 无误差棒、误差棒未注明类型（`.std()` 数据计算不再被误当类型声明）、jet/rainbow 色图、3D 扭曲。`python scripts/figure_integrity_lint.py --file plot.py`（含 `--selftest`）。**对照反例教材** `examples/bad_figure_example.py`（故意违规、可端到端命中多条）。规范见 `references/figure_integrity.md`。只提示不阻断，最终判断交作者。**局限：仅覆盖 matplotlib/seaborn 静态正则，plotly/altair/ggplot2/MATLAB 链路的诚实性不被检查，那些需人工对照 figure_integrity.md。**
- **示例**（均可 `python examples/xxx.py` 跑通，Agg 存图）：
  - `example_matplotlib_multipanel.py`：GridSpec 不规则布局 + (a)(b)(c) 标号 + 误差棒 + 显著性星标。
  - `example_seaborn_stats.py`：箱线/小提琴/条形统计对比 + despine。
  - `example_framework.dot` + `example_framework_render.py`：Graphviz 框架图，有 `dot` 二进制则渲染，否则降级 matplotlib 块图。

## 逐刊硬规格表（栏宽 mm + DPI + 格式 + 字号下限）
> **栏宽数字唯一真相源 = `scripts/figure_export.py` 的 `JOURNAL_SPECS`**；下表为其人读镜像，若与脚本不一致以脚本为准（改数字只改脚本）。verified=实测：已 curl 该刊作图规格页并记 HTTP 码；其余为依公开指南整理但本次未逐项实测（多因付费墙/反爬 403），投稿前请以目标刊"最新"作者须知为准。

| 期刊 | 单栏宽 | 双栏/整版宽 | 字号下限 | 线条 DPI | 半调/照片 DPI | 首选格式 | 实测 |
|---|---|---|---|---|---|---|---|
| **Nature** | 89 mm | 183 mm | 5 pt（面板标 8pt 粗体 a,b,c；正文 ≤7pt） | 600 | 300–600 | PDF/TIFF/EPS（文字勿转曲，Helvetica/Arial） | ✅ HTTP200 |
| **PLOS** | 83 mm | 140 mm(1.5栏) / 190 mm | 8 pt（8–12pt，Arial/Times/Symbol） | 600 | 300–600 | **仅 TIFF/EPS**；789–2250px@300dpi，<10MB | ✅ HTTP200 |
| **Science (AAAS)** | 55 mm (5.5cm) | 120 mm(12cm) / 整版 183 mm(18.3cm) | 5 pt（常 6–9pt） | 600 | 300 | EPS/PDF/AI/TIFF，无衬线 | ✅ 三档制经联网多源核实(2026-06-11) |
| **Cell Press** | 85 mm | 174 mm | 5 pt | 1000（线条） | 300 | PDF/AI/EPS/TIFF | ⚠️ 页 403 未实测 |
| **IEEE** | 88.9 mm(3.5in) | 181 mm(7.16in) | 8 pt | 600 | 300 | PDF/EPS/TIFF | ⚠️ 未逐项实测 |
| **Elsevier** | 90 mm | 140 mm(1.5栏) / 190 mm | 7 pt | 1000（线条） | 300（彩/灰）、组合 500 | PDF/EPS/TIFF | ⚠️ 页 404 未实测 |
| **MDPI** | 170 mm（单列正文宽，图按此宽或整数分数） | 170 mm | 8 pt | 1000（线/组合） | 300（照片） | TIFF/PNG/EPS | ⚠️ 付费墙未实测；含 db01 的 Animals/Agronomy/Sensors/Remote Sensing |

> **custom 逃生通道**：尚未进上表的刊（如中文刊）用 `save_for_journal(fig, base, journal="custom", custom_width_mm=86.0)` 直接传物理栏宽（mm），校验同理 `check_figure_size(fig, journal="custom", custom_width_mm=86.0)`。**栏宽数据须有来源（db01 卡或实测记录），禁止臆测**。中文刊实测栏宽已落 db01 risk_note（2026-06-11，pdfplumber 实测）：农业工程学报 单栏 86 / 整页 180；中国农业科学、作物学报 单栏 81 / 整页 170；农业机械学报 待核查（PDF 入口被反爬拦截）。

数值与 `JOURNAL_SPECS` 同源，可在代码里直接读取（如 `figure_export.JOURNAL_SPECS["nature"]`）。

## 审美与规范（投稿级）
- **配色**：色盲友好——matplotlib/seaborn 用 `viridis/cividis/colorblind`，R 用 `scale_*_viridis`，连续数据避免 jet/rainbow。同一论文统一调色板（登记 db07）；**项目有 `databases/db09-projects/projects/<project_name>/palette.json` 则必用其取色**（与 PPT/前端共享的视觉 SSOT 实例，主色/强调/语义色照取，不另起一套；schema 见 db09 README），无则按 db07 卡推荐配色。不超过必要颜色数（离散 ≤8 类，超出手动指定）。
- **字体**：与正文一致(常 Times/Arial)；字号在缩放后仍可读(≥6–8pt)。seaborn 用 `context="paper"` 整体定字号；按目标栏宽设物理尺寸（单栏≈3.5in、双栏≈7.2in），避免投稿后被缩放失真。
- **线条/标记**：区分清楚，黑白打印仍可辨(线型 linestyle + 标记 marker 双重区分，不仅靠颜色)；线宽用绝对值(pt)。
- **分辨率/格式**：矢量优先(PDF/SVG/EPS)；位图线条图 ≥600dpi、含照片 ≥300dpi。**文字保持可编辑**便于二次精修：matplotlib 设 `rcParams["pdf.fonttype"]=42`；R 用 `device=cairo_pdf`；MATLAB 用 `exportgraphics ContentType=vector`。EPS 不支持透明，要透明背景用 PDF/SVG。
- **元素**：坐标轴标签+单位、图例、误差棒、显著性标记，去 chart junk（多余网格/边框，`sns.despine()` 或 `theme_classic()`）。
- **caption**：自洽，能独立读懂。

## 组图逻辑
- 同类对齐、共享坐标/色标、统一尺寸。matplotlib 用 `constrained_layout` 自动对齐共享色标；ggplot 用 `facet_*` 或 patchwork；MATLAB 用 `tiledlayout`。
- 子图编号(a)(b)(c)，标题精简。patchwork `tag_levels="a"` 可自动标号。
- 用留白和分组体现层次，突出主结果。
- 拼最终大图：各子图导出矢量(SVG/PDF) → Illustrator/Inkscape 置入 → 图层管理 + Align 对齐 + 统一字体线宽 → 加标号 → 按期刊要求导出(PDF/EPS/TIFF，印刷常 CMYK)。命令行拼/转格式可用 Inkscape 1.x `--export-type` / `--actions`。

## 投稿前自查清单
- 物理尺寸=目标栏宽？字号缩放后 ≥6–8pt？
- 颜色色盲安全？黑白打印可辨（线型+标记）？
- 矢量输出且文字可编辑（fonttype42 / svg.fonttype=none / cairo_pdf / vector）？位图 dpi 达标？
- 坐标轴有标签+单位？图例/误差棒/显著性标记齐全？去除 chart junk？
- **诚实性（不误导，审稿人必查）**：详见 `references/figure_integrity.md`，可跑 `scripts/figure_integrity_lint.py` 扫绘图代码。要点：误差棒在 caption 注明是 SD/SEM/95%CI 并写明 n=；y 轴截断必须显式标断点（不偷偷截断放大差异）；慎用双 y 轴（易制造伪相关，能拆分就拆分）；小样本优先散点/箱线展示原始分布，别用 bar 掩盖分布；坐标轴范围不为夸大效果而人为收紧/放大。
- **AI 生成图像（2026 投稿红线）**：本图是否用生成式 AI（DALL·E/Midjourney/SD/GPT Image 等）生成或篡改？数据图绝对禁止——Nature/Science/Elsevier 三家头部出版商一律禁止 AI 生成论文图像，唯一例外是「AI 本身是研究对象/方法」（须 methods 可复现披露）。论文图走自有 mplstyle 数据驱动绘制；m16 的 R6 生图流水线只服务 PPT/前端、严禁进论文图链路。政策细节与各家口径差异见 `references/figure_integrity.md`「AI 生成图像政策」节。
- 全论文调色板/字体/线宽一致（对照 db07）？

## 工作方式
按 m09 的规划卡（`light-figure-planning/templates/figure_plan_card.md`，叙事层+规格层双层字段）逐图实现：给出可运行代码或源文件 + 预览说明 + 设计理由。读卡的上层叙事确认这张图绑的 claim 与组图角色，读下层规格的 `source_card`/`target_journal`/`column` 照卡执行。需要数据时回 m06/m02 取。多次打磨直到达到顶会观感。
- **先读 source_card（必填）**：规划卡必须带 `source_card`，指向 `databases/db07-figures/resources_real.md::figure_type` 或 `databases/db07-figures/figure_advanced_cards.md::figure_type`。`figure_cards.md` 只是模板索引，不能作为实体执行来源；只有 `source_card: new_canonical_candidate -> databases/db07-figures/resources_real.md`（或 `databases/db07-figures/figure_advanced_cards.md`）才表示需新增可复用模式并回写 db07。
- **输入字段分层**：db07 基础字段控制图表模式（`figure_type/purpose/data_required/layout/...`）；项目执行字段控制交付（`figure_id/target_journal/column/caption_draft/output_formats`）。不要把单个项目的 F1/F2、caption、导出路径回写成 db07 实体卡。
- **栏宽不臆测**：直接读规划卡的 `target_journal` 与 `column` 字段，原样传给 `save_for_journal(fig, basename, journal=target_journal, column=column)`——物理栏宽 mm、figsize、最小字号全由 `JOURNAL_SPECS` 锁定。规划卡缺这两字段时回规划技能（light-figure-planning）补，不要自行猜测栏宽（猜错整张图物理尺寸作废）。`column` 取值须为该刊实有键（`single`/`double`/`full`/`onehalf`）。`JOURNAL_SPECS` 现含 `nature/science/cell/plos/ieee/elsevier/mdpi` 七键；表外刊（如中文刊）走 `journal="custom"`+`custom_width_mm=<mm>` 逃生通道，**栏宽数据须有来源（db01 卡或实测记录），禁止臆测**。
- **导出后必检**：每张图导出后运行 `check_figure_size(fig, journal=target_journal, column=column, measured=True, path=<落盘文件>)` 复核实测物理宽度，并跑 `check_export_compliance(path, journal, column)` 查 dpi/体积/格式/高度合规；`save_for_journal` 已自动检字体落空（看 info["font"]）。**`check_scaled_fonts` 只在"手动大画布作图再缩放"工作流才需要**——用 `save_for_journal` 设精确栏宽时它必报无风险，可跳过。若代码图涉及误差棒、截断轴、双 y 轴、jet/rainbow 等，再用 `scripts/figure_integrity_lint.py --file <plot.py>` 做诚实性检查。

## 产出
图文件(矢量+位图) + 生成代码/源文件 + 项目风格说明(写入仓库根目录下的 `databases/db09-projects/projects/<project_name>/version_history.md`，供 a07 统一) + **figure manifest**（落到仓库根目录下的 `projects/<project_name>/figures/manifest.md`）。只有新增了跨项目可复用的图表模式，才回写 db07 canonical 文件。
- **figure manifest**：交付 m07 的单一工件，把"图文件↔图号↔caption"绑定。逐图一项，含：`figure_id`(沿用 m09 规划卡的 F#/T# 编号，与 m07 模板 `[图位 F1]`/`[表位 T1]` 占位对齐) + `source_card` + 图片文件路径(矢量+位图) + 最终 caption + 放置章节 + target_journal/column + 导出/字号检查结果。m07 据此把占位替换为实图与图号，无需回查规划卡。
  示例：
  ```yaml
  - figure_id: F1
    source_card: databases/db07-figures/resources_real.md::模型框架图(architecture)
    files:
      vector: figs/framework.pdf
      bitmap: figs/framework.png
    caption: "图1. 方法整体框架：左输入经解耦表征模块……"
    section: 方法-框架
    target_journal: nature
    column: single
    checks:
      figure_size: pass
      scaled_fonts: pass
  ```

## 衔接
受 m09 驱动；交 m12 排版插入；风格一致性由 a07 跨图维护。
**专利附图**：受 m15(light-ip-application) 委托绘制时，按 references「专利附图规范」节执行——黑白矢量线条、图号编排、附图标记线不交叉、流程图/框图术语与权利要求一致，不套论文数据图配色。

---
各工具真实 API/参数/导出命令/已知坑的逐条笔记见 references.md。
