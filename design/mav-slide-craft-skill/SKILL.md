---
name: mav-slidecraft-skill
description: Create stunning, animation-rich HTML presentations from scratch or by converting PowerPoint files. Use when the user wants to build a presentation, convert a PPT/PPTX to web, or create slides for a talk/pitch.
---

# mav-slidecraft-skill

Create zero-dependency, animation-rich HTML presentations that run entirely in the browser.

**版本**：3.0（SlideCraft × Guizang 升级）

---

## Core Principles

1. **Zero Dependencies** — Single HTML files with inline CSS/JS. No npm, no build tools.
2. **Show, Don't Tell** — Generate visual previews, not abstract choices.
3. **Distinctive Design** — No generic "AI slop." Every presentation must feel custom-crafted.
4. **Viewport Fitting (NON-NEGOTIABLE)** — Every slide MUST fit exactly within 100vh. No scrolling within slides.
5. **Font-First & Texture-First** — Use highly distinctive Display fonts + real scanned textures; never default to Inter/Space Grotesk/Nunito/Orbitron as Display.
6. **Color Restraint** — No pure RGB primaries (`#FF0000`, `#0000FF`, `#00FF00`) as main colors; all key colors must be muted or pigment-like.
7. **Motion Restraint** — Animations 200–600 ms by default; support `prefers-reduced-motion` and manual `B` low-power mode.
8. **Horizontal Optional** — Default remains vertical scroll-snap; enable horizontal deck via `data-deck="horizontal"` only when requested.
9. **Layout Catalog First** — Use standardized layouts from `references/layout-catalog.md` instead of inventing structures.
10. **Theme Rhythm** — Every slide carries `light` / `dark` / `hero light` / `hero dark`; no more than 2 consecutive same themes.

详细设计指南参见 [references/design-principles.md](references/design-principles.md)

---

## Viewport Fitting Rules

- Every `.slide` must have `height: 100vh; height: 100dvh; overflow: hidden;`
- ALL sizes use `clamp(min, preferred, max)` — never fixed px/rem
- Content Density: Title (1 heading + 1 subtitle), Content (4-6 bullets), Grid (6 cards max)
- Images: prefer `.frame-img.r-*` standard ratios with `max-height` constraints
- Include `prefers-reduced-motion` support and `B` key low-power toggle

**详细规范参见 [references/viewport-base.css](references/viewport-base.css)**

---

## Phase 0: Detect Mode

- **Mode A: New Presentation** — Create from scratch. Go to Phase 1.
- **Mode B: PPT Conversion** — Convert a .pptx file. Go to Phase 4.
- **Mode C: Enhancement** — Improve existing HTML. Read, understand, enhance.

### Mode C Rules

1. Before adding content: Check against density limits
2. Adding images: Must use `.frame-img.r-*` standard ratios. Split slide if full
3. Adding text: Max 4-6 bullets. Split if exceeds
4. After modification: Verify `overflow: hidden`, `clamp()` usage, viewport max-height
5. If adding horizontal mode: add `data-deck="horizontal"` and update `#deck` structure

---

## Phase 1: Content Discovery

**Ask ALL questions in a single AskUserQuestion call:**

| Header | Question | Options |
|--------|----------|---------|
| Purpose | What is this presentation for? | Pitch deck / Teaching-Tutorial / Conference talk / Internal |
| Length | Approximately how many slides? | Short 5-10 / Medium 10-20 / Long 20+ |
| Content | Do you have content ready? | All ready / Rough notes / Topic only |
| Editing | Need browser editing? | Yes (Recommended) / No |
| Direction | Horizontal swipe deck? | Yes / No (default vertical) |

Remember the editing choice — determines if edit-related code is included in Phase 3.

### Step 1.2: Image Evaluation (if images provided)

1. Scan — List all image files
2. View each — Use Read tool (multimodal)
3. Evaluate — USABLE or NOT, concept, colors
4. Co-design outline — Design around images + text together
5. Confirm — AskUserQuestion: "Does this outline look right?"

