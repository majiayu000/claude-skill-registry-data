---
name: release
description: Walks through an EasyTask release end to end - checks, version bump, bilingual changelog, release PR, tag, Release workflow, draft verification, publish and updater check. Use when the user wants to release, publish a version, bump the version, ship X.Y.Z, or says "pubblica".
---

# Release (EasyTask)

Source of truth: `RELEASING.md` (read it if anything here is unclear). The Release workflow (`.github/workflows/release.yml`) always creates a DRAFT release; nothing reaches users until the draft is published. The user writes in Italian: answer in their language.

Rules:
- Commit, tag, push, merge and publish are outward-facing. Confirm each with the user before running it, unless they already said to proceed. Never publish the draft without an explicit "pubblica" (or equivalent).
- Merging a PR can be blocked in auto permission mode: ask the user to switch mode or to merge it.
- Follow the session's attribution rules for commit messages and PR bodies.
- Do not reuse a version number that may already be installed.

## 1. Decide the version

- Last release: `git describe --tags --abbrev=0`; commits since: `git log <tag>..HEAD --oneline`. Pick X.Y.Z (semver) and confirm it with the user.
- Check state: `git status --short`, `gh run list --workflow ci.yml --branch master -L 3` (master must be green), `gh release list -L 3`.
- Everything to ship must already be on `master`. Do not sweep unrelated uncommitted work into the release commit.

## 2. Branch

```
git switch master && git pull
git switch -c chore/release-X.Y.Z
```

## 3. Changelog (both languages)

Edit `CHANGELOG.md` (English) and `CHANGELOG.it.md` (Italian translation of the same section; Italian headings are `Aggiunto`, `Modificato`, `Corretto`). Keep a Changelog format:
- Rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` and add a fresh empty `## [Unreleased]` above it.
- Sections `### Added` / `### Changed` / `### Fixed`; entries are full sentences describing the user-visible effect (see 0.10.1 / 0.10.0 for tone).
- Bottom links: change `[Unreleased]: .../compare/vPREV...HEAD` to `vX.Y.Z...HEAD` and add `[X.Y.Z]: https://github.com/ivanerricis/easytask-tauri/compare/vPREV...vX.Y.Z`. Same in both files.
- `release:check` and the workflow fail if either file lacks the `## [X.Y.Z]` section. The notes go in the release as `## English` + `## Italiano`.

## 4. Bump

```
npm run release:bump X.Y.Z
npm run release:check
git status --short
```
Updates `package.json`, `package-lock.json`, `src-tauri/Cargo.toml`, `src-tauri/Cargo.lock`, `src-tauri/tauri.conf.json`. Does not commit.

## 5. Pre-release checks (same as the "Check: all (like CI)" task)

Run in order, stop at the first failure and fix it:
```
npm run release:check
npx eslint .
npx tsc -b
npm run e2e:typecheck
npm run test
npm run build
cd src-tauri
cargo fmt --check
cargo clippy -- -D warnings
cargo test
```
CI also runs `cargo audit` and `cargo deny check` (in `src-tauri`) and `npm audit --omit=dev --audit-level=high`. `src-tauri/deny.toml` currently accepts the yanked `zip@4.6.1` pulled in by `tauri-plugin-updater`; revisit it when the plugin moves to zip 9.0.3.
The Windows e2e CI job only runs via `workflow_dispatch` (elevation breaks WebView2 on the runner); it is not a release blocker.

## 6. Commit and PR

After confirmation:
```
git commit -am "chore(release): vX.Y.Z"
git push -u origin chore/release-X.Y.Z
gh pr create --base master --title "chore(release): vX.Y.Z" --body "..."
gh pr checks --watch
```
Wait for CI green, then merge with the user's OK (`gh pr merge --merge`; history uses merge commits, e.g. "Merge pull request #40 from ivanerricis/chore/release-0.10.1"). Then:
```
git switch master && git pull
```

## 7. Preflight and tag

On `master`, clean tree, merged release commit:
```
powershell -NoProfile -ExecutionPolicy Bypass -File .vscode/release-preflight.ps1 -Version X.Y.Z
```
It checks: on master, clean tree, `package.json` = X.Y.Z, both changelogs have the section, tag does not exist, `release:check` passes. Fix every NO. Then, after confirmation:
```
git tag vX.Y.Z
git push origin vX.Y.Z
```
Pushing the tag should start the Release workflow.

## 8. Watch the workflow

```
gh run list --workflow release.yml -L 3
gh run watch <id> --exit-status
```
If no run appears after the tag push (this happened on 0.10.1), start it on the tag:
```
gh workflow run release.yml --ref vX.Y.Z
```
It only works on `v*` tags (not branches). Jobs: `prepare` (tag, versions, notes extraction, seconds), then `release` (Windows + Linux, draft, the Windows leg also uploads the portable zip) and `verify` (Linux checks) at the same time. The builds do not wait for `verify`, so the draft can exist while `verify` is red: the whole run must be green (`gh run view <id>`) before the draft is published. On failure read `gh run view <id> --log-failed`, fix via a new PR; to redo a wrong tag: `git tag -d vX.Y.Z` and `git push origin :refs/tags/vX.Y.Z`, delete the draft, then re-tag.

## 9. Verify the draft (do not publish yet)

```
gh release view vX.Y.Z
gh release view vX.Y.Z --json isDraft,assets -q '{draft: .isDraft, assets: [.assets[].name]}'
```
First confirm the Release run finished green, `verify` included (`gh run list --workflow release.yml -L 1 --json conclusion`). Expect `isDraft: true` and: NSIS `EasyTask_X.Y.Z_x64-setup.exe` + `.sig`, `.deb`, `.AppImage` + `.sig`, `latest.json`, `EasyTask_X.Y.Z_x64_portable.zip`. Check the body has `## English` and `## Italiano`. Check `latest.json` (`gh release download vX.Y.Z -p latest.json -D <scratch dir>`): `version` is X.Y.Z and the platforms carry `url` and `signature`. Report the result to the user and wait.

## 10. Publish

Only when the user says so ("pubblica"):
```
gh release edit vX.Y.Z --draft=false
```

## 11. Post-release check

The updater endpoint (`plugins.updater.endpoints` in `src-tauri/tauri.conf.json`) is `https://github.com/ivanerricis/easytask-tauri/releases/latest/download/latest.json`; it resolves to the latest published release.
```
gh release view vX.Y.Z --json isDraft,url
curl -sL https://github.com/ivanerricis/easytask-tauri/releases/latest/download/latest.json
```
Confirm `version` is X.Y.Z. Suggest that the user tries "Check for updates" in Settings > About from the previous version. If a published release is bad, set it back to draft or delete it so the updater stops offering it, then ship a new version.

Finally, offer to update the user's release memory note (latest release and date).
