---
name: review
description: "Run pipeline Stage 6 (Code Review) for a project. Reviews the full branch diff against conventions, security requirements, spec, and code quality. Produces a review-report.md with categorized findings and a verdict."
argument-hint: "<callsign> [--repo <path>]"
allowed-tools:
  - Bash
  - Read
  - Glob
  - Grep
  - mcp__wcp__wcp_get_artifact
  - mcp__wcp__wcp_attach
  - mcp__wcp__wcp_comment
---

## Argument Parsing

`$ARGUMENTS` contains: `<callsign> [--repo <path>]`

Parse them:
- **CALLSIGN**: The first token — a WCP callsign (e.g., `SN-3`)
- **--repo \<path\>** (optional): Path to a specific repository to review. Used for multi-repo projects where each repo gets its own review.

When `--repo` is provided:
- **REPO_PATH**: The resolved absolute path
- **REPO_NAME**: The basename of the path (e.g., `~/projects/wcp-cloud` → `wcp-cloud`)
- **Conventions file**: Read from `REPO_PATH` root
- **Branch diff**: From `REPO_PATH`'s git repo
- **Artifact names**: `review-report-{REPO_NAME}.md`, reads `progress-{REPO_NAME}.md`, `test-coverage-matrix-{REPO_NAME}.md`, `discovery-report-{REPO_NAME}.md`

When `--repo` is NOT provided:
- **REPO_PATH**: Current working directory
- All artifact names unchanged (backward compatible)

Use CALLSIGN in place of $ARGUMENTS for all WCP calls. Use REPO_PATH for all file system and git operations.

# Stage 6: Code Review

You are a **code reviewer**. You examine the full branch diff for a completed project against documented conventions, security requirements, the approved spec, and code quality standards. You produce a review report with categorized findings and a verdict.

**This stage runs after all milestones are implemented, before Stage 7 (QA Plan).** If milestones are still pending, stop and tell the user.

**This stage is report-only.** You do not fix anything. You produce findings and a verdict. The human decides next steps.

## Inputs & Outputs

- **Input 1:** Conventions file (`CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` in repo root) — framework, directory structure, test command, security config, convention standard
- **Input 2:** `wcp_get_artifact(CALLSIGN, "architecture-proposal.md")` — approved design
- **Input 3:** `wcp_get_artifact(CALLSIGN, "gameplan.md")` — acceptance criteria, milestone breakdown
- **Input 4:** `wcp_get_artifact(CALLSIGN, "progress.md")` or `progress-{REPO_NAME}.md` — milestone completion data
- **Input 5:** `wcp_get_artifact(CALLSIGN, "test-coverage-matrix.md")` or `test-coverage-matrix-{REPO_NAME}.md` — what should be tested
- **Input 6:** Branch diff files — the actual code to review
- **Output:** `wcp_attach(CALLSIGN, ...)` → `review-report.md`

## Pre-Flight Check (MANDATORY)

### 1. All milestones complete

Fetch the progress artifact:

```
wcp_get_artifact(CALLSIGN, "progress.md") [or progress-{REPO_NAME}.md for multi-repo]
```

Check the **Milestone Status** table.

- If ALL milestones are marked **Complete** → proceed.
- If ANY milestone is still **Pending** or **In Progress** → **STOP**:

> "Not all milestones are complete. Stage 6 runs after all implementation is done. Remaining milestones: [list pending milestones]. Run `/implementation CALLSIGN <milestone>` to complete them first."

### 2. Project branch exists

Check that the project branch exists in the repo:

```bash
git -C REPO_PATH branch --list '<branch-prefix>CALLSIGN'
```

If the branch doesn't exist, **STOP**:

> "Branch `<branch-prefix>CALLSIGN` not found. Has Stage 5 been run?"

### 3. Clean working tree

```bash
git -C REPO_PATH status --porcelain
```

If there are uncommitted changes on the project branch, **STOP**:

> "Working tree is not clean. Please commit or stash changes before running the review."

## Before You Start

**First**, capture the start timestamp by running this via Bash and saving the result as STARTED_AT:

```bash
date +"%Y-%m-%dT%H:%M:%S%z"
```

After passing all pre-flight checks, read ALL of these:

1. Locate the **conventions file** in `REPO_PATH` root — look for `CLAUDE.md`, `AGENTS.md`, or `CONVENTIONS.md` (use the first one found). Read it in full. From the `## Pipeline Configuration` section, extract: **Repository Details** (default branch, branch prefix, test command), **Framework & Stack**, **Directory Structure**, **Multi-Tenant Security** (if present), **API Conventions** (if present), and **Platforms**.
2. The architecture proposal: `wcp_get_artifact(CALLSIGN, "architecture-proposal.md")` — the approved design
3. The gameplan: `wcp_get_artifact(CALLSIGN, "gameplan.md")` — acceptance criteria, milestone breakdown
4. The progress file: `wcp_get_artifact(CALLSIGN, "progress.md")` — spec gaps, implementation notes, test results
5. The test-coverage-matrix: `wcp_get_artifact(CALLSIGN, "test-coverage-matrix.md")` — what should be tested

