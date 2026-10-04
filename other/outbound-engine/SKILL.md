---
name: outbound-engine
description: Design, analyze, and optimize cold outbound email campaigns on Instantly. Handles end-to-end ICP definition, expert panel scoring (recursive to 90+), sequence copywriting, infrastructure audit, capacity planning, and an implementation/strategy doc for human review. Use when asked to build cold outbound sequences, optimize cold email, audit an outbound motion, write sales sequences, or design cold email campaigns. Supports "start from scratch" and "optimize existing" modes. Execution skill — it produces copy, math, and a doc; it does not auto-send. Requires Instantly for audit/send features.
when_to_use: |
  Use when asked to build cold outbound email sequences from scratch, optimize existing cold email campaigns, audit outbound infrastructure (sending accounts, warmup scores, domain inventory), define or refine ICP parameters, score email copy with a recursive expert panel, or generate capacity math and weekly metrics targets for an outbound motion.

  Platform dependency: the audit script, send script, and deliverability rules are Instantly-specific (Instantly v2 API, `{{firstName}}`-style variable syntax). The workflow, copy rules, expert panel, and capacity math are platform-agnostic. If the user runs Apollo, Lemlist, Smartlead, or another platform, surface this before proceeding — the strategy and copy still apply, but skip the audit/send scripts and adapt variable syntax to their platform.

  Not when: the request is intake/scoping with no defined ICP, sequence goal, or campaign structure — use `marketing-shaper` to produce the brief first, then bring it here. `outbound-engine` handles execution (sequences, copy, infrastructure, capacity), not strategy definition. Not when the task is drafting follow-ups from a specific sales-call (Gong) context — use `revenue-intelligence`; this skill owns cold-sequence building and delivery. Not when the request is A/B test design or statistical analysis of outbound variants across the wider motion — use `growth-engine` for the experiment framework; come back here for the copy variants it tests. Not when the request is general marketing campaign planning across multiple channels — use `marketing-shaper`.
compatibility: Requires Bash (Python 3 where scripts are invoked). Works in Claude Code and Codex via install.sh.
---

# Outbound Engine

End-to-end cold outbound: ICP definition, expert panel copy scoring (recursive to 90+), infrastructure audit, capacity planning, and an implementation doc. This skill **produces a strategy doc and ready-to-load copy for human review** — it does not send. See `references/workflow.md` for the full procedure.

## Core Rules

1. Determine mode first (existing Instantly account with API key, or starting from scratch) before any other step.
2. Run the three-phase workflow: Discovery & Audit → Expert Panel Recursive Scoring → Deliverables.
3. Expert panel scoring target is 90/100 — non-negotiable. Iterate until reached.
4. Show every scoring round in the final doc — the iteration trail is part of the value.
5. **Never send or push to the platform autonomously.** This skill's output is a doc for human review. Writes/sends happen only after explicit human approval — see the Sending gate below.
6. Use capacity math to set realistic volume and pipeline projections.

## Operating Modes

**Optimize existing** — there is a live account to learn from. First questions: (1) Do you have an Instantly API key? (2) Which campaigns are underperforming, and on what metric? (3) Is there historical data to pull? With an API key, run `scripts/instantly-audit.py` to pull campaigns, account inventory, and warmup scores before touching copy.

**Start from scratch** — no campaigns yet. First questions: (1) Who is the ICP (titles, industries, company size)? (2) What do you sell, in one jargon-free sentence, and what is the primary offer (audit, trial, demo, call)? (3) What proof points are real and linkable? Use `assets/icp-template.md` to collect the ICP before writing copy.

## The Three Phases (summary)

1. **Discovery & Audit** — Determine mode. If audit mode, run the Instantly audit and flag any account with warmup score <80 or <14 days as NOT ready. Define the ICP, capture business context (offer, real URLs, proof points), and confirm the expert-panel roster. Detail in `references/workflow.md`; ICP fields in `assets/icp-template.md`.
2. **Expert Panel Recursive Scoring** — Draft the sequence, then score it with the 10-expert panel (`references/expert-panel.md`), each scoring through their own lens. Each round emits a per-panelist score table, an aggregate, the top weaknesses, the edits made, and the revised copy. Score honestly — no padding to 90. Below 90: fix the top 3 weaknesses and run another round. At ≥90: finalize. Copy must follow `references/copy-rules.md` (and `references/instantly-rules.md` for Instantly variable/deliverability rules).
3. **Deliverables** — Produce the strategy doc: brutal-truth analysis, ICP summary, infrastructure status, every scoring round, final copy for every step, implementation plan, capacity math, weekly metric targets, and STOP/START lists. Full doc structure in `references/workflow.md`.

## What the 90/100 Gate Means

90 is an operational gate, not a vibe. It means the aggregate average across all panelists hit 90 in a single round with no score padded to get there. Below 90, the copy is not done — identify the lowest-scoring lenses, address those specific weaknesses, and re-run. The point of the recursive trail is that each round names a concrete weakness and the edit that fixed it; ship the trail, not just the final copy.

## Sending Gate (resolves Rule 5)

`scripts/cold-outbound-sender.py` and the write paths in `scripts/instantly-audit.py` exist but are **gated**. The default deliverable is the strategy doc. Do not invoke the sender or perform any platform write autonomously. Invoke `cold-outbound-sender.py` only when the human has explicitly confirmed the strategy doc is reviewed and approved AND explicitly asks to send. Always run `--dry-run` first and show the result before a live send. Never treat "build the campaign" as authorization to send.

## Scope Note

The core skill is the three-phase design workflow above. Three scripts ship in this directory but sit **outside** that workflow and should not run unprompted: `scripts/lead-pipeline.py` (Apollo→LeadMagic→Instantly sourcing), `scripts/competitive-monitor.py` (competitor tracking), and `scripts/cross-signal-detector.py` (multi-source signal detection). Use them only on an explicit, specific request for that function.

## Reference Files

| File | Purpose |
|------|---------|
| `references/workflow.md` | Full three-phase workflow with scoring criteria and doc structure |
| `references/capacity-math.md` | Capacity formula, weekly metrics targets, add-on recommendations |
| `references/instantly-rules.md` | Instantly variable syntax, sequence structure, deliverability rules |
| `references/expert-panel.md` | Default 10-expert roster with scoring lenses |
| `references/copy-rules.md` | Email copy rules (first sentence, CTA, stats framing) |
| `assets/icp-template.md` | ICP data collection template |
| `scripts/instantly-audit.py` | Pulls campaigns, accounts, warmup scores via Instantly v2 API (write paths gated) |
| `scripts/cold-outbound-sender.py` | Sends approved emails — gated; human approval required (see Sending Gate) |

## Related skills

- [content-ops](../content-ops/SKILL.md) — expert-panel quality gate; the recursive 90+ scoring of sequence copy is a content-ops review pass
- [marketing-shaper](../marketing-shaper/SKILL.md) — produces the scoped outbound brief (ICP, goal, structure) this skill executes from
