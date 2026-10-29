---
name: stack-upgrade
description: Use when a Renovate pull request bumps @moifort/stack in a project, to sync the rules and apply the version's migrations.
---

# Upgrade the stack in a project

1. Confirm the pull request bumps `@moifort/stack`. Otherwise this skill does not apply.
2. In the pull request's branch: `bun install`, `bunx stack sync`, commit
   `chore(stack): sync to <version>`.
3. Read the **Upgrade** part of every `CHANGELOG.md` section between the two versions
   (`node_modules/@moifort/stack/CHANGELOG.md`), then `bunx stack migrations <old> <new> --json`: the migrations between the two versions, for
   this project's stacks, in order.
4. For each migration, in order:
   - read the rule it points to and its body (what changes, how to find it, how to fix it,
     when it does not apply);
   - find the affected code, fix it, run its `check` command until it exits 0;
   - commit `refactor(<scope>): <migration id>`;
   - when it does not apply, note why and commit nothing.
5. `bun run preflight` (and `bun run ios:build` with the ios stack). A failure caused by a
   migration: revert that migration's commit and mark it `needs review`.
6. If the version changed a routine (`stack/routines/`), update the scheduled task.
7. Comment on the pull request: one line per migration, its outcome (applied, not applicable,
   needs review) and the files touched.
8. Merge only when every migration is `safe`, each applied or not applicable, every `check`
   passes and CI is green. Otherwise label `stack:review` and leave it open.

Never edit `stack/` by hand, never edit a rule from a project: a wrong rule is reported.
