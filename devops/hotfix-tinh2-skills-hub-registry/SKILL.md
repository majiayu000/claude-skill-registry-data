---
name: hotfix
description: Emergency bug fix pipeline — diagnose, fix, test, commit, push, and PR in 2 iterations max. Speed over perfection.
version: "2.1.0"
category: deploy
platforms:
  - CLAUDE_CODE
---

You are in EMERGENCY MODE. Fix the bug and ship. Do NOT ask the user questions. Infer everything from the error, stack trace, and codebase.

Maximum 2 iterations. Do NOT refactor surrounding code. Do NOT improve anything
beyond the bug. Apply the minimal correct fix.

============================================================
TARGET: $ARGUMENTS
============================================================

$ARGUMENTS contains the bug description, error message, stack trace, or area that is broken.

If $ARGUMENTS is empty:
1. Check conversation context for an error message or bug report.
2. Check recent git log for revert commits or fix attempts.
3. Run the project test suite to find failing tests.
4. If nothing is found, report that no bug was identified and suggest running `/qa` to find issues.

============================================================
PHASE 1: BRANCH SAFETY
============================================================

Before making any changes:
1. Check the current branch: `git branch --show-current`
2. If on main, master, or develop: create a hotfix branch first:
   `git checkout -b hotfix/{short-description}`
   Use a slugified version of the bug description (e.g., hotfix/null-pointer-user-login).
3. If already on a feature or hotfix branch: stay on it.

============================================================
PHASE 2: DIAGNOSE AND FIX (Iteration 1)
============================================================

1. DIAGNOSE:
   - Parse the error message, stack trace, or bug description.
   - Search the codebase for the failing code path (grep class names, method names, error strings).
   - Read the relevant files. Trace the execution path.
   - Identify the root cause.

2. FIX:
   - Apply the minimal fix. Change as few lines as possible.
   - Do NOT refactor. Do NOT clean up. Do NOT add comments.
   - If the fix requires a database change, create a migration (follow /db-migrate conventions).

3. TEST:
   Auto-detect the project type and run the appropriate test suite:
   - Scala (build.sbt): `ENVIRONMENT=test sbt "testOnly *AffectedSpec*"`
     If no specific test identified: `ENVIRONMENT=test sbt test`
   - Flutter (pubspec.yaml): `flutter test`
   - Node.js (package.json): `npx vitest run` or `npm test`
   - If tests pass -> go to PHASE 4 (SHIP).
   - If tests fail -> go to PHASE 3.

============================================================
PHASE 3: REFINE (Iteration 2 — only if iteration 1 tests failed)
============================================================

1. Analyze the test failures from iteration 1.
2. Adjust the fix based on what the tests revealed.
3. Re-run the test suite.
4. If still failing -> STOP. Report what you found and what you tried.

============================================================
PHASE 4: SHIP
============================================================

1. Stage ONLY the files you changed (no unrelated files).
2. Commit:
   ```
   fix: {brief description of what was broken and fixed}
   ```
   Do NOT include Co-Authored-By lines.
3. Push immediately.
4. Create PR with `gh pr create`:
   - Title: `fix: {brief description}` (under 70 chars)
   - Body:
     ```
     ## Summary
     - **Bug:** {what was broken}
     - **Cause:** {root cause}
     - **Fix:** {what was changed}

     ## Test Plan
     - [ ] {relevant test verification}
     - [ ] All existing tests pass
     ```
   - Do NOT reference Claude, AI, or include any AI attribution.
   - Extract story number from branch name if present and link Jira.


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After completing deployment/infrastructure changes, validate:

1. Verify all generated files are syntactically valid (YAML, JSON, HCL, Dockerfile).
2. Run validation commands if available (terraform validate, docker build --check, kubectl dry-run).
3. Verify no secrets, credentials, or sensitive values are hardcoded.
4. If validation fails, diagnose and fix the specific syntax or config error.
5. Repeat up to 2 iterations.

IF STILL FAILING after 2 iterations:
- Document what failed and the exact error
- Include partial output if available

============================================================
OUTPUT
============================================================

| Section | Detail |
|---------|--------|
| Bug | {what was broken} |
| Cause | {root cause} |
| Fix | {file:line — what changed} |
| Tests | {pass/fail, count} |
| PR | {URL} |
| Iterations | {1 or 2}/2 |

============================================================
NEXT STEPS
============================================================

After the hotfix is shipped:
- "Run `/qa` to verify the fix in context of the full application."
- "Run `/arch-review` to validate the fix does not introduce architectural issues."
- "Run `/analyze` to check for domain consistency after the change."
- "Run `/manual-test-plan` to generate a targeted QA plan for the affected area."
- "Run `/ship` if additional work is needed beyond the hotfix scope."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /hotfix — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.

============================================================
DO NOT
============================================================

- Do NOT refactor surrounding code — fix only the bug, nothing else.
- Do NOT add features or improvements — this is an emergency fix.
- Do NOT spend more than 2 iterations — if it is not fixed after 2, stop and report.
- Do NOT make sweeping changes — change as few lines as possible.
- Do NOT skip creating the PR — every hotfix must be tracked and reviewable.
