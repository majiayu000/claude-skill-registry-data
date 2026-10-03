---
name: yq-editorial-presentation-html
description: 可变体的 warm editorial 演示设计系统，用于 presentation、case sharing、项目汇报、战略叙事和产品发布。支持横向全屏 HTML deck 与程序化 PPTX，通过 style profile、语义 slide manifest、构图新颖度规划和反重复验证，在保持编辑设计 DNA 的同时避免固定配色、固定卡片和固定 11 页模板。用户要求 Pfizer/Anthropic/warm editorial/编辑设计风格、类似血液科那套，或需要高规格且非模板化的 HTML/PPT 演示时使用。
---

# Editorial Presentation (HTML + PPTX 双模)

## 这个 skill 是什么

一套**可规划、可验证、可变体**的视觉设计语言 skill，源自 Pfizer 血液科 IFI 案例分享 v5 desktop 版，并把单一成品样式拆成稳定 DNA 与可选 style profile。

**核心价值**：先按受众、目的、正式度、密度和语义关系规划，再渲染 HTML/PPTX。复用的是编辑设计原则、角色化 token、构图语法与质量门，不是把不同主题替换进同一套米色卡片模板。

**双输出模式**:
- **HTML 模式**（默认）：用于浏览器演示的**横向全屏 deck**。F11 下每页固定 100vw × 100vh，支持左右翻页、底部圆点、触屏/滚轮、ESC overview，并完整支持 profile 与构图语法。
- **PPTX 模式**：用于必须交 .pptx 文件的场景（高管会、客户演示、传统企业）。通过 python-pptx 程序化生成，与 HTML 共用 manifest；只选择明确支持 PPTX 的 profile。

**两种模式共享的设计 DNA**：
1. 温暖但克制的编辑质感、证据可读性和固定 16:9 舞台。
2. display / body / data 三类字体角色；具体字族由 profile 决定，原始 Pfizer profile 仍使用 Fraunces / Inter / JetBrains Mono。
3. 颜色通过 canvas / surface / ink / primary / secondary / signal / positive / negative 等角色分配，不锁死一组 RGB。
4. 先判断数据关系、基数、密度、不确定性和叙事角色，再分别选择表达家族与构图。
5. 同一 profile 内保持一致，但相邻页面不得机械复用相同构图、几何和背景节奏。
6. HTML 与 PPTX 共用同一份 slide manifest；格式降级必须记录，不能全部退化为卡片网格。

## 何时使用(**必须主动触发,不要等用户说风格名**)

任一信号出现时使用：

- 明确要求 "warm editorial / Anthropic / Pfizer / 编辑设计 / 类似血液科那套"
- "做一个 presentation / slides / PPT / 幻灯片 / 演示文稿 / 汇报" 且上下文要求高规格视觉设计
- "做 case sharing / 案例分享 / 项目展示 / 战略汇报"
- "给老板/director/VP 看 / 给客户演示"
- "类似血液科那套 / Pfizer 风格 / Anthropic 风格 / warm editorial / 编辑设计风格"
- "把 X 内容做成可演示的页面 / 做成 deck"
- 用户给一份内容(产品发布、市场调研、技术分享、案例复盘),需要做成展示

普通 PPT 编辑、只改一行文字或用户已指定另一套视觉系统时不要抢占。触发后也先选择 profile 与构图语法，不默认套原始 Pfizer 配色。

## 第 0 步:**判断输出格式**

问自己 / 看用户表述:

| 用户说... | 用 |
|----------|-----|
| "做 HTML 页面 / 网页 / 浏览器演示 / F11 全屏 / 加跳转链接 / 嵌入视频" | **HTML 模式** |
| "做 PPT / .pptx / PowerPoint / 幻灯片文件 / 给传统企业用" | **PPTX 模式** |
| "做 presentation"(没说格式)| 默认 **HTML 模式**(更高保真),并主动问"要不要也出一份 PPT 版?" |
| "做一份给客户演示用的"(看上下文)| 客户是 IT/科技 → HTML;客户是医药/金融/政府 → PPTX |
| "做幻灯片样式"但没说文件类型 | HTML 模式(横向全屏 deck) |

