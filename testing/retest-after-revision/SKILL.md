---
name: retest-after-revision
category: qa
description: Use when the task came back to QA after need_revision - what to re-run, what may carry over, and how to keep old passes from approving new code
source: obra/superpowers (MIT), adapted
---
# Retest After Revision

A resubmitted task carries history: earlier `passed` test cases (matched by title) and criterion approvals marked `approved (as of SHA, changed since: files)`. Neither is free evidence for this round — a stale pass is exactly what lets a fixed bug reappear unnoticed, or a different bug ship under an old verdict.

## Procedure

1. `list_test_cases` and the criteria lines — read every "changed since" note; it names the files touched since the last approval.
2. `get_task_pull_request` for the changed-file list (this is the named re-test-scope exception, not a code-reading shortcut for the verdict).
3. **Re-run first** every case that failed last round, using its original reproduction. Bug fixed → prove it by testing the original symptom, not a nearby path.
4. **Re-run** every case linked to a criterion whose changed-files list touches shared surface: styles/tokens/theme, layout/router, API client, auth/session, migrations/schema, env/config, package manifests/lockfile, i18n catalogues. This is what "plausibly affects" means in practice — a concrete file-category list, not a feeling.
5. Run the regression smoke set (regression-checklist).
6. Re-send every re-run case with its new result and evidence, prefixed by the new short SHA. A case you deliberately did not re-run keeps its old result only if its criterion line already says "nothing changed since", or its own notes record why the diff cannot reach it — say which, don't just skip silently.
7. New behaviour the fix introduced gets new cases, same as any other round.

## Red Flags

- Approving a criterion whose line says "changed since" without a fresh run this round.
- Re-running only the case that failed last time when the fix touched a shared file (styles, auth, migrations, …) that many other cases depend on.
- Trusting the developer's "fixed it" without re-running the original failing reproduction.
