---
name: fleet-architecture-health
description: How the architect monitors architecture health across the fleet — detecting drift, coupling violations, pattern inconsistency, and dependency direction breaks. Maps to arch_codebase_assessment and the weekly architecture-health-check CRON.
---

# Architecture Health Monitoring — Architect's Continuous Vigilance

10 agents working independently will naturally drift from the design. The engineer solves their immediate problem. The devops agent takes a shortcut. Over time, the architecture erodes. Your job is to DETECT drift before it becomes debt.

## What Constitutes Architecture Health

### 1. Dependency Direction

The fleet follows onion architecture. Dependencies point INWARD:

```
ALLOWED:
  fleet/mcp/tools.py → fleet/core/contributions.py  (outer → inner)
  fleet/cli/dispatch.py → fleet/core/model_selection.py  (outer → inner)
  fleet/infra/mc_client.py ← fleet/core/context_assembly.py  (core defines interface, infra implements)

VIOLATION:
  fleet/core/phases.py → fleet/infra/plane_client.py  (inner → outer)
  fleet/core/contributions.py → fleet/mcp/tools.py  (inner → outer)
```

Use the `dependency-mapper` sub-agent to trace import graphs without bloating your context.

### 2. Single Responsibility

Each module should do ONE thing. Warning signs:
- Module with 10+ public functions across different domains
- Class that reads config AND calls APIs AND transforms data AND writes files
- File over 500 lines (fleet convention — split when approaching)

Use the `pattern-analyzer` sub-agent to scan for responsibility violations.

### 3. Pattern Consistency

The fleet has established patterns (see fleet-design-pattern-selection skill). When agents introduce inconsistent patterns, flag them:
- Two different ways to access the same external service (one uses adapter, one calls directly)
- Mix of sync and async patterns for the same operation type
- Config loaded differently in different modules (some from YAML, some from env vars, some hardcoded)

### 4. Cross-Agent Drift

Agents work on different areas. Over time, the areas develop different conventions:
- One area uses dataclasses, another uses dicts
- One area has comprehensive error handling, another has bare except passes
- One area follows the event emission pattern, another doesn't

## The Health Check Process

### During Review (Reactive)

When reviewing a task via `arch_codebase_assessment`:
1. Identify the files touched by the task
2. Check dependency direction for each modified file
3. Check pattern consistency with surrounding code
4. Flag any architecture violations in your review comment

### CRON: Weekly Architecture Health Check (Proactive)

Your `architecture-health-check` CRON (config/agent-crons.yaml) runs weekly:

1. Scan key directories for dependency violations:
   - `fleet/core/` should NEVER import from `fleet/mcp/`, `fleet/cli/`, or `fleet/infra/`
   - `fleet/mcp/` can import from `fleet/core/` and `fleet/infra/`
   - `fleet/cli/` can import from everything (it's the outermost layer)

2. Check module sizes (files approaching 500 lines)

3. Detect new patterns that deviate from established ones

4. Produce architecture health report:
```
## Architecture Health Report — Week of {date}

### Dependency Direction
- Violations found: {N}
- {file}: imports {forbidden_import} (core → infra violation)

### Module Size
- Files approaching limit: {N}
- fleet/mcp/tools.py: {lines} lines (split candidates: {suggestions})

### Pattern Consistency
- Inconsistencies found: {N}
- {area}: uses dict where rest of codebase uses dataclass

### Drift Between Areas
- {observation}

### Recommendation
- Priority fixes: {list}
- Technical debt tasks to create: {list}
```

5. Post to board memory with tags `[architecture, health, report]`
6. If critical violations found: `fleet_alert(category="architecture", severity="high")`

## What You Do NOT Do

- Do NOT fix violations yourself (create tasks for the responsible agent)
- Do NOT block work for non-critical drift (flag it, track it, fix it later)
- Do NOT impose patterns beyond what the PO has approved (suggest patterns, PO decides)

Architecture health is a continuous practice, not a gate. You monitor, report, and recommend — the fleet acts.
