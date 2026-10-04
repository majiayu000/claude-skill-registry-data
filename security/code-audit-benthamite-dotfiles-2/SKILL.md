---
name: code-audit
description: Audit code for actual defects, including bugs, application security issues, error handling gaps, and correctness problems. Not for readability, architecture, test coverage, performance-only, or broad environment security reviews.
argument-hint: "[--accept] [dir]"
argument-choices: "--accept"
---

# Code audit

Review the scope named in the user's request or actual invocation arguments for correctness, security, and robustness issues. Use `$ARGUMENTS` only when the active runtime supplies it; do not treat an unsubstituted placeholder as a path. Find defects with a concrete supported failure or threat model, not generic hardening opportunities.

If the user explicitly asks to fix confirmed findings, whether in natural language or with `--accept`, audit first, then fix all confirmed findings whose fix is clear and within the requested scope. Do not broaden into refactors, feature work, or speculative defensive rewrites. If a finding needs product judgment, credentials, or an externally visible action, report it as unresolved instead of guessing. Run the relevant verification for the project and commit only the accepted fixes.

## Workflow

1. **Resolve the scope**: use the explicit files, directories, diff, PR, or issue named in the user's request first, then any actual invocation scope; only when neither names a scope should you default to the current project. Read project instructions and inspect the working tree, including staged changes. Identify the reviewed revision and distinguish new regressions from pre-existing defects for diff/PR reviews. Follow relevant callers outside a named file to confirm behavior without silently broadening the deliverable.
2. **Identify verification**: inspect the project's docs and config for the right checks before changing code. Examples: byte-compile and ERT for Elisp, typecheck/lint/test commands for typed or compiled projects, dependency scanners when the audit includes package risk. Inspect commands and fixtures before running them: an audit does not authorize production probes, credential access, downloads/installs, migrations or externally visible writes merely because they occur in a test script. Use safe isolated reproductions and report inaccessible evidence.
3. **Read real code paths**: inspect the implementation, callers, inputs, and persistence boundaries. Use available subagents or parallel searches for broad codebases, but do not infer findings from filenames alone. Audit-only checks must not rewrite tracked files or update expected snapshots. Re-check the reviewed revision and affected edits before implementing a finding; concurrent changes may invalidate the diagnosis.
4. **Confirm each finding**: trace a concrete failure mode, bad input, race, leak, or attack path through actual callers and guarantees. State prerequisites, expected versus observed behavior, impact and confidence. Distinguish a reproduced failure from a well-supported static finding or an unresolved hypothesis. Verify unfamiliar API contracts and current vulnerability/version claims against authoritative sources; do not infer exploitability from a package name or advisory count alone. Deduplicate symptoms sharing one root cause.
5. **Report or fix**: for an audit-only request, report findings in the format below and offer to fix critical and bug-level issues. When the user asked for fixes in natural language or with `--accept`, apply the confirmed in-scope fixes, verify them, and commit the result.
6. **Verify fixes**: reproduce the supported failing behavior before changing it when safe, then check that exact behavior after the change. Add a focused regression where practical, check analogous paths affected by the same implementation, and run relevant project checks. A compile/lint pass alone is not evidence that the defect is gone. Preserve unrelated edits and staged work; commit each logical fix according to project policy, using only owned changes. Report partial outcomes and unmeasured runtime gaps without calling every finding resolved. Do not push or publish as an implicit audit step.

## What to look for

### Correctness

- **Logic errors**: off-by-one, wrong operator, inverted conditions, short-circuit evaluation that skips side effects
- **Race conditions**: shared mutable state accessed without synchronization, TOCTOU (time-of-check-to-time-of-use) bugs
- **Unhandled edge cases**: empty inputs, None/null where not expected, division by zero, integer overflow, empty collections passed to min/max
- **Silent data loss**: exceptions caught and swallowed, truncation without warning, overwrites without backup
- **Incorrect assumptions**: hardcoded values that could drift from reality, stale caches that are never invalidated, assumptions about file encoding or line endings

### Security

- **Injection**: SQL injection, command injection, XSS, template injection, path traversal
- **Authentication/authorization gaps**: missing auth checks on endpoints, privilege escalation, insecure token handling
- **Secrets exposure**: credentials in code or logs, API keys in client-side bundles, verbose error messages leaking internals
- **Input validation**: missing or insufficient validation at system boundaries (API endpoints, file uploads, URL parameters)
- **Dependency risks**: installed/resolved vulnerable versions with applicable exposure, or dependency drift that demonstrably breaks a supported contract. Lack of an exact pin alone is not a defect; inspect lockfiles and the project's update policy.

### Error handling

- **Lost failures**: catches that incorrectly swallow or misreport an error the caller must handle. A broad catch is valid when its boundary and recovery contract justify it.
- **Missing error paths**: failure, cancellation or timeout cases that violate a supported contract. Missing retries or preflight existence checks are not defects by themselves: blind retries can duplicate effects, and existence checks do not remove filesystem races. Prefer handling the operation's result; reconcile uncertain side effects before a safe idempotent retry.
- **Incorrect error signaling**: callers demonstrably misinterpret a return, exception or status. Different signaling styles alone are a design concern, not a correctness finding.
- **Resource leaks**: files, connections, or browser contexts opened but not reliably closed (missing `finally`, `with`, or `try/catch`)

### Data integrity

- **Non-atomic operations**: multi-step writes that leave corrupt state if interrupted (no transactions, no atomic file writes)
- **Missing validation on imports/loads**: malformed or untrusted data can cross a boundary and violate a required invariant. Account for existing upstream validation and trusted internal contracts before adding duplicate checks.
- **Idempotency violations**: operations that claim to be idempotent but produce different results on re-run
- **Encoding issues**: mixing bytes and strings, assuming UTF-8 without handling BOM or other encodings

## What NOT to flag

- Style, formatting, or naming issues (use `/interpretability-audit` for that)
- Architecture, abstraction, duplication, or refactoring opportunities where behavior is already correct (use `/design-audit` for that)
- Missing features or enhancements
- Performance issues that don't affect correctness (unless they could cause timeouts or OOM)
- Test coverage gaps (mention if a critical path is untested, but don't audit test quality)
- Broad machine, secrets, dependency, or agent-configuration posture issues outside the application code under review
- Code that is correct and handles errors properly — don't suggest defensive code for impossible conditions

## Output format

Use the host/project's required review schema when one exists. Otherwise organize confirmed findings by impact, omitting empty categories:

1. **Critical**: issues that could cause data loss, security breaches, or silent corruption in production
2. **Bugs**: things that are demonstrably wrong or will fail under specific conditions
3. **Fragile**: code that works now but will fail under a concrete supported input, configuration, dependency, or environment transition
4. **Minor**: low-impact confirmed defects, not style or speculative cleanup

For each finding, include:

- File path and line number(s)
- What's wrong (be specific — "this crashes when X is empty", not "error handling could be improved")
- The concrete input, call path, data state, or threat model that makes it fail
- Evidence and confidence; distinguish reproduced behavior from static reasoning
- A concrete fix or approach

Then include:

- **Verification**: checks run, results, and any checks that were relevant but could not be run
- **No findings**: if no confirmed defects were found, say that clearly and describe the reviewed scope and material evidence gaps. This is not a guarantee of defect-free code. Keep unresolved hypotheses separate from confirmed findings.

At the end of an audit-only request, offer to fix the critical and bug-level issues. When the user asked for fixes in natural language or with `--accept`, summarize the fixes, verification, unresolved findings, and commit hash.
