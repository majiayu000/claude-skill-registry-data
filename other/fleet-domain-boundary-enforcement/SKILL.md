---
name: fleet-domain-boundary-enforcement
description: How the architect enforces domain boundaries — core doesn't depend on infra, dependency direction is inward. The structural principle that keeps the codebase from becoming a tangled web.
---

# Domain Boundary Enforcement — Architect's Structural Principle

The fleet follows onion architecture. Inner layers define interfaces. Outer layers implement them. Dependencies point INWARD. When this principle erodes, the codebase becomes untestable, unmaintainable, and fragile.

## The Fleet's Layer Structure

```
OUTERMOST: fleet/cli/       — CLI commands, entry points
           fleet/mcp/       — MCP tools, server, roles
    MIDDLE: fleet/infra/     — External service clients (MC, IRC, GitHub, Plane, ntfy)
           fleet/templates/  — Output formatting
 INNERMOST: fleet/core/      — Domain logic, business rules, models
```

## The Rule

**Inner layers MUST NOT import from outer layers.**

| Import Direction | Example | Allowed? |
|-----------------|---------|----------|
| cli → core | `from fleet.core.model_selection import ...` | YES — outer uses inner |
| mcp → core | `from fleet.core.contributions import ...` | YES — outer uses inner |
| mcp → infra | `from fleet.infra.mc_client import ...` | YES — outer uses outer |
| core → infra | `from fleet.infra.plane_client import ...` | NO — inner depends on outer |
| core → mcp | `from fleet.mcp.tools import ...` | NO — inner depends on outer |
| core → cli | `from fleet.cli.dispatch import ...` | NO — inner depends on outer |

## How to Check

### During Design (Contribution)

When producing `design_input`, verify your proposed solution respects boundaries:
- Does the new module belong in `core/` or `infra/`?
- If `core/`: does it need external services? → Define an interface in core, implement in infra
- If `infra/`: does it call domain logic? → Import from core, don't duplicate

### During Review (Architecture Health)

Use the `dependency-mapper` sub-agent:
```
Agent: dependency-mapper
Prompt: "Scan fleet/core/ for imports from fleet/infra/, fleet/mcp/, or fleet/cli/.
        Report any violations of inward dependency direction."
```

### Manual Check

```bash
# Find core modules importing from infra
grep -rn "from fleet\.infra\|from fleet\.mcp\|from fleet\.cli" fleet/core/

# Should return NOTHING. Any match is a violation.
```

## Common Violations and Fixes

### Violation: Core imports infra client
```python
# BAD: fleet/core/contributions.py
from fleet.infra.mc_client import MCClient  # core depends on infra!
```
**Fix:** Core defines what it needs as a parameter. Caller provides the implementation.
```python
# GOOD: fleet/core/contributions.py
async def check_contribution_completeness(task_id, mc, board_id):
    # mc is passed in, not imported — core doesn't know about MCClient
    comments = await mc.list_comments(board_id, task_id)
```

### Violation: Core reads config files directly
```python
# BAD: fleet/core/phases.py
import yaml
with open("config/phases.yaml") as f:  # core knows about file paths!
```
**Fix:** Config loading belongs in infra or a config module. Core receives data.
```python
# GOOD: fleet/core/phases.py
def check_phase_standards(task, phase_config):
    # phase_config is loaded elsewhere and passed in
```

### Violation: Core emits to specific surfaces
```python
# BAD: fleet/core/contributions.py
from fleet.infra.irc_client import notify_irc  # core talks to IRC!
```
**Fix:** Core emits events. The chain runner (outer layer) routes to surfaces.
```python
# GOOD: fleet/core/event_chain.py
def build_contribution_chain(...):
    # Defines WHAT should happen. ChainRunner (mcp layer) executes HOW.
```

## Why This Matters

1. **Testability:** Core modules can be tested without external services. No mocking MC, IRC, Plane in core tests.
2. **Flexibility:** Swap MC backend without touching core logic. Swap IRC for Slack without touching contributions.
3. **Comprehensibility:** Reading `fleet/core/contributions.py` tells you the business rules without wading through HTTP calls.
4. **The fleet's 20 systems:** Each system crosses multiple layers. Enforcing boundaries keeps the crossings clean and traceable.

## Integration with Architecture Health CRON

Your weekly architecture-health-check CRON should include boundary verification as a standard check. Report violations in the architecture health report. Create tasks to fix structural violations before they spread.
