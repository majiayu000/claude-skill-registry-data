---
name: gitnexus
disable-model-invocation: true
description: "Unified GitNexus dispatcher for CLI, guide, exploration, debugging, PR review, impact analysis, and refactoring workflows. Use when the user says 'run gitnexus', 'analyze this repo', 'check impact', 'trace dependencies', or 'review this PR'."
triggers: ["/gitnexus", "code intelligence dispatcher", "impact analysis"]
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

### 2026-05-29
- session: 349m | peak ctx: 71% | compacts: 4
- tools: Bash×268, Read×133, Edit×104, TodoWrite×12, Write×8, StructuredOutput×8, Workflow×2, ToolSearch×1, AskUserQuestion×1
- corrections: none
- errors: none
