---
name: codex-exec-subagent
description: Launch focused Codex subagents via `codex exec` (single, resumed, or batched), capture outputs to files, and aggregate results as if using The Agent subagents.
---

# Codex Exec Subagent

## Overview
Use this skill when you want to delegate focused tasks to one or more separate Codex instances using `codex exec`, then merge their outputs in a parent run.

This is the Codex equivalent of spawning "The Agent" subagents:
- each subagent is an isolated `codex exec` process
- each subagent has a strict prompt contract
- each subagent writes artifacts the parent can review

## When to Use
- "Spawn a subagent for this repo task."
- "Run two parallel Codex workers and summarize."
- "Use Codex exec like The Agent subagents."
- "Delegate investigation/edit/review to separate Codex instances."

## Verified Commands (Research)
Read `references/codex-exec-reference.md` for verified option details from:
- `codex exec --help`
- `codex exec resume --help`
- `codex exec review --help`

## Prerequisites
- `codex` is installed and on `PATH`.
- Run from the target repo root, or set `SUBAGENT_CWD`.
- Keep sandbox at `workspace-write` by default.

## Workflow
1. Define subagent scope:
- one clear task per subagent
- explicit file boundaries
- explicit output format

2. Launch execution:
- single run: `bash scripts/run_subagent.sh <name> "<prompt>"`
- batch run: `bash scripts/run_subagent_batch.sh references/tasks.tsv`
- resume thread: `codex exec resume <session_id> "<prompt>"`
- review mode: `codex exec review --uncommitted "<prompt>"`

3. Capture and inspect artifacts:
- `.codex/subagents/<timestamp>_<name>.md`
- optional `.codex/subagents/<timestamp>_<name>.jsonl` when `SUBAGENT_JSON=1`

4. Parent synthesis:
- compare outputs across subagents
- resolve conflicts with repo evidence
- keep final decisions centralized in the parent run

## Safety Defaults
- Use `-s workspace-write` unless a stricter mode is required.
- Avoid `--dangerously-bypass-approvals-and-sandbox` unless externally sandboxed.
- Use `-C <DIR>` to pin working root.
- Use `--skip-git-repo-check` only when intentionally running outside a repo.

## Command Patterns

Single delegated run:
```bash
bash scripts/run_subagent.sh resolver_audit "Inspect resolver fallback behavior and return findings."
```

Single delegated run with JSON event capture:
```bash
SUBAGENT_JSON=1 bash scripts/run_subagent.sh resolver_audit "Inspect resolver fallback behavior and return findings."
```

Batch delegated runs (serial default):
```bash
bash scripts/run_subagent_batch.sh references/tasks.tsv
```

Batch delegated runs (parallel):
```bash
SUBAGENT_BATCH_MODE=parallel bash scripts/run_subagent_batch.sh references/tasks.tsv
```

Resume most recent subagent thread:
```bash
codex exec resume --last "Continue and finalize with tests."
```

Run review mode:
```bash
codex exec review --uncommitted "Focus on regressions and missing tests."
```

## Batch File Format
`references/tasks.tsv` format:
```tsv
# name<TAB>prompt<TAB>cwd(optional)
resolver_audit	Inspect resolver fallback behavior and return findings.	.
cli_contract	Audit CLI compatibility wrappers and propose minimal fixes.	.
```

## Subagent Prompt Template
Use this to keep outputs consistent:

```text
You are a focused subagent.
Task: <one clear task>
Constraints:
- Scope only: <files/modules>
- Follow AGENTS.md and local conventions.
- Do not refactor unrelated code.
- If blocked, state exactly what is missing.
Output format:
1) Findings
2) Proposed changes
3) Risks/tests
```

## Script Inputs
- `SUBAGENT_CWD`: working directory for child run (default current directory)
- `SUBAGENT_ROOT`: artifact directory (default `.codex/subagents`)
- `SUBAGENT_SANDBOX`: `read-only|workspace-write|danger-full-access` (default `workspace-write`)
- `SUBAGENT_MODEL`: optional model override
- `SUBAGENT_PROFILE`: optional profile override
- `SUBAGENT_JSON=1`: emit `--json` and store JSONL events
- `SUBAGENT_BATCH_MODE=parallel`: run TSV entries concurrently
- `SUBAGENT_UNSAFE=1`: add dangerous bypass flag (avoid unless externally sandboxed)
