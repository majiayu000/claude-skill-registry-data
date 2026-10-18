---
name: publish-skills-baseline
description: Publishes local skill-library changes through the public skills repo, syncs them into the Devpunks CLI repo, and publishes the CLI scaffold baseline. Use when asked to commit/push skill changes, sync skills into wearedevpunks-cli, or release a new scaffold baseline.
---

# Publish Skills Baseline

## Scope

Local operator skill only. Keep it under `.agents/skills/`; do not copy it into the public `skills/` tree or CLI scaffold baseline.

## Workflow

1. In `/Users/stefan/Desktop/repos/wearedevpunks-skills`:
   - run `git status --short`
   - run `git diff --check`
   - stage the intended changes
   - commit with a concise message
   - push `main`

2. In `/Users/stefan/Desktop/repos/wearedevpunks-cli`:
   - confirm the worktree is clean before sync
   - run `bun run sync:skills`
   - inspect `git status --short` and `git diff --stat`
   - run `git diff --check`
   - stage the synced `skills/` changes
   - commit with a concise sync message
   - push `main`

3. Publish the baseline from `/Users/stefan/Desktop/repos/wearedevpunks-cli`:
   - ensure `git status --short` is clean
   - run `bun run baseline:publish`
   - verify the printed GitHub release URL with `gh release view <tag> --json tagName,url,isDraft,isPrerelease`

## Notes

- Use `bun run baseline:publish`; `bun release:baseline` is not a package script.
- Baseline release tags live under `baseline/stable/*`; do not use npm `v*` release tags.
- If any worktree is dirty with unrelated changes, stop and report the dirty paths before publishing.
