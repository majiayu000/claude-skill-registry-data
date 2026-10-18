---
name: maestrwave-ui-system
description: 当使用者说"用 MaestrWave 那套 UI"、"新项目的界面照着 MaestrWave 做"、"用我之前那套暗色衬线的风格"、"把这个项目的样式统一成我常用的那套"时使用。直接套用一套现成的深色衬线视觉系统：暖炭黑底 + 浅水蓝主色、Source Serif 4 配 Noto Serif SC、巨大标题配 11px 小标签的尺度对比，附可直接粘贴的 global.css 与组件层 CSS。先铺 token 再拼组件，颜色只从 token 出。不复用 MaestrWave 的 logo 和图标，那是品牌资产。
category: coding-helper/ui-design
version: 0.1.1
status: draft
priority: P0
compatible_agents:
  - claude-code
  - cursor
  - codebuddy
  - generic-llm-agent
display_name: 套用 MaestrWave 那套界面
outputs:
  - chat
max_rounds: 20
suggest_hint: 新项目要起前端？用「套用 MaestrWave 那套界面」把现成的暗色衬线系统铺上去
---

# 套用 MaestrWave 那套界面 / MaestrWave UI System

一套现成的深色衬线视觉系统，从 MaestrWave 前端提取出来，可以直接铺到新项目上。

**这套系统长什么样**：暖炭黑基底（不是纯黑）+ 浅水蓝主色 + 酒红状态色；
全站衬线体（拉丁 Source Serif 4 / 中文 Noto Serif SC）；
`clamp(40px,6vw,64px)` 的巨大标题配 11px 全大写小标签；
层级靠明度台阶而非阴影；无 UI 框架，组件全是自己的 CSS。

## 何时使用 / When to use

- 新项目起前端，想直接用这套已经打磨过的视觉，不重新设计
- 已有项目的样式散乱，要统一到这套上
- 要给这套系统加一个新组件，希望和已有的对得上

**不适用于** / Not for：

- 想给项目定一套**自己的**视觉语言 → 用 `ui-design-system-builder`，那是从项目意象推 token 的流程
- 要浅色界面 → 这套只有暗色（`color-scheme: dark`），直接反色会毁掉整个明度台阶
- 项目已有设计规范或品牌色 → 照那个做，不要覆盖

## 这套系统的三条硬规则

违反任何一条，铺出来的界面就不是这套了：

1. **颜色只从 token 出**。CSS 里出现 `#` 开头的字面量（除了装饰层的渐变 stop），
   就是漏了。文字层级用 `color-mix(in srgb, var(--ink) N%, transparent)`，不新造灰色变量。
2. **字号只用已有的五档**（`display-1` / `display-2` / body 14px / 12px label / 11px eyebrow）。
   中间加档会把标题与标签的尺度对比磨平，那个对比是这套系统的性格所在。
   按钮、输入框、侧栏、计时器这些控件里的字也落在这五档上，不另起 13px、13.5px 这类半档；
   控件之间的主次靠第 3 条的手法，不靠字号。
3. **层级换手法，不是调强度**。一级导航用描边+微亮底，二级用实心高亮；
   主切换用实色分段控件，次级用无底小按钮。两级同手法会让视线分不出主次。

## 流程 / Process

### 1. 装字体，铺 global 层

```bash
npm i @fontsource/source-serif-4 @fontsource/noto-serif-sc
```

把 `assets/global.css` 复制到 `src/styles/global.css`，在入口 import 一次。
这一层给你：字体引入、`:root` token、六个排版类（`.display-1` `.display-2`
`.eyebrow` `.label` `.mono-chip` `.field-label`）、表单基础样式、统一焦点态、
`prefers-reduced-motion`、滚动条。

**界面以中文为主时不要删掉 CJK 那两行 import** —— 只引拉丁字体的话中文会掉到系统黑体，
一衬线一无衬线，界面立刻割裂。

### 2. 决定要不要换主色

