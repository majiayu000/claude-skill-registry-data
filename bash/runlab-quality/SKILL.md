---
name: runlab-quality
description: Check whether the running data is arriving cleanly — which channels the watch and the source actually deliver, sample coverage per run, pauses, duplicates, gaps and unit oddities. Use when the user says "my run looks wrong", "is my watch recording running dynamics", "why is this pace off", "did the import work", or invokes /runlab:runlab-quality. Read-only, so it is safe to trigger automatically.
allowed-tools: Read, Bash
---

# runlab data quality

The question this answers is "does my data arrive complete and correct", and it
is the right first question whenever something looks strange. A form analysis on
a channel that was never recorded produces a confident wrong answer.

## Run it

Two commands, in this order. The first checks the installation and the source,
the second checks what the data itself looks like.

```
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/doctor.py" --json
bash "${CLAUDE_PLUGIN_ROOT}/.claude/hooks/rl-python.sh" "${CLAUDE_PLUGIN_ROOT}/scripts/read-db.py" \
  --section computed.data_quality --section computed.activities --section problems
```

`doctor.py` takes `--root <dir>`, `--offline` (skip every network check),
`--strict` (warnings become blocking) and `--json`. It returns `ok`, `n_checks`,
`counts`, `checks[]` and `blocking[]`.

`read-db.py` always prints JSON and needs no `--json` flag.

Both are read-only. They open files, count samples and report; they change
nothing.

## What the answer contains, and how to read it

**Channels present versus channels expected.** A channel that was never recorded
is absent from the stream dict entirely; a channel that was recorded with gaps
has `None` inside its list. These two mean different things and must never be
conflated. "Your watch does not record ground contact" and "your watch recorded
ground contact for 41 % of this run" call for different responses.

**Coverage per channel.** `computed.data_quality.channels` gives every channel
its `fields`, its `n`, its `n_total` and the resulting `coverage`. Report `n` of
`n_total`, not just "present". Below roughly half, a mean over that channel is a
statement about the half that was recorded. Note the block's own `scope` and
`sample_level`: at read time this is computed from activity summaries, not from
the samples, and it says so.

**State health.** `problems[]` lists state files that failed validation. A
broken state file blocks everything downstream, so report it before anything
about the running itself.

**Pauses and stop time.** A sample belongs to a pause when speed stays below the
configured threshold for at least the configured duration. Moving time excludes
pauses; elapsed time does not. When the two diverge, the watch's average pace and
every runlab pace disagree, and that is the explanation, not an error.

**Sport normalisation.** Sources report the sport in the account's own language.
Adapters normalise it. If runs are missing from the cache while the source shows
them, a locale string that failed to normalise is the first suspect — and it
produces a silently empty result, not an error message.

**Duplicates.** One workout can arrive from two devices. Ids are derived from
content, not from filenames, so re-imports and renames collapse; two genuinely
different recordings of the same session do not.

**Unmaterialised cloud files.** FIT files in a synced folder can be placeholders.
Opening one triggers a download and can hang, so they are skipped and counted.
The count is part of the answer.

**Temperature.** Some devices never record ambient temperature. That is a
capability of the hardware, not a fault, and it disables heat-related analyses
for good.

## What to answer

1. What is complete.
2. What is missing, with the number of affected runs out of the total.
3. Whether the cause is the device, the source tier, or the import — the report
   distinguishes these, so do not guess.
4. What the athlete can actually do about it, if anything. Sometimes the honest
   answer is that this watch cannot deliver this channel.

## Do not

- Do not repair, interpolate or smooth anything, and do not suggest that runlab
  will. Repairs belong in the analysis layer where they can be switched off and
  tested, never in the reading of the data.
- Do not treat a low coverage figure as a training finding. It is a measurement
  finding.
- Do not write anything. This skill has no writing path.
