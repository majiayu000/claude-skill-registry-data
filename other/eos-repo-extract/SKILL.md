---
name: eos-repo-extract
description: Study an external repo and mine it on two axes — the code axis (extract its discipline as the smallest honest abstraction over existing primitives, proven by two real consumers plus a first-consumer implementation) and the workflow axis (does its sequencing expose a stage our pipeline never emits?). Build-nothing is a first-class outcome and still lands a logged verdict, a memory, and a triggered deferred row. Use when the user says "study this repo", "borrow from X", "repo review", "extract the pattern from X", "is this worth borrowing", or pastes a foreign repo to learn from — and equally when they paste a technique claim rather than a codebase, a post saying a model, LoRA, prompt trick or workflow "can do X". A capability claim is still a borrow decision, but its verdict needs an experiment on our own stack, not just a read. NOT deduplication within this codebase (use eos-sdk-extract) and NOT porting a foreign app wholesale.
---

# EmptyOS Repo Extract

Study an external repo/project, then extract its **discipline** into EmptyOS — a
reusable pattern, not a port. The sibling of `eos-sdk-extract`: that one dedupes
*within* the codebase; this one mines a *foreign* codebase for a workflow shape
worth adopting and lands it as EmptyOS-native infrastructure.

Goal: **turn "this external project does X well" into either (a) the smallest
honest EmptyOS abstraction, built on existing primitives, proven by ≥2 real
consumers and a first-consumer implementation, or (b) a named gap in one of our
own pipelines — without rebuilding the external app.** Most runs end in
**build-nothing**; that is a success, and it still lands a verdict (step 8).

Codifies the move made for MoneyPrinterTurbo → `emptyos/sdk/pipeline.py` +
`footage` capability (2026-06-07). Triggered the second time the repo-mining
shape recurred (cf. `project_repo_mining_2026_06`); this skill is the runner so
the third time isn't hand-walked.

## When to Use

- User points at a GitHub repo / project and says "study X and design an EmptyOS
  version", "extract the pattern from X", "what's worth lifting from X",
  "don't rebuild X, take its discipline".
- `/eos-simplify` §8 flagged a hand-run "study repo → extract pattern" workflow.
- You're about to read a foreign codebase to copy an idea — run this instead of
  free-handing it.

- User pastes a repo blurb / trending post and asks "is this worth borrowing?" —
  that's a **repo review**, and it runs this skill. It usually ends in
  build-nothing, which is step 8, not a reason to skip the skill.
- The external thing is a **technique, not a codebase** — a LoRA, a prompt trick,
  a "it turns out model X can do Y" post. Same skill: it is still a borrow
  decision with a verdict to log. The only difference is that step 1's digest
  cannot settle it, so step 1b applies. Missed 2026-07-29 (Krea 2 markup trick)
  because every trigger noun here was repo-shaped; a Reddit post about a LoRA
  matched none of them and the whole pipeline — including step 0 — was
  hand-walked out of order.

**Not** for: rebuilding the external app feature-for-feature (that's a port, not
an extraction); adopting a single function (just write it); pure research with no
EmptyOS decision attached (that's `deep-research` or a repo-review note —
`reference_repo_review_log`). Note a *verdict* is a decision, so a build-nothing
review belongs **here**, not in `deep-research`.

## The Pipeline

> **Standing constraint — the study and audit agents are read-only.** Steps 1
> and 2 fan out subagents whose entire job is to *report*. Say so in the prompt
> explicitly: **explore and report findings only — no file writes, no edits, no
> commits.** A subagent left with default tools will happily "helpfully" write
> the digest to a file or fix something it noticed, and a background fork has
> already clobbered docs that way. You are synthesising the verdict; they hand
> you evidence.
>
> **Enforce it with the agent type, not the prompt.** Pass
> `subagent_type: "Explore"` — that type has no `Edit` / `Write` /
> `NotebookEdit` at all, so a write is impossible rather than merely
> discouraged. Same lesson as step 0's executable gate: an instruction that
> *asks* for read-only is one a subagent can talk itself out of.
>
> **Step 1b is the deliberate exception** — falsifying a capability claim *is* an
> experiment and it writes render outputs. Scope it to its own output dir, and
> never let it touch tracked source.

### 0. Check for a closed verdict — *don't re-derive*

`python scripts/check_borrow_verdict.py <repo-or-library-name>` (exit 1 = a verdict
already exists in `docs/OPEN-SOURCE-BORROWING-PLAN.md` / `docs/DEFERRED-WORK.md`).
Read it and stop. Also grep the memory archive — 20+ closed verdicts live there.

