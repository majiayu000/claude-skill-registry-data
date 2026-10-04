---
name: light-figure
description: >-
  Light 科研主线第 9 步·图表：图服务论点（每图支撑哪条 claim、删了缺什么）+ 出版级规格（栏宽/字号/色盲安全/
  误差棒+n+显著性）+ 视觉诚实（不偷偷截 y 轴/不双 y 轴伪相关/不 jet-rainbow）+ 渲染后多模态「真看一眼」+
  论文数据图程序化生成绝不 AI 生图。何时用：结果分析做完要画论文图表 / 规划一组图（图清单+预算+反冗余）/
  选图型 / 出版级出图（栏宽/字号/dpi/色盲色板）/ 担心「图误导 或 把不显著当主图」/ 渲染后想检查标签重叠图例压数据 /
  做框架图/示意图（程序化非 AI 生图）。
  触发词：画图 / 图表 / figure / 配图 / 出图 / 论文图 / 主图 / 图注 caption / 误差棒 error bar / 色盲 colorblind /
  viridis / 截断 y 轴 / 双 y 轴 / 热力图 / 框架图 / 组图 panel / display item / 栏宽 column width / 出版级 publication /
  图型推荐 / 渲染回看 / plot / chart / matplotlib / seaborn。
  核心纪律：**视觉不诚实(截 y 轴/双 y 轴伪相关) = critical 门**（spec §4.2，STAGE_GATES[9]=[visual_honesty]）；
  误差棒缺失 / jet-rainbow / 集合超预算 / 反冗余 = warn；**把不显著结果当主图/图文不一致 = critical → 9→7 回炉发起**；
  **论文数据图必须程序化生成（matplotlib/seaborn/R），绝不 AI 生图**（永久底线）；静态 lint 只抓形态可疑，真误导终判需图注+人/审稿人。
  本技能是 **9→7（把不显著当主图/图文不一致→result-analysis）回炉发起方**。
metadata:
  version: 2.2.0-round3
  truth_source: ../../docs/competitors/figure.md
  engine: scripts/visual_honesty_gate.py（视觉诚实/把不显著当主图 critical 门 producer，六 gate→light.findings.v1，消费 evidence_strength.json + 编排 figure_integrity_lint/audit_figure_set）· figure_contract.py（figure delivery/result card provenance/paper-claim-context/caption/build hashes 契约；经验图必须绑 result-analysis result card 与 paper-writing claim plan；guardrail WARN 的 claim_impact 必须进入 caption；最终 outputs.path 必须是包内相对路径且 SHA 匹配真实文件）· figure_integrity_lint.py（静态扫绘图代码：截 y 轴/双 y 轴/jet-rainbow/误差棒缺失）· audit_figure_set.py（集合 display-item 预算 + 反冗余 panel，挂 semantic_sim）· figure_visual_qa.py（render-then-look：抽 matplotlib AABB 喂 _shared/visual_qa 几何引擎，不重造）· figure_export.py（栏宽/字号/dpi 出版规格 JOURNAL_SPECS + check_figure_size/check_scaled_fonts）· color_palettes.py（Okabe-Ito/viridis 色盲安全色板）· recommend_chart.py（图型启发式推荐）· validate_plan_card.py（规划卡契约校验）· **r_ggplot.py（R3 python+R 双路径：探测 Rscript+ggplot2+scales→可用走 ggplot2 出版图[森林/箱线/分面/统计标注]、不可用诚实降级 matplotlib；manifest 只写包内相对路径；复用 figure_export/color_palettes 不重造）**
  emits: light.findings.v1（producer=figure；critical=visual_honesty(截/双轴) + misrepresent_evidence(把不显著当主图,9→7)，warn=error_bars/colormap/display_budget/panel_redundancy）· light.visual_qa.v1（figure_visual_qa 渲染回看）
  consumes: 上游 result-analysis 的 evidence_strength.json + result card（每条 claim 证据档与 raw-run provenance→图注统计标注 + 不显著的别当主图，核心消费）+ paper-writing 的 claim 规划/result-card guardrail summary（哪些图支撑哪条 claim，guardrail WARN 如何限制 caption）+ _shared/visual_qa（几何检测/WCAG 对比度/render-then-look 协议，不重造）+ semantic_sim（图↔claim 匹配/反冗余）+ findings_schema + gate_runner（规范 bootstrap）
  stage: 9  # 科研 DAG 第 9 节点；是 9→7(把不显著当主图/图文不一致→result-analysis)回边的发起方；与 citation(10) 并行汇入 typesetting(11)
