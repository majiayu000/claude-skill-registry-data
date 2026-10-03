---
name: runlab-methodology
description: The evidence rules for every runlab statement — what a given sample size supports, when a finding counts as established, why null results get their own card, and the exact payload update-db.py accepts. Use whenever a running finding, correlation, pattern or race prediction is about to be stated, when a number needs a source, or when writing to the runlab state database. Text only, no tools, no side effects.
---

# runlab methodology

Standing rules for the rest of this session. They apply to every runlab answer,
not only to the skill that loaded them.

## 1. The division of labour

The script decides every number. The model decides what the numbers mean.

| The script owns | The model owns |
|---|---|
| pace, efficiency index, drift, decoupling, decay | the claim sentence and the reasoning |
| `n`, `p`, `r`, `r²`, slopes, confidence intervals | assigning an observation to a catalogue pattern |
| block medians, neighbour differences, z-scores, ranks | proposed status, priority, what to discuss today |
| load, ramp ratio, monotony, zone shares | counter-measures, in prose |
| era boundaries, calibration constants | the narrative around all of it |
| every verdict code | which finding is worth recording |

A number you cannot point to in a result file does not go into an answer. If you
want to state one, run the analysis that produces it.

## 2. Evidence grades

| Grade | Condition | How to phrase it |
|---|---|---|
| `established` | p < 0.01 and the effect survives era control | plain statement, with effect size, `n` and `p` |
| `provisional` | 0.01 ≤ p < 0.05 | statement plus the sensitivity: what would have to be true for it to vanish |
| `hypothesis` | p ≥ 0.05, or too few observations | not a finding. Goes in the hypothesis section with a test protocol naming the observable that would decide it |
| `no effect` | tested, and the effect is absent within the resolution of the data | its own card, grey, with an explicit "no action needed" target line |

Three constraints on top:

- **Every target value names its origin.** Either the athlete's own data or a
  named literature reference. A target with no stated origin is a preference.
- **Every extrapolation is named** in the limits paragraph of the document that
  uses it.
- **A verdict of `insufficient_data` is a result.** Report it with the `n`
  available and the `n` that would be needed, never as silence.

## 3. What a sample size supports

- **n = 1.** One run is an observation. It can instantiate a pattern; it cannot
  establish anything about the athlete. No trend, no cause, no correlation.
- **n < 3 occurrences.** Not yet a pattern. Say "seen twice", not "recurring".
- **n ≥ 4 occurrences with status `open`.** No longer a note. Say what it costs
  and propose the counter-measure stored with it.
- **Correlations.** Report `r`, `n` and `p` together or not at all. Under roughly
  twenty paired observations, report but do not act.
- **Coverage before mean.** A mean over a channel present in 40 % of samples is
  a statement about those 40 %. Report the coverage next to the mean, always.

## 4. The three traps this domain sets

1. **The calendar confounder.** Any correlation measured across many months may
   be a proxy for training state: cold runs cluster in the untrained season, hot
   runs in the peak. Control for the training era before believing a seasonal
   effect. A correlation that changes sign under era control was never an effect.
2. **The remainder block.** Decay is computed in blocks from minute ten of moving
   time; the final short block is reported separately because it can move the
   figure by a wide margin. A walk at the end is not a collapse of running
   economy. Quote both numbers or neither.
3. **Stop time.** Pace is computed on moving time. When elapsed time exceeds
   moving time noticeably, the watch average and every runlab number disagree,
   and the reason is the pauses, not an error.

## 5. Soft anchors

Anchor qualities: `measured`, `estimated`, `working_value`, `literature`,
`lower_bound`.

If an anchor a statement depends on is anything other than `measured`, the
uncertainty is stated in the same sentence. "You spent 40 minutes in zone 2" is
false advertising when the zone boundary is a `working_value`; "in the band we
are currently treating as zone 2, which is a provisional boundary" is honest and
just as short.

`lower_bound` is the trickiest: it means the true value is at least this. Never
present it as a maximum reached.

## 6. The update payload

State is written by one script and no other path. Validate first, then write:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/update-db.py" \
  --payload-file payload.json --dry-run
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/update-db.py" \
  --payload-file payload.json
