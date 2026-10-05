---
name: code-review
description: Reviews pull request diffs for correctness, security, maintainability, and test coverage. Use when the user asks for a code review of a change set, patch, or PR description.
---

# Code Review

## Instructions

When reviewing a diff/PR, follow this flow:

1. **Clarify context (if missing)**
   - Ask for the repo name, language/framework, and what “done” means (e.g., “ready to merge” vs “early review”).
   - If the user did not provide a diff, ask them to paste the relevant patch or describe the files/behavior changed.

2. **Summarize the change**
   - Provide a 2–5 sentence summary of what changed and the most important impact.

3. **Identify issues with severity**
   - Report issues in this order: **Critical**, **Suggestion**, **Nice-to-have**.
   - For each issue, include: `severity`, `area` (correctness/security/performance/maintainability/tests/style), `location` (file path and the changed symbol/section when possible), and `why it matters`.
   - Prefer specific, actionable fixes over general guidance.

4. **Security review**
   - Check for common risks relevant to the language/framework: injection (SQL/NoSQL/command), XSS/CSRF, authz/authn mistakes, unsafe deserialization, SSRF, secrets in logs, and overly-permissive CORS.
   - If user input handling exists, validate, sanitize/escape appropriately, and enforce allow-lists where possible.

5. **Correctness & robustness**
   - Look for broken invariants, edge cases, race conditions, timezone/locale bugs, error handling, and inconsistent data types.
   - Verify new/modified code paths are exercised by the change.

6. **Maintainability**
   - Check naming, complexity, duplication, API boundaries, and whether abstractions match existing patterns.
   - Flag “spaghetti logic” or overly broad functions/modules.

7. **Tests & quality gate**
   - Identify missing/weak tests that would have caught the issues you found.
   - If the repo has test tooling detectable from the diff (e.g., `jest`, `vitest`, `pytest`, `go test`, `npm test`), suggest the most likely command(s) to run.
   - If you cannot infer a command reliably, list what to test instead (unit/integration/E2E) without guessing exact commands.

8. **Close-out recommendation**
   - End with a short decision suggestion: “Approve”, “Request changes”, or “Needs follow-up” based on Critical items.

## Output Template

Use this structure by default:

```text
Summary
- ...

Critical
- [file/path] <what> — <why> — Fix: <specific change>

Suggestion
- [file/path] <what> — <why> — Fix: <specific change>

Nice-to-have
- [file/path] <what> — <why> — Improvement: <specific change>

Test plan (what to run / what to add)
- ...

Recommendation
- Approve / Request changes / Needs follow-up
```

## Standards

- If the repo contains a style guide or security guidelines (commonly `docs/STYLE.md`, `STYLE_GUIDE.md`, `SECURITY.md`, or `CONTRIBUTING.md`), align findings and fix suggestions to those documents.

