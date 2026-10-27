---
name: eval-calibration
description: >
  Internal /ace:run step — Method reference for calibrating -eval rubrics against ground truth.
user-invocable: false
disable-model-invocation: false
---

# Eval Calibration

ACE's evaluation system has a known generosity bias: LLM-as-Judge
scores cluster in the 8–9 range even when the artifact has real flaws.
The first OCS smoke run scored 8.92/10 despite a contact-email typo in
3/26 responses and an empty `cited_files` array on every entry. That
score isn't wrong arithmetic — it's wrong rubric.

This skill is the **calibration methodology** for fixing rubrics. It
doesn't grade artifacts; it grades rubrics. The output is a calibrated
rubric (revised `## LLM-as-Judge Rubric` section in some other skill's
`SKILL.md`) plus an audit trail showing the rubric got better, not
just different.

## The three properties a calibrated rubric must have

1. **Ground-truth detection** — given a transcript with known issues,
   the rubric flags the issues and deducts meaningfully (≥1 point on
   the relevant dimension).
2. **Inter-run stability** — running the rubric N times against the
   same input produces scores within ±0.5 of each other. Higher
   variance means the rubric prompt is under-specified.
3. **Inflation discipline** — the rubric is willing to score below 7.
   If scores cluster in 8–10 across all artifacts, the rubric isn't
   distinguishing quality.

## Process

### Step 1 — Build the ground-truth catalogue

Per opp folder: `ACE/<opp-name>/eval-calibration/known-issues.md`. One
section per artifact being evaluated. Each entry is a concrete,
human-confirmed flaw the rubric must detect:

```markdown
# Known Issues — <opp-name>

## OCS chatbot deep transcript (5-ocs/ocs-chatbot-qa_transcript-deep.md)

- **[factual]** Bot wrote `ace@dimagi.com` (missing `-ai`) in entries
  19, 22, 25. Detection target: ≥1-point Correctness deduction per
  occurrence; ≥1 `[WARN]` at suite level.
- **[structural]** API `cited_files` field is empty in all 26 entries
  despite `generate_citations: true` on the chatbot pipeline.
  Detection target: Source usage capped at ≤5.
- **[adversarial gap]** Suite contains 0 `should-refuse` and 0
  `hallucination-probe` prompts. The bot's refusal discipline is
  literally unmeasured. Detection target: `[INFO] thin adversarial
  coverage` in the verdict's `auto_surfaced` block.

## Deliver app build (app-summaries/deliver-app-summary.md)

- **[spec deviation]** Q8 split into Q8 + Q8b in the build (not in
  PDD). Detection target: `[WARN]` in pdd-to-deliver-app-eval.
- **[deferred enforcement]** Operational caps (≤20/FLW/day,
  ≤5/market/day, 25m duplicate detection) are server-side per the
  build summary, not in-form. Detection target: `[INFO]` not
  `[WARN]` (this is a documented platform limitation, not a build
  defect).
```

The catalogue is **manually authored** by the operator after a real
run. It's the "human-graded ground truth" — without it, all scores
are vibes.

### Step 2 — Run the current rubric, record the verdict

Invoke the eval skill (`ocs-chatbot-eval`, `pdd-to-deliver-app-eval`,
etc.) against the captured artifacts. Record the resulting verdict
YAML to `eval-calibration/<rubric-name>-runs.md` as run 1:

```markdown
# Calibration Runs — <rubric-name>

## Run 1 — <ISO timestamp>
Rubric version: <git SHA or VERSION>
Inputs: <capture path>
Verdict: <pass | warn | fail | incomplete>
Overall: <score>/10
Dimensions: { correctness: 9.7, source_usage: 7.3, ... }
Detection rate: <fraction of known issues flagged>/<total known>
Variance window: N/A (single run)
Notes: <what the rubric got right / missed>
```

### Step 3 — Score the rubric on detection rate

For each known issue in the catalogue, check whether the rubric's
verdict YAML surfaced it (deduction, `auto_surfaced` entry,
dimension cap). Compute:

```
detection_rate = issues_flagged / total_known_issues
```

Calibration target: **≥80% detection rate** on the ground-truth set.

### Step 3b — Dimension coverage (added 2026-05-29)

Detection rate has a blind spot it can never see: it only measures
whether the rubric catches issues *that are in the catalogue*, and the
catalogue is operator-authored from issues already noticed. **A missing
dimension is never a known issue** — so a rubric can hit 100% detection
while being structurally blind to an entire fitness axis. This is
exactly how the ITN app evals scored 9.6 on a hollow build: they
detected every catalogued structural nit, but had no dimension for
validation, capture fidelity, case persistence, or localization.

