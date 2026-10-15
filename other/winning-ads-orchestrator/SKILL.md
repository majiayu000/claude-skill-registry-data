---
name: winning-ads-orchestrator
description: The master workflow for going from "find winning ad ideas for X" to a shoot-ready creative brief. Routes through competitor-ad-intelligence, own-creative-diagnosis, creative-psychology-hooks, winning-pattern-synthesis, and ad-brief-generator in order, adapting to what data sources are actually available. Use this whenever the user asks broadly for winning ad ideas, a competitive+creative teardown, "what should we make next," or any request that spans research and production rather than a single narrow step — that's the signal to run the full pipeline instead of just one component skill.
---

# Winning Ads Orchestrator

The entry point for the winning-ads skill pack. Decides which component skills to run, in what order, and what to do when a step's data isn't available — rather than making the user manually invoke five separate skills.

## When to use this skill

- "Find me winning ad ideas for [product/brand]"
- "Do a competitive + creative teardown and give me briefs to shoot"
- "What should we test next and give me the script"
- Any request where the end goal is production-ready creative, not just one analysis step

For narrow single-step requests ("just show me competitor ads," "just tell me why this ad is underperforming," "just give me hooks"), go straight to the relevant component skill instead of running the full pipeline — don't force every request through all five steps.

## Pipeline

```
1. competitor-ad-intelligence   (GoMarble MCP required)
2. own-creative-diagnosis       (MCP preferred, CSV/screenshot fallback)
3. creative-psychology-hooks    (no data source needed)
4. winning-pattern-synthesis    (consumes outputs of 1-3)
5. ad-brief-generator           (consumes output of 4)
```

## Step 0: Scope and data-availability check

Before running anything, establish in one pass:
- Is GoMarble MCP connected? If not, step 1 (competitor intel) cannot run — say so, and confirm whether to proceed with steps 2-5 using own-creative + psychology only, or stop and ask the user to connect it.
- What's the product/brand/category and target audience?
- Does the user want the full pipeline output, or just the research (steps 1-2) without a brief yet?

State the plan in one short paragraph before executing — which steps will run, which will be skipped and why, e.g.:
> "GoMarble MCP is connected, so I'll pull competitor ads for [category] (step 1), diagnose your own strong performers (step 2), grade hooks psychologically (step 3), synthesize into ranked directions (step 4), and brief the top 2-3 (step 5)."

## Step 1-2: Run research in parallel where possible

Competitor intelligence (step 1) and own-creative diagnosis (step 2) don't depend on each other — gather both before synthesizing. If MCP isn't available for one but is for the other, proceed with whichever is available and flag the gap rather than blocking the whole pipeline.

## Step 3: Psychological grading

Apply `creative-psychology-hooks` to the hooks/angles surfaced in steps 1-2 (grade, don't regenerate from scratch — the goal here is explaining *why* observed patterns work, feeding step 4). Only generate wholly new hooks at this stage if steps 1-2 turned up thin results and fresh ideation is needed to fill the batch.

## Step 4: Synthesize

Run `winning-pattern-synthesis` over whatever combination of steps 1-3 completed. Note explicitly in the synthesis output which inputs were available vs skipped.

## Step 5: Brief

Run `ad-brief-generator` on the top-ranked 2-3 directions from synthesis, unless the user asked for research only. Confirm format/length constraints before generating if they weren't established earlier in the conversation.

## Handling partial runs

- No MCP at all → competitor intel is fully blocked. Run own-creative diagnosis (if data available) + psychology hooks + a synthesis that's explicitly own-account-only, and say plainly that competitor whitespace can't be assessed without GoMarble MCP.
- No own ad account data (new brand/account) → own-creative diagnosis is blocked. Run competitor intel + psychology + a synthesis based on competitor patterns and psychological soundness only, flagged as unvalidated-for-this-account.
- Neither available → this pack can't meaningfully run past `creative-psychology-hooks`. Say so and offer cold ideation instead of pretending to synthesize.

## Output

The orchestrator's final output is whatever the last executed step produces (typically the brief set from `ad-brief-generator`), preceded by a one-paragraph recap of what ran, what was skipped, and why — so the user can see the provenance of the final recommendation without re-reading every intermediate step.
