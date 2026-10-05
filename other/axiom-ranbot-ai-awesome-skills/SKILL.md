---
name: axiom
description: First-principles assumption auditor. Classifies each hidden assumption (fact / convention / belief / interest-driven), ranks by fragility × impact, and rebuilds conclusions from verified premises. Bi
category: AI & Agents
source: antigravity
tags: [claude, ai, aws, rag, cro]
url: https://github.com/sickn33/antigravity-awesome-skills/tree/main/skills/axiom
---


# Axiom — First-Principles Assumption Auditor / 第一性原理拆解器

Strip any question down to its irreducible truths, then rebuild from there.
This is not framework fill-in-the-blank — it is assumption prosecution.

把任何问题强制剥离到"不可再拆的最小真相单元"，再从那里重建。
不是框架填空，是假设审判。

## Language Rule / 语言规则

> **Auto-detect the user's input language and respond entirely in that language throughout the session.**
> If the user writes in Chinese, all phases, labels, and outputs must be in Chinese.
> If the user writes in English, all phases, labels, and outputs must be in English.
> Do NOT mix languages unless the user explicitly switches.

---

## When to Use This Skill / 何时使用

- A major life or career decision is on the table (quitting a job, starting a company, buying a house)
- You want to stress-test a business direction or product hypothesis
- You suspect a belief you hold might be wrong but can't articulate why
- You need to cut through complexity and find the real bottleneck
- Someone asks you to "think from first principles" or "break it down"

**Trigger phrases (中文):** 第一性原理 / 帮我想清楚 / 拆解一下 / 从底层分析 / 这个假设对吗 / 我在做一个决定 / 从根本上分析 / 底层逻辑 / 元问题 / 重新思考 / 有没有想错 / axiom

**Trigger phrases (English):** first principles / break it down / question my assumptions / think from scratch / challenge this belief / audit my reasoning / what am I missing / help me think clearly / axiom

---

## What This Skill Does / 核心能力

1. **Problem Reframing / 问题澄清** — Confirms the question itself is correctly defined before touching assumptions
2. **Assumption Mining / 假设挖掘** — Systematically surfaces 8-12 hidden assumptions across three depth layers
3. **Assumption Classification / 假设分类** — Force-labels every assumption into one of four types with different challenge strategies
4. **Risk Ranking / 优先级排序** — Scores each assumption on Fragility × Impact and outputs a "Most Dangerous Top 3"
5. **Reconstruction / 重建** — Rebuilds conclusions from verified premises only, explicitly comparing "before vs after" cognitive shift

---

## The 5-Phase Process / 拆解流程 — 5 阶段

### Phase 1: Problem Reframing — What are you REALLY trying to solve?

**阶段1：问题澄清 — 你真正想解决的是什么？**

Do NOT start decomposing assumptions yet. First confirm the problem itself is correctly defined.

Many people ask "Should I quit my job?" when the real question is "Why can't I grow in my current role?" These are fundamentally different problems with different assumption sets.

**Ask:**
- Who defined this problem? You, someone else's expectations, or a social narrative?
- Is this the root problem, or a symptom of something deeper?
- Restate the core question in one sentence.

**Output:** A single reframed core question, presented to the user for confirmation before proceeding.

> 先不拆假设，先确认问题本身没有被误定义。
> 很多人问"我该不该换工作"，但真正的问题是"我在当前工作里能不能成长"。
> Axiom 先问：这个问题是谁定义的？是你自己、他人期待、还是社会叙事？
> **输出：一句重新表述的核心问题，供用户确认。**

---

### Phase 2: Assumption Mining — What are you believing without proof?

**阶段2：假设挖掘 — 你在相信什么？**

Systematically mine hidden assumptions in three layers:

| Layer | Description | Example |
|-------|-------------|---------|
| **Surface** | Obvious, often stated aloud | "I need more money" |
| **Middle** | Industry conventions, common wisdom | "A degree is required for good jobs" |
| **Deep** | Never questioned, feels like gravity | "Success means financial independence" |

**Goal:** Find 8-12 assumptions. The more concrete, the better. Reject vague statements like "I think this is right" — force specificity.

**When detecting the user's scenario type**, reference the appropriate scenario checklist from `references/scenarios.md` to ensure thorough mining.

> 系统性挖掘隐含假设，分三层：
> - **表层假设**（显而易见的）
> - **中层假设**（行业惯例或常识）
> - **深层假设**（你从未质疑过、觉得"天经地义"的信念）
>
> 深层假设才是最有价值的。
> **目标：找到 8-12 个假设，越具体越好，不接受模糊的"我以为这样更好"。**

---

### Phase 3: Assumption Classification — What is the nature of this belief?

**阶段3：假设分类 — 这个信念的本质是什么？**

Label every assumption with one of four types. Each type has a fundamentally different challenge strategy:

| Type | Label | Definition | Challenge Strategy |
|------|-------|------------|--------------------|
| 🔵 | **Physical Fact / 物理事实** | Laws of nature, mathematical truths. Cannot be changed. | Accept it. Do not waste energy questioning gravity. |
| 🟡 | **Historical Convention / 历史惯例** | Once valid, widely practiced. | Check if the environment has changed. What was true in 2010 may not be true now. |
| 🔴 | **Subjective Belief / 主观信念** | Personal experience projected as universal truth. | Who told you this? Have you personally verified it? Seek counter-evidence. |
| ⚫ | **Interest-Driven / 利益驱动** | Someone benefits from you believing this. | Trace the incentive chain. Who profits from this narrative? |

**The classification itself is the insight.** Many people discover for the first time that something they treated as "fact" is actually "convention."

For detailed identification methods, examples, and edge cases, reference `references/assumption-types.md`.

> 对每个假设打标签。不同性质的假设有不同的质疑方式，处
