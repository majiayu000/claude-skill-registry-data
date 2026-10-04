---
name: frontend-quality-guardrails-cn
description: 当用户需要构建、修改或审查前端界面，并验证文本溢出、布局、响应式、可访问性和视觉质量时使用。
---

# 前端质量守门规则

## Overview

将本技能作为前端实现和审查的质量守门规则，覆盖超长文本、溢出、换行、截断、对齐、间距、响应式、组件状态、可访问性、国际化、视觉细节、项目代码审查、浏览器截图验证和常见 UI 样式踩坑点。

把所有 UI 都当成会遇到不完美内容来处理。默认假设标签、姓名、URL、ID、价格、翻译文本、用户输入、错误信息、表格单元格、徽章、面包屑、Tab 和按钮文案都可能比设计稿更长。

优先做小而局部的 CSS/布局修复，不要为了局部问题重写整体结构。除非用户明确要求重设计，否则保留现有设计系统、组件 API、设计 token、间距尺度和框架约定。

## 何时使用

在构建、修改或审查前端 UI 且布局质量重要时使用本技能，尤其是：

- 超长文本、URL、ID、翻译文案、表单错误、标签、表格单元格、卡片、Tab、面包屑或徽章可能溢出。
- 任务涉及 HTML、CSS、React、Vue、Svelte、Next.js、Tailwind、shadcn/ui、Ant Design、表单、表格、仪表盘、弹窗、抽屉、导航或响应式布局。
- 用户要求打磨 UI、修复溢出、改进对齐、审查前端代码、验证浏览器截图或规避前端样式踩坑点。

## 不要使用

以下场景不要把本技能作为主要指南：

- 后端、CLI、数据库或基础设施等没有可见 UI 的任务。
- 完整品牌设计、插画、Logo 设计或图片生成。
- 基于截图做像素级还原，且已有更专门的 image-to-code 或设计还原技能。
- 需要正式 WCAG 评分或合规报告的无障碍专项审计。

## 使用说明

把下面的流程作为项目现有前端规范之上的质量守门层。简单修改只使用核心清单；更深入的开发、审查或验收，按需读取“深度参考”里的文件。

## 工作流程

1. 先检查现有 UI 约定：
   - 识别框架、样式系统、组件库、断点、字体尺度、间距 token 和图标库。
   - 复用现有组件和工具类。
   - 不要为了局部修复引入新设计系统。

2. 找出文本风险面：
   - 用户名、组织名、文件名、路径、slug、UUID、hash、token、URL、邮箱、手机号。
   - 标题、卡片标题、表格单元格、导航项、Tab、面包屑、筛选器、chip、badge、tooltip、toast、dialog。
   - 表单标签、占位符、帮助文本、校验错误、空状态、加载文案。
   - 翻译文案和中英文混排内容。

3. 明确每个文本容器的预期行为：
   - 换行：内容可以多行显示且不破坏布局。
   - 限行：内容视觉上限制行数，但完整值在其他地方可访问。
   - 截断：紧凑重复 UI 中使用省略号缩短。
   - 滚动：代码、日志、表格或面板等内容刻意滚动。
   - 自适应：布局随内容变化，但有稳定的最小/最大约束。

4. 实现最小且稳健的修复：
   - 在 flex/grid 文本子项上补 `min-width: 0` 或 `min-height: 0`。
   - 在必要位置添加明确的 `max-width`、`overflow-wrap`、`text-overflow`、`line-clamp` 或滚动行为。
   - 只有父容器才是溢出源时，才调整父级布局。

5. 用极端内容和视口验证：
   - 测试窄屏手机、平板、桌面和宽屏桌面。
   - 测试超长无空格字符串、长自然语言、中英文混排、URL、空值和密集列表。
   - 可行时使用浏览器截图或 DOM 检查验证视觉变化。

## 深度参考

需要更完整覆盖时读取这些参考文件：

- [code-review-checklist.md](references/code-review-checklist.md)：编辑或审查 React、Vue、Svelte、HTML/CSS、组件库、状态型 UI、表单、表格或现有项目代码前使用。
- [visual-standards.md](references/visual-standards.md)：创建、重设计、打磨或评审视觉风格、密度、层级、色彩、圆角、阴影、字体和交互状态时使用。
- [browser-verification.md](references/browser-verification.md)：完成可见 UI 修改后，或调试布局、溢出、响应式问题时，用于浏览器自动化、截图、控制台和视口检查。

