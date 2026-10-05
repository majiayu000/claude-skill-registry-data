---
name: tools
description: "Tools subsystem in TTA.dev: list_active_ownership, control_start_workflow, control_mark_workflow_step_running and related code. 35 symbols | 6 files | Cohesion: 85%"
---

# Tools

35 symbols | 6 files | Cohesion: 85%

## When to Use

- Working on `tools`-related functionality in TTA.dev
- Modifying `list_active_ownership`, `control_start_workflow`
- Navigating `ttadev/primitives/mcp_server/tools/control_plane.py`, `ttadev/primitives/mcp_server/tools/_helpers.py`

## Key Files

| File | Symbols |
|------|---------|
| `ttadev/primitives/mcp_server/tools/control_plane.py` | control_create_task, control_list_tasks, control_get_task, control_claim_task, control_decide_gate (+13) |
| `ttadev/primitives/mcp_server/tools/_helpers.py` | _paginate, _create_control_plane_service, _serialize_task, _serialize_run, _serialize_lease (+4) |
| `ttadev/primitives/mcp_server/tools/workflow.py` | control_start_workflow, control_mark_workflow_step_running, control_record_workflow_step_result, control_record_workflow_gate_outcome, control_mark_workflow_step_failed |
| `ttadev/control_plane/service.py` | list_active_ownership |
| `ttadev/primitives/mcp_server/tools/primitives.py` | tta_bootstrap |
| `ttadev/primitives/mcp_server/tools/observability.py` | _get_providers_status |

## Entry Points

Start here when exploring this area:

- **`list_active_ownership`** (Function) — `ttadev/control_plane/service.py:181`
- **`control_start_workflow`** (Function) — `ttadev/primitives/mcp_server/tools/workflow.py:22`
- **`control_mark_workflow_step_running`** (Function) — `ttadev/primitives/mcp_server/tools/workflow.py:81`
- **`control_record_workflow_step_result`** (Function) — `ttadev/primitives/mcp_server/tools/workflow.py:126`
- **`control_record_workflow_gate_outcome`** (Function) — `ttadev/primitives/mcp_server/tools/workflow.py:175`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `list_active_ownership` | Function | `ttadev/control_plane/service.py` | 181 |
| `control_start_workflow` | Function | `ttadev/primitives/mcp_server/tools/workflow.py` | 22 |
| `control_mark_workflow_step_running` | Function | `ttadev/primitives/mcp_server/tools/workflow.py` | 81 |
| `control_record_workflow_step_result` | Function | `ttadev/primitives/mcp_server/tools/workflow.py` | 126 |
| `control_record_workflow_gate_outcome` | Function | `ttadev/primitives/mcp_server/tools/workflow.py` | 175 |
| `control_mark_workflow_step_failed` | Function | `ttadev/primitives/mcp_server/tools/workflow.py` | 221 |
| `control_create_task` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 31 |
| `control_list_tasks` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 67 |
| `control_get_task` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 92 |
| `control_claim_task` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 108 |
| `control_decide_gate` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 147 |
| `control_reopen_gate` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 181 |
| `control_list_locks` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 209 |
| `control_acquire_workspace_lock` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 232 |
| `control_acquire_file_lock` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 255 |
| `control_release_lock` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 278 |
| `control_list_runs` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 294 |
| `control_get_run` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 317 |
| `control_heartbeat_run` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 337 |
| `control_complete_run` | Function | `ttadev/primitives/mcp_server/tools/control_plane.py` | 358 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Control_list_project_ownership → Get` | cross_community | 5 |
| `Control_start_workflow → To_dict` | cross_community | 4 |
| `Control_claim_task → To_dict` | cross_community | 4 |
| `Control_mark_workflow_step_running → To_dict` | cross_community | 4 |
| `Control_record_workflow_step_result → To_dict` | cross_community | 4 |
| `Control_record_workflow_gate_outcome → To_dict` | cross_community | 4 |
| `Control_mark_workflow_step_failed → To_dict` | cross_community | 4 |
| `Control_list_tasks → To_dict` | cross_community | 4 |
| `Control_create_task → To_dict` | cross_community | 4 |
| `Control_get_task → To_dict` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 16 calls |
| Control_plane | 9 calls |
| Observability | 2 calls |

## How to Explore

1. `gitnexus_context({name: "list_active_ownership"})` — see callers and callees
2. `gitnexus_query({query: "tools"})` — find related execution flows
3. Read key files listed above for implementation details
