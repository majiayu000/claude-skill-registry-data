---
name: aiwf-atlas-cartographer
description: Local Atlas/cartographer continuity capture and retrieval for Codex handoffs, chat compaction, deleted-chat recovery, durable local task state, Atlas-style cards, lanes, source pointers, continuity manifests, and local indexed memory. Use when the prompt mentions cartographer, atlas/cartographer, cards and lanes, compressing or compacting chat, preserve context locally, resume later, handoff state, or storing relevant data outside the chat.
---

# Atlas Cartographer

## Core Rule

Use this skill when useful task state should survive chat compaction or deletion.
Write compact local cards with source pointers, lane IDs, decisions, validation
results, and unresolved next actions. Read those cards before assuming a resumed
task has no prior context.

Do not store secrets, private chain-of-thought, raw credentials, personal contact
details, or bulk copied source content. Store pointers and short summaries unless
the user explicitly asks for a larger local archive.

Keep this separate from the canonical ATLAS research archive by default. Only
write into the ATLAS repo itself when Shawn explicitly asks to import or maintain
archive lanes.

## Local Store

Default continuity root:

`C:\Users\Shawn\.codex\aiwf-atlas-cartographer`

Files:

- `cards.jsonl`: all continuity cards.
- `lanes/<lane>.jsonl`: per-lane mirrors for fast scoped retrieval.
- `manifest.json`: counts, lane totals, project totals, and last update.
- `latest-card.json`: last card written by the helper.

Override the root with `ATLAS_CARTOGRAPHER_HOME` or the scripts' `--data-root`
argument when a task needs an alternate local store.

## Workflow

1. Before resuming old work, search local cards with
   `scripts/search_continuity_cards.py`.
2. During substantial work, keep normal workspace notes and receipts in the
   project. Use cards for durable summaries and source pointers, not as a live
   scratchpad.
3. Before compaction, deletion, handoff, or long pause, write a card with
   `scripts/record_continuity_card.py`.
4. Put the card in a stable lane such as `atlas_archive`, `aiwf_studio`, `mok`,
   `rv1`, `retrain`, `codex_tooling`, `local_ai_runtime`, `dataset_library`,
   `windows_host`, or `general_continuity`.
5. Include enough to restart: exact repo/path, touched files, decisions made,
   commands or tests run, validation result, unresolved next action, and where
   source evidence lives.

## Scripts

Record a card:

```powershell
python <this-skill>\scripts\record_continuity_card.py `
  --project "AIWF - ATLAS" `
  --lane atlas_archive `
  --title "Lane 20 refresh handoff" `
  --summary "Updated retrieval cards and source coverage; JSONL validation passed." `
  --source "C:\path\to\repo\01_CANONICAL_RESEARCH_LANES\20_data_engineering_for_ai" `
  --verification "python validation passed" `
  --unresolved "Future Vol. 2 examples still needed"
```

Search cards:

```powershell
python <this-skill>\scripts\search_continuity_cards.py `
  --query "retrieval cards schema" `
  --lane atlas_archive `
  --limit 5
```

Read `references/cartographer-continuity.md` before changing card schema,
storage layout, lane taxonomy, or import/export behavior.

## Project Boundaries

Use the bundled continuity scripts for normal Codex handoffs. The current ATLAS
archive checkout verified during pack maintenance is:

`C:\Users\Shawn\Desktop\AI_Projects\ai project workspace\Repos\AIWF - ATLAS`

Verify that path again before archive edits because mirrors and checkouts can
move. Project-specific cartographers are not dependencies of this skill.

## Reporting

When this skill writes or reads continuity data, report:

- card IDs written or read
- lane used
- local store path
- validation performed
- any facts that still need live verification