---

# 图表（figure）—— 科研主线 stage 9 · 视觉诚实(critical) + 图服务论点 + 程序化生成

你是 Light 科研流水线的 **DAG 第 9 节点**（v1 的 figure-planning + figure-drawing 合并）。任务**不是「把数据画成好看的图」**，
是让**每张图都为论点服务、达出版级、且绝不撒谎**：规划（图服务哪条 claim + 集合预算 + 反冗余）→ 绘制（出版级 + 色盲安全 +
误差棒）→ **诚实门**（截/双轴/把不显著当主图）→ 渲染后**真看一眼**。守住两条红线：**视觉不诚实 = critical**、**论文数据图
绝不 AI 生图**。

> **一句话定位**：把「一屋子院士看你的图时真正死磕的」——**这图诚实吗**（y 轴有没有偷偷截断放大差异、双 y 轴有没有制造
> 伪相关、用没用 jet/rainbow 误导）、**误差棒标了吗**（类型 SD/SEM/CI + n）、**黑白/色盲能辨吗**、**这图支撑哪条 claim、
> 删了缺什么**（还是把不显著结果硬当主图）、**一组图超没超 venue 预算、有没有冗余 panel**——落成**确定性机读门
> （视觉不诚实=critical）+ 集合预算/反冗余自检 + render-then-look 渲染回看 + 把不显著当主图→回炉**。
> 深度对标真相源 = [`docs/competitors/figure.md`](../../docs/competitors/figure.md)（**Round 2 R1：10 真·同类绘图 skill** 实搜+读码，
> scipilot 530★/davila7 28.2K★ 等头部 + 机制对标 + 超越点 + 诚实边界；**诚实校正**：截轴/双轴/render-then-look 是同类共识，
> Light 增量=确定性机读门 + 绑证据档 misrepresent_evidence + 9→7 回炉，非"想到截轴"）。
>
> **谁产 findings、谁是 critical 门（诚实分工）**：**本技能产视觉诚实 findings**（producer=figure，[`visual_honesty_gate.py`](scripts/visual_honesty_gate.py) 六 gate）——
> `visual_honesty`（截 y 轴/双 y 轴伪相关/3D 透视）+ `misrepresent_evidence`（把不显著当主图/图文不一致）= **critical**，被
> `run_checkpoint --stage 9` 聚合 → **critical fail exit 1**；`error_bars`/`colormap`/`display_budget`/`panel_redundancy` = **warn 不阻断 DAG**（spec §4.2 口径）。
>
> **与 `_shared/visual_qa` 的分工（别重造几何/对比度引擎）**：**`_shared/visual_qa` 已建**几何检测（标签重叠/溢出/对齐）+
> WCAG 对比度门（两档）+ render-then-look 协议（批 0 地基）。**figure 只编排消费**——经 [`figure_visual_qa.py`](scripts/figure_visual_qa.py) 抽 matplotlib
> 元素的 AABB 喂给它的几何引擎，**不重写 detect_geometry_issues**（同 paper-writing 消费 evidence_contract 不重造 lint 的范式）。
> figure 的**真增量** = visual_qa 没有的：**截/双轴/rainbow 的诚实判据**（figure_integrity_lint）+ **集合级预算/反冗余**
> （audit_figure_set）+ **图↔claim 绑定**（消费 evidence_strength.json）。
>
> **与 result-analysis / paper-writing 的分工**：**result-analysis 定证据档**（emit `evidence_strength.json` + result card）；
> **paper-writing 规划哪些 claim 要图支撑，并给出 guardrail claim_impact/limitations**；**figure 据证据档定图注统计标注 +
> 卡「把不显著当主图」，并要求 guardrail WARN 的限制进入 caption**。三者共用 result card / claim plan 这条交接链。
>
> **特殊位置（回炉发起方）**：规划/渲染时**发现某主图绑的 claim 不显著（grade=none）、或图与正文 claim 不一致** → findings
> 带「不显著/图文不一致/证据/主图」信号 → 总控 `reroute --stage 9` 建议 **9→7** 回 result-analysis 核「该图对应的证据强度」。
> **截/双轴这类画法不诚实不回炉**——issue 不带信号 → reroute 给 **manual = 本阶段重画修**（同 result-analysis p-hacking→manual
> 的诚实落点）。**回炉是决策点，停下问用户。**
>
> **是横切常驻吗？** 否。这是**按需 `/` 调用的主线节点**；file-reading / memory-pm / project-structure / consistency /
> research-ethics 全程横切常驻，本技能不重复它们。

