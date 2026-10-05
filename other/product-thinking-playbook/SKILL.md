---
name: product-thinking-playbook
description: A decision-making playbook for solo product builders. 20 principles across 5 dimensions — Intent, Boundary, Execution, Quality, Closed Loop — extracted from 6 shipped products. Use when starting a new product, stuck on a product decision, reviewing your own work, or collaborating with an AI coder who can write anything but doesn't know what to build.
---

# Product Thinking Playbook

> A judgment framework for indie developers and product people.  
> Not a "product manager handbook" — a record of what's actually going through your head *in the moment* you make a call.  
> 一套给独立开发者 / 产品人的判断框架。不是"产品经理手册"，是把"做决策的那一刻在想什么"写下来。

**Each principle file below is bilingual (English first, then 中文).**

## When to use this skill

Open the corresponding principle before making the call:

- **Starting a new product** → `principles/01-scenario-first.md` → `principles/02-spec-before-code.md`
- **Feature creep, can't stop adding** → `principles/05-subtraction-over-addition.md`
- **Working with AI, product feels off** → `principles/11-commander-posture.md`
- **Have a batch of bugs, don't know where to start** → `principles/13-end-to-end-fixes.md` + `14-design-vs-execution-error.md`
- **Product "works" — what's next?** → `principles/17-real-engagement-metrics.md` + `20-distribution-is-product.md`
- **Quick lookup** → `quick-reference.md`

新产品立项 / 功能蔓延 / 收不住手 / bug 收不住 —— 打开对应的原则文件再做决定。

## Five dimensions

| Dimension | Answers | Principles |
|---|---|---|
| **I. Intent 立意** | Why does it exist? For whom? | 01–04 |
| **II. Boundary 边界** | What NOT to do? | 05–08 |
| **III. Execution 执行** | How to ship the judgment? | 09–12 |
| **IV. Quality 品质** | How to make it stick? | 13–16 |
| **V. Closed Loop 闭环** | When is it "done"? | 17–20 |

## 20 principles · index

**I. Intent 立意**
1. [Scenario-first · 场景先于功能](principles/01-scenario-first.md)
2. [Spec before code · 先定性，再动手](principles/02-spec-before-code.md)
3. [Aesthetic as stance · 气质即立场](principles/03-aesthetic-as-stance.md)
4. [Subtitle as promise · 副标题是承诺](principles/04-subtitle-as-promise.md)

**II. Boundary 边界**

5. [Subtract, don't add · 做减法而非加法](principles/05-subtraction-over-addition.md)
6. [Vision non-negotiable · 愿景不妥协](principles/06-vision-non-negotiable.md)
7. [Product boundary = user's decision path · 产品边界 = 用户决策路径](principles/07-product-boundary.md)
8. [Infrastructure mindset · 克制：不是基础设施该做的别做](principles/08-infrastructure-mindset.md)

**III. Execution 执行**

9. [Decisive & meticulous · 决策果断，细节挑剔](principles/09-decisive-and-meticulous.md)
10. [Borrow existing cognition · 借力已有认知](principles/10-borrowed-cognition.md)
11. [Commander posture · 指挥者姿态](principles/11-commander-posture.md)
12. [Content standards > technical standards · 内容标准 > 技术标准](principles/12-content-standards-first.md)

**IV. Quality 品质**

13. [End-to-end fixes · 端到端修复](principles/13-end-to-end-fixes.md)
14. [Design vs execution error · 设计错误 vs 执行错误](principles/14-design-vs-execution-error.md)
15. [Experience before review · 先用再评](principles/15-experience-before-review.md)
16. [Security = product quality · 安全 = 产品品质](principles/16-security-as-quality.md)

**V. Closed Loop 闭环**

17. [Core metric bound to real engagement · 核心指标绑定真实投入](principles/17-real-engagement-metrics.md)
18. [Persistence is trust · 持久化 = 信任基础](principles/18-persistence-is-trust.md)
19. [Cross-platform parity + honest permissions · 跨端一致 + 权限诚实](principles/19-honest-parity.md)
20. [Distribution is part of the product · 分发是产品的一部分](principles/20-distribution-is-product.md)

## Case studies

Every principle above is grounded in a real project. The full development conversations:

- [Contra Code](case-studies/contra-code.md) · VS Code Contra overlay
- [AudioLib](case-studies/audiolib.md) · Audio library API service
- [Gospel Hub](case-studies/gospel-hub.md) · Gospel music aggregator
- [Spybook](case-studies/spybook.md) · Interactive detective fiction
- [Tarot](case-studies/tarot.md) · AI tarot consultation
- [Xianxia](case-studies/xianxia.md) · AI xianxia novel generation

## How to invoke

```
In Claude Code:
> Using product-thinking-playbook, help me decide: should this feature go in now?

In your own head:
> Read through quick-reference.md, find the line that hurts most.
```

---

## Three core postures · 三个核心姿态

**English:**
> 1. **Intent stands firm:** scenario, aesthetic, vision — each clearly articulated, you'd push back on a one-character change.
> 2. **Execution holds up:** decisive direction × meticulous detail; you're the commander, not the contractor.
> 3. **Loop closes:** it works → it stands up to scrutiny → users can actually reach it.

**中文：**
> 1. **立意定得住**：场景、气质、愿景都能说清楚，别人改一字都不舒服。
> 2. **执行扛得住**：果断拍板 × 细节不放过，自己是指挥者不是乙方。
> 3. **闭环做得到**：能跑起来 → 经得起推敲 → 用户真的能用到。

---

*Distilled from the full-process conversations of 6 shipped products · 2026-04*  
*基于 6 个已上线产品的全过程对话提炼*  
*Author [@yangyue1974](https://github.com/yangyue1974) · [43.group](https://43.group)*