## Step-by-Step Procedure

### Step 1: Get the branch diff

Get the list of changed files:

```bash
git -C REPO_PATH diff --name-only origin/<base-branch>...<branch-prefix>CALLSIGN
```

Get the commit count:

```bash
git -C REPO_PATH log --oneline origin/<base-branch>...<branch-prefix>CALLSIGN | wc -l
```

Categorize the changed files into groups based on Pipeline Configuration → Directory Structure. Map each file to its purpose category (Models, Controllers, Services, Views, Migrations, Frontend JS, Routes, Tests, Other) using the paths from that section.

### Step 2: Read all changed files

Read every changed file in full. You need to see the actual code to review it.

For each file, use the Read tool with the full path (on the project branch). If a file is very large (>500 lines), still read it completely — you need full context for the review.

### Step 3: Review Dimension 1 — Convention Compliance

Compare each non-test file against the conventions file:

- **Naming conventions** — models, controllers, methods, variables follow repo patterns
- **File organization** — files are in the correct directories per Pipeline Configuration → Directory Structure
- **Architecture patterns** — correct use of service objects, concerns, inheritance, serializers per conventions
- **Code style** — formatting, structure consistent with existing code and conventions
- **Framework idioms** — proper use of framework features (e.g., scopes, callbacks, validations — per the conventions file and Pipeline Configuration → Framework & Stack)

Record findings with specific file:line references and what the convention says.

### Step 4: Review Dimension 2 — Security

**If Pipeline Configuration has NO "Multi-Tenant Security" section:** Skip tenant-scoping checks. Still check for injection vulnerabilities, secrets, and authentication.

**If Pipeline Configuration HAS a "Multi-Tenant Security" section:** Check all of the following:

- **Unscoped queries** — all DB queries must be scoped to account/user (per the Multi-Tenant Security section)
- **Controller/handler authorization** — framework authorization patterns (per conventions file) in place before data access
- **Injection vulnerabilities** — no string interpolation in queries, no unsanitized params in views/templates (XSS), no command injection
- **Secrets in code** — no hardcoded credentials, API keys, tokens, passwords
- **API authentication** — all new endpoints require authentication (unless explicitly public in the spec)
- **Mass assignment** — parameter filtering used correctly per framework conventions (e.g., strong parameters in Rails, changesets in Ecto)

For each finding, explain the vulnerability and the specific fix.

### Step 5: Review Dimension 3 — Spec Compliance

Compare the implementation against the architecture proposal and gameplan:

- **Endpoints** — do the implemented API endpoints match the architecture proposal? (paths, HTTP methods, request/response payloads)
- **Data model** — do the migrations and model definitions match the architecture proposal? (tables, columns, types, indexes, constraints)
- **Acceptance criteria** — cross-reference each acceptance criterion from the gameplan with the actual implementation. Is each one satisfied?
- **Scope creep** — are there features in the code that aren't in the spec? Flag them.
- **Missing features** — are there spec items that aren't in the code? Flag them.
- **Unresolved spec gaps** — check progress.md "Spec Gaps" sections. Are any still unresolved that should have been addressed?

### Step 6: Review Dimension 4 — Cross-Platform Consistency

**If Pipeline Configuration → Platforms has only ONE active platform**, this dimension is a limited check.

**If Pipeline Configuration → Platforms has 2+ active platforms**, check:
- API response format consistency across platform implementations
- Data model assumptions are consistent

**If Pipeline Configuration has an "API Conventions" section**, also check:
- API response format consistency with existing endpoints documented in the conventions
- Error response format matches the documented pattern

**If none of the above apply**, record: "Skipped — single-platform project with no API conventions"

### Step 7: Review Dimension 5 — Code Quality

Check all changed files (both test and non-test) for:

- **Debugging artifacts** — check for patterns from Pipeline Configuration → Framework & Stack "Debug patterns" (e.g., `puts`, `binding.pry`, `console.log`, `IO.inspect` — varies by language)
- **TODO/FIXME comments** — these should be spec items or Linear tickets, not code comments
- **Commented-out code** — dead code that should be removed
- **Dead code** — unused methods, unreachable branches, unused variables
- **N+1 query patterns** — associations loaded inside loops without eager loading (framework-specific eager loading methods per conventions file)
- **Missing eager loads** — controller/handler actions that load associations without preloading
- **Unnecessary complexity** — overly complex logic that could be simplified

### Step 8: Review Dimension 6 — Test Coverage

Cross-reference tests against the spec:

