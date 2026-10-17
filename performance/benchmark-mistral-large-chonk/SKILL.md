---
name: benchmark-mistral-large-chonk
description: Benchmark and evaluation harness for Mistral Large on heavy codebase, large-context (chonk), and multi-file refactoring workloads.
compatibility: node >= 18, typescript >= 5.0
---

# Benchmark Mistral Large Chonk

Evaluates Mistral Large (Tier 1 Muscle Cloud) across heavy codebase tasks, large-context ("chonk") token ingestion, multi-file refactoring, and cost-efficiency trade-offs against Frontier baselines.

See [Skill Operator Guide](../../docs/meta/skill-operator-guide.md) for shared operating requirements.

## Inputs & Outputs

### Input Schema

| Property | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `workload` | `string` | **Yes** | Scenario identifier: `needle_retrieval`, `ast_refactor`, `invariant_synthesis`, or `all` |
| `contextSizeTokens` | `number` | No | Context buffer size in tokens (default: `32000`) |
| `iterations` | `number` | No | Number of measurement cycles per workload (default: `3`) |
| `compareFrontier` | `boolean` | No | Compute cost-savings delta against Claude 3.5 Sonnet baseline (default: `true`) |

### Output Schema

```json
{
  "status": "PASS",
  "modelEvaluated": "mistral/mistral-large-2407",
  "contextWindowTested": 32000,
  "overallScore": 94.2,
  "throughputTokensPerSec": 68.4,
  "costPerTaskUsd": 0.0128,
  "costSavingsVsFrontierPct": 85.7,
  "scenarios": [
    {
      "name": "needle_retrieval",
      "score": 98.0,
      "latencyMs": 1420,
      "exactMatch": true
    },
    {
      "name": "ast_refactor",
      "score": 92.5,
      "latencyMs": 3100,
      "syntaxValid": true
    }
  ]
}
```

## Benchmark Scenarios

1. **Needle-in-a-Haystack Retrieval**: Extracts buried interface contracts from 32k–128k token source buffers.
2. **Multi-File AST Refactoring**: Validates structural consistency and type safety across cross-module imports.
3. **Formal Invariant Synthesis**: Evaluates theorem/invariant generation matching Lean 4 verification standards.
4. **Frontier Cost Arbitrage**: Computes price/performance frontier to determine automatic Tier 1 routing gates.
