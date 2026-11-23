---
name: conflict-resolve
description: Resolve Git conflicts raised by merging the latest base branch by analyzing the intent of both the ours and theirs changes and combining them, then commit and push. Use when a conflict needs resolving.
argument-hint: "Base branch (defaults to the latest origin/main HEAD)"
---

<!-- markdownlint-disable MD029 -->

# Git conflict resolution (coexisting intents)

Resolve the conflicts raised by merging the latest base branch without breaking the intent of either branch's changes.

## Completion criteria

- [ ] `git diff --name-only --diff-filter=U` returns 0 files
- [ ] For each conflicted file, you can explain why both branches' intents are preserved
- [ ] Commit and push are done

## Phase 0: Preconditions

1. Update the remote:

```bash
git fetch origin
```

2. Determine the base branch (argument given: that value; none: `origin/main`).
3. Check for conflicts:

```bash
git status --short
git diff --name-only --diff-filter=U
```

4. If there are 0 conflicts, stop and report `No conflicts`.

## Phase 1: Thorough analysis of change intent

1. List the conflicted files:

```bash
git diff --name-only --diff-filter=U
```

2. For each file, inspect the 3-way contents:

- `git show :1:<file>` (base)
- `git show :2:<file>` (ours)
- `git show :3:<file>` (theirs)

3. Inspect the related history and diff:

- `git log --oneline --decorate -- <file>`
- `git diff -- <file>`

4. Fill in the "Intent analysis matrix" in [reference.md](reference.md) for each file.
5. Decide the integration approach that lets both intents coexist first, rather than "which side to adopt".

## Phase 2: Implement the resolution

1. Following the integration approach, remove the conflict markers and merge the implementation.
2. Adopting `ours` or `theirs` wholesale is prohibited in principle. When an exception is made, record the reason in the work report.
3. Confirm that no conflict markers remain:

```bash
rg -n "<<<<<<<|=======|>>>>>>>"
```

4. Stage the resolved files:

```bash
git add <resolved-files>
```

## Phase 3: Verification

1. Run the project's lint, format, type check and tests, and confirm the resolution has not broken existing behavior.
2. If anything fails, fix it and stage again.

## Phase 4: Commit and push

Follow the commit message convention in [reference.md](reference.md).

```bash
git commit -m "merge: resolve conflicts with <base-branch>"
git push
```

## Prohibited

- Disabling CI workflow definitions, or editing them to skip checks
- Hand-editing generated files (rerun the code generation tool instead)
- Working around failures with test `skip` / `todo` / deletion
- Working around failures by disabling type safety (`@ts-ignore`, `@ts-expect-error`, `any`, lint-disable, etc.)

## Stop conditions

- The same error repeats (3 or more times)
- The problem cannot be reproduced because it depends on the environment, or progress is blocked by the network
- The intents of the two branches cannot coexist
- The impact is too large to judge safely

When stopping, report the situation, what was tried and what needs a decision, using the work report template in [reference.md](reference.md).
