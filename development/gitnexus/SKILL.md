---
name: gitnexus
description: "Unified GitNexus dispatcher for CLI, guide, exploration, debugging, PR review, impact analysis, and refactoring workflows. Use when the user says 'run gitnexus', 'analyze this repo', 'check impact', 'trace dependencies', or 'review this PR'."
scope: harness
invocation: ability
---

# GitNexus Dispatcher

Use the matching submode for the task:

| Submode | Use |
|---|---|
| cli | analyze, status, clean, wiki, list |
| guide | tool/resource/schema reference |
| explore | architecture and execution-flow discovery |
| debug | root-cause and failure tracing |
| pr-review | pull request risk review |
| impact | blast-radius analysis before edits |
| refactor | graph-aware rename/extract/split/move |

Before editing any function, class, or method, run impact analysis and report blast radius. Before commit, run detect-changes when available.

## Session Notes

- 2026-06-16 — Unified dispatcher for GitNexus workflows across CLI, debugging, exploration, and PR review. Reach for this when the task involves GitNexus tooling or codebase analysis.
