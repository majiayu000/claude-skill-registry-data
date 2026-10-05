---
name: survey-architect
version: 1.2.3
author: Personify Labs
description: >
  Turns a research question into a validated, deploy-ready survey: a short
  intake, the right instrument for what's being measured (SEQ, SUS,
  UMUX-Lite, SUPR-Q, NPS, CSAT, CES, PSSUQ, or a custom item set), and a
  platform-native file for Qualtrics, Typeform, or an in-app survey. Trigger
  when someone says "I need to survey users about X," "what should I ask
  users after they do Y," "build me an NPS survey," "help me measure
  usability of Z," or pastes a vague research need and wants it turned into
  an actual instrument. Entry point 1 of the research loop (see
  research-loop).
tags:
  - user-research
  - ux-research
  - surveys
  - qualtrics
  - nps
  - sus
  - supr-q
license: CC-BY 4.0
---

# Survey Architect

Turns "I need to know something about users" into a specific, validated,
deployable survey — not a generic questionnaire.

This skill does not open with a survey. It opens with an interview, because
the wrong instrument answers a question nobody asked.

-----

## Step 0: Intake — never skip this

Before picking an instrument, ask (as a short back-and-forth, not a form
dump):

1. **What product or surface is this for?** Check `../config/product-context.yaml`'s
   `products` list rather than assuming which products exist — this file
   is the one place that list lives, precisely so this skill stays
   portable across organizations without editing prose. If the named
   product isn't on the list, follow `unknown_product_policy`: ask
   whether it's new (add it) or a typo of an existing entry — never
   silently guess.
2. **What decision will this survey inform?** Not "understand users" —
   something a stakeholder will actually do differently based on the
   answer (ship/hold a feature, fix a flow, report a trend, justify
   spend).
3. **Where in the user's experience does this sit?** A single task, a
   full session with the product, the ongoing relationship with the
   product, or one specific transaction (support ticket, checkout,
   onboarding).
4. **Has this been measured before for this product?** If yes, check
   `/research/_benchmarks/<product>.md` — reuse the same instrument and
   wording so the new wave is comparable. Don't introduce a new
   instrument mid-series without a stated reason.

If the answers to 2 and 3 don't line up (e.g., "I want to know if the
onboarding flow is easy" but the answer to 3 is "relationship"), point that
out before proceeding. Don't silently pick one.

Do not proceed to instrument selection until 1–3 are answered.

-----

## Step 1: Instrument selection

Classify the intake answers into a decision_type first — this part is
judgment, not arithmetic — then **run `scripts/selection.py`'s
`select_instrument(decision_type)`** rather than eyeballing the table
below, so the same decision_type can never silently map to a different
instrument on a different run. The table is here for the judgment call
of classifying the situation, not for hand-picking the instrument once
it's classified:

| Decision type | `decision_type` value | Where it sits | Instrument |
|---|---|---|---|
| Is this task doable? | `task_completion` | Single task, mid-test | SEQ |
| Is the product/feature usable overall? | `product_usability_full` / `product_usability_lite` | Full session, post-study | SUS / UMUX-Lite |
| How does our UX compare to the market? | `website_relationship_benchmark` | Website/app relationship | SUPR-Q |
| Are users loyal / would they recommend us? | `relationship_loyalty` | Relationship, quarterly | NPS |
| Were they happy with this specific interaction? | `transactional_satisfaction` | Transactional | CSAT |
| Was this support/self-serve interaction low-friction? | `transactional_effort` | Transactional (support) | CES 2.0 |
| Need diagnostic subscales? | `diagnostic_subscales` | Post-study, deeper | PSSUQ |
| Will they actually adopt this before it ships? | `adoption_prediction` / `adoption_prediction_lite` | Pre-launch prediction | TAM / UMUX-Lite |

Don't let the requester's phrasing ("I want NPS") override what they're
actually asking — if someone asks for NPS but the real question is "is
this specific flow usable," say so and recommend SEQ instead, with the
trade-off named. If `select_instrument` raises (nothing fits), build a
short custom item set and say explicitly that it has no external
benchmark, so the report later doesn't imply false comparability.

**Never modify the wording of a validated instrument** (SUS, SUPR-Q, UMUX,
UMUX-Lite, PSSUQ). A single reworded item breaks the benchmark comparison.
If the wording genuinely doesn't fit (e.g., "system" feels wrong for a
consumer app), swap the bracketed placeholder only — never the item
structure.

-----

## Step 2: Sample size

**Run `scripts/selection.py`'s `required_sample_size(purpose)`** for the
floor, rather than reciting the numbers from memory:

