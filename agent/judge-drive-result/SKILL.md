---
name: judge-drive-result
description: Check a finished drive's result against what the drive promised, and give a pass or reject verdict with a reason for every criterion. It holds the drive checker's rules, its prompt and its verdict shape — the one source for them, used by both kinds of checker (a sub-agent on a different model, or a different coding agent such as Codex). The checker is handed only a bundle of the drive's outputs (the change it made, its plays' review records, the answers and where each came from, the decision-trace check, each play's done check) and the drive's own criteria; never the drive's reasoning. Use when a drive reaches its checker step (Shared Drive Run, R6).
user-invocable: false
model: sonnet
allowed-tools: Read, Write, Glob, Grep
---

# judge-drive-result

A drive runs plays until its intent is met (ADR 029). Each play proves its own done check; the
stop condition proves the drive's files exist. Neither says whether the result is *right*. The
checker does: a model or agent that is not the one that ran the drive reads what the drive made
and judges it against what the drive promised. This skill is the one source for how it judges.

## Input

The bundle — and nothing else: a folder `prepare_check.py` built (`<working>/check/`). Read
only the files in it:

| File | What it holds |
|------|---------------|
| `criteria.md` | The drive's goal (`G`), its constraints (`C1`…) and its Done means (`D1`…), from its ICE. The criteria to judge. |
| `manifest.json` | `criteria_ids` (every id you must judge), the issue, the base, and the list of files. |
| `change.diff` | The change the drive made, from the base to now, without its own run records. |
| `review/` | Each play's review record for the drive's end (what the play would have shown at its checkpoint). |
| `answers.json`, `answers-sources.json` | The answers gathered first, and where each came from (`person`, or `memory` with tier, path and trace). |
| `traces.json` | The memory tool's decision-trace check (`citations --check`): every decision and its source, and `problems` — a source gone or changed. Clean means `problems` is empty. |
| `done/` | Each play's done check (`<play>-done.json`). |

Do not open anything outside the bundle, and do not ask for the drive's reasoning. If the
bundle lacks something a criterion needs, that criterion fails for want of evidence.

## Process

1. Read `criteria.md` and `manifest.json`. Judge every id in `criteria_ids` — no more, no less.
2. For each criterion, look for evidence in the bundle that it holds. Evidence is a file and
   what it shows: a line of the diff, a review record, a trace. Write it so a person can find
   it ("change.diff: adds `product/…/capability.md` with its agent intent section").
3. Mark it `pass` only when the evidence shows it holds. Mark it `fail` when the evidence shows
   it does not, or when no evidence shows it does. A plausible guess is a fail.
4. Rules every drive is held to, whatever its criteria say:
   - **Nothing from the model alone** (ADR 034): every answer in `answers-sources.json` comes
     from `person` or `memory`; every decision in `traces.json` has a trace; and `traces.json`
     lists **no problems** (its `problems` list is empty). Its `ok: true` only says the check
     ran — it is `true` even when problems are listed. A criterion about answers or decisions
     fails when this does not hold.
   - **Every play proved done**: each file in `done/` reads `done: true`.
   - **One issue**: the change touches no other issue's run records.
5. The verdict is `pass` only when every criterion passes. Otherwise `reject`, and `reasons`
   names each failed criterion in one plain sentence — what is missing or wrong, and where.

## Output

JSON, exactly this shape (`verdict.schema.json` beside this file is its schema):

```json
{
  "verdict": "pass",
  "criteria": [
    {"id": "G",  "result": "pass", "evidence": "review/vision-….md: seeds the ecommerce domain …"},
    {"id": "C1", "result": "pass", "evidence": "change.diff: every run file is under issues/7/"}
  ],
  "reasons": []
}
```

- `verdict`: `pass` or `reject`.
- `criteria`: one entry per id in `criteria_ids`, each `pass` or `fail`, each with evidence.
- `reasons`: empty for a pass; one sentence per failed criterion for a reject.

A sub-agent checker writes this JSON to the `verdict` path its contract names. A coding-agent
checker returns it as its final message (the runner saves it). `record_check.py` then checks the
shape and writes the drive's `check.yaml`; a verdict that does not match is never a pass.

## Rules

- Judge only from the bundle. Never from what a drive "probably" did.
- Never fix anything, and never write anywhere but the verdict path.
- No evidence, no pass.
