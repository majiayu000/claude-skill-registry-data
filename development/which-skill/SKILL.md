---
name: which-skill
category: research-analysis
description: Router over this pack's skills and flows. Ask it "which skill fits X" when you don't remember what's available.
disable-model-invocation: true
codex-short-description: "Find the right skill for your situation"
compatibility: claude-code codex opencode
---

# Which Skill

You don't remember every skill in the pack, so ask.

Given the user's situation, name the **one skill** (or the **flow**) that fits, say why in a sentence, and give the exact invocation. If two fit, name both and the distinction. Don't run the skill — point at it and let the user invoke it.

A **flow** is a path through several skills toward one outcome. The flows and their members live in [FLOWS.md](../FLOWS.md) — read it, then route against it. The full one-line inventory is in [CLAUDE.md](../CLAUDE.md#skills-inventory).

## Process

1. **Read the situation.** If it's vague ("help me with this ticket"), ask one clarifying question — which flow are they in (planning? building? triaging?), what's the artifact (Jira ticket? codebase? draft?).
2. **Match to a flow first, then a skill.** Most requests land on a flow in [FLOWS.md](../FLOWS.md); name the flow's entry point. A request that's a single situation (not a chain) maps straight to one skill.
3. **Answer in this shape:**
   - **Skill:** `/skill-name` — one-line why.
   - **Invoke:** the literal command (Codex: `$skill-name`).
   - **Then:** the next skill in the flow, if there is one.
   - **Or:** the sibling to consider, if a close second exists.
4. **When nothing fits,** say so plainly and suggest `/skill-create` — it may be a skill worth building.

## Routing shortcuts

The distinctions people most often need disambiguated:

- **idea-choice vs idea-decision-maker** — `idea-choice` deliberates and writes a pros/cons record; `idea-decision-maker` forces a fast pick with no artifact.
- **grill-me vs grill-with-docs** — same interview primitive; `grill-with-docs` leaves a paper trail (CONTEXT.md, ADRs) and needs a codebase.
- **work-plan vs codebase-plan-refactor** — `work-plan` charts *decisions* for a foggy large effort; `codebase-plan-refactor` produces an *executable* incremental plan for a known refactor.
- **debug vs issue-triage** — `issue-triage` ranks *candidate* root causes from a ticket; `debug` reproduces and fixes *one* bug with a tight loop.
- **break-it-down vs rejection-sensitivity-check vs writing-tone-check** — decode an *incoming* message / calibrate whether an incoming message *warranted the sting* / check how *your outgoing* draft will land.

## Executive-function fast paths

When the user names a *state* rather than a task, route by feeling — the table in [FLOWS.md](../FLOWS.md#executive-function-support--situational-not-a-chain) is the source. E.g. "can't start" → `/task-initiation`; "overcommitted" → `/energy-budget`; "how long will this take" → `/time-reality-check`.

> **Host portability:** tool names follow Claude Code conventions; on other hosts map by intent — see [PORTABILITY.md](../PORTABILITY.md).

<!-- self-evolve:start -->
## Self-Evolve Loop
Journal `~/.ink-and-agency/learnings/which-skill.md` (or workspace-local `.ink-and-agency/` where the sandbox confines writes). Read it first; append what the run taught — [SELF-EVOLVE.md](../SELF-EVOLVE.md).
<!-- self-evolve:end -->
