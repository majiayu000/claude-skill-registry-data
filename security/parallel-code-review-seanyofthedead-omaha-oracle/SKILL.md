---
name: parallel-code-review
description: |
  Parallel 3-reviewer code review orchestration: launch Security, Business-Logic,
  and Architecture reviewers simultaneously, aggregate findings by severity, and
  produce a unified BLOCK/FIX/APPROVE verdict. Use when reviewing PRs with 5+
  files, security-sensitive changes, new features needing broad coverage, or when
  user requests "parallel review", "comprehensive review", or "full review".
  Do NOT use for single-file fixes, documentation-only changes, or when
  systematic-code-review (sequential) is sufficient.
version: 2.0.0
user-invocable: false
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
  - Task
routing:
  triggers:
    - "parallel review"
    - "3-reviewer review"
    - "security review"
  category: code-review
---

# Parallel Code Review Skill

Orchestrate three specialized code reviewers (Security, Business Logic, Architecture) in true parallel using the Fan-Out/Fan-In pattern. Each reviewer runs independently with domain-specific focus, then findings are aggregated by severity into a unified BLOCK/FIX/APPROVE verdict.

---

## Instructions

### Phase 1: IDENTIFY SCOPE

**Goal**: Determine changed files and select appropriate agents before dispatching.

**Step 1: Read repository CLAUDE.md** to load project-specific conventions.

**Step 2: List changed files**

```bash
git diff --name-only HEAD~1
# or for PRs:
gh pr view --json files -q '.files[].path'
```

**Step 3: Select architecture reviewer agent** based on dominant language.

**Gate**: Changed files listed, architecture reviewer agent selected.

### Phase 2: DISPATCH PARALLEL REVIEWERS

**Goal**: Launch all 3 reviewers in a single message for true concurrent execution.

**Critical constraint**: All three Task calls MUST appear in ONE response.

**Reviewer 1 -- Security**: OWASP Top 10, authentication, authorization, input validation, secrets exposure.

**Reviewer 2 -- Business Logic**: Requirements coverage, edge cases, state transitions, data validation, failure modes.

**Reviewer 3 -- Architecture**: Design patterns, naming, structure, performance, maintainability.

**Gate**: All 3 Task calls dispatched in a single message. Proceed only when ALL 3 return results.

### Phase 3: AGGREGATE

**Goal**: Merge all findings into a unified severity-classified report.

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Security vulnerability, data loss risk | BLOCK merge |
| HIGH | Significant bug, logic error | Fix before merge |
| MEDIUM | Code quality issue, potential problem | Should fix |
| LOW | Minor issue, style preference | Nice to have |

Deduplicate overlapping findings. Keep the highest severity.

**Gate**: All findings classified, deduplicated, and summarized.

### Phase 4: VERDICT

| Condition | Verdict |
|-----------|---------|
| Any CRITICAL findings | **BLOCK** |
| HIGH findings, no CRITICAL | **FIX** (fix before merge) |
| Only MEDIUM/LOW findings | **APPROVE** (with suggestions) |

**Gate**: Structured report delivered with verdict. Review is complete.

---

## Error Handling

| Error | Solution |
|-------|----------|
| Reviewer times out | Report partial findings, note blind spots |
| All reviewers fail | Verify file paths, reduce scope, fall back to systematic-code-review |
| Conflicting findings | Keep higher severity, include both perspectives |
