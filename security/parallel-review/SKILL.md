---
name: parallel-review
description: "Run code-review, security-audit, and documentation review in parallel using agents. Use when reviewing completed work, pre-merge checks, or when user mentions 'parallel review', 'full review', 'review everything', or 'comprehensive review'."
allowed-tools: Read, Glob, Grep, Bash, Agent, Write, Edit
---

# Parallel Review

Run three independent review agents simultaneously, then synthesize a unified report. This implements the **parallel workflow pattern** — each agent specializes in one review domain, and their findings are merged into a severity-ranked report.

## Setup

Before starting: identify the project context, read `status.yaml`, run `git status` and `git diff --stat` to understand what changed.

## Process

### Step 1: Identify Scope

Determine the review target:
- If recent changes: `git diff --name-only` or `git diff HEAD~1 --name-only`
- If specific files: use the file list provided by the user
- If full project: scan `src/` or equivalent source directory

Capture the file list and diff summary — you'll pass this to all three agents.

### Step 2: Launch Three Review Agents in Parallel

Spawn exactly **3 Agent calls in a single message** (parallel execution). Each agent gets the same file list but different review focus.

**Agent 1 — Code Quality Review:**
```
Review these files for code quality:
{file list and diff}

Check for:
- Functions longer than 30 lines
- Duplicated logic (more than 2 occurrences)
- TypeScript `any` types
- Missing error handling on async operations
- N+1 query patterns or SELECT *
- Naming convention violations
- Single responsibility violations
- Dead code or unused imports

For each finding, report: severity (critical/warning/suggestion), file:line, description, and recommended fix.
```

**Agent 2 — Security Audit:**
```
Review these files for security vulnerabilities:
{file list and diff}

Check OWASP Top 10:
- Hardcoded secrets or credentials
- SQL injection (raw queries, string interpolation in SQL)
- XSS (innerHTML, v-html, dangerouslySetInnerHTML)
- Command injection (exec, system, shell_exec)
- Broken access control (missing auth checks)
- Insecure dependencies (check package.json/composer.json)
- SSRF risks (unvalidated URLs)
- Missing input validation at system boundaries

For each finding, report: severity (critical/high/medium/low), file:line, OWASP category, description, and fix.
```

**Agent 3 — Documentation & Structure Review:**
```
Review these files for documentation and structure:
{file list and diff}

Check for:
- Missing or outdated comments on complex logic
- Public API methods without documentation
- README accuracy (does it reflect current state?)
- Test coverage gaps (new code without corresponding tests)
- Configuration files that need updating
- Migration files that may need review
- Breaking changes that need changelog entries

For each finding, report: severity (warning/suggestion), file:line, description, and recommended action.
```

### Step 3: Synthesize Results

After all three agents complete, merge their findings into a single report:

1. **Deduplicate** — if multiple agents flag the same file:line, merge into one finding with the highest severity
2. **Rank by severity** — Critical > High > Warning > Suggestion
3. **Group by file** — so the developer can address findings file-by-file
4. **Count totals** — summary table of findings per category

### Step 4: Generate Report

Use this format:

```markdown
# Parallel Review Report

**Date:** {YYYY-MM-DD}
**Project:** {project-name}
**Files Reviewed:** {count}
**Review Agents:** Code Quality, Security, Documentation

## Summary

| Category | Critical | High | Warning | Suggestion |
|----------|----------|------|---------|------------|
| Code Quality | X | X | X | X |
| Security | X | X | X | X |
| Documentation | X | X | X | X |
| **Total** | **X** | **X** | **X** | **X** |

**Verdict:** APPROVED / CHANGES_REQUESTED / BLOCKED

## Critical & High Findings

### {file_path}

1. **[CRITICAL/HIGH]** {description}
   - Category: {Code Quality/Security/Documentation}
   - Line: {line_number}
   - Fix: {recommended fix}

## Warnings

{Grouped by file, same format}

## Suggestions

{Grouped by file, same format}

## Recommendations

1. {Prioritized action items}
```

Save the report to: `contexts/{context}/projects/{project}/reviews/parallel-review-{date}.md`

If no project directory exists, output the report directly to the user.

## Self-Assessment (Internal)
Rate this skill execution 0-10. If < 8, write feedback to `.handoff/feedback/{date}-{skill-name}.yaml` with: skill, rating, friction, suggestion, context. Do not mention to user.
