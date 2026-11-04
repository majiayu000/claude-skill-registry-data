---
name: implement-plan
description: "Execute remaining leaves in a .tmp/grunt/plans checklist. Skip [x]."
---
# implement-plan

You execute the plan in this session. Start only on a plan the user approved, when the request said "plan and do it", or when `/implement-roadmap` is running a `locked` or `in-progress` roadmap. Skip `[x]`. Start at the first open leaf. Flip only the box after each leaf. When a phase's children are `[x]`, mark the phase `[x]`. Frontmatter `in-progress` then `done`.

Arg `{n|path}` picks that file. Empty arg: unique in-progress, else unique ready, else list serials.

Format: `.rulesync/reference/plan-format.md`. Write-allowlist = paths listed in the plan. Run Verify leaves. Do not skip a test leaf. Do not flip a behavior leaf `[x]` until its test ran.

A leaf that names a principle skill is done by reading that skill and following it. Also follow the next paragraph, and read a principle an already-read principle cites. Do not open the rest of the catalog.

Before Verify, read `principle-prove-it-works` and follow it. After two fixes that share a premise fail the same gate, read `principle-attack-the-premise` before a third try. Before you ask the user, read `principle-never-block-on-the-human`. Before a large dump or a fan-out, read `principle-guard-the-context-window`. Fat dumps go through `node .rulesync/scripts/grunt-job.mjs`.

On a failing-test leaf, run the test and see it fail for the missing behavior before the production edit. Then make it pass. Then run the nearest suite.

After Verify, if frontmatter `commit:` is set, run `/commit` with that subject and the journal Files. One plan, one commit, including a failing-test leaf and the fix. If a git hook fails on a path inside the plan write-allowlist, fix that code and commit again until the hook passes. Stop when the hook cites a path outside the allowlist or a missing secret. Do not skip the hook. Do not push. A plan with no `commit:` key does not auto-commit.

On start: if this plan has no journal, Write one under `.tmp/grunt/implementations/` (`IMPL_NAME:`, `IMPL_PLAN: {n}`). Format: `.rulesync/reference/implementation-format.md`. After each leaf: append `N.M [x] …` to Log, update Files (repo-relative product paths) and Done. Blocked → `status: blocked` and Blockers. Verify done → `status: done`. Straight shots do not write a journal.
