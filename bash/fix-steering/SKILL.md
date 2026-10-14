---
name: fix-steering
description: Analyze Codex history for interruptions, corrections, and user steering that indicate agent errors. Use when asked to find common steering mistakes, audit a model's behavior across Codex sessions, compare steering patterns for a specified model, or propose prevention changes through new skills or AGENTS.md guidance.
---

# Fix Steering

## Overview

Use this skill to find agent failure modes from steering evidence in Codex histories. Collect candidate interruption and correction turns, use subagents for cleanup and evidence summarization, then use the current model to group failures by addressable missing context and recommend prevention changes.

## Workflow

1. Determine the target model.
   - If the user names a model, use only histories for that model.
   - Otherwise default to the current model when it is known from the active runtime or session metadata.
   - If the current model cannot be identified from metadata, run the collector with `--model auto`, state that the model filter could not be enforced, and do not compare across models unless the user asks.

2. Collect candidate steering turns.
   - Prefer the bundled collector:

```bash
python3 scripts/collect_steering_cases.py --model "<model-or-auto>" --since 30d --limit 80 --format markdown > /tmp/fix-steering-cases.md
```

   - Use `--codex-home <path>` when histories are outside `${CODEX_HOME:-$HOME/.codex}`.
   - By default, the collector scans user-originated sessions and skips subagent/internal threads. Use `--include-subagents` only when the audit explicitly includes delegated agents.
   - Use `--include-unknown-model` only when the user accepts mixing sessions whose metadata does not expose a model.
   - Use `--keywords` to add project-specific steering terms, not to replace the built-in interruption patterns.

3. Use subagents to clean candidate cases.
   - Use the configured default model rather than hard-coding a model name; inherit the current model when the subagent tool does not support model selection.
   - Read and adapt `references/subagent-case-cleanup-prompt.md`.
   - Ask subagents to remove obvious false positives, keep raw evidence intact, and split large sets into review batches.
   - Do not ask cleanup agents to infer final failure categories.

4. Use subagents to summarize case evidence.
   - Use 2-4 subagents for independent batches when enough cases exist.
   - Read and adapt `references/subagent-review-prompt.md`.
   - Pass raw cleaned case batches, not conclusions.
   - Allow subagents to inspect narrow additional context from the original session logs when the collector excerpt is inadequate. They should only fetch lines around the cited case or adjacent turns from the same session, and should report any extra context they used.

5. Use a subagent to merge and dedupe outputs.
   - Read and adapt `references/subagent-merge-prompt.md`.
   - Ask the merge subagent to deduplicate cases, remove non-errors, normalize evidence IDs, and produce a compact table of inferred failures.
   - Keep the merge output focused on evidence and likely missing context. Do not ask it to write the final user-facing report.

6. Categorize with the current model.
   - Identify failure modes de novo from the merged evidence instead of forcing a predefined taxonomy.
   - Group failures by addressable missing context: the instruction, skill, AGENTS.md rule, tool habit, or verification step that would have prevented the error.
   - Use behavioral pattern labels only as supporting detail when they help explain the addressable context.
   - Keep one primary group per case and note secondary groups only when they materially change the prevention recommendation.

7. Report actionable results.
   - Start with the most common addressable failure groups, including counts and short representative evidence.
   - Separate observed evidence from inference.
   - Include residual uncertainty: sample size, model-filter caveats, context-expansion caveats, and false-positive risk.
   - Recommend prevention mechanisms:
     - New skill: use when the failure requires a repeatable domain workflow, collector, checker, or task-specific procedure.
     - AGENTS.md change: use when the failure is broad behavioral guidance for every task in a repo or environment.
     - Tooling/script change: use when the failure is detectable mechanically.
   - Make each recommendation concrete enough to implement, with a proposed short rule or skill name.

## Collector Output

The collector emits candidate cases, not final truth. Treat it as a recall-oriented filter. A case is useful when the user message appears to correct, interrupt, redirect, constrain, or clarify after the assistant had already acted or committed to a path.

For JSON output:

```bash
python3 scripts/collect_steering_cases.py --model "<model-or-auto>" --format json > /tmp/fix-steering-cases.json
```

Use JSON when writing another script or when case IDs need to remain machine-stable across subagent batches.

## Context Expansion

If a case excerpt is too thin to judge, inspect only the minimum original log context needed:

- Use the case's `path`, `line`, and `session_id` to fetch nearby JSONL records.
- Prefer a small window around the cited line before reading more of the session.
- Read adjacent user and assistant turns, tool calls, and tool outputs only when they materially affect whether the steering was caused by an agent error.
- Do not mine unrelated sessions or broad history to support a preferred conclusion.
- Record which log lines or turns were inspected so the final report can distinguish collector evidence from expanded context.
