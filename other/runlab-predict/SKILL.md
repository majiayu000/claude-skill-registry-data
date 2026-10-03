---
name: runlab-predict
description: Predict a race time from the athlete's own data, with an explicit evidence level, a range rather than a single number, and the one measurement that would narrow it most. Use when the user asks "what marathon time can I run", "predict my half", "what should I aim for", or invokes /runlab:runlab-predict. Runs the prediction cascade, so only the user starts it.
allowed-tools: Read, Bash
disable-model-invocation: true
argument-hint: "[distance] [race date]"
---

# runlab race prediction

A prediction without its evidence level is a guess wearing a decimal point. This
skill always delivers three things together: a range, the level of evidence the
range rests on, and what would improve it.

## Run it

Check first that the prediction gate is open — it names what is missing before
you run anything:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" --section computed.gates
```

`computed.gates.race_prediction.missing[]` lists each unmet requirement with
`have`, `need` and `shortfall`. Then:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/predict.py" --distance <metres>
```

Check `--help` before relying on a flag. If the script is absent or its interface
differs from what is written here, say so and stop — a race prediction assembled
by hand is exactly the kind of confident number this plugin exists to prevent.

Useful options, all optional and all improving the answer when known:

| Option | Effect |
|---|---|
| `--date YYYY-MM-DD` | race date. It ages the anchor and reports whether the anchor is still inside the eligibility window on race day. It deliberately does **not** become the cascade's "today": the same value also bounds the volume window behind the prior exponent, and weeks that have not happened yet would be counted as weeks without training |
| `--temperature <c>` | expected race-day temperature; without it, no heat correction is applied and `target_temperature_c` appears under `missing_inputs` |
| `--elevation-up <m>` / `--elevation-down <m>` | course profile; `--elevation <m>` sets both, which is what a loop course means |
| `--races <file>` | official race results as JSON. An activity carries **no race flag** in this data model, so without this file the two strongest anchor levels stay empty and the answer falls back to a training best |
| `--decay <pct/h>` or `--decay-result <id>` | the measured efficiency decay rate. With it the script computes **two** predictions rather than one — see the section below |
| `--json` | the full structure instead of the printed summary |

Standard distances: 5000, 10000, 21097.5, 42195. `--distance` also accepts a unit
(`42.195km`) or a name (`marathon`, `half`, `10k`, `5k`); a bare number below 1000
is read as kilometres, and that reading is stated in the output rather than
assumed silently.

## Read the answer in this order

**1. `ok` and `reason`.** `ok: false` with `reason: no_anchor_candidate` (exit
code 1) means there is no performance in the data that a prediction could be
built on. Say that. Do not substitute a pace from an easy run.

**2. `data_level.code`** — the evidence level, from strongest to weakest:

| Code | What it rests on | Confidence |
|---|---|---|
| `race_anchor` | an official race over 10 km | high |
| `short_race_anchor` | an official 5 km race | moderate |
| `time_trial_anchor` | a clean, hard, uninterrupted effort in training | moderate |
| `training_best_anchor` | the best effort found in ordinary training | low |
| `pace_hr_model_only` | a pace-to-heart-rate model, no hard effort at all | low |

Name the level in the same sentence as the number. A `training_best_anchor`
prediction is a plausible target, not a forecast.

**3. `prediction.is_lower_bound`.** True when the anchor was not a maximal
effort. Then the predicted time is an upper bound on what the athlete would run:
the true time is at most this, and the interval says nothing about how much
faster. Phrase it that way, do not present a two-sided range.

**4. The range, not the median.** Report `p10_hms` to `p90_hms` first and the
median second. A marathon prediction whose 10–90 band spans twenty minutes is an
honest twenty-minute band.

**5. `data_level.missing_inputs`** — every input that was not available. Each one
widens the range, and each one is fixable.

**6. `next_measurement.code`** — the single measurement that would narrow the
range most, with `narrows_range_by_s` and `share_of_range` attached. This is the
most useful sentence in the whole output; end with it.

## The two paths, and why there are two

`paths[]` holds one entry per way of getting the distance exponent, and
`comparison` holds the difference between them in seconds and percent. Report
both. They exist because the cascade's own priority — a measured decay rate beats
the prior table — is not neutral:

- **`measured_decay`** integrates a *linear* speed decay. A rate measured over a
  half marathon, continued over a marathon, credits the runner with a late-race
  fade that no runner has, so this path runs fast.
- **`prior_table`** encodes the opposite belief: a runner whose long-run habit
  does not reach the target distance fades harder than any shorter measurement
  shows. It is a rule of thumb, not a measurement of this athlete.

On the reference dataset the two land about fifteen minutes apart over a
marathon. Nothing in a dataset without a race at the target distance decides
between them, so say both numbers and say why they differ. Do not average them,
and do not quietly report the faster one.

`extrapolation.warn` is true when the target takes more than
`extrapolation.warn_above` times as long as the anchor did (`extrapolation.ratio`
says how far). A half marathon anchor for a marathon sits near 2.2; a 35-minute
training best for a marathon sits near 8, and at that point the exponent, not the
anchor, is doing nearly all the work. When the warning is set, name the ratio.

## Things that are true about this model and worth saying

- **No race bonus is applied by default.** "You always race faster than you
  train" is a claim about a specific athlete. It enters only after it has been
  observed twice and written into the calibration file.
- **The distance exponent** comes either from the athlete's own two races, from
  their measured efficiency decay, or from a prior table. Check
  `exponent.source`; when it is `prior_table`, the confidence is capped at
  moderate no matter how good the anchor was.
- **Heat and elevation are corrections, not decorations.** Applied only when the
  target conditions were supplied; `conditions.temperature.applied` says whether
  they were.
- **The platform's own prediction is not evidence.** If the athlete quotes one
  from a training site, treat it as a second opinion with an unknown method, and
  compare rather than defer.

## Do not

- Do not average this prediction with another one to look confident, and do not
  average the two exponent paths with each other.
- Do not convert the range into a single number "for simplicity". The range is
  the result.
- Do not write the prediction into the state database. It is derived from data
  that changes with every run; a stored prediction goes stale silently. Findings
  about *how* the athlete decays belong in the database, the predicted time does
  not.
