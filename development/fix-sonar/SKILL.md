---
name: fix-sonar
disable-model-invocation: true
# TODO(adapt): add Bash(<runner>:*) entries for the FORMAT_FIX_CMD / LINT_CMD / TYPECHECK_CMD / TEST_CMD executables.
allowed-tools: mcp__sonarqube__search_sonar_issues_in_projects, mcp__sonarqube__change_sonar_issue_status, Bash(git:*), Bash(gh:*), Agent
description: Orchestrate SonarQube issue resolution across the project using parallel agents and specific fix strategies.
---

# SonarQube Issue Fixer

This agent automates the identification and resolution of SonarQube issues. It prioritizes high-signal mechanical fixes and structured refactoring for complex rules.

> **Setup:** this skill talks to a SonarQube MCP server. Set `SONAR_PROJECT_KEY` in `.env`
> (see `.env.example`) to your project's key and enable the server in
> `.claude/settings.local.json`. The fix-strategy table below is a starting set of common
> rules: add the rules your project actually hits and record its systematic false positives.

## Operation Modes

### 1. Status Check (`--status`)

- **Action:** Retrieve all `OPEN` issues for project `${SONAR_PROJECT_KEY}`.
- **Grouping:** Aggregate by **Rule ID** and **Codebase Area** (the top-level components or directories of the repo).
- **Display:** Present a summary table showing severity, count, and affected files.

### 2. Parallel Resolution (`--parallel`)

- **Batching:** Group issues by Rule + Area. Create up to 3 independent batches targeting different files.
- **Isolation:** Dispatch 3 parallel agents with `isolation: "worktree"`.
- **Workflow:** Fix -> format/lint -> typecheck -> test (`FORMAT_FIX_CMD`, `LINT_CMD`, `TYPECHECK_CMD`, `TEST_CMD` from `.claude/project.env`; skip an empty key) -> Commit -> Push -> PR.
- **Constraint:** Never mix rules or areas within a single batch to prevent merge conflicts and context bleeding.

### 3. Targeted Fix (`<rule>` or `<rule> <area>`)

- **Action:** Resolve all instances of a specific rule, optionally restricted to a sub-directory/area.

## Fix Strategy & Batching Reference

| Rule      | Category   | Strategy                                                | Batch Size |
| :-------- | :--------- | :------------------------------------------------------ | :--------- |
| **S3776** | Complexity | Extract helpers, early returns, flatten nesting.        | 1-2 files  |
| **S107**  | Refactor   | Group parameters into a single options object.          | 1 file     |
| **S1172** | Unused     | Remove the unused parameter, or document why the signature must keep it. | 3-5 files |
| **S1481** | Unused     | Remove the unused local variable.                       | 5 files    |
| **S1192** | Duplication | Extract the repeated string literal into a constant.   | 3-5 files  |
<!-- TODO(adapt): add the language-specific rules this project hits, and a `falsepositive` row (mark via `change_sonar_issue_status`, do NOT code-fix) for each systematic false positive. -->

## Agent Dispatch Template

Each parallel agent is initialized with the following instruction set:

> "Fix [COUNT] instances of SonarQube rule [RULE] in [AREA].
> **Context:** Refer to [FILE:LINE] list.
> **Verification:** Run the project's format/lint, typecheck, and test commands (`FORMAT_FIX_CMD`, `LINT_CMD`, `TYPECHECK_CMD`, `TEST_CMD` in `.claude/project.env`).
> **Commit:** `fix: resolve SonarQube [RULE] [DESCRIPTION] in [AREA]`"

## Exclusions & Constraints

- **Auto-generated Files:** Skip paths matching `GENERATED_PATHS_REGEX` in `.claude/project.env`, and any build output directories (`dist/`, `build/`, `target/`).
- **Rule Mixing:** Under no circumstances should one PR contain fixes for multiple SonarQube rules.
