---
name: discover-the-real-requirement
description: Use at the very start of a 0-to-1 build, before any architecture or code, when the user has a goal but cannot fully articulate their requirement, workflow, or the unspoken domain rules they take for granted. Runs a guided discovery loop with hard approval gates — elicit and write the requirement back, draw the workflow, surface the hidden rules and assess risk — and loops back whenever a hidden rule reopens the requirement, so you only design once the picture is stable and confirmed.
---

# Discover the Real Requirement

Most people cannot hand you a complete spec. They have a fuzzy goal, a workflow they have never had to put into words, and domain rules they assume "everyone knows." If you build from their first sentence, you build the wrong thing — and every rule they never mentioned becomes a rewrite. This skill is the guided discovery that comes *before* any architecture: draw the requirement out, write it back for approval at every gate, and treat a newly surfaced hidden rule as a reason to loop, not to push forward.

## The loop, and the gate rule

Discovery is **not one pass**. Each stage below produces a written artifact the user reads and *explicitly approves* before you move on. Stage 3 routinely reopens Stage 1 — that is the loop working, not failing. Re-run **Chapter 1 → 2 → 3** until a full pass surfaces nothing new and the user agrees to all three. Only then do you design (Chapter 4).

## Chapter 1 — Elicit, then write the requirement back

- **Guide with detailed questions, not a form dump.** Draw out the goal *behind* the ask — "what are you actually trying to do / how do you handle this today without it" — because the first thing said is usually a guessed solution, not the problem.
- **When you have enough, stop and summarize.** Write the requirement back in plain language — a description the user can actually read and react to.
- **Gate:** the user reads the summary and agrees. No agreement → keep eliciting. Never carry an unconfirmed summary into the next stage.

## Chapter 2 — Draw the flow

- **Turn the confirmed requirement into an explicit workflow:** the actors/roles, the steps, what triggers what, where data / money / approval changes hands, and the states an entity moves through.
- **Get one real end-to-end walk-through** ("walk me through the last time you did this") so the flow is concrete and real, not idealized — people describe workflow accurately only through a concrete case.
- **Gate:** the flow is confirmed before you move on.

## Chapter 3 — Surface the hidden rules, then assess risk

- **Deliberately excavate the unspoken rules.** Probe for edge cases, exceptions, "what happens when…," and the domain conventions the user assumes are obvious (who's allowed to do what, what's forbidden, seasonal or scale realities).
- **List them back explicitly so the user can see them** — then have them assess the risk of each and re-evaluate every requirement item in that light. A rule the user only half-knew is now on the table.
- **This is the feedback point.** A newly surfaced rule almost always changes the requirement. When it does, **loop back to Chapter 1** — re-confirm the requirement, re-draw the flow (Ch. 2), re-check the rules (Ch. 3). Iterate until a full pass turns up nothing new and all three are agreed.

## Chapter 4 — Only now: design, framework, and continuous fine-tuning

- **With requirement + flow + rules all agreed and stable,** explore the design and write the framework — core entities / data model, module boundaries, main flows — in plain language first, then structure.
- **Keep fine-tuning against the user.** Design makes new questions concrete that discovery couldn't; feed each one back through the same gates and re-confirm the requirement as it sharpens.
- **Constraint:** never let the design run ahead of a confirmed requirement. Every adjustment is re-confirmed, not assumed — the whole point of the loop is that nothing load-bearing is ever silently guessed.

## The principle

The gates *are* the product. An agent that guesses looks faster and ships the wrong thing; an agent that writes each stage back and waits for a "yes" trades a handful of confirmations for not rebuilding the foundation. And a hidden rule reopening the requirement is not the loop stalling — it is the loop catching, before code, exactly the surprise that would otherwise have surfaced as a rewrite.

## See it in action

[`examples/discovery-loop-walkthrough.md`](examples/discovery-loop-walkthrough.md) — a short annotated transcript where a "booking system" request loses its first-sentence shape and a forgotten 48-hour cancellation rule reopens the requirement mid-loop.

---

> Adapt, don't copy-paste. This is the shape of the idea, not a config to drop in verbatim — how many questions each stage needs, and which domain rules are worth probing for, come from the user and the field you're building in.

---

