---
name: writing-cold-open
category: writing
codex-short-description: "Get the first sentence when the blank cursor is winning; 2-3 openings, then steps out"
description: >
  Produce the first sentence of a message when the blank cursor is winning — two or three
  openings matched to relationship and goal, then step out. Use when the user says "cold
  open", "help me start this message", "how do I begin", or invokes /writing-cold-open.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - AskUserQuestion
  - Skill
---

# Cold Open

The user knows what they need to say. They cannot type the first word. The blank cursor is winning. Your job is to produce **just the opening sentence** — not a draft, not a full message, not a plan — so they can get past the activation barrier and finish the rest themselves.

Sibling to [task-initiation](../task-initiation/SKILL.md) (which handles tasks) and [writing-social-script](../writing-social-script/SKILL.md) (which writes the whole script). This one is narrower: just the opener.

## Why usually no council

Cold-open is fast by design. For most cases, run inline — three openings, no debate.

For a high-stakes opener (cold outreach to a stranger, a sensitive message, a message you've drafted and deleted three times), invoke `clarity-council` via `Skill` in single mode with `persona_name=psychologist`:

- **user_problem:** *"Generate three opening sentences for this message. Each should match a different register (direct / warm / contextual). Predict how each will land for the recipient."*
- **context:** the goal of the message + recipient + relationship + channel.
- **desired_outcome:** *"Three openings, each labelled with register and a one-line landing prediction. Nothing else — they'll write the rest."*
- **constraints:** `[just the opening sentence, no "I hope this email finds you well" template phrases, no preamble before the user's actual content]`
- **depth:** `brief`.

## When to activate

When the user says:
- "How do I start"
- "Stuck on the opening"
- "First sentence"
- "I've been staring at this message"
- "Cold open"
- "What do I even say first"

## The questions

Ask in one `AskUserQuestion` call (skip if already answered):

1. **What's the message goal?** (One sentence — the actual ask or update, not the framing.)
2. **Who's the recipient and what's the relationship?**
3. **Channel?** (Email vs Slack vs text — opening conventions differ a lot.)

## Output format

### Three openings

**Direct** — gets to the point in the first sentence:
> [Opening sentence]

**Warm** — one beat of relational acknowledgment, then pivots:
> [Opening sentence]

**Contextual** — names the trigger or shared context first:
> [Opening sentence]

For each, in one line: who it works best for.

### Pick one. Write the rest.

End with a literal nudge:

> **Pick one. Paste it in. Keep typing.**

That's the whole output. Do not offer to write the rest. Do not write subject lines (unless the user asks). Do not offer revisions until the user comes back asking.

## What NOT to do

- Do not write more than three openings — more options = more paralysis
- Do not write past the first sentence — that's not what this skill is for
- Do not use "I hope this email finds you well" or other template phrases
- Do not include a sign-off — the user only needs the opener
- Do not ask "are you sure?" after generating — they came here to be unstuck
- Do not editorialize about how the message should go — just produce the openers

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/writing-cold-open.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
