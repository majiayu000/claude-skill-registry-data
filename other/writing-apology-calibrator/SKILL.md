---
name: writing-apology-calibrator
category: writing
description: >
  Calibrate a drafted apology — strip reflexive over-apology, keep warranted accountability.
  Use when the user says "calibrate this apology", "am I over-apologizing", "apology check",
  "did I say sorry too much", or invokes /writing-apology-calibrator.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Read
  - AskUserQuestion
  - Skill
---

# Apology Calibrator

The user drafted an apology. Their first draft is almost certainly over-calibrated — too many sorries, too much self-blame, taking responsibility for things that weren't their fault, apologizing in advance for being a burden by sending the apology in the first place.

Your job is to keep the **accountability** and cut the **over-apology**. There's a difference: accountability lands cleanly, repairs trust, and ends the matter. Over-apology lands awkwardly, makes the recipient have to reassure the apologizer, and prolongs the discomfort.

Sibling to [writing-tone-check](../writing-tone-check/SKILL.md). Tone-check is general; this one is specifically the apology shape.

## Lens: psychologist + devils-advocate

This skill always invokes `clarity-council` via `Skill` in multi mode with personas `[psychologist, devils-advocate]`:

- **user_problem:** *"Calibrate this apology draft. Strip over-apology while keeping warranted accountability. Identify which 'sorrys' are reflexive vs. earned."*
- **context:** the draft + what the user actually did (or thinks they did) + the relationship + whether harm actually occurred.
- **desired_outcome:** *"A line-by-line annotation (keep / cut / soften), a calibrated rewrite, and a one-line read on whether this apology was even needed."*
- **constraints:** `[do not strip accountability where it's warranted, do not flatten warmth into clinical detachment, name the cognitive pattern when over-apology is operating, do not add 'no worries' style burden-shifting]`
- **depth:** `standard`.

Always run the council — the second perspective is the value, just like writing-rejection-sensitivity-check.

## When to activate

When the user:
- Pastes an apology draft and asks for a check
- Says "is this too much"
- Says "am I over-apologizing"
- Sends an apology after the fact and is now spiraling about how it came across

## The questions

Ask in one `AskUserQuestion` call (skip any the user already answered):

1. **What's the apology draft?**
2. **What actually happened?** (One sentence — not the apology, the *event*.)
3. **Who's the recipient and what's the relationship?**

## Output format

### Was an apology needed?

A one-line read: **Yes (warranted)** / **Yes (proportional courtesy)** / **No (reflexive — you didn't owe one)**.

If the answer is "no, you didn't owe one", explain in one sentence what the user is actually apologizing for (often: existing, taking up space, having needs, being late by 4 minutes). Offer to skip the rewrite and just suggest *not sending it*.

### Line-by-line annotation

Show the original draft. For each apology-related phrase, annotate:

- **Keep** — this is warranted accountability and lands cleanly
- **Soften** — this is over-strong; suggested replacement
- **Cut** — this is reflexive over-apology that adds nothing; remove
- **Add** — something missing (rare; usually only if a concrete repair/fix wasn't named)

### Calibrated rewrite

The full apology, rewritten with the annotations applied. Same voice as the user, just calibrated.

### Why the cuts

A few sentences explaining the *pattern* (not the specific lines) — what reflexive apology is doing in this draft, so the user can notice it next time. Be specific: "You apologized for the existence of the message itself in the opening line, that's the masking-tax tell."

## What NOT to do

- Do not strip out apology where the user actually owes one — the goal is calibration, not minimization
- Do not add "no worries!" style burden-shifting back onto the recipient
- Do not lecture about over-apologizing as a pattern (one sentence in "Why the cuts" is enough)
- Do not produce a robotic "I take responsibility for X. Going forward I will Y." — that's not calibration, that's a different problem
- Do not invalidate the user's instinct to apologize — instinct is fine, the calibration is the work

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/writing-apology-calibrator.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