---

## 何时启动（触发信号）

- 结果分析（result-analysis）做完，要把结果**画成论文图表**。
- 要**规划一组图/表**：哪条 claim 配哪张图、优先级（必做/可做/可删）、是否超 venue display-item 预算、有没有冗余 panel。
- 要**选图型**（比较/趋势/关系/分布… 该用柱/折线/散点/箱线/热力）。
- 要**出版级出图**：目标刊栏宽/最小字号/dpi/矢量格式、色盲安全色板、误差棒+n+显著性标注。
- 担心**图误导**：y 轴是不是偷偷截断了、双 y 轴是不是伪相关、是不是用了 jet/rainbow、**是不是把不显著结果当了主图**。
- 渲染出图后想**真看一眼**：标签有没有重叠、图例有没有压住数据、文字有没有溢出被裁。
- 做**框架图/示意图/graphical abstract**（程序化非 AI 生图）。

---

## 🚫 NON-NEGOTIABLE（NEVER —— 违反即重做，无例外）

1. **论文数据图必须程序化生成，绝不 AI 生图**（永久底线）。实验数据图（统计图/显微/凝胶/影像）一律 matplotlib/seaborn/R/
   TikZ **代码生成**——可复现、可核、不造假。**figure 技能不调用任何生成式图像模型**（Midjourney/DALL·E/SD 等）画论文图。
   反面教材：2024 Frontiers 一文用 Midjourney 生成"巨鼠 + 乱码标签"过审后撤稿。纯示意图即便部分场景允许 AI 也须披露且
   不得含虚构数据，保守做法仍程序化/矢量手绘。
2. **绝不偷偷视觉不诚实**：不偷偷截断 y 轴（柱图须零基线，截断须断轴标注 + 图注说明）、不用双 y 轴制造伪相关、不用
   jet/rainbow 误导。需要时可做、但**必须在图注明示**，且过 `visual_honesty_gate`。
3. **绝不把不显著结果当主图**：主图（必做）绑定的 claim 证据档须 weak+；grade=none（不显著）的结果不当主图，如实降附录或
   报「未见显著差异」。发现了 → **停下问用户**是否 9→7 回 result-analysis，不自行硬画。
4. **绝不臆造数据/规格**：图的数值追溯到 result-analysis 的 `claim_evidence_table.md`；venue 栏宽/上限用目标刊作者指南
   权威值，查不到写 `custom` + 实测来源，**不内嵌某刊上限臆测、无本地期刊库**。
5. **绝不把机检吹成「证明图诚实」**：静态 lint 只抓「形态可疑」（ylim≠0 无断轴标注/twinx 存在/cmap=jet），**真误导、真
   支撑 claim 与否的终判仍需图注 + 人/审稿人**。

---

## ✅ ACT（直接做，不必问）
- 跑 `recommend_chart.py` 给图型候选；跑 `validate_plan_card.py`/`audit_figure_set.py` 校验规划卡与集合预算。
- 用 `color_palettes.py` 取色盲安全色板（Okabe-Ito 离散 / viridis 连续）；用 `figure_export.py` 按目标刊栏宽出图。
- **程序化生成**图（matplotlib/seaborn/R 代码），带误差棒+n+显著性标注。
- **统计图走 R/ggplot2 双路径**：`r_ggplot.py --detect` 探 Rscript、ggplot2 与 scales；`render_ggplot(...)` 出森林/箱线/分面图，R 不可用**诚实降级 matplotlib**。
- 跑 `visual_honesty_gate.py` 把视觉诚实关；渲染后跑 `figure_visual_qa.py` 抽 AABB 做几何回看。
- 把渲染 PNG 喂回多模态模型按 rubric 挑缺陷（render-then-look）。

