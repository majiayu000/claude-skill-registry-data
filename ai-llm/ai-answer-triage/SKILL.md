---
name: ai-answer-triage
description: 当想知道一段 AI 回答"哪些能直接用、哪些必须先验证、哪些只能当建议"时使用。按声明类型分四级——低风险草稿材料、观点与策略建议、可查证的事实声明、会改变状态的可执行指令——每级配一句默认处置动作；再按影响半径排序，给出最小的下一步检查。可执行类一律标"不能直接执行；先做代码审阅/沙箱测试/回滚准备"，其中破坏性或提权的命令排在最前。教的是一套可复用的复查习惯，不是替使用者把所有内容都核实一遍：本 skill 只分级、排序、定处置，要逐条核实走 ai-output-fact-checker，整段代码要做入库体检走 ai-code-onboarding-checklist。
category: ai-usage/verification
version: 0.1.1
status: draft
priority: P0
compatible_agents:
  - claude-code
  - codex
  - cursor
  - codebuddy
  - nestudy
  - generic-llm-agent
display_name: AI 回答分级
outputs:
  - chat
max_rounds: 16
suggest_hint: 用「AI 回答分级」把这段回答分成能直接用的、要先验证的和只能当建议的
---

# ai-answer-triage

## Purpose

Help a user decide **which parts of an AI answer are safe to use now, which parts must be verified first, and which parts should only be treated as suggestions**.

This skill is for **risk sorting**, not for silently fact-checking everything. It teaches a repeatable review habit that works across different AI products and agent environments.

## Use this skill when

Use this skill when the user has an AI-generated answer and asks things like:

- “这个回答哪些能直接用，哪些要先核实？”
- “这段 AI 建议靠谱吗？”
- “我该怎么检查这份 AI 方案？”
- “这段代码 / 命令 / 配置能不能直接跑？”
- “这份总结、解释、计划里哪些风险最高？”

Typical inputs:

- a pasted AI answer
- a screenshot or transcript of an AI answer
- a code snippet, shell command, config patch, or checklist produced by AI
- a user question about whether an AI output is safe to apply directly

## Do not use this skill when

- The user wants you to **verify the claims themselves**. Route to `ai-output-fact-checker`, which gives every claim a verification path; triage can still run first to decide which claims go there.
- The input is **a whole block of AI-written code** (a script, a module, a small repo) and the question is whether to trust, run or build on it. Use `ai-code-onboarding-checklist`. When code is only one part of a mixed answer, triage the answer here and hand the code blocks marked "test first" to that skill.
- The user wants you to **improve the prompt before generation**. Use `prompt-brief-builder`.
- The user wants a **handoff summary for a long task**. Use `ai-session-handoff-writer`.
- There is **no actual AI answer to inspect yet**. Ask for the answer first, or help the user prepare a request instead.

## Core rule

**Classify by claim type, not by confidence vibes.**

Do not say “this looks good” or “this seems suspicious” without tying the judgment to the kind of claim being made.

## Required inputs

Ask for the smallest missing piece needed to triage safely:

1. **The AI answer itself** — exact text, code, command, or screenshot.
2. **Intended use** — what the user plans to do with it.
3. **Blast radius** — what breaks if the answer is wrong.

If the answer contains code, commands, configs, medical/legal/financial guidance, or externally checkable facts, those details matter.

## Output contract

Produce these sections in order:

1. **结论** — one short paragraph on what can be used now vs what must wait.
2. **分级表** — each important claim grouped by type, risk, and next action.
3. **先做什么** — the next 1–5 checks, in priority order.

Keep it concise. Do not rewrite the whole answer unless the user asks.

## Claim types and default handling

Classify every material part of the AI answer into one of these buckets.

### A. Low-risk draft material

Examples:

- wording, tone, headline variants
- brainstorming options
- structure suggestions for an outline
- non-factual paraphrases of user-provided content

Default handling:

- **Can usually be used directly with a quick human read**
- Still check fit, tone, and accidental overstatement

Say:

- “可直接当草稿用，但请做一次人工通读。”

### B. Opinion or strategy suggestions

Examples:

- prioritization advice
- product or design suggestions
- tradeoff judgments
- “best approach” recommendations without hard evidence

Default handling:

- **Use as options, not as facts**
- Compare against goals, constraints, and alternatives

Say:

- “可以当候选方案，但不是事实结论。”

### C. Checkable factual claims

Examples:

- dates, policies, prices, limits, quotas, deadlines
- library names, versions, API behavior, command flags
- paper titles, DOI, statistics, laws, regulations
- statements about what a tool, platform, school, or company officially requires

Default handling:

- **Must be verified before being relied on**
- Prefer primary sources or authoritative documentation

Say:

- “在核对来源前不要当成已确认事实。”

### D. Executable or state-changing instructions

Examples:

- code to run
- shell commands
- migration steps
- infra changes
- config edits
- database operations
- automation steps with side effects

