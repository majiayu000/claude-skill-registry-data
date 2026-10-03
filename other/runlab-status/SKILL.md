---
name: runlab-status
description: Short read-only situation report from the local running database — last run, data quality, open patterns, due tests, anchor quality, and which analyses are unlocked. Use when the user asks "where do I stand", "what does runlab know", "how is my week going", "any open issues", or invokes /runlab:runlab-status. Reads local files only and writes nothing, so it is safe to trigger automatically.
allowed-tools: Read, Bash
---

# runlab status

The cheap answer to "where do I stand". Read-only: no file is written, no
analysis runs over the full history, and it takes well under a second.

## Run it

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" --section computed
```

`read-db.py` always prints JSON. `--section` is repeatable and takes a dotted
path; `--list-sections` prints every path available. Use `--root <dir>` only when
the athlete has more than one project.

Exit code `2` means no data root was found. Then say runlab is not set up in this
project and mention `/runlab:runlab-setup` — do not go looking for running data
elsewhere on the machine.

## What to report

Everything is derived on read. Never read a derived value out of a state file: a
materialised cache goes stale and then lies with authority.

| Field | Say it as |
|---|---|
| `computed.activities.days_since_last`, `.n_running`, `.span_days` | when the last run was, how much history there is |
| `computed.activities.index.age_days` | how old the cache is; above a week, say so before interpreting anything |
| `computed.patterns_open.n_open` and `.items[]` | id, occurrence count, last seen |
| `computed.tests_due.n_due`, `.n_overdue`, `.items[].days_overdue` | which field test is overdue and by how long |
| `computed.anchors.anchors[].requires_uncertainty` / `.zone_statement_allowed` | which anchors are soft, and what that forbids |
| `computed.data_quality.channels[]` | coverage per channel as `n` of `n_total` |
| `computed.comparison_base` | `verdict` plus `runs_for_spread.shortfall` when comparison is not yet possible |
| `computed.gates` | which analyses are unlocked and what the locked ones are short of |
| `problems[]` | a state file that failed validation — report it first, it blocks everything |

Keep it to a handful of lines. This skill is the glance, not the analysis.

## Rules that apply even here

- **A pattern seen four or more times and still open is not a note.** Say what it
  is costing and propose the counter-measure stored with it. Listing it flatly
  among the others is not enough.
- **`zone_statement_allowed: false` is binding.** No sentence names a zone while
  that flag is false, unless it also says the boundary is provisional.
- **`comparison_base.verdict: insufficient_data` blocks comparison, not
  description.** Say how many runs are still needed — the number is in
  `runs_for_spread.shortfall`.
- **A shortfall is a number, not an adjective.** "Three more weeks with runs",
  never "a bit more data".

## Do not

- Do not run analyses from here. If the user wants a number that is not in
  `computed`, point at `/runlab:runlab-run` or `/runlab:runlab-report`.
- Do not propose a state update. This skill has no writing path at all.
- Do not fill an absent field with an estimate. An absent field is reported as
  absent, with the reason the block gives.
