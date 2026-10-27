---
name: opp-eval
description: >
  Internal /ace:run step — Umbrella aggregator that rolls every per-skill -eval verdict into a
  run-level scorecard.
user-invocable: false
disable-model-invocation: false
---

# Opportunity Eval

Aggregate every per-skill `-eval` verdict for an opportunity into a
single run-level scorecard, surface the weakest skills + dimensions,
and draft improvement recommendations. opp-eval is the **umbrella**
half of ACE's evaluation story — each per-skill eval judges its own
artifact in isolation; opp-eval judges the whole opp.

opp-eval is **ad-hoc** and **opt-in**. It is not part of the
`--mode review` auto-pause-at-gate flow. Run it anytime during or
after an opportunity to answer "how well did this run go overall, and
what should I improve?" — the operator's original ask for "one
overview judge/review agent that we can apply to overall runs."

See `skills/README.md § QA vs Eval — the two-phase pattern` for the
framework rationale and the uniform verdict-YAML shape that this
aggregator reads.

## Inputs

Pipeline-only: rolls up the per-skill `-eval` verdicts of one run; its inputs are that run's verdict files (§ Process).

## Modes

All paths below are run-scoped under
`ACE/<opp-name>/runs/<run-id>/10-closeout/opp-eval/` (opp-eval's own
subfolder — it writes more than one artifact and per-run isolation
keeps re-runs clean).

| Mode | What it does | LLM cost | Writes |
|---|---|---|---|
| `--quick` | Structural-only: walk the artifact manifest for the opp's current phase, confirm every required (non-dated) artifact exists in the run folder. No verdict aggregation. | None | stdout summary + `10-closeout/opp-eval/opp-eval_scorecard-quick.md` |
| `--deep` | Structural check **plus** aggregation: discover every `runs/<run-id>/<phase>/*_verdict*.yaml`, roll scores into skill-category dimensions, compute run-level verdict, emit per-skill narrative + improvement recommendations | LLM-as-Judge (recommendation drafting) | `10-closeout/opp-eval/opp-eval_scorecard-deep.md` (human) + `10-closeout/opp-eval/opp-eval_verdict-deep.yaml` (machine) |
| `--monitor` | Same as `--deep`, plus append a one-liner to `10-closeout/opp-eval/opp-eval_trend.md` | LLM-as-Judge | Same as `--deep` + trend append |

If no mode is passed, default to `--quick`.

## Process

1. **Read the PDD for archetype context (best-effort, not required).**
   Look up `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md`. If present, read the `archetype:`
   field and `## Evidence Model` section and keep them in scope for
   recommendation phrasing. **If the PDD is missing, do not fail** —
   opp-eval is designed to work on partially-completed opps (that's
   exactly the point of `--quick`). Emit `[INFO] pdd.md not found —
   recommendations will be archetype-agnostic` and continue.

2. **Read `run_state.yaml`** from `ACE/<opp-name>/run_state.yaml` to determine
   the opp's current phase. This drives which manifest entries to check
   in step 3. If `run_state.yaml` is missing, assume `design` phase (only
   the earliest required artifacts are expected).

3. **Structural check (runs in every mode).** For each required,
   non-dated artifact in `lib/artifact-manifest.ts` whose `phase` is at
   or before the opp's current phase, verify the path exists in the
   Drive folder via `drive_list_folder`. Build three lists: `present`,
   `missing`, `unexpected`. Mirror the shape of `validateFixture()` in
   `lib/artifact-manifest.ts` — opp-eval is effectively the live-folder
   equivalent of that fixture-validation helper.

4. **Short-circuit on `--quick`.** Write the quick scorecard (see §
   Quick-mode output below), print a one-line stdout summary
   (`present/expected artifacts, N missing`), and stop. Do not read any
   verdict files. No LLM calls.

