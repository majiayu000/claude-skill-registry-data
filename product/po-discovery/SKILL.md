---
model_tier: inherit
name: po-discovery
description: "Use when shaping a fuzzy product ask into a refined backlog item — problem framing, user-story rewrite, AC tightening — even if the user just says 'help me write this ticket'."
personas:
  - product-owner
  - stakeholder
domain: product
workspaces:
  - product
packs:
  - product-basic
trust:
  level: professional
install:
  removable: true
---

# po-discovery

> Take a vague product request and return a **problem-framed**,
> **user-story-shaped**, **AC-tight** backlog item ready for refinement.
> Output is copy-paste ready; write-back to the tracker is user-gated.
> Sibling of [`refine-ticket`](../refine-ticket/SKILL.md) — that one
> tightens an existing ticket, this one shapes the *raw input* before
> a ticket exists.

## When to use

- The user pastes a fuzzy idea ("we should let users export their data")
  and asks to turn it into a ticket.
- A stakeholder request arrives without a clear problem statement.
- Acceptance criteria are missing, contradictory, or written as
  implementation steps instead of observable outcomes.
- German triggers: "schreib daraus ein Ticket", "ist die Story klar?",
  "AC fehlen noch".

Do NOT use when:

- A ticket already exists and needs tightening — route to
  [`refine-ticket`](../refine-ticket/SKILL.md).
- The ask is already a clear, well-formed user story with measurable
  AC — skip discovery and proceed to estimation.
- The request is an engineering task with no product framing
  ("upgrade Laravel to 11") — discovery adds noise; skip.

## Procedure

### 1. Capture the raw input and identify the asker

Read the user's text verbatim. Do NOT rephrase yet. Identify: who is
the asker (PO, support, eng, exec)? What artefact did they hand over
(slack thread, screenshot, voice note transcript, free text)?

### 2. Frame the problem

Answer four questions, every answer cited from the input or marked
`unknown`:

| Question | Why it matters |
|---|---|
| Who has the problem? | Personas, segments, internal vs external |
| What outcome do they want? | Distinguishes need from solution |
| What is the current pain or workaround? | Sizes the gap |
| What changes if we ship this? | Surfaces success signals |

Any answer marked `unknown` blocks story shaping — surface the gap
back to the user before continuing.

### 3. Shape the user story

Use the canonical form: *As a `{persona}`, I want `{capability}`, so
that `{outcome}`*. Capability ≠ implementation. If the input says
"add a CSV button", reframe to "I want my data in a portable format,
so that I can use it outside the product".

### 4. Tighten acceptance criteria

Each AC is **observable**, **binary** (passes or fails), and **does
not name an implementation**. Use Given / When / Then or a numbered
list. Reject ACs that hide assumptions ("works correctly", "is fast
enough") — replace with measurable thresholds or strike them.

**Cross-source discrepancy scan** (per [`cross-source-consistency`](../../rules/cross-source-consistency.md), gated by `consistency.cross_source`): when the raw input includes a screenshot / mockup alongside the story text, check the sources against each other and surface any conflict as a `gap` / open question — never resolve it silently. Watch for: story text contradicting an attached screenshot; the AC contradicting the description; a clearly-needed behavior the input never states (weekend/holiday shift, empty/error state). Batch them into one clarifying question. Taxonomy: [`cross-source-consistency-mechanics`](../../../docs/guidelines/agent-infra/cross-source-consistency-mechanics.md).

### 5. Surface non-functional gaps

Flag anything missing that downstream skills will need: success
metric, target users, rollout window, accessibility, security or
privacy boundary, multi-tenant scope. Do NOT invent values — list
them as `gap` items for the user to fill.

## Output format

```
Asker:    <role / name>
Source:   <slack / email / verbal / pasted text>
Problem:  <one sentence — who, want, why>

User story:
  As a <persona>, I want <capability>, so that <outcome>.

Acceptance criteria:
  1. Given <state>, when <action>, then <observable result>.
  2. ...

Open gaps (block estimation):
  - <gap 1>
  - <gap 2>

Suggested next step: /refine-ticket  |  /estimate-ticket  |  fill gaps
```

If gaps remain, surface them and stop — do NOT push to estimation.

## Gotcha

- If the asker is the agent itself (autopilot, roadmap), still run the
  full procedure — the gap list is what catches the agent inventing
  requirements.
- "Outcome" is what the user *gets*, not what we *build*. "Faster
  page" is an outcome; "switch to Postgres" is an implementation.
- AC count is not a quality signal. Three sharp AC beat eight vague
  ones; merge or split as needed.

## Do NOT

- Do NOT write code, plan tasks, or estimate effort — those are
  downstream skills.
- Do NOT silently fill gaps with plausible-looking defaults; the
  whole point of discovery is to surface what the user has not
  decided.
- Do NOT rewrite the asker's wording into agent voice in the
  Problem field — preserve their framing so they recognise it.
- Do NOT push the rewritten ticket into Jira / Linear without the
  user explicitly asking — output is copy-paste ready, write-back
  is gated.
