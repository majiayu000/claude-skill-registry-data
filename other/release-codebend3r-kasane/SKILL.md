---
name: release
description: Use when cutting a kasane release — bumping the version, tagging, shipping the web build to Netlify, producing Tauri desktop binaries, or building for iOS/Android. Also use when asked why the store version differs from `package.json`.
---

# Release

kasane ships one codebase to five targets. The version lives in **two** files that drift silently: `package.json` (npm/tooling) and `app.json` (`expo.version`, the user-visible app version on iOS and Android). They are currently out of sync.

## Preflight

```bash
git switch main && git pull
bun install
bun run system-check     # typecheck + oxfmt + oxlint + test + web build
bun run build:web && bun run e2e
bun run scripts/audit-mappings.ts --errors-only
```

The catalog audit belongs here even though mappings are not in the repo: a release is the moment users refetch, and a catalog error reaches them regardless of what the code does.

## Bump the version in both places

**Check first whether the `version-bumper` skill already did this.** It bumps both files, commits, and tags locally without pushing, so a release often starts with the work below already done:

```bash
node -p "require('./package.json').version"
git tag --points-at HEAD          # prints v<version> if the bump is already tagged
```

If the tag is there and points at the version in `package.json`, skip to the push at the end of this section. Do not bump again — a second bump on top of an untagged-in-your-head-but-actually-tagged commit produces a version nobody released.

Otherwise:

```bash
VERSION=1.3.0
npm pkg set version=$VERSION
python3 - <<EOF
import json
p = "app.json"
d = json.load(open(p))
d["expo"]["version"] = "$VERSION"
json.dump(d, open(p, "w"), indent=2)
open(p, "a").write("\n")
EOF
git diff --stat package.json app.json    # both must appear
```

Native builds additionally need a monotonically increasing build number per submission (`expo.ios.buildNumber`, `expo.android.versionCode`). Bump those on every store upload even when the marketing version is unchanged.

Commit with the repo's `KSN:` convention, then tag:

```bash
git tag -a "v$VERSION" -m "v$VERSION"
```

Either way, the release starts at the push:

```bash
git push --follow-tags
```

## Per-target

| Target        | Command                 | Notes                                                                                                                                                                                                      |
| ------------- | ----------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Web           | `bun run build:web`     | Netlify builds from `netlify.toml` on push. Verify the deploy, then check the MangaDex covers actually load — that path depends on the `/_mdx` proxy and the `no-referrer` policy, and it breaks silently. |
| Desktop       | `bun run desktop:build` | Tauri 2 wraps `dist/`. Requires Rust and a `src-tauri/` created by `bunx tauri init` (see README). Keep the Tauri version in `src-tauri/tauri.conf.json` in step with `app.json`.                          |
| iOS / Android | EAS Build               | **There is no `eas.json` in the repo** despite the README claiming EAS ships both. Create one (`bunx eas build:configure`) before promising a native release, or correct the README.                       |

## Post-release

- Load the deployed site and confirm the catalog fetch succeeds; a Supabase RLS change can break reads without failing the build.
- Confirm a cold load renders from the persisted TanStack Query cache (the catalog is cached for 7 days).
- Confirm a deep link such as `/series/5114` resolves, which exercises the SPA fallback.

## Common mistakes

| Mistake                                        | Consequence                                                                                        |
| ---------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| Bumping only `package.json`                    | Store listings and the about screen keep showing the old version. This has already happened.       |
| Bumping again over a `version-bumper` tag      | The tag names one version and the files another. Check `git tag --points-at HEAD` before bumping.  |
| Reusing a native build number                  | The store rejects the upload.                                                                      |
| Releasing without re-running the catalog audit | Code ships clean while the data users refetch is wrong.                                            |
| Assuming a green web build means covers work   | The MangaDex proxy and `Referrer-Policy: no-referrer` only matter in production. Look at the page. |
| Skipping hooks with `--no-verify`              | `system-check` is the gate. Fix the failure.                                                       |
