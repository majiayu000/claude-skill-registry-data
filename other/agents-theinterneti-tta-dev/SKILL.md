---
name: agents
description: "Agents subsystem in TTA.dev: handle_agent_command, get, get_registry and related code. 66 symbols | 24 files | Cohesion: 72%"
---

# Agents

66 symbols | 24 files | Cohesion: 72%

## When to Use

- Working on `agents`-related functionality in TTA.dev
- Modifying `handle_agent_command`, `get`
- Navigating `ttadev/cli/agent.py`, `ttadev/agents/registry.py`

## Key Files

| File | Symbols |
|------|---------|
| `tests/agents/test_spawn_agent_model_injection.py` | _make_spec, _make_model_aware_agent, _make_legacy_agent, test_spawn_agent_context_default_model_no_type_error, test_spawned_agent_has_non_none_model (+5) |
| `tests/agents/test_registry.py` | test_register_and_get, test_register_overwrites, test_global_restored_after_context, test_override_restored_on_exception, test_all_returns_registered (+3) |
| `tests/agents/test_tool_call_loop.py` | _make_anthropic_response, _make_google_response, test_parse_anthropic_tool_calls, test_parse_anthropic_multiple_tool_calls, test_parse_google_tool_calls (+3) |
| `tests/agents/test_router.py` | _make_registry, _make_router, test_agent_hint_bypasses_scoring, test_keyword_routing_no_llm_call, test_ambiguous_task_calls_orchestrator (+2) |
| `ttadev/cli/agent.py` | handle_agent_command, _cmd_list, _cmd_show, _cmd_run, _run_agent |
| `ttadev/agents/registry.py` | get, get_registry, all |
| `ttadev/agents/router.py` | _get_model, _get_orchestrator, _execute_impl |
| `ttadev/agents/base.py` | __init__, _execute_impl, _spawn_with_handoff_span |
| `tests/agents/test_spec.py` | _make_result, test_construction, test_failing_gate |
| `tests/agents/test_agent_primitive.py` | _make_spec, __init__ |

## Entry Points

Start here when exploring this area:

- **`handle_agent_command`** (Function) — `ttadev/cli/agent.py:54`
- **`get`** (Function) — `ttadev/agents/registry.py:28`
- **`get_registry`** (Function) — `ttadev/agents/registry.py:51`
- **`test_all_agents_registered`** (Function) — `tests/workflows/test_prebuilt.py:26`
- **`test_registered_after_import`** (Function) — `tests/agents/test_security.py:76`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `handle_agent_command` | Function | `ttadev/cli/agent.py` | 54 |
| `get` | Function | `ttadev/agents/registry.py` | 28 |
| `get_registry` | Function | `ttadev/agents/registry.py` | 51 |
| `test_all_agents_registered` | Function | `tests/workflows/test_prebuilt.py` | 26 |
| `test_registered_after_import` | Function | `tests/agents/test_security.py` | 76 |
| `test_register_and_get` | Function | `tests/agents/test_registry.py` | 18 |
| `test_register_overwrites` | Function | `tests/agents/test_registry.py` | 40 |
| `test_global_restored_after_context` | Function | `tests/agents/test_registry.py` | 54 |
| `test_override_restored_on_exception` | Function | `tests/agents/test_registry.py` | 61 |
| `test_registered_after_import` | Function | `tests/agents/test_qa.py` | 78 |
| `test_registered_after_import` | Function | `tests/agents/test_performance.py` | 86 |
| `test_registered_after_import` | Function | `tests/agents/test_github.py` | 83 |
| `test_registered_after_import` | Function | `tests/agents/test_git.py` | 70 |
| `test_registered_after_import` | Function | `tests/agents/test_devops.py` | 86 |
| `test_registered_after_import` | Function | `tests/agents/test_developer.py` | 76 |
| `test_spawn_agent_context_default_model_no_type_error` | Function | `tests/agents/test_spawn_agent_model_injection.py` | 95 |
| `test_spawned_agent_has_non_none_model` | Function | `tests/agents/test_spawn_agent_model_injection.py` | 120 |
| `test_spawn_agent_explicit_model_kwarg` | Function | `tests/agents/test_spawn_agent_model_injection.py` | 142 |
| `test_explicit_model_takes_precedence_over_context_default` | Function | `tests/agents/test_spawn_agent_model_injection.py` | 161 |
| `test_legacy_agent_still_works_no_model_param` | Function | `tests/agents/test_spawn_agent_model_injection.py` | 187 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 33 calls |
| Llm | 2 calls |
| Observability | 1 calls |

## How to Explore

1. `gitnexus_context({name: "handle_agent_command"})` — see callers and callees
2. `gitnexus_query({query: "agents"})` — find related execution flows
3. Read key files listed above for implementation details
