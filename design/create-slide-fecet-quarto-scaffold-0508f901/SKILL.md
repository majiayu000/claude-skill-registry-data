---
name: create-slide
description: >
  fluid-slide 项目专用的幻灯片制作规范。
  定义了 Grid 布局、MD3 工具类、特殊组件等项目内约定。
  配合 quarto-revealjs 技能使用。
---

## Purpose

本技能为 fluid-slide 项目提供专用的幻灯片编写规范。涵盖：
- 自定义 Grid 布局系统
- Material Design 3 工具类
- 特殊组件（Timeline、Masonry、LeaderLine）
- 文件结构约定

## Syntax Preference

**优先使用 Pandoc bracketed spans 语法**，避免手写 HTML：

| 避免 | 推荐 |
|------|------|
| `<span class="foo">text</span>` | `[text]{.foo}` |
| `<span id="bar">text</span>` | `[text]{#bar}` |
| `<div class="foo">...</div>` | `::: {.foo}`...`:::` |

Bracketed spans 语法更简洁，且与 Pandoc/Quarto 生态一致。

## When to Use

在本项目中制作或修改幻灯片时使用此技能。

**Do NOT use when:**
- 需要 Quarto/Reveal.js 通用知识（使用 `quarto-revealjs` 技能）
- 非本项目的演示文稿

## Relationship with quarto-revealjs

| 技能 | 职责 |
|------|------|
| `quarto-revealjs` | Quarto/Reveal.js 通用知识（YAML、SCSS、扩展） |
| `create-slide` | 本项目特定约定（Grid 系统、MD3 类、组件） |

## File Structure

```
deck.qmd                 # 主文件：标题 + include
slides/
  [slide-name]/
    index.md             # 幻灯片内容（不含 ## 标题）
    assets/              # 资源文件（SVG、图片、视频）
```

**deck.qmd 结构**：
```markdown
## 标题文字 {background-color="#fff"}

```{=comment}
演讲者注释
```

{{< include slides/slide-name/index.md >}}
```

**资源引用**：`assets/filename.ext`（会被同步到根目录）

---

## Grid Layout System

### Basic Grid

```markdown
::: {.grid cols="1fr 1fr" gap="2em"}
::: {.slot}
左侧内容
:::
::: {.slot}
右侧内容
:::
:::
```

### Parameters

| 参数 | 说明 | 示例 |
|------|------|------|
| `cols` | 列定义 | `1fr 2fr`, `1fr 1fr 1fr` |
| `rows` | 行定义 | `auto 1fr`, `1fr 1fr` |
| `gap` | 间距 | `1em`, `0.5em 1em` |

### Spanning

| 类 | 效果 |
|----|------|
| `.span-2`, `.span-3` | 跨 2/3 列 |
| `.row-span-2`, `.row-span-3` | 跨 2/3 行 |

**显式定位**：
```markdown
::: {.slot style="grid-row: 3 / 5; grid-column: 3;"}
跨第3-4行，第3列
:::
```

### Incremental Display

```markdown
::: {.grid .incremental cols="1fr 2fr 2fr" gap="0.5em"}

::: {.slot .nonincremental style="font-weight: 600; border-bottom: 2px solid var(--md3-outline-variant);"}
Header（不参与增量）
:::

::: {.slot}
Content（增量显示）
:::

:::
```

---

## MD3 Utility Classes

### Colors

| 类 | 用途 |
|----|------|
| `.color-primary` | 主色（蓝） |
| `.color-error` | 强调/错误（红） |
| `.color-warning` | 警告（黄） |
| `.color-success` | 成功（绿） |
| `.color-muted` | 次要文字 |

**行内使用**：
```markdown
[关键词]{.color-primary}
[警告]{.color-error}
```

### Surfaces

| 类 | 深度 |
|----|------|
| `.surface-lowest` | 最浅 |
| `.surface-low` | 浅 |
| `.surface` | 默认 |
| `.surface-high` | 深 |
| `.surface-highest` | 最深 |

### Shapes

| 类 | 圆角 |
|----|------|
| `.rounded-xs` | 4px |
| `.rounded-sm` | 8px |
| `.rounded-md` | 12px |
| `.rounded-lg` | 16px |
| `.rounded-xl` | 28px |
| `.rounded-full` | 圆形 |

### Elevation

`.elevation-0` 到 `.elevation-5`

### Card Pattern

```markdown
::: {.surface-low .rounded-md style="padding: 1.2em;"}
**Title**

Content here
:::
```

---

## Special Components

### Timeline

```markdown
::::: {.grid rows="4fr 1fr" gap="0.2em"}
:::: {.timeline}

::: {.timeline-item}
::: {.content}
[**2017**]{.color-primary} · 标题

描述文字^[脚注]
:::
:::

::: {.timeline-item}
::: {.content}
[**2019**]{.color-primary} · 标题

描述文字
:::
:::

::::
:::::
```

### Masonry

```markdown
::::: {.masonry data-columns="2"}

![](assets/img1.jpg)

![](assets/img2.jpg)

![](assets/img3.jpg)

:::::
```

### LeaderLine (Animated Connectors)

```markdown
[起点文字]{#cycle-top}
[终点文字]{#cycle-bottom}

[]{.leaderline start="#cycle-bottom" end="#cycle-top" color="#f9a825" path="arc" start-socket="left" end-socket="left" size="2"}
[]{.leaderline start="#cycle-top" end="#cycle-bottom" color="#f9a825" path="arc" start-socket="right" end-socket="right" size="2"}
```

