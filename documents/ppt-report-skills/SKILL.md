---
name: ppt-report-generator
description: 汇报 PPT 生成器 / 数据报告演示稿生成工具——把数据汇报做成 16:9 网页版 PPT（设计稿 1600×900，浏览器自适应缩放），可全屏播放、一键导出 PDF。分页拆分源码 + 数据物理分离 + 多主题可切换 + ECharts 图表。当用户要"做月度/季度汇报"、"做工作汇报 PPT"、"把数据做成网页/PDF 形式的演示稿"，或希望复用一套"每页一个文件、数据单独存放、主题可换"的 PPT 模板时，**务必使用本 skill**。即使用户没说"PPT"二字，只要任务是把"多组数据 + 结论"产出为可演示/可分享的网页报告，也按本 skill 的工作流走。
---

# PPT Report Generator — 汇报 PPT 生成器（网页版 PPT 模板）

把"多组业务数据 + 阶段性结论"产出成一份 16:9 的、可在浏览器全屏播放、可一键导出 PDF 的网页版 PPT。

## 核心承诺（设计目标）

1. **每页 PPT = 三个文件**：`slides/slide-N.html` + `scripts/slide-N.js` + `styles/slide-N.css`，由 `build.py` 合成单一 HTML。改一页只动一页，**省 token、省冲突**。
2. **数据与渲染物理分离**：所有图表/表格的数据放在 `data/slide-N.{xlsx,csv,json}`，build 时自动转 JSON 注入。**日常用 Excel 改数据**，渲染代码完全不动。
3. **图表选型有规则**：每种数据形态对应一种图表类型（见 `references/chart-mapping.md`），**不要随心情画图**。默认使用 **ECharts**。
4. **信息层次有硬规则**：标签 / 大标题 / 副标题（结论）/ 区块标题 / 卡片标题 / 正文 / 注释 / 辅助文字 8 级，每级字号、字重、颜色都固定（见 `references/design-system.md`）。
5. **多主题可切换**：5 套预设主题（modern-light / dark-tech / warm-business / brand-blue / minimal-mono），通过 `data-theme` 属性切换（见 `references/themes.md`）。

## 何时启用本 skill

触发条件（任意一条命中即用）：

- 用户说："做一份月度/季度/项目汇报"、"做工作汇报"、"做数据汇报 PPT"、"把数据做成可演示的网页"
- 用户给了一份原始数据（xlsx / 多个表格 / 一段文字描述结论）并希望产出"汇报"
- 用户已有一份这种结构的项目（`src/slides/`、`build.py`、`shell.html`）想新增一页或换主题
- 用户想"把这个 PPT 沉淀下来下次复用"

## 工作流（标准步骤）

### Step 1 — 理解输入与产出

- 问清楚（如果不知道）：**几页？每页讲什么？关键数据在哪？目标读者是谁？要不要 PDF？**
- 不要直接动手画图。先把每页的 **(label, title, subtitle/结论, 主体类型)** 列出来给用户确认。

### Step 2 — 选模板（每页）

打开 `assets/slides-templates/`，按页面"主体类型"挑一个起点：

