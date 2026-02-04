---
name: cursor-diary
description: Keep a tiny-step implementation diary during coding sessions (what changed, why, commands run, failures, and what was learned), with docmgr integration (doc add/relate/changelog). Use when the user asks to "keep a diary", "write a dev log", or document work step-by-step.
---

# Cursor Diary

## Overview

Maintain a step-by-step implementation diary as you work, focused on reproducibility (exact commands, file paths, commit hashes) and review efficiency (what to check + how to validate).

## Workflow

### 1) Bootstrap
- Create a diary doc early (before exploration if possible).
  - If using docmgr tickets: `docmgr doc add --ticket TICKET-ID --doc-type reference --title "Diary"`

### 2) Record each tiny step (frequently)
- Write 1–2 short prose paragraphs first (intent + what it unlocked).
- Include exact commands, key outputs, and versions when relevant.
- Capture failures verbatim (errors are valuable).

### 3) Keep code ↔ docs consistent (docmgr loop)
- Implement + format + test.
- Commit code (record hash).
- Update diary with the commit hash + rationale.
- Relate files to the diary with absolute paths: `docmgr doc relate --doc <diary-path> --file-note "/abs/path:why it matters"`
- Update ticket changelog per step: `docmgr changelog update --ticket TICKET-ID --entry "Step N: ..." --file-note "/abs/path:reason"`
- Commit docs separately (e.g., `Diary: record Step N`).

## Output template
- Use the diary template in `references/diary.md` (copy/paste) as the canonical structure.

## Notes
- Prefer many small steps over a few big ones.
- Always include: “What was tricky to build” + “What warrants a second pair of eyes” when behavior changes.
