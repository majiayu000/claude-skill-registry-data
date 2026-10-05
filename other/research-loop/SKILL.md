---
name: research-loop
version: 1.2.3
author: Personify Labs
description: >
  Orchestrates survey-architect, feedback-synthesizer, and research-reporter
  as an iterative research loop that routes back upstream when a downstream
  step can't proceed cleanly, with per-study state and a per-product
  longitudinal benchmark. Use this as the single entry point for any UX
  research task — a new study, raw data to make sense of, or a report to
  write — rather than calling the three skills directly. Trigger when
  someone starts a new research study, pastes raw feedback/survey data
  without a study already in motion, or asks to "run the research loop."
tags:
  - user-research
  - ux-research
  - orchestration
  - router
license: CC-BY 4.0
---

# Research Loop

Runs survey-architect, feedback-synthesizer, and research-reporter as a
loop that behaves like an actual research team: someone can say "that
sample's too small, we need more data" and send it back, rather than
quietly writing up a shaky number.

Each of the three skills works standalone. This skill exists for the
handoffs between them and the file structure that lets a later skill (or
a later *study*) pick up where an earlier one left off.

-----

## The loop at a glance

```
Entry detection
    ↓
survey-architect (intake → instrument → sample size → deploy-ready spec)
    ↓
 [ pause: wait for data collection ]
    ↓
feedback-synthesizer (score + CI + significance + theme + severity)
    ↑___________kick back if n insufficient for stated goal_______|
    ↓
research-reporter (audience-formatted output)
```

Max loop-backs: 2 per study. If a second kickback doesn't resolve it,
surface the trade-off to the researcher rather than looping a third time.

-----

## Entry detection

**Run `scripts/routing.py`'s `detect_entry_point(...)`** rather than
eyeballing the table below — pass whether a learning goal, raw data, an
existing study folder, and a synthesis file are present, and use its
return value. The table is here to show the reasoning, not to be
hand-matched each time:

| What's pasted / asked | Entry point |
|---|---|
| A research question, no data yet ("I need to know if X is usable") | survey-architect |
| Raw survey results / CSV / feedback pile, no study folder exists yet | feedback-synthesizer (standalone mode — no spec file to read) |
| Raw data + an existing `/research/<study-name>/` folder | feedback-synthesizer (loaded mode — reads the spec) |
| A finished `02-synthesis.md` and a request to write something up | research-reporter |
| "Run the research loop" with a vague ask | Start at survey-architect Step 0 (intake) — let intake clarify |

A finished synthesis file always wins the routing decision, even if a
learning goal or raw data is also present — it's the most-progressed
artifact for that study. Don't force every input through all three
stages: a pile of app store reviews with no survey behind it goes
straight to feedback-synthesizer in standalone mode, full stop — this
is a common failure mode worth guarding against explicitly (see
qualitative_cases.md Case 1).

`detect_entry_point` is the **cold-start** path — it infers progress by
checking which files exist, for a study that has no state file yet
(including one that predates this state model). Once `00-state.json`
exists for a study, prefer reading it (below) over re-sniffing files on
every turn.

-----

## File structure

```
/research/<study-name>/
  00-intake.md          — product, learning goal, instrument decision (survey-architect)
  00-intake.json          — same facts, canonical/machine-readable (survey-architect)
  00-state.json           — explicit state + loopback count + artifact validation (research-loop)
  01-survey-spec.json     — deploy-ready spec: items, scoring, n, triggers (survey-architect)
  02-synthesis.md         — scores, CIs, significance, themes, severity (feedback-synthesizer)
  02-synthesis.json         — same facts, canonical/machine-readable (feedback-synthesizer)
  03-report-internal.md   — internal-audience report (research-reporter)
  03-report.json            — same facts, canonical/machine-readable (research-reporter)
  03-report-formal.docx   — formal-audience report, if requested (research-reporter)

/research/_benchmarks/<product>.md
  — running log: date, instrument, score, CI, n, measurement conditions, per wave
  — running qual theme taxonomy for the product
```

