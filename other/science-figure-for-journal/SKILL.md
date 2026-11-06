---
name: science-figure-for-journal
description: Use when a figure has to survive peer review and print — when choosing a figure type for a comparison, a distribution, a paired design or a survival curve; when a journal demands specific column widths, minimum type size, vector formats or resolutions; when error bars must state what they are; when a figure came back from review as "unreadable" or "insufficient resolution"; also use when deciding whether a bar chart is the wrong choice.
---

# 图：先决定它要证明什么，再决定它长什么样

## 尺寸先定，字号其次，字体最后

期刊的栏宽是**物理量**：单栏 85–90 mm，双栏 180–190 mm。你的图必须按这个物理尺寸排版，
然后再去看字号。

反过来做（先画一张 8 英寸宽的图，再在排版时缩到 85 mm）会出人命：缩放 2.4 倍后，
8 pt 的字变成 3.3 pt，印刷出来是一团灰。

`science_figure` 就是按这个顺序做的：`widthMm` → `fontSize`（默认 7 pt，低于 6 pt 直接拒绝）→ 出件。

| 预设 | 毫米 | 什么时候用 |
| --- | --- | --- |
| `single-column` | 85 × 60 | 单栏期刊的多数图 |
| `double-column` | 180 × 120 | 时间序列、多面板、热图 |
| `square` | 90 × 90 | 相关散点、混淆矩阵 |
| `wide-short` | 180 × 75 | 时间轴上的多个条件 |
| `slide` | 160 × 90 | 报告用，300 dpi 够 |

## 图型选择：别用柱状图默认一切

| 你想说 | 该用什么 | 别用什么 |
| --- | --- | --- |
| 两组连续值有差异 | 带散点的柱图，或 `box` / `violin` | 只有两根柱子的柱图（看不出分布与 n） |
| 同一批人两个条件 | `paired`（每人一条线） | 两个并排柱（丢掉了配对信息） |
| 分布形状重要 | `violin` / `hist` | 只报均值±SEM |
| 两个连续变量的关系 | `scatter` + 拟合线 | 把连续变量分箱后画柱图 |
| 时间/序列 | `line` | 柱图（相邻时间点被视觉隔断） |
| 生存 | Kaplan-Meier 阶梯曲线 | 柱状图比"生存率" |
| 多变量相关结构 | `heatmap` | 一堆散点矩阵 |

## 误差棒：必须声明是什么

`science_figure` 不给你默认误差棒——`errorType` 传 `sd` / `sem` / `ci95` 才有。

原因很实际：三者数值差 √n 倍，读者无法从图上看出来。不说明的误差棒，审稿人一定会问，
而且往往说明作者自己也没想清楚。

- **SD**：描述这批数据的离散程度。想让读者知道个体差异时用。
- **SEM**：描述均值估计的精度。想强调"均值有多准"时用，但容易被误读成离散度。
- **95% CI**：与假设检验直接对应（跨 0 即不显著），信息量最大，推荐。

图注里写清，例如："误差棒为 95% 置信区间（n = 24，bootstrap 2000 次）"。

## 颜色

默认 `okabe-ito`：8 色，色盲友好，且不依赖红绿对立。

不要用：红/绿配对（约 8% 男性分不出）、彩虹色图（感知不均匀，会凭空造出边界）、
纯靠透明度区分（黑白打印后全糊）。

灰度检查：把图转成灰度看一眼，如果两类分不开，换调色板或换形状/线型。

## 文件格式

| 格式 | 用途 | 注意 |
| --- | --- | --- |
| PDF | 投稿首选（矢量） | 字体嵌入，`pdf.fonttype 42` 已设 |
| SVG | 需要在 Illustrator 里改 | 文字保持可编辑（`svg.fonttype none`） |
| PNG | 预览、网页、部分系统要求 | ≥300 dpi，线条图建议 600 |
| TIFF | 少数刊强制 | 需要额外依赖，缺了就报 `skipped`，不假装生成 |

一次出 PDF + SVG + PNG，别只给一种。投稿系统临时要什么都能应付。

## 自检（`ready` 字段）

`science_figure` 返回 `checks`，四项：字号 ≥6 pt、有矢量格式、位图 ≥300 dpi、宽度合理。
`ready: false` 时先修，不要"先交上去再说"——这类退修完全可避免。

## 常见退修理由与对策

| 退修理由 | 真实原因 | 对策 |
| --- | --- | --- |
| "图分辨率不足" | 交了 72 dpi 的 PNG | `dpi: 600` + 交 PDF |
| "文字太小无法阅读" | 大图缩放排版 | 按毫米定尺寸，字号 ≥6 pt |
| "误差棒含义不明" | 没写图注 | 写清 SD/SEM/CI 与 n |
| "颜色难以区分" | 红绿配色 | 换 `okabe-ito`，做灰度检查 |
| "图为装饰性而非信息性" | 柱图替代了分布 | 换 `box`/`violin`/`paired` |
| "图与正文数字不一致" | 图来自旧版分析 | 重跑 `science_figure`，把 `analysisId` 关联上 |
