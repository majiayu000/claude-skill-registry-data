---
name: review-product
description: Review a product from the user's perspective — build/refine a user persona, map their use cases (jobs-to-be-done), then audit the product for friction, gaps, and things to add or change. Triggers "review product", "product review", "review from the user's perspective", "product/UX critique", "what's missing for users". Use --live to also exercise the running app.
argument-hint: '[--live | --multi]'
effort: high
---

<!-- Generated from https://github.com/nielsmadan/agentic-coding — edits here are overwritten. -->

# Review Product

Review a product the way its users experience it, not the way its code is
structured. Where `code-review` and the `review-*` family judge the
implementation, this skill judges whether the *product serves the people using
it*: it builds a profile of the user, maps the jobs they come to do, then walks
those jobs through the product to find friction, gaps, and concrete things to
add or change.

Reusable findings (the persona and the use cases) are persisted to `docs/product/`
and **refined** on each run, so the product's understanding of its users
accumulates instead of being re-derived every time. The review itself is written
to `docs/product/<date>-review.md` so it isn't lost. All of this lives under
`docs/product/` as a section of the project's `docs/` tree, indexed by
`docs/product/overview.md` once the section has several files (consistent with the
`doc` skill's "index when warranted" convention).

`docs/product/` is the **high-level, user-centric** layer (why, for whom, what's
missing). It is the upstream of `docs/features/` (the "what it does" layer the `doc`
skill owns and keeps in sync with the implementation; formerly `docs/prd/`). This
skill owns `docs/product/` and does not write `docs/features/`; it only *checks* that
the feature docs reflect the product understanding (Step 7).

## Usage

```
review-product                 # codebase + product description (default)
review-product --live          # also drive the running app to verify real behavior (slow)
review-product --multi         # add external advisor opinions on the findings
review-product checkout flow   # scope the review to a feature/area
```

## Scope

| Argument | What it reviews | Cost |
|----------|-----------------|------|
| (none) | Infers the experience from the **codebase + any product description** (README, `docs/features/`, CLAUDE.md, docs). Default. | Fast |
| `--live` | Adds to the default: launches/exercises the **running app** to confirm what really happens (use `run` or browser tooling). Don't assume — observe. | Slow |
| `--multi` | After the review, calls `second-opinion --quick` with the findings and adds a short cross-model section. | +external advisors |
| free text | Scopes persona/use-cases/audit to the named feature or area instead of the whole product. | — |

`--live` is opt-in because exercising the app is slow; the default reasons from
code + docs only and says so.

## Gotchas

- **Evidence, not invention.** Every persona claim and use case must trace to the
  codebase, a doc, or explicit user input. Do not fabricate demographics, market
  size, or user quotes. If something is an assumption, label it and ask.
- **User's job, not the code's structure.** A "friction point" is something that
  slows or blocks the *user*, described in their terms — not a refactor or a code
  smell. Send those to `review-cleancode` / `code-review`.
- **Refine, don't clobber.** If `docs/product/persona.md` or `use-cases.md` already
  exist, edit them — reconcile new evidence with prior content and note what
  changed. Don't overwrite a richer file with a thinner one.
- Without `--live`, you are reasoning about *intended* behavior from source. State
  that explicitly; flag where real behavior would need to be verified.

## Workflow

Create a TodoWrite item per step.

### Step 1 — Build or refine the user persona
- Read `docs/product/persona.md` if it exists. Read the product description (README,
  `docs/features/`, `docs/`, CLAUDE.md) and survey the codebase (entry points, routes/screens,
  auth, settings) for who the product is built for.
- Produce the persona(s) using the template in `references/checklist.md`: who they
  are, why they're here, environment, what they value, frustrations, what success
  looks like. Mark the **primary** persona.
- If core facts can't be inferred (who the real user is, what they're optimizing
  for), **ask the user 2-4 focused questions** before continuing — a wrong persona
  invalidates the whole review.
- Write/refine `docs/product/persona.md`.

### Step 2 — Map the use cases (jobs-to-be-done)
- Read `docs/product/use-cases.md` if present. From the persona's goals plus the
  product's actual flows, enumerate the jobs the user comes to do, phrased from
  their point of view (When ___, I want to ___, so I can ___).
- For each: trigger, the path the product requires today (cite screens/routes),
  definition of done, frequency/stakes. Order by centrality to the persona.