和音频/水无关的项目通常要换。**只动 `--accent` / `--accent-dim` / `--wave-*` 三处**，
底色和 `--ink` 是一套暖调，成组替换或者不动 —— 只把 `--bg` 改成纯黑会让所有颜色发脏。

换色的三条约束（够亮、偏冷、别动 `--wine`）见 `references/recipes.md` 末节。

### 3. 铺组件层

`assets/components.css` 里已有：按钮三变体 + 圆形主操作、页头与页面容器、卡片与浮层、
分段控件 / 次级切换 / 标签页、两级侧栏、状态点与进行中呼吸、空状态、表单行、手机端外壳。

两种用法：直接当普通类引入，或按组件拆进各自的 `*.module.css`（MaestrWave 本体是后者）。
**加新类之前先在这份文件里找一遍**，需要的东西多半已经在了。

### 4. 拼页面

每个页面都是同一个骨架：

```tsx
<PageHeader eyebrow="栏目名" title="这一页是什么" meta={<span className="mono-chip">…</span>} />
<div className="page-body">
  <section className="card">…</section>
</div>
```

具体组件的实现（Button / PageHeader / 装饰波浪层 / 两级侧栏 / 状态显示 /
canvas 里怎么用 token / 图标怎么画）读 `references/recipes.md`，不要凭印象写。

### 5. 铺完自查

- [ ] 全项目搜 `#` 开头的颜色字面量，只剩装饰层渐变
- [ ] 没有新增字号档位：搜 `font-size`，取值只有 `.display-1` / `.display-2` 的 clamp 和 14 / 12 / 11px
      （自带的两份 CSS 就是这样），标题仍然是 `.display-1`
- [ ] 焦点态没被 `outline: none` 干掉
- [ ] 数字（时间码、计数、图表刻度）都有 `tabular-nums`
- [ ] canvas / SVG 里的字体和颜色是从 computed style 读的，不是抄的字面量
- [ ] 除了"进行中"的呼吸，没有别的循环动画

## 输出格式 / Output

铺完之后报三件事，别贴整份 CSS：

```markdown
**已铺**：<哪些文件、哪些页面>
**换了的 token**：<改了哪几支、为什么>
**还缺的组件**：<这套里没有、这个项目需要的，以及建议怎么加>
```

## 边界 / Boundaries

- **不复用 MaestrWave 的 logo 和图标**。字标（斜切 M/W 折线）和那套领域图标是品牌资产，
  新项目要自己画。图标的**规格**可以照抄（20x20、1.6 描边、`currentColor`），图形不行。
- **不引 UI 框架**。这套系统的前提就是组件全部自持。装 Tailwind / MUI 之后
  token 会和框架的默认值打架，两边都不干净。
- **不做浅色反色版**。明度台阶（`bg → surface → surface-2 → surface-3`）在浅色下不成立，
  真要浅色是另起一套的工作量，如实说。
- **不改业务逻辑**。只动样式、类名和纯展示结构；发现逻辑问题说出来，别顺手改。
- **不一次铺完全站**。先在一个页面上跑起来看过，再铺开。
- **不为了统一而降低可读性**。正文对比度、42px 触摸目标、可见焦点态没有商量余地。

## Token 控制 / Token discipline

- `assets/global.css` 是复制过去的，不需要读进上下文再改；要改就直接编辑目标文件
- `references/recipes.md` 按需读，落地哪个组件读哪一节
- 自查用 grep（搜 `#` 颜色字面量、搜 `font-size`、搜 `outline: none`），不要通读所有 CSS

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 自带 CSS 的 7 处档外字号收回五档（14.5/13.5/13/15→14px，11.5/13→12px，10.5→11px），按钮改为继承字号，去掉浏览器默认的 13.33px；`.field-label` 由 ink 48% 提到 52%，在三层底色上对比度 5.00/4.84/4.59，过 AA 4.5:1；「五个排版类」改为六个；字号自查改成 grep 核对 | patch |
| 0.1.0 | 2026-08-10 | 初始草稿，从 MaestrWave 前端提取 | minor |
