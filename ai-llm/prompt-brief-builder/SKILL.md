---
name: prompt-brief-builder
description: 当需求还只是"帮我写个东西""让 AI 做这个任务"这种一句话时使用。用至多 3–5 个高杠杆追问把它补成一份可交付的任务简报——目标、产物、受众、已有素材、约束、验收标准、不做什么、待确认假设，外加一段可直接粘贴的执行 prompt。简报的九个标题保持英文（内容用什么语言都行），字段完整性由 scripts/check_brief.py 校验。产出不绑定任何一家模型，人或 Agent 都能照着执行。不适用于：写歌交给 lyric-concept-builder，复习计划交给 deadline-to-study-plan，建模题交给 modeling-problem-reading-coach，物理题交给 physics-problem-router；使用者坚持直接要成品、一个问题都不肯答时也不用本 skill。
category: ai-usage/prompting
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
display_name: 任务简报生成器
outputs:
  - document
max_rounds: 16
suggest_hint: 需求还是一句话时，先用「任务简报生成器」补成目标、约束和验收标准都齐的简报
---

# prompt-brief-builder

## Purpose

Convert a fuzzy request such as “help me write something” or “make an agent do this task” into a compact, execution-ready brief.

This skill is **agent-agnostic**:
- it does not depend on any single model vendor;
- it does not assume hidden tools, private APIs, or proprietary prompt syntax;
- its output should be usable by a human, a coding agent, a writing agent, or a general-purpose assistant.

## Use this skill when

Use this skill when the requester has a goal but the task is still underspecified, for example:
- the desired deliverable is unclear;
- the audience or user is unclear;
- constraints are missing;
- success criteria are missing;
- the requester knows what they want changed but cannot yet state the task crisply.

Typical triggers:
- “帮我写个东西 / help me write something”
- “给 AI 一个更清楚的任务”
- “把这个想法整理成能执行的 brief”
- “我不知道该怎么提问，但我知道我要什么结果”

## Do not use this skill when

Do **not** use this skill when:
- the task is already precise enough to execute directly;
- the real need is domain reasoning rather than clarification;
- the request already belongs to a domain skill in this library: a song → `lyric-concept-builder`; a revision or study plan → `deadline-to-study-plan`; a modeling-competition problem → `modeling-problem-reading-coach`; a physics problem → `physics-problem-router`;
- the user needs brainstorming, not scoping;
- the user is asking for a final artifact and not willing to answer even minimal clarification. Step out: stop asking, write no brief, and let normal writing produce the piece. You may state in one or two lines the assumptions you inferred (audience, length, tone) so the user can correct them.

If the request is already complete, skip the interview and return a finished brief immediately.

## Required outcome

Produce a brief that covers these fields:
1. objective
2. deliverable
3. audience or consumer
4. available inputs or source material
5. constraints
6. acceptance criteria
7. non-goals / out of scope
8. open questions or explicit assumptions

If a field cannot be confirmed, mark it as one of:
- `Unknown`
- `Assumption: ...`
- `Needs user confirmation`

Write these three labels in English exactly as shown, like the headings, even when the rest of the brief is Chinese.

Never silently invent missing facts.

## Operating principles

1. **Ask fewer questions, not more.** Ask only the smallest set of questions that materially improves execution.
2. **Prefer high-leverage clarification.** Ask about deliverable, audience, constraints, and success criteria before cosmetic preferences.
3. **Reuse what the user already said.** Do not ask for information already present in the conversation.
4. **Separate facts from assumptions.** Label assumptions explicitly.
5. **Keep the brief portable.** Avoid vendor-specific prompt markup unless the user explicitly asks for it.
6. **One brief, one job.** If the request actually contains multiple jobs, split them.

## Workflow

### Step 1: Identify the job shape

Classify the request along these axes:
- **task type**: writing / coding / research / analysis / planning / design / mixed
- **target artifact**: email / spec / code change / summary / plan / checklist / slide / other
- **primary consumer**: human / agent / team / public audience / unknown

If the request mixes multiple artifact types, propose a split.

### Step 2: Extract known information

Before asking anything, draft a partial brief from the user’s existing message.

Create a working table:

