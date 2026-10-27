---
name: app-release-eval
description: >
  Grade whether every Learn and Deliver build was actually released so Connect can read deliver
  units. Needs the HQ app ids.
disable-model-invocation: false
---

# App Release Eval

`app-release` makes versioned + released builds for the Learn and Deliver
apps Nova uploaded as drafts. Connect's `Sync Deliver Units` reads only
*released* builds, so an unreleased app silently breaks the next phase
with an empty deliver-units list. This rubric grades whether the
release step delivered everything downstream needs.

Single-artifact eval. Sees `_eval-template.md` for shared contracts.
Authored 0.10.29 in response to turmeric run_time_followups item 2
(CCZ-marker regex bug in app-release).

## Inputs

| Source | Artifact | Used for |
|---|---|---|
| Phase 3 | `3-commcare/app-deploy_summary.md` | **context only** — `app-deploy` owns this file (HQ app ids, `hq_domain`). It carries no release state and must never be graded for any: the `releases:` cross-reference `app-release` used to append here was retired in ace#1636. |
| Phase 3 | `3-commcare/app-release_summary.md` | **the artifact `app-release` owns** — released `build_id` + version per app; the sole source for `build_id_traceability` |
| Phase 3 | `?latest=release` CCZ projection | deliver-unit list as Connect's Sync Deliver Units will see it (see `deliver_units_enumerable`) |
| Phase 4 (optional, later passes only) | `4-connect/connect-opp-setup.md` | live Connect confirmation of deliver-unit enumeration, when Phase 4 has already run |

