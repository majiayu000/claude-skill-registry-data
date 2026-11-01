---
name: gh-issue
description: Fetch a GitHub issue, create a branch, plan and implement with TDD, then open a PR
user-invocable: true
argument-hint: "<issue-number>"
allowed-tools: Bash, Read, Edit, Write, Grep, Glob, Agent, WebFetch
---

# GitHub Issue Workflow

Fetch a GitHub issue, create a branch, implement following TDD, and open
a PR.

## Arguments
- `$ARGUMENTS` - Issue number (e.g., `42` or `#42`)

## Instructions

### Phase 1: Setup

1. **Parse the issue number** from `$ARGUMENTS` (strip `#` if present).

2. **Fetch issue details**:
    ```bash
    gh issue view <number> --json title,body,labels,assignees,milestone,state
    ```

3. **Assign yourself if unassigned**:
    ```bash
    gh issue edit <number> --add-assignee @me
    ```

4. **Create a branch** from `main`:

    Determine prefix from labels:
    - `bug` → `fix/`
    - `enhancement` → `feat/`
    - `documentation` → `docs/`
    - Default → `feat/`

    Branch name: `<prefix><issue-number>-<slug>` (slug: lowercase title,
    spaces → `-`, max 50 chars).

    ```bash
    git checkout main && git pull
    git checkout -b <branch-name>
    ```

### Phase 2: Plan

5. **Analyze the issue**: requirements, labels, referenced issues,
    affected areas (which `bashdep::` function or doc).

6. **Explore the codebase** for context:
    - Find the relevant section in `bashdep` (single file)
    - Find the closest related tests in `tests/unit/bashdep_test.sh`
    - Read the corresponding entry in `docs/api.md` or `docs/behavior.md`

7. **Create implementation plan**:
    - Acceptance Criteria
    - Test Strategy (which tests to write first - pure-logic vs
      filesystem vs snapshot)
    - Files to Change (`bashdep`, `tests/unit/bashdep_test.sh`,
      `docs/*.md`, `CHANGELOG.md`)
    - Implementation Order (smallest first step)

8. **Use EnterPlanMode** if implementation is non-trivial.

### Phase 3: Implement

9. **Follow strict TDD workflow** (see `.claude/rules/tdd-workflow.md`):

    For each test:
    - **RED** - Write failing test, verify it fails for the RIGHT reason
    - **GREEN** - Minimal code in `bashdep` to pass
    - **REFACTOR** - Improve while keeping tests green

10. **Run the suite frequently**:
    ```bash
    make test
    ```

11. **Quality checks** after each refactor:
    ```bash
    make sa && make lint
    ```

12. **Mode coverage** - if the change is mutating, add tests for
    `BASHDEP_DRY_RUN`, `BASHDEP_SILENT`, `BASHDEP_VERBOSE`,
    `BASHDEP_FORCE` as relevant.

### Phase 4: Ship

13. **Final verification**:
    ```bash
    make pre_commit/run
    ```

14. **Commit** using the `/commit` skill, with a body referencing the
    issue (e.g., `Closes #<issue-number>`).

15. **Create PR** using the `/pr` skill:
    ```
    /pr #<issue-number>
    ```

## Output Format

After fetching, present:

```
## Issue #<number>: <title>

**Labels:** <labels>
**State:** <state>
**Branch:** <branch-name>

### Description
<body content>

### Next Steps
1. Explore `bashdep` for the relevant function
2. Create implementation plan
3. Begin TDD cycle
```