## 文本溢出规则

用户必须直接阅读的内容优先换行：

```css
.wrap-text {
  overflow-wrap: anywhere;
  word-break: normal;
  hyphens: auto;
}
```

只有在空间刻意紧凑且完整值仍可访问时才截断：

```css
.truncate-one-line {
  min-width: 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
```

对于重复 UI 里的紧凑名称或标题，优先使用单行省略号，并通过项目已有的 Tooltip/title 模式在鼠标悬停和键盘聚焦时展示完整文本。不要只靠裁剪来“保护布局”；用户仍然必须能查看完整值。

卡片摘要、搜索结果和说明文本可使用多行限行：

```css
.clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
```

日志、代码、长表格和原始技术值适合滚动：

```css
.scroll-panel {
  min-width: 0;
  min-height: 0;
  overflow: auto;
}
```

避免这些陷阱：

- 不要只靠 `overflow: hidden` 解决问题，它会隐藏 bug 并让内容不可访问。
- 不要把 `white-space: nowrap` 套在可能接收翻译文案的容器上。
- 不要默认对可读正文使用 `word-break: break-all`；长无空格 token 优先用 `overflow-wrap: anywhere`。
- 不要截断表单错误、关键警告、价格、日期或危险操作文案。
- 没有受约束宽度和块级/行内块/flex 行为时，不要指望省略号生效。
- 使用限行时，要考虑键盘焦点、屏幕阅读器和完整内容访问路径。

## Flex 和 Grid 踩坑点

含文本的 flex/grid 子项通常要检查 `min-width: 0`：

```css
.row {
  display: flex;
}

.row__content {
  min-width: 0;
  flex: 1;
}
```

CSS Grid 中含长内容的列优先使用 `minmax(0, 1fr)`：

```css
.grid {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
}
```

防止布局抖动：

- 给头像、图标、按钮、表格列和缩略图稳定尺寸。
- 图标和固定控件使用 `flex: none` 或等价写法。
- 重复的横向/纵向节奏优先使用 `gap`。
- 避免百分比宽度叠加 padding 后导致溢出。
- 项目没有全局设置时，补 `box-sizing: border-box`。
- 需要内部滚动的嵌套 flex/grid 面板要检查 `min-height: 0`。

## 对齐和间距

按视觉角色对齐，不按偶然的 DOM 顺序对齐：

- 表单、详情面板、表格和卡片中的 label/value 要一致对齐。
- 图标和文本用 `inline-flex`、`align-items: center` 和稳定 `gap`。
- 纯图标按钮保持正方形并居中。
- 图标+文本控件要视觉上基线平衡，避免图标漂在文字上方。
- 使用项目已有间距尺度，不随意发明一次性 margin。
- 保持标题、正文、控件和区块边界之间的垂直节奏。
- 长段落、表格、表单标签和高密度业务界面不要居中对齐。
- 只有便于列间比较的数字才右对齐。
- 指标、价格、计时器和数字列优先使用等宽数字。

推荐：

```css
.button {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
}
```

## 字体排版

保持字体可读且稳定：

- 不要用视口宽度直接缩放字号。
- 除非项目设计系统明确使用，否则避免负字间距。
- 中英文混排和 CJK 内容要有足够行高。
- 紧凑卡片、侧边栏、工具栏、表格和弹窗里避免过大的标题。
- 按钮文案要短，但不要难懂。
- 即使视觉尺寸不同，也保持语义化 heading 顺序。
- 不要滥用字重，层级也应来自字号、间距、颜色和布局。
- 测试翻译膨胀，德语、俄语、越南语、中文、日文、韩文会以不同方式挑战宽高。

建议起点：

- 正文行高约 `1.45` 到 `1.7`，按密度调整。
- UI 标签行高约 `1.2` 到 `1.4`。
- 高密度表格先保证可读，再追求行数。

## 响应式布局

面向真实断点设计，不只看一个桌面宽度：

- 可行时检查 `320px`、`375px`、`768px`、`1024px`、`1280px` 和一个宽屏尺寸。
- 避免超过小屏的固定宽度。
- 媒体和文本容器使用 `max-width: 100%`。
- 确保 sticky header、侧边栏、底部栏和浮动控件不会遮挡内容。
- 只有大表格、时间线、代码或对比矩阵等天然需要时才横向滚动。
- 移动端点击目标尽量接近 `44px` 高/宽，除非项目明确采用高密度规范。
- 移动浏览器地址栏会影响视口高度，必要时使用 `svh`、`dvh` 或项目支持的 fallback。

