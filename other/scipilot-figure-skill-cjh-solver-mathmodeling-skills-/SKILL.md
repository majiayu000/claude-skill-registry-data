---
name: scipilot-figure-skill
description: >-
 SciPilot Skills 家族成员，负责科研数据可视化——但定位不是"画图工具"，
 而是"可视化顾问"。先做数据剖析（列类型/样本量/分布/异常值/分组结构/相关性），
 再结合用户的论证目标推荐图型，主动拦截科研画图的经典错误（小样本画均值柱掩盖
 分布、双 Y 轴、饼图、Y 轴不当截断、rainbow 色图、把分类点连成折线等），最后
 产出 Nature / Science / IEEE / Elsevier / PNAS / 中文核心期刊级别的成图。
 覆盖纯数据图：折线、柱状、散点、箱线 / 小提琴、热力图、误差棒、分布图（直方
 图 / KDE）、相关性矩阵 / 散点矩阵、多面板组合。技术栈 matplotlib + seaborn +
 SciencePlots（静态）+ plotly（交互）。中英文双语，中文模式自动配置 Noto Sans
 CJK / Source Han Sans / SimHei 并修复负号方框，支持中文期刊"宋体正文 +
 Times New Roman 数字"混排。默认色盲安全配色 + 冗余编码 + 灰度预览。出图后做
 "视觉自检闭环"：渲染 PNG 预览→程序自检缺字/文字裁切/刻度重叠→AI 读图复核遮盖
 与子图对齐→回改重渲，直到通过。
 当用户的任务涉及以下任何情况时主动触发：论文配图、科研画图、数据可视化、
 不知道用什么图、怎么展示数据、用什么图好、期刊投稿图、figure、出版级图表、
 matplotlib、seaborn、plotly、误差棒、显著性标注、色盲安全配色、矢量图导出、
 中文论文图表、多面板。**即使用户只是给一批数据问"这个怎么画"或"用什么图
 好"，也应使用本技能——本技能首要能力是"判断该用什么图"，其次才是绘制。**
 不做示意图、流程图、架构图。
---

# scipilot-figure-skill — 科研数据可视化顾问

> SciPilot Skills 家族成员 | 从数据剖析到出版级成图

## Contest-Orchestrator Adapter

在 `contest-orchestrator` 及其轻量、DSH、MathorCup 模式中，本技能按两个阶段运行，只负责数据结果图，不负责技术路线图、流程图、模型结构、算法过程、机制图或几何图。数据图执行 SciPilot 决策卡 → ModelViz 生成 → SciPilot 检查；所有非数据图统一路由到 `tikz-scientific-figures`。输入来自项目工作区的 `result_registry`、`numeric_source_map`、图表计划、任务卡和已批准结果。

`active_mode: full-contest-mathorcup` 时，M2 的 EDA 图读取 `data_overview.yaml`、`eda_report.md`、原始数据和当前任务卡；若图中展示冻结特征或标签关系，还需读取 `features.yaml` 与 `leakage_audit.yaml`，且不得用测试折标签决定表示方式。M4 的正式数据图读取已批准 `visual_argument_plan.yaml`、M3 `run_manifest.yaml`、`result_interpretation_cards.yaml`、`independent_validation.yaml` 及对应数据/结果文件。缺少 Harness 命名的登记文件不等于缺少证据；每个图中数字、字段、单位和图注主张仍须绑定当前项目的真实来源与哈希。M4 仅负责已批准的数据图位，不另行决定全局图表计划。

### DISCOVERY phase

MathorCup 启用 `nodes.M4.visual_workflow: writer_first_batches` 时，M4 从当前任务卡读取由 writer 在批次初稿后提出、经用户确认的批次视觉计划与初稿引用，不以前置全篇正式图或全局计划为输入条件。writer 决定需要解释的读者问题与落位，本技能负责数据剖析、具体图型和视觉编码；最终 QA 与真实来源要求照常执行。全篇计划由 writer 汇总各批已批准槽位，图表 agent 不重新决定论文需要哪些图。其他模式的计划职责不变。