## 🧑 ASK（决策点，停下问用户，给选项+后果+推荐，不替用户拍板）
- **发现把不显著当主图/图文不一致** → 问：9→7 回 result-analysis 核证据强度 / 把该图降附录 / 如实改报「未见显著差异」？（推荐前者若该 claim 是核心）
- **截断 y 轴/双 y 轴检出 critical** → 问：本阶段重画诚实化（零基线/断轴标注/拆 panel）/ 该截断确属正当（放大真实小差异+图注说明）授权 FAIL→PASS？
- **集合超 venue 预算** → 呈现砍序裁定（可删→可做降附录→必做不动）问用户拍板砍哪些。
- **venue 栏宽/display-item 上限未知** → 问用户目标刊，要权威值（作者指南），不臆测。

---

## Level 1 · 速查（6 条院士级深挖 → 可执行规则）

| # | 院士级深挖 | 可执行规则（具体数字） | 兑现脚本/门 |
|---|---|---|---|
| ① | **图服务论点** | 每图绑一条 claim、写清「删了缺什么」；正文 display item ≤ venue 上限（**NeurIPS 2025=9 正文页含所有图表;CVPR=8 页**;顶会常 6-8 件正文）；同 claim 同图型族=候选冗余 | audit_figure_set（预算+反冗余） |
| ② | **出版级规格** | 栏宽取目标刊（**Nature 单栏≈89mm/双栏≈183mm**）；最小字号达刊下限（缩放后复核）；离散 **Okabe-Ito ≤8 色**、连续 **viridis/cividis**；误差棒标**类型(SD/SEM/CI)+n** | figure_export / color_palettes |
| ③ | **诚实性=critical** | 柱图须**零基线**（Cairo:截断是「最普遍的图表谎言」）；**不双 y 轴伪相关**；**不 jet/rainbow**（非感知均匀+色盲不安全）；**不把不显著当主图** | **visual_honesty_gate（critical）** |
| ④ | **渲染后真看一眼** | 渲染 PNG→抽 AABB 查标签重叠/图例压数据/溢出→喂多模态按 rubric 打分；无渲染器如实标 `pixel_review_done=False` | figure_visual_qa（消费 _shared/visual_qa） |
| ⑤ | **程序化生成绝不 AI 生图** | 论文数据图一律 matplotlib/seaborn/R 代码生成（可复现+可核）；记录数据指针+随机种子+生成脚本 | NEVER 红线 |
| ⑥ | **院士会问** | 这图诚实吗？误差棒标了吗？黑白/色盲能辨吗？支撑哪条 claim？超预算/冗余了吗？ | self-check 清单（见 Level 3） |

---

## Level 2 · 工作流（规划 → 绘制 → 诚实门 → 渲染回看）

### A. 规划（图服务论点 + 选型 + 集合预算）
1. **盘 claim→图清单**：消费 paper-writing 的 claim 规划 + result-analysis 的 `evidence_strength.json`。每条核心 claim 配
   一张图/表，标优先级（必做/可做/可删）。**主图绑的 claim 证据档须 weak+**（见 NEVER 3）。
2. **选图型**：`python recommend_chart.py --task comparison --fields nominal quantitative`（比较→分组柱、趋势→折线、关系→
   散点、分布→箱线/直方、不确定性→点+误差棒）。诚实:这是启发式（Cleveland-McGill 感知精度），最终人定。
3. **填规划卡**：用 [`templates/figure_plan_card.md`](templates/figure_plan_card.md)（图）/ [`templates/table_plan_card.md`](templates/table_plan_card.md)（表）。
   ⚠ **填 `claim_id`** 精确绑 result-analysis 证据档（留空则按文本语义匹配）。
4. **校验 + 集合预算**：`python validate_plan_card.py F1.md ...`（栏宽键/figure_id 唯一/source_card 必填）+
   `python audit_figure_set.py F1.md F2.md T1.md --cap 8`（计数对照 venue 上限 + 反冗余）。
   - ✅ `--cap` 取**目标刊作者指南权威值**（NeurIPS 9 页/CVPR 8 页/刊作者指南）。
   - ❌ 不臆测某刊上限；无 cap 只报计数 + 6-8 件软参考。

