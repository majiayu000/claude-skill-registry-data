---
name: control-plane
description: "Control-Plane subsystem in TTA.dev: get_task, get_run, put_run and related code. 88 symbols | 15 files | Cohesion: 81%"
---

# Control_plane

88 symbols | 15 files | Cohesion: 81%

## When to Use

- Working on `control-plane`-related functionality in TTA.dev
- Modifying `get_task`, `get_run`
- Navigating `ttadev/control_plane/store.py`, `ttadev/control_plane/workflow_service.py`

## Key Files

| File | Symbols |
|------|---------|
| `ttadev/control_plane/store.py` | _read_map, _write_map, _lock_for, get_task, get_run (+10) |
| `ttadev/control_plane/workflow_service.py` | _emit_control_plane_span, _now_iso, _make_workflow_gate_id, _get_workflow_step, _build_workflow_gate_decision_record (+6) |
| `ttadev/control_plane/task_service.py` | _now, _now_iso, _current_agent_id, _find_gate, _ensure_gate_decider_allowed (+6) |
| `ttadev/control_plane/lease_service.py` | _now, _now_iso, _validate_lock_owner, _acquire_lock, _expire_lease (+6) |
| `ttadev/control_plane/run_service.py` | _now, _now_iso, get_run, get_lease_for_run, list_active_ownership (+5) |
| `ttadev/control_plane/models.py` | to_dict, to_dict, from_dict, to_dict, from_dict (+4) |
| `ttadev/control_plane/service.py` | list_runs, get_run, get_lease_for_run, heartbeat_run, acquire_file_lock (+2) |
| `tests/unit/test_l0_store.py` | _now, test_task_roundtrip, test_run_roundtrip, test_lease_roundtrip_and_delete |
| `ttadev/cli/control.py` | _handle_run_command, _handle_lock_command |
| `tests/unit/test_control_plane_trace_attribution.py` | test_claim_task_stamps_trace_id_on_run, test_workflow_step_round_trips_trace_fields |

## Entry Points

Start here when exploring this area:

- **`get_task`** (Function) — `ttadev/control_plane/store.py:51`
- **`get_run`** (Function) — `ttadev/control_plane/store.py:66`
- **`put_run`** (Function) — `ttadev/control_plane/store.py:71`
- **`list_leases`** (Function) — `ttadev/control_plane/store.py:77`
- **`get_lease_for_task`** (Function) — `ttadev/control_plane/store.py:81`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `get_task` | Function | `ttadev/control_plane/store.py` | 51 |
| `get_run` | Function | `ttadev/control_plane/store.py` | 66 |
| `put_run` | Function | `ttadev/control_plane/store.py` | 71 |
| `list_leases` | Function | `ttadev/control_plane/store.py` | 77 |
| `get_lease_for_task` | Function | `ttadev/control_plane/store.py` | 81 |
| `put_lease` | Function | `ttadev/control_plane/store.py` | 92 |
| `delete_lease` | Function | `ttadev/control_plane/store.py` | 98 |
| `put_lock` | Function | `ttadev/control_plane/store.py` | 123 |
| `delete_lock` | Function | `ttadev/control_plane/store.py` | 129 |
| `to_dict` | Function | `ttadev/control_plane/models.py` | 481 |
| `to_dict` | Function | `ttadev/control_plane/models.py` | 528 |
| `from_dict` | Function | `ttadev/control_plane/models.py` | 539 |
| `to_dict` | Function | `ttadev/control_plane/models.py` | 563 |
| `test_task_roundtrip` | Function | `tests/unit/test_l0_store.py` | 12 |
| `test_run_roundtrip` | Function | `tests/unit/test_l0_store.py` | 31 |
| `test_lease_roundtrip_and_delete` | Function | `tests/unit/test_l0_store.py` | 50 |
| `get_run` | Function | `ttadev/control_plane/run_service.py` | 160 |
| `get_lease_for_run` | Function | `ttadev/control_plane/run_service.py` | 167 |
| `list_active_ownership` | Function | `ttadev/control_plane/run_service.py` | 171 |
| `claim_task` | Function | `ttadev/control_plane/run_service.py` | 213 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → Get_integration` | cross_community | 5 |
| `Main → Get_integration` | cross_community | 5 |
| `Main → Get_integration` | cross_community | 4 |
| `Acquire_workspace_lock → Release_locks_for_run` | intra_community | 4 |
| `Acquire_file_lock → Release_locks_for_run` | intra_community | 4 |
| `Finalize_tracked_workflow → _now` | intra_community | 4 |
| `Decide_gate → _get_active_session` | intra_community | 3 |
| `Decide_gate → _gate_role_matches` | intra_community | 3 |
| `Control_claim_task → To_dict` | cross_community | 3 |
| `Control_get_run → To_dict` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 17 calls |
| Cli | 2 calls |

## How to Explore

1. `gitnexus_context({name: "get_task"})` — see callers and callees
2. `gitnexus_query({query: "control_plane"})` — find related execution flows
3. Read key files listed above for implementation details