5. **Discover verdicts.** Walk each phase folder under
   `ACE/<opp-name>/runs/<run-id>/` (`1-design/`, `3-commcare/`,
   `4-connect/`, `5-ocs/`, `6-qa-and-training/`,
   `8-solicitation-management/`, `9-execution-manager/`,
   `10-closeout/`) and collect every file matching
   `*_verdict*.yaml`. Also descend one level into
   `10-closeout/opp-eval/` for the umbrella's own verdicts (excluded
   from aggregation by `skill: opp-eval` filter — see step 6). For
   each file, parse as YAML. Expected top-level keys per
   `skills/README.md § QA vs Eval — the two-phase pattern`:
   `skill`, `target`, `mode`, `ran_at`, `capture_path`,
   `overall_score`, `verdict`, `dimensions`, optional `per_item`,
   optional `gate`.

   **Tolerate missing fields.** If a verdict YAML is malformed or
   missing a required key, **do not crash**. Emit
   `[INFO] skill <X> verdict missing required field <Y>` and continue.
   The aggregator must surface gaps, not hide behind them.

6. **Group verdicts into skill categories.** Map each verdict's `skill`
   to one of seven run-level dimensions:

   | Category | Weight | Covers skills |
   |---|---|---|
   | `design`        | 0.20 | `idea-to-pdd`, `pdd-to-test-prompts` |
   | `commcare`      | 0.18 | `pdd-to-learn-app`, `pdd-to-deliver-app`, `app-deploy`, `app-test-cases`, `training-llo-guide`, `training-flw-guide`, `training-quick-reference`, `training-faq`, `training-onboarding-email`, `training-deck-generate` |
   | `connect`       | 0.13 | `connect-program-setup`, `connect-opp-setup` |
   | `ocs`           | 0.18 | `ocs-agent-setup`, `ocs-chatbot-eval-quick`, `ocs-chatbot-eval-deep` |
   | `solicitation`  | 0.10 | `solicitation-create`, `solicitation-review` (added 0.12.0 — Phase 8) |
   | `operate`       | 0.13 | `llo-onboarding`, `llo-uat`, `llo-launch`, `ocs-chatbot-eval-monitor`, `flw-data-review`, `timeline-monitor` |
   | `closeout`      | 0.08 | `opp-closeout`, `llo-feedback`, `learnings-summary`, `cycle-grade` |

   Category weights sum to 1.0. Per-category score is the simple mean
   of all verdicts that map into the category, **excluding any verdict
   with `verdict: incomplete`** (added 0.9.8). An `incomplete` verdict
   means the rubric correctly detected a structural gap (degraded mode,
   phase not run, target artifact missing) and refused to grade —
   that's a coverage gap, not a quality signal, and shouldn't affect
   the category mean.

   Categories with zero gradable verdicts (zero non-incomplete) score
   `null` and their weight is redistributed proportionally across
   categories that **did** score — so a partial opp (e.g., still in
   Phase 4, no OCS verdict yet) gets a meaningful run-level number
   rather than an artificially low one.

7. **Compute the run-level overall score.** Weighted mean of the
   non-null category scores, with weights renormalized per step 6. The
   formula is: `sum(score_i * weight_i) / sum(weight_i)` for categories
   where `score_i` is not null.

8. **Classify the run-level verdict (coverage-aware as of 0.8.0).** The
   raw weighted-mean score is computed first; then **coverage** caps
   the verdict regardless of score. This is the explicit fix for the
   "1/6 categories scored 8.9 → run-level PASS" inflation surfaced by
   the first smoke run.

   Coverage tier (count of categories with score ≠ null — i.e.,
   categories with at least one non-incomplete verdict — ignoring
   categories with `expected_at_phase` later than the opp's current
   phase):

   | Categories scored | Tier | Verdict cap | Notes |
   |---|---|---|---|
   | 0 | none     | `incomplete` | Nothing to grade |
   | 1 | thin     | `incomplete` | Single-category score isn't a run grade — flag `[INFO]` |
   | 2 | partial  | `warn` (max) | One cross-skill signal exists but most of the run is unmeasured |
   | 3 | adequate | `pass` if raw ≥ 7 | Less than half-coverage; raw score governs |
   | 4 | adequate | `pass` if raw ≥ 7 | Half-coverage; raw score governs |
   | 5+ | full   | `pass` if raw ≥ 7; `warn` 4.0–6.9; `fail` <4.0 | Cross-skill view is real |

   The verdict cap applies AFTER the raw score: a 9.5 raw with
   1-category coverage emits `incomplete`, not a misleading PASS.
   `incomplete` is a new verdict introduced in 0.8.0 — downstream
   readers treat it as "needs more rubric coverage before this number
   is meaningful," not as a quality fail.

   **Deployability cap (added 2026-05-29):** the verdict is ALSO capped
   at `warn` by the independent deployability spot-check (step 10b) when
   that probe scores < 5 against a would-be PASS rollup. This is the
   anti-laundering backstop — coverage breadth is not fitness depth, and
   a high rollup of inflated per-skill scores must not survive an
   independent raw-artifact judgment that the build is undeployable.

