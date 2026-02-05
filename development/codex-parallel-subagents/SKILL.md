---
name: codex-parallel-subagents
description: "[DEPRECATED] Run multiple AI agent threads in parallel with bounded concurrency. Use evolving-workflow instead."
---

# Codex Parallel Subagents

> **DEPRECATED**: This skill is deprecated. Use [evolving-workflow](../evolving-workflow/SKILL.md) instead, which provides a declarative workflow API with built-in parallel execution support via `.concurrency(n)`.

Run multiple AI agent threads concurrently with bounded parallelism and collect results safely.

## When to use this skill

- Running multiple agent tasks in parallel
- Fan-out work across files, packages, or repositories
- Batch processing with rate limiting
- Streaming progress from concurrent tasks
- Collecting structured outputs from multiple agents

## Quick navigation

| Need | Resource |
|------|----------|
| New to Codex SDK | [references/codex-basics.md](references/codex-basics.md) |
| Advanced options | [references/codex-advanced.md](references/codex-advanced.md) |
| Async patterns | [references/async-basics.md](references/async-basics.md) |
| Troubleshooting | [references/troubleshooting.md](references/troubleshooting.md) |

## Production-ready assets

Copy these to jumpstart your implementation:

| Asset | Description | Run |
|-------|-------------|-----|
| [parallel_batch](assets/parallel_batch) | Reentrant batch processing with stdin/file input, offset/limit, JSON output | `moon run -C assets/parallel_batch assets/parallel_batch` |
| [package_analyzer](assets/package_analyzer) | Discover and summarize all MoonBit packages | `moon run -C assets/package_analyzer assets/package_analyzer` |

### How to use these assets

1. **Copy the asset directory** to your project
2. **Customize `run_task()`** (or the main processing function) for your use case
3. **Adjust structs** (`TaskInput`, etc.) if you need additional fields
4. **Set environment variables** as needed (`CODEX_WORKDIR`, `PARALLELISM`)

See each asset's README for detailed usage and options.

## Key rules

1. **One thread per task** - never share threads across concurrent tasks
2. **Use semaphores** - guard parallel runs with `@async.Semaphore::new(n)` to avoid rate limits
3. **Set working directory** - use `ThreadOptions::new(working_directory=...)` for task isolation
4. **Allow failures** - use `allow_failure=true` and capture errors per task
5. **Avoid conflicts** - for tasks that modify shared resources (e.g., building software, editing same files), use git worktrees or separate directories to isolate each agent