Default handling:

- **Must be reviewed and tested before use**
- The bigger the side effect, the stronger the review gate
- Treat destructive, privileged, or production-facing steps as high risk by default
- Ordering (Step 4): destructive or privileged D items go first of everything; other D items come after the factual claims that would cause rework

Say:

- “不能直接执行；先做代码审阅/沙箱测试/回滚准备。”

## Escalation rules

Even if an answer looks polished, automatically raise the risk level when it includes any of the following:

- precise numbers, limits, or dates
- citations, links, laws, standards, or policy statements
- package names, versions, or command-line flags
- hidden assumptions about the user’s environment
- security, privacy, medical, legal, financial, or compliance claims
- production systems, irreversible actions, or large blast radius

## Triage procedure

Follow this procedure every time.

### Step 1: Identify the intended action

Ask: “What will the user do if they trust this answer?”

Examples:

- send it
- publish it
- run it
- submit it
- buy based on it
- change a system based on it

The same sentence can be low-risk in a draft and high-risk in production.

### Step 2: Split the answer into claims

Break the answer into the smallest useful units.

Good units:

- one factual assertion
- one recommendation
- one command block
- one code block
- one policy statement

Do not lump unrelated claims together.

### Step 3: Classify each claim

For each unit, assign:

- **类型**: A / B / C / D
- **风险**: low / medium / high
- **原因**: why this class needs that handling
- **动作**: use now / use as draft / verify first / test first / stop

### Step 4: Prioritize by blast radius

Review first:

1. destructive or privileged commands
2. factual claims that would cause rework, rejection, or embarrassment if wrong
3. code or config changes
4. strategic recommendations
5. low-risk draft wording

### Step 5: Give the smallest next checks

Recommend the minimum practical checks, such as:

- open the official docs page
- compare version/flag names
- run tests locally
- try in a sandbox
- ask the user to confirm one environment assumption
- mark a sentence as opinion rather than fact

## Deterministic checklist

Use this checklist mechanically before finalizing:

- Did you inspect the **actual AI answer**, not just the user’s summary of it?
- Did you state the **intended use**?
- Did you separate **facts**, **opinions**, **draft text**, and **executable steps**?
- Did every high-risk item get a concrete next action?
- Did any code or command get marked **must test first**?
- Did any factual claim with numbers/dates/versions get marked **verify first**?
- Did you avoid claiming that verification already happened if it did not?

## Suggested output template

```markdown
## 结论
- 可直接用：...
- 先别直接用：...

## 分级表
| 项目 | 类型 | 风险 | 为什么 | 下一步 |
|---|---|---|---|---|
| ... | A/B/C/D | low/medium/high | ... | ... |

## 先做什么
1. ...
2. ...
3. ...
```

If tables are awkward in the target environment, use bullet points with the same fields.

## Failure modes to avoid

- giving a vague overall vibe-check without claim-level classification
- calling something “safe” just because it sounds fluent
- treating recommendations as facts
- treating code as trustworthy because it is syntactically plausible
- claiming a link, version, or policy is correct without checking
- recommending a giant verification workflow when 1–2 quick checks would do

## Example scenarios

### Example 1: Marketing copy draft

User asks whether an AI-written product blurb can be used.

Good handling:

- classify most lines as **A. Low-risk draft material**
- flag any performance promises or customer counts as **C. Checkable factual claims**
- recommend a quick human tone pass plus fact verification for claims

### Example 2: Shell command from an AI assistant

User asks whether a suggested command can be run.

Good handling:

- classify the command block as **D. Executable or state-changing instructions**
- identify side effects and assumptions
- recommend dry-run, sandbox, backup, or rollback steps before execution

### Example 3: “This library supports feature X in version Y”

Good handling:

- classify as **C. Checkable factual claim**
- say not to rely on it before checking official docs or release notes

## Boundaries

This skill does **not**:

- perform external verification by default
- guarantee correctness of code, strategy, or facts
- replace testing, review, or source checking
- make risk disappear; it only helps the user spend attention where it matters most

## Handoff note

If the user wants verification after triage, hand over to `ai-output-fact-checker` (code blocks to `ai-code-onboarding-checklist`) and pass along:

- the extracted high-risk claims
- the intended use
- the blast radius
- the recommended check order

That makes the next verification step faster and more reliable.

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | 可执行类（D 类）的处置在 description 与正文统一为"不能直接执行；先做代码审阅/沙箱测试/回滚准备"，去掉容易读成"先跑一下看看"的"必须先实跑"，并写明排序：破坏性或提权的排最前，其余 D 类排在会导致返工的事实声明之后；三条泛称路由改成实名（ai-output-fact-checker、prompt-brief-builder、ai-session-handoff-writer），整段代码转 ai-code-onboarding-checklist | patch |
| 0.1.0 | 2026-08-30 | 初始版本 | minor |
