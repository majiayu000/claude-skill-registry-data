---
name: section-matching
description: Use when kivo-creator section specs in .creator/<run>/specs must be mapped to the project's existing blocks before anything is generated - building the match plan, applying the compatibility filter, judging the remaining candidates with the written rubric (including an explicit none), asking the person below the confidence threshold and checking the plan. For ingesting a source use html-ingest or figma-ingest; for generating missing blocks use block-scaffolding-from-design.
license: MIT
compatibility: Node 20+. Reads the project's block catalog through the kivo-creator adapter; writes only .creator/<run>/match-plan.json and match-plan.md.
---

# Section matching

Recognise first, generate last. Each section is matched to a block the project already has; a new block is generated only when nothing fits. The plan is written to disk and approved before anything is emitted.

## When to use

- After `html-ingest` or `figma-ingest` produced valid specs.
- "Which of our blocks should this section use?", "map the design to our blocks".
- Not for writing block code (`block-scaffolding-from-design`) or checking the rendered page (`visual-fidelity`).

## Inputs required

1. The run folder `.creator/<run>/` with valid specs.
2. The project root with `.roots-stack.json`, or the kivo-wise detector JSON passed with `--stack=<file>`.
3. The kivo-creator plugin root (two levels above this skill's folder).

## Procedure

1. Read the catalog: `node <kivo-creator>/scripts/match.mjs --catalog --project=.` (name, `type`, title, description, `whenToUse`, fields). It holds every existing block of both types (ACF Composer classes and `block.json` files); a section may fill either. The project's block type only matters for new blocks (`blockType` in the plan; see `/creator`).
2. Build the plan: `node <kivo-creator>/scripts/match.mjs --run=.creator/<run> --project=.`. It writes `match-plan.json` and prints the sections to `judge`. Already decided by the script:
   - chrome sections: `skip`;
   - a Code Connect mapping (`spec.codeConnect.block`): `fill` with confidence 1;
   - no block passes the compatibility filter: `scaffold` (or `gap` when the target forbids generated blocks).
3. For each section in `judge`, read its spec, its reference image and its `candidates` (blocks whose fields can hold every slot, ranked by field coverage). Score each candidate with the rubric, then write the decision into `match-plan.json`:

   | Criterion | Question | Weight |
   |---|---|---|
   | Purpose | Do the block's description and `whenToUse` describe this kind of section? | Decisive: a block built for another purpose is never a match, even when its fields fit |
   | Structure | Do the slots and the repeat count fit without dropping content? Unused optional fields are fine | High |
   | Layout | Can the block show the media position and column count (styles, variants)? | Medium |
   | Cost of a new block | Would a new block duplicate one that only needs a style variant or one field? | Tie-breaker |

   Always consider `none`: when the only candidates serve another purpose (a testimonial fits a hero's fields but is not a hero), choose `scaffold` with `block: null`.

   Decision shape:

   ```json
   { "action": "fill", "block": "acf/faq", "confidence": 0.85, "reason": "Questions and answers; the questions repeater holds the three items" }
   ```

   Confidence: 0.9 or more when purpose and structure are clear; 0.6 to 0.9 with a caveat written in `reason`; below the plan's `threshold` (0.6) set `"action": "ask"` and ask the person.
4. Ask the person about every `ask` decision, listing the candidates and `none`. Record the answer as the decision with `"approvedBy": "person"`.
5. Check: `node <kivo-creator>/scripts/match.mjs --run=.creator/<run> --check --project=.`. Fix every error it prints and run it again.
6. Show `match-plan.md` and stop. Emitting happens only after the person approves the plan.

## Verification

- `match.mjs --check` exits 0 and prints `match plan ok`.
- Every `fill` names a block from the catalog that is among the section's candidates (or was approved by the person).
- Every `scaffold` or `gap` has a reason a person can accept without opening the files.

## Failure modes

| Symptom | Cause | Fix |
|---|---|---|
| Every section goes to `scaffold` | Catalog empty: blocks live outside the adapter's folder (ACF Composer classes in `app/Blocks`, `block.json` files under the app) | Run `--catalog`; if blocks are missing, check the profile in `.roots-stack.json` and the block folder |
| A good block is missing from `candidates` | A slot type its fields cannot hold (for example an image slot and no image field) | Decide whether the slot matters; dropping it is the person's call, never yours |
| `did not pass the compatibility filter` | A fill names a block that cannot hold all slots | Pick a candidate, or ask the person and record `approvedBy` |
| `confidence ... is below 0.6` | A low-confidence fill without approval | Ask the person; record `approvedBy: "person"` |
| Same block chosen for two different purposes | Purpose criterion skipped | Re-score with the rubric; purpose is decisive |

## Escalation

Ask the person whenever the decision is below the threshold, when two candidates are equally good, or when the right answer is a new style variant of an existing block instead of a new block.
