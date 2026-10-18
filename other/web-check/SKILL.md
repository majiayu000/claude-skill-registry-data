---
name: "Web: Check"
description: "Run the principles check in wireframe, pass or signoff mode: the mechanical half by script, the judgement half by the web-principles agent, findings into the observation store, blocking until each is fixed or waived; proposes amendments to the principles for approval"
when_to_use: "At the three check moments: after a wireframe is approved, at the end of an observation pass and at sign-off before the walkthrough. Also on demand to check any page against the principles."
model: sonnet
effort: medium
metadata:
  glyph: ᛊ
  family: web
  goblin-spinner: checking the principles|counting callouts|weighing waivers
disable-model-invocation: true
allowed-tools: ["Read", "Glob", "Grep", "Edit", "Bash", "Agent", "AskUserQuestion", "ArtifactData"]
argument-hint: "<wireframe | pass | signoff> [paths: scope document, wireframe, export file, shots directory]"
---

# The principles check

Load `web-conventions` first. The principles and their mechanical or judgement split: `~/.claude/skills/web-conventions/principles.md`. Scripts: `~/.claude/library/scripts/web/check.py` and `observations.py`.

## Step 1: Mode and inputs

The first word of `$ARGUMENTS` is the mode; the rest are paths. Find what is not given from the task's directories (`docs/scope/`, `docs/artefacts/<slug>/`, `docs/assets/walkthrough/`) and say what was used.

| Mode | Needs | Mechanical subcommands |
|---|---|---|
| `wireframe` | the wireframe page(s), the scope document, the product's CSS | `tokens`, `brief` |
| `pass` | the export file, the source directory, the UI library's CSS, `git diff --name-only` for the pass | `export`, `classes` |
| `signoff` | all of the above plus the captures directory, the route list and the device list | `export --max-age 24`, `classes`, `coverage`, `brief` |

The UI library's CSS is under `node_modules/<package>/` for the library named in the inventory; pass the directory.

## Step 2: Mechanical half

Run each subcommand in the table with `--json`; collect the findings. A `2` exit is a missing input: fix the invocation, do not skip the check.

## Step 3: Judgement half

Spawn the `web-principles` agent once with: the mode, the principles file path, every input path and the mechanical findings as JSON. It returns `{findings, amendments}`. Drop any judgement finding that names the same `where` and principle as a mechanical one.

## Step 4: Write the findings to the store

Every finding is an entry: `source: check`, its `principle`, `status: open`, `createdAt` now.

- **A live store exists** (the export file's `artifact` is a URL): `ArtifactData` `batch` of `set` writes to collection `observations`, new doc ids, `seq` continuing from the export's highest. Then re-export with `observations.py export`.
- **No live store** (design mode): `observations.py add <export> --entry <json>` per finding.

Print the findings as one table: principle, where, severity, title.

## Step 5: Verdict

The check blocks until every finding is fixed or waived. Ask Jason per finding, batching up to four in one question: fix now, or waive with a reason. A waiver writes `status: waived` and `resolution: "Waived: <reason>"` to the entry (pinned `update` in the live store, or an edit to the export file). A fix reopens the mode's work: the wireframe in `wireframe` mode, the branch in `pass` and `signoff`; re-run the check after.

No findings, or all waived: print `Principles check: clear (<n> waived)`.

## Step 6: Amendments

For each proposed amendment, show the principle, the change and what prompted it, then ask: approve, reword or decline. An approved amendment edits `principles.md`: the principle's wording, a row in the per-principle table if the split changed, and a row in the amendments table with today's date and the task. Declined ones are not recorded.

## Step 7: Report

Mode, the inputs used, findings by status (fixed, waived, open), amendments approved. In `signoff` mode a clear verdict is what `web-walkthrough` waits for.