---

## Phase 2: Style Discovery

### Step 2.1: Style Selection

**直接输出以下风格组合列表，让用户回复序号或名称：**

```
请选择视觉风格组合（回复序号或名称）：
1. 数字粗野建筑 Neo-Brutalism + 3D — 粗犷几何+立体深度+真实混凝土纹理 | 最适合：创意机构、Web3、科技初创
2. 80年代未来 Retro-Futurism — 霓虹渐变+复古科技感+CRT 磷光点阵 | 最适合：科技发布会、游戏、音乐娱乐
3. 极繁实验 Maximalism + Typography — 大胆混搭+编辑网格+拼贴纹理 | 最适合：创意机构、音乐艺术、时尚品牌
4. 天真实验 Naive + Typography — 手绘质感+Rough 风边框+贴纸拼贴 | 最适合：教育、儿童产品、手工品牌
5. 高端 SaaS Bento + 3D + Liquid Glass — 卡片布局+磨砂亚克力+三套行业色板 | 最适合：SaaS产品、数据仪表板、产品展示
6. 新极简温暖 Neo-Minimalism — 克制留白+真实颗粒+陶土粉点缀 | 最适合：高端品牌、奢侈品、科技公司
7. 孟菲斯派对 Memphis — 真实孟菲斯色板+几何图案+层压板纹理 | 最适合：创业公司、潮流品牌、教育产品、社区平台
8. 蓝图设计 Blueprint — 工程图纸+标注系统+等轴测投影 | 最适合：建筑/工程、技术分享、产品设计
9. 编辑杂志 Editorial Magazine — 大号衬线+强留白+出血大图+专栏网格 | 最适合：品牌故事、品牌发布会、设计作品集
10. 深色学院 Dark Academia — 深棕皮革+羊皮纸文字+烫金点缀+首字下沉 | 最适合：知识型演讲、历史文化、深度研究
11. 侘寂科技 Wabi-Sabi Tech — 大量留白+和纸纹理+竖排装饰+东方科技美学 | 最适合：人文关怀科技、可持续设计、东方美学
```

**风格组合公式**: A类(主风格) + B类(维度增强) + C类(质感滤镜) — 每个组合包包含完整的设计系统、配色方案、字体搭配和动画预设。

### Step 2.2: Load Style Reference

用户选择后，加载对应的 reference 文件：

| 序号 | 风格组合 | Reference 文件 |
|------|----------|----------------|
| 1 | 数字粗野建筑 | [references/combo-1-neo-brutalism-3d.md](references/combo-1-neo-brutalism-3d.md) |
| 2 | 80年代未来 | [references/combo-2-retro-futurism.md](references/combo-2-retro-futurism.md) |
| 3 | 极繁实验 | [references/combo-3-maximalism-typography.md](references/combo-3-maximalism-typography.md) |
| 4 | 天真实验 | [references/combo-4-naive-typography.md](references/combo-4-naive-typography.md) |
| 5 | 高端SaaS | [references/combo-5-bento-3d-glass.md](references/combo-5-bento-3d-glass.md) |
| 6 | 新极简温暖 | [references/combo-6-neo-minimalism.md](references/combo-6-neo-minimalism.md) |
| 7 | 孟菲斯派对 | [references/combo-7-memphis.md](references/combo-7-memphis.md) |
| 8 | 蓝图设计 | [references/combo-8-blueprint.md](references/combo-8-blueprint.md) |
| 9 | 编辑杂志 | [references/combo-9-editorial-magazine.md](references/combo-9-editorial-magazine.md) |
| 10 | 深色学院 | [references/combo-10-dark-academia.md](references/combo-10-dark-academia.md) |
| 11 | 侘寂科技 | [references/combo-11-wabi-sabi-tech.md](references/combo-11-wabi-sabi-tech.md) |

