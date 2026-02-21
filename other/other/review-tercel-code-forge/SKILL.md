---
name: review
description: Review code quality for a completed feature or entire project — checks code, tests, security, and plan/doc consistency.
---

# Code Forge — Review

Review code quality against its reference documents, checking code quality, test coverage, security, and consistency.

Supports two modes:
- **Feature mode:** Review a single feature against its `plan.md`
- **Project mode:** Review the entire project against planning documents or upstream docs

## When to Use

- Feature implementation is complete or nearly complete
- Want to verify code quality before creating a PR
- Need a structured review against the original plan or documentation
- Want a holistic project-level quality check

## Workflow

```
Config → Determine Mode → Locate Reference → Collect Scope → Multi-Dimension Review (sub-agent) → Display Report → Update State → Summary
```

## Context Management

The review analysis is offloaded to a sub-agent to handle large diffs without exhausting the main context.

## Detailed Steps

@../shared/configuration.md

---

### Step 1: Determine Review Mode

Parse the user's arguments to determine which mode to use.

#### 1.1 Feature Name Provided

If the user provided a feature name (e.g., `/code-forge:review user-auth`):

→ **Feature Mode** — go to Step 2F

#### 1.2 `--project` Flag Provided

If the user passed `--project` (e.g., `/code-forge:review --project`):

→ **Project Mode** — go to Step 2P

#### 1.3 No Arguments

If no arguments provided:

1. Scan `{output_dir}/*/state.json` for all features
2. Filter to features with at least one `"completed"` task
3. Build choice list:
   - If completed features exist: include each as an option, **plus** "Review entire project" as the last option
   - If no completed features: go to **Project Mode** automatically
4. If only one option (project review): go to **Project Mode** automatically
5. If multiple options: use `AskUserQuestion` to let user select

---

### Step 2F: Feature Mode — Locate Feature

#### 2F.1 Find Feature

1. Look for `{output_dir}/{feature_name}/state.json`
2. If not found: show error, list available features

#### 2F.2 Load Feature Context

1. Read `state.json`
2. Read `plan.md` (for acceptance criteria and architecture)
3. Note completed task count and overall progress

→ Go to Step 3F

---

### Step 2P: Project Mode — Locate Reference

Determine the reference level using a fallback chain.

#### 2P.1 Check for Planning Documents (Level 1: Planning-backed)

Scan `{output_dir}/*/plan.md`:

- If one or more `plan.md` files found → **planning-backed**
- Read all `plan.md` files and aggregate:
  - Acceptance criteria from each feature
  - Architecture decisions
  - Technology stack
- Read corresponding `state.json` files for progress context
- Record: `reference_level = "planning"`
- Record: list of plan file paths and aggregated criteria
- → Go to Step 3P

#### 2P.2 Check for Documentation (Level 2: Docs-backed)

If no planning documents found, scan for upstream documentation:

Search paths (in order):
1. `{input_dir}/*.md` — feature specs
2. `docs/` directory — PRD, SRS, tech-design, test-plan files

Look for files matching patterns:
- `**/prd.md`, `**/srs.md`, `**/tech-design.md`, `**/test-plan.md`
- `**/features/*.md`
- Any `.md` files directly under `docs/`

If documentation files found → **docs-backed**:
- Read all found docs
- Extract: requirements, architecture decisions, acceptance criteria, scope definitions
- Record: `reference_level = "docs"`
- Record: list of doc file paths and extracted criteria
- → Go to Step 3P

#### 2P.3 No Reference (Level 3: Bare)

If neither planning nor docs found → **bare**:
- Record: `reference_level = "bare"`
- → Go to Step 3P

---

### Step 3F: Feature Mode — Collect Changes and Review

#### 3F.1 Collect Change Scope

**From Commits:**
Extract all commit hashes from `state.json` → `tasks[].commits`:
- Flatten all commit arrays into a single list
- If commits are recorded, use `git diff` between the earliest and latest commits
- If no commits recorded, fall back to scanning files involved in tasks

