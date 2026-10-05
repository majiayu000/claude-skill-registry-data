---
name: memory-management
description: Recall, checkpoint, and audit durable Laravel project knowledge across sessions when prior context materially affects the current task.
tags:
  - laravel
  - php
---

# Memory Management

Use this skill as conditional context infrastructure when a Laravel task depends on prior context, project history, or known conventions. For self-contained local tasks, skip memory entirely.

## Core Principles

- Remember only what remains useful.
- Retrieve only what is relevant.
- Verify before trusting.
- Anonymize before sharing across projects.
- Never persist secrets.
- Preserve provenance for every durable entry.
- Prefer continuity without context overload.

## Conditional Preflight

The `using-laravel-standards` entrypoint decides this automatically before broad code exploration. Do not wait for explicit phrases like "remember" or "use memory-management".

Run memory preflight only when at least one is true:
- the user references previous work or prior decisions
- the task depends on project history
- a known project convention is needed
- durable prior context materially affects the implementation

For self-contained local tasks, skip memory entirely.

Prefer the active MCP server when the host exposes it:

```text
MCP server: syarif-memory-management
Tool: memory_auto
Root: %USERPROFILE%\.ai-memory on Windows unless AI_MEMORY_ROOT overrides it
Installed skill path: %USERPROFILE%\.agents\skills\memory-management
```

If MCP is unavailable and Node/file access exists, fall back to the local CLI:

```bash
node <skill-dir>/scripts/memory.mjs auto --cwd <project-root> --query "<task intent>" --limit 5
```

This returns an explicit `decision: RUN` or `decision: SKIP`. On `SKIP`, continue normal work without memory. On `RUN`, use only compact relevant memory. Do not load every memory file by default. Do not fail the task merely because memory infrastructure is unavailable.

Memory is outside specialist routing. It does not consume the primary specialist slot, the supporting specialist slot, or the 0-2 specialist cap.

Preflight is retrieval-only. It must not create durable memory entries; writes happen through `remember` or `checkpoint` after safety checks.

## Recall Budget

Default recall budget:

- User memory: ~200 tokens
- Conversation memory: ~500 tokens
- Project memory: ~800 tokens
- Workflow memory: ~400 tokens
- Codebase context: remaining budget up to ~2200 tokens
- Reserve: ~400 tokens

Stop retrieving when marginal relevance is lower than token cost.

## Graph Memory

When `memory-graph.json` exists, query the graph before opening Markdown evidence:

```bash
node <skill-dir>/scripts/memory.mjs graph query "<task intent>" --limit 5
node <skill-dir>/scripts/memory.mjs graph path <from-id> <to-id>
node <skill-dir>/scripts/memory.mjs graph explain <memory-id>
```

Use graph edges with confidence tags:
- `EXTRACTED` = explicit in source
- `INFERRED` = derived by reasoning
- `AMBIGUOUS` = weak or conflicting evidence

## Memory Staleness

Memory is not forever. Every memory entry should carry a lifecycle:

- `CURRENT` - actively valid and aligned with current codebase.
- `STALE` - likely outdated; verify before trusting.
- `SUPERSEDED` - replaced by newer memory or current code.
- `TEMPORARY` - valid only for the current session or short horizon.

When the codebase or architecture changes, mark older project memories as `STALE` or `SUPERSEDED` rather than deleting them. Prefer current code over old memory.

## Source Precedence

When memory and current evidence conflict, trust this order:

1. Current code
2. Current config
3. Project docs
4. Explicit project memory
5. Conversation memory
6. Inferred memory

This prevents memory poisoning during implementation.

When memory conflicts with current evidence, mark the memory mentally as stale or superseded until verified. Do not silently implement old memory over current code/config.

## Selective Checkpointing

Do not checkpoint everything. Store only reusable durable knowledge:

- architectural decision
- non-obvious constraint
- bug root cause that is reusable
- project convention
- environment quirk

Do not store:
- line-number changes
- temporary debug notes
- short-lived branches
- one-time grep results

## Decision Memory

Prefer storing the decision, not just the fact.

Good:
- Chose session-persisted filters instead of query-string persistence because existing project convention uses session state.

Bad:
- Search filter uses session.

Decision memory helps the next agent understand why, not just what.

## Checkpoint At Handoff

Run checkpoint after meaningful work only when durable reusable project knowledge changed:

```bash
node <skill-dir>/scripts/memory.mjs checkpoint --project <alias> --summary "<handoff summary>" --pending "<open questions>" --files "app/Actions/Foo.php,tests/Feature/FooTest.php"
```

Memory checkpoint is never a requirement for task completion. It occurs only when durable reusable knowledge was produced. Temporary debugging, transient terminal failures, trivial line edits, one-time grep results, and raw logs should not be checkpointed.

## Security Pipeline

Before writing memory, pass data through:

```text
raw input -> secret detection -> personal-data classification -> scope classification -> anonymization -> retention policy -> encryption at rest -> memory storage
```

Never store secrets, raw emails, phone numbers, .env contents, or customer personal data.

## References

- Graph memory commands and formats: `references/graph-memory.md`
- Hermes-style orchestrator profile: `references/hermes-orchestrator-profile.md`