<details>
<summary><b>中文版</b>(点击展开)</summary>

# 探索真实需求

大多数人没法直接递给你一份完整的需求文档。他们有一个模糊的目标、一套自己从没被迫用语言讲清楚过的流程、还有一堆他们默认「这还用说」的行业规则。如果你照着他说的第一句话就开建,你建的就是错的东西——而每一条他没提过的规则,后面都变成一次重写。这个 skill 就是排在任何架构之前的那步引导式探索:把需求一点点问出来,每道闸门都写成文字让用户点头,并且**把新冒出来的潜规则当成倒回去循环的理由,而不是继续往前冲的理由**。

## 这个循环,以及闸门规则

探索**不是一遍过**。下面每个阶段都产出一份文字,用户读过并**明确同意**了,才往下走。第三章会经常倒逼第一章重开——这是循环在起作用,不是出了问题。反复跑**第一章 → 第二章 → 第三章**,直到一整轮都冒不出新东西、且三样用户全都同意,才进入设计(第四章)。

## 第一章:引导提问,再把需求写回去

- **用详细的提问去引导,不是甩一张表格。** 把请求**背后**的目标问出来——「你到底想干成什么/现在没有这个东西你怎么办」——因为人开口说的第一件事,通常是他猜的解决方案,不是问题本身。
- **信息够了就停下,做总结。** 用大白话把需求写回去——一份用户真的能读、能反应的描述。
- **闸门:** 用户读了这份总结并同意。不同意 → 继续问。绝不把一份没确认的总结带进下一阶段。

## 第二章:画流程

- **把确认过的需求变成明确的工作流:** 有哪些角色、哪几步、什么触发什么、数据/钱/审批在哪里易手、一个实体会经过哪些状态。
- **拿一个真实案例从头到尾走一遍**(「上次你干这件事,一步步是怎么走的」),让流程是具体的、真实的,而不是理想化的——人只有通过具体案例才能把流程描述准。
- **闸门:** 流程确认了,才往下走。

## 第三章:挖出潜规则,再评估风险

- **主动去挖那些没说出口的规则。** 逼问边界情况、例外、「遇到 X 会怎样」,以及用户默认「显而易见」的行业惯例(谁能干什么、什么是禁区、旺季或规模上的现实)。
- **明确地列回给用户看**——然后让他逐条评估风险、并据此重新审视每一项需求。一条他此前只知道一半的规则,现在被摆到了台面上。
- **这里就是反馈点。** 一条新冒出来的规则,几乎总会改变需求。一旦改变,就**倒回第一章**——重新确认需求、重画流程(第二章)、再校潜规则(第三章)。循环到一整轮再也翻不出新东西、三样全部同意为止。

## 第四章:到这一步才:设计、写框架、持续微调

- **在需求 + 流程 + 规则全部同意且稳定之后,** 才去探索设计、写框架——核心实体/数据模型、模块边界、主要流程——先用大白话,再上结构。
- **持续跟用户微调。** 设计会把一些探索阶段问不出来的细节变得具体;把每一个都通过同样的闸门反馈回去,随着需求变清晰再确认一遍。
- **约束:** 绝不让设计跑到「已确认的需求」前面。每一次调整都要重新确认,而不是假设——这个循环的全部意义,就在于没有任何承重的东西是被悄悄猜出来的。

## 核心原则

闸门**本身**就是产物。爱猜的 agent 看起来更快,交付的却是错的东西;而每个阶段都写回去、等一声「同意」的 agent,只是用几次确认,换来了不必重建地基。一条潜规则倒逼需求重开,不是循环卡住了——那是循环在代码之前,恰好逮住了那个否则会以「重写」的形式浮现出来的意外。

## 看它怎么跑

[`examples/discovery-loop-walkthrough.md`](examples/discovery-loop-walkthrough.md) —— 一段带批注的对话样例:一个「预订系统」的请求丢掉了第一句话的形状,一条被忘掉的「48 小时取消规则」在循环中途倒逼需求重开。

---

> 别照搬,自己微调。这里给的是思路的骨架,不是一份可以直接粘贴进项目的配置——每个阶段要问多少、哪些行业规则值得去挖,来自用户本人和你要构建的那个领域。

</details>
