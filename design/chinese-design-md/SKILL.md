---
name: chinese-design-md
description: 中式 DESIGN.md 设计系统。当用户要"中国风网页""国风页面""中式设计系统""给项目定个中式风格""DESIGN.md""让 AI 按设计规范生成界面""中文网页排版规范"时使用。提供 8 套可直接丢进项目根目录的 DESIGN.md，AI 读了就按这套规范生成界面。含西文设计系统普遍缺失的中文排版规则。
metadata:
  author: sanhuang520-ship-it
  category: design
  tags: design, standards, chinese, ui
---

# 中式 DESIGN.md

**DESIGN.md 是给 AI 编程工具读的设计系统文档。** 放到项目根目录，
AI 生成界面时就照着里面的颜色、字体、组件规则来，不用你每次描述一遍。

这个技能提供 **8 套中式设计系统**，格式与社区通行的 DESIGN.md 一致。

## 什么时候用

要做中国风网页 / 国风 H5 / 中式品牌页；或者你只是不想让 AI 又生成一个
「紫色渐变 + 圆角卡片」的通用界面。

## 怎么用

```bash
# 1. 挑一套，复制到项目根目录
cp skills/chinese-design-md/design-md/ink/DESIGN.md ./DESIGN.md

# 2. 告诉你的 AI 编程工具
```

> 按照项目根目录 DESIGN.md 里的设计规范，实现这个页面

就这两步。Claude Code、Codex、Cursor 都能读。

## 8 套怎么选

| 主题 | 气质 | 适合 |
|---|---|---|
| **水墨** `ink` | 宣纸、墨色层次、大留白 | 长文阅读、文化内容、需要安静的界面 |
| **青绿** `azurite` | 石青石绿矿物色、装饰性强 | 文旅、展览、需要贵气的场景 |
| **宋韵** `song` | 素雅克制、青瓷灰绿 | 茶饮、书店、高端服务 |
| **敦煌** `dunhuang` | 土红石青、斑驳壁画质感 | 文化 IP、叙事型页面 |
| **朱砂** `vermilion` | 雅红、暖白底 | 节日、活动页、转化页 |
| **新中式** `neo` | 木色暖灰、低饱和 | 家居、生活方式、品牌官网。**最百搭** |
| **竹韵** `bamboo` | 竹青素白、清爽 | 健康、教育、环保 |
| **夜宴** `night` | 深色底 + 暖金。**唯一深色** | 影音、夜间模式、高端活动 |

拿不准就用 **新中式**。

## 每份 DESIGN.md 里有什么

YAML frontmatter（语义化 color token，AI 直接读）+ 这些章节：

Overview（含出处）· Colors（含**逐项对比度实测**）· **Typography（中文排版规则）**
· Layout · Elevation · Shapes · Components · Do's and Don'ts · Responsive · Iteration Guide · Known Gaps

## ⭐ 关键差异：中文排版

这是多数设计系统缺的一块。西文 DESIGN.md 的 Typography 章节讲的是字重、
字距、x-height —— **搬到中文页面上基本不适用**。

每份文件里写死了这些：

| 规则 | 值 | 为什么 |
|---|---|---|
| 行高 | **1.75** | 中文字面率高，1.5 会挤 |
| 行宽 | **38em** | 中文每行 30–40 字最舒服 |
| 对齐 | **left，不用 justify** | 中文没有词间空格，两端对齐会拉出难看的字距 |
| 断行 | `line-break: strict` | CJK 避头尾：`。，、）」` 不能出现在行首 |
| 强调 | `text-emphasis: dot` | **中文不用斜体** —— 系统中文字体没有真正的意大利体 |
| 中英间距 | 加空格 | 「使用 AI 工具」比「使用AI工具」易读 |

**而且不依赖任何商业字体**，全部用系统自带中文字体——不会出现「设计稿好看、上线糊掉」。

## 对比度是实测的，不是声称的

每份文件里有一张实测表（用 WCAG 相对亮度公式算的），并且**标出了不达标的项**：

- 8 套的**正文与标题**对比度全部通过 AA（9.40:1 – 17.10:1）
- `song` 的辅助文字色 4.23:1、主色 2.83:1 **未达 AA** —— 文件里写明了只能用于色块和大字
- `neo` 的主色 4.46:1 **略低于 AA** —— 同样标注了

**标出自己不达标的地方，比笼统说一句「全部通过」有用。**

## 这个技能不做的事

1. **不做西文设计系统** —— 要 Stripe、Linear 那种风格，去用社区里现成的 74 份
2. **不保证「像某个具体品牌」** —— 这 8 套是美学传统的提炼，不是对任何公司视觉的复刻
3. **不提供商业字体** —— 只用系统字体，这是刻意的
4. **色值不代表传统色的权威标准** —— 传统色在不同文献里本就有出入，这是本设计系统自己的实现

## 配套

- [8 套主题的真实渲染截图](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/shots/) —— headless Chrome 实跑生成
- [在线切换预览](https://sanhuang520-ship-it.github.io/awesome-chinese-ai-tools/themes/)
- 同源的 CSS 实现：`skills/chinese-web-themes/themes.css`
- 更细的中文排版规则：`skills/chinese-typography/SKILL.md`