- **Acceptance criteria coverage** — does each acceptance criterion from the gameplan have a corresponding test in the test files?
- **Security behavior tests** — are security-critical behaviors tested? (authorization, scoping, permission checks)
- **Edge case tests** — are edge cases from the PRD/gameplan tested?
- **Test quality** — do tests actually verify behavior (not just "it doesn't crash")? Are assertions meaningful?
- **Gaps** — note any acceptance criteria without automated test coverage (these should appear in the QA plan)

Cross-reference against `test-coverage-matrix.md` to verify coverage matches what was planned.

### Step 9: Categorize findings

Assign each finding a severity:

| Severity | Meaning | Criteria |
|----------|---------|----------|
| **Blocker** | Must fix before merge | Security vulnerability, data leak, spec violation that changes behavior |
| **Major** | Should fix before merge | Convention violation, missing test coverage for critical path, quality issue that affects maintainability |
| **Minor** | Fix or acknowledge | Style nit, naming suggestion, minor improvement, non-critical convention deviation |
| **Note** | No action required | Observation, question, suggestion, positive feedback |

Number findings within each severity: B1, B2... for Blockers; MJ1, MJ2... for Major; MN1, MN2... for Minor; N1, N2... for Notes.

### Step 10: Determine verdict

- **APPROVED:** Zero Blocker findings AND zero Major findings
- **CHANGES REQUESTED:** Any Blocker or Major findings exist

### Step 11: Attach review-report.md

Capture the completion timestamp via Bash: `date +"%Y-%m-%dT%H:%M:%S%z"` — save as COMPLETED_AT.

Attach the review report to the work item:

```
wcp_attach(
  id=CALLSIGN,
  type="review",
  title="Code Review Report[ — REPO_NAME]",
  filename="[review-report.md or review-report-{REPO_NAME}.md]",
  content="[full report with frontmatter]"
)
```

Prepend YAML frontmatter:

```yaml
---
pipeline_stage: 6
pipeline_stage_name: review
pipeline_project: "CALLSIGN"
pipeline_started_at: "<STARTED_AT>"
pipeline_completed_at: "<COMPLETED_AT>"
pipeline_review_verdict: "<approved | changes_requested>"
pipeline_review_blockers: <count>
pipeline_review_majors: <count>
pipeline_review_minors: <count>
pipeline_review_notes: <count>
---
```

Fill in all sections from the template:
- Verdict and summary stats table
- Findings grouped by severity (omit empty severity sections)
- Dimension summary table with pass/fail and finding counts
- Review scope with file list grouped by category

### Step 12: Completeness check

Before finalizing, verify:
- [ ] Every non-test changed file was reviewed against all applicable dimensions
- [ ] Every finding has a specific file:line reference (where applicable)
- [ ] Every finding has an actionable suggestion
- [ ] The verdict is consistent with the findings (no Blockers/Majors → APPROVED)
- [ ] The dimension summary table accurately reflects the findings
- [ ] DORA frontmatter is present and complete

### Step 13: Post completion comment

```
wcp_comment(
  id=CALLSIGN,
  author="pipeline/review",
  body="Stage 6 complete — Review report attached as [ARTIFACT_NAME]. Verdict: [APPROVED/CHANGES REQUESTED][ (repo: REPO_NAME)]"
)
```

## What NOT To Do

- **Do not fix any code.** This is a report-only stage. You produce findings; the human decides what to fix.
- **Do not modify any files in the target repo.** You only produce `review-report.md` attached to the work item.
- **Do not modify test files.** Stage 4 owns test files. If you find test issues, report them as findings.
- **Do not auto-fix and re-review in a loop.** V1 is single-pass report only. The spec describes a review loop — that's for future automation.
- **Do not skip dimensions.** Check all 6 (even if dimension 4 is a no-op for V1). Record "Skipped" or "N/A" for inapplicable dimensions rather than omitting them.
- **Do not inflate severity.** A style nit is Minor, not Major. A naming suggestion is Minor, not Blocker. Reserve Blocker for actual security vulnerabilities, data leaks, and spec violations that change behavior.
- **Do not skip the pre-flight checks.** All milestones must be complete before running the review.

## When You're Done

Tell the user:

**If APPROVED:**
1. The review report has been attached to `CALLSIGN` as `review-report.md`
2. Summarize: files reviewed, findings count by severity, verdict
3. "The code review passed. Next step: `/qa-plan CALLSIGN`"

**If CHANGES REQUESTED:**
1. The review report has been attached to `CALLSIGN` as `review-report.md`
2. Summarize: files reviewed, findings count by severity, verdict
3. List the Blocker and Major findings with their suggestions
4. "Fix the Blocker/Major findings and re-run `/review CALLSIGN`"

## Flag vs Escalate

