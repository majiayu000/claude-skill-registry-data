---
name: analyze-pr
description: Analyze branch and generate context-aware quality checklist
user-invocable: false
model: sonnet
allowed-tools: Bash, Read
---

# analyze-pr

Model-invocable skill for analyzing PR readiness with dynamic quality checklists.

## Purpose

Analyze the current branch against base and produce a context-aware quality checklist.

You DO the analysis work. You do NOT make decisions about what to do with the results.

## Input

Receive from agent:
- Base branch (defaults to `main`)
- Optional: specific commit range
- Optional: pr_number (GitHub PR number; when provided, skill uses gh CLI to fetch PR diff and metadata instead of git diff)

## Process

### 0. Determine Analysis Mode

If `pr_number` was provided in the input:
- Mode = **PR-scoped**. Skip Step 1; proceed to Step 0a.

If `pr_number` was not provided:
- Mode = **Branch-diff**. Proceed to Step 1 (unchanged).

### 0a. Read PR State (PR-scoped mode only)

Invoke the `platform-adapter` skill with `verb: diff-pr` and `args: {pr_number: {pr_number}}` to fetch the unified diff.

Invoke the `platform-adapter` skill with `verb: view-pr` and `args: {pr_number: {pr_number}}` to fetch PR metadata (number, title, body, files, commits, baseRefName/target_branch, headRefName/source_branch).

If the adapter returns a non-zero exit code, halt with error: "PR-scoped mode requires a configured platform CLI. Check platform configuration and authentication."

Use the `files` list from the view-pr response as the changed files list (equivalent of `git diff --name-only`). Use the diff from the diff-pr response for content analysis. Use commit messages from the `commits` array for commit type analysis. Access the target branch via `baseRefName` (GitHub) or `target_branch` (GitLab) as appropriate for the active platform.

Proceed to Step 2 with the PR-derived data.

### 1. Read Branch State (branch-diff mode only)

This step is skipped when pr_number is provided — PR-scoped mode uses Step 0a instead.

```bash
git diff --stat main..HEAD
git diff --name-only main..HEAD
git log --oneline main..HEAD
git branch --show-current
```

### 2. Analyze Context

Using the changed files list (from Step 0a in PR-scoped mode, or Step 1 in branch-diff mode), determine which file patterns are affected:
- Code files (`*.ts`, `*.js`, `*.py`, `*.java`, `*.go`)
- API files (`**/api/**`, `**/routes/**`, `**/controllers/**`)
- Security files (`**/auth/**`, `**/security/**`, `*.pem`, `*.key`)
- Database files (`**/migrations/**`, `*.sql`, `**/schema/**`)
- UI components (`**/components/**`, `*.tsx`, `*.vue`)
- Test files (`**/*.test.*`, `**/*.spec.*`, `**/test/**`)
- Documentation (`*.md`, `**/docs/**`)

Determine branch pattern using: `reference/branch-patterns.md`

Determine commit types from commit messages using: `~/.garura/core/memory/standards/rules/commits.md`

### 3. Load Rules

Load quality rules from: `reference/quality-rules.md`
- Contains all quality rules including project-specific disabled rules
- Rules in the "Disabled Rules" section should be skipped

### 4. Evaluate Triggered Rules

For each rule in the loaded ruleset:
1. Check if trigger conditions match the analyzed context
2. If matched, add to the applicable checklist
3. Apply branch-based overrides (hotfix demotes, release promotes)

### 5. Run Automated Verifications

For items with automated verification:
- **No merge conflicts**: Run `git merge-tree --write-tree main HEAD`
- **No secrets committed**: Scan changed files for secret patterns
- **Tests pass**: Check CI status or run test command
- **Build succeeds**: Check CI status or run build command

Mark manual items as `REVIEW` status requiring human sign-off.

### 6. Produce Checklist

Generate the context-specific checklist with:
- Items grouped by priority (must-have vs nice-to-have)
- Each item showing its trigger (why it applies)
- Automated items with evidence
- Blocking issues summary
- Overall readiness assessment

## Output

Produce output using template: `templates/analysis-output.md`

**IMPORTANT**: This skill produces analysis data. The calling agent receives this output and decides what to do next. Do NOT instruct the agent to return or stop.

## Constraints

- NEVER create the PR — only analyze
- NEVER modify any files — read-only analysis
- ALWAYS show trigger reason for each checklist item
- ALWAYS provide evidence for automated checks

## Version

| Field | Value |
|-------|-------|
| Version | 1.0.0 |
| Category | analysis |
