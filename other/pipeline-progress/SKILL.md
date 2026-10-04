---
name: pipeline-progress
description: Manage durable multi-step Story-Film pipeline progress, Pi todo rendering, checkpoints, pause/resume, blockers, selective retry, and session handoff without relying on chat history.
author: Alan Guice (Badgids)
license: Apache-2.0
compatibility: Standalone file workflow. Optional Pi extension adds the interactive todo viewport.
---

# Pipeline Progress

Use this skill whenever a Story-Film playbook contains multiple ordered steps.

## Authority

`00_project/pipeline_progress.json` is the authoritative execution-progress ledger.

The Pi todo widget is only a renderer of that ledger. It must never invent progress, estimate counts, or mark work complete on its own.

Creative truth remains in canon, state, approved artifacts, dependency records, and media registries. Progress does not replace those systems.

## Start or resume

1. If `pipeline_progress.json` is `inactive` or the previous pipeline is `complete`, initialize the selected playbook:

```bash
python scripts/pipeline_progress.py init <project-root> --playbook <playbook-name>
```

2. If an active, paused, or blocked ledger already exists for the requested work, read it and resume the recorded current target instead of rebuilding the plan from chat history.
3. Read `00_project/HANDOFF.md` after a restart or compaction, but treat the JSON ledger as authoritative if the two disagree.

## Checkpoint rule

Do not work ahead. The current leaf in `pipeline_progress.json` is a hard execution boundary. Do not start a later Story-Film specialist, write its artifact, or mark a generic Pi Todo ahead until the current leaf is complete.

After each actionable leaf step/substep:

1. perform the work
2. validate the relevant artifact
3. checkpoint only after validation succeeds
4. include changed files when practical
5. let the checkpoint advance to the next pending leaf
6. reread the progress ledger before starting that new target

If Pi also has a generic Todo tool, use it only as a small mirror. Keep at most three Story-Film items there: the current target, the immediate next target, and the requested endpoint. Update that mirror immediately after each Story-Film checkpoint. Never duplicate the complete Story-Film playbook into Pi's generic Todo. When the host exposes a compatible generic Todo initialization tool, the Story-Film extension blocks a new mirrored list with more than three items.

Example:

```bash
python scripts/pipeline_progress.py checkpoint <project-root> \
  --status completed \
  --last-action "Approved the scene outline" \
  --file 01_story/scene_outline.md
```

A blocking validation failure must not advance:

```bash
python scripts/pipeline_progress.py checkpoint <project-root> \
  --status blocked \
  --blocker "SCN-014 references an unknown location ID" \
  --next "Repair SCN-014 and rerun project validation"
```

After correction:

```bash
python scripts/pipeline_progress.py resume <project-root>
```

Then validate and checkpoint the same target.

## Conditional steps

Use `skipped` only when a conditional playbook step genuinely does not apply. A skip requires a reason:

```bash
python scripts/pipeline_progress.py checkpoint <project-root> \
  --status skipped \
  --note "No social campaign was requested"
```

Never skip work merely because it is difficult or a runtime is unavailable. Runtime absence is a blocker when the requested endpoint requires that runtime.

## Pause and resume

Pause only when the user intentionally pauses work or a human approval boundary requires it:

```bash
python scripts/pipeline_progress.py pause <project-root> --note "Waiting for user selection of TAKE-004 or TAKE-006"
```

Resume from the same target:

```bash
python scripts/pipeline_progress.py resume <project-root>
```

## Selective retry

Use reset for a bounded execution retry:

```bash
python scripts/pipeline_progress.py reset <project-root> PST-006.STEP-SCENE-TO-SHOTS-03 \
  --note "Retry only the failed shot-list step"
```

Resetting progress does not restore creative files or infer dependency impact. If an approved artifact changes, run `project-impact` separately and invalidate only its actual downstream dependency slice.

## Pi UI

When the optional Pi extension is installed, it displays stage, step, and substep state above the editor and follows the current item automatically.

The Story-Film viewport starts in compact mode with three visible pipeline rows. Expanded mode shows ten rows. Both modes can scroll and follow the real current target.

Controls:

- `/story-todo status`
- `/story-todo toggle|expand|collapse`
- `/story-todo up|down`
- `/story-todo page-up|page-down`
- `/story-todo current`
- `/story-todo help|keys`
- `Ctrl+Alt+End` toggles compact/expanded Story-Film Todo
- `Ctrl+Alt+Up/Down`
- `Ctrl+Alt+PageUp/PageDown`
- `Ctrl+Alt+Home`

Markers:

- `✓` completed
- `▶` current
- `!` blocked
- `○` pending
- `-` skipped

## Done

Pipeline execution is done when every applicable leaf is completed or explicitly skipped, no required blocker remains, and the requested endpoint has passed its normal Story-Film validation gates.

## Resource-handoff status

`00_project/resource_handoff.json` is a separate deterministic runtime-status channel for exclusive local-LLM/ComfyUI handoffs. The Pi extension may render it beside the Todo and emit phase-change notifications without calling an LLM. It never replaces `pipeline_progress.json` as the pipeline cursor, and the resource runner must not checkpoint creative work on its own.
