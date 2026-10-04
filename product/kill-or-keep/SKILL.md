---
name: kill-or-keep
description: Quarterly portfolio review with forced verdicts (DOUBLE-DOWN / MAINTAIN / MINIMAL / KILL) for every product.
---

# /kill-or-keep

Usage: `/kill-or-keep` (run quarterly, end of quarter)

## What this does
Invokes `agents/portfolio/kill-or-double-down/`. Produces a full portfolio review document at `brain/decision-log/portfolio-review-YYYY-QN.md`.

## What you do as the assistant
1. Confirm with user: "this is a quarterly review and will force verdicts. Proceed?"
2. Read all products' `product.config.json`, `metrics.md`, last 90 days of `decisions/`.
3. Pull current metrics via telemetry-aggregator.
4. Ask user: "estimated hours per week on each product over last quarter" — fill in.
5. Generate the review per the agent's output spec.
6. For each KILL verdict, generate the sunset plan in full.
7. Save to file. Print summary in chat.
7b. **Factory curator pass** (rides here quarterly — v2.20 MECE curator, now measured):
   run `bun run skill-report --days 90`. `dormant` skills are archive candidates
   (`factory/skills/_archive/` — archive, never delete), `demoted` skills get a
   look before anything trusts them, and guard-sunset questions cite
   `bun run defect report` counts. Record pin / consolidate / archive per the
   skill-authoring playbook's curator rules.
8. Update each killed product's `product.config.json` → `status: "sunset_planned"` + `sunset_date: <T+60>`.
9. Add an entry to `MEMORY.md` if portfolio-level patterns emerged.

## Warning
This skill produces uncomfortable decisions. Don't soften the verdicts. The whole point is the forcing function.
