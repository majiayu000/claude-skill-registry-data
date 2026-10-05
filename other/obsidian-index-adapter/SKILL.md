---
name: obsidian-index-adapter
description: Create guarded Obsidian index notes from completed memo outputs. Use when a raw archive and summary memo already exist and the user wants an Obsidian index card, topic note, or project memo note that points back to those sources. Do not use for first-pass conversation capture, freeform vault writing, or formal document authoring.
metadata:
  runtime_support_files: true
runtime_projection: true
source_of_truth: registry/skills/obsidian-index-adapter/SKILL.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/obsidian-index-adapter/SKILL.md`
> Source of truth: `registry/skills/obsidian-index-adapter/SKILL.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill`
# Obsidian Index Adapter

## Overview

`obsidian-index-adapter` is a downstream adapter for the memo pipeline. It turns an existing memo state into a controlled Obsidian index note while preserving the raw archive and summary memo as the primary sources of truth.

Use this skill only after `conversation-memo` or an equivalent workflow has already produced:

- a raw conversation archive
- a summary memo
- optional candidate or completed formal outputs

## When To Use

Use this skill when the user asks for tasks such as:

- "make an Obsidian index note for this memo"
- "add this discussion memo to the vault index"
- "create an Obsidian card that links the raw talk and summary"
- "turn this completed memo into a guarded vault note"
- "add a topic index note for these memo outputs"

Do not use this skill when the user asks for:

- first-pass conversation capture
- raw transcript archival
- freeform vault writing
- arbitrary append/update behavior on existing notes
- formal document writing or code implementation
- direct use of a last-focused vault without explicit identifiers

## Required Preconditions

Before doing anything else, confirm that all of the following exist:

- a `raw_archive_path`
- a `summary_memo_path`
- an explicit `vault_name`
- an explicit `vault_root`
- an explicit `target_path`
- an allowed `note_type`

If any of these are missing, stop and ask for the missing input or tell the user what upstream step is still incomplete.

## Workflow

1. Verify memo state.
   Confirm the raw archive and summary memo already exist. This skill is downstream only.
2. Normalize adapter inputs.
   Collect `vault_name`, `vault_root`, `note_type`, `target_path`, `raw_archive_path`, and `summary_memo_path`. Add `topic`, `project`, `formal_outputs`, and `tags` when available.
3. Enforce guardrails.
   Reject freeform vault writes, disallowed note types, missing source files, or target paths outside the whitelist.
4. Build the note payload.
   Create a small index-style note with frontmatter, summary bullets, source links, and formalization status.
5. Write only the index note.
   Keep the raw transcript out of the Obsidian note by default. The note should point to source artifacts, not replace them.
6. Report what was created.
   Return the target note path plus the linked raw archive, summary memo, and any formal outputs.

## Supported Operations

### `create-index-note`

Create a `conversation-index-note` from a completed memo state.

Typical inputs:

- `vault_name`
- `vault_root`
- `target_path`
- `raw_archive_path`
- `summary_memo_path`
- `topic`
- `project`

### `link-formal-output`

Update or generate a note so it points at one or more completed formal outputs. Use this only after the formal output already exists.

### `create-topic-note`

Create a topic-level index note that groups several related memo outputs. Keep it index-oriented rather than turning it into a canonical formal document.

### `refresh-index-status`

Refresh note metadata or status fields so an existing note reflects whether formalization is still pending or already completed.

## Allowed Note Types

Only these note types are allowed in v1:

- `conversation-index-note`
- `topic-index-note`
- `project-memo-index-note`

Anything else is out of scope until the adapter policy is expanded.

## Path Policy

Only write to whitelisted vault locations:

- `Inbox/Agent Memos/`
- `Indexes/Conversations/`
- `Projects/<project>/Memos/`

Do not write outside the whitelist in v1.

## Guardrails

- Never use the last-focused vault implicitly.
- Never treat Obsidian as the only source of truth.
- Never write the first copy of the discussion to the vault.
- Never inline the complete raw transcript unless the user explicitly asks for that behavior.
- Never freely append to arbitrary notes as part of the default memo pipeline.
- Keep the Obsidian note small, index-oriented, and source-linked.

## Output Expectations

The resulting note should include:

- frontmatter describing the note type, topic, date, project, and tags
- a short summary section
- a source-links section pointing to the raw archive and summary memo
- a formalization-status section

Preferred template details live in:

- [references/adapter-workflow.md](references/adapter-workflow.md)
- [references/guardrails.md](references/guardrails.md)
- [references/note-schema.md](references/note-schema.md)

## Resources

Use the references for detailed operational constraints and templates:

- `references/adapter-workflow.md`
- `references/guardrails.md`
- `references/note-schema.md`
