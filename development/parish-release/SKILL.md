---
name: parish-release
description: Release the new farakurim.cz site with `pnpm release` - preview the commits, version and staged uploads, ask the user for an explicit yes, then upload uploads/, tag vX.Y.Z and push, which checks, builds and publishes the site (or, with --local when GitHub Actions is down, does it from this machine). Use at the end of parish-publish-content, or whenever the user asks to deploy, release, upload, publish to the server or sync the site.
---

# Release the site

`pnpm release` does the release: it uploads the staged files, tags and pushes, and the pushed tag is checked, built
and published. `pnpm release --local` publishes from this machine instead. How and where the site is deployed is the
scripts' business (`docs/deployment.md`), not this skill's.

## Release

1. **Preview:** run `pnpm release`. Without a terminal it only previews: it checks the tree is clean, on `main` and
   not behind `origin/main`, lists the commits since the last tag, picks the version (minor for a `feat` outside the
   `content` scope, patch otherwise) and lists the new files for `/uploads/` and the new or changed cron scripts
   (`cron-scripts/`). If it stops on a dirty tree (often `AGENTS.md` re-added by `next dev`), ask the user to commit or
   discard it.
2. **Ask** the user, with the version, the commits, the uploads and any cron scripts from the preview, for example:

   > Release v1.1.0? (2 commits, 3 new files in /uploads/)

   Wait for a clear yes; it publishes the site. Without it, stop: the commits stay as they are.

3. **Release:** `pnpm release --yes` (add `--major` only when the user asks). It uploads the new files and the cron
   scripts, makes the commit `chore(release): vX.Y.Z` and the tag, and pushes `main` with the tag.
4. **Stop there:** do not query the run (no `gh`, no GitHub API). Tell the user the release is pushed and that the
   repo's Actions tab shows the check, the build, the linked-uploads check, the deploy and the Verify step. A failed
   run is fixed in a new commit and released with a new version.

Never move or reuse a pushed tag.

## Release from this machine

Only when the user asks, e.g. because GitHub Actions is down: `pnpm release --local` previews more (a minute or two). It
builds with `RELEASE_BUILD=1`, which stops first unless `.env.local` sets the Google Calendar key and both Matomo
variables, runs the full check (Prettier, the site tests, lint, types) and a fresh `pnpm build`, and summarises the sync
of `out/` (new, changed, deleted files) with every deleted file outside `_next/`. Name any deleted page or file outside
`_next/` in the question. After the yes, `pnpm release --local --yes` runs the checks and the build again, uploads the
new files, checks that every linked upload is online, publishes `out/`, verifies the live site, then commits, tags
and pushes; the commit's trailer `Release-Deploy: local` keeps the workflow from deploying the tag again. Report the
version and the verify lines. If the run stops after publishing (verify failed), the site is live but untagged: tell the
user, fix it in a new commit and release again.
