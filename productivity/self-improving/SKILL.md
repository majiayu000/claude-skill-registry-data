---
name: self-improving
description: Use when self-reflection + Self-criticism + Auto-learning from corrections
  + Self-organizing memory. Agent evaluates its own work, catches mistakes, and improves
  permanently. Use when working with self improving.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- ai-agent
- improving
- infrastructure
- memory
- self
- self-improvement
version: 1.2.1
homepage: https://clawic.com/skills/self-improving
metadata:
  clawdbot:
    emoji: 🧠
    requires:
      bins: []
    os:
    - linux
    - darwin
    - win32
    configPaths:
    - ~/self-improving/
category: core
---

# Self Improving

## When to Use
**Trigger phrases:**
- "self improving"
- "Self-reflection + Self-criticism + Auto-learning from corrections + Self-organiz"


User corrects you or points out mistakes. You complete significant work and want to evaluate the outcome. You notice something in your own output that could be better. Knowledge should compound over time without manual maintenance.


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

Self Improving is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

## Architecture

- **Input layer** — Receives and validates incoming requests
- **Processing layer** — Core logic for system foundation
- **Output layer** — Formats and delivers results
- **State management** — Maintains context across invocations

## Configuration

- Set up required environment variables and paths
- Configure logging level and output format
- Define resource limits (memory, time, API calls)
- Enable/disable features via configuration flags

## Integration

- Exposes standard interfaces for other skills to consume
- Supports event-driven and request-response patterns
- Compatible with the 1ai-skills hook system
- Logs metrics for the skill performance monitor

## Anti-Rationalization Table

| Rationalization | Reality |
|---|---|
| "I will add monitoring later" | Without monitoring, you cannot detect failures. Add it from day one. |
| "One model is enough" | Different tasks need different models. Route intelligently. |
| "Premature optimization" | Infrastructure decisions are hard to change later. Design for scale early. |

```python
# Example: Model routing
ROUTES = {
    "code": ["claude-sonnet-4-20250514", "gpt-4o"],
    "vision": ["gemini-2.5-pro", "gpt-4o"],
    "fast": ["gemini-2.5-flash", "gpt-4o-mini"],
}

def route_request(task: str, prompt: str):
    models = ROUTES.get(task, ROUTES["fast"])
    for model in models:
        try:
            return call_model(model, prompt)
        except Exception:
            continue
    raise RuntimeError("All models failed")
```


## Process

1. **Prepare** — Gather requirements, verify prerequisites, set up environment
1. **Execute** — Run self improving workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] New task started by reading the experience index (see references/field-journal.md) when the task
  domain has prior cases

## Companion Patterns

- **[Field Journal — Lessons-Per-Case](references/field-journal.md)** — dated, anonymized, scenario-indexed
  per-case notes with a `_index.md` lookup surface; makes completed work a reusable lesson instead of a
  dead artifact. Condensed from the [reverse-skill field-journal](https://github.com/zhaoxuya520/reverse-skill) (MIT).
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings