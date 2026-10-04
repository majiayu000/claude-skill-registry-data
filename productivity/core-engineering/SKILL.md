---
name: core-engineering
description: "General implementation only when no narrower task or ecosystem skill fits."
---

# Skill: core-engineering

## Purpose

Apply the default engineering workflow for production-grade implementation work.

## Core Rules

- Verify before acting.
- Prefer the smallest correct change.
- Preserve public contracts unless explicitly asked to change them.
- Match existing project style.
- Do not introduce unrelated refactors.
- Do not invent files, APIs, schemas, commands, or test results.
- Do not use placeholders as implementation.
- Do not leave dead code.
- Do not hide uncertainty.

## Workflow

### 1. Understand

Identify:

- requested behavior;
- expected output;
- constraints;
- ambiguous points;
- relevant domain boundaries.

If ambiguity blocks correctness, ask one precise question.

If ambiguity is manageable, proceed with an explicit assumption.

### 2. Inspect

Before writing code, inspect:

- relevant files;
- nearby related code;
- project config;
- tests;
- existing patterns;
- validation commands.

### 3. Plan

Create a concise plan:

- target files;
- intended changes;
- expected behavior;
- validation method;
- risks/assumptions.

For small tasks, one short paragraph is enough. The plan is a tool, not a paperwork shrine.

### 4. Implement

Implement in small focused slices.

Rules:

- one concern per change;
- explicit control flow;
- explicit error handling;
- no hidden global state;
- no unrelated formatting churn;
- no new dependencies unless justified.

### Tooling Defaults

Use the strongest relevant local tool when it is available:

- `rg` and `rg --files` before slower text or file search;
- `fd` for file discovery when it improves the search;
- `ast-grep` or `tree-sitter` for syntax-aware search and safe mechanical rewrites;
- `jq` or `yq` for structured JSON/YAML inspection and transformation;
- `just` when a `justfile` owns project commands;
- `delta` for local diff review when useful;
- `fzf` only for interactive narrowing, not as a required automation dependency.

If the preferred tool is unavailable, use the best fallback and name the gap
only when it materially affects confidence or reproducibility.

### Context Tooling Tiers

Use the same question-based routing as the steady global prompt, when the
current host exposes the relevant capability:

| Need | First route |
| --- | --- |
| Local edit or literal | `rg`, path filters, and targeted reads |
| Definitions and references | Serena's LSP-backed symbol navigation |
| Architecture and impact | Graphify, with fresh source verification |
| Documentation and ADRs | QMD over allowed roots; `wiki-query` for read-only wiki questions |
| External library documentation | Context7 for the installed library version |
| Dependency source | opensrc for the exact dependency revision |
| Worker handoff | `context-pack`; Repomix when an export is useful |

Do not run every search tool for each task. Keep path filters and bounded
excerpts. A package installation does not prove host availability. If a route
is unavailable, use targeted local evidence and report the material gap.
Repomix is an export, not a live code index.

### Project Context Bootstrap

Before broad reads or repeated cross-file exploration, do a cheap state check:

- Serena: `.serena/project.yml` plus any exposed Serena MCP/symbol tools;
- Graphify: `graphify-out/graph.json`;
- Repomix/context pack: existing requested pack path;
- output compressors: command availability and raw-output location.

Use the result as a decision gate:

- localized task -> use `rg`, symbol lookup, and targeted reads;
- existing Serena, Graphify, or QMD state -> compare its source revision and
  file hashes with the required scope, including uncommitted changes, before
  trusting it; an index older than an edit is stale evidence;
- missing state but architecture-heavy, symbol-heavy, dependency/call-graph, or
  repeated onboarding task -> initialize the narrowest useful project-local
  state when file mutation is allowed;
- read-only, security, validation-critical, or "do not modify files" task ->
  ask before creating `.serena/`, `graphify-out/`, context packs, hooks, or
  other repo-local artifacts.

Serena may be initialized with `serena project index .` when the CLI is
available and LSP-backed navigation will materially reduce file reads. Report
new `.serena/` files and never stage or commit them unless asked.

Graphify belongs to architecture/dependency/call-graph work. If no graph
exists, build a scoped graph only when it will reduce repeated reading; report
`graphify-out/` as generated state and verify important claims against source.

After edits, refresh the affected index scope and confirm one changed symbol
or document is found. If freshness cannot be established, read current source
and mark the index unverified. QMD roots must be an explicit allowlist; do not
add other repositories, personal notes, or home directories automatically.

Do not run persistent hook/config upgrades such as Graphify hooks or Git hooks
without an explicit user request.

### Output Compression Guardrail

Select one transformation: `jq` or deterministic filters for structured data,
RTK for supported noisy CLI output, Context Mode for large results with
selective retrieval, or Distill for semantic grouping. Do not chain multiple
summarizers by default. Distill is not sole evidence of a successful test.

Capture stdout/stderr and the original command's exit code before any filter
or summarizer. Store raw artifacts outside tracked files. Record command,
working directory, source revision, and raw artifact path separately from the
summary. A nonzero test exit remains FAIL even when a filter exits zero;
preserve scanner errors separately from findings and SKIP separately from PASS.
Before enabling an automatic wrapper, run an intentionally failing test and
verify its raw exit code and failure remain visible. Read raw evidence before
claiming validation or explaining ambiguous failures.

Context Mode hook enablement is a separate decision from using output
compression. `context-mode doctor` may diagnose missing hooks, but that result
does not authorize installing them.

Do not run `context-mode upgrade` for small, localized, read-only, security, or
validation-critical tasks. Propose it only when the work is multi-session,
repeated, or likely to produce large/noisy outputs where automatic capture will
materially reduce context loss.

Run `context-mode upgrade` only after explicit user authorization to modify
persistent Codex hooks/config. If the user asks to "reduce context/log noise
automatically", summarize that this requires persistent hook/config changes and
ask for confirmation before running it.

After enabling hooks, run `context-mode doctor` and report modified global files
such as `~/.codex/config.toml`, `~/.codex/hooks.json`, and any backups.

### 5. Validate

Run the best available targeted validation.

If validation fails, report the failure honestly and fix root causes when in scope.

If validation cannot be run, explain exactly why.

### 6. Report

Report:

- changed files;
- summary;
- validation command and result;
- assumptions;
- remaining risks.

## Assumptions Format

```markdown
Assumption: <clear assumption>
Reason: <why this assumption is reasonable>
Risk: <what breaks if it is wrong>
```

## Definition of Done

The task is done when:

- behavior is implemented;
- architecture is respected;
- tests/validation are handled;
- assumptions and risks are explicit;
- no fake placeholders remain;
- output is understandable to a senior engineer.
