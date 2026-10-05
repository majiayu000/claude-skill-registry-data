---
name: cli
description: "Cli subsystem in TTA.dev: cmd_status and related code. 110 symbols | 27 files | Cohesion: 70%"
---

# Cli

110 symbols | 27 files | Cohesion: 70%

## When to Use

- Working on `cli`-related functionality in TTA.dev
- Modifying `cmd_status`
- Navigating `ttadev/cli/run.py`, `ttadev/cli/models.py`

## Key Files

| File | Symbols |
|------|---------|
| `tests/cli/test_status.py` | _args, _make_validation_result, _make_ok_result, test_exit_code_zero_when_providers_healthy, test_output_contains_checkmark_for_healthy_provider (+14) |
| `tests/cli/test_setup.py` | _make_args, test_exit_0_when_at_least_one_connected, test_exit_1_when_none_connected, test_json_output_parses, test_json_output_no_key_values (+8) |
| `ttadev/cli/run.py` | execute, _path, get, set, run_cache (+5) |
| `ttadev/cli/models.py` | handle_model_command, _cmd_suggest_qwen, _cmd_ollama, _cmd_ollama_recommend, _cmd_info (+5) |
| `ttadev/cli/control.py` | _step_duration, _handle_task_create, _handle_task_list, _handle_task_show, _handle_task_claim (+4) |
| `ttadev/cli/setup.py` | _get_key, cmd_validate_keys, validate_provider, _read_env, _write_env (+4) |
| `ttadev/cli/benchmark.py` | _validate_response, _benchmark_model, run_benchmark, cmd_benchmark, _run (+2) |
| `ttadev/cli/status.py` | _provider_slug, _check_port, cmd_status, _count_control_plane |
| `ttadev/cli/hw_detect.py` | detect_gpu_vram_gb, detect_system_ram_gb, recommend_ollama_model, hardware_summary |
| `tests/unit/test_hw_detect.py` | _with_gpu, _no_gpu, test_recommended_model_matches_standalone_recommend |

## Entry Points

Start here when exploring this area:

- **`cmd_status`** (Function) — `ttadev/cli/status.py:122`
- **`test_exit_code_zero_when_providers_healthy`** (Function) — `tests/cli/test_status.py:200`
- **`test_output_contains_checkmark_for_healthy_provider`** (Function) — `tests/cli/test_status.py:216`
- **`test_output_shows_latency_for_healthy_providers`** (Function) — `tests/cli/test_status.py:240`
- **`test_exit_code_one_when_all_missing`** (Function) — `tests/cli/test_status.py:266`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `cmd_status` | Function | `ttadev/cli/status.py` | 122 |
| `test_exit_code_zero_when_providers_healthy` | Function | `tests/cli/test_status.py` | 200 |
| `test_output_contains_checkmark_for_healthy_provider` | Function | `tests/cli/test_status.py` | 216 |
| `test_output_shows_latency_for_healthy_providers` | Function | `tests/cli/test_status.py` | 240 |
| `test_exit_code_one_when_all_missing` | Function | `tests/cli/test_status.py` | 266 |
| `test_output_shows_missing_key_message` | Function | `tests/cli/test_status.py` | 282 |
| `test_json_output_is_valid_json` | Function | `tests/cli/test_status.py` | 304 |
| `test_json_output_has_required_keys` | Function | `tests/cli/test_status.py` | 324 |
| `test_json_output_contains_no_key_values` | Function | `tests/cli/test_status.py` | 342 |
| `test_json_healthy_true_when_provider_connected` | Function | `tests/cli/test_status.py` | 361 |
| `test_json_healthy_false_when_all_fail` | Function | `tests/cli/test_status.py` | 378 |
| `test_dashboard_running_shown_in_output` | Function | `tests/cli/test_status.py` | 399 |
| `test_mcp_running_shown_in_output` | Function | `tests/cli/test_status.py` | 417 |
| `test_json_services_reflect_port_state` | Function | `tests/cli/test_status.py` | 434 |
| `test_control_plane_counts_in_human_output` | Function | `tests/cli/test_status.py` | 455 |
| `test_control_plane_counts_in_json_output` | Function | `tests/cli/test_status.py` | 471 |
| `cmd_validate_keys` | Function | `ttadev/cli/setup.py` | 314 |
| `test_exit_0_when_at_least_one_connected` | Function | `tests/cli/test_setup.py` | 281 |
| `test_exit_1_when_none_connected` | Function | `tests/cli/test_setup.py` | 296 |
| `test_json_output_parses` | Function | `tests/cli/test_setup.py` | 309 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Handle_model_command → Rank_models_for_task` | cross_community | 6 |
| `Handle_model_command → _classify_entry` | cross_community | 6 |
| `Handle_model_command → Estimate_finetune_cost` | cross_community | 5 |
| `Handle_model_command → Estimate_quality_improvement` | cross_community | 5 |
| `Handle_model_command → Calculate_roi_breakeven` | cross_community | 5 |
| `Main → _path` | cross_community | 4 |
| `Handle_model_command → _build_rationale` | intra_community | 4 |
| `Main → Register_agent_subcommands` | cross_community | 3 |
| `Main → Register_agents_subcommands` | cross_community | 3 |
| `Main → Register_workflow_subcommands` | cross_community | 3 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Unit | 36 calls |
| Control_plane | 4 calls |
| Observability | 3 calls |
| Model_advisor | 2 calls |
| Agents | 1 calls |

## How to Explore

1. `gitnexus_context({name: "cmd_status"})` — see callers and callees
2. `gitnexus_query({query: "cli"})` — find related execution flows
3. Read key files listed above for implementation details