**同时加载共享底层文件**：
- [references/viewport-base.css](references/viewport-base.css) — 强制响应式 CSS、统一排版类、图片系统
- [references/html-template.md](references/html-template.md) — HTML 结构、SlidePresentation 类、WebGL、动画 recipe
- [references/animation-patterns.md](references/animation-patterns.md) — 动画配方系统
- [references/theme-rhythm.md](references/theme-rhythm.md) — 主题节奏规范
- [references/layout-catalog.md](references/layout-catalog.md) — 标准布局骨架 L01-L09
- [references/checklist.md](references/checklist.md) — 质量检查清单

**同时加载 Delight Library**（为选定风格增加微交互趣味性）：
- [references/delight-library/delight-library.md](references/delight-library/delight-library.md) — 45种微交互机制（每个风格组合5个专属机制）
- [references/delight-library/usage-system.md](references/delight-library/usage-system.md) — 选择规则与约束（每实现随机选择3个）

**同时加载纹理资源**：
- [references/textures.css](references/textures.css) — 6 种真实扫描纹理的 base64 data-uri（paper / concrete / grain / leather / washi / film），生成 HTML 时内联到对应风格的 `:root` 中。

---

## Phase 3: Generate Presentation

### Step 3.0: Plan Theme Rhythm

在写任何 HTML 之前，先列出每一页的主题与布局：

```markdown
| 页 | 主题 | 布局 | 备注 |
|---|---|---|---|
| 1 | hero dark | L01 | 封面 |
| 2 | light | L03 | 数据 |
| 3 | dark | L04 | 故事 |
```

规则：
- 每页必须有 `light` / `dark` / `hero light` / `hero dark` 之一
- 禁止连续 3 页同主题
- 8 页以上必须有至少 1 个 `hero dark` 和 1 个 `hero light`
- 每 3-4 页插入 1 个 hero 页

### Step 3.1: Image Requirement Check

Ask (header: "配图"): 是否需要为演示文稿添加配图？
- 不需要配图 — 纯 CSS 视觉效果，跳到 Step 3.3
- 我有配图 — 用户自行准备图片，继续 Step 3.2

### Step 3.2: User Image Guide (仅当选择"我有配图"时)

**引导用户放置图片**：

```
📁 请将图片放到与 HTML 同目录的 images/ 文件夹：

{presentation-name}/
├── index.html（即将生成）
└── images/
    ├── bg-1.png
    ├── hero.png
    └── ...

建议命名规则：
- 背景图：bg-1.png, bg-2.png ...
- Hero 图：hero.png, hero-2.png ...
- 其他图片：使用有意义的名称，并匹配落位比例

标准比例建议：
- 主视觉 / S22: 21:9
- 左文右图: 16:10 或 4:3
- 图片网格: 统一高度 h-24 / h-28
- 小插图: 3:2 或 1:1

放置完成后回复「已就绪」。
```

**用户确认后，进入 Phase 2.5。**

---

## Phase 2.5: Content Preview

生成 ASCII 预览让用户审核（如果用户有配图，预览中包含图片占位符）：

```
╔══════════════════════════════════════════════════════════════╗
║  SLIDE 1: [幻灯片标题]                                         ║
║  ─────────────────────────────────────────                   ║
║  [副标题/说明文字]                                             ║
║  [IMAGE: hero.png] ← 如果用户有配图                           ║
╚══════════════════════════════════════════════════════════════╝
```

Ask (header: "内容预览"): 是否需要调整？ Options: 确认生成 / 修改文字

---

### Step 3.3: Generate HTML

**Before generating, read:**
- [references/html-template.md](references/html-template.md) — HTML architecture and JS features
- [references/viewport-base.css](references/viewport-base.css) — Mandatory CSS (include in full)
- [references/animation-patterns.md](references/animation-patterns.md) — Animation recipes
- [references/theme-rhythm.md](references/theme-rhythm.md) — Theme rules
- [references/layout-catalog.md](references/layout-catalog.md) — Layout skeletons
- [references/textures.css](references/textures.css) — Real scanned texture base64 data-uris
- 风格 reference 文件：`references/[风格名].md`
- **Delight Library**: [references/delight-library/delight-library.md](references/delight-library/delight-library.md)

