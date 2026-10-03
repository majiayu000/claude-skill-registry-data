---
name: debug
description: Investigate a problem, log it to the debug changelog, cross-check past issues, and suggest a non-duplicate fix
type: debugging
version: v0.3
argument-hint: <error message, bug description, or symptom>
---

# Debug

Investigate a reported problem, maintain a persistent debug changelog (`docs/debug-changelog.md`), and propose a fix that avoids repeating past solutions.

## Process

1. **Parse the input** from `$ARGUMENTS`:
   - Error message or stack trace → extract file paths, line numbers, error types.
   - Bug description → identify expected vs. actual behavior.
   - If no arguments provided, ask the user what to debug.

2. **Capture environment snapshot:**
   - Current git branch, last 5 commits (`git log --oneline -5`), and any uncommitted changes (`git status --short`).
   - Note the date and working directory.
   - Read `CLAUDE.md` for project conventions.

3. **Ensure the debug changelog exists:**
   - If `docs/` does not exist, create it.
   - If `docs/debug-changelog.md` does not exist, create it with this template:

   ```markdown
   # Debug Changelog

   Persistent log of investigated issues, root causes, and applied fixes.

   <!-- Entries are prepended below in reverse-chronological order -->
   ```

4. **Check for prior occurrences:**
   - Read `docs/debug-changelog.md` in full.
   - Search for entries matching the current symptom — look for similar error messages, affected files, root cause areas, or categories.
   - If a match is found:
     - Report what was tried before (the fix, whether it worked, any notes).
     - Flag if the recurrence suggests a **systemic issue** that needs deeper attention beyond a point fix.
   - If no match is found, note this is a new issue.

5. **Investigate the problem:**
   - Follow the execution path from the symptom to the source.
   - Read only the files in the chain — do not explore the full codebase.
   - Check for common causes: null/undefined, wrong types, missing env vars, stale imports, race conditions, schema mismatches, config drift.
   - Check `git log --oneline -20` for recent changes that may have introduced the issue.
   - If relevant tests exist, run them to confirm the current broken state.

6. **Propose a fix:**
   - Write the minimal code change that fixes the root cause.
   - **Cross-check the changelog**: if a similar fix was attempted before and failed or recurred, choose a different approach or escalate to a broader refactor.
   - If tests exist, update them. If not, write a test that would have caught this.
   - Run the relevant tests to confirm the fix works.

7. **Log the entry** by prepending a new entry to `docs/debug-changelog.md` immediately below the header comment:

   ```markdown
   ## [YYYY-MM-DD] Short title of the problem

   - **Symptom**: What was observed
   - **Category**: regression | logic | config | dependency | types | infra | performance
   - **Severity**: critical | high | medium | low
   - **Environment**: branch, relevant commit(s)
   - **Root Cause**: `file:line` — one-sentence explanation
   - **Fix Applied**: What was changed (files, approach)
   - **Tests**: Pass/fail status after fix
   - **Related Entries**: Links to prior changelog entries if applicable, or "None"
   - **Systemic?**: Yes/No — if yes, describe what recurring pattern this reveals
   - **Notes**: Anything else useful for future debugging
   ```

8. **Report to the user** using the output format below.

## Output

### Problem
- **Symptom**: What was reported
- **New or recurring**: First occurrence / Seen before on [date] — [what was tried]

### Investigation
- **Root Cause**: `file:line` — explanation
- **Introduced by**: commit hash or "pre-existing"

### Fix
- **Approach**: What was changed and why this approach (especially if a different approach was tried before)
- **Files modified**: List
- **Test results**: Pass/fail

### Changelog Updated
- Entry added to `docs/debug-changelog.md`
- Related entries: [any cross-references]

## Next-Step Routing

After reporting the debug outcome:

- If the root cause remains unresolved or verification still fails, use **Recommended next command:** `/debug <specific failing symptom>` with the failing command and evidence, or `/investigate <claim>` when the remaining work is broader repo validation.
- If the fix created or modified tracked files, check `.agents/project.json` for `exec-loop`; recommend `/ship` when enabled, or `npx skillpacks install exec-loop` from the project shell when it is not enabled.
- If a systemic follow-up was added to `tasks/todo.md`, check `.agents/project.json` for `exec-loop`; state that the approved task artifact is ready for an execution-loop runner; if runner tooling is missing, recommend installing `exec-loop` with the project package manager.
- If verification passed, no tracked files are dirty, and no systemic follow-up remains, state that no follow-up command is recommended.

### Prevention
- What test, lint rule, or check would have caught this earlier
- If systemic: recommended follow-up action

## Constraints
- Always read the full debug changelog before proposing a fix — never skip the cross-check.
- Do not refactor unrelated code while fixing the bug.
- Do not guess — if you can't trace the root cause, say so and list what you've ruled out.
- Always run tests after applying the fix.
- Never duplicate a previously failed fix without a clear reason why it will work this time.
- If the fix requires changes outside the current project (infra, env vars, external service), document what's needed in the changelog entry instead of attempting it.
- Keep changelog entries concise but complete — they are the institutional memory for debugging.


## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.
