---
name: runlab-run
description: Analyse one run — pacing, efficiency decay, decoupling, mechanics, and how it compares with the athlete's own history at the same pace. Use when the user asks "how was today's run", "analyse my long run", "what happened at kilometre 30", or invokes /runlab:runlab-run. Runs scripts and can propose a state update, so only the user starts it.
allowed-tools: Read, Write, Bash
disable-model-invocation: true
argument-hint: "[activity-id or date]"
---

# runlab single run

One run is a small sample. Everything this skill says has to survive that fact.

## Standing rule

Run every script through the shim, and check `--help` before relying on a flag.
If a script is absent or its interface differs from what is written here, say so
and stop. Never compute the number yourself.

## Step 1 — identify the run

If the user named a date or "today", resolve it to an activity id:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" --section computed.activities
```

`read-db.py` always prints JSON — there is no `--json` flag. Ids are
adapter-scoped and stable, for example `runalyze:900000001` or `fit:9c1e...`. If
two activities match one date, ask which; do not pick the longer one.

Check `computed.gates` in the same call when the question needs a comparison:
a gate with a non-empty `missing[]` tells you the answer before you run anything,
and it gives the `shortfall` to quote.

## Step 2 — run the analysis

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/analyze.py" run --activity <id>
```

Individual tools, when the question is narrower:

| Tool | Question it answers |
|---|---|
| `decay` | Does the efficiency index fall over moving time, and how fast in %/h? |
| `pacing` | Start pattern, variability, negative split, stop time |
| `compare` | How does this run sit against the athlete's own runs at the same pace? |
| `mechanics` | Ground contact, vertical oscillation, step length, and their coverage |
| `week` | The week this run belongs to: volume, load, monotony, ramp |
| `patterns` | How often each catalogue pattern occurs across many runs |
| `history` | The whole history: eras, pace and efficiency trends, durability |
| `eras` | Where the training eras begin and end, and why |

`run`, `decay`, `compare`, `mechanics` and `pacing` take the activity; `patterns`,
`week`, `history` and `eras` take a period instead. Each writes
`cache/results/<result_id>.json` and prints the id. Quote the id when you state
one of its numbers.

The output is JSON on stdout and nothing else. `metrics` and `coverage` are
exactly what the file named by `result_id` contains; anything else the tool
computed is under `detail`, beside the id in `result_ids` that vouches for it.
So cite the id that actually holds the number, not the one printed last.

## Step 3 — read the result correctly

- **`verdict.code`** is the machine answer: `insufficient_data`,
  `not_applicable`, `inconclusive`, `within_expected`, `above_expected`,
  `below_expected`, `improving`, `worsening`, `stable`, `confirmed`, `refuted`.
  `insufficient_data` is a real answer and is reported as one, with the `n` that
  was available and the `n` that would be needed.
- **`coverage`** decides how much weight a mean carries. A ground contact mean
  over 40 % of samples and one over 96 % are not the same measurement, and the
  difference is never averaged away.
- **The remainder block.** Decay is computed in five-minute blocks from minute
  ten of moving time. The final short block is reported separately because it
  can move the figure by a wide margin — a walk at the end is not a decay of
  running economy. State both numbers or neither.
- **Moving time, not elapsed time.** Pace is computed on moving time. If
  `stop_time_excess` shows up, the athlete's watch average and this analysis
  will disagree, and the reason is worth one sentence.
- **Comparison needs a base.** `compare` returns
  `verdict: insufficient_data` when too few neighbouring blocks exist. That is
  not a bad run, it is a young database.

## Step 4 — what to say

Three parts, in this order:

1. What the run was: distance, moving time, pace, heart rate — all from the
   result file.
2. What is unusual about it, if anything, with the comparison that makes it
   unusual and the `n` of that comparison.
3. What follows for the next session — or explicitly nothing. "This run gives no
   reason to change anything" is a complete and often correct answer.

## Step 5 — offer to record a pattern

Only if the run shows something a single run can show: a pattern occurrence, not
a finding about the athlete. Patterns use the closed catalogue (`zone3_excess`,
`start_too_fast`, `cadence_below_target`, ...); an unknown id is rejected by the
validator with the valid list.

Propose the payload, show it, dry-run it, then write:

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/update-db.py" \
  --payload-file payload.json --dry-run
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/update-db.py" \
  --payload-file payload.json
```

The payload also goes in on stdin when you have no file to spare. It holds no
numbers: it cites `result_id` and `metric_keys`, and the writer copies the values
out of the result file. See `/runlab:runlab-methodology`.

## Do not

- Do not turn one run into a trend. A single run cannot establish a pattern; it
  can only be an observation of one.
- Do not attribute a slow run to fatigue, heat or sleep unless a result file
  actually tested it. "It was warm" is a hypothesis, and it belongs in the
  hypothesis wording.
- Do not write into `state/` with Write or Edit. The hook blocks it, and the
  block is the point.