**质感与字体升级说明（CRITICAL）**：
1. **必须使用**风格 reference 中指定的 Display + Body 字体，并提供 Google Fonts 降级。
2. **必须使用真实纹理**：从 `references/textures.css` 复制对应 base64 变量到生成的 HTML `:root` 中，每页 slide 添加 `<div class="texture-overlay" aria-hidden="true"></div>`。
3. **禁止**使用 SVG `feTurbulence` 作为主要纹理；仅允许作为辅助 SVG 滤镜（如 Rough 风位移）。
4. **主色必须降调**：无纯 RGB 主色。
5. **动画克制**：默认 200-600 ms；所有动画提供 `prefers-reduced-motion` 降级和 `B` 键低功耗。
6. **中西文混排**：内容容器使用 `.mixed-text` 类。
7. **焦点控制**：每页仅 1 个视觉锚点；标题与正文字号比 ≥ 5:1。
8. **统一排版层级**：使用 `.kicker`、`.h-hero`、`.h-xl`、`.lead`、`.body`、`.meta-row`、`.big-num`、`.frame-img`。
9. **布局目录优先**：从 `references/layout-catalog.md` 选择 L01-L09，标注 `data-layout`。
10. **主题节奏**：每页标注 `light` / `dark` / `hero light` / `hero dark`，遵守不连续 3 页同主题。

**Delight Mechanism Selection (IMPORTANT):**
根据选定风格，从 Delight Library 中选择 **3 个微交互机制** 加入 HTML：
1. 参考 [usage-system.md](references/delight-library/usage-system.md) 的选择规则
2. 确保交互类型多样性（至少 1 hover + 1 非 hover）
3. 避免交互冲突（同一元素不绑定多个相同触发器）
4. 实现 `prefers-reduced-motion` 支持

**Key requirements:**
- Single self-contained HTML file, all CSS/JS inline
- Include FULL contents of viewport-base.css
- Use fonts from Fontshare or Google Fonts — never system fonts as Display
- Add clear section comments: `/* === SECTION NAME === */`
- 风格一致性：CSS 变量、字体、动画与选定风格 reference 一致
- **趣味性**：融入 3 个 Delight Mechanisms，增强交互体验
- **CRITICAL - 内容自适应**：SlidePresentation 类必须包含 `fitSlideContent()` 方法

**图片引用（如果用户提供了配图）**：
- 使用相对路径：`images/{filename}`
- 背景图：`background-image: url('images/bg-1.png')`
- 内容图片：`<img src="images/hero.png" alt="描述">`
- 确保 HTML 文件与 images/ 目录同级
- 使用 `.frame-img.r-*` 或 `.frame-img.h-*` 标准比例

---

## Phase 4: PPT Conversion

1. **Extract** — `python scripts/extract-pptx.py <input.pptx> <output_dir>` (install: `pip install python-pptx`)
2. **Confirm** — Present extracted slide titles, content, image counts
3. **Style** — Go to Phase 2
4. **Generate** — Convert to chosen style, preserve text, images, order, notes

---

## Phase 5: Delivery

1. **Validate** — Run `node scripts/validate-deck.mjs [filename].html`
2. **Checklist** — Verify against [references/checklist.md](references/checklist.md) P0 items
3. **Clean up** — Delete `.claude-design/slide-previews/` if exists
4. **Open** — `open [filename].html`
5. **Summarize** — File location, style name, slide count, navigation (Arrow keys/Space/click/B for low power), customization (`:root` variables)

---

## Phase 6: Share & Export (Optional)

Ask: "Would you like to share this? I can deploy to URL or export PDF."

