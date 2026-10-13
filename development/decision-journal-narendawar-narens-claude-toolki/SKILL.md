---
name: decision-journal
description: "Use when the user wants to log a prediction or estimate about a dev or project decision, grade past predictions, or see how calibrated they are (for example 'log a prediction', 'grade my predictions', 'how calibrated am I?')."
---

# Decision Journal

## Overview

Keep a log of the user's predictions about dev and project decisions, grade them when outcomes are known, and show where they are overconfident. A script does all the writing and arithmetic so the numbers are always right; you do the conversation. It runs only when the user asks. Never log, grade, or offer to log unprompted: an offhand "this should take a few hours" is not a request.

## The script

`scripts/journal.py` in this skill's directory (use the base directory shown when the skill loads). It needs Python 3 and the standard library only. The log is `~/.claude/decision-journal.jsonl`, one JSON object per line. Commands:

- `python journal.py add --type claim --text "..." --confidence 70 [--know-by YYYY-MM-DD] [--tag a,b]`
- `python journal.py add --type estimate --text "..." --unit hours --estimate 2 [--range-low 1.5 --range-high 4] [--know-by YYYY-MM-DD] [--tag a,b]`
- `python journal.py list [--open | --due]` (prints JSON)
- `python journal.py grade ID --outcome yes|no` or `grade ID --actual NUMBER` [--note "..."] [--force]
- `python journal.py stats [--tag T]`

If a command prints an error, tell the user in one sentence what was wrong and ask for the corrected value. If Python 3 is missing, say so and stop.

## Log a prediction

1. Decide the type. A yes/no judgment ("won't scale") is a claim; a number ("2 hours") is an estimate.
2. Ask only for what is missing: confidence (a whole number from 50 to 99; 70, 70% and 0.7 all mean 70) for a claim; a number and a unit for an estimate. Do not ask for things the user already gave.
3. Once the required fields are known, ask one short line offering the optional extras: an 80% range (estimates), a know-by date, a tag. The user can say "log it" to skip them. Do not run `add` before this, because the script has no edit command, so the extras cannot be added afterwards.
4. Run `add`, then confirm in one line with the id.
5. Never argue the user out of their number. If they ask what you think, give your own view separately and say it was not logged; log only theirs.

## Grade predictions

1. Run `list --due`; if nothing is due, run `list --open`.
2. One entry at a time: restate the prediction and the user's number, and ask what actually happened.
3. Record only what the user tells you in answer to that question. If you saw something in the session that hints at the outcome, mention it and ask them to confirm; never record an outcome from your own inference.
4. If the outcome is ambiguous (partly true, or the claim's wording does not clearly apply), ask one clarifying question before recording.
5. Run `grade`, then show its `result` line (printed only when the grade succeeds; for example "70% claim: it happened" or "2 hours estimated, 3.5 actual: 1.75x"). Never work out the ratio yourself.
6. If `grade` says the entry is already graded, ask whether to overwrite it; use `--force` only after they say yes.

## Review calibration

1. Run `stats` (add `--tag` if the user names an area).
2. Explain it in plain language: where they are overconfident (by confidence bucket and tag), how their estimates run (over or under), and how often actuals land inside their ranges (about 80% is calibrated). Use the script's numbers exactly; never recompute or round them differently.
3. Respect sample size: if the script says there are too few graded entries, or a slice is marked (n<5), say there is not enough data and do not interpret it.
4. Give one concrete suggestion only for a slice with at least 5 graded entries, for example "pad refactor estimates by about 1.5x". Otherwise say there is not enough data yet.

## Edits and deletes

There is no edit or delete command. If the user wants to fix or remove an entry, say so and give the log path (the value of `DECISION_JOURNAL_PATH` if it is set, otherwise `~/.claude/decision-journal.jsonl`; a plain file, one JSON object per line). Never change the file in the same turn as the request: first show which entry you think they mean (id and text; "last" is ambiguous, so say which one you picked) and ask them to confirm. Only after they confirm, make the change yourself, keeping one JSON object per line, and tell them what changed.

## Tone

Neutral and brief. This is bookkeeping, not coaching. Do not lecture about overconfidence or praise good scores.

## Common Mistakes

- Logging, or offering to log, when the user did not ask.
- Asking for details the user already gave.
- Recording an outcome the user did not confirm.
- Recomputing or rephrasing the script's numbers.
- Drawing conclusions from a slice marked (n<5).
- Logging your own number instead of the user's.
- Running `add` before offering the optional extras.