9. **Build per-skill breakdown.** For each discovered verdict, capture:
   - `ref` — the eval skill name + mode (e.g. `ocs-chatbot-eval-deep`)
   - `score` — the verdict's `overall_score`
   - `verdict` — pass / warn / fail
   - `note` — one-line summary: overall score + weakest-dimension name +
     its score. Weakest dimension is the `dimensions` entry with the
     lowest `score` value.

10. **Draft improvement recommendations (LLM-as-Judge).** For each
    verdict that is `warn` or `fail`, and for each `dimensions` entry
    with `score < 6.0` across **any** verdict, generate a one-line
    recommendation. Seed the prompt with:
    - The verdict YAML (full).
    - The relevant skill's `## LLM-as-Judge Rubric` section from
      `skills/<skill-name>/SKILL.md` if present — read with
      `drive_read_file`'s local-file equivalent (or by locating the
      skill definition under `skills/`). If the skill has no rubric
      section, emit `[INFO] skill <X> lacks a rubric — recommendation
      will be generic`. (That's the forcing function for per-skill
      rubric work.)
    - A terse instruction: "Given this verdict, propose one concrete
      change that would move the weakest dimension toward 8+."

    Keep each recommendation to a single sentence, imperative voice,
    actionable (point at a skill + what to change). Example:
    `"Tagging dimension consistently below 7.0 across 2 runs —
    consider tightening [training-gap] application rules in the golden
    template prompt"`.

10b. **Independent deployability spot-check (fitness backstop — added
    2026-05-29).** opp-eval's rollup trusts the upstream verdicts, which
    means it *launders* any inflation in them: if every per-skill eval
    is conformance-only and inflated, the rollup computes a high number
    and stamps PASS (the ITN failure mode — both app evals scored 9.6 on
    a hollow build and the cycle grade would have rolled straight up).
    To break the self-referential loop at the one funnel point, `--deep`
    and `--monitor` run **one** LLM-as-Judge probe against the
    highest-stakes **raw artifact** the opp has produced — decoupled
    from every upstream verdict.

    - **Pick the artifact** (first available, in priority order): the
      built Deliver app Nova blueprint (`get_app` on the deliver
      `nova_app_id` from `3-commcare/pdd-to-deliver-app_summary.md`) →
      the generated synthetic records → the published solicitation body.
    - **The probe prompt** (does NOT see the upstream scores): "Reading
      this actual artifact, would a Dimagi domain expert ship it to a
      real LLO today? Score 0–10 on deployability and name the concrete
      blockers (missing input validation, capture fidelity, case
      write-back, language conformance, enforcement — whatever applies)." This
      is the same out-of-chain fitness bar the per-skill rubrics now use
      (`_eval-template.md § out-of-chain fitness requirement`).
    - **Hard-cap rule:** if the deployability probe scores **< 5** while
      the rolled-up overall is **≥ 7** (would-be PASS), cap the
      run-level verdict at **`warn`** and surface a `[BLOCKER]`:
      "rollup says PASS but the independent deployability spot-check
      found the artifact undeployable (score X, blockers: …) — the
      per-skill evals for this category are inflated; recalibrate before
      trusting this cycle grade." Record the probe score + blockers in
      the verdict YAML under `deployability_probe`.
    - The probe is scoped (one artifact, one judgment) — opp-eval is
      still an aggregator, not a full re-grader. This is the single
      deliberate exception to "trust the upstream judgments."

