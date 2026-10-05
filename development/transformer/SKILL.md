---
name: transformer
description: "Transformer subsystem in TTA.dev: walk, visit_Try, visit_If and related code. 37 symbols | 5 files | Cohesion: 91%"
---

# Transformer

37 symbols | 5 files | Cohesion: 91%

## When to Use

- Working on `transformer`-related functionality in TTA.dev
- Modifying `walk`, `visit_Try`
- Navigating `ttadev/primitives/analysis/transformer/orchestrator.py`, `ttadev/primitives/analysis/transformer/ast_detectors_advanced.py`

## Key Files

| File | Symbols |
|------|---------|
| `ttadev/primitives/analysis/transformer/orchestrator.py` | _apply_transform, _apply_transform_regex, _transform_timeout_ast, _transform_fallback_ast, _transform_parallel_ast (+14) |
| `ttadev/primitives/analysis/transformer/ast_detectors_advanced.py` | _check_sequential_chain, _extract_call_chain, walk, _extract_func_name, _check_function_for_delegation (+1) |
| `ttadev/primitives/analysis/transformer/ast_detectors.py` | visit_Try, _extract_return_func, _extract_func_name, _get_call_name, _check_function (+1) |
| `ttadev/primitives/analysis/transformer/ast_transformers_advanced.py` | visit_If, _extract_all_routes, _transform_function, _find_cache_pattern |
| `ttadev/primitives/analysis/transformer/ast_transformers.py` | visit_Try, _extract_return_func |

## Entry Points

Start here when exploring this area:

- **`walk`** (Function) — `ttadev/primitives/analysis/transformer/ast_detectors_advanced.py:310`
- **`visit_Try`** (Function) — `ttadev/primitives/analysis/transformer/ast_detectors.py:160`
- **`visit_If`** (Function) — `ttadev/primitives/analysis/transformer/ast_transformers_advanced.py:26`
- **`visit_Try`** (Function) — `ttadev/primitives/analysis/transformer/ast_transformers.py:260`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `walk` | Function | `ttadev/primitives/analysis/transformer/ast_detectors_advanced.py` | 310 |
| `visit_Try` | Function | `ttadev/primitives/analysis/transformer/ast_detectors.py` | 160 |
| `visit_If` | Function | `ttadev/primitives/analysis/transformer/ast_transformers_advanced.py` | 26 |
| `visit_Try` | Function | `ttadev/primitives/analysis/transformer/ast_transformers.py` | 260 |
| `_apply_transform` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 228 |
| `_apply_transform_regex` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 263 |
| `_transform_timeout_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 364 |
| `_transform_fallback_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 386 |
| `_transform_parallel_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 407 |
| `_transform_router_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 428 |
| `_transform_retry_regex` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 1057 |
| `_transform_timeout_regex` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 1101 |
| `_transform_fallback_regex` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 1128 |
| `_transform_parallel_regex` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 1168 |
| `_transform_router_regex` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 1196 |
| `_transform_retry_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 278 |
| `_transform_retry_ast_fallback` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 306 |
| `_transform_cache_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 500 |
| `_find_function_end` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 549 |
| `_transform_circuit_breaker_ast` | Function | `ttadev/primitives/analysis/transformer/orchestrator.py` | 689 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Visit_Try → _get_call_name` | intra_community | 4 |
| `Visit_If → _extract_route` | intra_community | 3 |

## How to Explore

1. `gitnexus_context({name: "walk"})` — see callers and callees
2. `gitnexus_query({query: "transformer"})` — find related execution flows
3. Read key files listed above for implementation details
