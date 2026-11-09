---
name: clean-context
description: Clean and compress host-repository context by compacting completed task files, deduplicating memory/rules/debug notes, and refreshing a high-signal context summary. Use after finishing tasks, before handoff, or when context artifacts become noisy.
engines: [AGNOSTIC]
---

## When to use
Use when active context has grown noisy and you need to keep only high-signal artifacts for the next session.

## Workflow
1. Verify task changes first.
2. Compact a specific completed task note when needed:
   - `../commands/archive-task-context.sh "<task-name>"`
3. Run full cleanup and summary refresh:
   - `../commands/clean-context.sh`

## Output
- task files compacted
- system and tagged project memory entries merged
- repository-map entries merged
- duplicate rules removed
- debug notes compressed
- tag inventory and context summary refreshed

## Safety rules
- Never delete durable knowledge without archiving first.
- Prefer summarization over destruction.
- Keep system memory flat and project memory tagged, concise, and high-value.
- Preserve traceability through the resolved project archive and report directories.
- All context lives under `<project-root>/.hephaera/.cache/`. This ignored directory holds durable project state; its name never authorizes deleting it as a disposable tool cache.