### 1. Study the external repo — *digest, not feature list*

Fan out an `Agent` (general-purpose) to fetch the repo's README + source tree +
key files (raw.githubusercontent URLs) and return a **structured architectural
digest**: the layering split, the per-unit state/data model, where intermediate
state is persisted, what's swappable, and — critically — **the minimal
discipline worth copying** + **the one thing NOT to copy verbatim**. Demand file
paths and code-shape quotes, not prose. You're designing an abstraction from
this, so vague is useless.

### 1b. If the claim is a *capability*, falsify it on our own stack

Reading settles an architecture claim. It cannot settle "model X can do Y" —
for that, the verdict is an experiment, and it is usually minutes of GPU against
a week of adoption work. Grep for the code path we **already own** that would
host the capability, and run the claim through *that*, not a fresh graph:

- **Off/on at one fixed seed.** Vary only the thing under test. Everything else
  — prompt, steps, resolution, sampler, first frame — held byte-identical.
- **Add a permutation control** where the claim is about *placement or mapping*.
  Object priors alone can fake a positive (a lantern goes up, a stool goes down);
  permuting the inputs is what separates correlation from cause.
- **Measure, don't eyeball.** A mean-abs pixel diff against the noise floor beats
  "looks the same" — and it is what makes the verdict re-checkable later.
- **Kill the obvious confound before concluding.** A null result can mean the
  mechanism is absent *or* that the model obeyed the one clause it understood.
  One more run is cheaper than a wrong verdict.
- If you mirrored a builder rather than calling it, **diff your mirror against
  the real preset** before trusting the word "our path" in the verdict.

Then explain the outcome mechanically — which conditioning channel exists on our
stack and which doesn't. "It didn't work" is not a verdict; "our encoder never
sees the image, theirs does" is, and it tells the reader what adopting would cost.
Sibling discipline: `eos-measure-claim` failure-mode 1 (*you measured a code path
the system does not use*) applies here verbatim.

### 2. Audit EmptyOS — *two axes, in parallel*

Fan out a **second** `Agent` (same message, parallel). Ask **both** questions —
they have different floors, and asking only the first is how a real finding gets
thrown away as "build nothing":

**Axis A — the code axis (abstraction).** Which EmptyOS features already
hand-roll the same *shape*? For each: concrete stages/state/persistence with
file:line, whether it'd benefit, and **whether the rule-9 threshold (2+ real
consumers) is met**. Count *latent* consumers too, not just active ones
(`feedback_sdk_audit_missing_helper_trap`). One consumer → **stop this axis**;
build it specific in that one app, don't extract (CLAUDE.md rule 9 / Forge
anti-abstraction).

**Axis B — the workflow axis (missing stage).** Ignore their code entirely and
look at how they **sequence** their work. Does that sequencing expose a *stage
or artifact our own pipeline never emits*? Compare against `products/`,
`sdk/pipeline.py` consumers (podcast, MV), the release scripts, the publish
chain. **Rule 9 does NOT apply here** — a missing stage in one pipeline is a
*feature*, not an abstraction, so "one consumer → stop" must not kill it.

Axis B is the one that survives when we already own every mechanism they have.
`ucsandman/marketing-studio` (2026-07-15) is the worked example: Axis A returned
build-nothing on all six mechanisms (our `prose_lint` already beat their copy
gate), while Axis B found that `products/` ships binaries with **no presentation
artifacts** and that `products/_shared/smoke.py` already boots the frozen
artifact — i.e. it is 80% of the capture rig, one step from
`sdk/media/html_record.py`. Axis A alone would have discarded that.

### 3. Grep the SDK before reinventing — *build on, don't beside*

The highest-leverage step and the easiest to skip. Before designing anything,
grep `emptyos/sdk/` + `base_app.py` for an existing primitive that already owns
part of the shape (`feedback_grep_sdk_before_reinventing`). The MPT case found
`RunRegistry` already owned the run-folder/state half and its docstring
*explicitly deferred* the other half until a 4th consumer — so the right design
was a thin layer **on top of** it, not a greenfield module. If an existing
primitive's "Out of scope" note names exactly what you're about to build, that's
your graduation signal — extend it, don't duplicate it.

### 4. Design — layer-on-top, provider-agnostic

Design the smallest abstraction that adds only the missing piece. Keep
provider/model choice in the capability chain, not the new abstraction (that's
how EmptyOS already does swappability + cloud consent). Honour the "don't copy
verbatim" finding from step 1 (e.g. MPT's stop-early-only resumability → we added
true resume-from-partial).

