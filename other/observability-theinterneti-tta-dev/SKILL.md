---
name: observability
description: "Observability subsystem in TTA.dev: demo_hierarchical_trace, handle_api_active_agents, handle_api_agent_actions and related code. 115 symbols | 38 files | Cohesion: 73%"
---

# Observability

115 symbols | 38 files | Cohesion: 73%

## When to Use

- Working on `observability`-related functionality in TTA.dev
- Modifying `demo_hierarchical_trace`, `handle_api_active_agents`
- Navigating `ttadev/observability/server.py`, `ttadev/observability/project_session.py`

## Key Files

| File | Symbols |
|------|---------|
| `ttadev/observability/server.py` | _langfuse_creds, _estimate_cost, _v2_langfuse_session_cost, _v2_langfuse_scores, _init_state (+5) |
| `tests/observability/test_span_pipeline.py` | test_retry_succeeds_after_transient_failure, test_retry_exhausted_raises, test_retry_with_mock_primitive, test_cache_hit_skips_inner_primitive, _make_otel_span (+3) |
| `ttadev/observability/project_session.py` | join, get, get_by_id, add_member, assign_role (+2) |
| `ttadev/observability/span_processor.py` | from_activity_log, from_agent_tracker, extract_primitive_type, _normalize_provider, _parse_timestamp (+2) |
| `ttadev/observability/agent_tracker.py` | track_agent_action, log_activity, get_active_agents, get_recent_actions, get_tracker (+1) |
| `ttadev/primitives/observability/logging.py` | _log, debug, info, warning, error (+1) |
| `ttadev/observability/session_manager.py` | end_session_by_id, list_sessions, get_or_create_agent_session, update_session_project, _persist_session (+1) |
| `ttadev/observability/auto_instrument.py` | log_activity, log_tool_use, log_workflow_end, get_logger, log_workflow_start (+1) |
| `tests/observability/test_handoff_tracing.py` | _free_port, test_dag_endpoint_empty_when_no_handoffs, test_dag_endpoint_returns_nodes_and_edges, _make_agent_spec, test_handoff_span_emitted_with_required_attributes (+1) |
| `ttadev/observability/auto_track_copilot.py` | is_copilot_session, get_copilot_context, wrapper, track_workflow_execution, track_agent_activation |

## Entry Points

Start here when exploring this area:

- **`demo_hierarchical_trace`** (Function) — `examples/demo_hierarchical_traces.py:8`
- **`handle_api_active_agents`** (Function) — `ttadev/ui/observability_server.py:260`
- **`handle_api_agent_actions`** (Function) — `ttadev/ui/observability_server.py:270`
- **`track_agent_action`** (Function) — `ttadev/observability/agent_tracker.py:40`
- **`log_activity`** (Function) — `ttadev/observability/agent_tracker.py:68`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `demo_hierarchical_trace` | Function | `examples/demo_hierarchical_traces.py` | 8 |
| `handle_api_active_agents` | Function | `ttadev/ui/observability_server.py` | 260 |
| `handle_api_agent_actions` | Function | `ttadev/ui/observability_server.py` | 270 |
| `track_agent_action` | Function | `ttadev/observability/agent_tracker.py` | 40 |
| `log_activity` | Function | `ttadev/observability/agent_tracker.py` | 68 |
| `get_active_agents` | Function | `ttadev/observability/agent_tracker.py` | 107 |
| `get_recent_actions` | Function | `ttadev/observability/agent_tracker.py` | 165 |
| `get_tracker` | Function | `ttadev/observability/agent_tracker.py` | 182 |
| `join` | Function | `ttadev/observability/project_session.py` | 51 |
| `get` | Function | `ttadev/observability/project_session.py` | 58 |
| `get_by_id` | Function | `ttadev/observability/project_session.py` | 68 |
| `add_member` | Function | `ttadev/observability/project_session.py` | 87 |
| `assign_role` | Function | `ttadev/observability/project_session.py` | 96 |
| `main` | Function | `examples/demo_full_observability.py` | 62 |
| `test_retry_succeeds_after_transient_failure` | Function | `tests/observability/test_span_pipeline.py` | 234 |
| `test_retry_exhausted_raises` | Function | `tests/observability/test_span_pipeline.py` | 261 |
| `test_retry_with_mock_primitive` | Function | `tests/observability/test_span_pipeline.py` | 275 |
| `test_cache_hit_skips_inner_primitive` | Function | `tests/observability/test_span_pipeline.py` | 367 |
| `execute` | Function | `ttadev/primitives/recovery/retry.py` | 81 |
| `root` | Function | `ttadev/primitives/core/base.py` | 217 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Control_list_project_ownership → Get` | cross_community | 5 |
| `Demo_hierarchical_trace → _update_registry` | intra_community | 4 |
| `Main → Get_logger` | cross_community | 4 |
| `Wrapper → _update_registry` | cross_community | 4 |
| `Track_workflow_execution → _update_registry` | cross_community | 4 |
| `Track_agent_activation → _update_registry` | cross_community | 4 |
| `Control_list_project_ownership → _create_project_session_manager` | cross_community | 3 |
| `Control_list_session_ownership → Get_session` | cross_community | 3 |
| `Control_list_session_ownership → _create_session_manager` | cross_community | 3 |
| `Wrapper → Get_tracker` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 32 calls |
| Agents | 2 calls |
| Tools | 2 calls |
| Recovery | 1 calls |
| Control_plane | 1 calls |

## How to Explore

1. `gitnexus_context({name: "demo_hierarchical_trace"})` — see callers and callees
2. `gitnexus_query({query: "observability"})` — find related execution flows
3. Read key files listed above for implementation details
