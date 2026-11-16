---
name: session-to-skill
description: >
  Auto-extract a reusable skill from the current session conversation.
  Use when the user says "save this as a skill", "turn this into a skill",
  "I want to reuse this workflow", "make this repeatable", "skillify this",
  "we just did something I want to automate", or after completing a useful
  multi-step task that could be repeated.
  Do NOT use for one-off fixes or tasks with no repeatable value.
origin: adapted:NanmiCoder/cc-haha (skillify.ts)
license: MIT
version: 1.0.0
compatibility: "yana-ai >= 0.14.0"
---

<!-- Adapted from cc-haha/src/skills/bundled/skillify.ts (MIT). Logic: session analysis → user interview → SKILL.md generation. Changes: adapted to yamtam SKILL.md format, added Anti-Fake-Pass gates, removed ANT-only constraints. -->

## When to Use

- Use when: user just completed a multi-step workflow they want repeatable
- Use when: user explicitly says "make this a skill" or "I want to automate this"
- Use when: the task has ≥3 distinct steps that follow a clear order
- Do NOT use: for one-off tasks, bug fixes, or exploratory investigations
- Do NOT use: if an equivalent skill already exists — check first

## Pre-check

Before starting, run:
```bash
ls core/skills/ | grep -i "<proposed-name>"
```
If a similar skill exists, suggest updating it instead.

## 4-Step Process

### Step 1 — Analyze the session

Read the conversation and identify:
- What repeatable workflow was just performed?
- What were the distinct, ordered steps?
- What inputs did it require (files, URLs, flags)?
- What was the success criteria?

Write a 1-sentence summary before proceeding.

### Step 2 — Interview the user (use AskUserQuestion)

**Round 1 — Name and scope:**
- Proposed skill name (kebab-case)
- One-line description: "Use when..."
- What should it NOT be used for?

**Round 2 — Steps and inputs:**
- Confirm the step sequence
- What arguments/inputs are required vs optional?
- Any environment requirements (env vars, tools)?

**Round 3 — Trigger phrases:**
- What would the user type to invoke this? (3–5 trigger phrases)
- What signal words make it obvious this skill applies?

### Step 3 — Draft the SKILL.md

Follow the yamtam SKILL.md format:
```markdown
---
name: <skill-name>
description: >
  <one-paragraph description with trigger phrases and Do NOT cases>
origin: session-extracted
version: 1.0.0
---

## When to Use
## Pre-conditions
## Steps
## Anti-Fake-Pass
```

Keep it under 200 lines. One clear thing per step. No padding.

### Step 4 — Show and confirm

Show the complete draft to the user.
Ask: "Does this capture it correctly? Any adjustments before I save?"

Only write the file after explicit approval.

Write to: `core/skills/<name>/SKILL.md`

## Anti-Fake-Pass

```
❌ Creating a skill for a one-off task with no repeatable value
❌ Writing the skill without confirming the step order with the user
❌ Saving without showing the draft first
❌ Skipping the duplicate-check
✅ User explicitly confirmed the draft before saving
✅ Skill has ≥3 distinct steps
✅ Trigger phrases are specific enough to avoid false positives
```
