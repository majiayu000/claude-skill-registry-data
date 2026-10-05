---
name: gateway-doctor
description: Use when diagnose and fix MCP gateway routing issues, health checks,
  and server connectivity problems. Use when working with gateway doctor.
domain: core
author: oyi77
license: Apache-2.0
subdomain: core-platform
tags:
- doctor
- gateway
- infrastructure
- memory
- self-improvement
persona:
  name: Brendan Gregg
  title: The Systems Performance Expert - Master of Diagnostics
  expertise:
  - System Diagnostics
  - Performance Analysis
  - Observability
  - Troubleshooting
  philosophy: Performance issues are just bugs you haven't found yet.
  credentials:
  - Senior Performance Engineer at Netflix
  - Authored 'Systems Performance' book
  - Created DTrace tools
  principles:
  - Measure everything
  - Find the bottleneck
  - Optimize the critical path
  - Monitor continuously
version: 1.0.0
category: core
---

# Gateway Doctor

## When to Use
**Trigger phrases:**
- "Brendan Gregg"
- "Diagnose and fix MCP gateway routing issues, health checks, and server connectiv"


- Periodic health checks (1 min interval)
- User reports lag
- After system sleep/resume
- Gateway unresponsive


## When NOT to Use

- When the task can be solved with existing standard libraries
- When the infrastructure is already in place and working
- When the added complexity does not provide measurable benefit


## Overview

Gateway Doctor is a foundational core infrastructure skill that provides system foundation capabilities for the agent ecosystem.

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
1. **Execute** — Run gateway doctor workflow with configured parameters
1. **Verify** — Validate output meets requirements, document results

## Verification

- [ ] All steps executed successfully
- [ ] Results validated against acceptance criteria
- [ ] Error handling tested with edge cases
- [ ] Documentation updated with findings