### 5. Land three artifacts

- **`.claude/rules/<pattern>.md`** — the design doc: why-it-sits-on-the-existing-
  primitive, the external lineage, when to use / not, the migration discipline.
- **First-consumer implementation, dark-flagged.** Refactor the cleanest consumer
  onto the new abstraction behind `[apps.<id>] feature.<slug>.enabled` (dark
  default, `feature_pipeline_flag_default_dark`). Use **behavior-preserving
  extraction** so the legacy path and the new path share one set of helpers (no
  drift); keep the legacy path as default until the new one is proven.
- **The one primitive they had that we lacked.** If step 1 surfaced a missing
  capability (MPT's `material.py` → stock footage), add it as a **capability**
  (mirrors draw/animate/browse: provider chain + human fallback + cloud consent
  for free, CLAUDE.md rule 18) when it's a generic verb, or a connector app when
  it's not. Dark until configured.

### 6. Verify

`python -m py_compile` the changed Python; write daemon-free unit tests for the
new SDK (wrap async with `asyncio.run()` per repo convention); then prove the
first consumer **end-to-end on a leased sandbox member**, never `:9000`
(`.claude/rules/sandbox-driven-testing.md`). The error path is part of the proof
— a captured-not-crashed failure with a persisted run is a passing result.

### 7. Record + sync docs

Add a one-line `project_*` memory (the design decision + the don't-re-research
note), update any capability/plugin counts in CLAUDE.md + `.claude/rules/`, and
run `/eos-simplify` before committing.

### 8. Build-nothing is a first-class outcome — *land the verdict anyway*

Most repo reviews end here, and a stop that leaves no artifact gets re-derived by
the next session. Whenever steps 2–4 conclude **build nothing** (or **borrow-idea
only**), the run is not over — land all of:

- **`docs/OPEN-SOURCE-BORROWING-PLAN.md`** — the verdict entry, so
  `check_borrow_verdict.py` finds it at step 0 next time. Say *what the repo
  actually is* (blurbs and READMEs lie — `project_trending_2026_07_12_verdict`),
  which mechanisms we already own **and where ours is stronger**, and the one
  genuine gap if any.
- **A `project_<name>_borrow_verdict` memory** + a line in `MEMORY.md`.
- **A `docs/DEFERRED-WORK.md` row — with a firing trigger** — for any Axis-B
  stage worth building later. A deferred row with no trigger is a wish; the
  trigger is what makes it findable when the need arrives
  (`reference_deferred_work_registry`).

Cite the actual source for every claim. A verdict derived from a README rather
than the code is worthless (`.claude/rules/deep-research.md`).

## Principles (the load-bearing ones)

- **Extract the discipline, not the app.** "Don't rebuild MPT — lift its workflow
  discipline." The deliverable is an EmptyOS-native abstraction, not a clone.
- **2+ consumers is the floor — for the code axis only.** No consumers in hand →
  research note, not code. But never let that floor kill an Axis-B finding: a
  missing *stage* in one pipeline is a feature, not an abstraction.
- **Mine the sequencing, not just the source.** When we already own every
  mechanism they have, the remaining value is in what they *do in what order* —
  and it usually shows up as an artifact our pipeline never emits.
- **Build on existing primitives.** Grep the SDK first; a layer on `RunRegistry`
  beats a parallel run-folder system that drifts.
- **Dark-flag the first consumer.** Nothing regresses until the flag flips.
- **The capability chain owns provider-swappability**, not your new abstraction.

## Anti-patterns

- Porting the external app's structure 1:1 (their MVC, their file names) instead
  of mapping it onto EmptyOS conventions.
- Greenfielding a module that duplicates an existing SDK primitive because you
  didn't grep first.
- Extracting on one consumer "because it'll obviously be reused" — premature.
- Fanning out a study/audit agent without pinning it read-only, then finding it
  edited the tree while you were reading its report.
- Flipping the first-consumer flag on by default in the same change.
- Skipping the sandbox E2E because the unit tests pass — unit tests don't catch
  boot-path / provider-availability reality.

## Cross-references

- `.claude/rules/staged-pipeline.md` — the reference output of this skill.
- `eos-sdk-extract` — the within-codebase sibling (dedupe, not foreign-mine).
- `reference_repo_review_log` — where a *review* (no extraction) is filed instead.
- `.claude/rules/sandbox-driven-testing.md` — the step-6 verification loop.
- CLAUDE.md rule 9 (extract on 2nd consumer) + rule 18 (cloud consent for the
  new capability).
