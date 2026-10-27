---
name: pdd-to-app-journeys
description: >
  Internal /ace:run step — Derive expected FLW app journeys from the PDD.
user-invocable: false
disable-model-invocation: false
---

# PDD to App Journeys

Generate the opp-specific expected-user-journey set that downstream app
QA grades against. Runs in Phase 2 (Scenarios & Acceptance), in
parallel with `pdd-to-test-prompts`. The chatbot side gets Q&A ground
truth from `pdd-to-test-prompts`; the app side gets UX-intent ground
truth here.

## Inputs

Pipeline-only: derives journeys from a run's approved PDD, which exists only in a run.

| Source | Artifact | Used for |
|---|---|---|
| Phase 1 | `1-design/idea-to-pdd.md` | source PDD; archetype + Target FLW persona drive journey generation |

## Products

- `2-scenarios/pdd-to-app-journeys.md` — opp-specific expected-user-journey set ("expected-journeys" for short)

Consumers:
- `app-test-cases` (Phase 3) — turns each journey into a concrete per-form test matrix once Nova has built the apps.
- `app-ux-eval` (deep QA) — LLM-as-Judge over captured screenshots + transcripts, scoring each journey's pass criteria and edge-case recovery.
- `app-screenshot-capture` (Phase 6) — uses the journey list to decide which step sequences to walk through on the AVD.

## Process

1. **Read inputs from GDrive:**
   - PDD: `ACE/<opp-name>/runs/<run-id>/1-design/idea-to-pdd.md`

2. **Read the PDD's `Archetype:` field.** This skill branches on
   archetype — `atomic-visit` uses visit-flow journeys, `focus-group`
   uses session-flow journeys, `multi-stage` produces per-stage
   journeys plus a stage-transition journey. See `## Archetypes` below
   for the full per-archetype journey list. If the PDD has no
   Archetype field, default to `atomic-visit` but flag it as a `[WARN]`
   in the coverage self-check.

3. **Extract persona from the PDD.** Pull the persona section verbatim
   into the `## Persona` block. The canonical name is **"FLW Requirements"**
   (per `templates/pdd-template.md`); the legacy name "Target FLW" is
   also accepted for older PDDs that haven't been re-rendered. If the
   PDD has neither section, halt — the journeys depend on knowing who
   the user is. Don't synthesize a persona; escalate.