移动端：

- 表单和筛选条在横向密度脆弱时应堆叠。
- 主要操作要可触达且不遮挡输入。
- 弹窗要适配视口高度，并让正文内部滚动。
- 不要依赖 hover-only 交互。

## 组件专项检查

### 按钮和控件

- 灵活按钮内的文本 span 要能处理溢出。
- loading 状态和 idle 状态保持同尺寸。
- 危险、禁用、焦点、悬停、按下和选中状态要可区分。
- 不要移除 focus outline，除非替换成可访问的焦点样式。
- 有图标库时，熟悉工具操作优先用图标，并提供可访问标签或 tooltip。

### 表单

- 尽量保留可见 label，占位符不是 label。
- 校验错误要能换行并靠近字段。
- 错误出现时避免布局大跳动。
- select、radio、checkbox、combobox 中的长选项要明确换行或截断。
- 覆盖 autofill、disabled、readonly、required、invalid、loading、success 状态。
- 输入文本不要小到影响阅读。

### 表格和数据网格

- 每列明确策略：固定宽、弹性宽、换行、截断或横向滚动。
- 重要标识符要可读；若截断，应提供复制或完整值访问路径。
- 数字右对齐，文本左对齐。
- sticky 表头/列不能制造裁剪或 z-index 问题。
- 测试空、单行、多行、加载、错误和筛选后状态。
- 除非产品模式已有，不要在每个表格单元格里塞复杂卡片。

### 卡片和列表

- 重复项结构稳定，操作位置一致。
- 可以限行摘要，但不要随意限行关键标题，除非 hover/focus/detail 能看到完整标题。
- badge 不应把主要内容挤出视野。
- hover/focus 样式不要改变卡片尺寸。
- 除非设计系统明确使用，否则避免卡片套卡片。

### 导航、Tab 和面包屑

- 测试长路由名和翻译标签。
- 按需使用溢出菜单、可滚动 Tab、可换行面包屑或有意截断。
- 标签截断时仍要看得出 active 状态。
- 保持键盘导航可用。

### 弹窗、抽屉、浮层、Tooltip

- header/footer 稳定，body 内容滚动。
- popover 不应被视口边缘裁剪。
- 不要把关键信息只放在 hover tooltip 里。
- dialog 要能处理长标题、长错误和复杂表单。
- escape、外部点击、焦点陷阱、关闭后焦点回归遵循组件库模式。

### 图片、头像和媒体

- 设置明确宽高或 aspect-ratio，避免布局位移。
- 有意使用 `object-fit`。
- 有意义图片提供 alt，装饰图使用空 alt。
- 测试缺失、加载慢、损坏和超大图片。
- 不要过度裁剪产品、人物或内容图片，影响用户辨认。

## CSS 和样式踩坑点

避免脆弱 CSS：

- 不要用随机 `z-index`、`position: absolute` 或负 margin 修溢出。
- app shell 不要无脑使用 `height: 100vh`，要考虑移动端视口。
- 高层布局容器不要随意 `overflow: hidden`。
- 不要用全局选择器影响无关组件。
- 没有理由时不要引入 token 之外的颜色、圆角、阴影或间距值。
- 不要让 placeholder、muted、disabled 或 secondary 颜色低对比到不可读。
- 不要把重要内容放在透明遮罩或装饰层后面。
- hover 边框不要改变元素尺寸。
- 能用 transform/opacity 的动画，不要动画布局属性。

稳健基础属性：

- `box-sizing: border-box`
- `min-width: 0`
- `min-height: 0`
- `max-width: 100%`
- `overflow-wrap: anywhere`
- `text-wrap: balance` 只用于标题增强，不作为正确性依赖
- `contain`、`content-visibility` 或虚拟列表只在确有性能需求时使用

## Tailwind 注意点

- flex/grid 文本子项补 `min-w-0`。
- `truncate` 必须配合受约束宽度。
- 可读文本优先 `break-words`，只有技术 token 可接受时才用 `break-all`。
- 支持时用 `line-clamp-*` 处理摘要。
- 大表格外层使用 `overflow-x-auto`，不要让整页横向滚动。
- 图标/头像用 `shrink-0`，文本用 `flex-1 min-w-0`。
- 有 token 或现有组件类时，避免堆很长的 arbitrary value。

