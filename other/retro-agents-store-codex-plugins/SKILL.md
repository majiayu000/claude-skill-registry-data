---
name: retro
description: 'Run a sprint retrospective and create action items Arguments: <project> [--format start-stop-continue|daki|4ls].'
---

# Retro

Run a sprint retrospective — present metrics, collect team feedback, create action items, save notes.

## Arguments
Format: `<project> [--format start-stop-continue|daki|4ls]`
- project: Project name or identifier (required)
- --format: Retro format (default: start-stop-continue)

Parse from "$ARGUMENTS".

## Process

0. **Bootstrap connector** — consult the `connector-bootstrap` skill. Probe `ToolSearch` for the Plane resource tools referenced below (`project`, `cycle`, `workitem`, `label`, `page`); their names are `mcp__<server>__<resource>`, never assume a specific MCP prefix. If multiple Plane instances are connected, ask the user which one to use. All formulas and rules come from the `agile-fundamentals` skill. Calls are written `resource(action=..., ...)`.

1. **Get sprint data:**
   ```
   cycle(action=list, project_id, status=current)       // or status=completed for the sprint that just ended
   ```
   Find active or most recently completed cycle.
   ```
   cycle(action=list_workitems, project_id, cycle_id)
   workitem(action=count, project_id, pql='cycle = "<cycle_id>"', group_by=state__group)
   ```
   Review the previous retro's actions first: `workitem(action=list, project_id, pql='label = "<retro-action-label-id>"')`.

2. **Generate sprint metrics:**
   - Completion rate (points and items)
   - Velocity vs historical average
   - Scope changes (items added/removed mid-sprint)
   - Blockers encountered

3. **Present retro template:**
   Based on --format:

   **start-stop-continue:**
   - What should we START doing?
   - What should we STOP doing?
   - What should we CONTINUE doing?

   **daki:**
   - DROP: What's not working?
   - ADD: What new practices to adopt?
   - KEEP: What's working well?
   - IMPROVE: What can be better?

   **4ls:**
   - LIKED: What did we enjoy?
   - LEARNED: What did we learn?
   - LACKED: What was missing?
   - LONGED FOR: What do we wish we had?

4. **Collect team input** (interactive conversation)

5. **Create action items (max 2-3):**
   ```
   workitem(action=create,
     project_id, name="[RETRO] <action>",
     priority="high", labels=["<retro-action-label-id>"],
     assignees=["<owner>"], target_date="<next sprint end>")
   ```

6. **Save retro notes:**
   ```
   page(action=create,
     project_id,
     name="Retro — <sprint name> (<date>)",
     description_html="<formatted retro notes>")
   ```

## Example Usage
```
/retro "TaskFlow"
/retro "My Project" --format daki
/retro "ShopFlow" --format 4ls
```