```

The payload can also arrive on stdin. `--dry-run` validates and resolves every
citation without writing a byte; `--root <dir>` selects the project when more
than one exists.

Exit codes: `0` written, `1` rejected with the errors listed and **no file
touched**, `2` I/O failure. A rejected payload never leaves a half-written state.

**The payload contains no numbers.** Not one, anywhere, except
`schema_version`. Every value is copied by the writer out of the result file you
cite. This is why an invented p-value cannot reach the database: the path does
not exist.

```json
{
  "schema_version": 1,
  "session_id": "s-2026-08-18-1",
  "patterns": [
    {"id": "zone3_excess",
     "activity_id": "runalyze:900000001",
     "status": "open",
     "result_id": "20260818-1032-pacing-900000001",
     "metric_keys": ["mid_zone_share"],
     "note": "Third long run in a row above the intended easy band."}
  ],
  "findings": [
    {"statement": "Cadence at easy pace sits below the configured target.",
     "result_id": "20260818-1033-mechanics-900000001",
     "metric_keys": ["cadence_mean_spm", "p", "n"],
     "pattern_id": "cadence_below_target",
     "verdict": "confirmed",
     "status": "open"}
  ],
  "calibration": [
    {"key": "hr_lt2_bpm", "quality": "measured",
     "result_id": "20260818-1101-test-lt2",
     "metric_key": "threshold_hr_bpm",
     "measured_at": "2026-08-18T11:01:00+02:00"}
  ],
  "tests": [
    {"kind": "lt2_field_test", "status": "completed",
     "test_id": "test-lt2-a", "result_id": "20260818-1101-test-lt2"}
  ],
  "log": [
    {"kind": "analysis", "text": "Long run reviewed; decay within the usual band.",
     "result_ids": ["20260818-1032-pacing-900000001"]}
  ],
  "plan": [
    {"action": "adjust", "block_id": "w-34", "effective_from": "2026-08-19",
     "note": "Cap the long run by heart rate rather than pace."}
  ]
}
```

Field rules:

| Section | Required | Optional | Closed vocabulary |
|---|---|---|---|
| `patterns` | `id` | `activity_id`, `status`, `note`, `result_id`, `metric_keys`, `first_seen`, `last_seen` | `id` from the pattern catalogue; `status` |
| `findings` | `statement`, `result_id` | `finding_id`, `pattern_id`, `metric_keys`, `verdict`, `status`, `note`, `subject`, `created_at` | `verdict`, `status`, `pattern_id` |
| `calibration` | `key`, `quality` | `result_id`, `metric_key`, `measured_at`, `source`, `note` | `quality` |
| `tests` | `kind`, `status` | `test_id`, `scheduled_for`, `result_id`, `target`, `note` | `status` |
| `log` | `kind`, `text` | `entry_id`, `result_ids`, `created_at`, `tags` | — |
| `plan` | `action` | `block_id`, `effective_from`, `result_id`, `note` | — |

Vocabularies:

- **status** (patterns, findings): `open`, `watching`, `confirmed`, `resolved`,
  `dismissed`, `superseded`
- **test status**: `planned`, `scheduled`, `completed`, `aborted`, `invalid`
- **verdict**: `insufficient_data`, `not_applicable`, `inconclusive`,
  `within_expected`, `above_expected`, `below_expected`, `improving`,
  `worsening`, `stable`, `confirmed`, `refuted`
- **quality**: `measured`, `estimated`, `working_value`, `literature`,
  `lower_bound`
- **pattern ids** come from the catalogue in `scripts/rl/schema.py`. An unknown
  id is rejected with the valid list attached. Genuinely new patterns are
  declared first in `profile.custom_patterns`; they are not invented in a
  payload.

`result_id` has the form `YYYYmmdd-HHMM-<tool>-<subject>` and must already exist
under `cache/results/`. If it does not, or if it does not contain the metric you
cited, the write is rejected.

## 7. Refuted findings are kept

A finding that turned out to be wrong stays in the database with **status**
`dismissed` (or `superseded`, when something replaced it) and a **verdict** of
`refuted`, plus the reason it fell. The two vocabularies are separate and the
writer enforces both: `refuted` is a verdict, never a status, and putting it in
the status field is rejected with the valid list attached. Deleting the finding
guarantees someone rediscovers it in six months and believes it. The record of
what was tested and did not hold is worth as much as the record of what did.

## 8. Rules that fire on a field

Each of these is a condition on stored data, not a preference. Check the field,
then behave.

| Condition | Behaviour |
|---|---|
| `profile.anchors.<key>.value is None` | Do not fill it in. Name the analysis it blocks and the field test that would produce it. |
| `profile.zones` is empty | Do not name zones at all. Use measured paces and heart rates. |
| `patterns.<id>.status == "resolved"` and it reappears | Say it has come back after being resolved. A recurrence after a fix carries more information than a first sighting. |
| `findings.<id>.status in ("dismissed", "superseded")`, or `findings.<id>.verdict.code == "refuted"` | Do not resurrect it as new. If fresh data revives the question, say it was tested before and why it fell. |
| `tests[].scheduled_for` has passed and status is `planned` or `scheduled` | Report it as overdue, with the number of days, until it is completed or dropped. |
| A temperature correction is being considered | Apply none. `compare.hr_comparison` corrects only when handed `calibration["temperature"]["correction_allowed"] = true`, and nothing in 0.1.0 sets it — so the correction is off, always. Report the uncorrected difference plus the sensitivity span the module returns beside it. |
| `computed.comparison_base.verdict == "insufficient_data"` | Do not compare a run against the athlete's own history at all. Quote `runs_for_spread.shortfall` as the number still missing. |
| `computed.anchors.anchors.<key>.zone_statement_allowed == false` | No sentence names a zone unless it also says the boundary is provisional. |
| `computed.gates.<analysis>.missing` is non-empty | That analysis is not available. Quote the `shortfall` with its `unit` — "three more weeks with runs" — never "not enough data". |
| `computed.activities.index.age_days > 7` | Say so before interpreting anything. A stale cache produces a confident report about a fortnight ago. |

## 9. Never

- Never write `state/`, `profile.json` or `cache/results/` with Write or Edit. A
  PreToolUse hook blocks it; the block is the mechanism that makes "the model
  does not write numbers" a fact rather than an instruction.
- Never carry a number from an earlier session's conversation. Cite the result
  file, or run the analysis again.
- Never present a plausible mechanism as a measured one. "Probably the heat" is
  a hypothesis and gets hypothesis wording.
- Never give medical advice. Values from consumer sensors are estimates; pain,
  illness and injury belong to a doctor.
