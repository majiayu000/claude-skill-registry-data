---
name: contract-accuracy
description: "Read-only inspector for the contract-critic accuracy-skip system. Prints the per-area clean_streak, skip_eligible flag, and recent history. Use when: user says /contract-accuracy, 'show accuracy', 'which areas can skip critic', 'why did /design-first skip the critic on X', or wants to audit the system before tuning area-mapping.json."
user_invocable: true
---

# /contract-accuracy — Inspect the Critic-Skip Accuracy State

When this skill is invoked, print the contents of `.claude/contract-accuracy.json` in a human-readable table and answer follow-up questions about why a given contract was or wasn't skipped.

This skill **never writes**. To mutate state use `accuracy_update.py` directly (or trust the hooks).

## Step 1: Dump the table

Run:

```bash
py -3 .claude/scripts/accuracy_update.py dump-table
```

If the output is `[]`, the state file is empty — no areas have been tracked yet. This is normal on a fresh install; tell the user that the system is in cold-start mode and the critic will run for every contract until each area accumulates 5 clean verdicts.

## Step 2: Format the output for the user

Render the JSON output as a Markdown table with columns: **area** · **streak** · **eligible** · **total** · **last verdict** · **last updated**. Sort by `clean_streak` descending so the closest-to-skip areas appear first.

For each `skip_eligible: true` row, prefix the area with a checkmark (`x`). For rows with `last_verdict` starting with `failed:`, prefix with `!` and append the failure source in parentheses.

## Step 3 (optional): Per-contract trace

If the user asks "why was/wasn't <contract-path> skipped?", run:

```bash
py -3 .claude/scripts/derive_area.py "<contract-path>"
```

For each derived area, run `py -3 .claude/scripts/accuracy_update.py query <area>` and print:

- The area's `clean_streak` vs the threshold (5)
- Whether `skip_eligible` is true
- The last 5 entries from `history` (verdict, source, contract)

Then state the answer: skip would engage iff ALL derived areas have `skip_eligible: true` AND no area has `mandated_remaining > 0` (when that field exists in a future schema version).

## Step 4: Surface tuning hints

If the table is empty, suggest the user run `/design-first` against a small change to start populating it.

If many areas show `last_verdict: failed:critic-warnings-only` clustering on a single contract, suggest the user inspect `area-mapping.json` — patterns may be too broad and pulling in unrelated areas.

If a single area is at `clean_streak: 4` for many days, suggest the user run `/design-first` on a small fixture in that area to push it to 5/5.

## What this skill does NOT do

- Does NOT modify `contract-accuracy.json`, `critic-runs-seen.json`, `contract-status-cache.json`, or `journal-entries-seen.json`.
- Does NOT spawn `contract-critic` (that's `/critique-now`).
- Does NOT delete or reset accuracy state. If the user wants a reset, instruct them to delete `.claude/contract-accuracy.json` manually — this is a deliberate friction point.

## Bypass note for `/design-first`

If the user wants to override the skip system without permanently changing state, mention the escape hatch:

```bash
$env:CLAUDE_CONTRACT_SKIP = "off"
```

`/design-first` Step 2.5 honors this env var and forces the critic to run regardless of `skip_eligible`.
