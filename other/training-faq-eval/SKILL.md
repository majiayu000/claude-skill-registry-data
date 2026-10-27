---
name: training-faq-eval
description: >
  Internal /ace:run step — Grade the training FAQ.
user-invocable: false
disable-model-invocation: false
---

# Training FAQ — Eval

Grades `6-qa-and-training/training-faq.md`. The FAQ is the highest-traffic
training artifact: an FLW interrupted in the field needs to find the answer
to "where do I tap to retake the photo?" in seconds, and an LLO triaging
their first cohort needs the escalation matrix in front of them. An
independent grader catches comprehension/accuracy gaps that the producing
skill's self-eval routinely under-counts.

**Fitness axis (out-of-chain anchor).** "Does the FAQ list the catalogued
questions?" is a topic tally — a faithful build of a thin PDD passes it by
echoing the headings. The fitness dimension is `answer_usefulness`: does
each answer *actually resolve* the question for a worker mid-visit (vs the
question merely *appearing* with a hand-wave answer), and is it written for
the field rather than for a developer at a desk? It anchors on whether the
reader could act on the answer in the real world, not on whether the
question is present, and hard-gates an FAQ whose answers are present but
non-resolving. The comprehensiveness tally is demoted below it. See
`skills/_eval-template.md § The out-of-chain fitness requirement`.

See `skills/_eval-template.md` for shared verdict / severity / stock-block
contracts and `skills/eval-calibration/SKILL.md` for the calibration
methodology. Provisional rubric — calibration TBD until 3+ shipped FAQs
produce ground truth.

## Inputs

Pipeline-only: grades a run's training FAQ, which exists only in a run.

| Source | Artifact | Used for |
|---|---|---|
| Phase 6 | `6-qa-and-training/training-faq.md` | artifact under judgment |
| Phase 1 | `1-design/idea-to-pdd.md` | anchors anticipated questions (Operational Caps, Evidence Model, Stage Gate triggers) and archetype |
| Phase 3 | `3-commcare/app-deploy_summary.md` | deliver-app field paths + form names; verifies "tap this button" prose matches reality |
| Phase 5 | `5-ocs/ocs-bot-config.md` (if present) | escalation routing — FAQ should match what the bot tells FLWs |

## Products

- `6-qa-and-training/training-faq-eval_verdict.yaml` — verdict YAML per
  `_eval-template.md § Verdict YAML contract`. Filename uses the producer
  stem.

## Process

