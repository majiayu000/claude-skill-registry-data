---
name: mutation-check
description: "Verify that a regression test detects a meaningful behavior change using a disposable checkout, green baseline and confirmed restoration."
---
# Prove that the test can fail

Use an isolated disposable checkout of the candidate. Never mutate the user's active worktree or live services. No automatic mutation helper is bundled.

1. Record candidate revision, clean status, target behavior, exact test command and expected failure assertion. Require a successful baseline with nonzero test discovery.
2. Change one behavioral condition: a comparison, permission check, ordering, boundary or required operation. Avoid editing log text or comments merely to trip text assertions.
3. Verify the mutation actually applied and remains syntactically valid. Run the same tests with the same configuration. Preserve output and the diff.
4. Classify **DETECTED** only when the intended tests execute and fail for the intended behavioral reason. Collection, import, infrastructure, timeout and no-test failures are **INCONCLUSIVE**, regardless of exit code.
5. If tests remain green, report **SURVIVED**. Investigate whether redundant controls mask the mutation; use a second targeted probe if justified. Do not assume survival is always a defect.
6. Restore only the owned mutation, compare with the original bytes and rerun affected tests. Preserve the disposable checkout on restoration failure; do not report clean recovery.

Keep counts of attempted, detected, survived and inconclusive mutations with their reasons. Use an existing mutation-testing framework when appropriate, but verify its discovery and failure classification. Tests that only find strings in source can pass with commented-out code; prefer behavior assertions.