| 主体类型 | 模板 | 用法 |
|---|---|---|
| 月度交付总览（多板块 × 多卡片） | `kpi-overview.html` | 第 1 页类汇总页 |
| 两个对象左右对照（如两国数据） | `two-country.html` | KPI 行 + 双卡片 metric 表 |
| 三阶段时间线 + 多个图表 | `three-phase.html` | 时间线 + 多 chart-card |
| 多对象时间趋势 | `multi-trend.html` | 4 国 / 4 渠道 折线图 + 里程碑标记 |
| 分类条形 + 趋势折线组合 | `supply-bars.html` | 物料/品类 mini-bar + 总趋势 |
| 产业图谱 / 竞品全景 / 客户分层（一个领域/生态的完整图谱） | `landscape-map.html` | **⚠ 用前必读 [`references/landscape-skeleton.md`](references/landscape-skeleton.md) 选骨架** —— 这套三层 tier 只适合 AI/SaaS 软件分层栈；实体产业/航天/能源等用价值流横轴；银行用客户矩阵；创新药用研发管线。选错骨架 = 八股套用,会被一眼识破 |
| 2×2 战略矩阵（波士顿 / GE-McKinsey 风） | `matrix-2x2.html` | 在两个连续维度上定位 N 个对象的咨询报告标配页型。**典型场景:竞品估值定位 / BCG 业务段矩阵 / 客户分层 / 项目优先级**。纯 CSS 实现(不要用 ECharts scatter — 4 象限着色 + 标签防遮挡用 CSS 干净得多)。详见 [`references/matrix-2x2.md`](references/matrix-2x2.md) — 含 6 套经典轴组合 + 数据归一化公式 + 标签防遮挡规则 |
| 人物画像 / 拟人化能力 / 风险热图 | `human-portrait.html` | **数据驱动一次成 ⭐**。中央人体剪影 + 部位**可见色点** + 周边标签 + 引线**自动连接**。只写一段 `labels` 数据(每个标签绑定一个身体 `part`),剪影 path / 部位坐标 / 色点 / 引线全部由 `assets/scripts/silhouette.js` 的 `renderHumanPortrait()` 算出 —— 无需手画剪影 / 校准坐标 / 摆引线像素。详见 [`references/human-portrait.md`](references/human-portrait.md) |
| 价值流横轴(实体产业「价值如何沿链条流动」) | `value-chain.html` | **B 骨架 · 实体产业框架图**。5~6 个环节卡横向 ▶ 串联,每段含「核心数字 + 关键活动 + 自营/外采徽章」,色彩沿链渐深表达价值聚集。适用:商业航天 / 能源 / 制造 / 消费品。纯 CSS 全静态,零 JS。⚠ 用前先读 [`references/landscape-skeleton.md`](references/landscape-skeleton.md) 确认骨架 |

模板是骨架，**复制后改文案、改数据、改 ID** 即可。

### Step 3 — 数据放进 `src/data/slide-N/`

**这一步最重要**。**每页一个文件夹**，里面放任意多个独立数据文件，文件名（不含扩展名）即 JS 里的 key，build 时自动合并注入为 `window.__DATA_N__`。

```
src/data/slide-3/
├── kpis.xlsx      →  window.__DATA_3__.kpis   （单 sheet 自动解包为数组）
├── trend.csv      →  window.__DATA_3__.trend
└── marks.json     →  window.__DATA_3__.marks
```

**支持三种格式**，可混用：

| 格式 | 转换结果 |
|---|---|
| `.xlsx` 单 sheet | `[{col: val}, ...]` 数组（**自动解包**，省掉一层 key） |
| `.xlsx` 多 sheet | `{sheetA: [...], sheetB: [...]}` dict |
| `.csv` | `[{col: val}, ...]` 数组 |
| `.json` | 原值直接读取 |

**约定**：第 1 行 = 表头；数字自动转 number；sheet 名 / 列名 / 文件名以 `_` 开头跳过（备注用）；空行跳过。

**JS 里访问**（多数据源各自独立）：

```js
function initSlide3() {
  const D = window.__DATA_3__;
  // D.kpis  = [{label: 'DAU', value: 12.4}, ...]    ← 来自 kpis.xlsx
  // D.trend = [{week: 'W1', na: 12.1, eu: 8.4}, ...]  ← 来自 trend.csv
  // D.marks = [{x: 'W4', label: '上线'}, ...]         ← 来自 marks.json
}
```

**下次更新数据**：直接在 Excel / CSV 里改完保存，重跑 `python3 build.py` — 渲染代码完全不动。

**独立调试**：`python3 xlsx2json.py src/data/slide-3/` 可单独看该页合并后的 JSON 输出。

