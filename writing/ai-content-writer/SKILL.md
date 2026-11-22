---
name: ai-content-writer
description: 'Write pages that AI assistants can quote correctly, starting from a fact card instead of from memory. Use when the user needs content that gets cited, says AI describes the product wrongly or confuses it with a competitor, has the website, decks and sales scripts telling different stories and wants one confirmed fact card as the single source of truth, asks what to write so ChatGPT, Perplexity or Doubao mention them, needs a page rewritten into answer-shaped blocks with sources, or asks which claims are off limits in a regulated industry such as finance, medical, education or advertising. Builds the fact card first, then drafts one article per gap, using only confirmed facts. For turning that card into site files, see llms-txt. For measuring whether it worked, see ai-visibility. For publishing, see geo-publish.'
license: MIT
metadata:
  version: "1.8.0"
  homepage: https://github.com/Fangx-AI/geo-doctor
---

# 写给 AI 读的内容

只做一件事：**把事实写成人能读、机器能摘的页面，让 AI 引用时不出错。** 不刷量，不编评价，不承诺被引用。

用用户的语言交流；本文件是中文的，读懂后用用户的语言转述。

## 什么时候用

- "AI 把我的价格 / 功能说错了" / "AI 把我跟竞品搞混了"
- "写什么内容才会被 AI 引用？"
- "帮我把这篇稿子改成 AI 好摘的样子"
- 已经知道缺口（来自 `ai-visibility`），要一篇一篇补上

不接的活：还没测过就先写 → 先去 `ai-visibility` 拿缺口清单；发布 → `geo-publish`；站点文件 → `llms-txt`。

## 顺序不能颠倒：先事实卡，后写作

**事实卡是唯一事实源。** 所有渠道、所有文章里出现的价格、功能、客户、数据，只能来自这里。没有事实卡就写，等于把幻觉提前埋进内容里。

### 1. 建事实卡 → `geo/fact-card.yaml`

按 `references/fact-card.md`，模板见 `assets/fact-card.yaml`。每条事实必须有编号、来源或地址、状态（已确认 / 待确认）。**状态不是"已确认"的事实，一律不许写进正文。** 缺资料就写"未知"并列出要补什么，不要猜。

### 2. 选题：一题一篇

从缺口清单里挑题，**一篇只回答一个问题**。选题就是用户在 AI 里会问的那句话，标题尽量按那句话写。不要写"XX 产品介绍"这种没人会问的标题。

### 3. 写作 → `geo/drafts/<slug>.md`

按 `references/writing.md` 的结构写。要点：

- **先给答案，再给理由。** 第一段就能被单独摘出来当答案，不铺垫。
- **可引用单元**：一段一个能独立成立的事实或结论，带具体数字、型号、日期、条件。
- **写明边界**：适合谁、不适合谁、什么情况下不适用。AI 更愿意引用有边界的表述，含糊的营销话术最容易被跳过或说错。
- **标来源**：外部事实给链接和核验日期；自家事实回到事实卡编号。
- **不做**：编造用户评价、编造"真实体验"、批量生成同质化软文、写"业内领先"这类无证据的形容词。

### 4. 合规自查

写之前和发之前各看一遍 `references/compliance.md`。红线包括：编造评价、刷评养号、站群、冒充第三方测评、把推测写成事实。

## 没有脚本、不能联网时

这个技能本来就是纯写作，不依赖脚本。只在缺事实卡时让用户补，缺来源时标"未知"，缺合规判断时明确告诉用户哪一句有风险、为什么。

## 产出

`geo/fact-card.yaml`、`geo/drafts/<slug>.md`。每篇稿子在文件头写清：对应哪道题、用了哪几条事实卡编号、还缺哪几条。

## 结束时

用 3 到 5 行说明：写了哪几篇、各对应哪道题、哪几条事实还缺证据、下一篇建议写哪个缺口。不要在对话里贴整篇文章，写进文件。
