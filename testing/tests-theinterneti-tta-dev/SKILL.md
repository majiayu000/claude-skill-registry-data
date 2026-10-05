---
name: tests
description: "Tests area in TTA.dev (session and related). 224 symbols | 25 files | Cohesion: 77%"
---

# Tests

224 symbols | 25 files | Cohesion: 77%

## When to Use

- Working on `tests`-related functionality in TTA.dev
- Navigating `ttadev/integrations/auth/session.py`
- Understanding test coverage for this area

## Key Files

| File | Symbols |
|------|---------|
| `tests/test_model_registry.py` | _ctx, _registry, _entry, test_register_and_get, test_register_updates_existing (+42) |
| `tests/test_eval_harness.py` | _task, _llm_resp, _ctx, test_execute_calls_all_models_and_populates_results, test_failed_model_sets_error_field_not_raises (+29) |
| `tests/test_ollama_primitives.py` | _ctx, test_health_check_healthy, test_health_check_unhealthy, test_list_models, test_running_models (+19) |
| `tests/test_model_monitor.py` | _ctx, _monitor, test_record_success_tracks_stats, test_record_failure_tracks_stats, test_success_rate_computed (+17) |
| `tests/test_tool_calling.py` | _make_ctx, _make_request, _make_openai_mock_response, test_openai_provider_with_tools_populates_tool_calls, test_openai_provider_without_tools_has_none_tool_calls (+12) |
| `tests/test_model_benchmarks.py` | _ctx, _registry, _entry, test_min_humaneval_score_excludes_low_scoring_models, test_min_humaneval_score_excludes_models_with_no_data (+8) |
| `tests/test_auth_session.py` | test_verify_session_returns_payload_for_valid_token, test_verify_session_preserves_user_id, test_verify_session_preserves_scopes, test_verify_session_returns_none_for_expired_token, test_verify_session_returns_none_for_wrong_secret (+1) |
| `tests/unit/test_auth_session.py` | test_encode_decode_roundtrip, test_valid_token_returns_payload, test_wrong_secret_rejected, test_tampered_payload_rejected, test_expired_token_rejected (+1) |
| `tests/test_auth_api_key.py` | test_store_and_get_round_trip, test_revoke_sets_revoked_flag_to_true, test_store_overwrites_existing_record_with_same_key_id, test_scopes_are_stored_correctly, test_is_valid_returns_true_for_valid_key (+1) |
| `ttadev/integrations/auth/session.py` | _b64url_encode, _b64url_decode, _sign, create_session, verify_session |

## Entry Points

Start here when exploring this area:

- **`test_register_and_get`** (Function) — `tests/test_model_registry.py:59`
- **`test_register_updates_existing`** (Function) — `tests/test_model_registry.py:78`
- **`test_get_missing_returns_none`** (Function) — `tests/test_model_registry.py:95`
- **`test_register_without_entry_is_error`** (Function) — `tests/test_model_registry.py:105`
- **`test_list_all`** (Function) — `tests/test_model_registry.py:119`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `test_register_and_get` | Function | `tests/test_model_registry.py` | 59 |
| `test_register_updates_existing` | Function | `tests/test_model_registry.py` | 78 |
| `test_get_missing_returns_none` | Function | `tests/test_model_registry.py` | 95 |
| `test_register_without_entry_is_error` | Function | `tests/test_model_registry.py` | 105 |
| `test_list_all` | Function | `tests/test_model_registry.py` | 119 |
| `test_list_empty_on_fresh_no_prepopulate` | Function | `tests/test_model_registry.py` | 133 |
| `test_list_returns_registry_response` | Function | `tests/test_model_registry.py` | 141 |
| `test_list_filter_by_provider` | Function | `tests/test_model_registry.py` | 152 |
| `test_list_filter_by_provider_no_match` | Function | `tests/test_model_registry.py` | 172 |
| `test_list_filter_by_cost_tier` | Function | `tests/test_model_registry.py` | 185 |
| `test_list_filter_by_cost_tier_low` | Function | `tests/test_model_registry.py` | 200 |
| `test_list_filter_by_capability_tool_calling` | Function | `tests/test_model_registry.py` | 218 |
| `test_list_filter_by_capability_vision` | Function | `tests/test_model_registry.py` | 243 |
| `test_list_combined_capability_filters` | Function | `tests/test_model_registry.py` | 267 |
| `test_select_prefers_local` | Function | `tests/test_model_registry.py` | 312 |
| `test_select_prefers_local_false_uses_cost_ordering` | Function | `tests/test_model_registry.py` | 348 |
| `test_select_max_cost_tier_filters` | Function | `tests/test_model_registry.py` | 383 |
| `test_select_max_cost_tier_medium_includes_lower_tiers` | Function | `tests/test_model_registry.py` | 414 |
| `test_select_require_tool_calling` | Function | `tests/test_model_registry.py` | 441 |
| `test_select_fallback_when_empty` | Function | `tests/test_model_registry.py` | 474 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 57 calls |
| Llm | 23 calls |
| Observability | 2 calls |
| Scripts | 1 calls |

## How to Explore

1. `gitnexus_context({name: "test_register_and_get"})` — see callers and callees
2. `gitnexus_query({query: "tests"})` — find related execution flows
3. Read key files listed above for implementation details
