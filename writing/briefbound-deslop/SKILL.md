---
name: briefbound-deslop
description: "Use when the user asks to de-AI-flavor a finished Chinese text (article, doc, blog, release notes, report, paper): fix AI-style sentence patterns, jargon, rhythm and punctuation while preserving facts, numbers, conditions, promises and attributions, keeping the author's voice; do not use for conversational reply styling, README restructuring, or translation."
license: MIT
---

# Briefbound Deslop 成文去 AI 味

## 目标

把用户指定的成文中文文本（文章、文档、博客、发行说明、周报、论文）改掉 AI 味：句式、节奏、黑话、标点。事实、数字、条件、承诺、归属零丢失；保留作者本来的声音，不强行口语化。对话式回复的措辞不归本技能。

## Briefbound task contract

- Context Boundary: 用户指定的成文文本、文体与读者、改写幅度；语义以原文为准；不新增观点，不重排结构。
- Output Contract: 改写后全文或定点修改清单、一句改动说明；文体豁免判定写明依据。
- Allowed Action: 直写用户指定的文本文件；不改变事实与数据；公文/法律文体先豁免判断；不重构文档结构与章节。
- Success Evidence: 句式禁令逐类有处理；数字、单位、引用、条件、承诺与原文相符；同一事物全文一个名字；作者语气保留。
- Stop Condition: 用户要的是内容重构或面向新读者重写、文体与幅度分歧需拍板、或原文事实自相矛盾。
- Route Out: README 面向读者的结构重构 briefbound-readme-optimization；对话回复措辞 briefbound-plain-talk；已验证残留 briefbound-development-cleanup；briefbound-router 或 BLOCKED。

## 统一调用契约

- 只处理 Briefbound task contract 范围；不匹配回 briefbound-router 或更具体 owner，复合任务不吞其他 owner。
- 用户可见内容默认中文、保留技术字面量与专有名词；Route Out 仅以 Briefbound task contract 为准；有自然闸门时末行 `下一步建议: <一个具体动作>`，否则声明继续已授权工作。

## 激活闸门

用户要求给成文文本去 AI 味、说人话改写、收紧文风时进入。排除：对话式回复的措辞取舍（briefbound-plain-talk）、README 作为交付物面向新读者重构（briefbound-readme-optimization）、翻译与从零代写、纯事实核查。

## 先审后改

1. 判文体：公文、法律、合同、论文的固定结构先豁免（见文体豁免）。
2. 定幅度：轻=只删最扎眼处；中=句式+黑话；重=加节奏标点。默认中，用户点名才升降。
3. 先减后改：先删赘余，再改句式，最后顺标点节奏。

## 句式禁令

- 段末总结句（「这说明/可以看出…」）：删，留事实句。
- 「不是…而是…」对比句：改直接陈述。
- 套话开头（「随着…的发展」「在当今…时代」）：删。
- 升华句（把技术观察拔成人生道理）：删。
- 总结标签（「一句话总结」「综上所述」，公文体除外）：删。
- 自问自答、反驳没人提的反对意见：删或改直接论断。
- 讲解腔与空预告（「让我们深入」「更干净地：」）：删。
- 三连排比、电报式短句连发、连续同句首：合并或错开。
- 限定词堆叠：一个论断最多一个限定词。
- 翻译腔：「进行+动词」改直接动词；「非常→很」「例如→比如」。
- 装饰性加粗、被首句复述的标题：去装饰，直接入题。
- 聊天残留（「好问题！」「希望这有帮助」）：删。
- 无出处的「研究表明」：点名来源或删。
- 弱信号不定罪：单一特征不定性，多特征佐证才动手。

## 黑话与标点

黑话分两档，全表见 [references/rewrite-wordlist.md](references/rewrite-wordlist.md)：绝对禁用（赋能、抓手、闭环等）换成具体动作；谨慎档（场景、生态、颗粒度等）确有所指才留。
标点节奏：破折号全文约每三段一个，超了改逗号句号；感叹号除社媒不用；中英与数字间加空格；同一事物全文一个名字，不做同义词轮换；句长长短混排。禁夸大新颖性：描述做了什么，不宣称首创。

## 文体豁免

公文、法律、合同、招投标与论文的固定结构（总分总、首先/其次/再次、摘要-引言-方法-结论）是文体要求，不是 AI 味，保留；条款、编号、引用与法律措辞一字不动。豁免只覆盖结构与程式，不豁免黑话：空转词仍按词表处理；边界拿不准时问用户再动手。

## 场景侧重

技术文档克制可扫读；博客可少量「你」；发行说明按 Breaking→Features→Fixes，一条一句、无 emoji；论文用「我们」、给具体数字。细则见 references/rewrite-wordlist.md。

## 与相邻 owner 的边界

- briefbound-plain-talk 管对话回复的呈现层；本技能管成文交付物的改写。回复说人话归 plain-talk，文档去味归本技能。
- briefbound-readme-optimization 面向新读者重构 README 结构与受众；本技能在既定结构上做文风处理。只去味归本技能，重排结构归 readme-optimization。

## 致谢

方法改编自三个 MIT 项目：ninehills/public-skills 的 deslop-zh（句式禁令、黑话分档、场景策略，Copyright (c) 2026 Tao Yang）、blader/humanizer（弱信号不定罪、聊天残留、标题复述、装饰加粗）、b1rdmania/claude-plain-english-skill（破折号预算、术语一致性、禁夸大新颖性）。均为重写表述，无整段引用。

## 输出

```text
结论: <文体判定、幅度、动了哪几类问题>
验证: <事实数字零丢失核对、术语一致性结果>
Route Out: <沿用 Briefbound task contract>
下一步建议: <有自然闸门时的一个具体动作；否则声明继续已授权工作>
```
