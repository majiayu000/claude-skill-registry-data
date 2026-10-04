---
name: code-model-benchmark-intel
description: Route code, model, dataset, experiment, and benchmark intelligence collection, crawling, normalization, and synthesis through public sources by default. Use when Codex needs a no-required-MCP/no-required-API-key closure for GitHub repository evidence, public code implementations, issues, PRs, releases, Hugging Face public models/datasets/Spaces/papers, model cards, eval results, benchmark leaderboards, public Kaggle/OpenML pages, LiveBench/SWE-bench/GAIA/LMArena-style benchmark data, or auditable JSONL/CSV/Markdown reports.
---

# Code Model Benchmark Intel

## Overview

Use this skill for source-grounded code, model, dataset, and benchmark evidence collection. The default closure uses public official APIs, public pages, local clones, Hub metadata, and benchmark repositories. MCP servers, private tokens, paid services, and login-gated sources are optional extensions, not required for the base workflow.

## Decision Tree

1. Identify the target:
   - GitHub repository, organization, code search, issue, PR, release, or workflow evidence;
   - Hugging Face model, dataset, Space, paper page, model card, README, or eval results;
   - benchmark leaderboard or model score across HF, Kaggle, OpenML, LiveBench, SWE-bench, GAIA, Arena/LMArena, or historical Papers with Code;
   - dataset search/download/profile;
   - model implementation comparison or paper-code linkage.
2. Run a route plan before installing crawlers or calling APIs:

```powershell
python skills\code-model-benchmark-intel\scripts\code_model_benchmark_intel.py plan `
  --target "Qwen code models SWE-bench leaderboard and GitHub implementations" `
  --needs code,models,benchmarks,leaderboards,report `
  --scale medium
```

3. Execute only the needed lane:
   - GitHub code/repo evidence: GitHub public REST, public GraphQL when available, or local clone first; GitHub MCP is optional.
   - Hugging Face Hub evidence: HF public API, Dataset Viewer, `hf` CLI, or `huggingface_hub` first; HF MCP is optional.
   - Benchmark scores: HF public leaderboard API, benchmark official repo/dataset, public Kaggle/OpenML pages/APIs, or benchmark-specific JSON.
   - Historical paper-code-benchmark linkage: Papers with Code archive or CodeSOTA-like third-party pages, clearly marked as archive/secondary.
4. Normalize before synthesis. Reports should cite normalized row IDs and source URLs, not loose browser state.

## Full Local Setup

For a complete no-secret local setup with Python dependencies:

```powershell
powershell -ExecutionPolicy Bypass -File skills\code-model-benchmark-intel\scripts\setup_code_model_benchmark_intel.ps1 -RunNetworkSmoke
```

For MCP registration shells:

```powershell
powershell -ExecutionPolicy Bypass -File skills\code-model-benchmark-intel\scripts\setup_code_model_benchmark_intel.ps1 -RegisterGitHubMcp -RegisterHuggingFaceMcp -RegisterKaggleMcp
```

This installs isolated global-skill runtimes when the skill is installed under `%USERPROFILE%\.codex\skills\code-model-benchmark-intel`. It registers official remote MCP entries without storing secrets or starting blocking OAuth flows. GitHub hosted MCP needs `GITHUB_PAT_TOKEN` visible to the Codex process; Hugging Face and Kaggle may require `codex mcp login <server>` or provider settings as separate user-approved steps. Read `references/full-setup.md` before configuring credentials.

For a visible assisted OAuth flow, use:

```powershell
powershell -ExecutionPolicy Bypass -File skills\code-model-benchmark-intel\scripts\assist_code_model_benchmark_auth.ps1 -Provider huggingface,kaggle
```

## Source Routing

Read `references/source-routing.md` before selecting a backend.

- Use GitHub public REST/GraphQL and local clones first for repositories, code search, issues, PRs, releases, commits, Actions, dependency/security signals, discussions, and repo trees. Use GitHub MCP only as an optional convenience route.
- Use Hugging Face public API, Dataset Viewer, `hf` CLI, and `huggingface_hub` first for models, datasets, Spaces, papers, model cards, dataset viewer rows, eval results, and benchmark datasets. Use HF MCP only as an optional convenience route.
- Use HF leaderboard API first for official benchmark datasets that expose `/api/datasets/{dataset_id}/leaderboard`.
- Use public Kaggle pages first. Use Kaggle official MCP or third-party `kaggle-mcp` only for explicitly approved authenticated/discussion/write-up workflows.
- Use OpenML API/Python for classic ML datasets, tasks, flows, runs, evaluations, and benchmark suites.
- Use benchmark-specific official repos/datasets for LiveBench, SWE-bench, GAIA, LiveCodeBench, BigCodeBench, and similar sources.
- Use Arena/LMArena snapshots or third-party APIs only as supplemental sources when no official public API exists.
- Treat Papers with Code as historical/archive unless a maintained replacement source is explicitly chosen.

## Common Commands

Classify a URL:

```powershell
python skills\code-model-benchmark-intel\scripts\code_model_benchmark_intel.py inspect-url `
  "https://huggingface.co/datasets/SWE-bench/SWE-bench_Verified"
```