**向后兼容**：旧格式 `slide-N.xlsx / .csv / .json` 单文件仍支持，build 优先找目录、找不到再找单文件。详见 [`references/architecture.md`](references/architecture.md)。

### Step 4 — 选图表（看 `references/chart-mapping.md`）

不要直接选自己想画的图。根据数据形态查决策表：

- 时间序列 → 折线（带里程碑竖线 plugin）
- 对照实验前后对比 → 100% 堆叠条形
- 对象排名（Top 20） → 横向 mini-bar（自定义 div，不用 chart 库）
- 多对象单期对比 → 分组条形
- 占比/构成 → **不要饼图**，用 100% 堆叠条形或矩形树图

### Step 5 — 信息层次（看 `references/design-system.md`）

每段文字必须能回答"我是哪一级"。slide-label / slide-title / slide-subtitle 三件套是**强制顶部结构**。结论里的关键数字必须包 `<strong>` 或 `<span class="pos|neg|warn">` 高亮。

### Step 6 — 构建与预览

```
python3 build.py            # 合成最终 HTML → 输出到 dist/（目录/文件名可在 build.py 顶部 CONFIG 改）
open dist/*.html            # 浏览器打开，按 ←/→ 翻页
python3 export_pdf.py       # （可选）导出 PDF（自动找 dist/，输出 dist/*.pdf）
```

### Step 7 — 主题切换（可选）

如果用户想换风格，**不要重写 CSS**。在 `<body data-theme="dark-tech">` 上改 attribute 即可。详见 `references/themes.md`。

### Step 8 — 交付前自检（必做，别"应该没问题"就交）

构建完不等于做完。交付前**三件事一件不少**（详见 [`references/report-quality.md`](references/report-quality.md) 的 14 条铁律 + checklist）：

```
python3 check_deck.py          # 机检：字号过小 / 币种混用 / 数字缺信源 / 术语清单
python3 export_images.py dist/*.html   # 逐页截图（横屏可用 export_pdf.py）——必须肉眼过一遍
```

1. **对照 `report-quality.md` 逐条自查**：内容可信（信源 / 单一真相 / 事实观点分离）→ 表达清晰（术语解释 / 结论先行 / 分层供给）→ 版面克制（不留空白 / 字号可读 / 对齐 / 一页一事）。
2. **跑 `check_deck.py`**：把能机检的（字号、币种、信源、术语）一把过，WARN 逐条确认。
3. **逐页截图肉眼过**：溢出 / 留白 / 错位 / 一页多事 这类**脚本测不准**（嵌套 flex/grid 自写检测会误判，教训见 `landscape-qa.md`），**只信截图**。

## 竖屏格式（手机 / 小红书 / 公众号 / 朋友圈）⭐

横屏（16:9）是默认；但**面向手机观看**（老板手机竖握看）或**社媒公司宣传**（小红书 / 公众号 / 朋友圈 / 视频号）时，要出**竖屏版本**——网页 / PDF / 图片三种输出都支持。详见 [`references/portrait.md`](references/portrait.md)。

**核心理念**：低「内容密度」、不低「有效信息密度」——一屏**少放东西**（元素 ≤ 5、大字号、大留白、一个核心观点 + 一个视觉锚），但每个元素**有信号、不放水**。别把横屏高密度页直接竖过来。

**工作流（场景驱动，关键）**：
1. **先问用户本次发哪儿**（不要默认）：小红书图文 / 公众号长图 / 朋友圈 / 老板手机看 / 视频号？
2. 查 [`assets/presets.json`](assets/presets.json) 取该场景的**标准尺寸 + 页面模型 + 导出形态**（小红书=3:4 1242×1656 逐张卡 / 公众号=1080 宽长图 / 朋友圈=4:5 / 手机全屏=9:16 …，中文别名也认）。
3. 用竖屏 shell + 竖屏模板生产：
   - `cp assets/shell-portrait.html src/shell.html`（按场景改 body 的 `--design-w/h`）
   - `cp assets/styles/portrait.css src/styles/`（build.py 自动纳入）
   - 选 `assets/slides-templates/portrait/` 的模板（10 套）：`cover`（封面钩子）/ `big-number`（单巨数）/ `list`（≤5 项）/ `single-chart`（单图）/ `quote`（金句）/ `section`（章节分隔）/ `end`（结尾 CTA）/ `comparison`（A vs B 对比）/ `timeline`（竖向时间线）/ `image-text`（上图下文）
   - **一套内容可多比例导出**：写好后 `export_images.py --preset 小红书/公众号/手机汇报` 会按目标比例重渲染出图，不用为每个平台重做
