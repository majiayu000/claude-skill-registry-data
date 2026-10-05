---
name: scripts
description: "Scripts subsystem in TTA.dev: get_open_prs, calculate_pr_age, calculate_pr_staleness and related code. 187 symbols | 39 files | Cohesion: 91%"
---

# Scripts

187 symbols | 39 files | Cohesion: 91%

## When to Use

- Working on `scripts`-related functionality in TTA.dev
- Modifying `get_open_prs`, `calculate_pr_age`
- Navigating `scripts/pr_manager.py`, `scripts/issue_manager.py`

## Key Files

| File | Symbols |
|------|---------|
| `scripts/pr_manager.py` | get_open_prs, calculate_pr_age, calculate_pr_staleness, categorize_pr, prioritize_pr (+7) |
| `scripts/issue_manager.py` | get_issue, auto_label, assign_milestone, label_unlabeled, main (+7) |
| `scripts/git_manager.py` | run_git, get_status, get_branches, get_merged_branches, analyze_stashes (+6) |
| `scripts/lazy_dev.py` | create_branch, collaborate_on_pr, collaborate_on_issue, show_status, interactive_mode (+6) |
| `scripts/agent_oversight.py` | colored, get_pending_commits, show_status, review_commit, approve_commit (+4) |
| `scripts/agent-activity-tracker.py` | _should_track, _get_file_type, _start_session, _update_session, on_modified (+4) |
| `scripts/smoke_test_primitives.py` | _ctx, _check_ollama, test_router_groq, test_router_gemini, test_router_ollama_skip_small (+3) |
| `scripts/scan-codebase-todos.py` | by_category, by_file_type, scan, _scan_directory, _scan_file (+3) |
| `scripts/branch_manager.py` | analyse_branches, audit, delete_closed_pr_branches, delete_orphaned_branches, main (+3) |
| `scripts/validate-primitive-usage.py` | add_warning, visit_Call, visit_For, visit_AsyncFunctionDef, _is_asyncio_call (+2) |

## Entry Points

Start here when exploring this area:

- **`get_open_prs`** (Function) — `scripts/pr_manager.py:45`
- **`calculate_pr_age`** (Function) — `scripts/pr_manager.py:103`
- **`calculate_pr_staleness`** (Function) — `scripts/pr_manager.py:117`
- **`categorize_pr`** (Function) — `scripts/pr_manager.py:131`
- **`prioritize_pr`** (Function) — `scripts/pr_manager.py:184`

## Key Symbols

| Symbol | Type | File | Line |
|--------|------|------|------|
| `get_open_prs` | Function | `scripts/pr_manager.py` | 45 |
| `calculate_pr_age` | Function | `scripts/pr_manager.py` | 103 |
| `calculate_pr_staleness` | Function | `scripts/pr_manager.py` | 117 |
| `categorize_pr` | Function | `scripts/pr_manager.py` | 131 |
| `prioritize_pr` | Function | `scripts/pr_manager.py` | 184 |
| `get_recommendations` | Function | `scripts/pr_manager.py` | 252 |
| `display_dashboard` | Function | `scripts/pr_manager.py` | 316 |
| `analyze_prs` | Function | `scripts/pr_manager.py` | 381 |
| `triage_prs` | Function | `scripts/pr_manager.py` | 453 |
| `health_check` | Function | `scripts/pr_manager.py` | 497 |
| `recommend_actions` | Function | `scripts/pr_manager.py` | 564 |
| `main` | Function | `scripts/pr_manager.py` | 626 |
| `run_git` | Function | `scripts/git_manager.py` | 23 |
| `get_status` | Function | `scripts/git_manager.py` | 30 |
| `get_branches` | Function | `scripts/git_manager.py` | 66 |
| `get_merged_branches` | Function | `scripts/git_manager.py` | 75 |
| `analyze_stashes` | Function | `scripts/git_manager.py` | 86 |
| `clean_experimental_branches` | Function | `scripts/git_manager.py` | 113 |
| `sync_with_remote` | Function | `scripts/git_manager.py` | 136 |
| `display_status_dashboard` | Function | `scripts/git_manager.py` | 150 |

## Execution Flows

| Flow | Type | Steps |
|------|------|-------|
| `Main → _build_messages` | cross_community | 7 |
| `Test_router_ollama_skip_small → _build_messages` | cross_community | 6 |
| `Test_router_ollama_allow_large → _build_messages` | cross_community | 6 |
| `Main → _categorize_file` | intra_community | 5 |
| `Main → _run_gh` | cross_community | 5 |
| `Main → Validate_against_schema` | cross_community | 5 |
| `Main → _run_gh` | intra_community | 4 |
| `Main → _is_cooling` | cross_community | 4 |
| `Main → _mark_cooling` | cross_community | 4 |
| `Main → Get_integration` | cross_community | 4 |

## Connected Areas

| Area | Connections |
|------|-------------|
| Llm | 5 calls |
| Tests | 1 calls |

## How to Explore

1. `gitnexus_context({name: "get_open_prs"})` — see callers and callees
2. `gitnexus_query({query: "scripts"})` — find related execution flows
3. Read key files listed above for implementation details
