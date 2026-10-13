---
name: release
description: Cut a release and put it in production. Use when the user asks to release, tag a version, write the changelog, promote to production, or what's in the next version.
argument-hint: <version>
disable-model-invocation: true
---

# Release to production

Releases are version tags the user pushes; production moves through a promotion pull
request (docs/deploy.md, "Releases → production"; the code is `scripts/release.ts`).

1. **What's in it.** `bun scripts/release.ts notes HEAD` prints the notes since the last
   tag, grouped from the Conventional Commit titles. Pick the version from them: any
   breaking change (`!`, or a `BREAKING CHANGE:` footer) is a new major, a `feat` a
   minor, otherwise a patch. `git describe --tags --abbrev=0` is the last one.
2. **The mobile version.** `version` in `apps/mobile/app.config.ts` must equal it (store
   builds carry it, and over-the-air updates only reach builds of their version). Bump
   it in a pull request and merge that first; the release check refuses a mismatch.
3. **Tag** a commit that deployed, with the user's go-ahead (it's a push): the merge once
   deploy.yml has passed for it (`gh run list --workflow deploy.yml --commit <sha>`), or
   the staging bump right after it (master's head, usually; a release of it ships the
   merge's images). `git tag v<version> <commit> && git push origin v<version>`.
   release.yml checks it (it waits while CI and deploy.yml still run, and refuses a
   commit with no images) and publishes the GitHub release; mobile.yml starts the store
   builds once that passed. Tags can't be moved, so check before pushing.
4. **Promote.** Once staging is healthy on those images: `bun run promote v<version>`
   opens `chore(infra): deploy v<version> to production`, which points
   `deploy/environments/production/release.yaml` at the tag (production's charts, values
   and Secrets are read there) and the release's images. It runs as the user, so CI runs
   on the pull request.
5. **Deploy** by merging it. Argo CD syncs `production-data` and `production-stack`;
   production admits only images deploy.yml signed on `master`. Watch it as in the
   deploy skill, with the production cluster's context.

A tag pushed by mistake: `gh release delete v<version> --cleanup-tag` (before anything
was promoted). Undoing a release in production: the rollback skill.