- Write/refine `docs/product/use-cases.md`.

### Step 3 — Walk the experience
- Trace each **primary** use case end-to-end through the product. Without `--live`,
  follow the code paths/screens. With `--live`, actually exercise the running app
  (launch via `run`, drive the UI, screenshot key states) and record what really
  happens vs what the code implies.
- Note **what works well** — effective flows worth keeping. A review that only
  lists problems is incomplete.

### Step 4 — Audit friction & gaps
- Evaluate each use case against the lenses in `references/checklist.md`:
  **(A) job coverage** (the most important — can the user actually finish the
  job?), **(B) friction** (Nielsen heuristics applied to flows), **(C) onboarding
  & first run**, **(D) trust & safety**, **(E) opportunities** to add/change/remove.
- For large products or `--live`, assign primary use cases to workers and queue
  them within the runtime concurrency limit, then merge their findings. Give them
  the read/browser tools needed for the walkthrough without code edits. Disable
  delegation tools for ordinary workers; any coordinating role needs explicit
  subtasks, a descendant limit, and a stopping condition.
- Rate each finding by user impact: **Critical / High / Medium / Suggestion**
  (definitions in the checklist).

### Step 5 — Prioritize recommendations
- Turn findings into concrete, actionable changes — what to add, change, or remove,
  in the user's terms. Each gets a severity, a rough effort (S/M/L), and ties back
  to the use case it unblocks. Lead with the changes that most help the primary
  persona on their primary job.
- **Wide-open gap → diverge before converging.** When a finding is a job the product
  doesn't serve *at all* (a Step 4(A) coverage gap or a Step 7 uncovered use case) and
  the fix isn't obvious, optionally invoke `ideation` (Skill tool) on that specific job —
  tell it the job is an already-validated unmet user need so it focuses on *how* to serve it
  rather than whether to — to generate a wider spread of approaches, then bring the best one
  back as the recommendation. The *gap* stays evidence-anchored (an observed unmet job); only
  the *solution search* is divergent, so this doesn't breach "evidence, not invention." Skip
  it when the fix is already clear — most findings won't need it.

### Step 6 — Write the review
- Run `date +%F` to get today's date. Write the review to
  `docs/product/<date>-review.md` using the Output Format below.
- If `--multi`, call `second-opinion --quick` (which queries every advisor it has
  configured, in parallel) with a summary of the findings and append a short
  "Second opinion" section (agreements / dissent / additions), attributing points
  to each advisor that responded by name.
- Give the user an inline summary: the headline finding, the top 3 prioritized
  recommendations, and the path to the written review.

### Step 7 — Check the feature docs against the product (if `docs/features/` exists)
The `doc` skill owns `docs/features/` (the "what it does" layer, formerly `docs/prd/`)
and keeps it in sync with the *implementation*; this step checks the *other* side — that
the feature docs reflect the product understanding in `docs/product/`. Report-only; do
not edit `docs/features/` (that's `doc`'s job).
- **Use cases with no feature-doc coverage**: a job in `use-cases.md` that no
  `docs/features/` doc describes → the product intends something the docs don't capture.
- **Feature docs serving no use case**: a `docs/features/` doc that ties to no documented
  use case or persona need → scope the product can't justify, or a missing use case.
- List both kinds of divergence so the user can reconcile (update a use case, write a
  feature doc via `doc`, or drop scope). Pair with `doc --review` (features ↔ implementation)
  for the full three-layer check: product ↔ features ↔ code.
- **Lean repos (no `docs/features/`):** a small project won't have a dedicated behavior
  layer. Skip the doc-to-doc check and instead spot-check the top use cases straight
  against the code (and any `docs/<flow>.md` explanation docs), noting jobs the code
  doesn't appear to support. Say you did this because there's no feature-doc layer.

### Step 8 — Update the docs/product index
- Write/refresh `docs/product/overview.md` as the section index: a one-line intro,
  links to `persona.md` and `use-cases.md` (the reusable, current-state artifacts), and
  a reverse-chronological list of the dated reviews (newest first). Overwrite each run.
- If a root `docs/overview.md` index exists, ensure it links to `docs/product/`. Don't
  create the root index when it's absent — that's the `doc` skill's job.

## Output Format

Written to `docs/product/<date>-review.md`, and summarized inline:

