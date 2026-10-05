---
name: t1k:context
description: "Check context usage limits, monitor time remaining, optimize token consumption, debug context failures. Use when asking about context window, token budget, or agent context sizing."
keywords: [tokens, optimize, context-window, agent-context, injection, degradation]
version: 1.0.0
argument-hint: "[topic or question]"
effort: medium
origin: theonekit-core
repository: The1Studio/theonekit-core
module: null
protected: true
---

# T1K Context Engineering

Context engineering curates the smallest high-signal token set for LLM tasks. The goal: maximize reasoning quality while minimizing token usage across all T1K workflows.

## When to Activate

- Designing/debugging T1K agent systems (cook, fix, debug, test, review)
- Context limits constrain subagent performance
- Optimizing cost/latency in multi-agent pipelines
- Building module-scoped context injection
- Implementing agent memory and cross-session persistence

## Core Principles

1. **Context quality > quantity** — High-signal tokens beat exhaustive content
2. **Attention is finite** — U-shaped curve favors beginning/end positions
3. **Progressive disclosure** — Load information just-in-time (sessionBaseline → keyword match → references)
4. **Isolation prevents degradation** — Partition work across subagents
5. **Measure before optimizing** — Know your baseline

**IMPORTANT:** Sacrifice grammar for concision. Pass these rules to subagents.

## Quick Reference

| Topic | Reference |
|-------|-----------|
| Fundamentals | [context-fundamentals.md](./references/context-fundamentals.md) |
| Degradation | [context-degradation.md](./references/context-degradation.md) |
| Optimization | [context-optimization.md](./references/context-optimization.md) |
| Compression | [context-compression.md](./references/context-compression.md) |
| Memory | [memory-systems.md](./references/memory-systems.md) |
| Multi-Agent | [multi-agent-patterns.md](./references/multi-agent-patterns.md) |
| Evaluation | [evaluation.md](./references/evaluation.md) |
| Tool/Skill Design | [tool-design.md](./references/tool-design.md) |
| Pipelines | [project-development.md](./references/project-development.md) |
| Runtime Awareness | [runtime-awareness.md](./references/runtime-awareness.md) |
| T1K Patterns | [t1k-patterns.md](./references/t1k-patterns.md) |

## Key Metrics

- Token utilization: warning 70%, optimize 80%
- Multi-agent cost: ~15x single agent baseline
- Compaction target: 50–70% reduction, <5% quality loss
- Cache hit target: 70%+ for stable workloads

## Four-Bucket Strategy

1. **Write** — Save context externally (scratchpads, files, `plans/`)
2. **Select** — Pull only relevant context (module scoping, skill activation)
3. **Compress** — Reduce tokens while preserving info
4. **Isolate** — Split across subagents (context partitioning)

## Runtime Awareness

T1K hooks auto-inject usage awareness via PostToolUse. Thresholds: 70% WARNING, 90% CRITICAL.
See [runtime-awareness.md](./references/runtime-awareness.md) for configuration details.

## Anti-Patterns

- Exhaustive context over curated context
- Critical info in middle positions
- No compaction triggers before limits
- Single agent for parallelizable tasks
- Injecting all installed module skills into every subagent
- Duplicating hook logic in AI responses

## Security

- Never include secrets, tokens, or credentials in context passed to subagents
- Scope injected context to the minimum needed for the task
- Do not log or persist sensitive tool outputs in `plans/` or memory files
- Follow `rules/security.md` for all context-handling operations
