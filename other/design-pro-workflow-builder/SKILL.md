---
type: Skill
name: design-pro-workflow-builder
description: Design and execute DAG-based automation workflows using the NV oOS Pro Workflow Builder — a ReactFlow visual builder for chaining tool calls, agent runs, and actions into repeatable pipelines. Covers the visual builder UI, 9 preset categories, 10 node types, Kahn's algorithm execution engine, scheduling via Pro Schedule Manager, template variable syntax, and best practices. Use when designing workflows, debugging DAG execution failures, choosing between a workflow schedule and raw tool chaining, or building CRM/PM automation pipelines with toolkit_cpt nodes.
license: Proprietary. See LICENSE.txt
metadata:
  type: Skill
---

# NV oOS Pro Workflow Builder

The Pro Workflow Builder is a **ReactFlow-based visual DAG (Directed Acyclic Graph)
editor** for designing automation pipelines. You drag nodes onto a canvas, connect
them with edges, configure each node's parameters, and save the workflow. Saved
workflows can be executed immediately via `execute_workflow` or scheduled to run
on a recurring basis via the Pro Schedule Manager's `workflow_builder` schedule type.

## WP-CLI Commands

Key `mcp-ai` WP-CLI commands for workflow development. Run via `terminal`:

| Command | Use for |
|---|---|
| `wp mcp-ai health` | Verify all tools and providers before workflow execution |
| `wp mcp-ai queue` | Inspect queued workflow jobs, retry failures |
| `wp mcp-ai cron` | Check scheduled workflow-builder cron events |
| `wp mcp-ai log` | View per-node execution logs and error traces |
| `wp mcp-ai harness` | Semantic search across workflow outputs |

## When to use this skill

Trigger when ANY of the following is true:

- Designing a new workflow in the builder UI.
- Choosing a preset as a starting point for an automation pipeline.
- Deciding which node type to use (tool vs agent vs action).
- Connecting nodes with edges to form a multi-step DAG.
- Debugging a workflow that fails at a specific node.
- Understanding how the execution engine walks the DAG (topological sort).
- Scheduling a workflow to run on a recurring basis.
- Deciding between a workflow-builder workflow vs raw step-by-step tool chaining.
- Using template variables to reference upstream node results.

## Mental model — DAGs, node types, and execution

A workflow is a **graph**:

```
nodes: the boxes on the canvas (what to do)
edges: the arrows connecting them (what order to do it in)
```

The execution engine uses **Kahn's algorithm** for topological sort — it walks
the graph from root nodes to leaf nodes, executing each in dependency order.
If the graph contains a cycle, execution is rejected with an error.

Each node's result is stored in a **shared context** keyed by node ID. Downstream
nodes can access upstream results via template variables like `{{node_id.result}}`.

Workflows are stored in the `wp_mcp_ai_pro_workflows` WordPress option. They can
be scheduled via the Pro Schedule Manager as `workflow_builder` type schedules.

## The visual builder

Access at: `/wp-admin/admin.php?page=nvoos-pro-workflow-builder`

The builder is a ReactFlow-powered canvas where you:

1. **Drag node types** from a palette onto the canvas.
2. **Configure each node** with tool/agent/action parameters.
3. **Connect nodes with edges** to define execution order.
4. **Save the workflow** (stored to `wp_mcp_ai_pro_workflows` option).
5. **Execute or schedule** the completed workflow.

## Node types

### Execution nodes (produce results)

| Node type | What it does | Configuration |
|---|---|---|
| **trigger** | Entry point — starts the DAG. No execution. | None. Always the first node. |
| **tool** | Calls an MCP tool via the Tool Registry. This includes `toolkit_cpt` for CRM/PM record operations (leads, deals, tasks, projects). | `tool_name` (required), `arguments` (object) |
| **action** | Fires the `wp_mcp_ai_workflow_execute_action` filter. Extensible by plugins. | `command` (string), `params` (object) |
| **agent** | Fires `wp_mcp_ai_workflow_execute_agent` filter — typically invokes an AI assistant. | `agent_id`, `prompt` |

### Control-flow nodes (pass-through in server-side execution)

| Node type | Purpose |
|---|---|
| **condition** | Branching logic (pass-through in scheduled execution; interactive in live runs). |
| **delay** | Time-based waiting (pass-through — schedule handles timing). |
| **parallel** | Fork execution into multiple paths. |
| **merge** | Join parallel paths back into a single flow. |
| **loop** | Repeated execution (pass-through — schedule handles repetition). |
| **approval** | Human-in-the-loop gate (pass-through in automated execution). |