**Do NOT grade against `run_state.yaml` (dimagi-internal/ace#1010).**
`app-release` explicitly disclaims that write — the **orchestrator** owns
it, at the Phase 3 boundary fence, which runs *after* the per-step evals.
So at the moment this eval fires, `run_state.yaml` is guaranteed not to
carry `hq_build_id` or a `phases.commcare-setup.steps.app-release` entry.
Grading it there scored a **perfect** release 6/10 on
`build_id_traceability` every single time — a fixed 0.8-point downward
bias, enough to move a `pass` toward `warn` on a build with any other
real finding. Grade the producer against its own contract, like every
other per-step eval does.

## Products

- `3-commcare/app-release-eval_verdict.yaml` — verdict YAML per `_eval-template.md § Verdict YAML contract`

## Process

**This rubric is graded in CODE, not by an LLM judge (2026-10-16).** Every
dimension below reads a fact an artifact or API already states, so
`lib/app-release-check.ts` computes it and writes the verdict — no subagent,
no judgment, no run-to-run variance. The steps after this block are the SPEC
that code implements; do not re-grade them by hand. Your whole job is to
gather the inputs and run the script:

1. `drive_read_file` → `3-commcare/app-release_summary.md`; save it locally.
2. `commcare_download_ccz` with `?latest=release` for each app (Learn and
   Deliver, `write_to_path` set so the bytes stay out of context); save each
   JSON response. A download that errors → pass `FAILED` for that app.
3. The PDD-payable deliver-unit slugs — `app-connect-coverage`'s role
   decisions (`3-commcare/app-connect-coverage_deliver.md`). Omit
   `--payable-slugs` if you cannot name them; the script then grades only
   "at least one unit" and says so.
4. Only when Phase 4 already ran: `connect_list_deliver_units` → JSON.
5. Run it, then `drive_create_file` the `--out` file to
   `3-commcare/app-release-eval_verdict.yaml`:

   ```bash
   ACE_ROOT="${CLAUDE_PLUGIN_ROOT:-$(python3 -c "import json,os; d=json.load(open(os.path.expanduser('~/.claude/plugins/installed_plugins.json'))); print(d['plugins']['ace@ace'][0]['installPath'])")}"
   node "$ACE_ROOT/node_modules/tsx/dist/cli.mjs" "$ACE_ROOT/scripts/fact-check-eval.ts" app-release \
     --summary <summary.md> --learn-ccz <learn.json|FAILED> --deliver-ccz <deliver.json|FAILED> \
     [--payable-slugs <slug,slug>] [--connect-deliver-units <du.json|FAILED>] \
     --target <opp>/<run-id> --out <local verdict.yaml>
   ```

The verdict carries `method: deterministic` and a `checks[]` entry per input
(an absent input is `unable`, never a silent pass). If a result looks wrong,
the fix is a code change with a test in `test/lib/fact-check-evals.test.ts`,
never a hand-edited verdict.

**Precedence — the owned artifact is the grading anchor (ace#1567).**
`app-release` owns exactly one artifact: `3-commcare/app-release_summary.md`
(its `§ Products` frontmatter contract). Everything else this rubric reads is
**corroboration** — live HQ reads, the CCZ projection, `app-deploy_summary.md`
(which belongs to `app-deploy` and carries no release state at all). So: only
the owned artifact can settle "did the skill run"; corroborating evidence that
DISAGREES is a real finding, and corroborating evidence that is merely ABSENT
is at most an `[INFO]`, never an ungradable verdict and never a deduction in
two dimensions at once. ace#1636 took the rule one step further and RETIRED
the `releases:` cross-reference `app-release` used to append to the deploy
summary, rather than leaving a write whose only hard reader had been
re-pointed away from it. This is the third recurrence of the same class in
this one rubric (ace#1010 →
`build_id_traceability`, ace#1439 → `both_apps_released`, ace#1567 → the
`incomplete` gate below), which is why it is now stated once, up front.
*Enforced:* `test/skills/eval-gate-artifact-ownership.test.ts`.

1. **Read inputs from GDrive** (paths in `## Inputs` above).

2. **Detect missing artifacts.** If `3-commcare/app-release_summary.md` is
   missing, or its frontmatter carries no `apps.*` block, emit
   `verdict: incomplete` immediately with `[INFO] app-release output missing —
   skill did not run or did not complete writing its artifact`. Do not score
   zero. That artifact is the ONLY one whose absence actually means
   `app-release` did not complete — never gate this verdict on a file another
   skill owns (ace#1567: a fully released, live-verified run read as "skill
   did not run" because a cross-reference append had been skipped, and in
   `opp-eval` `incomplete` is "not gradable", so the run lost its pass AND
   the real finding).

3. **Grade across 4 dimensions.** Each dimension is 0–10. Overall is
   the weighted mean.

   | Dimension | Weight | Criteria |
   |---|---|---|
   | **Both apps released** | 35% | **Read the keys the producer actually writes (ace#1439).** Per app: `apps.<app>.is_released: true` in **`3-commcare/app-release_summary.md`** frontmatter — a contract `app-release § Products` now DECLARES, so this dimension reads a key the producer is instructed to emit. The deploy summary carries no release state at all since ace#1636 retired the `releases:` cross-reference; **never look for release evidence there, and never deduct for its absence**. On a legacy run that still has the block, a disagreement is scored ONCE, in `build_id_traceability`, not twice across both. This dimension previously named `is_released` and `latest_released_version` **in the `releases:` block**, where neither has ever been written — the exact class ace#1010 fixed for `build_id_traceability`, surviving in the sibling dimension. A grader reading it literally deducts on a perfect release; on bednet-check-2-visit/20260814-2019 that was avoided only because the grader went and read the producer's contract. Per ace#1010's standing note: **never deduct for evidence the producer is not instructed to emit** — if a key you want is absent from BOTH artifacts, that is a finding against this rubric, not against the build. Either app missing release = ≤3 (fail). One app released, the other still draft = ≤6 (warn). |
   | **CCZ-marker integrity** | 25% | CCZ verification (Step 6 of app-release) confirms each released build has the canonical Connect markers (`connect.learn_module` / `connect.deliver_unit` / `connect.assessment`). Missing markers = ≤4 deduction per missing class. (Note: this is the dimension that catches turmeric run_time_followups item 2 — the CCZ regex bug that uses `<learn:` prefix instead of the actual `xmlns` attribute. A regex bug that mis-reports a perfectly-marked app as missing markers should surface as a [PLATFORM] entry on the CCZ-checker side, not a deduction here.) |
   | **Build-id traceability** | 20% | Graded **against `3-commcare/app-release_summary.md`** — the artifact `app-release` is contractually required to write (ace#1010). Per app, it must carry a released `build_id` and a version number. Missing `build_id` for an app = 4-point deduction. **`app-release_summary.md` is the SOLE source for this dimension** (ace#1636). The `releases:` block `app-release` used to append to `app-deploy_summary.md` was retired: it was skipped on 2 of 2 observed runs with no consequence, its only hard reader (`llo-launch`'s app-freshness gate) has been re-pointed at the owned artifact, and its corroborating role here produced a `[WARN]` on every clean run — noise, not signal. If a legacy run's deploy summary still carries a `releases:` block and it DISAGREES with `app-release_summary.md`, record a `[DRIFT]` entry naming both values; do not deduct, and never deduct for its absence. **Never deduct for `run_state.yaml` not carrying `hq_build_id` or an `app-release` step entry** — see the Inputs note: the orchestrator writes those minutes later, and grading them here is pure rubric noise. If a `run_state.yaml` written by a *previous* boundary-fence pass happens to be readable (e.g. on an `/ace:eval --all` re-grade), a disagreement with the summary is worth a `[DRIFT]` entry, not a deduction. |
   | **Connect deliver-units enumerable** | 20% | Does the released Deliver build actually expose deliver units for Connect to find? Score from whichever evidence exists, in this order: **(1) `?latest=release` CCZ projection (first-class, always available).** Download the released Deliver CCZ via the `?latest=release` projection — the literal artifact Connect's Sync Deliver Units consumes — and enumerate the forms carrying a `<learn:deliver>` marker. **The expected count is what the PDD declares PAYABLE, not the form count.** The standard ACE Deliver shape carries an unpaid registration form as a deliberate auxiliary participant with no `deliver_unit` (`app-connect-coverage § Step 2` decides this by role, not by form type — ace#1327), so 2 forms / 1 unit is the CORRECT reading of a PDD whose rule is "only the follow-up visit is paid". Read the payable stages from the PDD (§ Deliver App Specification / `products.pdd.program_parameters.payable_stage`) and compare against that: every payable form exposing a unit = full marks; a payable form with no unit = 4-point deduction; **zero units at all = 4-point deduction**. A unit on a form the PDD says is unpaid is a `[WARN]`, not a bonus — it is the shape that lets Phase 4 wire payment to a stage the programme does not pay for. Never deduct for units < forms without checking payability (ace#1331). Note also that Nova emits the MODULE slug as `<deliver id>` for every form in a module and Connect dedups `DeliverUnit` on `(app, slug)`, so one-unit-per-form is not even the shape a multi-form module produces. **(2) Live Connect probe (upgrade to full marks).** When Phase 4 HAS already run, additionally confirm via `4-connect/connect-opp-setup.md`'s `Sync Deliver Units enumerated:` line or a `connect_list_deliver_units` probe. **Do NOT return `unverifiable` / `partial` just because Phase 4 hasn't run** (ace#1010): this eval fires inside Phase 3, so both of the previously-named paths were structurally unavailable at invocation time and the dimension carried no information. The CCZ projection answers the real question — "will Connect find a unit?" — without Phase 4. |

   **Deduction rules:**
   - Any single dimension ≤3 → suite verdict `fail`.
   - **Inflation guard:** if ≥2 `[WARN]` `auto_surfaced` entries, overall capped at 8.5.
   - `[PLATFORM]` and `[DRIFT]` do NOT count toward the inflation guard.

   **Verdict tiers:**
   - `pass` — overall ≥ 7.0, no dimension ≤ 3, both apps released, CCZ clean.
   - `warn` — overall ≥ 5.0 < 7.0, or any inflation cap binds.
   - `fail` — overall < 5.0 OR any dimension ≤ 3.
   - `partial` — overall ≥ 7.0 but live MCP probes for Connect-side
     verification failed at grading time. **Phase 4 simply not having
     run yet is NOT a `partial`** — the `?latest=release` CCZ projection
     is a first-class scoring path (ace#1010).
   - `incomplete` — `3-commcare/app-release_summary.md` missing, or its
     frontmatter carrying no `apps.*` block. Nothing else earns this
     verdict (ace#1567).

   **Severity tiers** (mirror connect-program-setup-eval):
   - `[BLOCKER]` — must-fix before Phase 4 can proceed (e.g., one app unreleased).
   - `[WARN]` — should-fix; counts toward inflation guard.
   - `[PLATFORM]` — defect originates in CCHQ or Nova, not the skill
     (e.g., the CCZ-marker regex bug uses `<learn:` instead of xmlns
     attribute matching — that's a skill bug, see below; but a CCHQ
     5xx during release IS PLATFORM).
   - `[DRIFT]` — deployment-summary claim disagrees with live `apps/view`
     read. Diagnostic only.
   - `[INFO]` — observational.
   - `[INFO-SKIPPED]` — sub-check intentionally skipped.

4. **Special case — turmeric run_time_followups item 2 (CCZ regex
   bug).** Apps released cleanly on turmeric; the CCZ-marker check
   in app-release Step 6 falsely flagged "missing markers" because
   its regex looks for `<learn:` prefix while the actual XML uses
   `xmlns` attributes. The bug is in app-release (the skill that
   does the check), not in the build itself.
   - When running this eval and the CCZ check reports missing markers,
     ALSO read the build's actual XML (via the `build_id` in
     `3-commcare/app-release_summary.md` + the CCHQ build endpoint — NOT
     via `run_state.yaml`, which is not written yet; ace#1010) and verify
     whether markers are really missing. If markers are present in the XML but the CCZ check
     mis-reports them, surface as `[WARN] CCZ regex false-positive in
     app-release Step 6 — Observed: app-release reported 'no
     <learn:...> tag found' but xmlns inspection shows
     xmlns:vellum='http://commcarehq.org/xforms/vellum'. Likely cause
     (unverified): regex matches a literal '<learn:' prefix that
     CCHQ no longer emits.` Drop the CCZ-integrity dimension to ≤6
     ONLY if the markers are actually missing in the XML.

5. **Write the verdict YAML** to
   `3-commcare/app-release-eval_verdict.yaml` using the shape from
   `skills/_eval-template.md § Verdict YAML contract`. Dimensions:

   ```yaml
   dimensions:
     both_apps_released:        { weight: 0.35 }
     ccz_marker_integrity:      { weight: 0.25 }
     build_id_traceability:     { weight: 0.20 }
     deliver_units_enumerable:  { weight: 0.20 }
   ```

## Auto-surfaced concerns

Per `_eval-template.md § Auto-surfaced severity rules`, plus skill-
specific surfaces:
- `[WARN]` per CCZ regex false-positive that mis-flagged a clean build.
- `[PLATFORM]` per CCHQ 5xx, Nova upload-shape change, or CCZ format
  change requiring app-release update.
- `[DRIFT]` per deployment-summary ↔ live `apps/view/<app_id>` discrepancy.
- `[INFO]` per app whose released `version` > 1 (re-release scenario,
  worth noting in opp-eval).
- `[DRIFT]` when a LEGACY run's deploy summary still carries a `releases:`
  block that disagrees with `app-release_summary.md` (ace#1636). Its absence
  is normal on every run from 0.14.0 onward and is never reported.

## LLM-as-Judge Rubric

**Provisional calibration** — ships at provisional until 3 real releases
produce ground truth. Calibration target on a clean release:

- **Detection rate:** ≥ 80% of catalogued release issues from
  `eval-calibration/known-issues.md § App release` (TBD).
- **Inter-run variance:** ≤ 0.5 across 3 same-model runs.
- **Cross-model variance:** ≤ 1.0 for strong calibration.

The first 3 calibration runs should specifically include:
1. A clean dual-release (the canonical pass case).
2. A run where one app released but the other failed mid-release
   (drives the partial-release fail mode).
3. A run with a CCZ regex false-positive (drives the [WARN] tier).

## Archetypes

| Archetype | What this skill does |
|---|---|
| `atomic-visit` | Default. Two-app release (Learn + Deliver). |
| `focus-group` | Two-app release with FGD-form Deliver. Same shape. |
| `multi-stage` | One Learn + one Deliver per stage. Dimension scores aggregate per-stage. |

## MCP Tools Used

See `skills/_eval-template.md § MCP Tools Used (stock)` for the Drive
block. Plus:
- ace-connect MCP: `commcare_download_ccz` on the `?latest=release`
  projection — the first-class `deliver_units_enumerable` path.
- ace-connect MCP (only when Phase 4 has already run):
  `connect_list_deliver_units` to upgrade `deliver_units_enumerable` to
  full marks with a live Connect confirmation.
- CCHQ HTTP probe (no MCP yet): `GET /a/<domain>/apps/view/<app_id>/`
  to verify `is_released` against the `build_id` in
  `3-commcare/app-release_summary.md`.

## Known traps when grading a release

- **`last_released` reads `None` on a genuinely released build.** The
  ajax release path does not stamp that field, while `is_released` reads
  `True`. Do not use `last_released` as a release-recency signal or as
  evidence of a failed release.
- **`app-release-eval` and `app-release` share the same CCZ marker
  parser**, so a defect in that parser is invisible to both — there is no
  independent cross-check. When `ccz_marker_integrity` looks wrong,
  re-read the build XML directly (Step 4) rather than trusting either
  side's parse.
- **`eval-calibration/known-issues.md § App release` is still TBD**, so
  the ≥80% detection target below is currently *unmeasurable*. Treat the
  `fail` and `warn` tiers as asserted rather than validated, and add each
  graded release to the catalogue as it lands.

## Mode Behavior

See `skills/_eval-template.md § Mode Behavior (stock)`.

## Dry-Run Behavior

Per `skills/_eval-template.md § Dry-Run Behavior (stock)`, plus: skip
live CCHQ + Connect probes (read-only inputs OK; live probes treated
as effectful).

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-10-16 | **Graded in code: `lib/app-release-check.ts` via `scripts/fact-check-eval.ts app-release`.** Every dimension was a fact read off the owned summary and the `?latest=release` CCZ projection, so an Opus judge re-reading those payloads added minutes and variance and no judgment (ACE run-efficiency audit, 2026-10-16, three runs). The rubric text is unchanged and is now the spec the code implements; owned-artifact precedence (ace#1567), never-read-run_state (ace#1010) and units ≠ forms (ace#1331) are pinned in `test/lib/fact-check-evals.test.ts`. One tightening: any `[BLOCKER]` now forces `fail` — a weighted mean can no longer average away an unreleased app or a zero-unit Deliver CCZ. | ACE team |
| 2026-08-26 | **The `releases:` corroboration leg is gone with the block it read (ace#1636 — fourth instance of the ace#1010/#1439/#1567 class, and the one that retires the artifact).** ace#1567 demoted `app-deploy_summary.md`'s `releases:` block from a required leg to a corroborating one but did not check whether anything ELSE read it. `llo-launch § Step 4`'s app-verdict-freshness gate did — as a hard `[BLOCKER]` input — so on the 2 of 2 observed runs where `app-release` Step 7 was skipped, the Phase 9 launch gate either halted falsely or silently skipped the staleness check and let a stale deep app-UX verdict authorize a go-live. `llo-launch` now reads `3-commcare/app-release_summary.md`'s `apps.<app>.build_id`, the owned contract (ace#1439); `app-release` Step 7 is deleted (steps renumbered 8→7, 9→8; no external citation indexed above 6); and this rubric's corroborating leg goes with it, along with the `[WARN]` it emitted on every clean run. A legacy `releases:` block that disagrees is now a `[DRIFT]` note, never a deduction. *Enforced:* `test/skills/deploy-summary-owns-no-release-state.test.ts`. | ACE team |
| 2026-04-29 | Initial version. 4 dimensions: both_apps_released (0.35), ccz_marker_integrity (0.25), build_id_traceability (0.20), deliver_units_enumerable (0.20). Provisional calibration. Authored to absorb turmeric run_time_followups item 2 (CCZ regex false-positive in app-release Step 6) — the eval has an explicit step 4 to distinguish "regex bug" from "real missing markers." | ACE team (0.10.29) |
| 2026-08-23 | **The `incomplete` gate re-pointed at the owned artifact, and the precedence stated once (ace#1567 — third instance of the ace#1010/#1439 class).** Step 2 gated `verdict: incomplete` on `app-deploy_summary.md` having a `releases:` block. That file belongs to `app-deploy`; the block is a cross-reference `app-release` appends at its Step 7. On bednet-check-2-visit/20260820-0832 both apps were live-released (`is_released: true`, `version: 5`, confirmed against the HQ application API) and `app-release_summary.md` carried the full declared frontmatter — but Step 7 had not run, so a literal grader had to call a perfect release ungradable with the factually false message "skill did not run". In `opp-eval` that is worse than a deduction: `incomplete` counts as "not gradable" in the coverage cap, so the run got neither its pass nor the (minor, real) finding. Now: the gate keys on `3-commcare/app-release_summary.md` / its `apps.*` frontmatter; `both_apps_released` and `build_id_traceability` demote the `releases:` block from a required cross-check leg to a corroborating one (disagreeing = one 4-point traceability deduction, scored once, not in both dimensions; absent = one bounded `[WARN]`); and the precedence — **owned artifact anchors, everything else corroborates** — is stated at the top of `## Process` rather than re-derived per dimension. *Enforced:* `test/skills/eval-gate-artifact-ownership.test.ts`, which asserts the rule generically across every `-eval` whose producer declares a `## Products` contract. | ACE team |
| 2026-07-28 | **Two rubric dimensions re-pointed at gradable evidence (ace#1010).** (1) `build_id_traceability` graded `run_state.yaml`, which `app-release` explicitly does NOT write — the orchestrator does, at the Phase 3 boundary fence, AFTER the per-step evals run. A perfect release scored 6/10 on it every time: a fixed 0.8-point downward bias on every Phase 3 release eval. Now graded against `3-commcare/app-release_summary.md`, the artifact the skill actually owns, cross-checked against the `releases:` block. (2) `deliver_units_enumerable` was structurally un-verifiable at invocation — both its named paths needed Phase 4, and this eval runs inside Phase 3. The `?latest=release` CCZ projection (the literal artifact Sync Deliver Units consumes) is promoted to the first-class scoring path, with the live Connect probe as the upgrade to full marks; Phase 4 not having run is explicitly no longer a `partial`. Also recorded three grading traps: `last_released: None` on a released build, the shared marker parser with no independent cross-check, and the TBD known-issues catalogue that leaves the detection target unmeasurable. | ACE team |
