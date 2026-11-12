---
name: writing-durable-markdown
description: "Use when creating or editing ANY markdown file - CLAUDE.md, a role preamble, a SKILL.md, a runbook, project state, State.md, a spec, a plan, a README, or docs. Fires on adding a rule, writing a note, correcting a wrong claim, recording a lesson, or documenting an incident. Enforces state-the-rule-and-stop, because narrative in a loaded file costs tokens at every wake and leaves contradictions nobody can untangle."
---

# Writing or editing ANY markdown file — state the rule and stop

Not what was done. Not why it was wrong. Not what the previous version said. Not
what not to do. Not the incident. **Just the rule, in the imperative.**

## Before you save: measure

```bash
git diff --numstat -- <file>
```

**More than ~5 added lines for one rule means you wrote a story.** Cut it.

## The three costs

**1. Tokens, paid at every wake, by everyone.** `CLAUDE.md`, role preambles and
state files are injected into every agent's context at every wake. A 40-line
explanation is not paid once by the author — it is paid by every agent, every
session, forever. Inside a session it is worse than linear: injected text is
re-read on every later turn.

**2. Contradiction.** Stories assert facts. Three stories about one rule disagree
about its scope, whether it still applies, and which version is current. **An
agent cannot tell which sentence is authoritative, so it obeys both.** Prose rots
silently — a test goes red when it drifts, a paragraph never does.

**3. Abandonment.** Past a certain size nobody can audit the file for
contradictions, so nobody tries, and the contradictions become permanent.
**The bloat is what makes the file unfixable** — every story added removes
someone's ability to fix the story before it.

## A correction replaces; it does not accumulate

Delete the wrong text and write the right rule in its place. A correction left
*beside* what it corrects leaves two claims and no way to rank them. Corrections
are always longer than what they replace, so this is the main way these files
grow.

## Where the story goes

`thrum memory` — retrieved on demand by the agent who needs it, instead of
injected into everyone. Keep the rule in the doc; leave at most a one-line
pointer.

## Exempt from the cap

Tables, CLI output, command strings, file paths, enumerated vocabularies. **Never
truncate those to hit a line count.** The cap stops narrative; it does not
shorten data.

## Shipped content carries no internal particulars

No issue IDs, no dates, no agent names, no measurements in customer-facing files.
The tracker references the change; the change never references the tracker.

## A directive has no author and no history

State the rule; never name who ruled it. Never show a before-and-after — the
previous wording is deleted, not exhibited.

## A skill is generic — never specific to the repo you edit from

Write the rule so it holds for any repo running the skill. No repo names, config
keys, box names, agent names, or paths particular to the repo you happen to be in.
Repo-specific values live in that repo's config or memory; the skill names them by
role, not by literal.
