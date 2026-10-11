---
name: modules
description: Plane modules — feature and workstream grouping that cuts across sprints. Use when the user wants to group related work items by feature area, track progress of a larger feature over multiple sprints, create or manage modules, or ask about workstream progress. Modules complement cycles (time-boxed) by organizing work around outcomes (scope-boxed).
---

# Modules

Modules in Plane group work items by **scope** (feature, workstream, or outcome), in contrast to cycles which group by **time** (sprints). A single module can span multiple sprints and contain items owned by different people.

## Tool Name Resolution

Plane MCP exposes one `module` tool and the operation goes into the `action` parameter: `module(action=create, ...)`. This skill writes calls in that form. Resolve the real tool name (`mcp__<server>__module`) through the `connector-bootstrap` skill - never assume a server prefix.

## Available Calls

| Call | Purpose |
|------|---------|
| `module(action=list)` | List active modules in a project (`archived=true` lists archived ones; paginated) |
| `module(action=create)` | Create a new module |
| `module(action=retrieve)` | Get a module by UUID |
| `module(action=update)` | Update module details (name, lead, target date, status) |
| `module(action=delete)` | Delete a module |
| `module(action=archive)` / `module(action=unarchive)` | Archive lifecycle |
| `module(action=list_workitems)` | Get work items in a module (`pql` filter, paginated) |
| `module(action=manage_workitems)` | Add (`add_ids`) or remove (`remove_ids`) items in bulk |
| `workitem(action=count)` | Module totals per state group: `pql='module = "<module_id>"'` |

## When to Use a Module vs a Cycle

| Use a module when | Use a cycle when |
|-------------------|------------------|
| Grouping work around a feature or outcome | Grouping work into a time-boxed sprint |
| Work spans multiple sprints | Work is committed for the next 1–2 weeks |
| Tracking a workstream (mobile, billing, onboarding) | Tracking team commitment |
| Reporting progress to stakeholders by feature | Reporting progress to the team by sprint |

An item can live in **both** a module and a cycle simultaneously.

## Creating a Module

```
1. connector-bootstrap        → resolve tools and instance
2. project(action=list)      → pick project_id
3. member(action=list_project, project_id=<id>) → pick lead (UUID)
4. module(action=create,
     project_id=<id>,
     name="Billing v2",
     description="Revamp billing: Stripe migration, invoices, proration",
     lead=<user_uuid>,
     members=[<uuid>, <uuid>],
     start_date="YYYY-MM-DD",
     target_date="YYYY-MM-DD",
     status="planned")    // backlog | planned | in-progress | paused | completed | cancelled
```

## Adding Work Items to a Module

```
module(action=manage_workitems,
  project_id=<id>,
  module_id=<module_id>,
  add_ids=["<uuid>", "<uuid>", ...])
```

Items can come from any state — backlog, in-progress, or done. Adding a done item is valid; it counts toward module completion. `manage_workitems` returns nothing: read the result back with `module(action=list_workitems)`. To take items out pass `remove_ids=[...]` instead (the items stay in the project).

## Module Progress Reporting

```
1. workitem(action=count, project_id=<id>, pql='module = "<module_id>"', group_by=state__group)
   → item totals per state group in one call
   module(action=list_workitems, project_id=<id>, module_id=<module_id>, fields="id,name,point,estimate_point,state")
   → the items with points (follow next_cursor); pass pql='stateGroup = "completed"' for only the finished ones
2. Group items by state group: backlog | unstarted | started | completed | cancelled
3. Calculate:
   - total_items, total_points
   - completed_items, completed_points
   - completion_rate = completed_points / total_points
4. Surface blockers: workitem_relation(action=list) per open item, filter active blocked_by
```

Reporting table:

```
| Module | Status | Lead | Completion | Blocked | Target |
|--------|--------|------|-----------|---------|--------|
| Billing v2 | in-progress | @alice | 34/52 (65%) | 2 | Apr 30 |
```

## Module Lifecycle

1. **Planned** — scope defined, lead assigned, items drafted
2. **In Progress** — first items moved to "started"
3. **Paused** — explicitly deprioritized; lead re-assigns team
4. **Completed** — all items Done or explicitly dropped
5. **Cancelled** — abandoned; archive after retrospective

Always archive completed/cancelled modules to keep the active list clean:

```
module(action=archive, project_id=<id>, module_id=<module_id>)
```

**Caveat:** unlike `cycle(action=archive)` (which ends a running cycle first), the module tool documents no such behavior, and some Plane deployments reject archiving an **active** module (HTTP 400). If that happens, set `status="completed"` or `"cancelled"` with `module(action=update)` first, then archive; `module(action=unarchive)` reverses it. To remove an active module entirely, use `module(action=delete)` directly, after confirmation.

**Caveat:** if an `update` response looks empty or has mostly `null` fields, do not rely on it — refetch with `module(action=retrieve)` to get the post-update state.

## Best Practices

1. One lead per module — accountability is clearer.
2. Scope modules to 4–12 weeks of work. Smaller → use a cycle. Larger → use an epic or initiative.
3. Review module progress at each sprint review, not just at module end.
4. If a module stalls for 2 sprints, pause it explicitly — do not leave it "in progress".
5. Link the module's tracking page (see `pages-publishing`) in every work item description.