- `rough_benchmark` → 20
- `compare_two_conditions_between` → 213
- `compare_two_conditions_within` → 93
- `ongoing_tracking` → 30

These are MeasuringU's published rule-of-thumb bands, not a computed
power analysis — a true power calculation needs an effect size and
alpha/power assumptions most requesters can't supply at intake. If a
requester needs an actual power calculation for a specific comparison,
say that's a separate, more involved ask rather than quietly
approximating one here.

If the requester's expected reach won't hit the floor for what they asked
for, say so now — this is what feeds the small-sample flag downstream in
feedback-synthesizer. Don't let a study launch that's structurally
under-powered without the requester knowing going in.

-----

## Step 3: Trigger and frequency logic

Specify, as part of the spec, not left to the deploying team to guess:

- **Trigger event:** the specific action/moment that fires the survey
  (task completion, session end, ticket resolution, N days after
  signup) — never "on page load" or a calendar date alone
- **Frequency cap:** global cooldown (default: one survey per person per
  14 days) plus per-instrument cap (relationship metrics like NPS: no
  more than every 90–180 days)
- **Suppression rule:** don't re-survey someone who scored as a recent
  detractor/low scorer until the issue is addressed

-----

## Step 4: Output

Produce a **platform-native, deploy-ready** artifact — not a generic spec —
matched to how it'll actually be shipped:

- **Qualtrics** → QSF-importable question block (question text, response
  scale, scoring formula as a note)
- **Typeform** → JSON matching Typeform's question schema
- **In-app** (a product from `../config/product-context.yaml`'s stack) → a
  small React component using the existing Vois design system
  conventions (route through vois-tokens/righter if UI copy beyond the
  validated item wording is needed — e.g., intro screen, thank-you
  screen)
- **Unspecified platform** → ask which one before generating, don't
  default silently

Along with the deployable file, always also write the structured handoff
files (see research-loop for the full file structure) to
`/research/<study-name>/00-intake.md` + `00-intake.json`, and
`01-survey-spec.json`. The `.json` files are the canonical,
machine-readable versions — the `.md` is the human-readable copy of the
same facts, never a source of additional information the `.json`
doesn't have. Before writing them, run `scripts/selection.py`'s
`validate_intake_spec(intake)` and `validate_survey_spec(spec)` — if
either returns any missing fields, fill them in before writing the
files. This is what feedback-synthesizer and research-loop's state file
read later — they should never have to re-derive the instrument from
raw data or prose alone, and shouldn't hit a missing field that a
two-line check would have caught.

`00-intake.json` shape: `study`, `product`, `learning_goal`,
`experience_moment`, `decision_type`, `instrument`, `required_n`, plus
`prior_benchmark_reused` when Step 0's Q4 applies.

-----

## Rules

Priority when rules interact: **STOP** > **MUST NOT** > **MUST** >
**SHOULD** > **MAY** — see `ux-research/README.md` for the full
precedence explanation. A lower-priority rule never overrides a
higher-priority one.

- **STOP** if the answers to Step 0's Q2 and Q3 don't line up — surface
  the mismatch before picking an instrument, don't silently pick one.
- **MUST NOT** skip intake because the requester already named an
  instrument.
- **MUST NOT** modify validated item wording (SUS, SUPR-Q, UMUX,
  UMUX-Lite, PSSUQ) to "sound more natural."
- **MUST NOT** recommend an instrument the intake answers don't support
  (e.g., NPS for a single-task usability question).
- **MUST NOT** introduce a new instrument for a product with an existing
  benchmark series without flagging the break in comparability.
- **MUST** state the required sample size before a study launches.
- **MUST** produce a platform-native artifact, never a generic text spec,
  once a platform is named.
- **SHOULD** ask which platform to target when none was specified,
  rather than defaulting silently.

-----

## Quick reference

| Requester says | What to check | Likely instrument |
|---|---|---|
| "Is this new flow usable?" | Single task, mid-test | SEQ |
| "How's the product doing overall?" | Full session, post-study | SUS or UMUX-Lite |
| "Are people loyal to us?" | Relationship, quarterly | NPS |
| "Was support helpful?" | Transactional | CSAT or CES |
| "How do we compare to competitors' UX?" | Relationship, benchmarked | SUPR-Q |
| "Will people actually use this feature?" | Pre-launch | TAM / UMUX-Lite |
| Nothing above fits | Custom, one-off | Custom item set, no benchmark |

## Maintaining this skill

`evals/` is the regression suite. After touching `scripts/selection.py`,
run `python3 -m unittest discover -s evals -v` (CI runs the same). After
touching this file's prose, re-check the cases in
`evals/qualitative_cases.md` by hand.
