---
name: quality-check
description: Quality assessment framework using 11 parallel explore subagents across code, testing, security, architecture, documentation, operations, frontend, backend, data, performance, and tech-debt governance. Reads KB quality standards calibrated by the project's Quality Profile (quality-standards.yaml). Produces scored assessments with HTML spider chart, JSON, and Markdown reports. Use when assessing project quality, running quality audits, checking production readiness, or evaluating tech debt governance.
user-invocable: false
---

# Quality Check

LTM-driven quality assessment framework using **11 parallel explore subagents** across 11 dimensions, calibrated by the project's Quality Profile.

## Workflow

1. **Gather context** — repo path, detect stack, load Quality Profile
2. **Load KB standards** — search Project LTM then KB, filter by stack
3. **Launch 11 subagents** — batched 4+4+3, each with KB standards + QP levels
4. **Synthesize** — combine results, calculate scores/grades/compliance
5. **Generate reports** — HTML (11-axis spider chart) + JSON + MD

## Step 1: Gather Context

Determine:
- **Repository path**: Use current working directory or user-specified path
- **Stack detection**: Auto-detect from package.json, requirements.txt, go.mod, pom.xml, *.csproj, Cargo.toml, etc.
  - Frontend frameworks: React, Vue, Angular, Svelte, Next.js, Nuxt
  - Backend frameworks: Express, FastAPI, Django, Spring, .NET, Go, Rails
  - If no frontend detected → frontend subagent returns all N/A
  - If no backend detected → backend subagent returns all N/A
- **Quality Profile**: Load `quality-standards.yaml` from project root or `.garura/` directory

### Quality Profile Loading

```yaml
# quality-standards.yaml structure
dimensions:
  testing:          3  # QP-1: Testing Depth (1-5)
  code_quality:     3  # QP-2: Code Quality Standards
  documentation:    3  # QP-3: Documentation Level
  ci_cd:            3  # QP-4: CI/CD Maturity
  observability:    3  # QP-5: Observability
  accessibility:    3  # QP-6: Accessibility
  security_testing: 3  # QP-7: Security Testing
```

**Fallback:** If `quality-standards.yaml` is absent, default ALL QP dimensions to level 3. Note this in report metadata: `"qp_source": "default (no quality-standards.yaml found)"`.

## Step 2: Load KB Standards

**Three-layer search order:**
1. **Project LTM** — `{project}/.garura/core/memory/knowledge/quality/` — project-specific overrides
2. **KB (Memory Bank)** — `~/.garura/core/memory/knowledge/quality/` — framework defaults
3. If neither found — HALT: "No quality KB found. Run /sud:install to deploy quality standards."

For each of the 11 domains, load the knowledge files from the resolved path. Filter check items by detected stack (e.g., skip frontend files for backend-only projects).

**KB file inventory per domain:**

| Domain | Files | ID Prefix |
|--------|-------|-----------|
| Code Quality | `code/linting-formatting.md`, `code/complexity-structure.md`, `code/naming-conventions.md`, `code/error-handling-patterns.md` | CODE |
| Testing | `testing/unit-testing.md`, `testing/integration-e2e-testing.md`, `testing/coverage-test-patterns.md` | TEST |
| Security | `security/owasp-secure-coding.md`, `security/auth-data-protection.md`, `security/secrets-vulnerability-mgmt.md` | SEC |
| Architecture | `architecture/separation-of-concerns.md`, `architecture/dependency-management.md`, `architecture/api-design-scalability.md` | ARCH |
| Documentation | `documentation/api-architecture-docs.md`, `documentation/developer-onboarding.md` | DOC |
| Operations | `operations/cicd-quality-gates.md`, `operations/monitoring-alerting.md`, `operations/deployment-incident-response.md` | OPS |
| Frontend | `frontend/accessibility-performance.md`, `frontend/component-architecture.md`, `frontend/state-management-patterns.md` | FE |
| Backend | `backend/api-design-validation.md`, `backend/async-error-handling.md`, `backend/database-caching.md` | BE |
| Data & Privacy | `data/schema-design.md`, `data/migrations-versioning.md`, `data/privacy-compliance.md` | DATA |
| Performance | `performance/load-testing-profiling.md`, `performance/slos-reliability.md`, `performance/resource-optimization.md` | PERF |
| Tech Debt | `tech-debt/fowler-quadrant.md`, `tech-debt/debt-register-governance.md`, `tech-debt/accepted-vs-unaccepted.md` | DEBT |

## Step 3: Launch Subagents

**CRITICAL**: Launch in batches due to concurrent agent limits. All subagents use `subagent_type: "explore"`.

Inform user: "Launching 11 quality assessment agents in 3 batches. This will take 3-5 minutes..."

### Subagent Configuration

| # | Category | QP Dimension | Batch |
|---|----------|-------------|-------|
| 1 | Code Quality | QP-2 (`code_quality`) | 1 |
| 2 | Testing | QP-1 (`testing`) | 1 |
| 3 | Security | QP-7 (`security_testing`) | 1 |
| 4 | Architecture | Universal | 1 |
| 5 | Documentation | QP-3 (`documentation`) | 2 |
| 6 | Operations | QP-4 (`ci_cd`) + QP-5 (`observability`) | 2 |
| 7 | Frontend | QP-6 (`accessibility`) | 2 |
| 8 | Backend | Universal | 2 |
| 9 | Data & Privacy | Universal | 3 |
| 10 | Performance | Universal | 3 |
| 11 | Tech Debt Governance | Universal | 3 |

