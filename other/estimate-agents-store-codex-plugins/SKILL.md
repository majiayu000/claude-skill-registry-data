---
name: estimate
description: 'Estimate unestimated work items using Fibonacci story points Arguments: <project> [--cycle <cycle-name>] [--scale fibonacci|tshirt].'
---

# Estimate

Batch estimate unestimated work items in the backlog or a specific sprint.

## Arguments
Format: `<project> [--cycle <cycle-name>] [--scale fibonacci|tshirt]`
- project: Project name or identifier (required)
- --cycle: Specific sprint to estimate items in (optional, defaults to full backlog)
- --scale: Estimation scale — fibonacci (default) or tshirt

Parse from "$ARGUMENTS".

## Process

0. **Bootstrap connector** — consult the `connector-bootstrap` skill. Probe `ToolSearch` for the Plane resource tools referenced below (`project`, `cycle`, `workitem`, `project_estimate`); their names are `mcp__<server>__<resource>`, never assume a specific MCP prefix. If multiple Plane instances are connected, ask the user which one to use. All formulas and rules come from the `agile-fundamentals` skill. Calls are written `resource(action=..., ...)`.

1. **Resolve project:**
   ```
   project(action=list)
   ```

2. **Get items to estimate:**
   If --cycle specified:
   ```
   cycle(action=list, project_id) → find cycle
   cycle(action=list_workitems, project_id, cycle_id)
   ```
   Otherwise:
   ```
   workitem(action=list, project_id, pql='stateGroup IN ("backlog","unstarted")', fields="id,name,point,estimate_point,priority", per_page=100)
   ```
   Filter: items where point is null or 0 (PQL has no estimate field; follow `next_cursor`). If the project has an estimate system (`project_estimate(action=retrieve, project_id)`), estimates are written as `estimate_point` ids from `project_estimate(action=list_points, project_id, estimate_id)` — see the `estimation` skill.

3. **Find reference stories (for calibration):**
   Look for completed items with known point values to anchor estimates.

4. **Estimate each item:**
   For each unestimated item:
   - Present: name, description, priority
   - Analyze: components touched, unknowns, dependencies
   - Suggest estimate with reasoning
   - If scale is tshirt: show XS/S/M/L/XL then map to Fibonacci

5. **On confirmation per item:**
   ```
   workitem(action=update, project_id, workitem_id, point=<value>)
   ```

6. **Flag oversized items:**
   Items > 8 points → suggest decomposition with /decompose.

7. **Summary:**
   Total items estimated, total points, items flagged for splitting.

## Example Usage
```
/estimate "TaskFlow"
/estimate "My Project" --cycle "Sprint 12"
/estimate "ShopFlow" --scale tshirt
```