**From Task Files:**
Read all `tasks/*.md` files and collect their "Files Involved" sections:
- Build a complete list of files created/modified by this feature
- Read current state of each file

**Summary:**
- Total files changed
- Total lines added/removed (from git diff)
- List of all affected files

#### 3F.2 Multi-Dimension Review (via Sub-agent)

**Offload to sub-agent** to handle the full diff analysis.

Spawn a `Task` tool call with:
- `subagent_type`: `"general-purpose"`
- `description`: `"Review feature: {feature_name}"`

**Sub-agent prompt must include:**
- Feature name and `plan.md` file path
- List of all affected files (sub-agent reads them)
- The acceptance criteria from `plan.md`
- Instructions to review across all 4 dimensions below

**Review dimensions:**

**Code Quality:**
- Naming conventions: consistent, descriptive, follows project style
- Code structure: appropriate abstractions, no unnecessary complexity
- DRY: no duplicated logic
- Error handling: appropriate error handling at boundaries
- Comments: only where logic isn't self-evident

**Test Coverage:**
- Every task has corresponding tests
- Tests cover happy path, edge cases, and error cases
- Tests are independent and deterministic
- Test names describe the behavior being tested

**Security:**
- OWASP top 10 check: SQL injection, XSS, CSRF, etc.
- No hardcoded secrets or credentials
- Input validation at system boundaries
- Proper authentication/authorization checks

**Plan Consistency:**
- All acceptance criteria from `plan.md` are met
- Architecture matches the design in `plan.md`
- No unplanned features added (scope creep)
- All planned tasks are implemented

**Sub-agent must return:**

    REVIEW_SUMMARY:
      overall_rating: <pass | pass_with_notes | needs_changes>
      total_issues: <number>

    CODE_QUALITY:
      rating: <good | acceptable | needs_work>
      issues:
      - severity: <critical | warning | suggestion>
        file: path/to/file.ext
        line: <number or range>
        description: <what's wrong>
        suggestion: <how to fix>

    TEST_COVERAGE:
      rating: <good | acceptable | needs_work>
      coverage_gaps:
      - <description of untested scenario>

    SECURITY:
      rating: <pass | warning | critical>
      issues:
      - <description of security concern>

    PLAN_CONSISTENCY:
      criteria_met: <X/Y>
      unmet_criteria:
      - <criterion not met>
      scope_issues:
      - <unplanned additions or missing planned features>

→ Go to Step 4F

---

### Step 3P: Project Mode — Collect Source Code and Review

**The primary subject of review is the source code itself.** Reference documents (plans, specs) serve only as criteria to check against — the sub-agent must deeply read and analyze the actual implementation.

#### 3P.1 Collect Source Code

Identify and collect project source files for deep code review:

1. Use project root markers to find source directories (e.g., `src/`, `lib/`, `app/`, `pkg/`, or language-specific patterns)
2. Exclude non-source directories: `node_modules/`, `dist/`, `build/`, `.git/`, `vendor/`, `__pycache__/`, the output directory itself
3. If on a non-main branch, prefer `git diff main...HEAD` to scope changed files
4. If on main branch, scan all source files

Build file list for the sub-agent. If the project is large (>50 source files), focus on:
- Files changed recently (git log)
- Core modules (entry points, main logic, business logic)
- Test files
- Configuration and infrastructure files

Also collect:
- Package manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, etc.) for dependency review
- Build/CI configuration if present

#### 3P.2 Multi-Dimension Code Review (via Sub-agent)

**Offload to sub-agent** to handle deep source code analysis.

Spawn a `Task` tool call with:
- `subagent_type`: `"general-purpose"`
- `description`: `"Project code review: {project_name}"`