| Field | Status | Notes |
|---|---|---|
| Objective | known / partial / missing | ... |
| Deliverable | known / partial / missing | ... |
| Audience | known / partial / missing | ... |
| Inputs | known / partial / missing | ... |
| Constraints | known / partial / missing | ... |
| Acceptance criteria | known / partial / missing | ... |
| Non-goals | known / partial / missing | ... |

Ask questions only for fields that remain partial or missing and matter for execution.

### Step 3: Ask 3–5 targeted questions at most

Default ceiling: **5 questions total**.

Prioritize in this order:
1. What exactly should be produced?
2. Who is it for?
3. What constraints must be respected?
4. How will we judge success?
5. What should be avoided or left out?

If the user is in a hurry, ask fewer questions and surface assumptions instead.

### Step 4: Build the brief

Return a concise brief using the template below. Prefer crisp bullets over long prose.

## Output template

Keep the nine `##` headings exactly as written, in English, even when the user writes in Chinese; write the content under them in the user's language. `scripts/check_brief.py` matches the headings literally, so a brief with translated headings (`## 目标`) fails as "missing required headings".

```md
# Task Brief

## Objective
- ...

## Deliverable
- Artifact:
- Format:
- Depth / length:

## Audience
- Primary audience:
- Secondary audience:
- What they already know:

## Available Inputs
- ...

## Constraints
- Must include:
- Must avoid:
- Time / deadline:
- Tool / environment limits:

## Acceptance Criteria
- ...

## Non-Goals
- ...

## Open Questions / Assumptions
- ...

## Suggested Execution Prompt
...one portable prompt or instruction block that another agent/human could use directly...
```

## Brief quality bar

A good brief is:
- specific enough that another capable agent can start work immediately;
- scoped enough that success and failure are distinguishable;
- honest about missing information;
- portable across agent environments;
- short enough to scan in under two minutes.

## Failure modes to avoid

Avoid these common mistakes:
- asking generic discovery questions with no execution value;
- producing a long prompt instead of a brief;
- hiding important uncertainty;
- mixing requirements with preferences;
- turning one vague task into an overengineered questionnaire;
- embedding tool assumptions the next agent may not have.

## Adaptation rules

### If the user wants speed
- ask 1–3 questions only;
- fill remaining gaps with clearly labeled assumptions;
- produce a “good enough to start” brief.

### If the user wants precision
- ask up to 5 questions;
- convert fuzzy adjectives into testable criteria;
- restate ambiguous success metrics as observable checks.

### If the user wants to hand work to another agent
- keep the final brief environment-neutral;
- do not assume hidden memory or prior context;
- include the minimum necessary background inline.

## Deterministic validation

Use `scripts/check_brief.py` to validate a generated brief against the required section set:

```bash
python3 scripts/check_brief.py path/to/brief.md
python3 scripts/check_brief.py --selftest
```

The validator checks for:
- presence of all required headings (exact English headings; trailing spaces and letter case do not matter);
- empty placeholder headings: a section is empty when it holds only blank lines, template filler (`...`, `- ...`, `...instruction text...`) or labels with no value (`- Artifact:`); a label followed by indented sub-items counts as filled, and a section where only some labels are empty gets a warning;
- whether the brief contains at least one acceptance criterion as a list item;
- whether unresolved uncertainty is labeled instead of silently omitted.

Exit codes: 0 means the structure is valid (warnings may remain), 1 means missing or empty sections or no acceptance criterion, 2 means the file cannot be read. The template in this file, run as-is, fails; that is part of the self-test.

## Files in this skill

- `SKILL.md` — usage rules and workflow
- `templates/brief-template.md` — reusable brief skeleton
- `scripts/check_brief.py` — optional structural validator

## 变更记录 / Changelog

| 版本 | 日期 | 变更 | 类型 |
|---|---|---|---|
| 0.1.1 | 2026-09-26 | check_brief.py 修正：只有模板占位（`...`、空标签 `- Artifact:`）的节判为空，SKILL 自带模板原样跑不再通过；标题行尾多空格不再误判空节，标题改按整行匹配；改用 argparse（--help 不再被当成文件名），目录与不可读文件报错退出 2，补 --selftest；正文写明九个标题和三个不确定性标签保持英文；"不适用于"补实名分流（写歌、复习计划、建模题、物理题），使用者坚持要成品时退出本 skill，与用例 Case 4 一致 | patch |
| 0.1.0 | 2026-08-30 | 初始版本：可移植的任务简报与最少追问 | minor |
