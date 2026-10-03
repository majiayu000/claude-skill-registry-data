---
name: debug
description: Investigate a problem, log it to the debug changelog, cross-check past issues, and suggest a non-duplicate fix.
type: debugging
version: v0.3
---

# Debug

Invoke as `$debug`.

Investigate a reported problem, maintain a persistent debug changelog (`docs/debug-changelog.md`), and propose a fix that avoids repeating past solutions.

## Process

1. Parse the error message, stack trace, or bug description.
2. Capture environment context: current branch, recent commits, uncommitted changes.
3. Ensure `docs/debug-changelog.md` exists (create `docs/` directory and file if missing).
4. Read the full debug changelog and search for prior entries matching the current symptom.
5. If a match is found, report what was tried before and whether the recurrence is systemic.
6. Trace the execution path from the symptom to the root cause, reading only files in the chain.
7. Check recent git history for changes that may have introduced the issue.
8. Propose a minimal fix, cross-checking the changelog to avoid repeating a previously failed approach.
9. Apply the fix, write or update tests, and run them to verify.
10. Prepend a structured entry to `docs/debug-changelog.md` with: date, symptom, category, severity, root cause, fix, test results, related entries, and systemic flag.

## Output

- **Problem**: Symptom, new or recurring
- **Root Cause**: file:line, what's wrong, when introduced
- **Fix Applied**: approach, files modified, test results
- **Changelog Updated**: entry added, any cross-references
- **Prevention**: what check would have caught this earlier; systemic follow-up if applicable

## Next-Step Routing

After reporting the debug outcome:

- If the root cause remains unresolved or verification still fails, use **Recommended next command:** `$debug <specific failing symptom>` with the failing command and evidence, or `$investigate <claim>` when the remaining work is broader repo validation.
- If the fix created or modified tracked files, check `.agents/project.json` for `exec-loop`; recommend `$ship` when enabled, or `npx skillpacks install exec-loop` from the project shell when it is not enabled.
- If a systemic follow-up was added to `tasks/todo.md`, check `.agents/project.json` for `exec-loop`; state that the approved task artifact is ready for an execution-loop runner; if runner tooling is missing, recommend installing `exec-loop` with the project package manager.
- If verification passed, no tracked files are dirty, and no systemic follow-up remains, state that no follow-up command is recommended.

## Constraints

- Always read the full debug changelog before proposing a fix.
- Do not refactor unrelated code.
- Never duplicate a previously failed fix without justification.
- If the root cause can't be determined, report what was ruled out.
- Always run tests after applying the fix.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