- 对批准的数据执行数据剖析，核对字段、样本量、数据类型、分组结构、连续性、异常值和缺失情况。
- 先从论文上下文提取 `reader_question`、`claim` 和 `reader_takeaway`，再选择 `representation_mode`：`figure`、`table` 或 `text`。只有选择 `figure` 后才确定具体图型、视觉编码和模板；如果表格或文字已经能完整传达证据，不为满足图数生成图。
- 创建完整 `decision card`：读者问题、论证主张、数据字段与结构、表示方式及理由、推荐图型、备选图型、排除图型、信息单元、坐标单位、图注限制、前置引导语职责、后置解释语职责和论文落位。
- 只输出决策卡和数据剖析证据，不检索模板、不执行绘图。

MathorCup 或 Harness 启用 `chapter_parallel` 时，以主控对应的 `mathorcup_chapter_parallel.md` 或 `harness_chapter_parallel.md` 为时序依据：接收已批准章节绑定的提示词与视觉计划，完成本轮图表决策和 QA。提示词返修产生新版本，不撤销未变章节批准，也不阻塞后续章节；最终资产仍须绑定最新请求、来源和选定版本。此分支优先于历史批次或图件先行的描述。

### QA phase

- 接收 ModelViz 生成的 SVG、PNG、模板适配脚本和执行报告，执行 `semantic check`、`technical check` 和 `visual check`。
- 视觉检查默认开启，用于确认图片美观、整洁、可读、层级清楚和标注完整；技术检查与视觉检查分开登记。
- 检查失败时只返回明确的定向修复项，由 ModelViz 修复后重新进入 QA phase；通过后绑定 `generator=modelviz`、`semantic_qa=scipilot-figure-skill`。
- 返回 `status`、`active_mode`、`task_card`、`artifacts`、`evidence`、`checks`、`blockers`、`next_node` 节点包。缺少来源或任一检查失败时阻断论文使用。
- 图表、图注、报告不得包含元话语、内部交流、调试、失败过程、旧版本或其他负回响；本技能不改变原始数据、模型结果或论文公式。

## 概述

科研工作者最大的画图痛点往往不是"不会用 matplotlib"，而是"手上一堆数据，不知道该用什么图把结论讲清楚"。本技能的**首要能力是【思考与判断】**，其次才是【绘制】。

具体地——**永远先思考再画**：
1. 先理解数据再选图——拿到数据先做 EDA，用事实驱动图型选择
2. 先想清楚"这张图要论证什么"——同样数据，不同论点 = 不同图
3. 主动拦截科研画图的经典错误，而不是顺从
4. 维度太多就建议拆图，不硬塞

**只覆盖纯数据图**：折线、柱状、散点、箱线/小提琴、热力图、误差棒、分布图、相关性矩阵、多面板组合。**不做**示意图、流程图、架构图。

## 何时使用

- 用户给了一个 CSV / Excel / DataFrame 说"帮我画一下"或"用什么图好"
- 用户在写论文要插数据图
- 用户已有草图但说"达不到投稿要求"
- 用户提到 Nature / Science / IEEE 等具体期刊
- 用户问"中文论文 matplotlib 出方框怎么办"
- 用户提到误差棒、显著性、色盲、矢量导出、多面板

## 核心工作流（8 步）

**这是本技能与普通画图工具的根本区别——不能上来就画**。每一步缺位前一步的成果都不该执行。

### 第 0 步：理解任务

开画前**先搞清楚三件事**：

1. **读者在此处要理解什么，论文主张是什么？** 先写出一个可检验的 `reader_question` 和一个 `reader_takeaway`。同样数据，论点不同，表示方式也不同。
2. **不出图是否会损失理解？** 在 `figure`、`table` 和 `text` 中先选择最小充分表示，并写明理由；图表数量是结果，不是任务目标。
3. **数据在哪里？长什么样？** 文件路径 / 字段含义 / 多少行 / 是否已经清洗

**如果用户没说清论证目标**，主动问一句："读者看完这一处需要理解什么？" 或从论文上下文推断并明确记录假设。**不要把用户给出的图型直接当作语义决策**；先检查它是否服务于读者问题。

### 第 1 步：剖析数据

调用 `scripts/profile_data.py`：