4. **Generate journeys per the archetype branch.** For each journey
   in the matching archetype branch, write:

   - **Goal** — one-line user-outcome goal (e.g. "FLW completes a
     household survey and sees confirmation").
   - **Happy path narrative** — 2-4 sentences in user-outcome
     language, NOT field/form mechanics. The reader should be able to
     picture what the FLW sees and does. Bad: "tap the next button on
     screen 3, fill required field household_id." Good: "FLW confirms
     the household by name and phone, completes screening, photographs
     the MTN card, and submits."
   - **Edge cases (UX outcomes, not error codes)** — at least 2 per
     journey, each phrased as a UX outcome the FLW experiences, not
     a backend error condition. Bad: "duplicate-detection returns 409
     Conflict." Good: "FLW understands why a duplicate-household
     submission was rejected and how to proceed."
   - **Pass criteria** — measurable UX-level criteria that
     `app-ux-eval` can grade. Bad: "all required fields are
     non-null." Good: "Journey completes in <3 minutes including
     form fill" / "Required-field errors are recoverable in-form."

4a. **Generate deployability-exercising journeys (the fitness surface).**
    Happy-path journeys alone describe a thin instrument.
    `pdd-to-app-journeys-eval § deployability_fitness` hard-fails a
    journey set that never demands the capture/validation/persistence a
    deployable app needs, and `app-ux-eval § capture_robustness` needs a
    negative path to grade. So when the PDD's Evidence Model implies it,
    ALWAYS include:

    - **≥1 negative-path / bad-input journey** — the FLW enters a value
      the instrument should reject (blank required field, out-of-range
      count, malformed phone) and experiences a clear, recoverable
      rejection. This is the journey `app-test-cases` turns into a
      negative-path Maestro recipe and `app-ux-eval § capture_robustness`
      grades. A journey set with zero negative-path journeys is a
      coverage gap, not a pass. **A low-accuracy GPS fix is NOT a member
      of this set** — no build can reject one (dimagi-internal/ace#1006,
      ace#1013), so a journey demanding that rejection is ungradable by
      construction; it belongs under the capture-fidelity expectation
      below, as an advisory the FLW sees and can act on. Before demanding
      any enforcement a journey's pass criteria will be graded on, check
      it against `skills/_app-component-library.md § Mechanisms a PDD
      must not assert` — Table A (closed at the platform surface) and
      Table B (buildable, outside ACE's toolchain today). A journey that
      demands a Table A mechanism cannot pass, and a journey that calls a
      Table B mechanism impossible is its own error.
    - **A capture-fidelity expectation** in the relevant journey's pass
      criteria — e.g. "the fix's accuracy is shown to the
      FLW and submitted with every visit, and a reading worse than the
      stated tolerance raises an on-screen advisory," "enumerable answers
      are picked from a list, not typed,"
      "an 'Other' selection prompts a specify field."
    - **For multi-visit / follow-up designs, a persistence journey** —
      the follow-up visit records change against the existing household,
      and the change is visible/retained (the UX face of case
      write-back).

    Phrase all of these as UX outcomes (what the FLW sees/does), not
    backend mechanics — same voice rule as the happy path. These are
    *findings the journeys must demand even if the PDD only implied
    them* — PDD silence is not a waiver.

5. **Self-evaluate coverage** (see `## Coverage rules` below):
   - At least one journey per archetype branch category.
   - Every journey has at least one `error_recovery`-flavored edge
     case (so `app-ux-eval`'s rubric has signal on recoverability).
   - Every journey has at least one measurable pass criterion.
   - **≥1 negative-path / bad-input journey exists** (step 4a) so
     `app-ux-eval § capture_robustness` has signal and
     `deployability_fitness` can pass.
   - **Capture-fidelity + (for multi-visit) persistence expectations are
     present** per step 4a where the Evidence Model implies them.

   If any rule is missed, go back to step 4 and add.

6. **Write the journeys file** to
   `ACE/<opp-name>/runs/<run-id>/2-scenarios/pdd-to-app-journeys.md`. Use
   the template at `templates/expected-journeys-template.md` as the
   skeleton.

## Archetypes

ACE skills branch on the PDD's declared `archetype:` field. The journey
list here is what `app-test-cases` (Phase 3) and `app-ux-eval` (deep
QA) will later grade against, so getting them right for the archetype
matters: an FGD opp graded against atomic-visit-shaped journeys
produces false-positive failures in the deep app eval.

### How to read a branch count

Each branch below states a **DELIVER-SIDE** journey count. Three things sit
outside it, and reading the count as a total is how it goes wrong:

1. **The Learn smoke is additive.** Coverage rule 4 makes
   `training-completion-smoke` (`app: learn`, `is_smoke: true`) mandatory for
   every archetype that has a Learn app — i.e. all of them except
   `focus-group`. It is not one of the branch categories and does not consume a
   slot in the branch count.
2. **The count's FLOOR moves down on PDD deferral.** Coverage rule 1 permits
   skipping a category whose surface the PDD explicitly defers (no eligibility
   rules → no `eligibility-edge`; no photo or GPS → no photo-quality
   `data-quality-error`), marked `[INFO]` in the coverage self-check.
   `visit-flow` or its per-archetype equivalent is always required.
3. **The count's CEILING is the branch's own category list, including the
   conditional ones.** `longitudinal-visits` reads 4–6 rather than 4–5 because
   `registration` is emitted whenever the entity is registered in-app, which is
   the common case.

**These numbers are derived, not chosen — re-derive them when you add a
category.** Every branch count here was smaller than the coverage rules
mandated until 2026-09-08 (`longitudinal-visits` said 3–5 against a compliant
floor of 6, `atomic-visit` 2–4 against 5), because Coverage rule 4 was added in
2026-05 and no branch count moved with it. That made both ranges unsatisfiable
while complying with the same file's blocking rules, and every longitudinal and
atomic run paid the reconciliation. Third instance of the class in this file
family after ace#1545; ace#2274 for this one. *Enforced:*
`test/skills/journey-count-consistency.test.ts`.

### `atomic-visit` (default)

The PDD describes one FLW visit producing one structured delivery
(photo + GPS + form). Examples: turmeric market survey, household data
collection.

Generate **2–4 DELIVER-SIDE journeys** covering the categories below. **The
mandatory Learn smoke from Coverage rule 4 is ADDITIONAL to this count** — a
two-app opp therefore emits 3–5 journeys in total. See § How to read a branch
count.

- **visit-flow** — the happy-path walk through Connect → Deliver app
  → form fill → submit → confirmation. The FLW completes one full
  delivery end-to-end without errors.
- **eligibility-edge** — the FLW encounters a beneficiary who is on
  the boundary of the inclusion/exclusion rules. Pass criterion: the
  app makes the eligibility decision legible to the FLW; the FLW does
  not have to guess.
- **data-quality-error** — the FLW makes a data-entry mistake (bad
  GPS, blurred photo, required field skipped) and recovers in-form
  without losing prior input.
- **duplicate-handling** — the FLW visits a household that's already
  been submitted. Pass criterion: the FLW understands why the
  submission was rejected and what to do next.

### `longitudinal-visits`

The PDD describes repeat visits to a durable entity over time.
Generate **4–6 DELIVER-SIDE journeys**. **The mandatory Learn smoke from
Coverage rule 4 is ADDITIONAL to this count** — a two-app opp therefore emits
5–7 journeys in total. See § How to read a branch count. Keep `visit-flow` and
`data-quality-error` from `atomic-visit`, and add the journeys that only exist
once there is a case:

- **case-selection** — the FLW opens the Deliver app, finds the right
  entity in the case list (search / filter), and sees enough state on
  the case tile to know which visit is due. Pass criterion: the FLW can
  tell *which* visit is next without asking anyone.
- **followup-with-preload** — a follow-up visit against an existing
  case. Pass criterion: prior state visibly preloads, and the FLW is not
  re-keying what the case already knows.
- **repeat-activity** — the FLW submits an activity this entity has
  already had. Pass criterion: the app or the payment model handles it
  per `payability-against-history`, and the FLW is not misled into
  expecting payment for work that will dedup away.
- **registration** — only when the entity is registered in-app
  (skip when cases arrive by import or already exist).

### `focus-group`

The PDD describes FLW-facilitated group discussions where qualitative
content is captured **in a Google Doc out-of-band**. The mobile-app
surface is narrow: one ~5-field attestation form (consent, date,
venue, GPS, photo) submitted at session end as the payment trigger.
The gdoc is written separately, hours-to-days later, with no
`gdoc_link` field on the form. See
`docs/superpowers/specs/2026-05-15-focus-group-archetype-redefinition.md`.

Generate **2–4 DELIVER-SIDE journeys** covering the categories below. There is
**no Learn app for `focus-group`**, so Coverage rule 4 adds nothing here and
this count is also the total. See § How to read a branch count.

- **session-setup** — the FLW arrives at the venue, runs through the
  consent step verbally with participants per the consent script
  (out-of-app), and is ready to facilitate. **No in-app interaction
  at session start** — the mobile form is filled at session end.
  Happy path: arrives prepared, consent obtained, ready to begin.
- **recruitment-failure** — the FLW arrives and turnout is below the
  PDD's minimum group size. Pass criterion: the FLW knows the protocol
  (cancel / reschedule / proceed-with-fewer per the LLO coordinator's
  guidance — typically reschedule). **App-side:** if the session
  doesn't run, no attestation is submitted (no payment).
- **consent-handling** — one or more participants decline to
  participate. Pass criterion: the FLW captures the refusal verbally,
  knows whether to proceed (per consent script: proceed only if all
  remaining participants consented), and if proceeding, the
  attestation form's `consent_all_participants` field can answer `yes`
  for the participants who DID consent and stayed. If consent fails
  the session aborts; no attestation submitted.
- **attestation-submission** — the FLW reaches session end, opens the
  Deliver app, fills the 5-field attestation form (consent, date,
  venue, GPS, photo), and submits. Pass criterion: form submits
  cleanly within the 24h window; GPS captured at venue; photo not
  showing faces; coordinator can match this attestation to the gdoc
  the FLW will write later by `(FLW, session_date, venue)`. Edge
  cases: GPS out of expected radius, late submission (>24h).

### `multi-stage`

The PDD has two or more sequenced stages with different archetypes.
For each stage, identify its declared archetype and generate that
archetype's full journey list from the sections above. Prefix each
journey title with the stage number (e.g. `Stage 1 — session-setup`,
`Stage 2 — visit-flow`).

**Generating per-stage journeys:** treat each stage independently. A
`focus-group` Stage 1 generates the 4 focus-group journeys; an
`atomic-visit` Stage 2 generates the 4 atomic-visit journeys. Do not
collapse stages or skip journeys because they seem similar across
stages — the FLW needs clear per-stage UX flows.

**Cross-stage journey** (always add, once per PDD, not per stage):

- **stage-transition** — the FLW finishes Stage 1 and begins Stage 2.
  Happy path: the FLW knows from the app that Stage 1 is closed,
  understands what changed in their available actions, and can begin
  Stage 2 deliveries without confusion. Edge case (`error_recovery`
  flavor): an FLW attempts a Stage-1-only action after the gate has
  closed; the app makes the new constraint legible. If the PDD's
  Stage Gate section is missing or vague, flag it as a `[WARN]` in
  the coverage self-check (step 5) — without a clear gate the deep
  eval can't grade transition correctness.

## Coverage rules

Before writing the file, verify:

1. **One journey per archetype-branch category — when the PDD declares
   the underlying surface.** Atomic-visit's expected categories are
   visit-flow, eligibility-edge, data-quality-error, duplicate-handling.
   Emit a journey for every category whose surface the PDD declares;
   SKIP categories where the PDD explicitly defers the surface
   (eligibility rules deferred → no eligibility-edge journey; no photo
   or GPS → no photo-quality data-quality-error journey). Mark each
   skipped category with `[INFO]` calibration context in the coverage
   self-check at the bottom of the doc; the eval-side rubric grants a
   PDD-deferral exemption for these. Focus-group needs session-setup,
   recruitment-failure, consent-handling, attestation-submission
   (same PDD-deferral rule). Multi-stage needs per-stage coverage
   plus the stage-transition journey. **Minimum after deferral
   exemptions: visit-flow (or per-archetype equivalent) is ALWAYS
   required.**

2. **At least one `error_recovery`-flavored edge case per journey.**
   The `app-ux-eval` deep rubric specifically grades whether the app
   makes failure modes legible and recoverable; a journey with no
   error-recovery edge case starves that rubric of signal. Examples:
   "FLW recovers from a network drop mid-submit and doesn't lose
   form state," "FLW hits a validation error and understands which
   field needs fixing," "FLW understands why a duplicate was rejected
   and how to proceed."

3. **At least one measurable pass criterion per journey.** "Journey
   completes" alone is not measurable; pair it with a time bound, a
   recoverability claim, or a structural-output claim that the deep
   eval can grade.

4. **Training-app coverage (Learn smoke) — REQUIRED for every PDD with
   a Learn app.** Every archetype except a hypothetical Learn-less mode
   produces a Learn (training) app. Phase 6's training deck needs
   screenshots of BOTH apps, so the journey set MUST include at least
   one Learn-app journey:

   - `training-completion-smoke` — happy-path FLW completes Learn
     Module 1 (content form + assessment), passes the assessment,
     returns to the suite root with Module 1 marked complete. Pass
     criterion: the FLW reaches the first assessment, submits with a
     passing score, and Module 1 row shows a completion indicator
     (per atlas § 6 — completion-state is rendered on the row).

     Set `app: learn` and `is_smoke: true` on this journey. It is the
     mandatory pair to the Deliver-side smoke for two-app opps.

   Deeper Learn-app journeys (full curriculum walk, assessment-fail
   recovery, etc.) belong in `/ace:qa-deep` and may be added as
   non-smoke entries with `is_smoke: false`. Phase 6 shallow only
   needs the one smoke per app.

   This rule was added 2026-05-18 after the malaria-itn-app run
   20260517-1829 surfaced a Phase 6 halt: Phase 2 had generated 9
   Deliver journeys + 0 Learn journeys, Phase 3 dutifully wrote
   `smoke_journeys_per_app: {learn: 0, deliver: 1}`, and Phase 6's
   smoke run tried to reach Deliver via `connect-claim + Start +
   tap V1` — which lands in Learn, not Deliver, because Connect gates
   Deliver behind Learn-assessment completion (see
   `docs/learnings/2026-05-18-connect-gates-deliver-on-learn-completion.md`).
   The right fix is structural: always emit the Learn smoke so Phase 6
   captures it independently, AND the Deliver smoke walks Learn to
   completion first (see `app-test-cases` for the recipe shape).

If any rule is missed, return to the journey-generation step (step 4
in `## Process`) and add until coverage is satisfied.

The numbered rules above are blocking — failing any of them sends you
back to regenerate journeys. The `[WARN]` cases listed in `## Failure
Modes` (e.g., a vague Stage Gate) are non-blocking — flag them in the
output but proceed.

## MCP Tools Used

- Google Drive: `drive_read_file`, `drive_create_file`

## Mode Behavior

- **Auto:** Generate the full journey file, self-evaluate coverage,
  write it.
- **Review:** Pause before writing to present the generated journey
  list for operator approval. This artifact is the UX ground truth
  for downstream app QA, so getting it wrong cascades into
  false-positive / false-negative deep-eval failures in Phase 6.

## Dry-Run Behavior

When `--dry-run` is active:
- Generate the journey file content as normal.
- Write to `comms-log/dry-run-pdd-to-app-journeys.md` instead of
  `2-scenarios/pdd-to-app-journeys.md`.
- State tracks as `dry-run-success`.

## Failure Modes

- **PDD missing or empty** — blocker; Phase 1 Step 1 (`idea-to-pdd`)
  hasn't completed. Don't synthesize; escalate.
- **PDD has neither "FLW Requirements" nor "Target FLW" section** —
  blocker; the journeys describe what the FLW does and need a defined
  FLW. The canonical name is "FLW Requirements" (per
  `templates/pdd-template.md`); "Target FLW" is the legacy name and is
  also accepted. Flag back to the operator and request a PDD revision;
  don't synthesize a persona.
- **PDD has no eligibility / duplicate-handling / consent / output
  spec** — for the relevant archetype, the journey set will be
  missing a category. Flag a `[WARN]` rather than blocking, and note
  in the journey file which categories were skipped because the PDD
  was thin. The deep eval needs to know to expect partial coverage.
- **Multi-stage PDD with vague Stage Gate** — the
  `stage-transition` journey can't grade transition correctness if
  the gate isn't defined. Flag a `[WARN]` and write the journey with
  the best-available constraints; recommend the operator strengthen
  the Stage Gate section before activation.

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-05-08 | **No QA companion.** `pdd-to-app-journeys-qa` removed (PR #160) — downstream consumers are LLM-driven; structural label-format checks gate nothing real, and the eval already covers the substantive concerns. See `skills/_qa-decisions.md` for the registry entry + revisit conditions, and `docs/learnings/2026-05-08-fake-qa-detection.md` for the heuristic. | ACE team |
| 2026-05-15 | Accept either "FLW Requirements" (canonical, per `templates/pdd-template.md`) or "Target FLW" (legacy) as the persona section in Process step 3 + Failure Modes. Prompted by `malaria-itn-fgd/20260514-2007` where the template-conformant PDD said "FLW Requirements" and the skill halted looking for "Target FLW". See jjackson/ace#302. | ACE team |
| 2026-05-15 | Recharacterize `focus-group` journey categories for the attestation-form-only shape (PRs #305, #306): `output-coherence` (which assumed the FLW fills 28 in-app fields with content) → `attestation-submission` (FLW fills the 5-field form at session end, no per-section content in the app). Session-setup reframed to note "no in-app interaction at session start" — the mobile form is end-of-session only. Other categories (recruitment-failure, consent-handling) reframed to note no-attestation-on-abort semantics. Coverage rule updated to reference the new category name. Prompted by `malaria-itn-fgd/20260514-2352` re-run. | ACE team |
| 2026-05-29 | **Deployability-exercising journeys (ITN post-mortem, producer↔eval symmetry).** Added Step 4a + two coverage rules: when the Evidence Model implies it, the journey set MUST include ≥1 negative-path/bad-input journey (the recoverable-rejection path that `app-test-cases` turns into a negative-path recipe and `app-ux-eval § capture_robustness` grades), capture-fidelity pass criteria (GPS accuracy gating, structured-pick over typing, other→specify), and — for multi-visit designs — a persistence journey (follow-up records change). Symmetric with the new `pdd-to-app-journeys-eval § deployability_fitness` hard-gate; PDD silence is not a waiver. See `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md`. | ACE team |
| 2026-09-06 | **A low-accuracy GPS fix is no longer offered as a negative-path example, and the capture-fidelity example no longer says "rejected" (dimagi-internal/ace#1619).** The bad-input bullet listed "a low-accuracy GPS fix where a radius is specified" beside blank/out-of-range/malformed-phone, and the capture-fidelity bullet modelled the expectation as *"GPS capture is rejected below the accuracy threshold."* No build can do either: Nova rejects `validate` on `kind: geopoint` and Connect's verification-flags form no longer carries `gps` / `gps_radius_meters` (ace#1006, ace#1013), and `idea-to-pdd § Step 4a` FORBIDS the PDD from asserting it. So this skill was handing authors the exact phrasing Phase 1 is not allowed to write, `app-test-cases` then compiled it into a negative-path Maestro recipe that cannot pass, and `pdd-to-app-journeys-eval` graded the result against it. Both examples now model the observability contract (accuracy shown + submitted + a whole-range advisory), and the bullet points at `_app-component-library.md § Mechanisms a PDD must not assert` — the pointer `test/skills/pdd-must-not-assert-mechanisms.test.ts` already required of `idea-to-pdd` and its eval, and never of this pair. Sibling half of the same drift in `pdd-to-app-journeys-eval`; `pdd-to-deliver-app-eval § Capture fitness` received this correction on 2026-07-28 and it was not propagated here. | ACE team |
| 2026-09-08 | **Every archetype branch's journey COUNT was smaller than the file's own blocking coverage rules mandate (dimagi-internal/ace#2274).** `longitudinal-visits` declared 3–5 against a compliant floor of 6 and `atomic-visit` declared 2–4 against 5, because Coverage rule 4 (2026-05-18) made a Learn smoke journey mandatory and no branch count moved with it — so both ranges were unsatisfiable while complying with the same file's blocking rules, and every longitudinal and atomic run paid the reconciliation. Counts are now explicitly DELIVER-SIDE with the Learn smoke stated as additive, `longitudinal-visits` is 4–6 so the conditional `registration` journey fits, and a new § How to read a branch count records the derivation. Third instance of the count-drifts-behind-the-mandate class in this file family after ace#1545. Observed on `bednet-check-2-visit/20260908-1544`, where the compliant set was 7 journeys against a declared ceiling of 5. *Enforced:* `test/skills/journey-count-consistency.test.ts` (ratchet with controls — the ceiling must cover the branch's own bullets plus any it keeps from another branch). | ACE team |