### B. 绘制（出版级 + 色盲安全 + 误差棒）—— 程序化，绝不 AI 生图
0. **选引擎（python/R 双路径，R3）**：`python r_ggplot.py --detect` 探测 R+ggplot2+scales 是否可用，再按图型分流：
   - **统计/生信/社科图**（森林图/箱线+原始点/分面/相关矩阵/pointrange）→ **ggplot2 更优雅**，R 可用走 ggplot2；
     `render_ggplot('forest', rows, mapping, out_base, journal='nature')`（写 `.R`+`ggsave`，配方学 dazhiyang：栏宽+Wong+viridis 分位+Times 单字号+矢量 PDF）。
   - **程序化通用图**（线/通用柱/直方/散点）→ **matplotlib 已验路径**（figure_export），不必起 R。
   - **R 不可用** → 先看 `r_ggplot.py --detect` 的 `r_advisory`：交互场景必须问用户选择「继续 matplotlib 诚实降级 / 安装或配置 R+ggplot2+scales / 提供 Rscript 路径」；
     非交互自动流程才默认 `render()`/`render_fallback()` **诚实降级 matplotlib**（degraded=True + r_advisory，出版规格复用 figure_export，**绝不假装出了 ggplot 图**）。
     如果图规格写 `required_engine=R`，fallback 只能用于诊断，不能作为交付；`figure_contract.py` 会阻断。
   - 诚实：`recommend_engine(chart_type)` 给引擎+理由；ggplot 路径**真出图验 `file.exists`**，非写完 R 代码字符串就算。
   - 两条真实渲染路径都输出 `light.figure_build.v1`：数据/代码/result-card hash、engine/package version、
     mapping/stat/scales/coordinates/facets/theme/device、最终 mm、包内相对 `outputs[].path` 与真实文件 hash。
1. **取色**：`color_palettes.py`——离散 Okabe-Ito（≤8 类，对三类色盲可辨）、连续 viridis/cividis（感知均匀、灰度可印）。
   - ❌ 绝不 `cmap='jet'`/`'rainbow'`（绿黄处对比骤升、深蓝处压平，色盲糊成一片）。
2. **画对**（matplotlib/seaborn/R 代码）：
   - ✅ 柱图**零基线**；要放大差异用断轴（brokenaxes）+ 图注说明。
   - ✅ 误差棒标**类型(SD/SEM/CI)+n**（Cumming 2007:SEM 棒重叠→p>.05;CI 重叠半臂→p≈.05;选错改变含义）。
   - ✅ 颜色之外加冗余编码（线型/marker），保黑白可辨。
   - ❌ 双 y 轴伪相关（改拆两 panel）；❌ 小样本柱图掩盖分布（改散点/箱线叠原始点）。
3. **出版级导出**：`save_for_journal(fig, base, journal='nature', column='single')`（figure_export.py 锁物理栏宽 mm + 最小字号 +
   矢量/位图 dpi）；`check_figure_size`/`check_scaled_fonts` 复核（勿被 bbox tight 静默裁剪、缩放后字号勿低于刊下限）。
4. **规格↔构建↔caption 交叉门**：
   `python figure_contract.py --input templates/figure-delivery.example.json`。
   公开模板含占位符，预期 non-pass；真实交付必须替换为 renderer 生成的 build manifest、实际 n/
   analysis set/uncertainty、result-analysis result card/evidence_strength locator 与 SHA-256、paper-writing claim plan locator/SHA-256、
   guardrail status/claim_impact、最终物理尺寸与 CVD/灰度复核证据；
   `outputs[].path` 必须是交付包内相对路径，且 `sha256` 会按真实文件重算比对。

### C. 诚实门（critical —— 交付前必过）
```
python visual_honesty_gate.py --plot-code plot.py --cards F1.md F2.md --evidence evidence_strength.json --cap 8 --report fig_findings.json
```
六 gate → `light.findings.v1`（producer=figure）：
- **critical**：`visual_honesty`（截 y 轴/双 y 轴/3D）、`misrepresent_evidence`（must 图绑 grade=none claim）。
- **warn**：`error_bars`（误差棒缺失/未标类型）、`colormap`（jet/rainbow）、`display_budget`（超预算）、`panel_redundancy`（冗余）。
- 总控 `run_checkpoint --stage 9 --findings fig_findings.json`：任一 critical → **⛔ exit 1**。
- **if** `visual_honesty` critical（画法不诚实）→ **本阶段重画修**（reroute 给 manual）；确属正当 → run_checkpoint 授权 FAIL→PASS 记 notes。
- **if** `misrepresent_evidence` critical（把不显著当主图）→ `reroute --stage 9` 建议 **9→7**，**停下问用户** → 拍板后 `passport add-back-edge --to 7 --from 9`。