### Prompt Loading

Load prompts from [reference/subagent-prompts.md](reference/subagent-prompts.md). Each prompt receives:
- KB file content for its domain (read from resolved KB path)
- QP level for its dimension (from quality-standards.yaml or default 3)
- Repository path to assess

**Batch 1** (launch first): Subagents 1-4
**Batch 2** (after batch 1 completes): Subagents 5-8
**Batch 3** (after batch 2 completes): Subagents 9-11

### Subagent Output Schema

Each subagent returns structured JSON:

```json
{
  "category": "string",
  "qp_level": 3,
  "findings": [
    {
      "id": "CODE-01",
      "check_item": "Linter configured and running",
      "status": "done|ongoing|not_done|n_a",
      "evidence": "path/to/file:line — description",
      "notes": "optional context"
    }
  ],
  "summary": "one paragraph assessment",
  "score": 0.85
}
```

**Tech Debt subagent extended schema** — includes Fowler quadrant classification:

```json
{
  "category": "tech_debt",
  "qp_level": null,
  "findings": [...],
  "debt_items": [
    {
      "description": "...",
      "location": "path/to/file:line",
      "quadrant": "deliberate-prudent|deliberate-reckless|inadvertent-prudent|inadvertent-reckless",
      "tracked": true,
      "has_timeline": true
    }
  ],
  "summary": "...",
  "score": 0.70
}
```

## Step 4: Synthesize Results

After all 11 subagents complete:

### 4.1 Combine Data

Merge all 11 JSON results into a unified assessment. Cross-reference findings across categories for systemic issues (e.g., security + code quality both flagging the same pattern).

### 4.2 Calculate Scores

**Per-category compliance:**
```
compliance = (Done × 1.0 + Ongoing × 0.5) / (Total - N/A) × 100%
```

**Per-category grade:**

| Score Range | Grade | Label |
|-------------|-------|-------|
| 90-100% | A | Excellent |
| 80-89% | B | Good |
| 65-79% | C | Acceptable |
| 50-64% | D | Concerning |
| 0-49% | E | Critical |

**Overall score:** Weighted average across non-N/A categories (equal weights).

### 4.3 Identify Systemic Issues

Cross-reference patterns:
- Same file flagged by multiple subagents → systemic quality issue
- Error handling flagged in both code + backend → pervasive pattern
- No tests + no CI → compounding gap

### 4.4 Tech Debt Summary

From tech debt subagent results:
- Total debt items found
- Quadrant distribution (deliberate-prudent vs reckless)
- Tracked vs untracked ratio
- Items with repayment timelines vs without
- Debt decay (items > 6 months old without progress)

## Step 5: Generate Reports

Use templates from [templates/](templates/):
- `assessment-data.json` — JSON structure template
- `assessment-report.html` — Interactive HTML template

### Output Path

**Issue-scoped** (when running within an issue context):
```
{stm_base}/{issue}/evidence/quality-check/{YYYY-MM-DD_HHmmss}/
```

**Standalone** (no issue context):
```
.quality-check/{YYYY-MM-DD_HHmmss}/
```

### Output Files

1. **`assessment-data.json`** — Structured assessment data
   - All 11 category results with findings
   - Scores, grades, compliance percentages
   - Tech debt quadrant distribution
   - Metadata (repo path, stack, QP source, timestamp)

2. **`assessment-report.html`** — Interactive HTML report
   - 11-axis spider chart (Chart.js radar)
   - Category ratings with compliance bars
   - Interactive status toggles (Done/Ongoing/Not Done/N/A)
   - Tech debt quadrant visualization
   - Evidence links per finding
   - Export to Markdown
   - Persistent ratings (localStorage)

3. **`assessment-summary.md`** — Executive summary
   - Overall score and grade
   - Per-category grades in table
   - Top 5 critical findings
   - Tech debt governance summary
   - Systemic issues identified
   - Recommended next actions

### Report Generation

Read template files, inject assessment data, write output files.

Present to user:
```markdown
## Quality Assessment Complete

**Overall Score:** {score}% ({grade})
**Categories Assessed:** {count}/11

| Category | Score | Grade | Findings |
|----------|-------|-------|----------|
| Code Quality | 85% | B | 30 items |
| Testing | 72% | C | 26 items |
| ... | ... | ... | ... |

**Tech Debt:** {total_items} items — {tracked_pct}% tracked, {prudent_pct}% deliberate-prudent

**Reports saved to:** {output_path}
- `assessment-data.json`
- `assessment-report.html`
- `assessment-summary.md`
```

## Error Handling

| Scenario | Action |
|----------|--------|
| Large monorepo | Sample key directories: src/, lib/, app/, tests/, packages/ |
| Subagent fails | Retry once, then mark category with warning |
| Unknown framework | Use generic analysis patterns |
| No KB found | HALT with deployment instructions |
| No quality-standards.yaml | Default QP level 3, note in report |
| Frontend-only project | Backend subagent returns all N/A, excluded from overall score |
| Backend-only project | Frontend subagent returns all N/A, excluded from overall score |

## Read-Only Guarantee

This skill NEVER modifies project files. It reads code, configuration, and documentation to assess quality. All output goes to the designated output directory only.
