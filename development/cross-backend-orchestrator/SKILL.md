---
name: cross-backend-orchestrator
description: "Orchestrate AI tasks across multiple backends (Codex, Claude, Gemini) using memex-cli. Cross-platform Python implementation. Use when (1) Running tasks on specific AI backends, (2) Comparing outputs across different AI models, (3) Creating multi-model workflows, (4) Delegating specialized tasks to optimal backends, (5) Building AI pipelines with fallback support."
---

# Cross-Backend Orchestrator

Cross-platform Python toolkit for orchestrating AI tasks across Codex, Claude, and Gemini backends using memex-cli.

## Quick Start

### Single Backend Execution

```bash
python scripts/run_task.py --backend <backend> --prompt "<task>"

# Examples
python scripts/run_task.py --backend claude --prompt "Analyze this code for bugs"
python scripts/run_task.py --backend gemini --prompt "Generate UX wireframe description"
python scripts/run_task.py --backend codex --prompt "Optimize this algorithm"
```

### Multi-Backend Comparison

```bash
python scripts/compare_backends.py --prompt "<task>" --output ./comparison.json
```

## Backend Selection Guide

| Task Type | Recommended Backend | Rationale |
|-----------|---------------------|-----------|
| Code generation/debugging | `codex` | Optimized for code tasks |
| Creative writing/analysis | `claude` | Strong reasoning and writing |
| UX/UI design descriptions | `gemini` | Visual understanding |
| General tasks | Any | User preference |

## Core Workflows

### Workflow 1: Sequential Multi-Backend Pipeline

```bash
python scripts/pipeline.py \
  --stage "codex:Generate Python function for data processing" \
  --stage "claude:Review and improve the code" \
  --stage "gemini:Create documentation with diagrams"
```

### Workflow 2: Parallel Comparison

```bash
python scripts/parallel_run.py \
  --backends codex,claude,gemini \
  --prompt "Explain quantum computing" \
  --output ./results/
```

### Workflow 3: Fallback Chain

```bash
python scripts/fallback_run.py \
  --primary codex \
  --fallback claude \
  --fallback gemini \
  --prompt "Complex task description"
```

## Scripts Reference

| Script | Purpose |
|--------|---------|
| `run_task.py` | Execute single task on one backend |
| `compare_backends.py` | Compare outputs across backends |
| `pipeline.py` | Sequential multi-stage workflow |
| `parallel_run.py` | Parallel execution on multiple backends |
| `fallback_run.py` | Fallback chain execution |
| `replay_events.py` | Replay recorded run events |
| `orchestrator.py` | Core library module (imported by other scripts) |

## memex-cli Integration

All scripts wrap memex-cli commands:

```bash
# Direct memex-cli usage
memex-cli run --backend "codex" --model "deepseek-reasoner" --model-provider "aduib_ai" --prompt "Task" --stream-format "jsonl"
memex-cli run --backend "claude" --prompt "Task" --stream-format "jsonl"
memex-cli run --backend "gemini" --prompt "Task" --stream-format "jsonl"

# Resume interrupted run
memex-cli resume --run-id <ID> --backend <backend> --prompt "Continue" --stream-format "jsonl"

# Replay events
memex-cli replay --events ./run.events.jsonl --format text
```

## Programmatic Usage

```python
from scripts.orchestrator import BackendOrchestrator

orch = BackendOrchestrator()

# Single run
result = orch.run_task("claude", "Explain REST APIs")

# Compare backends
comparison = orch.compare_backends(["codex", "claude"], "Write a sort function")

# Pipeline
pipeline_result = orch.run_pipeline([
    ("codex", "Generate code"),
    ("claude", "Review code"),
])
```

## References

- [Prompt Templates](references/prompt-templates.md) - Structured prompts for consistent cross-backend results
- [Output Formats](references/output-formats.md) - Parsing guidance for JSONL events and outputs