如果不确定,**默认 HTML**(因为它复刻度最高,后续可再衍生 PPT)。

---

## HTML 模式工作流

### Step 1 · 读 references

按需读:

- **`references/visual-grammar.md`** 必读 — profile 选择、密度模式、slide manifest、构图语法与反重复质量门。
- **`references/style-index.json`** 必读 — 只做 shortlist；选定后只把一个 profile 的角色 token 带入生成上下文。
- **`references/design-tokens.md`** 必读 — invariant token 与 profile 角色映射。只有用户锁定原始 Pfizer look 时才原样使用 legacy token block。
- **`references/typography.md`** 必读 — display / body / data 角色与 projection scale；具体字族来自选定 profile。
- **`references/chart-selection.md`** 必读 — 图表选择规则。先判断数据关系,再选 stat / timeline / matrix / funnel / bar 等组件。**禁止把所有数字都画成条形图**。
- **`references/components.md`** — 视觉组件的 HTML+CSS 切片,包含每类组件的"何时用 / 不何时用"。
- **`references/layouts.md`** — 横向全屏 deck 的 slide 节奏、grid 布局、navigation。
- **`references/rewrite-existing-html.md`** — 改写已有 HTML deck 的专用流程。保留内容 section,只替换演示 shell / CSS / JS。
- **`references/qa.md`** — 生成后检查。重点查主内容宽度、垂直沉底、页脚遮挡、overview 和滚动条。

### Step 2 · 用 behavior-only shell 起手

`assets/deck-shell.html` 是默认行为骨架：横向全屏 deck shell、底部圆点、左右翻页、ESC overview、触屏与滚轮。它不提供成品内容页，避免示例内容和版式预先支配生成。**不要从旧的纵向滚动 starter 开始**。

动手前先读 shell 的行为 CSS 和 `<script>`。shell 是 `#deck`、overview、dots、wheel/touch 的结构来源，不是视觉方向或 slide anatomy 的来源。构图来自 manifest 和选定 profile。`assets/starter-template.html` 仅作为 legacy Pfizer component gallery，除非用户锁定原始 profile，否则不要加载。

### Step 2.2 · 先生成 slide manifest

先整理 brief JSON 和 slide intents，再运行：

```bash
python assets/plan_deck.py brief.json -o deck-manifest.json
```

检查 `validation.passed`。生成 HTML 与 PPTX 时复用同一份 manifest。用户锁定 profile 时传 `locked_profile`；未锁定且视觉空间较大时，先展示三个真正不同的方向供选择。相同 brief + profile + seed 必须生成相同 manifest。

### Step 2.4 · 用同一 manifest 渲染

新 deck 优先使用共享 renderer，而不是让 HTML 和 PPTX 各自猜一遍布局：

```bash
python assets/render_manifest.py deck-manifest.json --output-dir output/deck
```

它会生成 `deck.html`、`deck.pptx` 和 `render-report.json`，把同一 manifest SHA256 写入两种输出，并记录每页 composition 与 major-region signature。只需 HTML 或 PPTX 时使用 `--html-only` / `--pptx-only`。legacy `add_*_slide()` 只用于兼容旧调用或需要自定义低层绘制的页面。

### Step 2.5 · 如果用户给的是已有 HTML

打开 `references/rewrite-existing-html.md`。这种任务的目标不是重写内容,而是把旧 deck 按本 skill 的 shell 重新渲染:

- 保留原始 `<section class="slide"...>...</section>` 的内容块,除非用户明确要求改文案。
- 替换纵向 scroll-snap / `scrollIntoView` / `IntersectionObserver` 为横向 fixed deck。
- 把旧整页深色主题降级为局部语义色,整体仍用 v5 warm editorial。
- 按 `references/qa.md` 跑检测,不通过就先修 skill / 模板规则,再重新生成。

