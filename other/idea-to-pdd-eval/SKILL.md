---
name: idea-to-pdd-eval
description: >
  Internal /ace:run step — Grade the run's PDD against its source material.
user-invocable: false
disable-model-invocation: false
---

# Idea-to-PDD Eval

The `idea-to-pdd` skill self-evaluates with a 5-question rubric and
ships a stress-test grade in the PDD itself. That self-eval has two
known weaknesses: (a) the same model that wrote the PDD also grades
it (over-generosity bias), and (b) the PDD checks itself against the
rubric but not against the source idea — so a PDD that addressed the
intervention but missed reviewer comments from the source pack can
still self-grade 5/5 if the rubric doesn't ask "did you address every
reviewer concern?"

This skill is the independent grader. It re-runs the stress test from
outside, cross-checks against the source idea, and surfaces
inconsistencies the self-eval missed.

Cross-artifact eval — see `skills/_eval-template.md` for shared
contracts (verdict YAML shape, severity rules, inflation guard,
stock blocks). See `skills/eval-calibration/SKILL.md` for the
calibration methodology.

## Inputs

Pipeline-only: grades a run's PDD against its idea pack, which exists only in a run.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 source | `inputs-manifest.yaml` + each `file_id` in it | source idea pack (the full pack is what the PDD is graded against) |
| Phase 1 producer | `1-design/idea-to-pdd.md` | the PDD under judgment |
| Phase 1 producer | `decisions.yaml` (per-run decisions log) | `source_conflict_honesty` dimension — checks whether genuine source conflicts were tagged `evidence_basis: conflicting` with concrete `conflict_signals`, or silently resolved |

## Products

- `1-design/idea-to-pdd-eval_verdict.yaml` — verdict YAML per `_eval-template.md § Verdict YAML contract`

