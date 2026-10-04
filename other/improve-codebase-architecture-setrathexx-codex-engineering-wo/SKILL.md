---
name: improve-codebase-architecture
description: Produces a local-first architecture audit for codebases that feel hard to change, test, or navigate. Use when the user wants refactor opportunities, shallow module detection, interface simplification, dependency analysis, or a sequenced architecture improvement plan without immediate code edits.
---

# Improve Codebase Architecture

Find architectural friction and propose small, verifiable refactor opportunities.

This skill is analysis-first. Do not edit code, create reports, or start refactors until the user approves the report path and next action.

## Read First

Inspect repo context:

- `CONTEXT.md`
- `docs/agents/domain.md`
- `docs/adr/`
- `docs/agents/test-commands.md`
- relevant source files,
- relevant test files.

If setup docs are missing, infer from the repo and state what is unknown.

Use fast search when possible:

```powershell
rg --files
rg "<domain-term-or-module-name>"
```

Keep Windows paths with spaces quoted when showing commands or report paths.

## Output Location

Default local report directory:

```txt
docs/agents/architecture/
```

Suggested file:

```txt
docs/agents/architecture/YYYY-MM-DD-architecture-audit.md
```

Before writing a report:

- propose the target path,
- summarize what the report will contain,
- ask for approval.

## Scope

Use this skill for hard-to-change code, tangled module relationships, unclear ownership, shallow pass-through modules, broad interfaces, weak test surfaces, domain naming mismatch, and risky refactor sequencing.

Do not recommend a big rewrite. Prefer small changes that can be verified.

## Workflow

### 1. Define Audit Focus

Identify the area to inspect:

- folder,
- module group,
- feature path,
- bug-prone area,
- domain concept,
- PRD or issue scope.

If the focus is too broad, propose a narrower audit slice.

### 2. Map Current Structure

Read code and tests enough to understand:

- main modules,
- callers and callees,
- dependency direction,
- public interfaces,
- test entry points.

Use `zoom-out` first if the area is unfamiliar and the user only needs orientation.

### 3. Check Domain And Decisions

Compare code structure with:

- domain terms in `CONTEXT.md` or `docs/agents/domain.md`,
- ADR constraints,
- existing test command docs,
- related PRDs or issues.

Report mismatches:

- code uses different names than domain docs,
- module boundaries cut across domain concepts,
- ADR assumptions no longer match current implementation,
- tests verify internals instead of behavior.

### 4. Evaluate Architecture Axes

Assess architectural friction, deep module opportunities, shallow module candidates, interface complexity, test surface gaps, naming/domain mismatch, and risk sequencing.

See `references/architecture-audit-checklist.md`.

### 5. Identify Deep Module Opportunities

Look for places where complexity could move behind a smaller public interface.

Good opportunities:

- many callers repeat the same rules,
- callers know too much about ordering or invariants,
- a concept has many helpers but no clear owner,
- errors or edge cases are scattered.

See `references/deep-module-guide.md`.

### 6. Avoid Weak Recommendations

Do not produce abstract advice like "clean this up" or "improve separation."

Each recommendation must include files or modules, current friction, proposed change, locality/testability benefit, verification method, risk level, and suggested order.

### 7. Sequence Refactors

Break recommendations into small, ordered steps.

Prefer:

- add characterization or behavior tests,
- rename to domain language,
- introduce a narrow interface,
- move one rule behind the interface,
- remove pass-through wrappers.

See `references/refactor-sequencing-guide.md`.

### 8. Write Report After Approval

Use this structure:

```md
# Architecture Audit: <scope>

## Scope

## Current Map

## Findings

## Recommendations

## Risk And Sequencing

## Verification Plan

```

See `references/architecture-report-template.md`.

## Suggested Next Skill

Recommend one:

- `to-issues` when recommendations should become implementation slices.
- `tdd` when one refactor can begin behind tests.
- `prototype` when an interface or state model needs exploration.
- `zoom-out` when the audit uncovered a sub-area needing a deeper map.

Do not start the next skill automatically unless the user asks.

## Safety Rules

- Do not edit code during the audit.
- Do not create report files before approval.
- Do not recommend big rewrites.
- Do not run destructive git or filesystem commands.
- Do not ignore ADRs without explaining the conflict.
- Do not claim testability without identifying a verification path.

## Verification

Before finishing:

- State docs, source files, and tests inspected.
- State report path written or proposed.
- Confirm every recommendation references files or modules.
- Confirm each recommendation has verification guidance.
- Confirm sequencing is small and reversible.
- State the suggested next skill and why.
