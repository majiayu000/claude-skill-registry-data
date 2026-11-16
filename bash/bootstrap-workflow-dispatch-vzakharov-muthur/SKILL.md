---
description: Temporarily bootstrap a newly renamed or newly added `workflow_dispatch` workflow so GitHub can dispatch it before the workflow exists on the default branch. Use when `gh workflow run <file>.yml` returns `workflow ... not found on the default branch` for a feature branch, especially right after renaming or introducing a dispatch-only workflow.
---

GitHub does not reliably expose a brand-new `workflow_dispatch` workflow to
`gh workflow run` until that workflow has been seen by Actions metadata at least
once. Before merge, the default branch still points at the old workflow set, so
a feature branch can hit:

```text
HTTP 404: workflow <file>.yml not found on the default branch
```

The workaround is a **one-shot branch-scoped push trigger** that causes exactly
one non-dispatch run on the feature branch, registering the workflow so later
`workflow_dispatch` calls succeed.

## Step 0 — confirm the failure mode

Verify the workflow is blocked for the expected reason:

```bash
gh workflow run <workflow-file>.yml --ref "$(git branch --show-current)"
```

If the error is `workflow ... not found on the default branch`, continue. If the
failure is about bad inputs, missing permissions, or YAML syntax, fix that
instead — this skill is only for the metadata-registration problem.

## Step 1 — add the one-shot push trigger

Edit the workflow file and add a temporary `push` trigger next to
`workflow_dispatch`, scoped to:

- the **current feature branch name**, and
- the workflow file's own path

Pattern:

```yaml
on:
  workflow_dispatch: ...
  # One-shot bootstrap: GitHub only resolves `workflow_dispatch` for workflows
  # already registered in its Actions metadata, which happens on the first
  # non-dispatch run. Scoping this push trigger to the bootstrap branch plus this
  # file's path lets a single push register the workflow, then a follow-up commit
  # can remove the block before merge.
  push:
    branches: [your/current-branch]
    paths: ['.github/workflows/your-workflow.yml']
```

The branch scoping is critical: this must not become a general-purpose push
trigger.

## Step 2 — commit and push the bootstrap commit

Commit only the temporary trigger and push it:

```bash
git add .github/workflows/<workflow-file>.yml
git commit -m "ci: bootstrap workflow_dispatch registration for <workflow-name>"
git push -u origin "$(git branch --show-current)"
```

That push should fire exactly one non-dispatch run for the workflow and register
it in GitHub Actions metadata for the branch.

## Step 3 — retry the real dispatch

Re-run the intended `gh workflow run ...` command (or the wrapper script that
uses it). If the workflow now dispatches, the bootstrap succeeded.

## Step 4 — remove the temporary push trigger

Immediately delete the one-shot `push` block and commit the cleanup:

```bash
git add .github/workflows/<workflow-file>.yml
git commit -m "ci: drop one-shot push trigger after workflow registration"
git push -u origin "$(git branch --show-current)"
```

Do not leave the bootstrap trigger in the final PR diff unless a human
explicitly asks for it.

## Notes

- The bootstrap run is a normal Actions run, not a dispatch run.
- If you renamed the workflow file, the old filename may still 404 on the
  default branch too; that does **not** mean the trick failed.

## Related

This skill ends the moment `gh workflow run` stops 404ing — registering the
workflow is all it does.

`@.claude/skills/test-on-gh/SKILL.md` (once hydrated) is the usual source of the
blocked dispatch: a freshly written dispatch-only workflow is exactly what
Actions has not seen yet. `@.claude/skills/watch-ci/SKILL.md` takes the other
side, watching the run a _successful_ dispatch produces.
