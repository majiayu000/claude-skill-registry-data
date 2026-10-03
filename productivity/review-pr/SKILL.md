---
name: review-pr
description: Review a branch, diff, commit range, or pull request with a findings-first code review workflow. Use when the task is to identify bugs, regressions, risks, or missing tests in proposed code changes.
allowed-tools: [Read, Grep, Glob, Bash, git]
---

# Review Pull Request

Use this skill for review-style analysis of code changes.

---

## Rules

- Determine the exact review surface before drawing conclusions
- Prefer `rg` / `rg --files` for search
- Prioritise bugs, regressions, and risk over style commentary
- Verify each finding against real code paths, tests, types, or call sites
- Lead with findings, ordered by severity
- If no issues are found, say that explicitly and note residual risks or testing gaps

---

## Step 1 — Determine Review Surface

Inspect the available change surface first:

```bash
git status --short
```

```bash
git diff --stat
```

```bash
git diff -- <path>
```

If the user names a branch, commit range, or PR patch, review that exact surface instead of the whole repository.

---

## Step 2 — Review With Findings First

Prioritise:

- Functional bugs
- Behavioral regressions
- Missing error handling
- Incorrect assumptions about data flow, state, permissions, or concurrency
- Missing or weak test coverage for risky logic

Avoid leading with praise or a broad summary.

---

## Step 3 — Verify Claims Against Code

For each finding:

- Point to the relevant file and line
- Explain the failure mode
- Explain when it will happen
- Distinguish confirmed bugs from lower-confidence concerns

Prefer evidence from code paths, tests, types, and usage sites over style opinions.

---

## Output

Use this structure:

```markdown
Findings
1. [severity] `path/to/file:line` — concise statement of the issue and why it matters

Open Questions
- Any ambiguity that blocks a stronger conclusion

Change Summary
- Brief overview only after findings
```

If there are no findings, state that explicitly before noting remaining risk areas.

---

## Done Criteria

The review is complete only when:

- The intended diff or branch was inspected
- Findings were checked against the code
- The response is findings-first
- Residual risk or testing gaps are called out when relevant
