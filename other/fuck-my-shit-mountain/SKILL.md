---
name: fuck-my-shit-mountain
description: Use for codebase audits, repository health reviews, or scoped PR reviews. Produces evidence-based findings, risk and coverage assessments, and actionable reports.
---

# Fuck My Shit Mountain — Skill Definition

## Purpose

Guide AI to perform an evidence-based, professional code audit of a software project. Despite the irreverent name, the output must be冷静 (calm), professional, actionable, and free of emotional language.

## Setup and workflow

Infer audit scope from the request and repository context. Use the conversation language and stdout unless the user requests a different format or file. A general audit request defaults to broad repository coverage; a named concern or changed-file request narrows scope. Ask only when a missing decision materially changes the work. For incremental reviews, identify the base revision or changed-file scope.

1. Map relevant entry points, boundaries, tests, configuration, and release surfaces. Use `scripts/project_inventory.py` when available; prioritize risks and state coverage limits.
2. Load only relevant mode prompts and rubrics. Read `references/report-format.md` when preparing a report; use tooling guidance when it can improve evidence. Examples are calibration only.
3. Inspect relevant first-party code and tests. Tie findings to concrete evidence and realistic impact; distinguish confirmed from suspected issues, and include practical fixes and regression checks.
4. Produce the requested report format. Save report files or audit metadata only when requested. Run `scripts/report_lint.py` when available; apply equivalent checks to stdout reports.
5. An audit does not authorize application-code, test, configuration, or dependency changes. Implement remediation only when requested.

Cover relevant first-party source, tests, scripts, CI/configuration, migrations, manifests, and behavior documentation. Exclude dependencies, generated artifacts, binaries, and caches by default unless the selected concern needs them. Record inspected areas, exclusions, commands, and access limits; mark inapplicable dimensions Not assessed. Never imply complete coverage where inspection was partial.

Each finding needs severity, confidence/status, file and behavior evidence, a realistic failure scenario, the smallest practical fix, a regression-test suggestion, and estimated effort. Do not fabricate findings, exaggerate severity, or recommend rewrites without evidence. Protect secrets: identify location and type without reproducing values; recommend rotation when exposure is plausible.

## Mode vs Dimension Model

- **Selectable modes** are user-facing audit entry points. Each mode maps to one prompt file in `prompts/`.
- **Full dimensions** are the sections covered by `full` mode. Full mode covers all selectable focused dimensions and marks project-inapplicable dimensions as Not assessed.
- Focused modes may affect multiple score dimensions. For example, `configuration` can affect Security, Stability, and Release.
- If a dimension is only conditionally relevant, such as `frontend-state`, `accessibility`, or `ai-safety`, inspect for applicability first and mark it Not assessed with evidence when the project lacks that surface.

## Resource Loading

- Load only the prompt files for the selected modes.
- Load `references/report-format.md` before producing any report. Focused prompt files intentionally omit repeated setup and template rules.
- Load `references/tooling.md` when scanner, linter, typechecker, dependency, frontend, or AI/LLM tooling could improve evidence. Tools are optional; use configured local commands first and continue when tools are unavailable.
- Load examples from `examples/` only for calibration when the user asks for examples or the report shape is unclear. Do not copy their findings into a real audit.
- Do not load large generated or vendored files into context unless the selected mode specifically requires them.

## Audit Boundary

By default, this skill audits and reports. It may create requested report files, but it must not change application source code, tests, configuration, or dependencies unless the user explicitly asks for remediation implementation.

## Coverage Strategy

Cover relevant first-party source, tests, scripts, CI/configuration, migrations, manifests, and behavior documentation. Exclude dependencies, generated artifacts, binaries, and caches by default unless the selected concern needs them. Record inspected areas, exclusions, commands, and access limits; mark inapplicable dimensions Not assessed. Never imply complete coverage where inspection was partial.



## Sensitive Information Handling

If the audit discovers secrets, tokens, private keys, `.env` values, credentials, database dumps, or similarly sensitive material:

- Do not print the full secret in the report, terminal output, commit message, or conversation.
- Identify the path, variable/key name, secret type, and risk. Redact values as `<redacted>` or show at most a minimal prefix/suffix when necessary for disambiguation.
- Recommend rotation when exposure is plausible.
- Treat sensitive files as evidence of risk without copying their contents into the generated report.

