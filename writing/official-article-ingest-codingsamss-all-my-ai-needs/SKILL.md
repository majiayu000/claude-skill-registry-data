---
name: official-article-ingest
description: "Use when Sam wants to collect, save, translate, or reformat official source articles/blog posts/research/product announcements into the Obsidian vault, especially requests mentioning 官方文章, 官网排版, 原始排版, 美观, 收录, 1:1, 原文1:1, or 英文中文对照1:1. Preserve the source site's information architecture and visual hierarchy rather than forcing a generic Markdown template."
---

# Official Article Ingest

用于把官方来源文章收录到 Sam 的 Obsidian Vault，并尽量保持来源页面的原始结构、视觉层级和阅读美感。默认先读取 `orbit-os` 规则，遵守 Vault 路径、媒体本地化、外部写入后 `touch "<file>"` 等约束。

## 先判定模式

如果用户没有明确说明，先问要哪一种；不要把两种混用。

### 模式 A：原文 1:1

适用表达：`原文1:1`、`只要原文`、`原始英文保存`、`按官网原文排版`。

- 保留来源语言正文，不插入中文翻译。
- 保留源站信息架构：hero、标题、副标题/摘要、日期、作者、Quick links/TOC、正文层级、列表、表格、媒体、图注、labels、acknowledgments、source link。
- 在 Obsidian 中做“近似官网排版”，可以用少量内联 HTML；不新增全局 CSS，除非用户明确要求做模板化复用。
- 如果来源是公开受版权保护文章，避免在最终回复中贴出长段原文；本地落盘前优先确认用户是否已有合法来源/是否已在 Vault 中存有原文。无法确认时，采用结构对齐的摘录与自有整理，并说明边界。

### 模式 B：英文中文对照 1:1

适用表达：`英文中文对照1:1`、`中英对照1:1`、`逐段对照翻译`、`逐段补中文`。

- 保留英文原文顺序，在每个英文段落、列表项、图注、标题或表格块后紧贴中文翻译。
- 中文默认使用普通段落，除非原文自身是引用块、callout、列表、表格或代码块。
- 不把译文集中放到文末，不改写成摘要，不额外添加编辑说明或观点，除非用户要求。
- 标题、日期、作者、摘要、Quick links、媒体说明也要双语化，并尽量保持源站首屏节奏。

## 版式原则

- 以官方页面原始排版为第一参考，而不是套通用 Markdown 模板。
- 先识别来源页面首屏：品牌/栏目、hero 标题、中文/英文标题、封面或主图、日期、作者、dek/摘要、Quick links。
- 正文保持原顺序：不要重排章节，不合并独立段落，不移动图片/视频到文末。
- 对 Google/OpenAI/Anthropic 等官方文章，优先保留“官网阅读感”：大标题、充足留白、媒体靠近对应段落、caption 紧贴媒体。
- Obsidian 近似排版可以使用内联 HTML，但必须在当前笔记内自包含；不要污染全局主题或其他笔记。

## 媒体与链接

- 正文图片、视频、动态图默认本地化到同级 `assets/<slug>/`，正文使用相对路径。
- 保留原文链接；外部 source 放 frontmatter 的 `source`。
- 媒体必须做三数校验：预期正文媒体数 = 下载成功数 = 文内引用数。缺失时不要宣称完成。
- 图注/视频说明按模式处理：原文 1:1 只保留原语言；中英对照 1:1 保留原文 caption + 中文 caption。

## Vault 收尾

- Frontmatter 必须在第一行，`---` 分隔符只用于 frontmatter；正文分隔线用 `***`，避免校验混淆。
- 写入后执行 `test -s "<file>"`。
- 写入后执行 `touch "<file>"`，路径必须加引号。
- 抽查 Obsidian Reading/Preview：首屏 hero、Quick links、正文列表、媒体 caption 是否美观可读；如果标题被挤到逐字断行，降低字号或调整列宽。
- 最终只汇报改动范围、媒体/结构校验、`touch` 结果；不要把整篇文章正文贴到回复里。