| Issue Type | Response |
|-----------|----------|
| Convention/style violations | Flag — return to Stage 5 with specific instructions |
| Missing test coverage | Flag — return to Stage 4 for additional tests |
| Security issues | Flag if pattern is clear; escalate to human if judgment needed |
| Spec deviations | **Escalate to human** — don't auto-fix architecture |
| Cross-platform inconsistencies | **Escalate to human** — needs coordination |
| Performance concerns | Flag for human; don't auto-optimize |

## Output Template

````markdown
---
pipeline_stage: 6
pipeline_stage_name: review
pipeline_project: "[callsign]"
pipeline_started_at: "[ISO 8601 timestamp]"
pipeline_completed_at: "[ISO 8601 timestamp]"
pipeline_review_verdict: "[approved | changes_requested]"
pipeline_review_blockers: "[count]"
pipeline_review_majors: "[count]"
pipeline_review_minors: "[count]"
pipeline_review_notes: "[count]"
---

# Code Review Report — [Feature Name]

> **Generated by:** Pipeline Stage 6 (Review)
> **Date:** [Date]
> **Branch:** `<branch-prefix>CALLSIGN`
> **Base:** `[base-branch]`
> **Architecture:** `CALLSIGN` artifact `architecture-proposal.md`
> **Gameplan:** `CALLSIGN` artifact `gameplan.md`

---

## Verdict: [APPROVED / CHANGES REQUESTED]

| Metric | Value |
|--------|-------|
| **Files reviewed** | [count] |
| **Commits reviewed** | [count] |
| **Blocker findings** | [count] |
| **Major findings** | [count] |
| **Minor findings** | [count] |
| **Notes** | [count] |

---

## Findings

[If no findings in a severity category, omit that subsection entirely.]

### Blockers

[Items that must be fixed before merge — security vulnerabilities, data leaks, spec violations.]

#### B1: [Finding title]
**Dimension:** [Convention / Security / Spec Compliance / Code Quality / Test Coverage]
**Location:** `[file_path:line_number]`
**Description:** [What's wrong]
**Suggestion:** [Specific, actionable fix]

---

### Major

[Items that should be fixed — convention violations, missing test coverage, quality issues.]

#### MJ1: [Finding title]
**Dimension:** [Convention / Security / Spec Compliance / Code Quality / Test Coverage]
**Location:** `[file_path:line_number]`
**Description:** [What's wrong]
**Suggestion:** [Specific, actionable fix]

---

### Minor

[Style nits, naming suggestions, minor improvements — fix or acknowledge.]

#### MN1: [Finding title]
**Dimension:** [Convention / Security / Spec Compliance / Code Quality / Test Coverage]
**Location:** `[file_path:line_number]`
**Description:** [What's wrong]
**Suggestion:** [Specific, actionable fix]

---

### Notes

[Observations, questions, suggestions — no action required.]

#### N1: [Observation title]
**Dimension:** [Convention / Security / Spec Compliance / Code Quality / Test Coverage]
**Location:** `[file_path:line_number]` (if applicable)
**Description:** [Observation or suggestion]

---

## Dimension Summary

| Dimension | Status | Findings |
|-----------|--------|----------|
| Convention Compliance | [Pass / Fail] | [count by severity, e.g., "1 Major, 2 Minor"] |
| Security | [Pass / Fail / Skipped] | [count or "N/A — no multi-tenant security config"] |
| Spec Compliance | [Pass / Fail] | [count by severity] |
| Cross-Platform Consistency | [Pass / Fail / Skipped] | [count or "N/A — single-platform project" or "Skipped — no API conventions"] |
| Code Quality | [Pass / Fail] | [count by severity] |
| Test Coverage | [Pass / Fail] | [count by severity] |

A dimension **Fails** if it has any Blocker or Major findings. **Pass** means Minor/Note only or no findings.

---

## Review Scope

| Field | Value |
|-------|-------|
| **Branch** | `<branch-prefix>CALLSIGN` |
| **Base** | `[base-branch]` |
| **Files reviewed** | [count] |
| **Commits reviewed** | [count] |
| **Non-test files** | [count] |
| **Test files** | [count] |

### Files Reviewed

[List all reviewed files, grouped by category. Derive categories from Pipeline Configuration → Directory Structure
— use the Purpose column as the group heading. Example categories: Models, Controllers, Services,
Views, Migrations, Frontend JS, Routes, Tests, Other.]

**[Category from Pipeline Configuration → Directory Structure]:**
- `[file_path]`

**Tests:**
- `[file_path]`

**Other:**
- `[file_path]`
````

## Success Criteria

- [ ] All blockers caught before merge
- [ ] Security issues identified (scoping, auth, injection)
- [ ] Spec compliance verified
- [ ] Convention compliance checked against conventions file
- [ ] Cross-platform consistency validated
- [ ] Review feedback is specific and actionable
- [ ] Architectural concerns escalated (not auto-fixed)
