---
name: smart-subagent-dispatch
description: Use before dispatching any subagent/Task call. Classifies the subtask as pure-retrieval, diagnostic, or hybrid, and routes pure-retrieval work to a cheap/fast model while keeping the primary model for anything that requires reasoning — cutting token spend without silently degrading decision quality.
---

# Smart Subagent Dispatch

Most agentic coding sessions burn tokens by spawning a full-price subagent for *every* delegated task — including ones that are just "go read these five files and tell me what's there." That's a pure lookup, and a small/cheap model does it exactly as well as your primary model for a fraction of the cost. The trap is doing the opposite: pushing a task that actually requires judgment onto a cheap model and silently trusting whatever it returns.

This skill is the classification step that goes *before* you spawn a subagent.

## Step 1 — Classify the task

- **Pure retrieval**: search for references, list matching files, count call sites, format/reformat, read a file and state its literal contents.
  → route to a cheap/fast model (e.g. Haiku-tier).
- **Diagnostic**: root-causing an error, cross-file causal analysis, judging *why* behavior doesn't match expectation.
  → keep the primary model. Do not downgrade.
- **Hybrid** (needs both retrieval and judgment — e.g. "find every place X is called, and tell me which ones would cause Y"):
  → split it into two steps. Cheap model does the retrieval pass first; the primary model then reasons over that output. Never let a cheap model attempt a hybrid task in one shot — the "judgment" half quietly gets skipped or hallucinated.

## Step 2 — The actual test

Ask what the subtask's *output* looks like:

- If the output is a **fact list** (file path + line number + literal content, no interpretation) → cheap model is fine.
- If the output has to contain **"why"** — reasoning, a causal claim, a judgment call → do not downgrade.

If you're not sure which bucket a task falls into, default to **diagnostic** (no downgrade). The point of this skill is saving tokens without paying for it in wrong answers — when in doubt, don't gamble the answer's correctness to save a fraction of a cent.

## Step 3 — Verify before you trust it (this is the step people skip)

A cheap-model retrieval pass is not automatically correct. Once it comes back:

- The primary model does a **fast pass** over the returned file paths/line numbers to confirm they're actually right.
- Pay extra attention on anything involving **same-named variables across scopes, cross-scope references, or multi-hop call chains** — this is exactly where small models under-report edge cases.
- **Unverified cheap-model output must never be used directly** as the basis for a subsequent diagnosis or an edit. Spot-check it first, every time.

## The principle

Token savings are only a win if they don't cost you decision quality. If a task's category is ambiguous, that ambiguity itself is a signal to *not* downgrade — the failure mode of a wrong "cheap and fast" call is much more expensive than the tokens it saved.

---

> Adapt, don't copy-paste. This is the shape of the idea, not a config to drop in verbatim — the exact thresholds (which tasks count as "hybrid," how deep the verification pass goes) should be tuned against your own project's actual failure patterns.

---

<details>
<summary><b>中文版</b>(点击展开)</summary>

# 智能子代理调度

大部分 agent 编程 session 都在做一件浪费 token 的事:**每一个**委派出去的任务都用全价模型跑一遍子代理——哪怕这个任务只是"去读这五个文件,告诉我里面有什么"。这种纯查找类任务,便宜/快速的小模型跟你的主模型做得一样好,成本却低一大截。真正的坑在反方向:把一个其实需要判断力的任务丢给小模型,然后不加核实就直接采信它的结论。

这个 skill 就是**派发子代理之前**的那一步分类判断。

## 第一步:任务分类

- **纯检索类**:搜索引用、列出匹配文件、统计调用位置、格式化/重排、读文件并原样陈述内容
  → 派给便宜/快的模型(如 Haiku 档位)
- **诊断类**:定位报错根因、跨文件因果分析、判断"为什么"逻辑不符预期
  → 保持主模型,不降级
- **混合类**(既要检索又要判断,例如"找出所有调用 X 的地方,并判断哪些会导致 Y 问题")
  → 拆成两步:先用便宜模型做检索,再让主模型基于检索结果做判断。**禁止**让便宜模型一步到位完成混合任务——"判断"那一半会被悄悄跳过或编造。

## 第二步:真正的判断标准

问子任务的**输出**长什么样:

- 输出是"**事实清单**"(文件路径 + 行号 + 原文内容,不含解释)→ 用便宜模型没问题
- 输出必须包含"**为什么**"——推理、因果判断、下结论 → 禁止降级

不确定任务属于哪一类时,默认归为**诊断类**(不降级)。这个 skill 的意义是"省 token 但不牺牲答案质量"——不确定的时候,别为了省一点点钱去赌答案对不对。

## 第三步:采信前先核实(这一步最容易被跳过)

便宜模型跑出来的检索结果**不会自动就是对的**。拿到结果后:

- 主模型要快速复核一遍返回的文件路径/行号是否准确
- 涉及**同名变量跨 scope、跨作用域引用、多层调用链**的任务,复核时要重点检查是否漏掉边界情况——这正是小模型最容易漏报的地方
- **未经核实的便宜模型输出,不能直接作为后续诊断或修改的依据**——每次都要先抽查

## 核心原则

省 token 的前提是不能牺牲决策质量。如果一个任务的类别本身就模糊不清,这种模糊本身就是"别降级"的信号——一次廉价模型判断错误的代价,远比省下来的那点 token 贵得多。

---

> 别照搬,自己微调。这里给的是思路的骨架,不是一份可以直接粘贴进项目的配置——具体阈值(什么算"混合类"、复核要查到多细)应该根据你自己项目里真实踩过的坑来调整。

</details>
