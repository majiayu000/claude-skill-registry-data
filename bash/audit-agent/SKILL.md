---
name: audit-agent
description: "Audits AI-agent runs and session snapshots for token usage, cache traffic, cost, duration, turns, tool calls, failures, retries, subagent attribution, duplicated reads, and artifact yield. Use when reporting or comparing a Codex CLI rollout, GitHub Copilot CLI, Gemini CLI, OpenCode, Claude Code, a runner export, or transcript logs. Do NOT use to monitor live CI, prove a check can fail, or sandbox a CLI."
compatibility: "Requires filesystem access. Bundled auditors require Python 3.9+; shell examples use POSIX sh. Manual fallbacks are provided."
metadata:
  author: Serghei Iakovlev
  version: "2.2"
  category: analysis
---

# Audit an Agent Run

Reconstruct measurements from persisted records, not from the run's own summary. A native counter is evidence only after its scope, update semantics, and run boundary are known.

## Evidence contract

- Keep the audit read-only. Never modify, vacuum, delete, migrate, or import into the runner's session store.
- Treat transcripts and tool inputs as sensitive. Emit structural counts and identifiers by default; sanitize exports before they leave the machine.
- Classify the result as `exact`, `estimate`, or `snapshot`. `Exact` requires a closed boundary and a successful second-path reconciliation. A live or resumable session is a `snapshot` through an explicit cutoff.
- Preserve vendor categories. Report input, cache read, cache write, output, reasoning, and recorded cost separately; combine counters only when the schema proves they do not overlap.
- Distinguish user turns, assistant messages, model steps, and tool calls. Never label one of them simply `turns`.

Script paths are relative to this skill directory, not the project working directory. If a command cannot resolve `scripts/`, prefix it with the skill directory reported by the platform.

## Route by evidence source

Identify the runner and installed version before reading records, then load only the matching adapter:

- OpenCode with `opencode db`: read [references/opencode.md](references/opencode.md). This is the preferred and tested route.
- Codex CLI local rollout JSONL or a saved `codex exec --json` stream: read [references/codex.md](references/codex.md).
- GitHub Copilot CLI: read [references/copilot-cli.md](references/copilot-cli.md).
- Claude Code JSONL: read [references/claude-code.md](references/claude-code.md).
- Gemini CLI JSONL: read [references/gemini.md](references/gemini.md).
- Another runner, an export with unknown schema, or raw logs: read [references/generic-logs.md](references/generic-logs.md).
- Comparisons, duplicated reads, retries, or artifact yield: also read [references/analysis.md](references/analysis.md).

Do not load every adapter. Their schemas are mutually exclusive, and carrying one vendor's reduction into another vendor's records is the primary failure this skill prevents.

## Workflow

### 1. Pin the run boundary

Record the root run or session id, project or working directory, runner version, model/provider, agent configuration, start, end or cutoff, and terminal state (`completed`, `aborted`, or `snapshot`). Verify a discovered id against at least the directory and time window; nearest timestamp alone is not identity.

For a comparison, pin the task input and starting repository state before measuring either run. If they differ, report two case studies rather than a performance comparison.

### 2. Inventory the whole run

Enumerate the root and every descendant session before arithmetic. Rebuild parent-child links from explicit ids where available. Missing child evidence means attribution is incomplete, not that the child did not run. Deduplicate by the storage system's documented primary key or by `(source, id)` when scope is unknown.

### 3. Derive each metric from its update semantics

For every counter, determine whether each record is a delta, a cumulative snapshot, a repeated message total, or a session total. Sum deltas, take the terminal cumulative value, and count repeated totals once per proven key. There is no cross-vendor default reduction.

Use the runner's recorded cost when present. If cost must be derived from pricing, fetch current provider rates, name the model and rate date, and label the result `derived`.

Call `time_updated - time_created` a session span, not active runtime. Report active model or tool duration only when explicit start/end records support it.

### 4. Reconcile through a second path

Compare session totals with the sum of terminal step records, a native stats command, or another independently stored summary. State both values and the difference. A mismatch, missing descendants, unknown counter role, or absent terminal evidence downgrades the affected figure to `estimate`.

For every reported zero, run the extractor against a known positive record or fixture first. Without that control, say `no hits observed`, not `none occurred`.

### 5. Report without overclaiming

Use this order and omit sections the request does not need:

1. **Status:** `exact`, `estimate`, or `snapshot`, with cutoff and one-sentence reason.
2. **Scope:** root id, descendants included, runner/version, project, model/configuration, source queried.
3. **Usage:** separate token categories and recorded or derived cost, total and per agent/session.
4. **Behavior:** user turns, model steps, tool calls and errors; clearly label heuristic retry or strategy-change counts.
5. **Cross-checks:** detail-versus-summary reconciliation and positive controls.
6. **Limitations:** missing records, ambiguous fields, concurrent writers, or non-comparable inputs.

Every headline number names its source and formula in the same section. Do not convert missing usage data from artifact bytes, transcript length, or context-window size.

## Completion gate

- [ ] Run identity, boundary, state, and cutoff are explicit.
- [ ] Root and descendant sessions are included exactly once.
- [ ] Counter roles and update semantics were verified on this runner version.
- [ ] Detail totals reconcile through a second path, or the figure is labeled `estimate`.
- [ ] Token categories remain separate unless non-overlap is proven.
- [ ] Turn and duration labels state exactly what was counted.
- [ ] Every reported zero passed a positive control.
- [ ] Comparison inputs and starting state match, or no comparative verdict is made.
- [ ] The report contains no prompt, tool payload, credential, or unnecessary transcript content.