### Step 3 · 按需嵌组件

`references/components.md` 是组件粘贴库和使用说明:

- 数据展示:stat-card / stat-grid / market-bars / evidence-pyramid / literature-funnel / proof-bars
- 时间与流程:timeline / clock-path / decision-window / phase-pill / wf-phase / ttet-step / arch-overview
- 匹配关系:matrix / gene-drug-map / product-path-card / before-after
- 导航跳转:jump-row / subpage-card / aux-card
- CTA / Callout:cta-grid / data-pain / iron-rule-band / anti-pattern-callout
- 品牌:product-card / dual-products

### Step 4 · 图表选择(先做,不要跳过)

打开 `references/chart-selection.md`，先把每页的关系、基数、系列数、密度、不确定性和叙事角色列出来。表达家族与页面构图是两个决策，不要把 `comparison` 永远映射为同一张 bar slide。

| 数据关系 | 组件 |
|---|---|
| 一个数字很重要 | stat-card / big-number |
| 多个独立 KPI | stat-grid / stat-strip |
| 时间先后 / 诊疗窗口 | timeline / decision-window |
| 输入到输出 / 操作步骤 | pipeline / phase-pill |
| 病原体 / 基因型 / 机制 / 产品匹配 | matrix / gene-drug-map |
| 文献筛选数量递减 | funnel |
| 证据强弱分层 | pyramid / evidence-ladder |
| 同一指标跨对象比较 | proof-bars / ranked bars |
| 患者旅程阶段覆盖 | market-bars |

**硬规则**：
- 条形图只用于同一指标的横向比较、完成率、覆盖率、通过率。
- 多个互不相干 KPI 不得画成 proof-bars。
- 时间路径、机制匹配、证据链、决策流程不得画成普通 bar chart。
- 一个 deck 默认至少使用 3 类不同表达家族；10-12 页 deck 在内容允许时至少 5 个构图 ID、4 种主几何。
- 相邻非续页不得使用相同 `composition_id`；不得连续 3 页使用相同主几何或 tone。
- 重复同一表达家族时，必须改变构图或注释结构。

### Step 5 · 颜色语义化分配

从选定 profile 读取角色 token：`canvas`、`surface`、`contrast_surface`、`ink`、`muted`、`primary`、`secondary`、`signal`、`positive`、`negative`。状态色语义在整份 deck 内固定；分类色不能误用 positive / warning / negative。按 profile cadence 安排背景节奏，不逐页随机换色，也不连续三页使用同一 tone。

### Step 6 · 章节节奏（按论证结构规划，不默认 11 页）

```
opener → context/tension → evidence → explanation → decision → close
```

这是论证语法，不是固定页数。投资人、技术评审、学术报告、产品发布和运营复盘应产生不同节奏。每页在 manifest 中声明 `narrative_role`，需要续页时声明 `continuation_of`。

每个 slide 固定 `width:100vw;height:100vh`,内容区居中但必须吃满演讲画布。常规页面优先 `.wrap,.frame { max-width:min(1690px,88vw) }`;内容密集或投影演讲页面可用 `.wrap.wide,.frame.wide { max-width:min(1760px,93vw) }`,避免主体缩在屏幕中间太小。常规页标题应接近 90-106px,lead 应接近 28-36px;长标题或 1440×900 下可降到 78px,但 1920 下 regular title median 不能只有 78-85px。`dense-slide` 不等于 `compact`:dense 页可以更宽、更紧,但非 compact dense 页不能把标题封顶到 84px。只有 evidence/table/appendix `.compact` 页可以降级。页脚留在 slide flex 流里,但 `.wrap` 不要用 `margin:auto auto 0` / `margin:auto`,否则会和 footer 的 auto margin 叠加,导致偶发内容沉到底部。不要使用页面纵向滚动来展示下一页。

