---
name: llo-launch-eval
description: >
  Internal /ace:run step — Grade a run's go-live against the PDD launch preconditions.
user-invocable: false
disable-model-invocation: false
---

# LLO Launch Eval

`llo-launch` is the Phase 6 skill that activates an ACE
opportunity for live FLW use. It's the production gate: any defect that
slips past it ships to real LLOs and FLWs in the field. This rubric
grades whether the activation was faithful to the PDD's launch
preconditions, with the same explicit-deduction discipline as the
other 4 strongly-calibrated rubrics in the eval framework.

This is the most load-bearing of the operate-category rubrics. See
`skills/eval-calibration/SKILL.md` for the methodology and
`docs/eval-calibration-learnings.md` for patterns observed building
the first 4 strongly-calibrated rubrics.

## Inputs

Pipeline-only: grades a run's go-live record, which exists only in a run. Its inputs are listed in § Process.

## Process

1. **Read inputs from GDrive:**
   - PDD: `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md`
   - `runs/<run-id>/9-execution-manager/llo-launch_record.md` — the
     activation record
   - `runs/<run-id>/9-execution-manager/llo-uat_results.md` — UAT
     sign-offs the launch should have verified
   - `runs/<run-id>/3-commcare/app-deploy_summary.md` — app-publish
     status the launch verified
   - `runs/<run-id>/run_state.yaml` — phase states
     (`phases.execution-management.steps.llo-launch`,
     `phases.execution-management.steps.llo-invite`).
     (Pre-0.13.116 these were `gates.llo-launch` / `gates.llo-invite`;
     gates removed — `phases.<phase>.steps.<skill>.status` carries
     the same signal.)

2. **Detect "phase not run" mode.** If `run_state.yaml` shows
   `phases.execution-management.llo-launch` not `done` or the launch
   artifact is missing, emit `verdict: incomplete` immediately with
   `[INFO] Phase 6 llo-launch not run; not gradable yet`.

