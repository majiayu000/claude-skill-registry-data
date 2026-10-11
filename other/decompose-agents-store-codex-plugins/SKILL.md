---
name: decompose
description: 'Break down a work item into smaller stories/tasks using INVEST criteria Arguments: <work-item-identifier>.'
---

# Decompose

Break down a work item into smaller, sprint-ready stories or tasks using INVEST criteria and vertical slicing.

## Arguments
Format: `<work-item-identifier>`
- work-item-identifier: Item identifier like "MP-42" (required)

Parse from "$ARGUMENTS". The identifier (`MP-42`) goes to the server as one string.

## Process

0. **Bootstrap connector** — consult the `connector-bootstrap` skill. Probe `ToolSearch` for the Plane resource tools referenced below (`workitem`, `workitem_relation`); their names are `mcp__<server>__<resource>`, never assume a specific MCP prefix. If multiple Plane instances are connected, ask the user which one to use. All formulas and rules come from the `agile-fundamentals` skill. Calls are written `resource(action=..., ...)`.

1. **Retrieve the item:**
   ```
   workitem(action=retrieve_by_identifier, workitem_identifier="<PREFIX-N>")
   ```

2. **Analyze against INVEST criteria:**
   - Independent: check relations for hard dependencies
   - Negotiable: check description format
   - Valuable: check epic/business context
   - Estimable: check description detail
   - Small: check if points > 8
   - Testable: check acceptance criteria

3. **Propose decomposition:**
   Choose splitting pattern based on item type:
   - Workflow steps (most common)
   - Business rules
   - CRUD operations
   - Happy path vs edge cases
   - Data variations
   - Platform/interface

4. **Present proposed children:**
   | # | Child Item | Points | Rationale |
   |---|-----------|--------|-----------|

5. **On confirmation — create children:**
   ```
   For each child:
     workitem(action=create,
       project_id, name, parent=<parent_id>,
       point, priority, description_html)
   ```

6. **Set relations between children if needed:**
   ```
   workitem_relation(action=create, project_id, workitem_id=<child>, relation_type="blocked_by", workitem_ids=[<blocking child>])
   ```

## Example Usage
```
/decompose MP-42
/decompose TF-15
```