`research_root` (`/research`) and `benchmarks_root`
(`/research/_benchmarks`) come from `../config/product-context.yaml` —
`study_dir()`/`benchmark_path()` default to those same values, but the
config file is the place to change them, not this file or the scripts.

For every `.md`/`.json` pair above, **the `.json` is canonical** — it's
what the next skill reads and what state/validation logic checks. The
`.md` is the human-readable copy of the same facts, never a place where
additional information lives that the `.json` doesn't have.

Every skill reads what exists before assuming it needs to build it. If
`00-intake.md`/`.json` already answers a question a skill would
otherwise ask the researcher, use it — don't re-ask.

-----

## State

`00-state.json` shape: `study_id`, `state` (one of `routing.STATES`:
`INTAKE`, `SURVEY_DESIGN`, `DATA_READY`, `SYNTHESIS`,
`SYNTHESIS_REVIEW`, `REPORTING`, `REPORT_REVIEW`, `COMPLETE`),
`loopbacks` (`{total, max}`), `artifacts` (artifact name → path),
`validation` (artifact name → `"valid"` or the problem list a
`validate_*` function returned).

**Read/write it through the script, not by hand:**
- `routing.read_state(study_dir_path)` — `None` if the study hasn't
  started tracking state yet (fall back to `detect_entry_point`).
- `routing.next_state(current_state, target_state)` — validates the
  transition against a fixed graph before it happens; raises (naming the
  actually-allowed next states) on an invalid jump, e.g. `INTAKE`
  straight to `REPORTING`. Allowed kickback edges: `SYNTHESIS →
  SURVEY_DESIGN`, `SYNTHESIS_REVIEW → SYNTHESIS`, `REPORT_REVIEW →
  SYNTHESIS`.
- `routing.write_state(study_dir_path, state)` — persists it.

This is deliberately a flat file plus a small fixed graph, not a
workflow engine — its only job is to catch an accidental stage-skip and
to replace re-sniffing files on every turn with reading one file. It
doesn't replace judgment about *when* a stage is actually done; a skill
still decides that before calling `next_state`.

Print this at every handoff so the researcher can see where things stand
(the state block below can be derived directly from `00-state.json`):

```
━━ Research Loop State ━━━━━━━━━━━━━━━━━━━━
Study:         [study-name]
Product:       [product, from intake]
Learning goal: [one line, from intake]
State:         [current STATES value]

Stage:
  ✓ survey-architect    instrument: [X], n required: [Y]
  ● feedback-synthesizer   in progress
  ○ research-reporter      pending

Kickbacks:     [none | count + reason]
Confidence:    [none flagged | LOW — n=X vs required Y]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

-----

## Kickback conditions

A kickback is any point where a downstream skill cannot honestly proceed
without an upstream decision changing.

**feedback-synthesizer → survey-architect:**
Sample size is so far below the required floor that the stated learning
goal genuinely can't be answered (not just "flag and proceed" — that's
the normal small-n handling inside synthesizer itself; this is the
escalated case where the gap is too large to paper over with a wider CI).
Kick back with: current n, required n, and a recommendation (extend
collection window, widen distribution, or accept a narrower claim than
originally scoped).

**feedback-synthesizer → survey-architect (instrument mismatch):**
The data doesn't actually support the learning goal the intake recorded
— e.g., a single NPS item was collected but the real question was about
task-level usability. Kick back with what instrument should have been
used, so the next wave corrects it.

**research-reporter → feedback-synthesizer:**
The synthesis file is missing something the report structure requires
(no severity tiers, no CI on a headline score) — this should be rare if
synthesizer followed its own spec, but the reporter should never
backfill or invent a missing CI/severity itself.

Output format for any kickback:

```
━━ Kickback ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
From:   [skill]
To:     [skill]
Reason: [one sentence]
What changes: [what the upstream skill should do differently this time]
Loop-back count: [N of 2 max]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

