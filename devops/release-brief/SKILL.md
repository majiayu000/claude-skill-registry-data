---
name: release-brief
description: >
  Prep a release: detect the repo's release convention (lockstep tag vs
  per-service tag vs plain semver), draft the changelog from recent commits,
  propose the bump kind, and show the exact command to run. Does NOT run the
  release without explicit user approval.

  Trigger this skill when:
  - User says "cut a release", "bump version", "release", or invokes
    `/release-brief`.
  - After merging a big PR that closes a milestone.
---

## Detect release convention

Look for these markers at repo root, in this order:

### `.scripts/release.sh` present

- **cidca-platform**: lockstep — one `VERSION`, one tag `v<X.Y.Z>`, fires both
  ecg_auto and ecg-ui prod deploys.
- **cidca-services**: per-service — pass `<service>` as first arg. Tag is
  `<service>/v<X.Y.Z>`. Only that service's prod workflow fires.

Show:
```
.scripts/release.sh <?service?> patch|minor|major|<explicit>
git push origin dev --follow-tags
```

### `package.json` with `version` + no `.scripts/release.sh`

Plain semver. Use `pnpm version patch|minor|major` (or `yarn`/`npm`
equivalent). No auto-push.

### `pyproject.toml` only

Manual bump in `[project] version` (or `[tool.poetry] version`). Tag as `v<X.Y.Z>`.

### Zotea

Zotea auto-deploys `main` via Vercel. No explicit tag. "Release" = merge to
`main`. Instead of this skill, offer to summarize what's changed on `main` since
the last "release" (approximated via last significant commit or last tag).

## Behavior

1. Get last 20 commits since the current `VERSION` / last tag / last major
   commit.
2. Cluster by Conventional Commit type (`feat`, `fix`, `chore`, etc.).
3. Suggest bump:
   - Any `feat` → minor (unless big breaking change → major).
   - Only `fix`/`chore` → patch.
   - Any commit with `!` breaking marker → major.
4. Draft changelog:
   ```
   ## v<X.Y.Z> — YYYY-MM-DD

   ### Features
   - subject (author, PR #N)

   ### Fixes
   - subject (author, PR #N)

   ### Chores / docs / infra
   - subject (author, PR #N)
   ```
5. Show the exact command to run + wait for `push` authorization (see
   `never-auto-push`).

## Do not

- Run `git push --follow-tags` without explicit user "push" authorization.
- Bump the version file yourself unless `.scripts/release.sh` doesn't exist
  and the user explicitly asks.
- Overwrite an existing tag (`release.sh` refuses; respect that).
- Cut a release on a dirty tree — abort with `dirty tree, commit or stash first`.

## Post-release checklist (mention, don't do)

- Watch preprod → prod deploy in GH Actions.
- If cidca-platform: watch both `ecg_auto--deploy_prod.yml` and
  `ecg-ui--deploy_prod.yml`.
- If cidca-services: watch the per-service prod workflow only.
- Rollback: revert commit + rebump patch. Never delete a pushed tag.
