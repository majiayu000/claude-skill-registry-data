---
name: rejection-sensitivity-check
category: exec-function
codex-short-description: "Calibrate a message that stung: separate evidence from interpretation"
description: >
  Calibrate a message that stung — separate evidence from interpretation, score how much
  sting is warranted. Use when the user says "did they mean it that way", "is this
  criticism", "am I reading this wrong", "this stung", or invokes /rejection-sensitivity-
  check.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - Read
  - AskUserQuestion
  - Skill
related-skills:
  - clarity-council
loop-eligible: false
---

# Rejection Sensitivity Check

A message landed harder than expected. The user wants to know: is this actually critical, or am I reading hostility into something neutral? This skill separates the **evidence in the text** from the **interpretation the brain layered on top**.

Sibling to [break-it-down](../break-it-down/SKILL.md). Break-it-down is general decoding; this one is specifically for messages that triggered a rejection-sensitive reaction.

## Lens: psychologist + devils-advocate

This skill always invokes `clarity-council` via `Skill` in multi mode with personas `[psychologist, devils-advocate]`. The two-persona setup is the whole point — psychologist reads the text neutrally, devils-advocate stress-tests both the worst-case and the best-case reading.

- **user_problem:** *"The user received this message and it stung. Separate what the text actually says from what the user's pattern-matching is adding. Calibrate whether the sting is warranted."*
- **context:** the message + relationship + what the user is afraid it means + recent history with sender if shared.
- **desired_outcome:** *"A side-by-side: evidence vs. interpretation. A calibrated read (1-5 scale). A worst-case and a best-case interpretation. A recommended response stance."*
- **constraints:** `[do not invalidate the feeling, do not over-validate the worst-case reading, cite specific words from the message, name the cognitive distortion if one is operating]`
- **depth:** `standard`.

Never skip the council for this skill — the second perspective is the value.

## When to activate

Activate when the user pastes a message that landed badly and asks if they're overreacting, misreading, or seeing things that aren't there. Ask:

1. **What did you read into it?** (Their interpretation, before yours.)
2. **What's the relationship?** (Recurring sender? Authority? Peer?)
3. **How are you feeling physically?** (RSD is often a body response — naming it helps.)

## Output format

### What the text actually says

A neutral, evidence-only restatement. No reading-between-lines, just what's literally on the page.

### What your brain is adding

The user's interpretation, restated back to them without judgment. Name it as interpretation, not fact.

### Evidence-vs-interpretation table

| Their phrase | Neutral read | RSD read | Evidence weight |
|--------------|--------------|----------|-----------------|
| [phrase] | [neutral interpretation] | [worst-case interpretation] | Low / Medium / High |

The evidence weight is how much the text *itself* supports the RSD reading — not how plausible it feels.

### Calibrated sting score

**Warranted sting: [1-5]**

- 1: Almost certainly neutral — the text contains no critical signal.
- 2: Mostly neutral with one ambiguous phrase.
- 3: Genuinely mixed — could go either way.
- 4: Critical but proportionate to the situation.
- 5: Critical and disproportionate or hostile.

One-sentence rationale.

### Worst-case vs best-case reading

**Worst-case:** [the most negative plausible interpretation]
**Best-case:** [the most charitable plausible interpretation]
**Most likely:** [where the evidence actually points]

### Recommended response stance

- **If they meant the worst-case:** [response]
- **If they meant the best-case:** [response]
- **Safe middle response that works for both:** [response]

## What NOT to do

- Do not say "you're overreacting" — this is the voice in their head already
- Do not invalidate the feeling — RSD is real even when the reading is wrong
- Do not over-validate the worst case to seem supportive
- Do not assume the sender is neurotypical or has emotional fluency
- Do not recommend a response that requires emotional labor the user can't afford right now

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/rejection-sensitivity-check.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
