---
name: cooooost
description: Conserve AI context and API expense in long-running agent tasks through source-preserving checkpoints, targeted retrieval, stable-prefix caching, and opt-in exact replay. Use when developing, debugging, researching, or maintaining projects across lengthy sessions.
---

# Cooooost: quality-first agent workflow

## Immutable operating principles

1. **Correctness over cost.** Never skip required implementation, tests, source review or validation to save tokens. Do not replace a necessary source with an unverifiable summary.
2. **No invented data.** State checkpoints record evidence and status, not hallucinated completion. Revalidate if input/environment changed.
3. **Lossless evidence.** Treat the ledger as an index. Raw transcripts, originals and test outputs are the authority. Keep them locally in `.cooooost/archive` with SHA-256 integrity.
4. **Context integrity.** Keep objective, acceptance criteria, constraints, decisions, changed files, tests, blockers, next steps, and original source pointers accessible across compaction.
5. **Safe API caching.** Provider-native prefix caching is preferred; opt-in exact response replay only for stable identical requests with no tools/live data/streaming and explicit `temperature: 0`. Never claim replay equals fresh model reasoning.
6. **Measured savings.** Report actual `cache_read_input_tokens`/`cached_tokens` and request counts. Report replay token avoidance as an estimate; do not promise 80%.

## Start of task

Check `cooooost status --project .` (initialize via `cooooost init --project .` if missing). Read current user constraints first. If goals conflict, follow latest explicit instructions, preserving past project context. Record durable requirements:

```bash
cooooost update --project . --goal 'Complete the requested task with tests' --acceptance-criteria 'All specified features work' --constraints 'Do not reduce quality'
cooooost checkpoint --project .
```

When files are numerous, prefer scoped searches and `cooooost ingest` / `cooooost retrieve` instead of repeatedly sending entire sources. Retrieval returns an explicit `complete` flag and source hashes; fetch missing originals whenever relevance is uncertain. Do not assert the selected snippets include everything.

## Between steps

After meaningful changes, update `--files-changed`, `--decisions`, `--tests`, `--blockers`, `--next-steps`, and `--sources` with exact evidence. Avoid repeated tool calls whose inputs/results remain unchanged. Cache only stable, verified results. Keep long stable system/tool instructions at the front of prompts to increase provider cache hits; do not weaken the instructions.

## Compaction and recovery

Use `cooooost daemon --project . --interval-min 7 --interval-max 13` in a separate process to create local snapshots and archive registered transcripts. This does **not** force host model compaction. Claude Code optional hooks preserve transcript before native compaction and re-inject ledger at session start. When resuming, run `cooooost verify` and `cooooost summary`; consult source files before acting on ambiguity.

## Completion gate

Run full task-specific checks. Record their actual results. Compare completion against *every* acceptance criterion. Do not mark untested functions as verified. Show remaining uncertainties honestly.

## CLI reference

`cooooost --help`, `cooooost init`, `update`, `checkpoint`, `verify`, `recover`, `status`, `summary`, `archive`, `restore`, `ingest`, `retrieve`, `daemon`, `cycle`, `serve`, `stats`, `purge-cache`, `doctor`, `install`.

Always use the local installed CLI; do not assume a ChatGPT conversation provides arbitrary background process privileges or controls platform limits.