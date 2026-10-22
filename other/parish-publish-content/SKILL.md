---
name: parish-publish-content
description: Finish a content change on the new farakurim.cz site - commit, and release after the user confirms (the release checks, builds and publishes the site). Use at the end of parish-create-event, parish-correct-event, parish-cancel-event, parish-pin-event, parish-create-service-sheet, parish-correct-service-sheet, parish-create-exception, parish-create-album, parish-create-petrklic and parish-correct-petrklic, or whenever src/content/ was edited to publish events, service sheets ("ohlášky"), albums or Petrklíč issues.
---

# Publish a content change

The site is a static export: content lives in `src/content/*.ts`, and a change goes live with the next release
(`parish-release`), which runs the checks (format, tests, lint, types), builds and publishes the site, and
publishes nothing when a check fails. So this skill does not run them, and a content change needs no
browser check: the content tests check the data, and the pages are built from components already checked.

Uploaded files (posters, attachments, the weekly PDF, Petrklíč issues, album photos) are **not** in git or `out/`: they are
uploaded to `/uploads/…` and the content links them root-relative, as `/uploads/…`.
The create skills stage them in `uploads/` (git-ignored) with `pnpm stage` (album photos with
`pnpm add-album --write`), and the release uploads them.

## 1. Commit

Use the `commit` skill with the `content` scope, `feat` for new content and `fix` for a correction:

- `feat(content): add the Hody v České event`
- `feat(content): publish the service sheet for 4.–11. 10. 2026`
- `feat(content): cancel the mass on 25. 10. 2026`
- `fix(content): correct the Petrklíč 2/2026 PDF`

Never stage `uploads/` or `out/`.

## 2. Release

Run the `parish-release` skill: `pnpm release` previews the commits, the version and the staged uploads, and after the
user's yes `pnpm release --yes` uploads them, bumps the version, tags the release and pushes `main` with the tag,
which is then checked, built, published and verified. If the release fails (a
check, or a linked upload missing), fix it in a new commit and release again. Do not upload, deploy, tag or push without the
user's explicit yes. When the user only wants a backup, push `main` without a release.