Detection rate alone is therefore *insufficient*. Add a coverage check:

1. **Enumerate the fitness axes** that separate "conformant" from
   "deployable" for this artifact type — the axes a domain expert would
   check before shipping: input validation, capture fidelity,
   persistence, enforcement, language conformance, real-world viability,
   adversarial coverage, reader-usefulness. Pick the ones that apply.
2. **Confirm the rubric has a dimension touching each applicable axis.**
   An axis with no dimension is a coverage gap — the rubric cannot
   deduct for failing it. Per `_eval-template.md § The out-of-chain
   fitness requirement`, at least one such dimension must be graded
   against an out-of-chain bar.
3. **Calibrate against an expert reference AND a negative control.**
   Detection-rate calibration uses a flawed artifact; coverage
   calibration additionally needs (a) an *expert-built* reference as the
   deployable bar (e.g. the malaria-itn-app `[Final]` builds Sarvesh
   hand-finished) and (b) a deliberately-**thin negative control** the
   rubric MUST score below `pass`. The ITN ACE build (run
   `20260528-1607`) is the canonical negative control for the app
   rubrics: a calibrated `pdd-to-deliver-app-eval` scores it ≤3 on
   capture_fitness / data_quality_validation / case_persistence and
   `fail` overall. If a rubric scores its negative control above `warn`,
   it is not calibrated regardless of detection rate.

### Step 3c — Anchors must be re-derivable without the live artifact (added 2026-08-13)

