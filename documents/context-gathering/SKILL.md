---
name: context-gathering
description: MANDATORY skill. Invoke BEFORE any codebase exploration, code reading, writing, editing, or answering about code. If not active in the current conversation, DO NOT explore/read/edit code or answer code questions.
---

## Required `<project-root>/docs` reads

Read these project-root spec files before any codebase exploration, code reading, writing, editing, or answering about code (use shell `cat`/`ls` — they may be in `.gitignore`, invisible to built-in search). Missing file → fall back to native tools, note the gap; never invent contents.

- `<project-root>/docs/code-navigation.md`
- `<project-root>/docs/database-tools.md`
- `<project-root>/docs/doc-lookup.md`
- `<project-root>/docs/knowledge-graphs.md`

## Core Principle

Never write code from assumptions. Gather context first, then act.

Flow: clarify target → map (codebase + database) → fetch docs → analyze conventions → verify → act.

## Pre-flight checkpoint

Before any codebase exploration, `read`/`edit`/`write` on a code file, any code navigation tool call (see `<project-root>/docs/code-navigation.md` in the project root), or any answer about code, verify:
1. The target (file path, symbol, or question) is defined — if ambiguous, ask before exploring.

### 1. Clarify the target

A wrong target wastes the whole gather. If the request is ambiguous, ask BEFORE exploring: specific goal, affected module/area, constraints. Use `grill-me` if complex or under-specified. If the target is still undefined after one clarifying round, **stop and say so explicitly.** List what's ambiguous. Do not explore speculatively.

### 2. Discover symbols (Serena-first)

Code navigation tools are PRIMARY for symbol-level work (see `<project-root>/docs/code-navigation.md` in the project root): symbol lookup, reference tracing, class member/signature/parent/interface listing. Use `grep`/`read`/`find_file_by_name` ONLY for non-symbol lookups: plain-text searches (config keys, lang keys, strings), known file paths, glob patterns.

### 3. Map the codebase

- If a knowledge graph output exists (see `<project-root>/docs/knowledge-graphs.md` in the project root), query it before raw source browsing. Fallback to the knowledge graph wiki/report for broad navigation and architecture review (see `<project-root>/docs/knowledge-graphs.md` in the project root).
- Locate entry points, related modules, dependencies. Trace cross-module wiring via contracts and repositories. Identify callers and callees. Read existing implementations of similar features for patterns.
- Query the database when the target touches persisted state: schema, row counts, EXPLAIN plans, sample rows. Use database tools (see `<project-root>/docs/database-tools.md` in the project root). Database state is ground truth — verify it alongside code. Do not rely on seeders, migrations, factories, or operations for current data shape.

### 4. Fetch current documentation

Assume internal knowledge is outdated for any framework/library/SDK. Use documentation lookup tools (see `<project-root>/docs/doc-lookup.md` in the project root). Verify API signatures, current best practices, version-specific behavior, and gotchas.

### 5. Analyze conventions

Before proposing changes, identify: code style and formatting rules (e.g., code style config files), naming patterns, error handling and validation patterns, testing patterns and existing coverage, architecture patterns (module structure, repository/contract, DTOs). Never skip this step.

### 6. Verify understanding

Steps 2-5 collect material; step 6 confirms it is enough to act. Skipping leads to gaps that surface as rework or broken callers.

Confirm you know: current implementation and callers, libraries/versions, relevant doc patterns, impact areas and breaking changes, edge cases and error paths, and database state (schema, counts, sample rows) when the target touches persisted data.

**Ready to act when ALL hold:** implementation located (file:line + entry points named) · callers mapped (one `find_references` pass) · conventions matched (style, naming, error handling, test patterns) · impact scoped (breaking changes, edge cases, error paths) · gaps named (if any above can't be confirmed, state what's unknown and what's needed).

Only after this — plan and implement.

## When to skip steps

Default: don't skip. Each exception is narrow — verify the condition holds first.

- Step 2: only for pure text/config with no code symbols.
- Step 3: only if the target file is fully isolated (verify first). Database queries still apply if the target touches persisted state.
- Step 4: only if the relevant feature is verified in the last 30 lines of code already in context.
- Step 5: never skip.

## Trivial-Task Fast Path

Skip the deep scan only when ALL hold: single file with exact path known (no search needed), change is mechanical/obvious (rename, typo, one-line fix, add an import), no cross-module callers affected (verify with one `find_references` call).

When the fast path applies: act. Skip steps 2-4. Step 5 (conventions) still applies — match surrounding style. If any condition fails, run the full workflow.
