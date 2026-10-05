---
name: idea-decision-maker
category: research-analysis
description: >
  Force a binary pick when the user is stuck between options — three clarifying questions,
  then a verdict with reasoning. The fast counterpart to idea-choice. Use when the user says
  "I can't decide", "help me pick", "decision paralysis", "break the tie", or invokes /idea-
  decision-maker.
codex-short-description: "Force a binary pick when stuck between options — three questions, then a verdict"
version: 2.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - AskUserQuestion
  - Skill
related-skills:
  - clarity-council
loop-eligible: false
---

# Idea Decision Maker

The user is stuck. Two (or more) options, all roughly defensible, brain spinning. Your job is to **force a pick** with reasoning — not to expand the option space, not to surface more considerations, not to offer a framework. The user has done all that already; that's why they're stuck.

## Lens: senior-architect + devils-advocate + personal-assistant

For non-trivial decisions (anything reversible-but-costly, anything with stakeholders, anything the user has been stuck on for >30 minutes), invoke `clarity-council` via `Skill` in multi mode with personas `[senior-architect, devils-advocate, personal-assistant]`:

- **user_problem:** *"User is stuck between [N] options. Force a pick. Three personas vote. Majority wins. Surface the cost of being wrong and the reversibility, so the user can stop ruminating."*
- **context:** the options + what the user has already considered + any constraints + the deadline pressure.
- **desired_outcome:** *"A picked option, the vote breakdown, the reasoning for the pick, the cost of being wrong, the reversibility, and a deadline for revisiting (if any)."*
- **constraints:** `[do not introduce new options, do not say 'it depends', do not produce a framework, must end with a single pick]`
- **depth:** `brief`.

For trivial decisions (low stakes, fully reversible), skip the council and pick inline.

## When to activate

When the user says:
- "I can't decide between"
- "Help me pick"
- "Which should I"
- "I keep going back and forth"
- "Break the tie"
- "Just tell me what to do"

## The three questions

Ask in one `AskUserQuestion` call:

1. **What are the options?** (Force them to 2-4. If more, ask them to drop the worst ones first.)
2. **What does success look like in 30 days?** (Forces concrete-thinking, exposes hidden constraints.)
3. **What's the cost if you pick wrong?** (And: is it reversible?)

## Output format

### The pick: **[Option name]**

One sentence. No hedging. No "consider X first". The pick.

### Why this one

3-5 bullets. Concrete reasons, not generalities. Reference the user's own success criteria from question 2.

### Why not the others

One bullet per rejected option. Brief but specific — the user needs to feel that the other options were considered, not dismissed.

### Cost of being wrong

| If wrong | Cost | Reversible? |
|---|---|---|
| [option you picked turns out bad] | [what happens] | Yes / No / Partial |

### Revisit point

If the user wants to second-guess, here's the trigger that *would* warrant re-opening the decision:

> **Revisit if:** [concrete signal — e.g., "two weeks pass and you haven't shipped", "the team pushes back in writing", "the API ships breaking changes"]

Until that trigger fires, the decision is closed.

## What NOT to do

- Do not present a framework — frameworks generate more decisions, not fewer
- Do not say "both have merit" — that's where they already are
- Do not pick "it depends" — pick one
- Do not list considerations they should weigh — weigh them yourself
- Do not encourage the user to "trust their gut" — their gut sent them here
- Do not introduce a third option unless it's obviously dominant — that adds paralysis

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/idea-decision-maker.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