-----

## Max loop-backs

**Run `scripts/routing.py`'s `should_escalate_to_researcher(loopback_count)`**
before attempting another loop-back — don't just count in your head.
If it returns `should_escalate=True` (2 loop-backs already used):

> "Two loop-backs on [issue] without resolving it. Here's where things
> stand: [current state]. Options: A — accept the limitation and report
> it as a caveat, B — pause the study and revisit scope. Which do you
> want?"

Don't attempt a third loop-back without the researcher's input.

-----

## Modes

**Gated (default):** pause at each stage transition and each kickback
for confirmation. Use for a new study or an unfamiliar product.

**Fast:** run straight through, noting any kickbacks in the final
summary rather than pausing on them. Opt in with "fast mode" or "just
run it."

-----

## Loop completion block

```
━━ Research Loop Complete ━━━━━━━━━━━━━━━━━
Study:          [study-name]
Product:        [product]
Instrument:     [instrument used]
n:              [final n]  Confidence: [flagged / not flagged]

Headline result: [score + CI, one line]
vs. benchmark:   [trend direction if routing.check_benchmark_comparability
                 says comparable — otherwise "not comparable: <mismatched
                 fields>", waves reported side by side instead of a trend]

Top findings:    [Critical-tier items, one line each]
Kickbacks:       [none | list with reason]

Outputs:
  Internal report: [path]
  Formal report:   [path, if generated]
  Benchmark file:  updated at /research/_benchmarks/<product>.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

-----

## Rules

Priority when rules interact: **STOP** > **MUST NOT** > **MUST** >
**SHOULD** > **MAY** — see `ux-research/README.md` for the full
precedence explanation (that file is the one place it's spelled out;
every skill's Rules section just tags bullets with these keywords).

- **STOP** before a third loop-back — `should_escalate_to_researcher`
  returning `True` means end processing and surface the trade-off
  (options A/B below), not attempt the loop-back anyway.
- **MUST NOT** force standalone feedback (no survey behind it) through
  survey-architect first.
- **MUST NOT** treat a synthesizer small-n flag as an automatic
  kickback — that's normal handling inside synthesizer; only an
  unanswerable-goal gap escalates to a loop kickback.
- **MUST NOT** call `next_state` with a jump the transition graph
  doesn't allow, and MUST NOT advance state without running the
  validator for the artifact that stage produced.
- **MUST NOT** let research-reporter fill in a missing CI or severity
  tier itself instead of kicking back to synthesizer.
- **MUST NOT** imply a benchmark trend when
  `check_benchmark_comparability` reports a mismatch — report the waves
  side by side instead.
- **MUST** write to `/research/_benchmarks/<product>.md` after a
  completed synthesis.
- **SHOULD** skip re-running survey-architect's intake when `00-intake.md`/
  `.json` already answers the same questions.

-----

## Quick reference

| Input | Entry point |
|---|---|
| New research question, no data | survey-architect |
| Raw data, no study folder | feedback-synthesizer (standalone) |
| Raw data, study folder exists | feedback-synthesizer (loaded) |
| Synthesis done, need a writeup | research-reporter |
| Synthesizer: n too low for the goal | Kick back to survey-architect |
| Synthesizer: wrong instrument for the goal | Kick back to survey-architect |
| Reporter: synthesis missing CI/severity | Kick back to feedback-synthesizer |
| 2 kickbacks, still unresolved | Surface to researcher, stop |
| Two waves, measurement conditions differ | Report side by side, not as a trend |
| Loop complete | Completion block, update benchmark file |

## Maintaining this skill

`evals/` is the regression suite. After touching `scripts/routing.py`, run
`python3 -m unittest discover -s evals -v` (CI runs the same). After
touching this file's prose, re-check the cases in
`evals/qualitative_cases.md` by hand.