```bash
python scripts/profile_data.py data.csv --group group --group condition
```

输出包含：每列类型、样本量、缺失率、连续列的描述统计 + 偏度 + 异常值、分组样本量分布、相关性矩阵、初步图型建议。

不会读这份报告？查 `references/data_profiling.md`。

**重点核对**：
- 列类型识别对不对？（数字 ID 被认成 ordinal 是常见误判）
- 每组 n 是多少？小样本警告？
- 是否高度偏态？是否需要对数轴？

### 第 2 步：选图

**这是顾问职责的核心**。基于第 0、1 步的事实，查 `references/chart_selection.md` 的决策框架决定图型。要点：

- 先确定 `representation_mode`，再决定图型；`table` 和 `text` 是合法且优先的结果，不得把每个视觉义务机械转成图片。
- 每张图只承担一个核心读者问题，并列出至少两个相互独立的信息单元；单一信息单元只有在 `compact` 理由成立时才允许成图。
- **给出推荐 + 简短理由 + 1-2 个备选**（不要只丢一个选择给用户）
- 如果数据维度过多（如分组组合 > 12）→ **明确建议拆图**，而不是硬塞
- 如果用户指定的图型**不适合数据**（如 n=5 要画均值柱）→ **善意指出问题并说明更好的选择**，让用户决定。详见下方"主动拦截"小节
- 如果数据特征意味着特殊处理（双峰分布、严重异常值、跨量级）→ 在选图建议里明确提及

### 第 3 步：查期刊规范

确定目标期刊后查 `references/journal_specs.md` 拿到：单/双栏宽（mm 与 inch）、字号、推荐字体、DPI、矢量格式偏好。

不知道目标期刊就问一句。"毕业论文 / 中文核心 / 英文 SCI / NeurIPS" 都对应不同规范。

### 第 4 步：配环境

```python
from setup_style import setup_style
setup_style(journal='nature', lang='en')             # 英文 Nature
setup_style(journal='general', lang='zh', serif_for_zh=True)   # 中文宋体混排
```

`SciencePlots` 装了自动用，没装回退到内置预设——不会因为缺它崩溃。

### 第 5 步：绘制

按 `references/plot_recipes.md` 对应章节的配方画。每节都有可直接复制的 Python 代码 + 常见坑。

画图时强制做到：
- `figsize=(目标宽, 目标高)` 单位英寸——直接定最终尺寸
- 用 `seaborn.color_palette('colorblind')` 或 Okabe-Ito + 冗余编码（不同线型/marker）
- 误差棒 / 阴影要在图注交代是 SD / SEM / 95% CI + n
- 流程、机制、技术路线和几何关系不通过堆放公式或原始数据来“凑信息量”；竞赛模式下这些语义统一交给 `tikz-scientific-figures`，数据图只呈现其已登记的数值证据。

### 第 6 步：自检闭环（机器检查；视觉检查按适配层选择）

**三层都要过，缺一层都可能带病投稿**：

1. **语义层**：`references/viz_pitfalls.md` 18 条科研画图禁忌——图型/配色/误差是否踩坑
2. **形式层**：`references/publication_checklist.md` 形式合规（尺寸、DPI、字号、误差交代）
3. **视觉层（绘图任务默认开启）**：执行**渲染 PNG → 程序自检 → AI 读图复核 → 回改**：
   - `visual_qa.render_preview(fig, 'figs/_preview.png')` 渲一张预览
   - `visual_qa.audit_layout(fig)` 程序抓**缺字乱码 / 文字裁切 / 刻度重叠**（确定性问题）
   - **用 `Read` 工具读这张 PNG**，对照 `references/visual_review.md` 的 8 项清单核对
     **图例压数据 / 子图标签对齐 / 配色灰度可分**（程序难判的感知问题）
   - 发现问题 → 按 `visual_review.md` 回改表改 → 重渲 → 再读，直到通过

语义层、形式层和绘图任务默认开启的视觉层不通过都必须修复；只有调用方明确关闭视觉层时登记为未请求，不得伪造通过。视觉检查完成后再导出 SVG 和 PNG。

### 第 7 步：导出

