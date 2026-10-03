---
name: patch-pilot
description: A menu-bar diff triage panel that turns a patch or file list into a crisp fix brief, risk scan, and next command.
---

# Patch Pilot

Use this skill when the user needs to turn a local diff, staged file list, or review thread into a fast implementation brief before editing or replying.

## Best fit

- Reviewing a patch and deciding the next safe command.
- Converting a diff into a scoped fix plan or reviewer reply.
- Collapsing terminal, browser, and notes context into one compact surface.

## Build shape

- Prefer a menu-bar popover or compact side panel with one primary recommendation.
- Lead with touched areas, likely regressions, and the next safe action.
- Keep the output copyable so the brief can move into chat, PR comments, or a task.

## Inputs

- Local `git diff --stat`, `git status --short`, or pasted patch text.
- Reviewer comments or bug notes that refer to changed files.
- File paths, failing tests, or small reproduction notes.

## Guardrails

- Do not invent repository state that is not present in the diff or the local workspace.
- Flag uncertainty when the patch context is incomplete.
- Keep the summary concise enough to act on quickly.
- Prefer reversible next steps over speculative broad refactors.

## Prototype

- SwiftUI starter files live in `prototype/`.
- The prototype should feel like a native macOS triage panel, not a full IDE.

## When extending

- Add richer grouping or file clustering only if it improves the first decision.
- Keep the menu-bar path optimized for the pre-commit and pre-reply moment.