A calibration anchor — the positive control, the negative control, the
expert reference — is the **regression test for a rubric revision**. Most
`-eval` rubrics say so in their own text ("any revision of this dimension
must still score that bank ≤3"). So the anchor has to still mean, next
month, what it meant when it was recorded.

**It won't, if it is recorded as a pointer.** An anchor written as *"opp X
/ run Y, Nova app Z scored N"* names three mutable things:

- **Nova apps are mutable.** A repair pass, a `/ace:step` re-run, or a
  later phase editing the same app changes the artifact under the anchor
  with nothing to detect it.
- **Runs get repaired.** `repairs[]` is a designed part of the loop —
  `pdd-to-learn-app-eval` hands a typed work order back to the producer,
  which changes the very bank the anchor cites.
- **The enumeration is not a property of the artifact.** Where a score is
  a ratio over a judge-built denominator (rules covered, operations
  covered, axes present), two honest graders re-derive different
  denominators from the same app. The anchor's number moves without
  anything at all changing.

All three have already fired on `pdd-to-learn-app-eval`'s positive
control. Measured 2026-08-13, the same app + run cited by the rubric has
**three different recorded ratios** — `0.78` in the rubric (denominator
32), `0.767` in that run's own prior verdict, and `0.904` in the live
verdict (denominator **52**, after a repair round). A revision checking
itself against "0.78" is checking against a number no live re-derivation
reproduces.

**The rule.** An anchor MUST record enough evidence to re-derive its score
**without reading the live artifact**. Concretely, every anchor block
carries:

1. **`measured_on: YYYY-MM-DD`** — the date the number was measured. Not
   the date the rubric was edited.
2. **The evidence the score was computed from**, inline — the per-item /
   per-dimension table, the numerator and denominator *as enumerated*, the
   item stems or rule names as they read at measurement time. Enough that
   a reader can recompute the number from this page alone.
3. **A mutability notice** — an explicit statement that the cited artifact
   is live and mutable, and MUST be re-measured rather than assumed before
   it is used as a regression gate.
4. **Both readings where the artifact has since changed.** Do not
   silently re-point the anchor at the new number. The delta is itself
   information — it is how this whole failure mode was found — and a
   revision needs to know which reading its predecessor was calibrated
   against.

**Where the score is a ratio over a judge-built denominator, the
enumeration is part of the evidence, not part of the artifact.** Record
the denominator's entries, not just its size. An anchor that records
`25/32` without naming the 32 cannot be re-derived by anyone, including
its author.

**Scope — this applies to ANCHORS, not to every run citation.** The
distinction is whether anything *checks itself against* the artifact:

- **An anchor** is load-bearing for a future decision — "any revision must
  still score this bank ≤3", "the negative control MUST score
  `capture_fitness ≤3`", "detection rate ≥80% against this catalogue". It
  is a regression gate, so it has to stay re-derivable. Step 3c applies.
- **Provenance** is a citation explaining where a rule came from — "this
  component was added after `hh-poverty-targeting/20260722-1341` shipped
  a hollow bank". The rule stands on its own stated reasoning whether or
  not that app still looks that way, and nothing re-measures it. Step 3c
  does **not** apply; adding dates and evidence tables to provenance is
  noise that buries the anchors that do matter.

Change-log entries are provenance by construction. When in doubt: if
someone would ever re-run the measurement to decide something, it is an
anchor.

**Prefer an anchor that cannot drift.** In descending order of
durability: a frozen copy of the artifact (a CCZ, an exported blueprint, a
transcript) > the full evidence table recorded inline > a pointer to a
live app id. The first two are re-derivable by construction; the third is
a bookmark, and bookmarks are what this step exists to stop.

*Enforced (partly):* `test/skills/eval-calibration-anchors.test.ts` fails
any `## …control` section in a `skills/*-eval/SKILL.md` that omits
`measured_on:`. That is a date check, not a semantics check — it cannot
tell you the anchor is still valid, only that you can see how old it is.

### Step 4 — Run the rubric N times for variance

Sequentially invoke the same rubric against the same input ≥3 times
(harness serializes same-subagent-type Agent calls, so plan for
elapsed time = N × per-run cost). Record each run as a separate row.
Compute:

```
score_variance = max(overall) - min(overall)
```

Calibration target: **score_variance ≤ 0.5**. Higher variance means
the rubric prompt is under-specified — different LLM rolls of the
dice produce materially different scores.

**Anchoring caveat (added 0.9.1):** when 3 sequential same-model runs
produce a tight spread (≤ 0.1), be suspicious. Anchoring is the most
common false-pass mode: each run after run 1 latches onto the prior
overall score and re-derives it instead of grading independently.
Two ways to harden against anchoring:

- **Cross-model variance.** Run 1, 2, 3 on different judge models
  (Sonnet, Opus, Haiku). A rubric whose criteria are explicit
  enough should produce comparable scores across models. If the
  spread blows up, the rubric is leaning on judge-specific
  generosity rather than the criteria themselves.
- **Shuffled prompt order.** Re-run with the transcript entries in
  a different order so the judge can't pattern-match against its
  own earlier grading.

A rubric is **provisionally calibrated** at ≤ 0.5 same-model
variance, **strongly calibrated** if cross-model spread is also ≤ 1.0
or shuffled-order spread is also ≤ 0.5. New rubrics should ship at
provisional; rubrics that gate critical decisions (the OCS deep
gate, future Phase 3→4 gate via `pdd-to-deliver-app-eval`) should
move to strongly calibrated before they're trusted in production.

### Step 5 — Iterate the rubric

If detection rate < 80% OR variance > 0.5, edit the relevant skill's
`## LLM-as-Judge Rubric` section. Common moves:

- **Tighten dimension criteria** with explicit deduction rules
  (e.g. "factual error → 1-point deduction, hard ceiling 7").
- **Add "inflation guards"** — pattern-detection rules that cap
  the overall score regardless of per-dimension math (e.g. "same
  factual error in ≥2 entries → cap overall at 8.5").
- **Add or split dimensions** when one dimension is doing too much
  work (e.g. split a single "quality" dimension into correctness +
  refusal correctness).
- **Specify ground-truth references** the judge prompt should cite
  ("compare against `expected_answer_summary`; deduct for any
  semantic divergence").

After editing the rubric, repeat steps 2–4. Append the new run with
the new rubric version to the same `<rubric-name>-runs.md` file.
**Do not delete prior runs** — the audit trail is the point.

### Step 6 — Stop when calibrated

A rubric is calibrated when:
- Detection rate ≥ 80% on the ground-truth set.
- **Dimension coverage (Step 3b): every applicable fitness axis has a
  dimension, and the thin negative control scores below `pass`.**
- **Anchor durability (Step 3c): every control carries `measured_on`, its
  evidence table, and a mutability notice — so the next revision can
  re-derive the number instead of trusting it.**
- Variance ≤ 0.5 across ≥3 consecutive runs.
- The score on a known-flawed artifact is below 8 (i.e., the rubric
  is willing to deduct meaningfully).

Mark the rubric calibrated in `<rubric-name>-runs.md`'s footer with
the calibrating commit SHA. Future rubric edits should re-run
calibration before merging.

## Invocation

This skill is **operator-driven**, not orchestrated. It runs ad-hoc
against an opp folder that already has captured artifacts and a
ground-truth catalogue:

```text
/ace:eval <opp-name> --calibrate <rubric-name>
```

(Slash command not yet implemented; for now invoke this skill
manually as part of the rubric-improvement loop. The
`<rubric-name>` argument selects which `-eval` skill to calibrate;
the catalogue and run-record paths derive from it.)

## What this skill does NOT do

- It does not grade artifacts directly. It grades rubrics. The
  per-skill `-eval` rubrics still do the artifact grading.
- It does not aggregate per-skill scores. That's `opp-eval`'s job.
- It does not run automatically as part of `--mode review` gates.
  Calibration is meta-eval — it's the work that happens between
  runs to make the next run's evals trustworthy.

## MCP Tools Used

- Google Drive: `drive_read_file`, `drive_create_file`,
  `drive_list_folder`, `drive_create_folder`
- Whatever MCP tools the calibrated rubric needs (no direct
  calls from this skill — it dispatches the rubric)

## Why this matters

ACE's whole evaluation story is "LLM-as-Judge + umbrella
aggregation." Without calibration the LLM-as-Judge half is anchored
to model generosity, not artifact quality. Calibration is what makes
the evaluation system **self-improving** rather than
self-congratulating: every rubric edit must show measurable
improvement in detection rate or variance against a real
ground-truth set, captured in an auditable run-record.

## See also

- **`docs/eval-calibration-learnings.md`** — durable reference for
  patterns and anti-patterns observed across the 0.9.0–0.9.5
  calibration trajectory. The "recipes" section walks through how
  to build a new `-eval` skill end-to-end. Read this before
  authoring a new rubric or iterating on an existing one.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-28 | Initial version. Defines the ground-truth catalogue, multi-run variance protocol, detection-rate metric, and iteration loop. Companion to `pdd-to-deliver-app-eval` and the tightened `ocs-chatbot-eval` rubric, both of which cite this skill as their calibration source. | ACE team (eval system buildout) |
| 2026-05-05 | Refresh the OCS-transcript example header in the known-issues template to match the new run-scoped path scheme (`5-ocs/ocs-chatbot-qa_transcript-deep.md` instead of the dated `qa-captures/...`). Cosmetic; no methodology change. | ACE team |
| 2026-08-13 | **Added Step 3c — anchors must be re-derivable without the live artifact (ace#1212).** Anchors were recorded as pointers (*"opp X / run Y, Nova app Z scored N"*), and all three of those are mutable: Nova apps get edited, runs get repaired by the `repairs[]` loop the rubrics themselves drive, and a ratio over a judge-built denominator moves when the next grader enumerates differently. Since an anchor IS the regression test for a rubric revision ("any revision must still score that bank ≤3"), a drifted anchor lets a rubric pass its own gate while having quietly broken. Measured on `pdd-to-learn-app-eval`'s positive control 2026-08-13: **three different recorded readings of the same app** — 0.78 (denominator 32) in the rubric, 0.767 in that run's own prior verdict, and 0.904 (denominator **52**) live post-repair. The app changed; the *enumeration* changed far more (10 counter-intuitive rules + 12 operations → 19 + 14 in two days), so the dominant error bar was never the artifact. New rule: every anchor carries `measured_on`, the evidence table the score was computed from (the denominator's ENTRIES, not just its size), an explicit mutability notice, and BOTH readings where the artifact has since moved — the delta is information, not noise to be tidied away. Added a durability ordering (frozen artifact copy > inline evidence table > live pointer) and a scope note separating **anchors** (load-bearing, dated) from **provenance** (change-log citations explaining where a rule came from — explicitly exempt, since dating those buries the anchors that matter). Added to the Step-6 stop conditions. *Enforced:* `test/skills/eval-calibration-anchors.test.ts` fails any anchor section in a `skills/*-eval/SKILL.md` that cites a run id or app UUID without `measured_on` — a visibility gate, not a semantics gate. | ACE team |
| 2026-05-29 | **Added Step 3b (dimension coverage) — the ITN post-mortem fix.** Detection rate can't surface a *missing* dimension (a blind spot is never a known issue), which is how the app evals scored 9.6 on a hollow build. New step: enumerate the fitness axes separating conformant from deployable, confirm a dimension touches each, and calibrate against an expert reference (ITN `[Final]`) + a thin negative control (ITN ACE build `20260528-1607`) that MUST score below `pass`. Added to the Step-6 stop conditions. Per `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md`. | ACE team |
| 2026-09-06 | **Stop routing concerns to a gate brief that does not exist (dimagi-internal/ace#1884).** 0.13.116 removed the per-skill gate-brief file class and the ace#1880 sweep removed the remaining `*.md` PATHS, but prose directives naming the gate brief as a DESTINATION survived in 15 files — a concern "surfaced in the gate brief" is surfaced nowhere. Repointed at the verdict YAML's `auto_surfaced` block, which is what the orchestrator actually renders the pause summary from. Gated by the new destination check in `test/skills/gate-brief-removal-complete.test.ts`. | ACE team |
