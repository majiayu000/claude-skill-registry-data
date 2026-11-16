---
name: kit-code-review
description: Review code changes for correctness, security, and maintainability defects and report evidence-based findings with severity and file locations. Use when asked to review a diff, branch, pull or merge request, commit, or specific files. Do not use for writing new features, fixing bugs, or general questions about code; this skill reports findings and does not edit code.
---

# Code review

Review the requested changes and report defects with evidence. Do not modify files unless the user explicitly asks for fixes after the review.

## 1. Establish scope

- Identify what to review: the user's named files, commit, branch, or request; otherwise the uncommitted changes (`git diff` and `git diff --staged`), or the current branch against its base.
- If the scope is unclear or empty, say so and ask rather than reviewing unrelated code.
- Read project instructions and any project context document for conventions and commands.

## 2. Understand the change

- Read every changed hunk and enough surrounding code to understand it: callers, callees, types, schemas, and tests.
- Determine the intent from the description, commit messages, or code. Review against that intent.

## 3. Look for defects

Check, in priority order:

1. **Correctness**: logic errors, wrong conditions, off-by-one, null or undefined handling, error paths, concurrency and ordering, resource cleanup, behavior on empty or large inputs.
2. **Security**: injection (SQL, shell, path, template), missing authorization or validation at trust boundaries, secrets in code or logs, unsafe deserialization, data exposure.
3. **Data integrity**: migrations, transactions, partial failure, backward compatibility of stored data and APIs.
4. **Tests**: changed behavior without tests, tests that cannot fail, removed or weakened assertions.
5. **Maintainability**: duplication of existing utilities, violations of established project conventions, misleading names or comments. Report these only when they matter; do not nitpick formatting that tooling handles.

Verify each suspected defect before reporting it: trace the code path, check the types, or run a focused test or command when it is safe and cheap. Discard findings you cannot support.

## 4. Report

Order findings by severity:

- **Critical**: security vulnerability, data loss, or a crash in a common path.
- **High**: incorrect behavior users will hit.
- **Medium**: incorrect behavior in edge cases, or missing tests for risky changes.
- **Low**: maintainability issues worth fixing.

For each finding give the severity, `file:line`, the problem, the concrete scenario that triggers it, and a suggested fix. Then list open questions, and finally anything you could not verify. If there are no findings, say so plainly and state what you checked.

## Examples

- Use: "Review my changes before I open a PR." "Can you check src/auth/session.ts for bugs?"
- Skip: "Add pagination to the users endpoint." (feature work) "Why is this test failing?" (debugging)
