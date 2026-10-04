---
name: preflight-pr-release-flow
description: Use when working in /Users/axel/code/Preflight and the user wants a branch published, PR metadata updated, a draft moved to ready, merged, branch cleanup, or post-merge GitHub Actions proof.
---

# Preflight PR Release Flow

## Use For

- Publishing a local branch to `UlaYuga/promo-preflight`.
- Creating or updating a draft PR.
- Metadata-only PR body/title/state work.
- Marking a PR ready, merging it, deleting a branch, or returning exact SHA/CI proof.

Do not use for implementing product changes, copy rewrites, UI work, or app debugging before the branch content is already correct.

## Start State

Run from `/Users/axel/code/Preflight`:

```bash
git branch --show-current
git remote -v
git status --short
```

For publish or merge work, verify GitHub auth early:

```bash
gh auth status
```

## Verification Gate

If code changed and the user did not narrow the gate, default to:

```bash
npm run test
npm run i18n:check
npm run typecheck
npm run lint
npm run build
git diff --check
```

After `npm run build`, check `git status --short`. If build-only generated churn touches `next-env.d.ts`, restore it unless the task intentionally changed generated route types.

## PR Operations

- Prefer authenticated `gh` for create/edit/ready/merge when connector writes fail or look under-permissioned.
- For metadata-only updates, read the current PR first:

```bash
gh pr view <pr> --json number,title,body,isDraft,state,url,headRefOid,statusCheckRollup
```

- Edit with `gh pr edit <pr> --body-file <file>` or `--body <text>`, then re-read the PR and confirm the state/body actually changed.

## Merge Safety

Before merge, capture `headRefOid`, current checks, `mergeable`, and `mergeStateStatus`. For guarded merges use:

```bash
gh pr merge <pr> --merge --match-head-commit <head_sha>
```

After merge:

```bash
git fetch origin main
git merge-base --is-ancestor <head_sha> origin/main
```

If CI proof was requested, identify the `main` workflow run for the merge SHA and wait for it:

```bash
gh run watch <run_id> --repo UlaYuga/promo-preflight --exit-status
```

Return exact PR URL, final SHA, and CI run URL. Do not report “done” without those artifacts when proof was requested.

## Pitfalls

- `403 Resource not accessible by integration` or `422 must be a collaborator`: switch to `gh`.
- Metadata-only means no tests/build and no working-tree edits.
- Do not stage unrelated dirty files; this repo often has user or prior-agent changes in flight.
