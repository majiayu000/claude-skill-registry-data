---
name: integrations
description: "Integrations area in TTA.dev (openhands_primitive and related). 60 symbols | 6 files | Cohesion: 82%"
---

# Integrations

60 symbols | 6 files | Cohesion: 82%

## When to Use

- Working on `integrations`-related functionality in TTA.dev
- Navigating `ttadev/primitives/integrations/openhands_primitive.py`, `ttadev/primitives/integrations/supabase_primitive.py`
- Understanding test coverage for this area

## Key Files

| File | Symbols |
|------|---------|
| `tests/primitives/integrations/test_langgraph_primitive.py` | _ctx, _make_graph, _make_primitive, test_injects_workflow_id, test_injects_session_id_when_present (+16) |
| `tests/primitives/integrations/test_openhands_primitive.py` | _ctx, _make_message_event, _make_conversation, test_returns_result_dict_on_success, test_send_message_called_with_task (+15) |
| `ttadev/primitives/integrations/openhands_primitive.py` | execute, _run, _execute_with_workspace, _build_agent, _extract_result (+2) |
| `ttadev/primitives/integrations/supabase_primitive.py` | execute, _execute_select, _execute_insert, _execute_update, _execute_delete |
| `ttadev/primitives/integrations/e2b_primitive.py` | _execute_impl, _create_sandbox, _maybe_rotate_session, cleanup |
| `ttadev/primitives/integrations/langgraph_primitive.py` | _build_config, stream_output, execute |

## Entry Points

Start here when exploring this area:

- **`test_injects_workflow_id`** (Function) — `tests/primitives/integrations/test_langgraph_primitive.py:100`
- **`test_injects_session_id_when_present`** (Function) — `tests/primitives/integrations/test_langgraph_primitive.py:106`
- **`test_injects_trace_id_when_present`** (Function) — `tests/primitives/integrations/test_langgraph_primitive.py:112`
- **`test_merges_with_base_config`** (Function) — `tests/primitives/integrations/test_langgraph_primitive.py:118`
- **`test_base_metadata_and_ctx_metadata_are_merged`** (Function) — `tests/primitives/integrations/test_langgraph_primitive.py:125`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `test_injects_workflow_id` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 100 |
| `test_injects_session_id_when_present` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 106 |
| `test_injects_trace_id_when_present` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 112 |
| `test_merges_with_base_config` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 118 |
| `test_base_metadata_and_ctx_metadata_are_merged` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 125 |
| `test_calls_ainvoke_with_input` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 140 |
| `test_injects_context_into_config` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 152 |
| `test_returns_ainvoke_result` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 162 |
| `test_chains_with_double_arrow` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 186 |
| `test_yields_chunks_from_astream` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 213 |
| `test_empty_stream_yields_nothing` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 226 |
| `test_execute_creates_otel_span` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 292 |
| `test_stream_output_creates_otel_span` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 345 |
| `test_no_otel_span_when_tracing_unavailable` | Function | `tests/primitives/integrations/test_langgraph_primitive.py` | 372 |
| `execute` | Function | `ttadev/primitives/integrations/openhands_primitive.py` | 415 |
| `test_returns_result_dict_on_success` | Function | `tests/primitives/integrations/test_openhands_primitive.py` | 146 |
| `test_send_message_called_with_task` | Function | `tests/primitives/integrations/test_openhands_primitive.py` | 175 |
| `test_run_called` | Function | `tests/primitives/integrations/test_openhands_primitive.py` | 192 |
| `test_conversation_always_closed` | Function | `tests/primitives/integrations/test_openhands_primitive.py` | 209 |
| `test_dict_with_task_key` | Function | `tests/primitives/integrations/test_openhands_primitive.py` | 240 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → _execute_with_workspace` | cross_community | 5 |
| `Main → Get_integration` | cross_community | 5 |
| `Main → _execute_with_workspace` | cross_community | 5 |
| `Main → Get_integration` | cross_community | 5 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 1 calls |
| Control_plane | 1 calls |

## How to Explore

1. `gitnexus_context({name: "test_injects_workflow_id"})` — see callers and callees
2. `gitnexus_query({query: "integrations"})` — find related execution flows
3. Read key files listed above for implementation details
