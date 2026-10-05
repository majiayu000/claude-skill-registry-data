---
name: review-impl
description: "Review implementation changes for a given task against architectural standards. Use when reviewing a PR, evaluating recently committed code, assessing whether implementation changes are correct and architecturally sound, or when asked to 'review my changes', 'check this implementation', 'review what I built', 'is this PR ready', or 'audit recent commits'. Accepts a task description, task tracker URL, or issue shorthand (owner/repo#123, #123) as input. Produces a structured review with severity-rated findings, code evidence, and a verdict (Block / Request changes / Approve with notes / Approve). Saves the review to .reviews/Review-impl-{slug}.md. Do NOT use for specification review or spec-vs-implementation verification."
metadata:
  author: Serghei Iakovlev
  version: "1.0"
  category: review
---

# Implementation Review

## Task

**What was implemented:** Provided by the user as a task description or task tracker reference.

## Process

### Step 1: Resolve Task Reference

- If the invoker has already quoted the issue title and body in this prompt (typical when an orchestrator fetched the tracker in an earlier phase and passed the context forward), use those values as the canonical task description for all subsequent steps and **do not re-fetch**.
- Otherwise, if the task description above contains a GitHub issue URL (e.g. `https://github.com/owner/repo/issues/123`) or a shorthand reference (e.g. `owner/repo#123` or `#123`), run `gh issue view <url-or-reference> --json title,body` to fetch the issue title and body. Use the fetched title and body as the canonical task description for all subsequent steps.
- Otherwise, if the task description above contains a Jira issue URL (e.g. `https://yourcompany.atlassian.net/browse/PROJ-123`), use appropriate Agent Skills and/or MCP tools to fetch the issue summary and description, and use those as the canonical task description for all subsequent steps.
- If the task description is plain text and no issue context was provided, skip this step.

### Step 2: Understand the Project

Before evaluating any changes, build a mental model of the system:

1. Read project context files: `AGENTS.md`, `README.md`, `CONTRIBUTING.md`, and anything in `docs/`.
2. List the project root and key subdirectories to understand module structure and layering.
3. Read build/dependency manifests to understand the tech stack.
4. Search for code review standards or guidelines the project defines.

### Step 3: Understand the Task

Analyze the task description to determine:

- What problem is being solved or what capability is being added?
- Which architectural layers and modules should be affected?
- What quality attributes matter most for this change (correctness, performance, security, maintainability)?

### Step 4: Discover What Changed

Identify the implementation changes using all available signals:

1. Run `git diff HEAD~1` (and `git log --oneline -5` for context). If the change spans multiple commits, widen the range to capture the full scope.
2. If the diff is inconclusive, search for files recently modified that relate to the task description.
3. Read every changed file completely - not just the diff hunks. You need surrounding context to evaluate whether the change fits.

Build a change inventory:

| File | Change type | Lines changed | Module/Layer |
|---|---|---|---|

### Step 5: Evaluate the Implementation

For each changed file, assess:

1. **Correctness** - Does the code do what the task requires? Are edge cases handled? Are there logic errors?
2. **Architectural fit** - Does the change respect module boundaries, dependency direction, and the project's established patterns? Does it put logic in the right layer?
3. **Regression risk** - Could this change break existing behavior? Are callers of modified interfaces updated? Are assumptions still valid?
4. **Error handling** - Are errors handled consistently with the project's patterns? Are failure modes explicit?
5. **Naming and contracts** - Do new identifiers communicate intent? Are public API contracts clear?
6. **Completeness** - Is anything missing that the task implies? Migrations, config changes, documentation updates, test coverage?
7. **Simplicity** - Is the solution the simplest that works, or is there unnecessary complexity, indirection, or premature abstraction?

### Step 6: Prove a New Regression Test Can Fail

When the change is a bug fix that ships a test, reading the test is not enough. A test can name the defect, assert on a plausible observable, and still pass against the unfixed code, because something else already on that path produces the same observable. Such a test reads exactly like a real one and locks nothing.

Run the control:

1. Copy the change into an isolated scratch directory outside the repository; a throwaway worktree is optional. Keep the control away from the working checkout and other sessions' changes.
2. Revert only the production hunk, leaving the new test in place.
3. Run just the new test.
4. Restore, re-run, and confirm it is green again.

Green at step 3 is a **High** finding: the test does not lock the fix, and removing the fix later turns nothing red. Say so, and say what the assertion would have to move to - usually the observable only the fixed path can produce, rather than an end state the surrounding code reaches on its own.

The mechanics of the control - what counts as a valid break, restoring without disturbing the tree, cleaning up what a red run leaks - belong to `prove-checks`. Follow it rather than improvising.

When the session cannot run commands, do not skip the step silently. Record in the review that the new test was read but never observed red, so the reader knows that half of the evidence is missing.

### Step 7: Produce the Review

## Output Format

```
## Implementation Review: [task description, shortened]

### Change Summary
[2-3 sentences: what changed, across which modules, and the overall approach taken]

### Findings

#### [Finding title]
- **Severity:** Critical | High | Medium | Low
- **File:** `path/to/file` (lines N-M)
- **Issue:** [what is wrong, with code evidence]
- **Recommendation:** [concrete fix - not vague advice]

<repeat for each finding, severity-descending>

### What Works Well
[Brief - 1-3 sentences acknowledging sound decisions. Do not pad.]

### Verdict
- **Risk level:** Critical | High | Moderate | Low
- **Decision:** Block | Request changes | Approve with notes | Approve
- **Key actions:**
  1. …
  2. …
  3. …
```

### Severity Criteria

- **Critical** - Data loss, security vulnerability, correctness bug that affects users. Must fix before merge.
- **High** - Behavioral bug, broken contract, architectural violation that will cause pain. Should fix before merge.
- **Medium** - Maintainability concern, missing edge case in non-critical path, suboptimal but working approach. Fix soon.
- **Low** - Minor naming issue, opportunity for simplification, style inconsistency. Fix if convenient.

### Rules

- Every finding must cite specific code. No finding without a file path and line reference.
- Do not comment on formatting, whitespace, or style unless it signals a real problem.
- Do not suggest refactors beyond the scope of the task. Review what was changed, not what was not.
- If the change is clean and correct, say so briefly. A short review of good code is more valuable than a long review searching for problems that are not there.

## Save the Review

Write the review to `.reviews/Review-impl-{slug}.md`, where `{slug}` is a short kebab-case slug derived from the task description (3-5 words max).

Create the `.reviews/` directory if it does not exist. If the file already exists, append a numeric index: `-2`, `-3`, etc.

After writing, print the path to the created file.
