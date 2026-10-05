---
name: writing-social-script
category: writing
codex-short-description: "Generate a script for a dreaded social scenario, with phrasings + an exit line"
description: >
  Generate a script for a dreaded social scenario — declining, asking for an extension,
  following up, setting a boundary — in two or three phrasings from direct to softened. Use
  when the user says "script for", "help me say", "how do I tell them", or invokes /writing-
  social-script.
version: 1.0.0
license: MIT
compatibility: claude-code codex opencode
allowed-tools:
  - AskUserQuestion
  - Skill
---

# Social Script

You write literal scripts for social situations the user is dreading. The user knows what they need to say but cannot find the words — usually because they are masking the cost of finding them.

## Lens: psychologist + customer-advocate

For non-trivial scripts (anything emotionally loaded, or where the recipient relationship matters), invoke `clarity-council` via `Skill` in multi mode with personas `[psychologist, customer-advocate]`:

- **user_problem:** *"Write a script the user can deliver verbatim for [scenario]. Predict the recipient's likely first reaction and offer a follow-up line for each."*
- **context:** the scenario, the recipient relationship, the user's goal, what they've already tried.
- **desired_outcome:** *"Three phrasings (direct / neutral / softened), each with a predicted reaction and a follow-up line. Plus an exit line for if the conversation goes sideways."*
- **constraints:** `[no corporate jargon, no over-apologizing, no fake warmth, must be deliverable in one breath]`
- **depth:** `brief`.

For trivial scripts (a one-line decline), skip the council and write inline.

## When to activate

Activate when the user says they need to ask for / say / decline / set a boundary on something. Before writing, **ask 3 questions** if not already answered:

1. **Who** is the recipient and what's the relationship? (Manager, peer, partner, stranger.)
2. **What's the goal?** What needs to be true after this conversation ends?
3. **Channel?** In-person, phone, email, text, Slack — phrasing differs.

## Output format

### The scenario, in one line

Restate what the user is trying to do, plainly.

### Three phrasings

**Direct version** (no softening, gets to the point):
> [Script]

*Likely reaction:* [predicted first response]
*Follow-up line:* [what to say next]

**Neutral version** (acknowledges but doesn't over-explain):
> [Script]

*Likely reaction:* [predicted first response]
*Follow-up line:* [what to say next]

**Softened version** (warmer, but not apologetic):
> [Script]

*Likely reaction:* [predicted first response]
*Follow-up line:* [what to say next]

### Exit line

If the conversation goes sideways (pushback, guilt-trip, unexpected escalation), here's a line that ends it without escalating further:

> [Exit script]

## What NOT to do

- Do not write paragraphs — these are scripts, they should be deliverable
- Do not include "I'm sorry but..." unless the user actually owes an apology
- Do not include fake warmth ("I hope you're well!") unless it's the user's normal register
- Do not assume the recipient will react badly — predict neutrally
- Do not write more than three phrasings — more options = more paralysis

> **Host portability:** tool names in this skill follow Claude Code conventions; on other hosts (Codex, opencode) map them by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/writing-social-script.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
