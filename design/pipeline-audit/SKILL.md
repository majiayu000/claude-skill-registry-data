---
name: pipeline-audit
version: 1.0.0
description: "Full system audit pipeline — runs backend, security, operations, design, and product critiques in parallel, aggregates findings, validates with QA, and produces a unified audit report. Use for pre-launch reviews, periodic health checks, or compliance audits."
---

# Pipeline: System Audit

You are orchestrating a full system audit. All applicable critique skills run in parallel, findings are aggregated and deduplicated, then validated with browser-based QA.

## Input

- **project-path**: The project to audit (defaults to cwd)
- **scope** (optional): `full` (default) | `backend-only` | `frontend-only` | `security-only` | `infra-only`
- **url** (optional): Live URL for QA validation stage

## Pipeline State

Create a tracker at `.gstack/pipeline-audit-{date}.md`.

```markdown
## Pipeline: System Audit
Started: {timestamp}
Project: {project-path}
Scope: {scope}

| # | Stage | Status | Gate | Notes |
|---|-------|--------|------|-------|
| 1 | CRITIQUE | pending | — | — |
| 2 | AGGREGATE | pending | — | — |
| 3 | QA VALIDATION | pending | — | — |
| 4 | REPORT | pending | — | — |
```

---

## Stage 1: PARALLEL CRITIQUES

Detect which critiques apply by scanning the project:

```bash
# Check what exists in the project
ls -la src/ app/ lib/ server/ api/ 2>/dev/null        # backend indicators
ls -la src/components/ pages/ app/ *.tsx *.vue 2>/dev/null  # frontend indicators
ls -la Dockerfile docker-compose* .github/ terraform/ 2>/dev/null  # infra indicators
ls -la docs/ specs/ PRD* 2>/dev/null                  # product spec indicators
```

Dispatch applicable critiques as **parallel subagents** (Agent tool, all in one message):

| Indicator | Critique | Always run? |
|---|---|---|
| Any backend code exists | `/backend-critique` | Yes (unless frontend-only scope) |
| Any code exists | `/security-critique` | Yes (always) |
| Infra files exist | `/operations-critique` | Yes (unless frontend-only) |
| UI/frontend files exist | `/design-critique` | Only if UI exists |
| Specs/PRDs exist | `/product-critique` | Only if specs exist |

Each subagent receives:
- The project path
- Its specific critique skill to invoke
- Instructions to produce a structured report with grade (A-F) and severity-tiered findings

**Gate:** All subagents complete. Collect all reports.

**On pass:** Update tracker → PASS with individual grades.

---

## Stage 2: AGGREGATE

Combine all critique reports into a unified findings list:

### 2a: Merge findings
Collect all findings from all critiques into a single list.

### 2b: Deduplicate
Cross-reference findings across critiques. Common overlaps:
- Security critique + backend critique: both may flag auth issues
- Operations critique + security critique: both may flag secrets exposure
- Design critique + product critique: both may flag UX issues

Merge duplicate findings, keeping the higher severity and combining the descriptions.

### 2c: Priority sort
Sort unified findings by severity: Critical → High → Medium → Low.

### 2d: Cross-cutting themes
Identify patterns across critiques:
- Are there systemic issues (e.g., "no error handling anywhere")?
- Are there architectural concerns flagged by multiple critiques?
- Are there quick wins that appear in multiple reports?

**Gate:** Aggregated report produced with deduplicated, priority-sorted findings.

---

## Stage 3: QA VALIDATION (conditional)

**Skip if:** No live URL provided and no dev server can be started.

**Run if:** A URL is available or a dev server can be started.

Invoke `/qa-only` to browser-test the top findings:
- Focus on Critical and High severity items that have UI implications
- Verify that flagged issues are actually visible/reproducible
- Capture screenshots as evidence

**Gate:** QA report produced. Findings confirmed or disputed with evidence.

---

## Stage 4: REPORT

Produce the unified audit report:

```markdown
## System Audit Report
Project: {project-path}
Date: {timestamp}
Scope: {scope}

### Summary
- Total findings: {N}
- Critical: {n} | High: {n} | Medium: {n} | Low: {n}
- Critiques run: {list}

### Grades by Domain
| Domain | Critique | Grade | Top Issue |
|---|---|---|---|
| Backend | backend-critique | {A-F} | {one-liner} |
| Security | security-critique | {A-F} | {one-liner} |
| Operations | operations-critique | {A-F} | {one-liner} |
| Design | design-critique | {A-F} | {one-liner} |
| Product | product-critique | {A-F} | {one-liner} |

### Overall Grade: {weighted average}

### Critical Findings (fix immediately)
{numbered list with file:line, description, which critique found it}

### High Findings (fix before next release)
{numbered list}

### Cross-Cutting Themes
{patterns identified in Stage 2d}

### Quick Wins (high impact, low effort)
{top 5 items that can be fixed quickly}

### QA Validation
{QA findings confirming or disputing critique findings, with screenshots}
```

### Persist
- Save report to `.gstack/audit-reports/audit-{date}.md`
- Invoke `/obsidian-vault` to persist audit results (background)
- Invoke `/graphify` on the audit report to map risk areas (background)

---

## Final Pipeline Report

```markdown
## Pipeline Report: System Audit
Project: {project-path}
Run: {timestamp}
Duration: {total elapsed}

| # | Stage | Result | Duration | Notes |
|---|-------|--------|----------|-------|
| 1 | CRITIQUE | {grades} | {time} | {N critiques run in parallel} |
| 2 | AGGREGATE | PASS | {time} | {N findings, M deduplicated} |
| 3 | QA | {PASS/SKIPPED} | {time} | {N findings validated} |
| 4 | REPORT | PASS | {time} | Saved to {path} |

Overall Grade: {weighted average of all critique grades}
Top 3 Actions: {three most impactful fixes}
```
