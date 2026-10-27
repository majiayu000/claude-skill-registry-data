---
name: llo-uat-eval
description: >
  Grade an llo-uat results compilation against PDD success metrics —
  coverage completeness, sign-off clarity, blocker resolution.
disable-model-invocation: true
---

# LLO UAT Eval

`llo-uat` is the Phase 9 skill that compiles user-acceptance-test
results from collected LLO responses ahead of `llo-launch`. It is the
last quality gate before activation: blockers surfaced here either
become launch-stoppers or get a documented resolution path. This
rubric grades whether that compilation faithfully covers the PDD's
success metrics, names the LLOs giving sign-off, and resolves every
flagged blocker.

This is a Phase 9 process-skill eval, sibling of `llo-launch-eval`
which grades the activation step that follows. See
`skills/_eval-template.md` for shared contracts and
`skills/eval-calibration/SKILL.md` for calibration methodology.

## Inputs

Pipeline-only: grades a run's Phase 9 UAT compilation, which exists only in a run.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `1-design/idea-to-pdd.md` | source PDD; Success Metrics + Evidence Model define UAT coverage expectation |
| Phase 9 | `9-execution-manager/llo-uat_results.md` | UAT compilation under judgment |
| Phase 9 | `9-execution-manager/llo-onboarding_*` artifacts | LLO roster (who *should* have signed off) |
| Phase 6/2 | `3-commcare/app-deploy_summary.md` | what was deployed for UAT to exercise |

## Products

- `9-execution-manager/llo-uat-eval_verdict.yaml` — verdict YAML per `_eval-template.md § Verdict YAML contract`. Filename uses **this eval skill's** name (`llo-uat-eval`), not the bare producer name — per the 0.12.0 Option-α rule in `agents/ace-orchestrator.md § Per-Step Eval Hook`.

## Process

1. **Read inputs from GDrive** (paths in `## Inputs` above). Also read
   `runs/<run-id>/run_state.yaml` to confirm Phase 9 reached `llo-uat`.

2. **Detect "phase not run" mode.** If `run_state.yaml` shows
   `phases.execution-management.llo-uat` not `done` or
   `9-execution-manager/llo-uat_results.md` is missing, emit `verdict:
   incomplete` immediately with `[INFO] Phase 9 llo-uat not run; not
   gradable yet`.

3. **Extract the PDD's UAT-coverage expectation:**
   - Every Success Metric (rows of the `## Success Metrics` table).
   - Every Layer A verification rule from the Evidence Model that the
     UAT should have exercised (GPS, photo, consent gate, etc.).
   - The expected LLO roster (one sign-off per LLO from the
     onboarding artifact).

