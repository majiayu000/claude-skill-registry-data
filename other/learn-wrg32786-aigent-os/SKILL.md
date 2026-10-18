---
name: Learn
description: When the principal is in learning mode (reading a repo, watching a talk, processing a new tool), /learn takes a brief input and produces a structured note in vault/concepts/learning/ with category, modern-stack location, relevance verdict, and reconsideration triggers. Captures the value of every learning sweep without requiring it to immediately translate to building.
---

# Learn

The learning compounding skill. Most principals lose the value of a learning sweep within 48 hours — they read three repos, watch one talk, evaluate two tools, and a week later can't remember what they decided about any of them. `/learn` captures the structured outcome of every such sweep.

## When to use

- The principal has just read a repo, paper, talk, or tool description
- The principal is evaluating something but doesn't have an immediate need
- The principal asks "should I be using X?" or "what did we decide about Y?"
- After any session where the input was *learning*, not *doing*
- Triggered by Caddy on prompts like: "/learn", "I just read", "evaluating", "looked into", "should I use", "what did we decide about", "captured this", "interesting tool", "considered tool"

## How to execute

### Step 1 — Take the input

The principal provides:
- **Subject:** the thing being evaluated (tool, technique, concept, repo, paper, idea)
- **Source:** where it came from (URL, talk title, conversation, repo name)
- **Snapshot:** 2-5 sentences on what the thing is and what it claims to do

If any field is missing, ask one focused question to get it.

### Step 2 — Locate it on the modern AI stack

Reference [[Modern AI Infrastructure Stack]]. Place the subject at the right layer:
- Application
- Persistence
- Messaging
- Isolation
- Compute
- Observability
- Orchestration

If it doesn't fit cleanly on the stack, it's either a doctrine concept (note that explicitly) or an artifact-of-AI-trends category (e.g., "agent framework", "prompt-engineering pattern").

### Step 3 — Assess relevance

Three categories:

- **ADOPT** — fits an actual current bottleneck. Action follows.
- **HOLD** — could fit in a future state, but no current bottleneck. Capture the trigger condition.
- **REJECT** — wrong category, wrong scale, or violates a load-bearing constraint. Capture the reasoning.
- **MONITOR** — interesting but no clear path. Re-evaluate next quarter.

### Step 4 — Capture reconsideration triggers (for HOLD only)

What specific change in circumstances would flip the decision?
- "When the framework starts spawning >10 parallel agents, reconsider isolation tools."
- "When a downstream user can't sandbox safely, reconsider authority gates."
- "When the principal hits the 10K-note vault size, reconsider semantic search alternatives."

The trigger has to be observable. "When we have more time" isn't a trigger. "When DECISION_OUTCOMES.md shows 5+ failed Authority Level 1 actions in a quarter" is.

### Step 5 — Write the note

File: `vault/concepts/learning/<subject-slug>.md`

Format:

```markdown
---
title: {Subject}
tags:
  - learning
  - {category}
status: ADOPT | HOLD | REJECT | MONITOR
stack-layer: {layer or N/A}
created: YYYY-MM-DD
last-reviewed: YYYY-MM-DD
source: {URL or reference}
---

# {Subject}

## What it is

{2-5 sentences from the input}

## Stack location

{One paragraph on where it sits in the modern AI stack and what category it competes in}

## Verdict

**{ADOPT | HOLD | REJECT | MONITOR}**

{1-3 sentences on the reasoning}

## Reconsider when

{Trigger condition, only for HOLD; for REJECT, "Never (fundamental rejection)"; for ADOPT, this becomes "Adopted on YYYY-MM-DD; re-evaluate annually"; for MONITOR, "Re-evaluate next quarter"}

## Connects to

{Wikilinks to related vault notes — other tools in the same category, doctrine that applies, relevant projects}
```

### Step 6 — Update the index

Append a one-line entry to `vault/concepts/learning/INDEX.md`:

```
- [[{subject-slug}]] — {category} — {ADOPT|HOLD|REJECT|MONITOR} — {YYYY-MM-DD}
```

The INDEX.md is the principal's external memory of considered tools. When they hit a real problem and need to remember "did I look at X?", the index answers in one read.

## Anti-patterns this prevents

- Learning sweeps that produce no captured artifact, then are forgotten
- Re-evaluating the same tool from scratch six months later
- Not knowing whether a tool was rejected or just unread
- Reconsider triggers that exist in the principal's head but aren't written down (so they never fire)
- Adopting a tool because it's "cool" without locating it on the stack or assessing fit

## Connects to

- [[Modern AI Infrastructure Stack]] — the layer map used for placement
- [[What I Am Not Building]] — REJECT entries from `/learn` graduate here when worth permanent doctrine
- [[Bio-hacking Posture]] — `/learn` is the supplements-and-restriction-evaluation skill
- `vault/concepts/learning/INDEX.md` — the running index this skill maintains
