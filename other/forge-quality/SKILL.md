---
name: forge-quality
description: Quality Intelligence Layer — mission → MissionProfile, 10 lenses, omission mining, requirement cards, drift detection, context compiler and selective council-trigger. Router Step 1 for every build.
---

# forge-quality — Quality Intelligence Layer

Layer-2 instruction (progressive disclosure): this file is small; domain knowledge lives in layer 3
(`.claude/config/quality/cards/*.md`, 0 tokens until loaded). The module is
`.claude/forge-bin/forge-quality.cjs`; the canonical domain list is
`.claude/config/orchestration/domain-catalog.json` — on a conflict the CATALOG wins and the
diverging seam gets fixed, never a second list started.

## Commands

```bash
node .claude/forge-bin/forge-quality.cjs analyze "<the mission>"  # THE entry point: profile + playbook + lenses + omissions + card descriptors + council in one JSON (F-14)
node .claude/forge-bin/forge-quality.cjs profile "<the mission>"  # the MissionProfile only
node .claude/forge-bin/forge-quality.cjs card <slug>              # one knowledge card (layer 3, on-demand)
node .claude/forge-bin/forge-quality.cjs drift                    # catalog vs 4 seams — every difference is a finding (exit 3 on drift)
node .claude/forge-bin/forge-quality.cjs kernel                   # the fixed Quality Kernel (~600-800 tokens)
```

## Workflow (router Step 1 — required for BUILD tasks)

1. Run `analyze`; machine output beats any human-written table. `classification_confidence: none`
   means: the fallback is an ASSUMPTION — resolve the type explicitly (intake) before building.
2. Lenses: every lens gets EXACTLY one disposition (RELEVANT/NOT_APPLICABLE/DEFERRED/OWNER_GATED)
   with a reason. Silently skipping does not exist; neither does silently adding one.
3. Omissions are candidate requirements (pre-validated; `omissions_valid` must be true — a
   hand-edited card goes back through `validateRequirementCard`). A RESEARCH_HYPOTHESIS never
   becomes a hard requirement directly — promotion requires `confirmed_by` {type: local-validation|
   official-source|experiment, ref}.
4. Knowledge cards: load only descriptors with `exists: true` via `card <slug>` — max 6 cards,
   max 3 retrieval rounds. A missing card is an honest notice, never invented content.

## Council (selective, never the default)

`councilTrigger` decides: NONE is the default; FULL only on an explicit request or high impact +
high uncertainty. Real dispatch runs through the Agent tool; the CouncilDecisionRecord is validated
with `validateCouncilRecord` — that validation is shape_only (labels don't prove a principal; real
provenance is owner-gated, see OWNER-GATED.md). Council consensus is NEVER proof — only
tests/measurements are.