4. **Grade across 6 dimensions.** Each dimension is 0–10. Overall
   score is the weighted mean.

   `uat_coverage_completeness` grades whether the UAT *exercised* the PDD's
   metric list — a PDD-conformance check (intra-chain). It says nothing
   about whether the metrics actually **passed**. `metric_outcome_fitness`
   is the out-of-chain fitness dimension (per `_eval-template.md § The
   out-of-chain fitness requirement`): it grades the observed UAT
   **outcome** — did the success metrics clear their declared thresholds in
   the real test — against the real results, not against the PDD's list of
   what to measure. A UAT can cover 100% of metrics and still report that
   most of them *failed*; coverage alone would score that ~9 while the opp
   is plainly not launch-ready. `metric_outcome_fitness` carries the teeth
   that catch it.

   | Dimension | Weight | Criteria |
   |---|---|---|
   | **UAT coverage completeness** | 0.20 | Every PDD Success Metric and every Layer A verification rule must be exercised by at least one UAT scenario in `llo-uat_results.md`. Missing a Success Metric = 2-point deduction per metric. Missing a Layer A rule = 1.5-point deduction per rule. **Hard block:** UAT covering < 50% of declared Success Metrics is a fail (≤ 3) — the gate is not actually a gate. (This is a *coverage* check — see `metric_outcome_fitness` for whether the covered metrics actually passed.) |
   | **Metric-outcome fitness** | 0.25 | **OUT-OF-CHAIN FITNESS.** Grade the observed UAT *results*, not the metric list. For each PDD Success Metric the UAT reported a result for, did the measured value actually clear the declared threshold (e.g. PDD target "photo pass rate ≥ 90%" — did the real UAT measure ≥ 90%)? Score against the recorded outcomes: 9-10 = every measured metric cleared its threshold with margin; 5-7 = metrics passed but several only marginally, or one secondary metric missed; ≤ 3 = a primary Success Metric measurably *missed* its threshold, or the results are reported with no measured value to check against (a UAT that records activity but not pass/fail outcomes is not a real acceptance test). Anchor every score to the actual reported number in `llo-uat_results.md`; if a metric is "covered" but has no measured result, treat it as an outcome of *unknown/unverified* and deduct 2 points — coverage without a measured outcome is theater. **Hard block:** any primary Success Metric whose measured UAT value missed its declared threshold while the doc still recommends `launch` = fail (≤ 3). |
   | **LLO sign-off clarity** | 0.20 | Every LLO in the onboarding roster must have an explicit sign-off entry: named LLO, named contact, explicit `go` / `no-go` per Success Metric (or per overall opp, when the PDD is metric-light). Implicit sign-off ("LLO 1 didn't object") = 2-point deduction per LLO. Missing entry entirely = 3-point deduction per LLO. **Hard block:** ≥ 1 LLO explicit `no-go` recorded but the doc still recommends launch = fail (≤ 3). |
   | **Blocker resolution** | 0.15 | Every blocker flagged in the UAT must have a resolution path: fixed (with evidence), accepted-with-mitigation (with named owner + mitigation), or escalated (with named decision-maker + deadline). Unresolved blockers = 2-point deduction per blocker. **Hard block:** any blocker recorded as unresolved with no documented path = fail (≤ 3) — that's an open launch risk. |
   | **Evidence-citation discipline** | 0.10 | Every claim ("LLO 2 hit the photo-pass-rate target", "GPS accuracy < 30m on 95% of test visits") must cite a specific UAT artifact (transcript, photo log, calibration sheet) rather than improvise. Uncited claims are 0.5-point deductions per occurrence. The skill is supposed to *compile* evidence, not summarize from memory. |
   | **Launch-readiness recommendation** | 0.10 | The doc must end with a clear `recommend: launch | hold | iterate` decision keyed to the dimensions above. Missing recommendation = fail (≤ 3). Vague recommendation ("looking good", "we should be fine") without a keyword decision = 2-point deduction. Recommendation contradicts the evidence (says `launch` despite an unresolved blocker, an LLO `no-go`, or a missed primary Success Metric) = fail (≤ 3). |

   **Deduction rules:**
   - Any single dimension ≤ 3 → suite verdict `fail`, regardless of
     overall mean. (Last gate before activation; failure modes here
     ship to real LLOs and FLWs.)
   - **Inflation guard (mirrors prior rubrics):** if the rubric
     surfaces ≥ 2 `[WARN]`-tier `auto_surfaced` entries, overall is
     capped at **8.5**.
   - **Pre-cap and post-cap reporting** per `eval-calibration` § 0.9.4
     guidance.

   **Verdict tiers:**
   - `pass` — overall ≥ 7.0, no dimension ≤ 3.
   - `warn` — overall ≥ 5.0 < 7.0, or any inflation cap binds.
   - `fail` — overall < 5.0 OR any dimension ≤ 3.
   - `incomplete` — Phase 9 `llo-uat` not run, or artifact missing entirely.

   **Severity tiers** for `auto_surfaced` entries:
   - `[BLOCKER]` — must-fix before launch. Counts as a hard defect.
   - `[WARN]` — should-fix; counts toward inflation guard.
   - `[INFO]` — observational, no action required.

5. **Write the verdict YAML** to
   `9-execution-manager/llo-uat-eval_verdict.yaml` using the shape from
   `skills/_eval-template.md § Verdict YAML contract`. Dimensions:

   ```yaml
   dimensions:
     uat_coverage_completeness:       { weight: 0.20 }
     metric_outcome_fitness:          { weight: 0.25 }
     llo_signoff_clarity:             { weight: 0.20 }
     blocker_resolution:              { weight: 0.15 }
     evidence_citation_discipline:    { weight: 0.10 }
     launch_readiness_recommendation: { weight: 0.10 }
   ```

   Weights sum: 0.20 + 0.25 + 0.20 + 0.15 + 0.10 + 0.10 = 1.00.

