---
name: tech-debt
description: >
  Systematic technical debt analysis across architecture, testing,
  documentation, and infrastructure. Investigates the codebase,
  scores findings by impact and effort, and generates a prioritized
  TECH_DEBT.md remediation plan. Delegates to specialized skills
  for code quality (scout) and linting (lint-fix). Use when
  assessing overall project health, planning cleanup sprints, or
  onboarding to an unfamiliar codebase.
compatibility: >
  Requires git. Works with any project. Enhanced analysis when
  project has linting tools, test frameworks, and CI configuration.
---
<!-- Copyright 2025-2026 Richard Shade. Licensed under Apache-2.0. -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Technical Debt Analysis

Investigate the codebase across 8 categories, score each finding by
impact and effort, and generate a prioritized TECH_DEBT.md remediation
plan. Four categories are analyzed directly; four delegate to
specialized skills.

## Prerequisite check

```bash
git --version 2>/dev/null && git rev-parse --is-inside-work-tree 2>/dev/null
```

If not in a git repository, warn but proceed — git history analysis
will be unavailable but other checks still work.

## Step 1: Project context

Gather baseline metrics before analysis:

```bash
echo "Project: $(basename $(pwd))"
echo "Files: $(find . -type f -name '*.go' -o -name '*.js' -o -name '*.ts' \
  -o -name '*.py' -o -name '*.rs' -o -name '*.cs' | grep -v node_modules \
  | grep -v vendor | grep -v .git | wc -l)"
echo "Branch: $(git rev-parse --abbrev-ref HEAD 2>/dev/null)"
echo "Last commit: $(git log -1 --format='%h %s' 2>/dev/null)"
```

Detect project type (Go, Node, Python, .NET, Rust, mixed) from
config files present.

## Step 2: Delegated categories

For categories covered by specialized skills, delegate or note
for future delegation:

**Code quality** — if the scout skill is available, run it against
recently changed files. Scout identifies the top 3 improvement
opportunities per file using Impact x Low-Risk scoring.

**Linting** — if the lint-fix skill is available, run its detection
mode (Step 1 only) to identify which linting tools are configured
and whether any are missing. Do not run the full fix pipeline.

**Security** — if the security-audit skill is available, run it for
OWASP Top 10 analysis, secrets detection, supply chain assessment,
and threat modeling. Include the security score in the tech debt
scorecard.

**Dependencies** — if the dep-upgrade skill is available, run its
audit step (Steps 1-2 only) to identify outdated and vulnerable
packages with priority categorization. Include the dependency
health score in the tech debt scorecard.

**Design principles** — if the design-principles skill is available,
run it in delegated mode against the full codebase. It audits against
SOLID, DRY, YAGNI, KISS, Law of Demeter, Separation of Concerns,
Composition over Inheritance, and the 12-Factor code-relevant subset.
Include the overall design health score in the tech debt scorecard and
pull P1 findings into the remediation roadmap.

## Step 3: Architecture analysis (direct)

Investigate the codebase for structural issues. See
`references/analysis-patterns.md` for detailed patterns.

1. **Check for god files** — find files > 500 lines with mixed
   responsibilities
2. **Check coupling** — find files importing > 10 packages
3. **Check layer violations** — look for database/HTTP logic in
   wrong layers
4. **Check for circular dependencies** — trace import patterns
5. **Identify the 3-5 most impactful architecture issues** — focus
   on what blocks new feature development or causes bugs

## Step 4: Test analysis (direct)

Measure test health. See `references/analysis-patterns.md` for
detailed patterns.

1. **Measure coverage** — run coverage tools if available
2. **Calculate test/code ratio** — count test files vs code files
3. **Identify critical untested paths** — trace entry points and
   check for test coverage at each step
4. **Flag test anti-patterns** — tests with no assertions, sleep
   synchronization, shared state, implementation testing
5. **Check for missing test types** — are there only unit tests?
   Integration? E2E?

## Step 5: Documentation analysis (direct)

Check documentation completeness. See
`references/analysis-patterns.md` for detailed patterns.

1. **Essential files** — README.md, CONTRIBUTING.md, CHANGELOG.md,
   architecture docs, API docs
2. **API documentation coverage** — ratio of documented public
   functions/types vs total
3. **Stale documentation** — references to files, functions, or
   patterns that no longer exist
4. **Missing ADRs** — significant architectural decisions without
   recorded rationale

## Step 6: Infrastructure analysis (direct)

Assess operational readiness. See
`references/analysis-patterns.md` for detailed patterns.

1. **CI/CD** — check for workflow configs, test automation, deploy
   automation
2. **Deployment** — Dockerfile, container config, deployment scripts
3. **Observability** — structured logging, error tracking, metrics,
   alerts
4. **Configuration** — env vars vs hardcoded values, secrets
   management

## Step 7: Score each category

Score every category 0-10 using the scoring rubric in
`references/scoring-guide.md`. Assign impact
(LOW/MEDIUM/HIGH/CRITICAL) and effort (S/M/L/XL) to each finding.

Calculate priority: P1 (high impact, low effort) through P4
(low impact, high effort).

## Step 8: Generate TECH_DEBT.md

Write the report using the template in `references/scoring-guide.md`.
Include:

- Executive summary with overall health score (sum of 9 categories,
  out of 90)
- Scorecard table with all 9 categories
- Detailed findings per category with evidence and remediation
- Remediation roadmap organized by priority (P1 → P4)
- Success metrics with current and target values

Run markdownlint on the generated file.

## Step 9: Present summary

Show the user:

1. Scorecard table (8 categories, scores, top issue per category)
2. Overall health score (X/80)
3. P1 items requiring immediate attention
4. Top 5 remediation priorities with estimated effort
5. Ask which items to address first