Note: the verdict filename uses `idea-to-pdd-eval` (this skill's name)
not `idea-to-pdd` (the producer) — see `_eval-template.md` for the
filename rule.

## Process

1. **Use inputs already in context (preferred) or read from Drive.**
   When invoked from the `idea-to-design` subagent (the common
   `/ace:run` path), all inputs below are already loaded by the
   parent — do NOT re-issue `drive_read_file`. See
   `agents/idea-to-design.md` § Performance conventions: the parent
   subagent reads the source material in Step 1 and the PDD lands in
   context via Step 1's producer call; both are then trusted across
   all downstream steps. Re-reading wastes ~5–10s per file. Only
   re-read when invoked standalone (e.g. `/ace:step idea-to-pdd-eval
   <opp>/<run-id>`) where the parent context isn't pre-warmed.

   The inputs this skill reasons about (location for standalone reads):
   - Source material — the "source idea pack":
     - `ACE/<opp-name>/runs/<run-id>/inputs-manifest.yaml`, then each
       `file_id` it lists (the orchestrator's frozen evidence-pack
       pointer-set, captured at run start)
   - PDD (the artifact under judgment): `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md`
   - Decisions log: `ACE/<opp-name>/runs/<run-id>/decisions.yaml` (the
     per-run decisions log `idea-to-pdd` wrote; used by the
     `source_conflict_honesty` dimension).
   The "source idea" referenced throughout the rest of this skill is
   the union of the manifest's contents, treated as one synthesized
   seed.

1b. **Run the published-render gate before grading anything:** `scripts/check-published-doc-render.ts <published Doc URL>` — see `skills/_eval-template.md § Published-render gate (stock)`. A non-zero exit (raw markdown on the page, or a doc an anonymous reader cannot open) makes this eval's verdict `fail`, whatever the prose would score (ace#2213). Write the Doc URL you checked to the verdict as top-level `published_url`, and the result as `published_render` — `capture_path` keeps naming the run-folder source, so the verdict records both what was composed and what a reader opened.

   **On a confidential opp (ace#3191) the anonymous read fails by design** — the producer deliberately did not link-share the doc (`inputs/confidentiality.yaml` exists; `lib/opp-confidentiality.ts`). Do not fail the eval for that, and do not share the doc to make it pass. Read the doc with ACE's credentials (`drive_read_file`, default `text/plain`), save it and the opp's `confidentiality.yaml` locally, and run the gate in confidential mode: `scripts/check-published-doc-render.ts <Doc URL> --confidential <confidentiality.yaml> --text <export>`. It still fails on raw markdown, and refuses (exit 2) on an opp with no confidentiality file. Record `published_render.anonymous_access: not-applicable (confidential opp)`.

2. **Extract the source idea's reviewer-comment list.** Source-idea
   bodies (any file in the manifest) generally include footnoted or
   sectioned reviewer comments (e.g. "[a] FLW safety risks…",
   "[b] vendor consent…"). Build a structured list across all source
   files.

   **Clean-source detection (added 0.10.9):** if the entire source
   pack contains zero reviewer comments — no `[a]/[b]` footnotes, no
   "Reviewer Comments" / "Comments" / "Feedback" section in any of
   the manifest entries — set `clean_source = true` and skip step 3.
   The reviewer-comment-fidelity dimension will switch to the
   deferred-decision-discipline branch (see § Dimension below).
   Surfaced 0.9.11 cross-opp validation:
   `turmeric-dogfood-20260427`'s source idea was clean PM-authored
   with no review pass; the rubric's anchors at 9.5 ("all comments
   addressed") were a poor fit because there were no comments to
   address.

3. **Extract the PDD's promised dispositions** (skip if
   `clean_source = true`). PDDs include a "Reviewer Comments —
   Disposition" table mapping each comment to how the PDD addressed
   it. Build the matching list.

4. **Grade across 9 dimensions.** Each dimension is 0–10. Overall
   score is the weighted mean.

   Per the QA/Eval split principle (PR #146), this rubric is **quality-only**. Structural correctness (sections present, weights sum, archetype valid in enum, etc.) is now checked by `idea-to-pdd-qa` and gates this eval — if QA failed irrecoverably, this skill emits `verdict: incomplete` without grading. Quality dimensions: 5 doc/fidelity (40% weight) + 4 program viability (60% weight).

   | Dimension | Weight | Criteria |
   |---|---|---|
   | **Reviewer-comment fidelity** | 10% | **Two branches by source type.** If `clean_source = false` (the source pack contains reviewer comments): every reviewer comment must have a concrete disposition in the PDD (addressed via §X / scoped out / out-of-scope-for-this-opp). **Scoring anchors (tightened 0.9.4):** all comments addressed with concrete section citation = **9.5**; addressed plus one comment that's "addressed via § X" where § X is mentioned but light = **9.0**; one comment missing disposition = **7.5**; ≥2 missing = **5.0**; one false-disposition claim ("addressed via § X" but X doesn't exist) = **4.0** (3-point deduction floor); ≥2 false claims = **fail (≤3)**. ── **READ THE CITED SECTION; do not grade the disposition table (added 2026-08-14, ace#1210).** The table is the PDD's own self-attestation — grading it is reading the defendant's testimony. For EVERY comment: (a) the row must cite a specific section, (b) open that section and verify it actually implements the comment, and (c) a comment swept into a summary row such as "enforced by the build skills" gets **no credit** — a fix shipping in a skill does not prove THIS PDD's spec conforms, which is precisely the assumption that failed. **Anchor:** a comment whose disposition cannot be verified against a cited section scores no better than **partial** (≤7.5) regardless of what the table asserts; a disposition CONTRADICTED by the cited section is a false claim (see above), not a partial. Live miss (`measured_on: 2026-08-13`; that run's PDD is a live, mutable Drive doc — re-read it before treating this as a regression gate): `hh-poverty-targeting/20260812-2034` scored **9.5** while §6.1 asked `visit_outcome` on screen 2 and recoded it on screen 6 — ace#979 reintroduced against binding comment [d], which had supplied the correction verbatim. The four comments dispositioned as explicit decisions were genuinely honoured and each cited a verifiable section; the failure was confined to the swept bucket. `idea-to-pdd-qa` (structural) cannot see this, and `skills/feedback-ledger` renders the same claim into the reviewer's "where did my comment go?" view — so a false claim propagates to the reviewer twice. (QA verifies the table EXISTS with rows when reviewer comments are referenced; this dimension grades whether each disposition is *concrete*, not whether the table is populated.) ── **Clean-source branch (added 0.10.9, when `clean_source = true`):** the dimension grades **deferred-decision discipline** instead. Anchors: every deferred decision is concrete (named question, named owner phase, named resolution mechanism) = **9.5**; section present, decisions concrete but owner phase implicit = **8.5**; section present but decisions vague ("TBD per LLO" with no question) = **7.0**; section absent AND PDD silently spec'd things that should have been deferred to LLO discovery = **5.0**; section claims to defer something that should have been Phase-1-speccable = **4.0**. |
   | **Archetype coherence** | 10% | The spec must follow the declared archetype's pattern *in spirit*: `atomic-visit` shouldn't introduce inter-visit stages or multi-visit case lifecycles; `longitudinal-visits` should carry an `Entity Lifecycle` section and a longitudinal clause under Evidence Model Layer A; `focus-group` shouldn't have a single-vendor-style Deliver form; `multi-stage` should have a Stage Gate section between stages. Pattern violations are 2-point deductions per violation. (QA verifies the archetype is *declared and in the valid enum*; this dimension grades whether the structure *matches* the declared archetype.) |
   | **Numbers consistent** | 10% | Cross-section numerical agreement (semantic — the *meaning* of the numbers, not just regex same-value-twice). **Severity-tiered deductions:** load-bearing inconsistencies that change downstream behavior (LLO recruiting filter, FLW certification gates, payment thresholds) are **2-point deductions** per occurrence. Doc-level inconsistencies (different number presentations of the same value, ordering differences) are **0.5-point deductions**. Default tier is 1.0 (mid). |
   | **Feasibility of headline metrics** | 8% | Each Primary success metric must be measurable today, not aspirational. Specifically: the PDD's Layer B verification claims must reference concrete checks (file-format validations, deterministic field rules), not future capabilities (e.g. "AI-assisted photo content check" without naming the model, threshold, or expected pass rate). 1.5-point deduction per metric that depends on unspeccable Layer B. ── **Mechanisms a PDD must not assert (added 2026-08-13, ace#1213; corrected same day).** Scope extends beyond Primary metrics to the **Evidence Model and the Learn/Deliver App Specifications**, because that is where enforcement claims actually live. Read `skills/_app-component-library.md § Mechanisms a PDD must not assert` — **both tables** — and check every mechanism the PDD asserts against them. A listed mechanism **asserted as enforced or delivered** — Connect-side GPS accuracy enforcement, an elapsed-time floor derived from bare `now()`, a randomized or per-attempt assessment item draw — is a **2-point deduction each** and a `[BLOCKER]`. The same mechanism stated honestly as its buildable approximation with the residual named (per `idea-to-pdd § Step 4a`), or deferred as an open question, takes **no deduction** — that is the correct behaviour, not a hedge. **Hard-gate:** ≥2 listed mechanisms asserted as enforced → dimension **≤3 → suite `fail`**. Judge the *assertion*, not the vocabulary: "the app rejects fixes worse than 50 m", "cannot be submitted in under 6 minutes", and "a fresh item draw each attempt" are assertions of enforcement however they are phrased. **Symmetric check — a PDD may also be wrong in the other direction.** A PDD asserting that a **Table B** mechanism is *impossible* or *platform-limited* (rather than "not built this cycle") is a **1-point deduction** and an `[INFO]`: a false platform constraint in a Work Order outlives the constraint and forecloses a capability request. Do not reward over-claiming a limit any more than over-claiming a control. |
   | **Source-conflict honesty** | 8% | The independent grader's highest-value check on Phase-1 *authoring integrity*: did the run honestly flag where the source material was ambiguous or self-contradictory, rather than silently resolving it? **Independently scan the source pack** for material disagreements — two inputs, or two parts of one input, that imply different load-bearing answers (e.g. the ITN source describing **one** visit instrument while separately stating households are **"visited twice"**). For each genuine conflict, the run's `decisions.yaml` must carry a row with `evidence_basis: conflicting` and ≥ 2 concrete `conflict_signals` naming the competing readings — OR the PDD body must explicitly flag the conflict and its resolution. **Anchors:** every material source conflict flagged (conflicting row with concrete signals, or explicit PDD callout) = **9.5**; conflicts flagged but signals thin / one-sided / missing a citation = **8.0**; a default that clearly extrapolates beyond the source is tagged `stated` rather than `inferred` (over-claims grounding) = **6.0**; **one** genuine source conflict silently resolved — no `conflicting` row, no PDD callout, presented as a confident default (the ITN visit-cadence failure mode) = **4.0**; ≥ 2 silent conflict resolutions = **fail (≤ 3)**. **Directed sub-check — reconcile the payment unit against the entity grain BEFORE scoring (added 2026-08-15, ace#1420).** State the reconciliation explicitly in the notes. A PDD whose `payment_rate_unit` is FINER than its `entity_id_grain` has an unflagged conflict regardless of what else the scan found — Connect resolves payable units by `entity_id`, so a per-visit rate against a grain keyed on a date means several same-day events by one worker collapse into ONE payment entity, and every money number in the PDD, the Work Order and the Phase 4 payment unit is wrong by that multiple. Treat an unflagged instance as **one genuine source conflict silently resolved (4.0)**. This is named rather than left to the open-ended scan because the open-ended scan is exactly what failed: on `bednet-check-2-visit/20260814-2019` this dimension scored **9.5** with an explicit assertion of "exactly one material self-contradiction" — the scan found the conflict the rubric's own worked example had primed for and missed the one that sets the programme's economics. `idea-to-pdd-qa`'s `payment_unit_matches_entity_grain` now catches the mechanical case; this covers the cases prose states without filling the parameters table. **N/A branch:** if the source pack contains no material conflicts, score **9.0** (neutral — no penalty, no inflation) and emit the INFO below. (Legacy pre-v4 `decisions.yaml` without `evidence_basis` fields: grade on the PDD-callout branch only, and emit an INFO that the decisions log predates the evidence-basis contract.) |
   | **Demand reality** | 22% | (Increased from 20% in 0.13.88 after redistributing the removed `structural_completeness` weight to viability.) Is there a NAMED downstream consumer of the PDD's output, with a documented commitment to act on it? **Anchors:** named entity (regulator, lab, partner org) WITH explicit pre-committed action ("output X triggers test/policy step Y by entity Z by date D") = **9.5**; named entity WITH implicit/scoped commitment = **8.0**; passive references to "analysts" / "downstream consumers" / "lab testing" without a named entity = **6.0**; no named consumer; data collection in search of a buyer = **4.0**; data collection with explicit "future use TBD" = **2.0**. A PDD can be structurally complete and internally consistent while producing an orphan dataset; this dimension catches that. |
   | **Resource realism** | 17% | (Increased from 15% in 0.13.88.) Does the budget cover the implied labor + overhead at recruitment-realistic rates in the named geography? Walk through: budget ÷ visits = per-visit gross; subtract LLO management overhead (typically 25–40%), analyst review costs, AI inference costs, FLW transport/airtime; arrive at per-FLW daily rate. Compare to local market floor for the named region. **Anchors:** per-FLW daily rate clears local market floor with ≥30% buffer = **9.0**; clears the floor with little buffer = **7.0**; below local market floor — LLO must subsidize silently or FLWs churn = **5.0**; budget doesn't cover named work even at minimum rates = **3.0**; budget appears intentionally fictional / placeholder = **1.0**. |
   | **Mission alignment** | 12% | (Increased from 10% in 0.13.88.) Does each Primary metric measure the program's stated goal, or an upstream proxy? **Anchors:** every Primary metric directly measures the program's stated outcome = **9.0**; Primary metrics measure proximate proxies but the inferential chain is documented = **7.0**; ≥1 Primary metric measures something the program *does* (process metric: "form submitted, photo present") rather than what the program is trying to *learn* (outcome metric: "adulteration detected") = **5.0**; ≥1 Primary metric is structurally disconnected from the stated mission = **3.0**. The chain "Primary metric passes → mission outcome achieved" must hold without unstated steps. |
   | **Fallback validates primary** | 9% | (Increased from 5% in 0.13.88.) When the PDD names a fallback for a primary verification mechanism (typically Layer B AI checks), does the fallback function as a TRUE validation harness or as a parallel sampling alternative? **Anchors:** fallback is a stratified sample of primary's output (positive + negative cases reviewed, computes confusion-matrix metrics validating per-decision accuracy) = **9.0**; uniform sample of primary's output (validates aggregate not per-class) = **7.0**; random N% of submissions independent of primary's classifications (parallel sampling, not validation) = **5.0**; no fallback OR re-implements primary without independent ground truth = **2.0**. |

   **Deduction rules:**
   - Any single dimension ≤3 → suite verdict `fail`, regardless of
     overall mean.
   - **Inflation guard (raised 7.5 → 8.0 in 0.9.4):** if PDD
     self-eval is 5/5 and this rubric's overall is ≤8.0, that's a
     calibration signal that the `idea-to-pdd` self-eval rubric is
     loose. Cap overall at 8.0 and surface `[WARN]` recommending
     tightening `skills/idea-to-pdd/SKILL.md § LLM-as-Judge Rubric`
     next iteration. The threshold was raised because the 0.9.2
     calibration produced overalls of 8.48–8.52 against a PDD that
     self-graded 5/5 — the original 7.5 threshold was non-binding.
     8.0 is the new threshold; if a PDD self-grades 5/5 and this
     rubric scores 8.1+, no inflation. 8.0 or below = inflation
     signal binds.
   - **Pre-cap and post-cap reporting (added 0.9.4, mirrors OCS
     and Learn rubrics):** verdict YAML's `overall_score` is
     post-cap; sibling `overall_score_pre_cap` is the raw
     weighted mean.

5. **Write the verdict YAML** to
   `1-design/idea-to-pdd-eval_verdict.yaml` using the shape defined in
   `skills/_eval-template.md § Verdict YAML contract`. Dimensions for
   this rubric (sum to 1.0):

   ```yaml
   dimensions:
     # Document quality + fidelity (40%) — quality-only after 0.13.88;
     # structural completeness moved to idea-to-pdd-qa. 5 dims × 0.08 = 0.40
     # after source_conflict_honesty was added (v4 evidence-basis contract).
     reviewer_comment_fidelity:    { weight: 0.08 }
     archetype_coherence:          { weight: 0.08 }
     numbers_consistent:           { weight: 0.08 }
     feasibility_headline_metrics: { weight: 0.08 }
     source_conflict_honesty:      { weight: 0.08 }
     # Program viability (60%, redistribution of removed structural weight)
     demand_reality:               { weight: 0.22 }
     resource_realism:             { weight: 0.17 }
     mission_alignment:            { weight: 0.12 }
     fallback_validates_primary:   { weight: 0.09 }
   ```

5b. **Fixture opps: `demand_reality` is scored and reported, but does NOT
   gate (dimagi-internal/ace#2128).**

   Call `classifyViabilityGrading({ oppRootNames })` from
   `lib/viability-grading.ts` — the same shape as ace#1487's fixture branch
   (since retired with the ledger it bounded), and the source of truth if this prose ever
   disagrees with it. When the opp root carries `iterate-state.yaml` it
   returns `mode: 'fixture-adjusted'` and `excludedFromGate:
   ['demand_reality']`.

   In that mode:

   - **Still score `demand_reality`, still write it into `dimensions:` and
     `per_item:` with its note.** It is excluded from the mean, not from the
     verdict — a fixture brief that genuinely regressed on demand framing must
     still be visible.
   - Emit BOTH numbers: `overall_score` (gating, renormalized over the
     remaining eight weights via `renormalizeWeights` — proportional, so the
     surviving ratios are preserved) and `overall_score_all_dimensions` (the
     raw nine-dimension mean). `computeViabilityScores` returns both. **Call it
     with ONE named object — never three positional args:**

     ```ts
     computeViabilityScores({ scores, weights, decision })
     ```

     `scores` are the 0–10 judge scores; `weights` are the rubric weights above
     and **must sum to 1.0**. Do not hand-compute either number instead — the
     helper is the source of truth for the arithmetic.

     **Do not swap `scores` and `weights` (dimagi-internal/ace#2162).** They are
     the same TypeScript type, so nothing upstream of the helper can catch it.
     A swap used to return `overall_score_all_dimensions` **exactly right**
     (multiplication commutes) beside a garbage `overall_score` — measured
     6.62/6.62 with the gate moving 7.36 → 0.09, i.e. across the 7.0 gate,
     which would have shipped a plausible-looking verdict whose two numbers
     silently disagreed. The named object plus a weight-sum assertion now make
     that throw rather than score; if you see `weights must sum to 1.0`, you
     transposed the two. *Enforced:* `test/lib/viability-grading.test.ts`.
   - Record `viability_grading: { mode, excluded_from_gate, reason }` in the
     verdict so the adjustment is auditable rather than silent.

   **Why this exists — the dimension was BIMODAL, not merely harsh.** On a
   fixture there is never a named downstream consumer of the *data*, and
   `no-inferred-backstory` forbids inventing one, so the artifact cannot move
   the score. But the rubric never said whether the `/ace:iterate` campaign
   itself counts as the consumer, and judges split on it. Two runs of
   `bednet-check-2-visit` twelve hours apart, on a byte-identical rubric row:

   | Run | Score | Judge's reading |
   |---|---|---|
   | `20260814-0856` | **8.5** | "A named consumer with a documented, pre-committed action does exist and is sourced, not invented: ACE's /ace:iterate campaign… Honesty is credited here, not penalised." |
   | `20260814-2019` | **4.0** | "The source names a consumer of the FIXTURE… but none of the data… **Not softened for a fixture: the rubric has no fixture branch.**" |

   A 4.5-point swing at weight 0.22 is 0.99 of composite — wider than the
   margin between every pass and fail this opp has recorded (its verdicts run
   6.96–8.89). So the dimension was contributing noise, not signal, to 22% of
   the gate **on the opp that IS the `/ace:iterate` regression baseline** — a
   permanently-unstable eval there cannot detect the regression it exists to
   detect. The second judge named this gap in its own verdict on 2026-08-14;
   it went unread for three weeks.

   **The exclusion is `demand_reality` ONLY.** `resource_realism` still gates
   on a fixture: it is not structurally constant, and on `20260906-2228` it
   scored 5.0 and caught a real defect (a worker-day payment grain at
   `daily_cap: 1` paying USD 0.31–0.75 per completed visit). Excluding the
   whole viability axis would discard exactly the finding that made this worth
   fixing. *Enforced:* `test/lib/viability-grading.test.ts`.

6. **Auto-surfaced concerns.** Severity rules per
   `skills/_eval-template.md § Auto-surfaced severity rules`. Skill-
   specific surfaces beyond the standard contract:
   - `[WARN]` for each reviewer comment without a concrete
     disposition or with a false disposition claim (only when
     `clean_source = false`).
   - `[WARN]` for each cross-section numerical inconsistency.
   - `[BLOCKER]` for each mechanism on
     `_app-component-library.md § Mechanisms a PDD must not assert` that the PDD
     asserts as **enforced**. Name the mechanism, quote the asserting
     sentence, and state the sanctioned alternative from the list — the
     operator needs to fix the PDD before it reaches the Work Order and the
     training materials, which is the whole cost of this class (ace#1213).
   - `[WARN]` for each material source conflict the run resolved
     silently — no `evidence_basis: conflicting` row in `decisions.yaml`
     and no explicit PDD callout. Name the competing source readings the
     grader found, so the operator can add the missing `conflicting` row.
   - `[INFO]` `no material source conflicts found in the source pack;
     source_conflict_honesty scored 9.0 (N/A neutral)` (when the source
     pack is internally consistent).
   - `[INFO]` `decisions.yaml predates the v4 evidence-basis contract;
     source_conflict_honesty graded on PDD-callout evidence only` (when
     the log has no `evidence_basis` fields).
   - `[INFO]` for each reviewer comment scoped out without rationale
     (PDD says "out of scope" but the idea reviewer flagged it as
     critical).
   - `[INFO]` `clean-source branch active: graded on deferred-decision
     discipline` (when `clean_source = true` — auditability for
     why the dimension scored on a different rubric than usual).
   - `[INFO]` if PDD's self-eval and this rubric's overall differ by
     ≥ 1.5 points — signal that the `idea-to-pdd` self-eval rubric
     needs tightening.

## LLM-as-Judge Rubric

`measured_on: 2026-04-28`. The cited PDD is a **live, mutable** Drive
document in a run folder — re-read it before treating these targets as a
regression gate rather than assuming the numbers still reproduce
(`eval-calibration § Step 3c`).

This rubric's calibration target on the smoke-20260428-1242 PDD:

- **Detection rate:** ≥ 80% of catalogued PDD issues from
  `eval-calibration/known-issues.md § PDD`.
- **Inter-run variance:** ≤ 0.5 across 3 same-model runs.
- **Agreement with self-eval:** within ±1.5 points of the PDD's
  own stress-test grade. Larger gap is itself a calibration signal
  for the upstream `idea-to-pdd` rubric.

## Archetypes

| Archetype | What this skill does |
|---|---|
| `atomic-visit` | Default. Grades the PDD's atomic-visit specification against the source idea. |
| `longitudinal-visits` | Adds a "longitudinal Layer A" sub-check under archetype_coherence, guarding the ace#1462 degradation (`spark-facilitator/20260813-2126`), where a PDD stays longitudinal-aware in prose while the payment predicate quietly becomes "any visit counts". Verify BOTH halves the archetype mandates (`idea-to-pdd § Archetypes → longitudinal-visits`): (a) an **Entity Lifecycle** section naming the followed entity, its states/phases, the expected visit sequence and cadence, and what completion means; and (b) an explicit **longitudinal clause under Evidence Model Layer A** stating which case facts the payment predicate reads and the resulting `entity_id`. A Layer A that reads only the current form's fields — or an `entity_id` left at an `atomic-visit`-style cross-sectional key such as `concat(username, today())` rather than entity + sequence position — IS the degradation, not a thin spec: score it as a pattern violation (2-point deduction each), because the PDD's prose will read correct while the money predicate does not. Also check the payability-against-history questions are answered rather than silent (same activity twice, out-of-order visits, per-entity cap, visit ownership); silence on payability is the specific input that produces the degradation. **Cap enforcement (ace#2512):** a per-entity cap or "repeat not payable" rule whose only stated enforcement is the `entity_id` key ("Connect pays each key once", "collapses to a single payment", "enforced by de-duplication") is a 2-point pattern violation — Connect pays a repeated key again with the `duplicate` flag off, which is always on ACE opportunities (`playbook/integrations/connect-api.md § A repeated entity_id is PAID AGAIN`). The cap must name a Connect-side stop (a computed `payable_slot` field + `form_field_rules` row, or `max_daily` / `max_total`). Also deduct when non-payable record kinds share the paid deliver unit while `max_total` is sized for payable units only: they consume the cap. |
| `focus-group` | Adds a "facilitation craft" sub-check under archetype_coherence (does the PDD specify probing techniques, neutral framing, group dynamics — not just question lists?). |
| `multi-stage` | Adds a "stage gate" sub-check under archetype_coherence (every stage transition has explicit go/no-go criteria). |

## MCP Tools Used

See `skills/_eval-template.md § MCP Tools Used (stock)`.

## Mode Behavior

See `skills/_eval-template.md § Mode Behavior (stock)`.

## Dry-Run Behavior

See `skills/_eval-template.md § Dry-Run Behavior (stock)`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-08-20 | **`archetype_coherence` gains its `longitudinal-visits` branch (ace#1541).** The archetype shipped 2026-08-17 but § Archetypes still enumerated the old three, so the 8%/10%-weighted coherence dimension had no sub-check for it — including no check on the very thing the archetype exists to prevent: a PDD whose prose stays longitudinal-aware while Layer A silently degrades to "any visit counts" (ace#1462). Added the row (Entity Lifecycle section + Layer A longitudinal clause + `entity_id` grain + payability-against-history), and named the archetype in the dimension row alongside its siblings. *Enforced:* this file is now in the guarded list in `test/skills/archetype-enum-drift.test.ts`, so the next archetype fails CI until this rubric catches up. | ACE team |
| 2026-08-13 | **`feasibility_headline_metrics` gains the known-unbuildable check — the gate that was missing (ace#1213).** This rubric scored `spark-facilitator/20260812-1635`'s PDD **7.97 `pass`** while its central assessment mechanism (12 items drawn per attempt from a bank of 30, fresh draw each retake) was fiction; the dimension that exists to catch over-claimed mechanisms flagged an SM-1 metric but not this, because its scope was Primary metrics and Layer B while enforcement claims actually live in the **Evidence Model and the App Specifications**. Scope extended there, with a check against `_app-component-library.md § Known-unbuildable mechanisms`: a listed mechanism asserted as ENFORCED is a 2-point deduction and a `[BLOCKER]`, hard-gating the dimension <=3 (suite `fail`) at >=2. The same mechanism stated as its buildable approximation with the residual named, or deferred as an open question, takes no deduction — that is the correct behaviour, not a hedge. Judges the assertion rather than the vocabulary. An eval check is needed in addition to Phase 3's build-time deviation because the build catching it is too late for the artifacts: on this run the PDD, Work Order and training materials were all authored from the unbuildable spec, and on ace#995 the same pattern put a dead fraud control into the Connect opportunity itself. | ACE team |
| 2026-08-13 | **Dated the calibration target (ace#1212).** The `smoke-20260428-1242` PDD the detection-rate and variance targets are calibrated against is a live, mutable Drive document, cited with no measurement date. Added `measured_on: 2026-04-28` plus a mutability notice directing a re-read before the targets are used as a regression gate. Per `eval-calibration § Step 3c`. *Enforced:* `test/skills/eval-calibration-anchors.test.ts`. | ACE team |
| 2026-05-29 | **Added `source_conflict_honesty` dimension (8%) for the v4 evidence-basis contract.** The independent grader now checks Phase-1 authoring integrity: it independently scans the source pack for material disagreements and verifies the run's `decisions.yaml` flagged each via `evidence_basis: conflicting` + ≥ 2 `conflict_signals` (or an explicit PDD callout) rather than silently resolving it. Motivated by the ITN run (`malaria-itn-app/20260528-1607`), where the source described one visit instrument but separately said households are "visited twice" — ACE silently built two distinct forms and the eval still scored 9.6 because no dimension graded conflict honesty. Weight carved from the doc/fidelity bucket: the four existing doc/fidelity dims drop 0.10 → 0.08 each; new dim 0.08; doc/fidelity stays 40%, viability unchanged at 60%. Adds `decisions.yaml` as an input. N/A-neutral (9.0) when the source pack has no conflicts; PDD-callout-only branch + INFO when the log predates v4. | ACE team |
| 2026-05-08 | **Rubric cleanup: 11 → 10 dimensions; weight-sum bug fix; viability rebalanced to 50%.** Three fixes in one edit: (1) Removed `stress_test_agreement` (10%) — it was structurally tautological (same model applies same rubric twice; cross-model probe confirmed it doesn't discriminate, scoring 8-10 on every grade with variance from rubric ambiguity not from real artifact differences). (2) Folded `numbers_present` (5%) into `numbers_consistent` (10%) since they cover the same axis and `numbers_present` was already a soft check most PDDs trivially pass. (3) Fixed the 0.13.81 weight-sum bug: weights summed to 0.95 not 1.0. New weights cleanly total 1.00 with viability at 50%: `demand_reality` 15→20%, `resource_realism` 10→15%, `mission_alignment` 5→10%, `fallback_validates_primary` held at 5%, `feasibility_headline_metrics` 5→10%. Verification (independent re-grade on turmeric PDD with the new 11-dim rubric scored 7.55 vs old rubric's 8.65 — confirming the viability axis discriminates). | ACE team (0.13.84) |
| 2026-05-08 | **QA/Eval split: removed `structural_completeness` (10%) — now lives in new `idea-to-pdd-qa` skill.** First migration of the QA/Eval split principle (PR #146). Structural completeness was a static check (regex over `## Heading` lines for the 11 required sections); moved to `skills/idea-to-pdd-qa/checks.ts` as `checkAllRequiredSectionsPresent`. The eval rubric is now quality-only: 4 doc/fidelity dimensions (40%) + 5 viability dimensions (60%). Removed weight (10%) was redistributed to viability dimensions: `demand_reality` 20→22%, `resource_realism` 15→17%, `mission_alignment` 10→12%, `fallback_validates_primary` 5→9%. QA gates eval — eval is skipped (`verdict: incomplete`) if QA fails irrecoverably. Updated dimension descriptions to clarify which structural concerns moved to QA (annotated inline). | ACE team (0.13.88) |
| 2026-05-22 | **Retire `idea.md` references.** The optional `idea.md` operator-seed input was removed from `idea-to-pdd`; this rubric loses its dual-input language. `clean_source` detection mechanism is unchanged (still keys off reviewer-comment presence across the source pack); language switched from "idea.md" to "the source pack" throughout. No scoring or weighting change. | ACE team |