6. **Auto-surfaced concerns** (per `_eval-template.md § Auto-surfaced
   severity rules`, plus skill-specific surfaces):
   - `[BLOCKER]` for any dimension scoring ≤ 3.
   - `[BLOCKER]` for any primary Success Metric whose measured UAT value
     missed its declared threshold while the doc recommends `launch`.
   - `[BLOCKER]` for any unresolved UAT blocker without a documented
     resolution path.
   - `[BLOCKER]` for any LLO `no-go` recorded but doc still recommends launch.
   - `[BLOCKER]` if overall score is below 7.0.
   - `[WARN]` per PDD Success Metric not exercised by any UAT scenario.
   - `[WARN]` per Success Metric "covered" but reported with no measured
     pass/fail value (outcome unverified).
   - `[WARN]` per missing or implicit LLO sign-off.
   - `[WARN]` per uncited cycle-level claim.
   - `[INFO]` per Layer A rule the UAT did not exercise but
     `connect-opp-setup` already enforces structurally.

## LLM-as-Judge Rubric

Calibration target on a real UAT compilation:

- **Detection rate:** ≥ 80% of catalogued UAT-compilation issues from
  `eval-calibration/known-issues.md § LLO UAT`.
- **Inter-run variance:** ≤ 0.5 across 3 same-model runs.
- **Cross-model variance:** ≤ 1.0 for strong calibration.

This rubric ships at **provisional** until a real Phase 9 UAT
compilation produces ground truth. Until then, it correctly emits
`incomplete` on opps where Phase 9 hasn't reached `llo-uat`.

## Archetypes

| Archetype | What this skill does |
|---|---|
| `atomic-visit` | Default. Grades per-visit Success Metric coverage (visits/day, photo pass rate, GPS accuracy). |
| `focus-group` | Grades per-session Success Metric coverage (session completion, transcript quality, theme synthesis). Adds a "facilitator-vs-participant sign-off" sub-check under `llo_signoff_clarity` (FGD UAT requires both roles to sign off). |
| `multi-stage` | Grades stage-by-stage UAT coverage. Adds a "per-stage gate-pass evidence" sub-check under `uat_coverage_completeness` (each stage transition's pre-conditions must be exercised). |

## MCP Tools Used

See `skills/_eval-template.md § MCP Tools Used (stock)`. No external
API calls beyond Drive.

## Mode Behavior

See `skills/_eval-template.md § Mode Behavior (stock)`.

## Dry-Run Behavior

Per `skills/_eval-template.md § Dry-Run Behavior (stock)`. Read-only,
verdict + report written to Drive.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-09 | Initial version. 5 dimensions: uat_coverage_completeness (0.30 — most load-bearing for "did we actually test what we said we'd test"), llo_signoff_clarity (0.25), blocker_resolution (0.20), evidence_citation_discipline (0.15), launch_readiness_recommendation (0.10). Inflation guard at 8.5. Three hard-block rules: <50% Success Metric coverage; LLO no-go but recommend launch; unresolved blocker with no path. Explicit `incomplete` verdict when Phase 9 hasn't reached `llo-uat`. Last quality gate before `llo-launch` activation. Ships at provisional calibration until a real UAT compilation produces ground truth. Closes the "not yet migrated" registry row for `llo-uat`. | ACE team |
| 2026-05-29 | Added `metric_outcome_fitness` (0.25) — the out-of-chain fitness dimension grading the observed UAT *outcome* (did each Success Metric's measured value clear its declared threshold) against the real results, separate from `uat_coverage_completeness` which only grades whether the metric list was *exercised*. Carries a hard block: a primary Success Metric measurably missing its threshold while the doc recommends `launch` = fail. Reweighted: uat_coverage_completeness 0.30→0.20, llo_signoff_clarity 0.25→0.20, blocker_resolution 0.20→0.15, evidence_citation_discipline 0.15→0.10; launch_readiness_recommendation held at 0.10. Per `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md` — coverage-of-the-metric-list is PDD conformance; a UAT could exercise every metric and still report most failing, scoring ~9 on coverage while the opp is not launch-ready. Weights sum to 1.00. | ACE team |