```python
from export_figure import export_figure
export_figure(
    fig, basename='figs/fig1',
    formats=['svg', 'png'],
    size_inches=(3.5, 2.625),
    dpi=300,
    grayscale_preview=True,    # 自动出灰度版供色盲检查
)
```

最后跑一遍 `scripts/check_figure.py --strict` 机器审计。

### 图表节点交接契约

针对数据结果槽位，交给 `contest-orchestrator` 的决策卡和 `figure_registry` 必须保留 `representation_mode`、选择理由、`reader_question`、`reader_takeaway`、前置引导语职责和后置解释语职责。`figure` 才能进入 ModelViz 模板检索与生成；`table` 或 `text` 直接登记为非绘图表示并由论文 agent 落位。当前模式的图表 agent 负责汇总全局 `visual_argument_plan.yaml` 并分配流程图、技术路线图和示意图路由；本技能只处理其中的数据结果槽位。数据图生成前必须能回答“图中哪些信息单元共同支撑主张”，生成图后必须能回答“读者看图后新增了什么理解”。

## 选图速查（详细决策在 chart_selection.md）

| 数据形态 | 推荐首选 | **不该用** |
|---|---|---|
| 1 个连续 看分布 | 直方图 + KDE / 箱线 | 饼图 |
| 1 个分类 看占比 | 横向柱状（按值排序） | 饼图、3D 饼 |
| 1 分类 + 1 连续，n<10/组 | **stripplot / dot plot**（直接列点） | 均值柱（**严禁**） |
| 1 分类 + 1 连续，n≥10/组 | **箱线/小提琴 + stripplot 叠加** | 仅均值柱 |
| 2 连续 看关系 | 散点 + 回归 + r 值 | 折线（除非 x 有序连续） |
| 时间 / 剂量 vs 连续 | 折线 + 误差带 | 柱状 |
| 多变量相关（>3 列）| 相关性热力图 / pairplot | 平行坐标 |
| 矩阵数据 | 热力图（viridis/RdBu_r）| 3D 表面、rainbow 色图 |
| 构成占比 | 堆叠柱 / treemap | **饼图** |

完整决策树和"同一数据不同论点 → 不同图"对照表见 `chart_selection.md`。

## 五条硬性原则

### 原则 1：按最终尺寸出图，不二次缩放

`figsize` 直接设论文里实际尺寸（Nature 单栏 3.5 in、双栏 7.2 in；IEEE 单栏 3.5 in、双栏 7.16 in）。导出后**绝不在 Word / LaTeX 里再缩放**。

**为什么**：matplotlib 字号是绝对单位（pt），Word 里缩 50% 9pt 就变 4.5pt——投稿前自检直接打回。

### 原则 2：矢量优先

折线 / 柱状 / 散点 / 热力（数据网格除外）/ 误差棒统一导出 SVG 和 PNG。SVG 用于 LaTeX 正式插入，PNG 用于预览和视觉检查。**不生成图片 PDF，也不用 JPEG、TIFF 等其他图片格式**。

**为什么**：矢量任意缩放不糊，文字仍可选；JPEG 数据图边缘有压缩 artifact，期刊 PDF 检查器直接打回。

### 原则 3：配色对色盲友好

默认 `seaborn.color_palette('colorblind')` 或 Okabe-Ito。**同一张图不同类别加冗余编码**（线型 / marker）。出图前 `export_figure(..., grayscale_preview=True)` 看灰度版能否区分。

**为什么**：约 8% 男性、0.5% 女性色觉异常。审稿人里有这群人，全靠红绿区分的图对他们传达力归零。

### 原则 4：字号在最终尺寸下可读

正文标签和刻度数字 7-9 pt，最小字 **≥ 6 pt**。

**为什么**：审稿编辑会按 mm 打印查字号；<6 pt 不可读直接退回。

### 原则 5：误差必有交代

只要有误差棒 / 阴影区间 / 箱线——**图注必须写清**：
- 误差类型（SD / SEM / 95% CI / IQR）
- 样本量 n
- 显著性检验方法 + 校正（如 Bonferroni）
- 显著性符号定义（`* p<0.05` 等）

**为什么**：SD 和 SEM 差一个 √n。混淆 = 结论反转 = 退稿。