### HTML 验证清单

- [ ] `:root` 完整 80+ 变量
- [ ] 选定 profile 的 display + body + data 三个字体角色都已映射，并有系统 fallback
- [ ] body 有噪声纹理叠层(`body::before`)
- [ ] `#deck` 横向 fixed flex,每个 `.slide` 是 100vw × 100vh
- [ ] 无页面纵向滚动条;F11 下页脚不遮挡正文
- [ ] 底部圆点、左右键、滚轮、触屏、ESC overview 可用
- [ ] 至少有一个 `.gradient-text` 锚点
- [ ] 至少 3 种 brand 色出现(不要单色到底)
- [ ] 数据使用 profile 的 data 字体和 tabular-nums；决定性大数字可使用 display 字体
- [ ] 至少 3 类不同图表表达家族;不要全 deck 都是 bar / proof-bars
- [ ] 选定一个明确 style profile；没有把所有 profile 同时混入一份 deck
- [ ] manifest 通过反重复验证；相邻构图、三页几何/tone run、卡片占比均合格
- [ ] overview/contact sheet 在不读文字时仍能看出清楚的节奏变化
- [ ] 主内容区不能过小:1920×1080 下 `.wrap/.frame` 可视宽度通常不低于 80%,常规投影页接近 88%
- [ ] 字号不能过小:常规页主标题不低于 78px,hero 标题不低于 110px,lead/subtitle 不低于 24px;只有 `.compact` 页例外
- [ ] 1920×1080 下 regular title median 接近 90-106px;`.dense-slide:not(.compact)` 不能用 78-85px 作为常态
- [ ] `.wrap` 不使用 `margin:auto auto 0` / `margin:auto`;这会和 footer auto margin 叠加造成内容沉底
- [ ] 独立 KPI 没被画成 proof-bars
- [ ] 时间窗口没被画成普通 bar chart
- [ ] 机制匹配没被画成条形图
- [ ] 移动断点处理 720px / 900px

---

## PPTX 模式工作流

### Step 1 · 读 references

- **`references/visual-grammar.md`** 必读 — PPTX 与 HTML 共用 manifest；不允许 PPTX 全部降级为 card grid。
- **`references/style-index.json`** 必读 — 只选择 `formats` 包含 `pptx` 的 profile。
- **`references/pptx-mode.md`** 必读 — PPT 输出模式的完整说明:design tokens 如何映射到 PPT 主题、组件如何用 shape 实现、哪些视觉特性降级、字体如何嵌入。
- **`references/chart-selection.md`** 必读 — PPTX 也必须先判断数据关系,不要默认 proof-bars。
- **`references/design-tokens.md`** — 共享的色板/字号 scale(直接复用)
- **`references/typography.md`** — 共享的字体规则(直接复用)

### Step 2 · 用 generate_pptx.py 生成

`assets/render_manifest.py` 是新 deck 的默认入口；`assets/generate_pptx.py` 提供兼容 API 和低层 python-pptx builder：

- `EditorialDeck` 类:封装好的 deck builder,自动应用色板/字体/版面
- 11 个 legacy slide 模板函数:`add_why_slide()`, `add_hero_slide()`, `add_evidence_slide()`, `add_architecture_slide()`, `add_workflow_slide()`, `add_coverage_slide()`, `add_relationship_slide()`, `add_proof_slide()`, `add_limitations_slide()`, `add_bonus_slide()`, `add_cta_slide()`
- 组件函数:`draw_stat_grid()`, `draw_decision_timeline()`, `draw_gene_drug_matrix()`, `draw_evidence_list()`, `draw_double_bar_chart()`, `draw_evidence_pyramid()`, `draw_phase_pill_row()`,...
- 用法:

```python
from generate_pptx import EditorialDeck

deck = EditorialDeck(
    industry="medical",
    style_profile=manifest["deck_profile"],
    manifest=manifest,
)
deck.add_hero_slide(
    eyebrow="HEMATOLOGY · IFI MARKET INTELLIGENCE · 2026",
    title_main="一句话起跑",
    title_accent="AI 编排 7 大血液疾病抗真菌药市场调研",
    sub="用户输入一句话疾病名 → 系统跑通 5 phase 流水线 → 4 件交付物",
    stats=[("38亿", "血液 IFI 总市场"), ("7", "Disease Modules"), ("22", "Engineered Charts"), ("43", "PMID Refs")]
)
deck.add_evidence_slide(
    eyebrow="EVIDENCE · TRACEABILITY",
    title="每一个数字都能回溯",
    funnel=[("PubMed 触达", "数千"), ("初筛", "~500"), ("纳入", "43")],
    pyramid=[("最高级", 18, "green"), ("重要级", 17, "blue"), ("参考级", 7, "gold")]
)
deck.save("output/blood_oncology_v5.pptx")
```

### Step 3 · 字体处理

PPT 不能像浏览器那样动态加载 web 字体。两条路:

**A. 字体嵌入(推荐 · Windows + 桌面 PowerPoint):**
```python
deck = EditorialDeck(embed_fonts=True)
```
要求 Fraunces、Inter、JetBrains Mono 已安装，且字体自身允许文档嵌入。生成器先用 `python-pptx` 写文件，再调用 `assets/embed_pptx_fonts.ps1` 让桌面 Microsoft PowerPoint 以 `EmbedFonts=true` 重新保存，并逐一比对请求字体、`ppt/fonts/` 与 `embeddedFontLst`。仅注册了兼容 COM 的 WPS Office 不满足此要求。如果 PowerPoint 不可用、字体未安装或字体授权禁止嵌入，任务必须失败并列出请求字体或缺失字体，不能静默声称已嵌入。

在非 Windows、没有桌面 PowerPoint或不需要嵌入时，使用 `embed_fonts=False` 和降级字体。

**B. 字体降级(共享/在线场景):**
- Fraunces → "Cambria"(Windows 自带) / "Times New Roman" 或客户机器装的衬线
- Inter → "Calibri"(Windows 自带) / "Segoe UI"
- JetBrains Mono → "Consolas"(Windows 自带)

降级会损失一点辨识度,但配色/版面/组件仍然 ~85% 还原。

### Step 4 · 视觉特性降级地图

| HTML 特性 | PPT 实现 | 保真度 |
|----------|---------|-------|
| profile 角色色 | `EditorialDeck(style_profile=...)` 映射到 PPT shape/theme 色 | 100% |
| profile cadence | 根据 manifest 切换页面 tone；不支持的暗色 profile 在规划阶段拒绝 | 90% |
| Fraunces / Inter / Mono | 嵌入字体或降级到 Cambria / Calibri / Consolas | 95% / 70% |
| 软阴影卡片 | shape 加 outer shadow + 圆角 12pt | 100% |
| 渐变文字 | text fill gradient 三色 stop | 100% |
| 噪声纹理 | slide background image fill 用 noise.png | 80% |
| 径向渐变光晕 | shape 径向渐变填充 alpha | 90% |
| 玻璃态 backdrop-filter | 半透明白色填充 + 软阴影 | 70% |
| Section navigation | PPT 没有滚动,改用 slide-jump hyperlinks | N/A |
| reveal 滚动动效 | 用 PPT 进入动画(渐入)等价 | 不同机制 |
| `clamp()` 响应式 | PPT 固定布局,16:9 1920×1080 设计 | N/A |

### PPTX 验证清单

