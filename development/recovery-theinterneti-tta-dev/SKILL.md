---
name: recovery
description: "Recovery subsystem in TTA.dev: execute and related code. 32 symbols | 4 files | Cohesion: 75%"
---

# Recovery

32 symbols | 4 files | Cohesion: 75%

## When to Use

- Working on `recovery`-related functionality in TTA.dev
- Modifying `execute`
- Navigating `ttadev/primitives/recovery/circuit_breaker_primitive.py`, `ttadev/primitives/recovery/fallback.py`

## Key Files

| File | Symbols |
|------|---------|
| `tests/primitives/recovery/test_retry_primitive.py` | _make_primitive, test_succeeds_on_first_attempt, test_passes_context_to_wrapped_primitive, test_raises_after_max_retries_exceeded, test_zero_retries_fails_immediately (+9) |
| `tests/primitives/recovery/test_fallback_primitive.py` | _make_ctx, _ok, _fail, test_primary_succeeds_returns_primary_result_with_tracer, test_fallback_invoked_when_primary_fails_with_tracer (+8) |
| `ttadev/primitives/recovery/circuit_breaker_primitive.py` | classify_error, should_retry, calculate_delay, wrapper |
| `ttadev/primitives/recovery/fallback.py` | execute |

## Entry Points

Start here when exploring this area:

- **`execute`** (Function) — `ttadev/primitives/recovery/fallback.py:64`
- **`test_primary_succeeds_returns_primary_result_with_tracer`** (Function) — `tests/primitives/recovery/test_fallback_primitive.py:67`
- **`test_fallback_invoked_when_primary_fails_with_tracer`** (Function) — `tests/primitives/recovery/test_fallback_primitive.py:79`
- **`test_raises_primary_error_when_both_fail_with_tracer`** (Function) — `tests/primitives/recovery/test_fallback_primitive.py:91`
- **`test_fallback_not_called_when_primary_succeeds_with_tracer`** (Function) — `tests/primitives/recovery/test_fallback_primitive.py:102`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `execute` | Function | `ttadev/primitives/recovery/fallback.py` | 64 |
| `test_primary_succeeds_returns_primary_result_with_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 67 |
| `test_fallback_invoked_when_primary_fails_with_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 79 |
| `test_raises_primary_error_when_both_fail_with_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 91 |
| `test_fallback_not_called_when_primary_succeeds_with_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 102 |
| `test_primary_succeeds_returns_primary_result_without_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 125 |
| `test_fallback_invoked_when_primary_fails_without_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 138 |
| `test_raises_primary_error_when_both_fail_without_tracer` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 151 |
| `test_checkpoints_recorded_on_primary_success` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 170 |
| `test_checkpoints_recorded_on_fallback_path` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 186 |
| `test_checkpoints_recorded_on_both_fail` | Function | `tests/primitives/recovery/test_fallback_primitive.py` | 201 |
| `test_succeeds_on_first_attempt` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 105 |
| `test_passes_context_to_wrapped_primitive` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 147 |
| `test_raises_after_max_retries_exceeded` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 190 |
| `test_zero_retries_fails_immediately` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 223 |
| `test_sleep_called_between_retries` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 258 |
| `test_defensive_runtime_error_when_last_error_is_none` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 332 |
| `test_succeeds_on_nth_attempt` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 125 |
| `test_passes_input_data_unchanged` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 167 |
| `test_respects_max_retries_count` | Function | `tests/primitives/recovery/test_retry_primitive.py` | 203 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Wrapper → Classify_error` | intra_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 18 calls |

## How to Explore

1. `gitnexus_context({name: "execute"})` — see callers and callees
2. `gitnexus_query({query: "recovery"})` — find related execution flows
3. Read key files listed above for implementation details