## 主动拦截（顾问职责）

发现用户的需求会触发以下错误时，**先说明再给替代方案，不要默默照做**。完整 15 条详见 `references/viz_pitfalls.md`。

| 错误 | 后果 | 替代方案 |
|---|---|---|
| n<10/组 还想画均值柱 | 掩盖分布、掩盖 n、审稿人怀疑 | 箱线 + stripplot；或直接 stripplot |
| 双 Y 轴显示无关变量 | 视觉上的相关 / 分歧是作图者捏造的 | 拆成上下子图共享 x；或标准化共轴 |
| 用饼图展示占比 | 人眼判角度差长度 3 倍 | 横向柱状（按值排序） |
| 3D 柱 / 3D 饼 | 视角扭曲所有数值 | 2D 柱、热力图 |
| 比例图 Y 轴不从 0 起 | 误导小差异看起来很大 | 从 0 起或用 log；或加明显断裂标记 |
| 颜色映射连续值无 colorbar | 读者不知道深浅对应数值 | 必加 colorbar + 标 label/单位 |
| x 是分类却用折线连均值 | 暗示不存在的连续关系 | 散点 / 点图 / 柱状 |
| 一图塞 5 个论点 | 没论点 | 拆图，一张图一个核心结论 |
| rainbow / jet 色图 | 感知不均匀、造假峰 | viridis / magma / RdBu_r |

**拦截话术示例**：

> 你要的"3 组各 5 个样本的均值柱状图"会触发 P1（均值柱掩盖分布）：n=5 太小，柱状会让审稿人怀疑你藏了什么。我建议改成**箱线 + stripplot 叠加每个点**，5 个点直接可见、分布形态一目了然。要按原方案画吗？

尊重用户最终决定，但**留下明确的劝阻记录**。

## 中文支持

中文 matplotlib 出方框的根本原因：默认字体（DejaVu Sans 等）不含 CJK 字符表。`setup_style(lang='zh')` 自动做两件事：

1. 按优先级查中文字体：`Noto Sans CJK SC` > `Source Han Sans SC` > `SimHei` > `Microsoft YaHei`
2. 修负号方框：`plt.rcParams['axes.unicode_minus'] = False`

找不到任何 CJK 字体会抛清晰的安装提示（不会让你画完发现是方框）。

**中文期刊的"宋体 + 数字 Times New Roman"混排**：传 `serif_for_zh=True`，优先选 Noto Serif CJK / Source Han Serif / SimSun。

详见 `references/journal_specs.md` 末尾的字体安装小节。

## 脚本说明

| 脚本 | 干啥 | 主入口 |
|---|---|---|
| `profile_data.py` | EDA：列类型 / 样本量 / 分布 / 异常 / 相关 / 初步图型建议 | `profile_data(source, group_cols)` |
| `setup_style.py` | 期刊预设 + CJK 字体配置 + SciencePlots 包装 | `setup_style(journal, lang, use_sciplots, serif_for_zh)` |
| `export_figure.py` | SVG/PNG 导出 + 按最终尺寸 + 灰度预览 | `export_figure(fig, basename, formats, dpi, size_inches, grayscale_preview)` |
| `check_figure.py` | 文件合规自检（格式 / DPI / 字体嵌入） | `check_figure(path, min_dpi, target_inches)` |
| `layout_tools.py` | 子图标签对齐 + constrained/tight 兜底理版 | `add_panel_labels(fig, style)` / `finalize_figure(fig)` |
| `visual_qa.py` | 渲染 PNG 预览 + 程序自检（缺字 / 裁切 / 刻度重叠） | `render_preview(fig, out)` / `audit_layout(fig)` |

## 参考文档

`references/` 下七份文档——**按需 view，不要一次全读**：

| 文档 | 何时读 |
|---|---|
| `chart_selection.md` | **每次选图必读**——决策框架、不同论点→不同图 |
| `data_profiling.md` | 读不懂 `profile_data.py` 输出 |
| `viz_pitfalls.md` | 自检前必读——18 条避坑清单（含 P16-18 排版/渲染坑） |
| `journal_specs.md` | 不确定目标期刊的栏宽/字号/DPI/字体 |
| `plot_recipes.md` | 9 类图各自的完整配方 + 适用场景 |
| `publication_checklist.md` | 投稿前最后过形式合规清单 |
| `visual_review.md` | 出图后视觉自检——AI 读图 8 项清单 + 回改循环协议 |

