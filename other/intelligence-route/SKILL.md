---
name: intelligence-route
description: Route tasks via the 3-tier model selector and learned patterns; emits a routing rationale via hooks_explain
argument-hint: "<task-description> [--why]"
allowed-tools: mcp__claude-flow__hooks_route mcp__claude-flow__hooks_explain mcp__claude-flow__hooks_model-route mcp__claude-flow__hooks_model-stats mcp__claude-flow__hooks_model-outcome mcp__claude-flow__hooks_intelligence_pattern-search mcp__claude-flow__hooks_intelligence_attention mcp__claude-flow__hooks_intelligence_stats mcp__claude-flow__neural_predict mcp__claude-flow__hooks_pre-task Bash
---

# Intelligence Routing

Pick the optimal agent + model tier for a task using learned patterns + the 3-tier router. Emits a `hooks_explain` rationale so the choice is auditable.

## When to use

Before starting any non-trivial task. Replaces manual agent selection with data-driven decisions.

## Steps

1. **Get an agent recommendation** — `mcp__claude-flow__hooks_route` with the task description. Returns `{ recommended, confidence, reasoning }`.
2. **Get a model tier recommendation** — `mcp__claude-flow__hooks_model-route` for Haiku/Sonnet/Opus selection.
3. **Search for similar past patterns** — `mcp__claude-flow__hooks_intelligence_pattern-search` to find prior successes.
4. **Predict outcome** — `mcp__claude-flow__neural_predict` with the task description for a confidence-scored prediction.
5. **Spawn the recommended agent** at the recommended model tier.
6. **(If `--why` was passed)** — call `mcp__claude-flow__hooks_explain` to surface the routing rationale to the user.
7. **After task completes** — call `mcp__claude-flow__hooks_model-outcome` with `success: true|false` to train the router.

## 3-Tier Model Routing

| Tier | Handler | Latency | Cost | When |
|------|---------|---------|------|------|
| 1 | Agent Booster (WASM) | <1ms | $0 | Simple transforms (var→const, add types, remove console) — skip LLM entirely |
| 2 | Haiku | ~500ms | ~$0.0002 | Low complexity (<30%), bug fixes, quick patches |
| 3 | Sonnet/Opus | 2–5s | $0.003–$0.015 | Complex reasoning, architecture, security, multi-file refactors |

When `hooks_route` returns `[AGENT_BOOSTER_AVAILABLE]` for an intent type (`var-to-const`, `add-types`, `add-error-handling`, `async-await`, `add-logging`, `remove-console`), skip the LLM and use the Edit tool directly.

## Recording outcomes

Closing the routing loop is mandatory:

```bash
# Success
mcp tool call hooks_model-outcome --json -- '{"taskId": "T123", "success": true, "model": "haiku"}'

# Failure with reason
mcp tool call hooks_model-outcome --json -- '{"taskId": "T123", "success": false, "model": "haiku", "reason": "complexity-misjudged"}'
```

The router learns from these calls. Skipping them = no learning.

## CLI alternative

```bash
npx @claude-flow/cli@latest hooks route --task "description"
npx @claude-flow/cli@latest hooks pre-task --description "description"
npx @claude-flow/cli@latest hooks explain --topic "routing decision"
```