> **Note:** Control-flow nodes are pass-through in server-side scheduled execution
> because the schedule manager executes nodes linearly in topological order. Their
> visual role in the builder helps communicate intent and structure.

## Template variables

Tool nodes can reference context and upstream node results using `{{...}}` syntax:

| Variable | Resolves to |
|---|---|
| `{{input.topic}}` | Value entered in a trigger/input node's `topic` field. |
| `{{node_id.result}}` | The result object from a previously executed node. |
| `{{node_id.result.field}}` | A specific field within a node's result. |
| `{{schedule_id}}` | The ID of the schedule running the workflow. |
| `{{schedule_name}}` | Human-readable name of the schedule. |

**Example — a blog post pipeline:**

```
Node 1 (trigger):    topic = "sri lankan street food"
Node 2 (web_search): query = "{{input.topic}}"
Node 3 (summarize):  content = "{{node_2.result.summary}}"
```

## Preset categories (9)

Pre-built workflow templates loadable into the builder:

| Category | Slug | Example workflows |
|---|---|---|
| Content Creation | `content` | Blog post pipeline, newsletter builder, social media calendar |
| SEO | `seo` | Site audit, keyword cluster, internal link builder |
| E-Commerce | `ecommerce` | Product launch, bulk price update, inventory sync |
| Marketing | `marketing` | Campaign launch, A/B test, ROI analysis |
| Data | `data` | Report generation, data import, analysis pipeline |
| Communication | `communication` | Multi-channel broadcast, support escalation |
| Maintenance | `maintenance` | Backup workflow, security scan, performance check |
| Onboarding | `onboarding` | User onboarding sequence, content migration |
| CRM Support | `crm_support` | Ticket triage, customer follow-up, SLA monitoring |

Presets are defined in `WP_MCP_AI_Pro_Workflow_Presets` and loaded via
`install_preset($preset_id)`. Each preset includes pre-built nodes and edges
ready for the canvas.

## Execution model (server-side)

When a workflow runs — either via `execute_workflow` or as a scheduled
`workflow_builder` run — the execution engine:

1. **Loads** the workflow from `wp_mcp_ai_pro_workflows` option.
2. **Validates** there are nodes and no cycles.
3. **Builds adjacency list** from edges (source → target mappings).
4. **Topologically sorts** nodes using Kahn's algorithm.
5. **Executes** each node in order:
   - **trigger**: no-op (pass-through).
   - **tool**: Resolves `{{...}}` template variables, looks up the tool in the Tool Registry, calls `$tool->execute($arguments, $context)`. Fails if the tool is not found or fails.
   - **action**: Fires `wp_mcp_ai_workflow_execute_action` filter with `$command`, `$params`, and context. Falls back to a `completed` status.
   - **agent**: Fires `wp_mcp_ai_workflow_execute_agent` filter with `$agent_id`, `$prompt`, and context. Falls back to a `completed` status.
   - **control-flow** (condition, delay, parallel, merge, loop, approval): Pass-through with `completed` status.
6. **Stops immediately** if any node returns a `WP_Error`.
7. **Returns** all node results keyed by node ID.

## Common patterns

### Chaining tools in sequence

```
[Trigger] → [web_search] → [summarize] → [create_post]
```

Each step feeds into the next. The `create_post` tool receives the summary
from the `summarize` node via `{{node_summarize.result}}`.

### Research → generate → publish

```
[Trigger: topic]
   → [web_search: "{{input.topic}}"]
   → [deep_research: "{{input.topic}}"]
   → [generate_outline]
   → [write_draft]
   → [optimize_seo]
   → [publish_post]
```

### Multi-step with parallel branches

```
                → [check_inventory]
[Trigger: sku] →                     → [merge] → [notify_channel]
                → [check_pricing]   →
```

Both `check_inventory` and `check_pricing` run (in topological order — effectively
sequentially in scheduled execution), then results merge and trigger a notification.

### Scheduling a workflow

1. Design and save the workflow in the builder.
2. In Pro Schedule Manager, create a `workflow_builder` type schedule.
3. Set `workflow_builder_id` to the saved workflow's ID.
4. Configure recurrence, notifications, timeout, etc.
5. Use `dry_run_pro_schedule` to test before enabling.

## Integration with Pro Schedule Manager

Workflows become schedules via the `workflow_builder` schedule type:

```
Pro Workflow Builder          Pro Schedule Manager
─────────────────────         ─────────────────────
Design DAG (visual)    ───→   Schedule (workflow_builder type)
Save to option store   ───→   workflow_builder_id reference
(Node types: trigger,  ───→   dispatch_workflow_builder()
 tool, action, agent,
 condition, delay, ...)
```

The schedule manager:
- Validates the workflow exists at schedule creation time.
- Loads and executes the DAG via `dispatch_workflow_builder()`.
- Records node-level results in the run history.
- Extracts a human-readable response from the last agent/tool node.

## Critical rules

- **Workflows must be acyclic.** The engine rejects DAGs with cycles.
- **Every workflow needs at least one trigger node** as the entry point.
- **Tool nodes require a registered tool.** The tool must exist in the Tool Registry or the node fails.
- **Template variables are resolved at execution time**, not validation time. A typo in `{{node_id.result}}` won't cause an error — it'll pass the literal string.
- **Control-flow nodes are pass-through in scheduled execution.** Don't rely on conditions or delays server-side — put that logic in the schedule configuration.
- **Node results are available to downstream nodes** via the `node_results` context keyed by node ID.
- **Execution stops at the first failure.** If node 3 of 10 fails, nodes 4-10 never run.
- **Scheduling a workflow creates a snapshot reference**, not a live link. Updating the workflow later does not auto-update existing schedules.
- **Use `dry_run_pro_schedule`** before enabling a new workflow schedule.

## Common mistakes

```
WRONG — workflow has a cycle
[trigger] → [tool_a] → [tool_b] → [tool_a]
Error: "Workflow contains a cycle and cannot be executed."

WRONG — missing trigger node
[tool_a] → [tool_b] → [tool_c]
Execution may still work (the engine doesn't require a trigger for execution),
but the builder UI expects a trigger as the visual entry point.

WRONG — referencing a tool that doesn't exist
Tool node with tool_name: "my_custom_tool"
Error: 'Tool "my_custom_tool" not found.'

WRONG — expecting condition nodes to branch at schedule time
[trigger] → [condition: is_weekend?] → [send_report]
The condition is pass-through in scheduled execution. Use separate schedules
for the two branches instead.

RIGHT — two separate schedules for conditional logic
Schedule A (weekdays): [trigger] → [send_daily_report]
Schedule B (weekends): [trigger] → [send_weekly_summary]

WRONG — updating a workflow and expecting existing schedules to pick up changes
1. Create workflow W1, save as workflow_builder schedule S1.
2. Edit W1 (add a node, change arguments).
3. S1 still runs the old version.
RIGHT — update the schedule or recreate it after workflow changes.

WRONG — passing large objects as template variables
tool node arguments: { "full_report": "{{node_2.result}}" }
Node results can be large nested objects. Extract only what you need.
RIGHT: { "summary": "{{node_2.result.summary}}", "urls": "{{node_2.result.sources}}" }
```

## Cross-references

- Run `wp-pro-schedule-manager` to schedule a workflow as a `workflow_builder` type schedule — covers `create_pro_schedule`, `dry_run_pro_schedule`, `get_schedule_run_history`.
- Run `wp-action-scheduler` for the underlying queue infrastructure that runs scheduled workflows.
- Run `wp-plugin-cron` for the cron mechanics that trigger scheduled workflow runs.
- Run `mcp-ai-wpoos-plugin` for details on available tools you can use in tool nodes (the Tool Registry).
- The `execute_workflow` MCP tool is the programmatic interface for running workflows on-demand.
- Run `design-crm` to build CRM automation workflows — lead scoring, auto-assignment, deal stage progression using `toolkit_cpt` nodes in the builder.
- Run `design-project-management` to build PM automation workflows — task creation from templates, sprint status roll-ups, project health checks.

## What this skill does NOT cover

- The Pro Schedule Manager tools — covered by `wp-pro-schedule-manager`.
- Action Scheduler internals — covered by `wp-action-scheduler`.
- Writing custom action/agent filter handlers — plugin development topic.
- The `execute_workflow` MCP tool interface — use the `mcp-ai-wpoos-plugin` skill.

## References

- NV oOS Pro Workflow Builder: `/wp-admin/admin.php?page=nvoos-pro-workflow-builder`
- Pro Schedule Manager: `/wp-admin/admin.php?page=nvoos-pro-schedule-manager`
- `WP_MCP_AI_Pro_Workflow_Presets` class: `includes/class-wp-mcp-ai-pro-workflow-presets.php` (9 preset categories)
- `dispatch_workflow_builder()`: `includes/class-wp-mcp-ai-pro-schedule-manager.php` (execution engine)