## Modes

| Mode | Prompt | Focus |
|------|--------|-------|
| `full` | `prompts/full-audit.md` | All dimensions + principles |
| `incremental` | `prompts/incremental-audit.md` | Diff-based audit of changed files since git reference |
| `architecture` | `prompts/architecture-audit.md` | Module boundaries, dependency direction, state ownership |
| `security` | `prompts/security-audit.md` | Security risks |
| `stability` | `prompts/stability-audit.md` | Reliability & errors |
| `performance` | `prompts/performance-audit.md` | Realistic bottlenecks |
| `testing` | `prompts/testing-audit.md` | Test quality & gaps |
| `maintainability` | `prompts/maintainability-audit.md` | Complexity, coupling, principles |
| `design` | `prompts/design-audit.md` | Engineering principles and design risk |
| `release` | `prompts/release-audit.md` | Release readiness |
| `documentation` | `prompts/documentation-audit.md` | Docs accuracy, setup, operator/developer guidance |
| `observability` | `prompts/observability-audit.md` | Logging, metrics, tracing, health checks, alerting |
| `configuration` | `prompts/configuration-audit.md` | Config validation, defaults, feature flags, env separation |
| `data-integrity` | `prompts/data-integrity-audit.md` | Transactions, idempotency, migrations, invariants |
| `privacy` | `prompts/privacy-audit.md` | PII, minimization, retention, deletion, data governance |
| `accessibility` | `prompts/accessibility-audit.md` | Keyboard, focus, semantics, responsive and UX states |
| `supply-chain` | `prompts/supply-chain-audit.md` | Provenance, reproducibility, CI integrity, signing |
| `cost` | `prompts/cost-audit.md` | Resource economics, budgets, external API and LLM costs |
| `ai-safety` | `prompts/ai-safety-audit.md` | Prompt injection, tool auth, RAG leakage, evals, cost abuse |
| `fallback` | `prompts/fallback-audit.md` | Silent fallback, catch, defensive guessing |
| `testing-authenticity` | `prompts/testing-authenticity-audit.md` | Real confidence vs green checkmarks |
| `type-safety` | `prompts/type-safety-audit.md` | Unsafe blocks, assertions, boundary types |
| `frontend-state` | `prompts/frontend-state-audit.md` | Component size, state, effects, coupling |
| `backend-api` | `prompts/backend-api-audit.md` | API design, validation, data access patterns |
| `dependency-weight` | `prompts/dependency-weight-audit.md` | Overweight deps, build toolchain |
| `code-consistency` | `prompts/code-consistency-audit.md` | Naming, imports, patterns, style uniformity |
| `comment-coverage` | `prompts/comment-coverage-audit.md` | Doc quality, stale comments, missing docs |
| `concurrency` | `prompts/concurrency-audit.md` | Race conditions, deadlocks, atomicity, shared state, locking |

## Scoring

Full audits produce a **score dashboard** with 7 dimension scores (0.0–10.0) and an overall score. Focused audits score only the relevant dimensions and mark unrelated dimensions as not assessed when the template needs that context.

- **Higher = better.** 10 = clean / production-ready. 0 = shit mountain / unacceptable. Do not reverse this.
- Scores are **judgment-based**, not mechanical deductions. The AI evaluates evidence holistically per dimension.
- Each score must have a **one-sentence justification** referencing the strongest evidence and the coverage confidence when it limits the conclusion.
- A letter grade (S/A/B/C/D/F) provides an at-a-glance health indicator.
- Scores supplement detailed findings — they do not replace them.

## Rules

1. Tie each finding to concrete evidence and realistic impact; separate confirmed from suspected, state uncertainty, and avoid exaggeration or generic advice.
2. Prefer the smallest practical fix. Recommend rewrites only when evidence shows local fixes are insufficient.
3. Suggest a relevant regression check for findings that warrant one; do not require a test suggestion for every informational observation.
4. Use the report template appropriate to the requested output and scope. Do not copy audit findings into unrelated project formats.
5. Protect secrets using the redaction guidance above.
6. Do not modify audited code unless remediation is requested.

## Delivery check

Confirm the report's requested language and format, relevant evidence and coverage limits, and that claims and conclusions match the inspected material. Run the report linter when available.
