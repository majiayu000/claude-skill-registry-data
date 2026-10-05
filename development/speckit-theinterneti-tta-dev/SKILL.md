---
name: speckit
description: "Speckit subsystem in TTA.dev: check_approval_status, approve, reject and related code. 26 symbols | 5 files | Cohesion: 82%"
---

# Speckit

26 symbols | 5 files | Cohesion: 82%

## When to Use

- Working on `speckit`-related functionality in TTA.dev
- Modifying `check_approval_status`, `approve`
- Navigating `ttadev/primitives/speckit/specify_primitive.py`, `ttadev/primitives/speckit/validation_gate_primitive.py`

## Key Files

| File | Symbols |
|------|---------|
| `ttadev/primitives/speckit/specify_primitive.py` | _execute_impl, _generate_feature_name, _analyze_coverage, _generate_spec, _render_spec_markdown (+2) |
| `ttadev/primitives/speckit/validation_gate_primitive.py` | _load_approval, check_approval_status, approve, _execute_impl, _save_approval (+1) |
| `ttadev/primitives/speckit/clarify_primitive.py` | _execute_impl, _generate_questions, _analyze_updated_spec, _update_specification, _format_questions (+1) |
| `ttadev/primitives/speckit/tasks_primitive.py` | _execute_impl, _parse_plan_file, _order_tasks, _identify_critical_path, _identify_parallel_streams |
| `tests/unit/test_primitives_speckit.py` | test_analyze_coverage_score_lower_with_more_clarify_markers, test_check_approval_status_returns_approved_after_approve |

## Entry Points

Start here when exploring this area:

- **`test_analyze_coverage_score_lower_with_more_clarify_markers`** (Function) — `tests/unit/test_primitives_speckit.py:415`
- **`test_check_approval_status_returns_approved_after_approve`** (Function) — `tests/unit/test_primitives_speckit.py:1604`
- **`check_approval_status`** (Function) — `ttadev/primitives/speckit/validation_gate_primitive.py:297`
- **`approve`** (Function) — `ttadev/primitives/speckit/validation_gate_primitive.py:327`
- **`reject`** (Function) — `ttadev/primitives/speckit/validation_gate_primitive.py:366`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `test_analyze_coverage_score_lower_with_more_clarify_markers` | Function | `tests/unit/test_primitives_speckit.py` | 415 |
| `test_check_approval_status_returns_approved_after_approve` | Function | `tests/unit/test_primitives_speckit.py` | 1604 |
| `check_approval_status` | Function | `ttadev/primitives/speckit/validation_gate_primitive.py` | 297 |
| `approve` | Function | `ttadev/primitives/speckit/validation_gate_primitive.py` | 327 |
| `reject` | Function | `ttadev/primitives/speckit/validation_gate_primitive.py` | 366 |
| `_execute_impl` | Function | `ttadev/primitives/speckit/tasks_primitive.py` | 157 |
| `_parse_plan_file` | Function | `ttadev/primitives/speckit/tasks_primitive.py` | 256 |
| `_order_tasks` | Function | `ttadev/primitives/speckit/tasks_primitive.py` | 553 |
| `_identify_critical_path` | Function | `ttadev/primitives/speckit/tasks_primitive.py` | 597 |
| `_identify_parallel_streams` | Function | `ttadev/primitives/speckit/tasks_primitive.py` | 657 |
| `_execute_impl` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 80 |
| `_generate_feature_name` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 122 |
| `_analyze_coverage` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 398 |
| `_load_approval` | Function | `ttadev/primitives/speckit/validation_gate_primitive.py` | 274 |
| `_generate_spec` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 137 |
| `_render_spec_markdown` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 256 |
| `_render_list` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 375 |
| `_get_timestamp` | Function | `ttadev/primitives/speckit/specify_primitive.py` | 388 |
| `_execute_impl` | Function | `ttadev/primitives/speckit/validation_gate_primitive.py` | 79 |
| `_save_approval` | Function | `ttadev/primitives/speckit/validation_gate_primitive.py` | 285 |

## How to Explore

1. `gitnexus_context({name: "test_analyze_coverage_score_lower_with_more_clarify_markers"})` — see callers and callees
2. `gitnexus_query({query: "speckit"})` — find related execution flows
3. Read key files listed above for implementation details
