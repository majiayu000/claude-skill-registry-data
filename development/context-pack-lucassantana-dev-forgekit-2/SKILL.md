---
name: context-pack
description: Build a task-aware context bundle (relevant code + applicable standards + related past decisions) via the local RAG index, capped at a token budget. Use at the start of any implementation/refactor/debug task instead of reading files blindly. Replaces "read whole file" with "retrieve the function + callers + rules + prior ADR."
type: skill
---

# context-pack

Compresses a whole-codebase-style context into the chunks that actually matter for _this_ task.

## When to use

- Start of `plan`, `pr-flow`, `code-review`, `ship`, bug fix, refactor.
- Before touching an unfamiliar file: ask pack for "relevant code" around the target symbol.
- When user asks "how does X work" across a large repo.

## When NOT to use

- You already have the exact file path and know what you need → Read directly.
- Exact string search → Grep.
- Symbol-level navigation in the current repo → Serena.

## Usage

```bash
~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/pack.py "<task description>" [options]
```

Options:

- `--files path1 path2 …` — explicit paths the task will touch.
- `--diff` — auto-populate `--files` from `git diff --name-only`.
- `--budget N` — token budget (default 4 000; chars/4 heuristic).
- `--cwd <path>` — override working dir for repo auto-scoping.

Always pipe the output back into context:

```bash
pack.py "fix send_discord retry logic" --diff --budget 3500
```

## What the bundle contains

Four sections in priority order, each capped per-chunk so the budget stays honest:

1. **Relevant code** — top-6 symbol-level code chunks (cwd auto-scopes to the current repo).
2. **Applicable standards** — top-3 sliced rules from `~/.claude/standards/*.md` matching the task.
3. **Past decisions / memory** — top-4 chunks from memory, plans, and handoffs (cross-repo).
4. **Explicit files** — if `--files` given, best chunks for each; falls back to first 40 lines when no match exists in the index.

## Output format

````markdown
# Context pack for: <task>

_Budget: 4000 tokens · remaining ≈ N_

## Relevant code

### code/Lucky::setupInternalNotifyRoutes `packages/backend/src/routes/internalNotify.ts:23-28` (cos=0.57 bm=12.9)

```...chunk...
### ...

## Applicable standards
### standards  `~/.claude/standards/security.md:1-5`  ...

## Past decisions / memory
### plans  `~/.claude/plans/my-project-planning.md:40-60`  ...
```
````

## Integration points

- `plan` skill runs pack first; plan-drafting sees only the pack output + user prompt, not the whole repo.
- `pr-flow` / `ship` runs with `--diff` to pull in context for the changed files.
- `code-review` pipes the PR's file list and diff summary in.

## Eval baseline

Retrieval layer is measured via `~/.claude/rag-index/eval/run.py` (MRR + Hit@K). The canonical 20-query rerank-on baseline is MRR 0.72 · Hit@3 0.80 · Hit@5 0.80; the expanded 30-query baseline is MRR 0.62 · Hit@3 0.63 · Hit@5 0.67. Compare against the matching dataset version.

## Rebuild triggers

- PostToolUse hook reindexes single files on Write/Edit.
- Full rebuild: `~/.claude/rag-index/venv/bin/python ~/.claude/rag-index/build.py` (~50 s).