4. `python3 build.py` → `python3 export_images.py dist/*.html --preset 小红书`（按场景精准出逐张 PNG / 长图 / PDF）。

> 竖屏全部 scope 在 `[data-format="portrait"]`，与横屏零冲突。`--design-w/h` 设在 `<body>` 上。

## 黄金规则（违反会被 review 打回）

1. **不要把数据写死在渲染代码里**。数据进 `data/slide-N.json` 或顶部 const 变量，渲染函数只接受参数。
2. **不要让一页 HTML 超过 200 行**。超了就拆子组件或挪到 JS 渲染。
3. **不要堆字号自由发挥**。只用 `--fs-label / --fs-title / --fs-subtitle / --fs-h2 / --fs-h3 / --fs-body / --fs-caption / --fs-mini` 8 个级别。
4. **不要用饼图展示 5 项以上的占比**。改用 100% 堆叠条形。
5. **不要硬编码颜色**。用 `var(--accent)`、`var(--accent2)` 等主题变量，确保切主题不崩。
6. **每页都要有 `slide-label`、`slide-title`、`slide-subtitle`** 三件套。subtitle 必须是**一句结论**，含关键数字。
7. **设计稿固定 1600×900**。所有元素按这个像素来定，浏览器自适应由 `transform: scale(--fit)` 自动处理。**不要用 vw/vh**。
8. **不要在 build 产物里手动改东西**。永远改 `src/`，再 `python3 build.py`。
9. **每页只回答一个问题，只有一个视觉锚点**。一页超过 12 个主体元素 = 拆两页（详见 `references/layout-principles.md` 第 6/10 节）。
10. **整份 deck 要有节奏**。不要 6 页全是高密度数据页，中间插"总览/呼吸/收尾"低密度页（详见 `layout-principles.md` 第 11 节"故事曲线"）。
11. **卡片边界必须严格对齐**：同行卡片底边齐、同列卡片左右边齐。靠 grid `1fr 1fr` + 子项 `flex:1 1 0; min-height:0` + 弹性占位（如 phase-arrow-v）补差，**不要写死 height**（详见 `layout-principles.md` 第 7b 节）。
12. **结构图/图谱类（landscape-map / value-chain）排版：全静态 CSS + 数据层规范，JS 只注入 logo——绝不测量卡片尺寸反推布局**。
    - 数据层（最关键）：每个 chip 一个短词（≤ 4~5 字 / 一个英文术语）；「A / B」「A + B」合并项拆成多个独立 chip；英文用业内简写（DSSM / MMoE / ANN）。**嵌套小格 ≤ 3 chip、简单卡 ≤ 4 chip**，保证落在 1/3 tier 高度内不裁切（超了就是该拆两页的信号）。
    - 渲染层：chip 固定字号（15px / 嵌套 13px）、`flex-wrap` 居中且 **`align-items:center`**（关键！flex 默认 stretch 会把 chip 纵向拉成 2 倍高，是高度失控的隐形元凶）；三 tier 用 `grid-template-rows:1fr 1fr 1fr` 等高封顶——有界，永不溢出。
    - **严禁**：写 JS 逐卡 / 全局测量卡片尺寸反推 chip 字号 / span / 列数 / tier 高度做"自适应铺满"——这条路（cqh / 二分逼近 / 等宽 / 动态重分 / logo 异步重算）被反复验证为死结，**现模板已彻底移除这类 JS**。
    - 验证只信**完整全页截图肉眼**，不信自写的 scrollWidth/Height 截断检测（嵌套 flex/grid 下系统性误判，多次"数字报裁切"被全图打脸）。文案超出 → 精简数据重跑，不改渲染逻辑。