**Sub-agent prompt must include:**
- Project name and root path
- **List of all source files to review — sub-agent MUST read and analyze each file's actual implementation**
- Reference level (`planning` / `docs` / `bare`) and associated criteria (if any)
- If planning-backed: aggregated acceptance criteria (as checklist for consistency dimension only)
- If docs-backed: extracted requirements (as checklist for consistency dimension only)
- Explicit instruction: **"Read every source file. Review the code itself — its logic, structure, correctness, and quality. Reference documents are only used as criteria for the consistency check, not as the subject of review."**

**Review dimensions:**

**Code Quality:** (always applies — **primary dimension**)
- **Logic correctness:** code does what it intends, no obvious bugs or logic errors
- **Naming conventions:** consistent, descriptive, follows project style
- **Code structure:** appropriate abstractions, no unnecessary complexity
- **DRY:** no duplicated logic across modules
- **Error handling:** appropriate error handling at boundaries, no swallowed errors
- **Comments:** only where logic isn't self-evident
- **Module organization:** clear separation of concerns, cohesive modules
- **API design:** public interfaces are clean, consistent, and well-defined
- **Performance:** no obvious performance anti-patterns (N+1 queries, unnecessary allocations, blocking in async code)
- **Dead code:** no unused functions, unreachable branches, or commented-out code

**Test Coverage:** (always applies)
- Source modules have corresponding test files
- Tests cover happy path, edge cases, and error cases
- Tests are independent and deterministic
- Test names describe the behavior being tested
- Test assertions are meaningful (not just "no error")

**Security:** (always applies)
- OWASP top 10 check: SQL injection, XSS, CSRF, etc.
- No hardcoded secrets or credentials
- Input validation at system boundaries
- Proper authentication/authorization checks
- Dependency concerns (known vulnerabilities in package manifest, if present)
- Unsafe operations (file system access, shell execution, deserialization)

**Consistency** (varies by reference level — uses reference docs as **checklist only**):

- **planning-backed** → **Plan Consistency:**
  - Aggregated acceptance criteria from all plans are met in the code
  - Implemented architecture matches the designs in plan files
  - No unplanned features added (scope creep)
  - All planned features have corresponding code

- **docs-backed** → **Documentation Consistency:**
  - Code implements the requirements described in documentation
  - Architecture aligns with tech design (if present)
  - Feature scope in code matches what specs describe
  - No undocumented major functionality in the code

- **bare** → **Skip this dimension.** Note in the report: "No reference documents found — consistency check skipped."

**Sub-agent must return:**

All issues MUST reference specific source files and line numbers/ranges.

    REVIEW_SUMMARY:
      overall_rating: <pass | pass_with_notes | needs_changes>
      total_issues: <number>
      reference_level: <planning | docs | bare>

    CODE_QUALITY:
      rating: <good | acceptable | needs_work>
      issues:
      - severity: <critical | warning | suggestion>
        file: path/to/file.ext
        line: <number or range>
        description: <what's wrong>
        suggestion: <how to fix>

    TEST_COVERAGE:
      rating: <good | acceptable | needs_work>
      coverage_gaps:
      - file: path/to/source.ext
        description: <what scenario is untested>

    SECURITY:
      rating: <pass | warning | critical>
      issues:
      - severity: <critical | warning>
        file: path/to/file.ext
        line: <number or range>
        description: <security concern>

    CONSISTENCY:
      type: <plan_consistency | doc_consistency | skipped>
      rating: <good | acceptable | needs_work | N/A>
      criteria_met: <X/Y> (if applicable)
      unmet_criteria:
      - <criterion not met>
      scope_issues:
      - <unplanned additions or missing documented features>

→ Go to Step 4P

---

### Step 4F: Feature Mode — Display Report

Review results are **displayed in the terminal** by default — no file is written. This reflects that reviews are iterative, intermediate checks rather than permanent artifacts.

Display the following report directly in the terminal using markdown:

```markdown
# Code Review: {feature_name}

**Date:** {ISO date}
**Reviewer:** code-forge
**Overall Rating:** {pass | pass_with_notes | needs_changes}

## Summary

{1-2 paragraph summary of the review findings}

## Code Quality

**Rating:** {rating}

{issues table or "No issues found"}

## Test Coverage

**Rating:** {rating}

{coverage gaps or "All scenarios covered"}

## Security

**Rating:** {rating}

{security issues or "No security concerns"}

## Plan Consistency

**Criteria Met:** {X/Y}

{unmet criteria or "All criteria met"}

## Recommendations

{prioritized list of changes to make}

## Verdict

{final assessment and recommendation: merge, fix then merge, or rework}
```

#### 4F.1 Optional: Save to File (`--save`)

If the user passed `--save` in the arguments, **also** write the report to `{output_dir}/{feature_name}/review.md`. Otherwise, do NOT create the file.

→ Go to Step 5F

---

### Step 4P: Project Mode — Display Report

Display the following report directly in the terminal using markdown:

```markdown
# Project Review: {project_name}

**Date:** {ISO date}
**Reviewer:** code-forge
**Reference:** {planning-backed | docs-backed | bare (no reference documents)}
**Overall Rating:** {pass | pass_with_notes | needs_changes}

## Summary

{1-2 paragraph summary of overall project quality}

## Code Quality

**Rating:** {rating}

{issues table or "No issues found"}

## Test Coverage

**Rating:** {rating}

{coverage gaps or "All scenarios covered"}

## Security

**Rating:** {rating}

{security issues or "No security concerns"}

## {Plan Consistency | Documentation Consistency}

{If planning-backed or docs-backed:}
**Criteria Met:** {X/Y}

{unmet criteria or "All criteria met"}

{If bare:}
*No reference documents found — consistency check skipped.*

## Recommendations

{prioritized list of improvements}

## Verdict

{final assessment and recommendation}
```

#### 4P.1 Optional: Save to File (`--save`)

If the user passed `--save` in the arguments, **also** write the report to `{output_dir}/project-review.md`. Otherwise, do NOT create the file.

→ Go to Step 5P

---

### Step 5F: Feature Mode — Update state.json

1. Read `state.json`
2. Add or update `review` field in metadata:
   ```json
   {
     "review": {
       "date": "ISO timestamp",
       "rating": "pass_with_notes",
       "total_issues": 3
     }
   }
   ```
   - If `--save` was used, also include `"report": "review.md"` in the review object
3. Update `state.json` `updated` timestamp

→ Go to Step 6

---

### Step 5P: Project Mode — No State Update

Project mode does not update any `state.json` — there is no single feature state to track.

→ Go to Step 6

---

### Step 6: Summary and Next Steps

#### 6.1 Feature Mode

Display:

```
Code Review Complete: {feature_name}

Rating: {overall_rating}
Issues: {total_issues} ({critical} critical, {warning} warnings, {suggestion} suggestions)
{If --save was used:}
Report saved: {output_dir}/{feature_name}/review.md

{If needs_changes:}
Recommended actions:
  1. {highest priority fix}
  2. {next priority fix}
  ...
  After fixing: /code-forge:review {feature_name}   Re-run review

{If pass or pass_with_notes:}
Ready for next steps:
  /code-forge:status {feature_name}         View final status
  Create a Pull Request

Tip: use --save to persist the review report to disk
```

#### 6.2 Project Mode

Display:

```
Project Review Complete: {project_name}

Rating: {overall_rating}
Reference: {planning-backed (N plans) | docs-backed (N documents) | bare}
Issues: {total_issues} ({critical} critical, {warning} warnings, {suggestion} suggestions)
{If --save was used:}
Report saved: {output_dir}/project-review.md

{If needs_changes:}
Recommended actions:
  1. {highest priority fix}
  2. {next priority fix}
  ...
  After fixing: /code-forge:review --project   Re-run review

{If pass or pass_with_notes:}
Project quality looks good.

Tip: use --save to persist the review report to disk
```
