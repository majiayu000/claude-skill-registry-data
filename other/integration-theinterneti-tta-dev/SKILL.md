---
name: integration
description: "Integration area in TTA.dev (universal_llm_primitive and related). 65 symbols | 10 files | Cohesion: 77%"
---

# Integration

65 symbols | 10 files | Cohesion: 77%

## When to Use

- Working on `integration`-related functionality in TTA.dev
- Navigating `ttadev/primitives/llm/universal_llm_primitive.py`, `ttadev/primitives/core/base.py`
- Understanding test coverage for this area

## Key Files

| File | Symbols |
|------|---------|
| `tests/integration/test_provider_apis.py` | _ctx, _timed_execute, _log, test_groq_llama_8b, test_groq_llama_70b (+11) |
| `tests/integration/test_universal_llm_integration.py` | _ctx, test_openai_execute, test_groq_execute, test_together_execute, test_openrouter_execute (+9) |
| `tests/integration/test_circuit_breaker_llm.py` | _ctx, _make_circuit, _drive_to_open, test_circuit_stays_closed_on_success, test_circuit_opens_after_failure_threshold (+4) |
| `tests/integration/test_llm_providers.py` | _ctx, test_groq_llm_round_trip, test_anthropic_llm_round_trip, test_openai_llm_round_trip, test_ollama_llm_round_trip (+3) |
| `tests/integration/test_workflow_code_review.py` | execute, test_security_check, execute, test_complexity_analysis, test_context_metadata_in_review (+1) |
| `tests/integration/test_agent_identity_e2e.py` | _build_isolated_provider, test_lambda_primitive_span_carries_agent_id, test_span_processor_preserves_agent_id, test_session_manager_creates_session_with_agent_id |
| `tests/integration/test_l0_workflow_proof.py` | _call_tool, _pin_agent, test_happy_path_two_step_workflow, test_low_confidence_gate_requires_human_decision_to_quit |
| `ttadev/primitives/llm/universal_llm_primitive.py` | execute, stream |
| `tests/observability/test_span_pipeline.py` | test_lambda_returns_expected_result |
| `ttadev/primitives/core/base.py` | execute |

## Entry Points

Start here when exploring this area:

- **`test_groq_llama_8b`** (Function) — `tests/integration/test_provider_apis.py:110`
- **`test_groq_llama_70b`** (Function) — `tests/integration/test_provider_apis.py:140`
- **`test_groq_gemma2`** (Function) — `tests/integration/test_provider_apis.py:167`
- **`test_groq_mixtral`** (Function) — `tests/integration/test_provider_apis.py:194`
- **`test_groq_rotation`** (Function) — `tests/integration/test_provider_apis.py:221`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `test_groq_llama_8b` | Function | `tests/integration/test_provider_apis.py` | 110 |
| `test_groq_llama_70b` | Function | `tests/integration/test_provider_apis.py` | 140 |
| `test_groq_gemma2` | Function | `tests/integration/test_provider_apis.py` | 167 |
| `test_groq_mixtral` | Function | `tests/integration/test_provider_apis.py` | 194 |
| `test_groq_rotation` | Function | `tests/integration/test_provider_apis.py` | 221 |
| `test_gemini_auto_prefix` | Function | `tests/integration/test_provider_apis.py` | 380 |
| `test_openrouter_free_model` | Function | `tests/integration/test_provider_apis.py` | 432 |
| `test_openrouter_gemma_free` | Function | `tests/integration/test_provider_apis.py` | 459 |
| `test_together_llama` | Function | `tests/integration/test_provider_apis.py` | 491 |
| `test_anthropic_haiku` | Function | `tests/integration/test_provider_apis.py` | 523 |
| `test_openai_gpt4o_mini` | Function | `tests/integration/test_provider_apis.py` | 558 |
| `test_router_groq_cascade` | Function | `tests/integration/test_provider_apis.py` | 591 |
| `test_router_gemini_tier` | Function | `tests/integration/test_provider_apis.py` | 651 |
| `test_groq_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 52 |
| `test_anthropic_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 81 |
| `test_openai_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 112 |
| `test_ollama_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 143 |
| `test_gemini_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 197 |
| `test_openrouter_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 231 |
| `test_together_llm_round_trip` | Function | `tests/integration/test_llm_providers.py` | 265 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 11 calls |
| Observability | 4 calls |
| Llm | 4 calls |
| Control_plane | 1 calls |

## How to Explore

1. `gitnexus_context({name: "test_groq_llama_8b"})` — see callers and callees
2. `gitnexus_query({query: "integration"})` — find related execution flows
3. Read key files listed above for implementation details
