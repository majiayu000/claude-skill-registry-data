---
name: adaptive
description: "Adaptive subsystem in TTA.dev: get_fallback_stats and related code. 156 symbols | 11 files | Cohesion: 80%"
---

# Adaptive

156 symbols | 11 files | Cohesion: 80%

## When to Use

- Working on `adaptive`-related functionality in TTA.dev
- Modifying `get_fallback_stats`
- Navigating `ttadev/primitives/adaptive/retry.py`, `ttadev/primitives/adaptive/cache.py`

## Key Files

| File | Symbols |
|------|---------|
| `tests/primitives/adaptive/test_adaptive_retry.py` | _ctx, test_execute_retry_success_on_first_attempt, test_execute_retry_succeeds_after_failures, test_execute_retry_exhaustion_returns_failure_dict, test_execute_retry_no_sleep_after_last_attempt (+32) |
| `tests/primitives/adaptive/test_adaptive_cache.py` | _ctx, _make_cache, test_cache_default_strategy_params, test_cache_miss_calls_target_primitive, test_cache_hit_returns_cached_value_without_calling_target (+26) |
| `tests/primitives/adaptive/test_adaptive_fallback.py` | _ctx, _make_fallback, test_get_default_strategy_returns_baseline, test_primary_succeeds_returns_primary_result, test_primary_success_increments_primary_attempts (+21) |
| `tests/primitives/adaptive/test_adaptive_timeout.py` | _ctx, _make_timeout, test_execute_success_records_latency, test_execute_success_tracks_context_latency, test_execute_multiple_successes_accumulate (+18) |
| `ttadev/primitives/adaptive/retry.py` | _execute_retry_with_tracing, _consider_error_specific_strategy, _context_extractor, _consider_reducing_retries, to_dict (+7) |
| `ttadev/primitives/adaptive/cache.py` | _get_default_strategy, _consider_new_strategy, get_cache_stats, evict_expired, _execute_with_strategy (+2) |
| `tests/unit/test_primitives_adaptive.py` | test_consider_error_specific_strategy_for_timeout_error, test_context_extractor_embeds_environment_and_priority, test_consider_reducing_retries_creates_strategy, test_max_strategies_limit_prevents_new_creation, test_from_dict_round_trip_preserves_values (+1) |
| `ttadev/primitives/adaptive/base.py` | record_usage, _execute_impl, _select_strategy, _execute_with_strategy, _get_default_strategy (+1) |
| `ttadev/primitives/adaptive/fallback.py` | _get_default_strategy, _consider_new_strategy, get_fallback_stats |
| `ttadev/primitives/adaptive/exceptions.py` | AdaptiveError, LearningError, StrategyValidationError |

## Entry Points

Start here when exploring this area:

- **`get_fallback_stats`** (Function) — `ttadev/primitives/adaptive/fallback.py:395`
- **`test_get_default_strategy_returns_baseline`** (Function) — `tests/primitives/adaptive/test_adaptive_fallback.py:135`
- **`test_primary_succeeds_returns_primary_result`** (Function) — `tests/primitives/adaptive/test_adaptive_fallback.py:167`
- **`test_primary_success_increments_primary_attempts`** (Function) — `tests/primitives/adaptive/test_adaptive_fallback.py:183`
- **`test_primary_fail_first_fallback_succeeds`** (Function) — `tests/primitives/adaptive/test_adaptive_fallback.py:202`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `AdaptiveError` | Class | `ttadev/primitives/adaptive/exceptions.py` | 35 |
| `LearningError` | Class | `ttadev/primitives/adaptive/exceptions.py` | 45 |
| `StrategyValidationError` | Class | `ttadev/primitives/adaptive/exceptions.py` | 61 |
| `get_fallback_stats` | Function | `ttadev/primitives/adaptive/fallback.py` | 395 |
| `test_get_default_strategy_returns_baseline` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 135 |
| `test_primary_succeeds_returns_primary_result` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 167 |
| `test_primary_success_increments_primary_attempts` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 183 |
| `test_primary_fail_first_fallback_succeeds` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 202 |
| `test_primary_fail_second_fallback_succeeds_when_first_fails` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 219 |
| `test_fallback_latency_recorded_on_success` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 236 |
| `test_all_fail_raises_last_exception` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 256 |
| `test_all_fail_primary_failure_counted` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 268 |
| `test_unknown_fallback_key_skipped_and_next_tried` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 290 |
| `test_unknown_fallback_key_all_unknown_raises` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 308 |
| `test_context_stats_initialized_on_first_access` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 328 |
| `test_context_stats_failure_tracked` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 346 |
| `test_get_fallback_stats_empty` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 380 |
| `test_get_fallback_stats_with_data` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 399 |
| `test_get_fallback_stats_best_order_by_success_rate` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 422 |
| `test_get_fallback_stats_strategies_included` | Function | `tests/primitives/adaptive/test_adaptive_fallback.py` | 440 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 9 calls |

## How to Explore

1. `gitnexus_context({name: "get_fallback_stats"})` — see callers and callees
2. `gitnexus_query({query: "adaptive"})` — find related execution flows
3. Read key files listed above for implementation details