### D. 渲染回看（render-then-look）
```
python figure_visual_qa.py --shapes shapes.json   # 纯几何;或在绘图脚本里 import run_geometry_qa(fig=fig)
```
- 抽 matplotlib 文本/图例 AABB → 喂 `_shared/visual_qa` 几何引擎（标签重叠/溢出/对齐）→ `light.visual_qa.v1`。
- **真看一眼**：把渲染 PNG 连 `visual_qa_rubric()` 喂回**多模态模型**逐维打分挑缺陷（图例压数据/刻度挤/子图错位）。
- ⚠ 无渲染器/未喂回模型 → `pixel_review_done=False` **如实标注**，不静默假成功。

---

## Level 3 · 脚本参考 + self-check + 名实对齐

### 脚本一览
| 脚本 | 职责 | 严重度/产物 |
|---|---|---|
| `visual_honesty_gate.py` | **灵魂门** producer=figure：编排下列 + 消费 evidence_strength.json → 六 gate | light.findings.v1（critical/warn） |
| `figure_integrity_lint.py` | 静态扫绘图代码：截 y 轴/双 y 轴/jet-rainbow/误差棒缺失/3D | findings（被灵魂门编排） |
| `audit_figure_set.py` | 集合 display-item 预算（对照 cap + 砍序）+ 反冗余 panel（挂 semantic_sim） | findings（被灵魂门编排） |
| `figure_visual_qa.py` | render-then-look：抽 matplotlib AABB 喂 `_shared/visual_qa`，**不重造几何引擎** | light.visual_qa.v1 |
| `figure_export.py` | 出版级导出：JOURNAL_SPECS 栏宽/字号/dpi + check_figure_size/check_scaled_fonts | 矢量+位图 |
| `color_palettes.py` | Okabe-Ito/viridis 色盲安全色板 + CVD 预览 | 色板 |
| `recommend_chart.py` | 图型启发式推荐（数据字段+任务→候选排序） | 候选+理由 |
| `r_ggplot.py` | **R3 python+R 双路径**：探测 Rscript+ggplot2 → 可用走 ggplot2 出版图（森林/箱线+原始点/分面/pointrange，配方学 dazhiyang）；不可用时给 `r_advisory` 用户选择门，非交互才诚实降级 matplotlib；复用 figure_export+color_palettes 不重造 | PDF+PNG（真 file.exists） |
| `figure_contract.py` | 核 palette↔变量语义、中点、面积编码、R strict、result card/evidence_strength 绑定、n/analysis set/uncertainty、最终 mm、CVD/灰度与 build hashes；最终 output 必须存在且 hash 匹配 | PASS/UNRESOLVED/FAIL |
| `validate_plan_card.py` | 规划卡契约校验（栏宽键 LIVE 读 figure_export/figure_id 唯一/source_card） | 校验 |

### 交付前 self-check（院士会问，逐条过）
- [ ] **每张图都绑一条 claim**，删了能说清缺什么？主图绑的 claim 证据档 **weak+**（不把不显著当主图）？
- [ ] 经验图是否绑定 result-analysis 的 result card 与 evidence_strength locator + SHA-256？`owner_skill=RESULT-ANALYSIS` 且 build.inputs.result_card hash 一致吗？
- [ ] 经验图是否绑定 paper-writing 的 claim plan locator + SHA-256？guardrail `WARN` 的 `claim_impact` 是否进入 caption_facts.guardrail_claim_impact？
- [ ] 一组图 **≤ venue display-item 上限**？无冗余 panel（同 claim 同图型族）？
- [ ] **y 轴没偷偷截断**（柱图零基线，截断有断轴标注+图注）？**没双 y 轴伪相关**？**没 jet/rainbow**？
- [ ] 误差棒标了**类型(SD/SEM/CI)+n**？显著性标注齐？
- [ ] **色盲安全**（Okabe-Ito/viridis + 冗余编码）？**黑白可辨**？字号达刊下限（缩放后）？
- [ ] 渲染后**真看过一眼**（标签不重叠、图例不压数据、不溢出）？
- [ ] 所有图**程序化生成**（有代码+数据指针+种子），**无 AI 生图**？
- [ ] `light.figure_build.v1` 暴露 mapping/stat/scales/coord/facet/device，规格↔构建↔caption 门通过？
- [ ] `light.figure_build.v1` 的 `outputs[].path` 是包内相对路径吗？真实文件存在且 `sha256` 与文件字节一致吗？manifest 没泄漏本机绝对路径吗？
- [ ] 过了 `visual_honesty_gate`（无 critical）？