```markdown
# Product Review — <scope> — <date>

> Method: codebase + docs [+ live app] · Persona: see persona.md · Use cases: see use-cases.md

## Summary
Headline assessment in 2-4 sentences: how well the product serves its primary
persona on their primary job, and the single most important thing to change.

## What works well
- ...

## Findings
### Critical
- **<title>** (UC<n>, effort: M) — what the user hits, why it blocks the job, the fix.
### High
- ...
### Medium
- ...
### Suggestions
- ...

## Prioritized recommendations
1. **<change>** — adds/changes/removes ___, unblocks UC<n>. Severity / effort.
2. ...

## Feature-doc consistency   (if docs/features/ exists)
- Use cases with no feature-doc coverage / feature docs with no use case (from Step 7).

## Second opinion   (only with --multi)
- Agreements / dissent / additions from each advisor that responded, attributed by name. Note where multiple advisors converge — consensus raises confidence.

## Verify with users / open questions
- Assumptions that real user behavior or `--live` testing would confirm.
```

## Examples

### Example 1: First review of a SaaS app
User says: "review the product"
Actions: No `docs/product/persona.md` exists. Read the README + dashboard routes,
infer a "small-team ops manager" persona, ask 2 questions to confirm their main
goal. Write `persona.md` and `use-cases.md` (UC1 set up a workspace, UC2 invite
teammates, UC3 read the daily report). Walk each from code. Find UC2 has no resend
for a lost invite (High) and the empty dashboard teaches nothing (Medium). Write
`docs/product/2026-05-30-review.md`; summarize top 3 fixes inline.

### Example 2: Live, scoped review
User says: "review-product --live the onboarding flow"
Actions: Refine the existing persona, focus use-cases on first-run. Launch the app
via `run`, click through signup → first value, screenshot each step. Discover the
email-verification step dead-ends on mobile (Critical) and time-to-first-value is
~6 steps (High). Recommend a deferred-verification path. Write the dated review.

### Example 3: Cross-model check before a roadmap meeting
User says: "review product --multi"
Actions: Run the full review, then pass the findings to `second-opinion --quick`.
The advisors variously agree on the missing undo, dissent on severity of one item,
and add a discoverability gap. Append the "Second opinion" section attributing each
point to the advisor that raised it.

## Troubleshooting

### The persona feels generic or made-up
**Cause:** Not enough evidence; defaulting to a stock persona.
**Solution:** Cite sources for every claim. If the codebase and docs don't reveal
the user, stop and ask the user directly — don't invent demographics.

### Findings read like a code review
**Cause:** Reviewing the implementation instead of the experience.
**Solution:** Re-anchor every finding to a use case and describe the impact in the
user's terms ("the user can't tell the save worked"), not the code's ("no toast
component"). Route true code issues to `code-review`.

### `--live` can't run the app
**Cause:** No run command, missing deps, or the app needs credentials.
**Solution:** Ask the user how to launch it (suggest `! <command>` for interactive
logins). If it can't be run, fall back to the code-only review and clearly mark
which findings are unverified against real behavior.

### docs/product/ already has reviews and they're drifting
**Cause:** Persona/use-cases edited per-review instead of kept canonical.
**Solution:** `persona.md` and `use-cases.md` are the single source of truth —
refine them in place. Dated review files are snapshots and are never rewritten.

## Notes

- `docs/product/` layout:
  ```
  docs/product/
  ├── overview.md         # Section index; open this first
  ├── persona.md          # Reusable, refined in place (current state)
  ├── use-cases.md        # Reusable, refined in place (current state)
  └── <date>-review.md    # Dated review snapshots; never rewritten
  ```
- Three-layer model (altitude stack): **`docs/product/`** (this skill — who & why,
  high level) → **`docs/features/`** (the `doc` skill — what it does, tracks the code;
  formerly `docs/prd/`) → **`docs/tech/` + implementation** (how it's built). This skill
  checks `docs/product/` ↔ `docs/features/` (Step 7); `doc --review` checks
  `docs/features/` ↔ code. `doc` never syncs `docs/product/` to code. On a Lean repo
  with no `docs/features/`, Step 7 checks use cases straight against the code.
- This skill judges the product, not the code. Pair it with `code-review` /
  `review-cleancode` for implementation quality and `frontend-design` for visual craft.
- See `references/checklist.md` for the persona/use-case templates, the friction
  lenses (Nielsen heuristics + product/JTBD), and severity definitions.