Print the normalized artifact contract:

```powershell
python skills\code-model-benchmark-intel\scripts\code_model_benchmark_intel.py schema
```

Generate a run scaffold:

```powershell
python skills\code-model-benchmark-intel\scripts\code_model_benchmark_intel.py scaffold `
  --output-dir output\code_model_benchmark\swebench_qwen `
  --target "Qwen SWE-bench evidence" `
  --needs models,benchmarks,leaderboards,code,report
```

Normalize a raw JSON/JSONL capture:

```powershell
python skills\code-model-benchmark-intel\scripts\code_model_benchmark_intel.py normalize `
  --input output\code_model_benchmark\swebench_qwen\raw\hf_leaderboard.json `
  --source huggingface-leaderboard `
  --output-dir output\code_model_benchmark\swebench_qwen\normalized
```

## Output Contract

Use this directory shape for substantial runs:

- `raw/`: untouched API JSON, scraped HTML, cloned metadata, CSV exports, downloaded files, and logs.
- `normalized/repos.jsonl`: repository, code, issue, PR, release, workflow, and implementation rows.
- `normalized/models.jsonl`: model, dataset, Space, model-card, dataset-card, and Hub metadata rows.
- `normalized/benchmarks.jsonl`: benchmark, task, leaderboard, score, evaluation result, run, and metric rows.
- `normalized/artifacts.jsonl`: local files, downloaded datasets/PDFs/model cards, notebooks, logs, and screenshots.
- `sources.csv`: source review table with URL, source type, priority, and status.
- `manifest.json`: plan, commands, timestamps, limits, credentials policy, and blockers.
- `summary.md`: human-facing synthesis grounded in normalized row IDs.

Read `references/output-schema.md` before merging multiple sources.

## Guardrails

- Default work must remain useful without MCP, paid services, private tokens, or login-gated data.
- Prefer official public APIs, Hub metadata, and benchmark repos over search snippets and aggregator claims.
- Keep GitHub tokens, HF tokens, Kaggle tokens, API keys, cookies, proxy URLs, browser storage state, and `.env` files out of git and final answers.
- Do not download gated/private models, datasets, competition data, or benchmark assets unless the user has authorized access and the source terms allow it.
- Do not bypass paywalls, CAPTCHAs, login gates, rate limits, or license controls.
- Do not request or store GitHub/HF/Kaggle/OpenML credentials unless the selected lane actually needs them and the user explicitly approves.
- Mark source priority as `primary`, `secondary`, `archive`, or `fallback` for every normalized row.
- Preserve `source_url`, `source_id`, `fetched_at`, source-specific identifiers, and score provenance.
- For benchmark numbers, capture benchmark version, metric, split, date, verification status, source, and whether the value is self-reported.
- Run a small smoke capture before bulk crawl/download and record blocked or stale sources in `manifest.json`.

## Resources

- `scripts/code_model_benchmark_intel.py`: planner, URL inspector, scaffold generator, schema printer, and lightweight normalizer.
- `scripts/setup_code_model_benchmark_intel.ps1`: safe setup script for isolated HF/OpenML/Kaggle Python dependencies, official MCP registrations, and optional shallow benchmark repo clones.
- `scripts/assist_code_model_benchmark_auth.ps1`: visible assisted auth helper for HF/Kaggle Codex OAuth and GitHub PAT setup routing.
- `references/full-setup.md`: complete setup matrix, MCP boundaries, credentials policy, benchmark repos, and smoke tests.
- `references/benchmark-repos.md`: curated official benchmark repo/dataset list and clone policy.
- `references/source-routing.md`: detailed platform routing and tool notes.
- `references/output-schema.md`: normalized fields and merge policy.