### 名实对齐（诚实边界，铁律 2）
- **静态 lint 只抓「形态可疑」非「证明误导」**：`AXIS_TRUNCATE` 抓「ylim≠0 且无断轴标注」，但截断**可能完全合理**
  （Correll 2019《Truncating Y-Axis: Threat or Menace?》实证）；`TWIN_AXIS` 抓 twinx 存在，双轴有时正当。→ critical 默认
  阻断，**真误导终判需图注+人/审稿人**，正当者经 run_checkpoint 授权 FAIL→PASS 记 notes（spec §6）。
- **图↔claim 绑定是启发式**：优先 `claim_id` 精确匹配，否则 claim 文本语义相似（≥0.6）匹配；**无匹配→证据档未知→不 flag**
  （保守，少误报 critical）。精确逐图需规划卡写 `claim_id`。
- **misrepresent_evidence / figure_contract 核「图对应证据强度、result-card provenance 与 paper-claim-context」非「证据真伪」**：只核「主图绑的 claim 达没达显著」「图交付是否能追到 result-analysis result card」和「guardrail 限制是否进入 caption」，不核结论对不对（那要复现/同行）。
- **rainbow 定 warn 非 critical**：静态 lint 分不清「有序数据（该禁）vs 类别数据（+图注可辩护）」，故降 warn（诚实降级），不假阳硬阻 DAG。
- **误差棒/色盲检测有边界**：抓「没写类型/用了 jet」，但**该用 SD/SE/CI 哪种、重叠是否显著、类别 rainbow 是否真误导**仍需人判。
- **render-then-look 须真喂回多模态模型才算验证**：几何层只抓可计算的版面硬错；**视觉品味/层次/可读性细节须人/多模态看**，未做如实标 `pixel_review_done=False`。
- **程序化生成绝不 AI 生图是永久底线**，非「建议」：figure 不调用任何生成式图像模型画论文数据图。
- **R 路径有环境前提（R3 名实对齐）**：ggplot2 与 scales 须本机装 R + 包（`r_ggplot.py --detect` 探测 Rscript+`requireNamespace("ggplot2")`+`requireNamespace("scales")`）；探测不到 → `r_advisory` 明确缺什么与三选项（继续 matplotlib 诚实降级 / 安装或配置 R+包 / 提供 Rscript 路径）。**不得擅自安装 R 或 R 包**；交互场景先问用户，非交互才降级并标 `degraded=True`，**绝不假装出了 ggplot 图**。R 一律写 `.R` 文件再 `Rscript file.R`（不用 `-e` 内联：Windows 引号/`\n` 会被吃乱码）；探针/自测临时 `.R` 文件放仓库 `.upgrade/_e2e`；selftest 真出一张图验 `file.exists`，非写完 R 代码字符串就算。
- **竞品诚实重述（Round 2 R1）**：截轴/双轴/render-then-look/出版规格/色盲是**同类共识**（scipilot 530★ 18-pitfall、davila7 28.2K★ 13-pt checklist 都覆盖），**非 Light 独创**；Light 真增量=把同一 catalog 做成**确定性机读 critical 门 + 绑 result-analysis 证据档(`misrepresent_evidence`，10 同类零覆盖) + 9→7 回炉 + 集合预算**——同类全是 prose 规则 + refusal 启发 + 人工 checklist。见 truth_source §0.A/§0.C。
- **零 MCP/零本地库**：framework 图用 Draw.io（diagram-as-code，CLI 导出）/TikZ 程序化生成，不依赖 MCP；venue 规格在线查/用户给，不内嵌本地期刊库。