每份开头都有目录——先查目录定位，再 view 对应小节。

## 常见任务示例

### 任务 A：用户只丢一个 CSV 说"帮我把这个画成论文图"

**思考-绘制工作流的范例**：

1. **第 0 步**：问用户"你这份数据主要想说服读者相信什么？"——是组间差异？时间趋势？变量关系？
2. **第 1 步**：跑 `python scripts/profile_data.py data.csv` 得到剖析报告
3. **第 2 步**：读报告里"列类型 + 样本量 + 分组结构"，结合用户的论证目标查 `chart_selection.md` 决策。**主动给出推荐 + 理由 + 1-2 备选**
4. **拿到用户确认后**进入第 3-7 步：查期刊规范、配环境、画、自检、导出

不要跳过任何一步。

### 任务 B：用户说"我想用柱状图展示三组各 5 个样本的均值"

**主动拦截的范例**：

```
你要的"三组各 5 个样本均值柱状图"会触发科研画图的经典 P1 错误
（参见 viz_pitfalls.md）——n=5 太小，柱状图的高度 + 一根误差棒无法
告诉读者数据真实分布。审稿人看到很可能要求"show individual data points"。

我建议改成 **箱线图 + stripplot 叠加每个点**：5 个点直接可见，
不掩盖任何信息，反而更可信。代码也只多一行。

要按原方案画，还是改成箱线+stripplot？
```

如果用户坚持要柱状，那也照做——但**至少**强制叠加 stripplot 显示每个点。

### 任务 C：多面板组合图

用户："给我画一个 Figure 1：4 个 panel，分别是 PCA、loss 曲线、混淆矩阵、生存曲线。"

流程：
1. 确认目标期刊（决定整张图 7.2 in 还是 7.16 in；Nature `a/b/c` vs IEEE `(a)(b)(c)`）
2. 各 panel 独立画，**保证字号、配色、坐标尺度统一**（同一变量在 4 个 panel 里同色）
3. 用 `plt.subplots(2, 2, figsize=(7.2, 5.4))` 组合（`setup_style` 已默认开 constrained_layout）
4. `layout_tools.finalize_figure(fig)` 理顺版面，再 `add_panel_labels(fig, style='nature')` 打 a/b/c/d——**统一 figure 坐标自动横竖对齐**，不要手摆 `ax.text`（易错位，见 viz_pitfalls P18；IEEE 用 `style='ieee'` → (a)(b)(c)）
5. **视觉自检闭环（绘图任务默认开启）**：`render_preview` 渲 PNG → `audit_layout` 程序自检 → `Read` 读图核对子图对齐/遮盖 → 回改 → 通过后再导出 + 灰度检查；只有调用方明确关闭时才跳过并登记状态。

详细配方见 `plot_recipes.md` 第 9 节。

### 任务 D：带显著性标注的统计图

用户："3 组数据，箱线图加显著性标注。"

流程：
1. profile 确认 n（n<10 → 必须叠 stripplot）
2. 跑统计检验（**用户必须告知**用了什么检验，是否多重比较校正）
3. 画箱线 + stripplot
4. 用 `matplotlib.lines.Line2D` 或 `statannotations` 在组之间画显著性桥
5. **图注必须写**：误差类型 / n / 检验方法 / 校正 / 符号含义

配方见 `plot_recipes.md` 第 4 节。

## 依赖

```
matplotlib>=3.7
seaborn>=0.13
plotly>=5.18
pandas>=2.0
numpy>=1.24
scipy>=1.10            # profile_data 的偏度计算用到
Pillow>=10.0           # check_figure / grayscale preview
SciencePlots>=2.1      # 可选；装了样式更接近期刊
kaleido>=0.2.1         # 可选；plotly 导出 SVG/PNG
```

可选依赖缺失时本技能仍能跑——会优雅降级并提示。