3. **Grade across 9 dimensions.** Each dimension is 0–10. Overall
   score is the weighted mean.

   Five **launch-correctness** dimensions (60% weight, was 100% before 0.13.84) verify the launch fired technically correctly: UAT signed off, Connect activated, apps published, notifications correct, gates respected. Four **launch-time viability** dimensions (40% weight, added 0.13.84) verify the program is actually viable AT THE LAUNCH MOMENT — different from Phase 1's design-time viability check (`idea-to-pdd-eval`). The Phase 1 PDD might have correctly named a downstream consumer; at launch we re-verify the consumer is still ready. Same axis as `idea-to-pdd-eval`'s viability dimensions, different specifics calibrated to the launch artifact.

   | Dimension | Weight | Criteria |
   |---|---|---|
   | **UAT sign-off completeness** | 15% | (Reduced from 25% in 0.13.84.) Every UAT participant from `llo-uat`'s sign-off list must have signed off (or have a documented blocker). Missing sign-offs = 3-point deduction per missing LLO. **Hard block:** a launch that fired with ≥1 LLO who explicitly did NOT sign off (vs simply pending) is a fail (≤3) — the producing skill missed a real veto. |
   | **Connect activation correctness** | 15% | (Reduced from 25% in 0.13.84.) Connect Opportunity status must transition from `draft` to `active`. Verification rules and payment units configured by Phase 4 must still match the PDD spec at activation time (no silent drift between Phase 4 and Phase 6). Missing activation transition = fail (≤3). Drift between Phase 4 and Phase 6 config = 2-point deduction per drift. |
   | **App-publish status** | 10% | (Reduced from 20% in 0.13.84.) Both Learn and Deliver apps must be published (not draft) on the configured HQ project space. App-publish status is read from `3-commcare/app-deploy_summary.md` and confirmed via Nova MCP at launch. Either app still in draft = fail (≤3). |
   | **Go-live notification fidelity** | 10% | (Reduced from 15% in 0.13.84.) The go-live notification email to LLOs must include: app links, calibration-gate threshold reminder (10/12 for atomic-visit calibrated rubrics), safety-plan summary if applicable, support-channel contact (`ace@dimagi-ai.com`). Missing required content = 1-point deduction per gap. **Factual error rule (mirrors OCS rubric 0.9.4):** wrong contact email, wrong threshold, wrong app link = 1-point Correctness deduction per occurrence with hard ceiling 7 on the affected email. |
   | **Pre-launch gate discipline** | 10% | (Reduced from 15% in 0.13.84; gates-as-fields removed in 0.13.116 — read each upstream's `phases.<phase>.verdict` instead.) All upstream phases must show `verdict: pass` (or equivalent done-shape) before activation: Phase 1 `idea-to-design`, Phase 3 `commcare-setup` (`steps.app-deploy`), Phase 5 `ocs-setup` (`steps.ocs-chatbot-eval-deep`), Phase 9 `execution-management` (`steps.llo-invite`). Activating with any upstream verdict still `in_progress` or `reject` is a 4-point deduction (gate bypass). Activating with `steps.llo-launch` itself still `in_progress` (the producing skill skipped its own write-back) is also a 4-point deduction. |
   | **LLO capacity actual** | 12% | (Added 0.13.84 — viability dimension.) Did the LLO actually recruit and onboard the team they claimed in their solicitation response? Cross-reference `solicitation/award_response` (FLW count promised) against `llo-uat_results` and onboarding artifacts (FLW roster, supervisor designation). **Anchors:** full team recruited, trained, supervisor named with contact = **9.5**; team recruited but ≥1 FLW vacancy or supervisor unnamed = **7.5**; team mostly recruited + supervisor commitment but no Day 1 roster = **6.0**; team understaffed at launch (recruited < claimed) = **4.0**; LLO claimed capacity that didn't materialize at launch = **2.0**. The biggest "things change between Phase 8 award and Phase 9 launch" risk. |
   | **Day-one readiness** | 10% | (Added 0.13.84 — viability dimension.) Are FLWs actually ready to do the work on Day 1? **Anchors:** all FLWs completed Learn-app modules + UAT walkthrough + Day 1 markets/sites named with assignment = **9.5**; most completed but ≥1 FLW incomplete training = **7.5**; team trained but no Day 1 plan / market assignments = **6.0**; trained but no per-FLW UAT signoff or no calibration baseline = **4.0**; firing the launch with FLWs not actually ready (no training records, no Day 1 plan) = **2.0**. The artifact must show Day 1 is actually scheduled, not just "soon." |
   | **Downstream handoff alignment** | 10% | (Added 0.13.84 — viability dimension.) Re-verify at launch that a named downstream consumer is aligned and ready to receive data. **Anchors:** downstream handoff confirmed with named delivery contract (data format, cadence, action-trigger threshold, recipient) = **9.5**; downstream confirmed at launch but contract is implicit = **7.5**; downstream named in PDD but no launch-time confirmation = **6.0**; downstream missing from launch artifact OR vague ("analysts" generic) = **4.0**; firing launch into a downstream that hasn't materialized (PDD claimed Lab X; Lab X never engaged) = **2.0**. The grader may consider upstream verdicts (e.g. `idea-to-pdd-eval`) as context when forming a judgment, but should apply this dimension's own anchors based on the launch artifact — no hardcoded cross-eval cap rules. |
   | **Stop-loss planning** | 8% | (Added 0.13.84 — viability dimension.) Is there a documented halt condition? At what metric thresholds, by what date, does the program pull the plug or iterate? **Anchors:** explicit halt criteria with metric thresholds AND timing AND named decision-maker ("if visits/day < 50% of target by week 2, supervisor X halts and triggers iteration") = **9.5**; halt criteria mentioned with thresholds but timing or owner vague = **7.5**; "we'll evaluate at week N" without specific criteria = **6.0**; no halt planning declared = **4.0**; only "if metrics fall short we'll iterate" without explicit conditions = **2.0**. Catches launches that assume happy path forever. |

   **Deduction rules:**
   - Any single dimension ≤3 → suite verdict `fail`, regardless of
     overall mean. (Production gate; failure modes here ship to
     real LLOs.)
   - **Inflation guard (mirrors prior rubrics):** if the rubric
     surfaces ≥2 `[WARN]`-tier `auto_surfaced` entries, overall is
     capped at **8.5**.
   - **Pre-cap and post-cap reporting** per `eval-calibration` § 0.9.4
     guidance.

4. **Write the verdict YAML** to
   `ACE/<opp-name>/runs/<run-id>/9-execution-manager/llo-launch-eval_verdict.yaml`. The filename uses
   **this eval skill's** name (`llo-launch-eval`), not the bare producer
   name (`llo-launch`) — per the 0.12.0 Option-α rule an `-eval` skill
   keeps `-eval` in its verdict filename; see
   `agents/ace-orchestrator.md § Per-Step Eval Hook` for the naming
   rule:

   ```yaml
   skill: llo-launch-eval
   target: <connect_opportunity_id>
   mode: deep
   ran_at: <ISO timestamp>
   capture_path: launch-summary.md

   overall_score: 8.5
   overall_score_pre_cap: 8.5
   verdict: pass | warn | fail | incomplete

   dimensions:
     # Launch correctness (60%)
     uat_signoff_completeness:       { score: 9.0,  weight: 0.15 }
     connect_activation_correctness: { score: 9.5,  weight: 0.15 }
     app_publish_status:             { score: 10.0, weight: 0.10 }
     go_live_notification_fidelity:  { score: 8.0,  weight: 0.10 }
     pre_launch_gate_discipline:     { score: 9.5,  weight: 0.10 }
     # Launch-time viability (40%, added 0.13.84)
     llo_capacity_actual:            { score: 7.5,  weight: 0.12 }
     day_one_readiness:              { score: 6.0,  weight: 0.10 }
     downstream_handoff_alignment:   { score: 4.0,  weight: 0.10 }
     stop_loss_planning:             { score: 4.0,  weight: 0.08 }

   per_item:
     - ref: "Connect activation: draft → active"
       score: 9.5
       verdict: pass
       note: "Activation timestamp recorded in run_state.yaml; verification rules unchanged from Phase 4."
     # ... per check

   auto_surfaced:
     - severity: WARN
       message: "Go-live email sent before LLO 4 signed off (1 missing UAT sign-off — documented blocker, but launched anyway)."

   gate:
     threshold: 7.5
     disposition: approve | reject | iterate
   ```

5. **Auto-surfaced concerns:**
   - `[BLOCKER]` for any dimension scoring ≤ 3.
   - `[BLOCKER]` if overall score is below 7.0.
   - `[BLOCKER]` for activation with any LLO explicit reject (not pending).
   - `[BLOCKER]` for activation with any upstream gate not approved.
   - `[WARN]` per missing UAT sign-off (pending, not rejected).
   - `[WARN]` per Phase 4→Phase 6 verification-rule drift.
   - `[INFO]` per nice-to-have notification content missing.

## LLM-as-Judge Rubric

Calibration target on a real launch:

- **Detection rate:** ≥ 80% of catalogued launch issues from
  `eval-calibration/known-issues.md § LLO launch`.
- **Inter-run variance:** ≤ 0.5 across 3 same-model runs.
- **Cross-model variance:** ≤ 1.0 for strong calibration.

This rubric ships at **provisional** until a real launch produces
ground truth. Until then, it correctly emits `incomplete` on opps
where Phase 6 hasn't reached llo-launch.

## Archetypes

| Archetype | What this skill does |
|---|---|
| `atomic-visit` | Default. Grades activation with calibration-gate threshold reminder. |
| `focus-group` | Adds a "facilitator-stipend payment-flow" sub-check (FGD opps pay differently from atomic-visit). |
| `multi-stage` | Grades stage-by-stage activation. Adds a "stage-gate-rule activation" sub-check (each stage transition must be configured at launch). |

## MCP Tools Used

- Google Drive: `drive_read_file`, `drive_create_file`,
  `drive_list_folder`
- ace-connect MCP: `connect_get_opportunity` (verify activation
  status against the connect_opportunity_id from connect-setup-summary).
- Nova MCP: `get_app` (verify HQ app publish status).

## Mode Behavior

- **Auto:** Grade, write verdict + report.
- **Review:** Pause after grading.

## Dry-Run Behavior

When `--dry-run` is active:
- Read inputs normally — read-only.
- Skip live Connect/Nova MCP verification (use `3-commcare/app-deploy_summary.md`
  as the single source).
- Write verdict + report.
- State tracks as `dry-run-success`.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-04-28 | Initial version. 5 dimensions: uat_signoff_completeness (0.25), connect_activation_correctness (0.25), app_publish_status (0.20), go_live_notification_fidelity (0.15), pre_launch_gate_discipline (0.15). Inflation guard at 8.5. Explicit `incomplete` verdict when Phase 6 llo-launch hasn't run. Most load-bearing Phase 6 rubric. | ACE team (eval system buildout — 0.9.9) |
| 2026-05-08 | **Viability axis added (40% weight). 5 → 9 dimensions.** Mirrors the 0.13.81 expansion of `idea-to-pdd-eval`: rubric was grading launch correctness exclusively (did the launch fire technically correctly?) without grading whether the launched program is viable at the launch moment. Added 4 launch-time viability dimensions: `llo_capacity_actual` (12%, did the LLO actually recruit the team they promised?), `day_one_readiness` (10%, are FLWs actually ready Day 1?), `downstream_handoff_alignment` (10%, is the named downstream consumer ready to receive data?), `stop_loss_planning` (8%, is there a documented halt condition?). Existing 5 launch-correctness dimensions reduced proportionally to make room: 25→15%, 25→15%, 20→10%, 15→10%, 15→10%. Pairs with `idea-to-pdd-eval` 0.13.84 — at design time and launch time the program is judged on viability axis. | ACE team (0.13.84) |