Options: Deploy to URL / Export to PDF / Both / No thanks

### 6A: Deploy to URL (Vercel)

1. Check Vercel CLI: `npx vercel --version`
2. Login: `npx vercel login` (首次需要账号)
3. Deploy: `bash scripts/deploy.sh <path-to-presentation>`

**注意**: 本地图片必须与 HTML 同目录；文件名避免空格；重新部署更新同一 URL

### 6B: Export to PDF

```bash
bash scripts/export-pdf.sh <path-to-html> [output.pdf]
```

**注意**: 首次运行安装 Playwright (~150MB)；Slides 必须用 `class="slide"`; 大文件加 `--compact`

---

## Supporting Files
| File | Purpose | When |
|------|---------|------|
| [references/design-principles.md](references/design-principles.md) | 设计铁律与通用规范 | Phase 2 & 3 |
| [references/html-template.md](references/html-template.md) | HTML 结构、JS、编辑、混排、纹理、动画降级、WebGL | Phase 3 |
| [references/viewport-base.css](references/viewport-base.css) | 响应式 CSS、统一排版类、图片系统、横向模式 | Phase 3 |
| [references/animation-patterns.md](references/animation-patterns.md) | 动画配方系统 | Phase 3 |
| [references/theme-rhythm.md](references/theme-rhythm.md) | 主题节奏规范 | Phase 3 |
| [references/layout-catalog.md](references/layout-catalog.md) | 标准布局骨架 L01-L09 | Phase 3 |
| [references/checklist.md](references/checklist.md) | P0/P1/P2/P3 质量检查清单 | Phase 5 |
| [references/textures.css](references/textures.css) | 6 种真实扫描纹理 base64 | Phase 2 & 3 |
| [references/combo-1-neo-brutalism-3d.md](references/combo-1-neo-brutalism-3d.md) | 数字粗野建筑风格 | Phase 2 |
| [references/combo-2-retro-futurism.md](references/combo-2-retro-futurism.md) | 80年代未来风格 | Phase 2 |
| [references/combo-3-maximalism-typography.md](references/combo-3-maximalism-typography.md) | 极繁实验风格 | Phase 2 |
| [references/combo-4-naive-typography.md](references/combo-4-naive-typography.md) | 天真实验风格 | Phase 2 |
| [references/combo-5-bento-3d-glass.md](references/combo-5-bento-3d-glass.md) | 高端SaaS风格 | Phase 2 |
| [references/combo-6-neo-minimalism.md](references/combo-6-neo-minimalism.md) | 新极简温暖风格 | Phase 2 |
| [references/combo-7-memphis.md](references/combo-7-memphis.md) | 孟菲斯派对风格 | Phase 2 |
| [references/combo-8-blueprint.md](references/combo-8-blueprint.md) | 蓝图风格 | Phase 2 |
| [references/combo-9-editorial-magazine.md](references/combo-9-editorial-magazine.md) | 编辑杂志风格（Guizang 试点） | Phase 2 |
| [references/combo-10-dark-academia.md](references/combo-10-dark-academia.md) | 深色学院风格 | Phase 2 |
| [references/combo-11-wabi-sabi-tech.md](references/combo-11-wabi-sabi-tech.md) | 侘寂科技风格 | Phase 2 |
| [references/delight-library/delight-library.md](references/delight-library/delight-library.md) | 45种微交互机制 | Phase 2 & 3 |
| [references/delight-library/usage-system.md](references/delight-library/usage-system.md) | 微交互选择规则 | Phase 2 & 3 |
| [scripts/validate-deck.mjs](scripts/validate-deck.mjs) | 静态校验脚本 | Phase 5 |
| [scripts/README.md](scripts/README.md) | PPT/部署/导出 | Phase 4 & 6 |

**全部 11 个风格组合包已实现，并新增横向模式 / WebGL / 布局目录 / 主题节奏 / QA 工具**