11. **Write the machine-readable verdict** to
    `ACE/<opp-name>/runs/<run-id>/10-closeout/opp-eval/opp-eval_verdict-<mode>.yaml`
    (only for `--deep` and `--monitor`). Uses the shared verdict shape
    — see § Verdict YAML Shape below.

12. **Write the human-readable scorecard** to
    `ACE/<opp-name>/runs/<run-id>/10-closeout/opp-eval/opp-eval_scorecard-<mode>.md`.
    Shape documented in § Scorecard Output below.

<!-- 0.13.116: gate-brief write step removed (step 13 was
"Write the gate brief (uniform contract)"). The orchestrator composes
pause-time summaries directly from verdict YAMLs, and
`lib/artifact-manifest.ts` registers no gate-brief artifact. The
`## Gate Brief` section below stays as a specification of that summary.
Cleanup completed 2026-09-01, dimagi-internal/ace#1880. -->

14. **In `--monitor` mode**, append a single-line entry to
    `ACE/<opp-name>/runs/<run-id>/10-closeout/opp-eval/opp-eval_trend.md`
    with date, overall score, each non-null category score, and the
    number of verdicts aggregated. One row per run so drift is visible
    at a glance.

15. **Write `phases.closeout.products.opp_eval`** to the current run's
    `run_state.yaml` so downstream readers (ace-web summary in
    particular) get the headline score without re-parsing the
    scorecard markdown.

    ```yaml
    phases:
      closeout:
        products:
          opp_eval:
            mode: <quick | deep | monitor>
            overall_score: <0-100 weighted score from Step 7>
            verdict: <pass | warn | partial | fail | incomplete>
            scorecard_file_id: <Drive fileId of opp-eval_scorecard-<mode>.md>
            verdict_file_id: <Drive fileId of opp-eval_verdict-<mode>.yaml — null on --quick>
            trend_file_id: <Drive fileId of opp-eval_trend.md — null outside --monitor>
            evaluated_at: <ISO timestamp>
    ```

    Apply via `mcp__plugin_ace_ace-gdrive__update_yaml_file` with
    `merge: 'deep'` (partial phase-child patch — `deep` preserves the
    phase's `status`/`steps`; `two-level` would drop them, #572/#587).
    Sole writer of `products.opp_eval`. Each
    re-run replaces the `opp_eval` keys in full — this is intended; consumers
    read the latest scorecard, not the history (the trend file
    captures history).

## LLM-as-Judge Rubric

opp-eval's rubric is **aggregation rules**, not a per-response grader.
The per-skill verdicts already did the LLM-as-Judge grading; opp-eval
rolls those scores up and decides what's worth flagging as a
recommendation.

**Category scoring rules:**
- Per-category score = simple mean of the `overall_score` values of
  every verdict whose `skill` maps into that category (see the
  category table in step 6).
- Categories with zero verdicts score `null` (not 0). A missing verdict
  is an **information gap**, not a zero.
- Weights renormalize across the non-null categories so a partial opp
  isn't penalized for being early in its lifecycle.

**Run-level scoring rules:**
- Overall = weighted mean of non-null category scores.
- Verdict: pass ≥ 7.0 · warn 4.0–6.9 · fail < 4.0.

**Recommendation triggers (one recommendation per trigger):**
- Any verdict with `verdict: warn` or `verdict: fail`.
- Any `dimensions` entry (inside any verdict) with `score < 6.0`.
- Any skill-category with only 1 verdict when ≥ 3 are expected at the
  opp's current phase — surfaced as `[INFO] thin coverage` recommendation.

**What opp-eval will NOT do:**
- Re-grade any individual response. That's the per-skill eval's job.
  **One scoped exception (2026-05-29):** the deployability spot-check
  (step 10b) makes a single independent fitness judgment on the
  highest-stakes raw artifact — not a per-response re-grade, but a
  backstop against laundering inflated upstream scores into a PASS.
- Invoke any `-qa` or `-eval` skill. Evidence is pre-captured; opp-eval
  only aggregates (plus the one spot-check above).
- Block a gate. The brief exists for uniformity, not gating.

## Archetypes

**This skill is archetype-agnostic by design.** Per-skill `-eval`
skills already applied archetype-specific rubrics when they graded
their own artifact (e.g., `cycle-grade` adds the Research Quality
dimension for `focus-group` PDDs). opp-eval reads the resulting
verdict scores without re-branching on archetype — it trusts the
upstream judgments.

The one place archetype matters is **recommendation phrasing**: if
the PDD is available, opp-eval reads `archetype:` in step 1 and
passes it to the LLM prompt in step 10 so recommendations land in the
right domain vocabulary (e.g., "tighten the FGD facilitator
instructions" for `focus-group` vs. "tighten the visit-flow prompt"
for `atomic-visit`). If the PDD is missing, recommendations are
archetype-agnostic.

## Verdict YAML Shape

Written to
`ACE/<opp-name>/runs/<run-id>/10-closeout/opp-eval/opp-eval_verdict-<mode>.yaml`
in `--deep` and `--monitor` modes. Follows the shared shape from
`skills/README.md § QA vs Eval — the two-phase pattern`:

```yaml
skill: opp-eval
target: <opp-name>
mode: deep | monitor
ran_at: <ISO timestamp>
capture_path: runs/<run-id>/   # opp-eval reads a run directory, not a single file

overall_score: 0.0-10.0    # weighted, renormalized across non-null categories
verdict: pass | warn | fail   # capped at warn if deployability_probe.score < 5 and raw rollup >= 7

deployability_probe:          # independent raw-artifact fitness backstop (step 10b); --deep/--monitor only
  artifact: <which raw artifact was judged, e.g. "deliver app blueprint 2VI6...">
  score: 0.0-10.0             # out-of-chain "would an expert ship this?" judgment
  blockers: ["<concrete blocker>", ...]
  capped_verdict: true | false  # true if this probe forced the run verdict down to warn

dimensions:
  # For opp-eval, "dimensions" are skill categories. A null `score`
  # means no verdicts were found in this category; its weight is
  # renormalized away from the overall.
  design:       { score: X.X | null, weight: 0.20 }
  commcare:     { score: X.X | null, weight: 0.20 }
  connect:      { score: X.X | null, weight: 0.15 }
  ocs:          { score: X.X | null, weight: 0.20 }
  operate:      { score: X.X | null, weight: 0.15 }
  closeout:     { score: X.X | null, weight: 0.10 }

per_item:
  # One entry per verdict file discovered under runs/<run-id>/
  - ref: ocs-chatbot-eval-deep
    score: 8.4
    verdict: pass
    note: "Overall 8.4; weakest dim: tagging (6.8)"
  - ref: cycle-grade
    score: 6.2
    verdict: warn
    note: "Overall 6.2; weakest dim: research_quality (4.1)"

recommendations:
  # One per trigger from the rubric. Severity matches the trigger type.
  - for: ocs-chatbot-eval
    severity: warn
    recommendation: "Tagging dimension consistently below 7.0 across 2 runs — tighten [training-gap] application rules in golden template prompt"
  - for: cycle-grade
    severity: warn
    recommendation: "Research Quality scored 4.1 — consider adding an explicit FGD sampling plan section to the PDD template"
```

## Scorecard Output

### Quick-mode (`10-closeout/opp-eval/opp-eval_scorecard-quick.md`)

```markdown
# Opportunity Eval — Quick
Opportunity: <opp-name>
Generated: <ISO timestamp>
Current phase (from run_state.yaml): <phase>

## Structural check

- **Present:** N / M required artifacts for phase <phase>
- **Missing:** <list, or "none">
- **Unexpected:** <files in the folder that aren't in the manifest, or "none">

## Notes

<One line per INFO from the structural scan. Concrete examples:
  [INFO] run_state.yaml missing — assumed design phase (default)
  [INFO] 2 unexpected files are operator-maintained (improvement-backlog.md, iteration-log.md); safe to ignore
  [INFO] pdd.md archetype: focus-group — deep-mode recommendations will use FGD vocabulary
If no INFOs to surface, write "None.">

_Run `--deep` to aggregate verdicts and get improvement recommendations._
```

**Stdout summary format** (always printed, both quick and deep modes):
```
opp-eval <mode>: <P>/<M> present, <K> missing, <U> unexpected (phase: <phase>)
```
Example: `opp-eval quick: 4/5 present, 1 missing, 2 unexpected (phase: design)`

### Deep / monitor (`10-closeout/opp-eval/opp-eval_scorecard-<mode>.md`)

```markdown
# Opportunity Eval — <mode>
Opportunity: <opp-name>
Generated: <ISO timestamp>
Overall Score: X.X / 10 · Verdict: <pass | warn | fail>

## Category Breakdown

| Category | Score | Weight | Verdicts counted |
|---|---|---|---|
| design    | X.X | 0.20 | N |
| commcare  | X.X | 0.20 | N |
| connect   | —   | 0.15 | 0 (not yet run) |
| ocs       | X.X | 0.20 | N |
| operate   | X.X | 0.15 | N |
| closeout  | X.X | 0.10 | N |

## Per-Skill Results

| Skill | Score | Verdict | Weakest Dimension | Note |
|---|---|---|---|---|
| ocs-chatbot-eval-deep | 8.4 | PASS | tagging (6.8) | Overall 8.4; weakest dim: tagging |
| cycle-grade | 6.2 | WARN | research_quality (4.1) | Overall 6.2; weakest dim: research_quality |
| ... | ... | ... | ... | ... |

## Recommendations

- **[ocs-chatbot-eval · warn]** Tagging dimension consistently below 7.0 across 2 runs — tighten [training-gap] application rules in golden template prompt
- **[cycle-grade · warn]** Research Quality scored 4.1 — consider adding an explicit FGD sampling plan section to the PDD template

## Structural check

- Present: N / M required artifacts for phase <phase>
- Missing: <list, or "none">

## Notes

<Any [INFO] lines: missing PDD, malformed verdict YAMLs, skills without rubrics, thin coverage, etc.>
```

## Gate Brief — reference only, NOT an artifact this skill writes

**This skill writes no gate-brief file.** The write step was removed in
0.13.116 and `lib/artifact-manifest.ts` registers no gate-brief artifact.
opp-eval does not gate any phase in any case. What follows specifies the
*content* an operator (or future automation) should read out of this
skill's scorecard + verdict YAML — it is not a set of write instructions.
Do not emit it as a file.

Source artifacts: `10-closeout/opp-eval/opp-eval_scorecard-<mode>.md` +
`10-closeout/opp-eval/opp-eval_verdict-deep.yaml`.

- **Artifact Under Review:** path to the scorecard at
  `ACE/<opp-name>/runs/<run-id>/10-closeout/opp-eval/opp-eval_scorecard-<mode>.md`;
  summary is
  `<overall-score>/10 across <N> verdicts, run-level verdict <pass|warn|fail>`
- **What to Check** (emit these 4 items verbatim):
  - Overall score ≥ 7.0 and no category-level score below 5.0
  - Every expected skill category for the opp's current phase has
    at least one verdict (no information gaps)
  - Each recommendation has a concrete, actionable target — if any
    recommendation is too vague ("improve quality"), push back
  - Skills flagged as lacking a rubric are queued for rubric work
    before the next opp (forcing function)
- **Auto-Surfaced Concerns:** one line per signal:
  - `[BLOCKER]` if overall verdict is `fail`
  - `[WARN]` for each per-skill verdict that is `warn` or `fail`
  - `[WARN]` for each category whose score is below 5.0
  - `[INFO]` for each skill without a `## LLM-as-Judge Rubric` section
  - `[INFO]` for each category with no verdicts yet (thin coverage)
  - "None — all auto-checks passed." if pass with no warns
- **Recommended Disposition:** `Review` (opp-eval never auto-approves
  or auto-rejects a phase; the brief is advisory by design). Spell out
  `Review` verbatim so downstream readers don't confuse it with the 5
  gating skills' Approve/Reject/Iterate set.

## MCP Tools Used

- Google Drive: `drive_read_file`, `drive_list_folder`,
  `drive_create_file`, `drive_update_file`
- No OCS calls — opp-eval reads pre-captured verdicts, it does not
  exercise any artifact

## Mode Behavior

- **Auto:** Walk the manifest, aggregate verdicts, write
  scorecard + verdict. No pause. Print stdout summary.
- **Review:** Pause after aggregation to show the scorecard before
  writing the final files. opp-eval is advisory either way — there is
  no Approve/Reject prompt.

## Dry-Run Behavior

opp-eval has **no external side effects** (no emails, no API calls, no
tickets). In `--dry-run` mode it behaves identically to a normal run:
reads Drive, writes scorecard + verdict + brief to Drive. These are
all human-facing artifacts; Drive writes are not treated as effectful
for dry-run purposes (same convention as `ocs-chatbot-eval`).

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-19 | Initial version — umbrella eval aggregator. Three modes (`--quick` / `--deep` / `--monitor`); rolls every `verdicts/*.yaml` into a run-level scorecard across 6 skill-category dimensions, emits improvement recommendations, and writes a uniform-contract gate brief (advisory; does not gate a phase). | ACE team (opp-eval rollout) |
| 2026-04-19 | Quick-mode template: add `Unexpected:` row (skill was already surfacing unexpected files but the template omitted it); tighten Notes wording with three concrete examples; specify stdout summary format including unexpected count. Surfaced in first run against a real partial opp (cosmetics-fgd-pilot) | ACE team (qa/eval iteration loop) |
| 2026-05-05 | **Path-scheme migration on the umbrella aggregator.** Discovery (Step 5) walks each phase folder under `runs/<run-id>/` collecting `*_verdict*.yaml` (instead of `ACE/<opp>/verdicts/*.yaml`, which is gone). Outputs land under `10-closeout/opp-eval/`: scorecard (`opp-eval_scorecard-<mode>.md`), verdict (`opp-eval_verdict-<mode>.yaml`), gate brief (`opp-eval_gate-brief-deep.md`), and `--monitor` trend (`opp-eval_trend.md`). Verdict YAML `capture_path` field updated to `runs/<run-id>/`. Wiring fix — prior glob would have found zero verdicts on a fresh run. No behavior change beyond paths. | ACE team |
| 2026-05-29 | **Anti-laundering deployability backstop (ITN post-mortem).** Added step 10b: an independent LLM-as-Judge deployability spot-check on the highest-stakes raw artifact (deliver blueprint → synthetic records → solicitation), decoupled from all upstream verdicts. If it scores < 5 while the rollup is ≥ 7, the run verdict is capped at `warn` with a `[BLOCKER]`. Previously opp-eval was a pure score-rollup with no independent fitness term, so inflated per-skill scores (the ITN 9.6s) laundered straight into a cycle PASS. New `deployability_probe` block in the verdict YAML. The one scoped exception to "trust the upstream judgments." Per `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md`. | ACE team |

## Claims

If the run folder holds `claims.yaml`, roll its tally into the scorecard via `summarizeClaims`
(`lib/run-claims.ts`) and render the section with `renderClaimsSection`
(`lib/render-claims.ts`).

The scorecard is an INTERNAL artifact, so call it as
`renderClaimsSection(set, { audience: 'internal' })` — that is the only audience that
carries each claim's audit `evidence`. The DEFAULT is `'counterpart'`, which renders the
`says` sentence and never `evidence`: Drive file ids, MCP atom signatures and scraped-field
reliability caveats are the class `skills/agent-turn-review` § F bans from anything a
counterpart reads (ace#2386, ace#2420). What the counterpart herself sees is the run's
ace-web page, which renders the same claim set to the same contract.

`all_met` is TRUE only when EVERY claim is `MET`. A run where every ANSWERED claim passed but a
checkpoint never ran has **not** met its claims — `NOT REACHED` accuses, it never passes, and
reporting otherwise recreates the silence the mechanism exists to remove. Design:
`docs/superpowers/specs/2026-09-15-pre-run-claims-post-run-validation-design.md`.
