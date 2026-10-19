---
name: rollback
description: Roll an environment back to the previous version after a bad deploy. Use when production or staging is broken after a release, the user says roll back or revert a deploy, or a migration or image is failing in a cluster.
argument-hint: <staging|production>
disable-model-invocation: true
---

# Roll back

Staging runs whatever `image.tag` says in `deploy/environments/staging/stack.yaml` on
`master`; production runs the release in `deploy/environments/production/release.yaml`
(the revision its charts and values are read at, and its images). Argo CD syncs
automatically and self-heals, so a rollback is a commit, never a change made in the
cluster (Argo CD's own rollback is refused while automated sync is on).

## Production

1. Find the promotion commit to undo:
   `git log --oneline -- deploy/environments/production/release.yaml`.
2. Revert it on a branch and open a pull request:
   `git revert <commit>`, then a PR titled `revert(infra): deploy v<version> to production`.
   Revert the commit rather than editing the file: releases and image tags in
   `deploy/environments/` are written only by CI and the promotion script
   (`.claude/rules/infra.md`), and the revert restores exactly what ran before. To go
   back further than one release, promote the older version instead:
   `bun run promote v<older version>`.
3. The pull request changes only `release.yaml`, so CI runs only lint, the charts and the
   scripts' tests (a few minutes), and the images are already built and signed. Merging
   it deploys the previous release, charts and images. Check with the deploy skill's
   commands.

## Staging

Reverting the staging bump doesn't stick: the revert is itself a push to `master`, so
deploy.yml builds that commit and moves staging to it, with the same code. Revert the
change that broke it instead (`git revert <merge commit>` in a PR); its deploy is the
rollback.

## The database

Migrations are never rolled back. Because every migration is expand-then-contract (the
db-change skill), the previous release runs on the new schema. A migration that fails
stops the rollout before any service changes; fix it forward with a new migration.