- [ ] 主题色板覆盖 6 brand 色
- [ ] 标题用衬线字体(Fraunces 嵌入或 Cambria 降级)
- [ ] 数据用等宽字体(JetBrains Mono / Consolas)
- [ ] 至少 3 张 slide 用了不同 brand 色
- [ ] 至少 3 类不同图表表达,proof-bars 只用于同一指标比较
- [ ] `style_profile` 与 manifest 一致，且 profile 支持 PPTX
- [ ] manifest 通过构图、几何、tone 和卡片占比检查
- [ ] `render-report.json` 中 HTML/PPTX 的 slide IDs、composition IDs 与 manifest hash 一致
- [ ] PPTX shape region signatures 不少于 HTML 的语义构图种类，且至少有 3 种页面 background/tone 映射
- [ ] 不支持的 HTML 构图有记录明确的 PPTX 替代，而不是统一退化为卡片网格
- [ ] 每张 slide 都有 eyebrow tag(顶部小字)+ 大标题 + 主组件
- [ ] CTA slide 用赭石主色实心按钮形 shape
- [ ] 16:9 1920×1080 分辨率
- [ ] 请求字体嵌入时，`last_font_embedding_report.embedded == true`，且 .pptx 解压后存在 `ppt/fonts/` 和 `embeddedFontLst`

---

## 关键设计原则(两模通用,不要破坏)

1. **不要全部正文用 Fraunces** — 衬线长篇阅读疲劳
2. **不要把所有 deck 都锁定同一 palette** — 先选 profile，再按角色 token 和 cadence 用色
3. **不要把所有数字都画成条形图** — 图表先表达关系,再表达大小
4. **不要用纯黑文字** — 用 `#141413` 暖墨
5. **不要让每页/每屏背景一样** — 按选定 profile 的 cadence 形成对比节拍，不随机换色
6. **不要混用按钮风格** — 主 CTA 一种样式,辅 CTA 另一种,跳转第三种,不要乱
7. **不要把演讲 deck 做成网页报告** — 常规页必须采用 projection typography;放不下就拆页或 compact,不要全局缩字
8. **PPT 模式:不要在 PPT 里写 CSS** — 所有视觉走 python-pptx 的 shape API,不要嵌网页
9. **不要把组件数量当作视觉多样性** — 相同白卡、相同标题位置和相同网格，即使名字不同也属于重复
10. **不要用随机性掩盖重复** — 使用稳定 seed 和 novelty penalty；语义正确优先于新奇

## 常见任务模板

### 任务 A · "做一份 X 主题的 case sharing presentation"

→ HTML 模式 default → 选择 profile 与密度 → 生成 manifest → 拷贝行为 shell → 按构图语法渲染 → 反重复与视口 QA

### 任务 B · "做一份 X 主题的 PPT 给客户演示"

→ PPTX 模式 → 生成 manifest → 选择 PPTX-compatible profile → 用 `EditorialDeck(style_profile=..., manifest=...)` → 按语义构图生成 → save .pptx

### 任务 C · "把这份 HTML presentation 转成 PPT 版"

→ 解析 HTML 11 sections → 每节调用对应 add_*_slide() → 字体降级 / 嵌入选一 → save

### 任务 D · "我要 HTML 和 PPT 都要,内容一致"

→ 同一份内容数据先抽成 JSON / dict → 生成一次 manifest → HTML 与 PPTX 分别渲染 → 记录格式替代并分别 QA

## 为什么这个 skill 重要

原始 Pfizer deck 证明了 warm editorial DNA 的可用性；本 skill 把它从一个固定成品扩展为可选择、可复现和可审计的设计系统。复用它意味着：

- 每次做 presentation 不必从零定义设计规则，但也不会自动得到同一套配色和卡片
- HTML / PPT 双格式无缝切换,保持视觉一致
- 跨项目沉淀视觉资产，同时让不同受众和内容拥有可辨识的 deck identity
- 客户/老板第一眼会觉得"这是花了心思的",而不是"模板套出来的"

源版本参考:血液科市场调研 v5 desktop deck。