13. **"产业全景图" / "行业图谱"类页面，先选骨架,再写 chip**。不要见到"全景图"就反射式套 `landscape-map` 三层 tier 模板 —— **那只是 AI / SaaS 软件分层栈的专用骨架,不适用所有行业**。
    - 实体产业 / 航天 / 能源 / 制造 → **价值流横轴**(原料→生产→流通→服务) · ✅ 模板 `value-chain.html`
    - 银行 / 保险 / 券商 / 咨询 → **客户矩阵**(纵轴客户分层 × 横轴产品 / 渠道)
    - 生物医药 / 新药研发 → **研发管线时间轴**(已上市 → III 期 → II 期 → I 期 → 临床前)
    - 平台型 / 生态型(微信 / 阿里) → **生态网络图**(中心节点 + 放射状外围)
    - 通用 AI / 软件分层栈 → **landscape-map 三层 tier** ✓
    - **强制流程:** 任何"产业全景图"类任务,先读 [`references/landscape-skeleton.md`](references/landscape-skeleton.md) 选定骨架,在 slide 顶部 HTML 注释里写下"骨架 + 理由",再开始动手。选错骨架会被一眼识破"参考案例呆板"——这条规矩是 SpaceX IPO Deck 那次教训沉淀的。

## 详细参考文档

读取顺序按需：

- [`references/architecture.md`](references/architecture.md) — 拆分架构、build.py 工作原理、自适应缩放
- [`references/design-system.md`](references/design-system.md) — 字号 / 字重 / 颜色 / 间距硬规则（**字怎么写**）
- [`references/layout-principles.md`](references/layout-principles.md) — 经典汇报 PPT 布局法则：金字塔结构、F/Z 阅读路径、三分法、视觉锚点、信息密度、故事曲线（**东西怎么摆**）
- [`references/report-quality.md`](references/report-quality.md) — **交付前质量铁律 14 条 ⭐**（内容可信 / 表达清晰 / 版面克制 / 工艺可靠）+ 可勾选 checklist。每条 ❌→✅。**交付前 Step 8 逐条对照**，配套机检脚本 `check_deck.py`
- [`references/chart-mapping.md`](references/chart-mapping.md) — 数据形态 ↔ 图表选型决策表（ECharts 配置范本）
- [`references/components.md`](references/components.md) — 通用组件库（KPI / 卡片 / Phase / Timeline / Mini-bar / Metric-row）
- [`references/themes.md`](references/themes.md) — 5 套预设主题 + 自定义主题方法
- [`references/landscape-skeleton.md`](references/landscape-skeleton.md) — **「产业全景图」骨架选择强制流程**(5 种骨架: 分层栈 / 价值流横轴 / 客户矩阵 / 研发管线 / 生态网络)。做全景图前**先读这个**,选定骨架再开工,避免见到"全景图"就套 landscape-map 八股
- [`references/landscape-qa.md`](references/landscape-qa.md) — landscape-map / 结构图类页面生成后的质量自检与优化清单（踩坑黑名单 · 数据规范 · 渲染自检 · LLM 二次复查），生成此类页面后**逐条对照**(注:仅在选定骨架是「A 分层栈」后才用本清单;其他骨架不适用)
- [`references/matrix-2x2.md`](references/matrix-2x2.md) — **2×2 战略矩阵设计与数据规范**(咨询报告标配页型)。6 套经典轴组合、归一化公式、4 象限战略命名、标签防遮挡规则、踩坑黑名单。做"竞品定位 / BCG 矩阵 / 客户分层 / 项目优先级"类页面**先读这个**
- [`references/svg-aesthetics.md`](references/svg-aesthetics.md) — **让 AI 手写的 SVG 真的好看**(5 大反丑原则 + OpenMoji 抓取大法)。任何需要写 inline SVG 的场景(人体 / 图标 / 流程节点 / 徽章)**先读这个**,不要凭直觉硬画 path
- [`references/human-portrait.md`](references/human-portrait.md) — **人物画像页型(数据驱动一次成)**。中央人体剪影 + 部位可见色点 + 引线自动连接,只写 `labels` 数据。配套 `human-portrait.html` 模板 + `scripts/silhouette.js`(剪影资产)
- [`references/portrait.md`](references/portrait.md) — **竖屏格式(手机 / 小红书 / 公众号 / 朋友圈)⭐**。场景驱动:先问发哪儿 → 查 `presets.json` 取标准尺寸 → 用竖屏模板 → `export_images.py` 出图。低内容密度高有效信息密度 + 场景规格表 + 10 套竖屏模板 + 三种输出。做竖屏汇报/社媒宣传**先读这个**