常见写法：

```tsx
<div className="flex min-w-0 items-center gap-2">
  <Icon className="size-4 shrink-0" aria-hidden="true" />
  <span className="min-w-0 truncate">Very long label</span>
</div>
```

```tsx
<div className="grid grid-cols-[minmax(0,1fr)_auto] items-center gap-3">
  <p className="min-w-0 break-words">Long readable content</p>
  <button className="shrink-0">Action</button>
</div>
```

## 组件库注意点

- 修改前先读项目里的 wrapper 组件。
- 优先使用组件库公开 props 控制尺寸、状态、禁用、位置、溢出和可访问性。
- 除非没有公开 API，不要用脆弱选择器覆盖内部实现。
- Ant Design 重点检查 `Table` 列宽、`ellipsis`、`scroll.x`、`Tooltip`、`Form.Item` help、`Select` option 渲染、`Typography.Text` ellipsis。
- shadcn/ui 要保留 Radix 的可访问行为和组合方式，优先通过 wrapper class 修布局。
- MUI/Chakra/Headless UI 优先用文档化的 slot props、style props 或组合点。

## 可访问性和语义

- 保留可见焦点和合理 tab 顺序。
- 按钮、链接、标题、列表、表格、表单和 landmark 使用语义元素。
- 纯图标控件提供可访问名称。
- 错误、警告、active 状态和 status 不只靠颜色表达。
- 重要内容被截断时要有完整值访问路径。
- tooltip 要可触达或不承载关键信息。
- 大范围或重复动画尊重 reduced motion。
- normal、muted、disabled、hover、selected、error 文本都要有足够对比。

## 国际化和内容变化

- 可能翻译的文本容器避免硬编码像素高度。
- 不要拼接翻译片段，语法顺序可能不同。
- 检查复数和变量插值。
- 不要假设英文单词边界。
- 确保 CJK、RTL、变音符、emoji 和长数字不破坏布局。
- 支持 RTL 时使用 `dir`、逻辑 CSS 属性或组件库 RTL 能力。

## 视觉细节检查

完成 UI 修改前扫描：

- 文本是否覆盖图标、badge、图片、输入框或相邻区块。
- 内容是否被圆角、sticky bar、抽屉或 hidden overflow 裁剪。
- 卡片或行 hover 时是否改变尺寸。
- 图标尺寸和描边是否不一致。
- 同一组件组内圆角是否混乱。
- 阴影或边框是否让嵌套层级显得偶然。
- 重复项间距是否不均匀。
- 空状态是否像加载坏了。
- skeleton 是否匹配最终布局尺寸。
- disabled 状态是否对比不足或含义不清。
- toast、dropdown、menu、popover 是否被 header 或 modal 遮挡。

## 必测内容

可行时使用这些字符串验证：

```text
This is a normal sentence that should wrap naturally without breaking the layout.
SuperLongUnbrokenOrganizationNameWithNoSpacesAndManyCharacters1234567890
https://example.com/a/very/long/path/with/query?search=frontend-layout-overflow-and-wrapping
张三李四王五赵六前端页面超长文本混排ABCDEFGHIJKLMN1234567890
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
```

同时测试：

- 空字符串
- 单字符
- 超长翻译标签
- 长数字或货币值
- 长校验错误
- 多个 badge/tag
- 缺失图片/头像
- 加载和错误状态

## 验收清单

不要在这些条件满足前标记完成：

- 除非有意设计，否则页面没有横向溢出。
- 文本不会覆盖相邻 UI。
- 长文本按预期换行、限行、截断或滚动。
- 关键完整内容仍可访问。
- 含文本的 flex/grid 子项有合适的 `min-width: 0` 或 `min-height: 0`。
- 移动端和桌面端布局可用。
- 相关时覆盖 loading、empty、error、disabled、hover、focus、selected 和密集数据状态。
- 修改遵循现有设计 token 和组件模式。
- 可用浏览器或截图流程时，完成视觉验证。

## 回复格式

使用本技能完成任务时：

- 说明处理了哪些具体溢出/布局风险。
- 说明做过哪些验证。
- 说明仍未检查的 UI 风险、视口或状态。
