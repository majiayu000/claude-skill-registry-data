---
name: llm
description: "Llm subsystem in TTA.dev: execute and related code. 171 symbols | 30 files | Cohesion: 67%"
---

# Llm

171 symbols | 30 files | Cohesion: 67%

## When to Use

- Working on `llm`-related functionality in TTA.dev
- Modifying `execute`
- Navigating `ttadev/primitives/llm/hardware_detector.py`, `ttadev/primitives/llm/ollama_primitive.py`

## Key Files

| File | Symbols |
|------|---------|
| `tests/primitives/llm/test_model_router.py` | _make_router, _ctx, test_raises_value_error_for_unknown_mode, test_error_message_lists_available_modes, test_calls_ollama_and_returns_response (+27) |
| `tests/primitives/llm/test_task_selector.py` | test_known_coding_model_scores_above_zero, test_returns_float_between_0_and_1, test_gemini_flash_scores_for_coding, test_unknown_model_with_large_params_scores_above_tiny, test_completely_unknown_model_gets_minimal_score (+11) |
| `ttadev/primitives/llm/hardware_detector.py` | max_params_b, summary, to_dict, detect, filter_ollama_models (+10) |
| `ttadev/primitives/llm/ollama_primitive.py` | _get_client, _list_models, _running_models, _show_model, _pull_model (+6) |
| `tests/primitives/llm/test_hardware_detector.py` | test_detect_cached, test_detect_force_re_reads, _profile, test_can_run_small_model_on_4gb_gpu, test_cannot_run_70b_on_4gb_gpu_limited_ram (+5) |
| `ttadev/primitives/llm/provider_dispatch.py` | build_openai_tool_kwargs, call_openai_compat, call_openai, call_openrouter, call_xai (+4) |
| `tests/primitives/llm/test_model_advisor.py` | test_recommend_tier_threshold_met_returns_valid_model, test_recommend_tier_ollama_preferred_when_score_meets_threshold, _make_tier_map, test_recommend_tier_returns_tier_recommendation, test_recommend_tier_no_threshold_met_returns_best_available (+4) |
| `ttadev/primitives/llm/model_registry.py` | _list, _has_benchmark, _select, _key, _get (+3) |
| `ttadev/primitives/llm/task_selector.py` | general, _extract_param_size_b, score_model_for_task, sort_key, coding (+2) |
| `tests/primitives/llm/test_free_model_tracker.py` | _make_httpx_response, test_returns_only_free_models, test_passes_api_key_as_auth_header, test_no_api_key_sends_no_auth_header, test_handles_null_pricing_gracefully (+2) |

## Entry Points

Start here when exploring this area:

- **`execute`** (Function) — `ttadev/primitives/llm/model_router.py:351`
- **`test_raises_value_error_for_unknown_mode`** (Function) — `tests/primitives/llm/test_model_router.py:164`
- **`test_error_message_lists_available_modes`** (Function) — `tests/primitives/llm/test_model_router.py:173`
- **`test_calls_ollama_and_returns_response`** (Function) — `tests/primitives/llm/test_model_router.py:187`
- **`test_ollama_tier_without_model_raises`** (Function) — `tests/primitives/llm/test_model_router.py:210`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `execute` | Function | `ttadev/primitives/llm/model_router.py` | 351 |
| `test_raises_value_error_for_unknown_mode` | Function | `tests/primitives/llm/test_model_router.py` | 164 |
| `test_error_message_lists_available_modes` | Function | `tests/primitives/llm/test_model_router.py` | 173 |
| `test_calls_ollama_and_returns_response` | Function | `tests/primitives/llm/test_model_router.py` | 187 |
| `test_ollama_tier_without_model_raises` | Function | `tests/primitives/llm/test_model_router.py` | 210 |
| `test_calls_openrouter_with_pinned_model` | Function | `tests/primitives/llm/test_model_router.py` | 224 |
| `test_openrouter_without_model_uses_tracker` | Function | `tests/primitives/llm/test_model_router.py` | 247 |
| `test_auto_uses_tracker_to_pick_model` | Function | `tests/primitives/llm/test_model_router.py` | 280 |
| `test_falls_through_to_next_tier_on_failure` | Function | `tests/primitives/llm/test_model_router.py` | 313 |
| `test_raises_runtime_error_when_all_tiers_fail` | Function | `tests/primitives/llm/test_model_router.py` | 356 |
| `test_raises_runtime_error_when_no_tiers` | Function | `tests/primitives/llm/test_model_router.py` | 378 |
| `test_override_skips_to_specified_tier` | Function | `tests/primitives/llm/test_model_router.py` | 392 |
| `test_override_out_of_range_raises_value_error` | Function | `tests/primitives/llm/test_model_router.py` | 413 |
| `test_unknown_provider_raises_runtime_error` | Function | `tests/primitives/llm/test_model_router.py` | 427 |
| `test_calls_groq_with_pinned_model` | Function | `tests/primitives/llm/test_model_router.py` | 455 |
| `test_groq_defaults_to_first_free_model_when_no_model` | Function | `tests/primitives/llm/test_model_router.py` | 482 |
| `test_calls_together_with_pinned_model` | Function | `tests/primitives/llm/test_model_router.py` | 514 |
| `test_together_without_model_raises` | Function | `tests/primitives/llm/test_model_router.py` | 543 |
| `test_bare_model_id_gets_models_prefix` | Function | `tests/primitives/llm/test_model_router.py` | 589 |
| `test_model_with_prefix_is_not_double_prefixed` | Function | `tests/primitives/llm/test_model_router.py` | 614 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → _build_messages` | cross_community | 7 |
| `Main → Resolve_model_id` | cross_community | 7 |
| `Handle_model_command → Rank_models_for_task` | cross_community | 6 |
| `Handle_model_command → _classify_entry` | cross_community | 6 |
| `Get_ranked_openhands_free_models → Resolve_model_id` | cross_community | 6 |
| `Llm_hardware_profile → _run` | cross_community | 6 |
| `Llm_viable_ollama_models → _run` | cross_community | 6 |
| `Test_router_ollama_skip_small → _build_messages` | cross_community | 6 |
| `Test_router_ollama_allow_large → _build_messages` | cross_community | 6 |
| `Main → _build_kwargs` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 18 calls |
| Tests | 1 calls |
| Integration | 1 calls |
| Model_advisor | 1 calls |
| Cli | 1 calls |
| Control_plane | 1 calls |

## How to Explore

1. `gitnexus_context({name: "execute"})` — see callers and callees
2. `gitnexus_query({query: "llm"})` — find related execution flows
3. Read key files listed above for implementation details