1. Read inputs from Drive. Read the artifact under judgment from its PUBLISHED file, never your local draft, and re-read it after any republish — see `skills/_eval-template.md § Grade the published revision (stock)` (an empty published artifact is a BLOCKER, ace#2592).
1b. **Run the published-render gate before grading anything:** `scripts/check-published-doc-render.ts <published Doc URL>` — see `skills/_eval-template.md § Published-render gate (stock)`. A non-zero exit (raw markdown on the page, or a doc an anonymous reader cannot open) makes this eval's verdict `fail`, whatever the prose would score (ace#2213). Write the Doc URL you checked to the verdict as top-level `published_url`, and the result as `published_render` — `capture_path` keeps naming the run-folder source, so the verdict records both what was composed and what a reader opened.

2. Build an "anticipated-questions catalogue" from the PDD: Operational
   Caps (daily visit limits, payment per visit), Evidence Model Layer A
   rules (what photo counts, what GPS accuracy is needed), Stage Gate
   triggers (when does a visit get rejected), payment timing, support
   contact. This is the rubric's expectation set.
3. For each catalogue entry, check whether the FAQ surfaces an answer
   (or documents why it doesn't apply for this archetype). **Distinguish
   "question appears" from "answer resolves the question"** — read each
   answer and judge whether a worker mid-visit could actually act on it,
   not just whether the Q/A pair exists. Answer non-resolution is the
   `answer_usefulness` signal.
4. Apply the rubric and write the verdict YAML.
5. Surface concerns by severity per `_eval-template.md § Auto-surfaced
   severity rules`.

## LLM-as-Judge Rubric

Score each dimension 0–10. Weights sum to 1.0.

| Dimension | Weight | Anchored criteria |
|---|---|---|
| **Answer usefulness** (fitness — out-of-chain) | 0.30 | For each Q/A pair, does the *answer actually resolve the question* for a worker mid-visit — and is it written for the field, not for a developer at a desk? This is distinct from comprehensiveness: a question can *appear* with an answer that doesn't resolve it ("How do I retake the photo?" → "Use the photo retake feature."). Anchor on whether the reader could act on the answer in the real world. 10 = answers are imperative, concrete (name the actual UI control / the actual number / the actual next step), and each genuinely resolves its question. 6 = mixed — some answers resolve, others hand-wave or stay abstract; voice drifts toward spec-prose. 3 = answers are present but non-resolving (restate the question, point at a feature without saying how, or read like a spec doc). **Hard-gate: if the load-bearing answers (payment, photo/GPS recovery, escalation) are present but non-resolving, score ≤ 3 → suite verdict `fail`.** PDD silence on how something actually works is a finding here, not a free pass. |
| **Comprehensiveness** (conformance) | 0.20 | Does the FAQ surface answers to the top-N anticipated FLW/LLO questions catalogued from the PDD? 10 = covers ≥ 80% of catalogued questions, including all Layer A verification edges (photo retakes, GPS retry, consent gate). 6 = covers 50–80%; visible gaps in payment or escalation. 3 = covers < 50%; user would need to ask the bot for basic flow. Hard-deduct -3 if any of {payment-per-visit, daily-cap, support-contact} is missing entirely. **Verify the consent-gate clause by scanning the body, never by impression** — this row scored a consent-free FAQ as covering the consent gate on `hh-poverty-targeting/20260824-1404`; absence is a BLOCKER under the hard-deduct rules below, not a partial credit here. |
| **Accuracy** | 0.20 | Every concrete claim (button labels, field names, numeric caps, payment amounts, escalation contacts) matches the PDD + deploy summary. 10 = no factual drift detected. 6 = ≤ 2 minor drifts (e.g., outdated screenshot caption, off-by-one cap). 3 = ≥ 3 drifts or one load-bearing inaccuracy (wrong payment number, wrong support email). Hard-deduct -5 for any contradicted operational cap. |
| **Scannability** | 0.15 | Can an interrupted FLW find their answer in ≤ 15 seconds? 10 = question-first headings, indexed/grouped by task, short answers, bolded keywords. 6 = walls of prose under generic headings; user must read paragraphs. 3 = no headings or anchors; FAQ is unusable mid-task. |
| **Anticipated-question depth** | 0.15 | Beyond the catalogued surface, does the FAQ anticipate edge cases the PDD implies (e.g., "what if the market is closed today?" for a market-survey opp)? 10 = surfaces ≥ 3 archetype-specific edge cases with answers. 6 = 1–2 surfaced. 3 = none; FAQ is rote. |

Weights sum to 1.0: 0.30 + 0.20 + 0.20 + 0.15 + 0.15 = 1.00.

**Hard-deduct rules:**
- **Consent absent while `consent-script-floor` fires → BLOCKER; suite verdict `fail`.** Grade this the way it was found, not by reading impressions: run a case-insensitive scan of the PUBLISHED body for the consent protocol and read the hits. The floor is at least two `[FLW]` entries — the script itself, and the refusal/withdrawal path (`training-faq § step 4b`, the producer-side obligation this mirrors). Fire the trigger straight from `_app-component-library.md § consent-script-floor`, whose clauses are evaluated INDEPENDENTLY and can fire on a PDD that never uses the word. An adjacent sentence that gestures at "what they were told at the start" without naming the script or the refusal path does **not** clear the floor. Live (`measured_on: 2026-08-26`; that run's FAQ and PDD are live, mutable Drive documents — re-read them before treating this as a regression gate): `hh-poverty-targeting/20260824-1404` shipped a consent-free FAQ — `grep -in consent` returned zero hits across 11,822 characters — on a PDD mandating a six-element read-aloud script in § 7.5 and making refusal one of three non-payable outcomes, while `comprehensiveness` scored it as covering the consent gate (ace#1687).
- Load-bearing answers present but non-resolving (`answer_usefulness` ≤ 3) → BLOCKER; suite verdict `fail`. A faithful echo of the catalogued questions with hand-wave answers does not earn a pass.
- Screenshot reference exists in markdown but resolves to a dead Drive ID → BLOCKER (cap overall ≤ 5).
- FAQ contradicts a PDD operational cap (e.g., FAQ says "10 visits/day" when PDD says 8) → BLOCKER.
- Any single dimension ≤ 3 → suite verdict `fail`.

**Inflation guard.** If `training-faq` self-eval graded itself top-tier
and this rubric's overall ≤ 8.0, cap overall at 8.0 and surface a
`[WARN]`. Default no-op until the producer ships a self-eval.

**Calibration target** (per `_eval-template.md § Calibration target boilerplate`):
- Detection rate ≥ 80% of catalogued FAQ issues from
  `eval-calibration/known-issues.md § Training FAQ` (catalogue TBD).
- Inter-run variance ≤ 0.5 across 3 same-model runs.
- Agreement with self-eval within ±1.5 points.

Provisional — flagged until first real run produces ground truth.

## Archetypes

| Archetype | Rubric tweak |
|---|---|
| `atomic-visit` | Default. Anticipated-question catalogue centers on per-visit flow, photo/GPS retries, payment per visit. |
| `focus-group` | Catalogue shifts to attendance, per-session payment, facilitator vs participant Qs. Comprehensiveness dimension expects FGD-specific entries. |
| `multi-stage` | Catalogue expects per-stage FAQ blocks + Stage-Gate-trigger explanations ("what does it mean my visit is in `stage_2_pending`?"). |

## MCP Tools Used

See `skills/_eval-template.md § MCP Tools Used (stock)`.

## Mode Behavior

See `skills/_eval-template.md § Mode Behavior (stock)`.

## Dry-Run Behavior

See `skills/_eval-template.md § Dry-Run Behavior (stock)`.

## Change Log

| Date | Change | Author |
|---|---|---|
| 2026-05-09 | Initial version. 5 dimensions: comprehensiveness (0.35), accuracy (0.25), scannability (0.20), field_realism (0.10), anticipated_question_depth (0.10). Provisional rubric — calibration TBD until first real run grades the artifact. | ACE team (qa-eval-registry initial buildout) |
| 2026-05-29 | Promoted the fitness axis above the comprehensiveness tally: renamed `field_realism` → `answer_usefulness` (0.10→0.30, out-of-chain, hard-gate) and folded in an "answer actually resolves the question" judgment distinct from "question appears". Demoted comprehensiveness 0.35→0.20 (it was a topic tally); accuracy 0.25→0.20, scannability 0.20→0.15, anticipated_question_depth 0.10→0.15. Sum = 1.00. Per `docs/superpowers/specs/2026-05-29-eval-fitness-gap.md`. | ACE team (eval-fitness-gap) |
| 2026-08-26 | **An absent consent protocol becomes a BLOCKER (ace#1687).** `comprehensiveness` already listed "consent gate" among the Layer A verification edges, and it scored `hh-poverty-targeting/20260824-1404` as covering it while the published FAQ contained the word zero times across 11,822 characters — on an `atomic-visit` PDD mandating a six-element read-aloud script in § 7.5 and making refusal one of three non-payable outcomes. A clause inside a 0.20-weighted dimension is not a gate: partial credit absorbed a total absence. Added a hard-deduct BLOCKER firing on `_app-component-library.md § consent-script-floor` — the same trigger the producer, the build, and `pdd-to-deliver-app-eval` share — requiring the script AND the refusal/withdrawal path, graded by scanning the published body rather than by impression. Weights unchanged. Mirrors the producer-side obligation added as `training-faq § step 4b` the same day, so build-emit and eval-grade cannot drift. *Enforced:* `test/skills/training-faq-consent-coverage.test.ts`. | ACE team |