## 资产清单

`assets/` 下都是**可直接拷贝**的成品文件：

- `shell.html` — HTML 骨架（含 `{{STYLES}}` `{{SLIDES}}` `{{SCRIPTS}}` 占位符）
- `build.py` — 合成脚本（按页号顺序拼接；**自动抽取模板内联 `<style>`/`<script>`** → 模板做到「一个文件，拷过去即插即用」，不用手动拆样式块；同时把 src/assets/ 拷进 dist/）
- `export_pdf.py` — 横屏 PDF 导出（playwright + img2pdf）
- `export_images.py` — **竖屏导出**（逐张 PNG / 公众号长图 / PDF），场景预设感知（`--preset 小红书`）
- `check_deck.py` — **交付前机检**（字号过小 / 币种单位混用 / 数字缺信源 / 术语清单）。只做不依赖布局测量的可靠检查；溢出 / 留白交给截图。配 `references/report-quality.md`
- `presets.json` — **竖屏场景规格表**（小红书 / 公众号 / 朋友圈 … → 标准尺寸 + 页面模型 + 导出形态）
- `shell-portrait.html` — 竖屏 shell（`data-format="portrait"` + 画幅变量）
- `fetch_logos.py` — 可选：把在线 logo 下载缓存到本项目 src/assets/logos/ 供离线/存档（landscape-map 默认在线引用 logo，不跑此脚本也能显示，跑了则断网也不丢）
- `styles/common.css` — 全局样式 + 5 套主题变量
- `styles/components.css` — 通用组件
- `scripts/common.js` — 自适应、导航、ECharts helper
- `scripts/silhouette.js` — **人体剪影资产**（男/女剪影 path + 部位坐标 + `renderHumanPortrait()`，human-portrait 页用，build 自动注入）
- `scripts/theme-switcher.js` — 主题切换 UI
- `data/slide-N.json` — 数据样例
- `slides-templates/*.html` — 9 套**横屏**页面模板（kpi-overview / two-country / three-phase / multi-trend / supply-bars / landscape-map / matrix-2x2 / human-portrait / value-chain）
- `slides-templates/portrait/*.html` — 10 套**竖屏**低密度模板（cover / big-number / list / single-chart / quote / section / end / comparison / timeline / image-text）
- `styles/portrait.css` — **竖屏低密度设计系统**（scope 在 `[data-format="portrait"]`，横屏零影响）

## 初始化新项目（推荐流程）

```bash
mkdir my-report && cd my-report
# 1. 拷贝 assets 整个目录到当前项目作为 src/
cp -r <skill_path>/assets src
# 2. 拷贝 build.py / export_pdf.py 到项目根
cp <skill_path>/assets/build.py <skill_path>/assets/export_pdf.py .
# 3. 按需挑模板，重命名为 slide-1.html / slide-2.html ...
# 4. 写数据 → 改文案 → build → 预览
```