### Demo Highlight (Video Border)

```markdown
![](assets/video.mp4){.demo-highlight autoplay="true" muted="true" loop="true"}
```

### Callout

```markdown
::: {.callout-warning}
**结论**：警告内容
:::
```

---

## Media

### Video

```markdown
![](assets/demo.mp4){autoplay="true" muted="true" loop="true"}
```

**带高亮边框**：
```markdown
![](assets/demo.mp4){.demo-highlight autoplay="true" muted="true" loop="true"}
```

### Image

```markdown
![](assets/diagram.svg){fig-align="center" style="max-height: 320px;"}
![](assets/photo.png){width="80%"}
```

### FontAwesome Icons

```markdown
{{< fa icon-name >}}
{{< fa circle-check >}}
{{< fa circle-xmark >}}
{{< fa brands github >}}
```

带样式：
```markdown
[{{< fa circle-check >}}]{style="font-size: 2.5em; color: #4CAF50;"}
```

---

## Text Styling

### Inline Highlighting

```markdown
[强调文字]{.color-primary}
[错误/重要]{.color-error}
[警告]{.color-warning}
```

### Explicit Font Size

```markdown
[小字]{style="font-size: 0.8em;"}
[大字]{style="font-size: 1.2em;"}
```

**禁止使用** Quarto 的 `.smaller` 类，使用显式 `style="font-size: ..."`

### Fit Text

```markdown
::: {.r-fit-text}
自动缩放的大标题
:::
```

### Fragment (Animation)

```markdown
::: {.fragment}
渐显内容
:::

::: {.r-fit-text .fragment}
渐显的大标题
:::
```

---

## Footnotes

### Inline Footnote

```markdown
文字内容^[脚注说明]
```

### Referenced Footnote

```markdown
文字内容[^ref-id]

[^ref-id]: 脚注定义，可以包含 [链接](url)
```

---

## Complete Examples

### Example 1: Two-Column Comparison

```markdown
::: {.grid cols="1fr 1fr" gap="2em"}

::: {.slot}
**数字世界**

![](assets/chart.svg){fig-align="center" style="max-height: 320px;"}

[基准测试快速被解决]{style="font-size: 0.8em;"}
:::

::: {.slot style="text-align: center;"}
**物理世界**

::: {.grid cols="auto auto" gap="0.3em" style="justify-content: center;"}
![](assets/robot.png){style="max-height: 300px;"}
[{{< fa circle-xmark >}}]{style="font-size: 2.5em; color: #f44336;"}
:::

[简单任务依然困难]{style="font-size: 0.9em;"}
:::

:::
```

### Example 2: Comparison Table with Headers

```markdown
::: {.grid .incremental cols="1fr 2fr 2fr" gap="0.5em" style="font-size: 0.95em;"}

::: {.slot .nonincremental style="font-weight: 600; border-bottom: 2px solid var(--md3-outline-variant); padding-bottom: 0.3em;"}
维度
:::
::: {.slot .nonincremental style="font-weight: 600; border-bottom: 2px solid var(--md3-outline-variant); padding-bottom: 0.3em;"}
Code Agent
:::
::: {.slot .nonincremental style="font-weight: 600; border-bottom: 2px solid var(--md3-outline-variant); padding-bottom: 0.3em;"}
Embodied Agent
:::

::: {.slot .nonincremental}
**适用范围**
:::
::: {.slot}
在主流技术栈中表现亮眼
:::
::: {.slot}
在实验室场景中成功率很高
:::

:::
```

### Example 3: Quote Cards Grid

```markdown
:::: {.grid cols="1fr 1fr 1fr" gap="0.2em"}

::: {.slot}
::: {.surface-low .rounded-md style="padding: 1.2em; height: 100%;"}

[路径不明]{.color-primary} · ![](assets/icon.svg){width="28px" style="vertical-align: middle;"}

**Expert Name**

> Quote text [highlighted]{.color-error}^[Reference]

:::
:::

::::
```

### Example 4: Video Demo Grid

```markdown
:::: {.grid cols="1fr 1fr 2fr" rows="1fr 1fr 1fr 1fr" gap="0.5em"}

::: {.slot .row-span-3}
![](assets/demo1.mp4){.demo-highlight autoplay="true" muted="true" loop="true"}
:::

::: {.slot .row-span-3}
![](assets/demo2.mp4){autoplay="true" muted="true" loop="true"}
:::

::: {.slot .row-span-2}
![](assets/demo3.mp4){.demo-highlight autoplay="true" muted="true" loop="true"}
:::

::: {.slot style="grid-row: 3 / 5; grid-column: 3;"}
![](assets/demo4.mp4){.demo-highlight autoplay="true" muted="true" loop="true"}
:::

::::
```

---

## Checklist

- [ ] 资源放在 `slides/[name]/assets/` 中
- [ ] 引用路径使用 `assets/filename.ext`
- [ ] 标题写在 `deck.qmd`，内容写在 `index.md`
- [ ] 使用 `.color-*` 进行语义高亮
- [ ] 使用显式 `style="font-size: ..."` 而非 `.smaller`
- [ ] 视频添加 `autoplay muted loop` 属性
