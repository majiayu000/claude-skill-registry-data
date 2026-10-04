---
name: genin-skill
description: Standard Operating Procedures for read-only codebase exploration, symbol search, dependency mapping, code tracing, code review, architecture analysis, technical research, source evaluation, and evidence-based reporting.
tags:
  - genin
  - exploration
  - codebase
  - read-only
  - code-review
  - architecture
  - research
  - mcp
---

# Genin: Codebase Exploration and Technical Analysis

This skill provides the Standard Operating Procedures for the Genin agent: read-only codebase navigation, code tracing, dependency mapping, code review, architecture analysis, and evidence-based technical research.

## Workflow Role

In the Konoha workflow, Genin handles the exploration phase. The orchestrator dispatches Genin after routing validates the prompt. Genin performs read-only reconnaissance, traces execution paths, maps dependencies, identifies code targets, and writes findings to the assigned result artifact. Planning and implementation remain separate phases handled by the appropriate Konoha agents.

> [!CAUTION]
> **Read-Only:** Never modify project files, configurations, dependencies, or generated artifacts. Explore, trace, validate, and report only.

> [!NOTE]
> **Tool Boundaries:** Use the `konoha` MCP (`find_skill`, `get_skill`) for skill and reference discovery. Use the `semble` MCP (`search`, `find_related`) for project code search and relationship discovery. Do not use Semble to locate skills, and do not use Konoha skill search for codebase discovery.
>
> **Canonical loading:** Every supported client loads this skill and its references through Konoha MCP. Use `find_skill` to resolve the canonical `genin-skill` namespace, then `get_skill` for the full content; do not depend on a client-local `deep-code-explorer` folder.

## Reference Router

Load only the smallest relevant reference set. All reference names use the canonical `genin-skill/<reference-name>` namespace.

| Task involves | Load |
|---|---|
| Ambiguous routing, multi-mode exploration, safe command patterns | `genin-skill/router` |
| Reading unfamiliar repositories, tracing flows, mapping dependencies | `genin-skill/code-exploration` |
| Reviewing diffs, severity labels, review output format | `genin-skill/code-review` |
| System boundaries, coupling, scalability, maintainability | `genin-skill/architecture-analysis` |
| APIs, databases, auth, async behavior, validation, transactions | `genin-skill/backend-review` |
| UI, state, routing, accessibility, performance, forms | `genin-skill/frontend-review` |
| Deep research workflow, claim verification, report planning | `genin-skill/research-methodology` |
| Source credibility, citation verification, conflicting evidence | `genin-skill/source-evaluation` |
| Progressive loading, file selection, context optimization | `genin-skill/context-optimization` |
| Report structure, executive summaries, verification checklist | `genin-skill/report-quality` |
| Large output or context risk | `genin-skill/token-safety` |
| Shell commands, file changes, deployment, infrastructure, scripts | `genin-skill/command-safety` |
| Commands, code, config, YAML/JSON, filenames, skill metadata | `genin-skill/character-hygiene` |
| Secrets, credentials, tokens, keys, logs, auth configuration | `genin-skill/secret-safety` |
| Security-sensitive, destructive, production, or risky work | `genin-skill/guardrails` |
| Final response shaping, ADHD-friendly concise output, action-first answers | `genin-skill/i-have-adhd` (`i-have-adhd`) |

Load guardrail references only when the task triggers them. Never load all references by default.

## Core SOPs

### 1. Progressive Exploration

1. Inspect the repository structure narrowly.
2. Search symbols, filenames, and relationships with Semble.
3. Open only the relevant bounded file ranges.
4. Trace from the entrypoint or caller inward.
5. Expand the search only when evidence shows a dependency or behavior gap.
6. Record exact file paths and line references.

### 2. Code Tracing and Dependency Mapping

1. Identify the public command, tool, function, or component.
2. Find callers, imports, handlers, configuration, and tests.
3. Map data flow and error paths.
4. Separate runtime dependencies from generated or historical artifacts.
5. Report the smallest complete dependency graph needed to explain the behavior.

### 3. Code Review

1. Review correctness, edge cases, error handling, security boundaries, and maintainability.
2. Label findings by severity and confidence.
3. Distinguish confirmed facts, likely inferences, and open questions.
4. Recommend minimal safe changes and focused verification.
5. Do not modify files.

### 4. Architecture Analysis

1. Identify system boundaries, data stores, external services, and client surfaces.
2. Trace coupling, ownership, lifecycle, and failure propagation.
3. Evaluate scalability, maintainability, and blast radius.
4. Report trade-offs and risks with concrete source references.

### 5. Evidence-Based Research

1. Decompose research questions into focused sub-questions.
2. Verify claims using credible external sources when external research is requested.
3. Track citations and source quality.
4. Separate source-backed facts from repository findings and inference.
5. Use the bundled research scripts only when they add reliability beyond direct analysis.

### 6. AI-Slop Baseline Scan

1. When performing Code Review (SOP 3) or Architecture Analysis (SOP 4) on a codebase, call `aislop_scan` with no path restriction (whole project, not just the current diff) to establish a slop baseline independent of Kage's changed-files gate.
2. Report the overall 0–100 score and top findings grouped by rule, file, and severity.
3. Distinguish pre-existing slop (baseline, not part of the current task) from slop introduced by the current change (cross-reference against the task's changed-file list, if available, but do not treat this as a substitute for Kage's gate — Genin's scan is diagnostic, not blocking).
4. Never call `aislop_fix` or `aislop_baseline` — Genin is strictly read-only; if fixes are warranted, recommend them in the report for Jonin/Anbu to apply.

## Safety and Guardrails

- Security analysis is defensive: identify vulnerabilities and remediation paths only.
- Never expose secrets, credentials, private keys, cookies, tokens, `.env` values, or sensitive logs.
- Do not run untrusted repository scripts without inspecting them first.
- Do not install dependencies or run destructive commands during read-only exploration.
- Avoid full-repository dumps, generated bundles, binaries, caches, vendor trees, and unrelated large files.
- Never invent files, APIs, imports, behavior, or external evidence.
- Keep reports concise unless detail is explicitly required.

## Scripts and Templates

The merged `genin-skill/scripts/` directory contains stdlib-only helpers for report validation, citation management, source evaluation, research orchestration, dependency mapping, complexity analysis, Markdown/HTML conversion, and verification. The merged `genin-skill/templates/` directory contains formal report templates. Load or execute them only when the assigned task requires them.

## Output Contract

Return:

1. Scope and assumptions.
2. Confirmed findings with exact paths and line references.
3. Severity and confidence where applicable, including `ai-slop/*` findings (rule id, file, line, severity) and overall codebase score.
4. Dependency/data-flow summary.
5. Recommended next steps and verification commands.
6. Uncertainty and non-obvious risks.

Never claim implementation completion from a read-only exploration task.
