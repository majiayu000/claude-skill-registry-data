---
name: evolve
description: "Audit one part of the code and rank what to improve. Changes nothing. Use when the user asks \"is this outdated\" or \"how could X be better\"."
license: MIT
metadata:
  author: Tony Gorb
  source: https://github.com/tonygorb/skills
  category: quality
  cover: "rank"
---

# Evolve

Propose upgrades; **never apply them in the same run**. The output is a ranked list the user picks from.

## Scope

One area per run (UI, data layer, auth, testing, caching, one flow). Asked to evolve "everything":
ask which area first.

## Process

1. **Baseline.** Read the project's own rules for that area (AGENTS.md, a design doc, an ADR) and
   the actual code. The current way is intentional: an upgrade has to beat it, not just differ.
2. **Current practice.** Check the docs of the versions actually installed (your training data
   may be older than the code), and the codebase's own newest screens: often the best idea
   already exists in one place and should spread.
3. **Disqualify** anything that breaks a hard rule of the project. Breaking an invariant isn't an
   upgrade.

## Output: always this table, ranked by value for cost

| # | Upgrade | Benefit | Cost (S/M/L) | Risk | Files touched |
|---|---|---|---|---|---|

Under it, at most three sentences per row: what changes, why it beats the current way, what could
break. End with your recommended pick and what you'd do first once it's approved.

## After approval (a separate run)

Implement it the normal way, then verify (build, tests, a look at the UI if it changed), then
update the doc that describes the area.
