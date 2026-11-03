---
name: flisk-release
description: Guides an AI assistant through cutting a Flisk CLI release end to end - picking the commit, running the release candidate, dispatching the release workflow, finishing the GitHub releases, npm (@flisk-sh/flisk, GitHub Packages) and the binary release on flisk-sh/releases, verifying every channel, and repairing a release that only half finished. Use when asked to "release", "run release", "ship a version", "publish to npm", or when a Release | Binaries or Release | Candidate run is red.
license: MIT
compatibility: Requires the gh CLI authenticated with write access to flisk-sh/flisk (and flisk-sh/releases for repairs), curl and Node 22+. Runs entirely through GitHub Actions; no local build is needed.
metadata:
  author: flisk-sh
  version: "1.0"
---

# Releasing Flisk

The human version of this guide is `docs/releasing.md`. It holds the background, every troubleshooting row and the settings and secrets. This skill is the procedure. Read the doc's [Troubleshooting](../../../docs/releasing.md#troubleshooting) table before you diagnose any red run.

Workflows (IDs are stable, names have emoji, so use the file name):

| File | What it does |
| --- | --- |
| `release-candidate.yml` | Packs the CLI, runs quickstart (Q1-Q4) and every release-blocking resource-type suite on that tarball, the longest suites first. Runs only on `release/*` branches and `rc-*` tags. ~6-10 min. With `-f release=true` it also dispatches `release-binaries.yml` on its own branch right after the plan; the release builds alongside the suites and its `publish` job waits for this candidate, publishing only if every job passed. |
| `release-binaries.yml` | `build` → `windows-binary` → `publish` (gate, binaries to `flisk-sh/releases`, npm, signing, bump or tag) → `publish-github-packages`. ~6 min. |
| `sign-release.yml` | Signs an already published version after the fact. |
| `publish-existing-npm-to-github-packages.yml` | Backfills GitHub Packages for a version already on npm. |

## 1. Check the state before touching anything

```bash
gh run list -R flisk-sh/flisk -w release-binaries.yml -L 5
gh run list -R flisk-sh/flisk -w release-candidate.yml -L 5
gh release list -R flisk-sh/releases -L 3      # binaries: the real "latest"
gh release list -R flisk-sh/flisk -L 3         # checksums; a Draft here means a half-finished release
curl -s https://registry.npmjs.org/@flisk-sh%2fflisk | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>console.log(JSON.parse(s)["dist-tags"]))'
```

If recent release runs are red, read why (`gh run view <id> --log-failed | grep -E "##\[error\]|FAIL"`) before dispatching again. A red publish gate (`No passing Release candidate covers <sha>`) is fixed by a candidate, never by re-dispatching. If a version is already on npm but its `flisk-sh/flisk` release is a draft or has no tag, go to step 6. Do not cut a new version.

## 2. Pick the commit

Use the newest `main` commit whose push CI and `E2E | Journeys` are green:

```bash
gh run list -R flisk-sh/flisk -w e2e-journeys.yml -b main -L 3 --json headSha,conclusion
```

Do not reuse an older `release/*` branch. Fixes land on `main` daily, and a candidate on a stale branch fails on bugs `main` already fixed (1.4.5 lost four dispatches this way).

## 3. Run the release candidate

```bash
SHA=<commit>; V=<next version, e.g. 1.4.6>; N=1   # N: attempt number, new for every retry on a new commit
gh api repos/flisk-sh/flisk/git/refs -f ref=refs/heads/release/$V-rc$N -f sha=$SHA
gh workflow run release-candidate.yml -R flisk-sh/flisk --ref release/$V-rc$N -f release=true   # also starts the release now; its publish job waits for this candidate
gh run watch <run-id> -R flisk-sh/flisk --exit-status
```

Never dispatch the candidate on `main`: its `package` job refuses `refs/heads/main`. If the run fails:
- Read the failing case first. Look up its message in the troubleshooting table.
- Retry only when every failure is the same infrastructure readiness timeout. Say so explicitly.
- A real failure is a bug. Fix it on `main` through a PR, then cut a new branch from `main` with the next `N` (the old ref already exists, and moving it would rewrite what an earlier run tested). Never weaken or skip the gate.

## 4. Dispatch the release

```bash
RC=release/$V-rc$N
GH_TOKEN="$(gh auth token)" node scripts/check-release-candidate.mjs --sha "$(gh api repos/flisk-sh/flisk/git/refs/heads/$RC --jq .object.sha)" --repo flisk-sh/flisk
gh workflow run release-binaries.yml -R flisk-sh/flisk --ref $RC
gh run watch <run-id> -R flisk-sh/flisk --exit-status
```

Dispatch on the candidate's branch, not on `main`: it releases exactly the commit the candidate tested, and other merges into `main` during the candidate no longer void it (1.4.24 lost rc5, rc6 and rc7 that way). The version bump PR still targets `main`. The workflow picks the version itself. Do not edit `package.json` to choose one.

Publishing happens inside `publish`. Once that job is green, npm and `flisk-sh/releases` are live even if later jobs are red. **Never re-dispatch after `publish` succeeded**: it would publish the next version.

## 5. Finish the bookkeeping

- `main` behind the published version: the run opens `Release <version> (automatic version bump)`. Approve it: `gh pr checks <n> --watch && gh pr review <n> --approve`. Its merge push runs `tag-bumped-release`, which tags `v<version>` and publishes the draft.
- `main` already at the version: the publish job tags the released commit and publishes the draft itself (`Tag the released commit and publish the GitHub release`).

## 6. Verify every channel

```bash
V=<version>
curl -s https://registry.npmjs.org/@flisk-sh%2fflisk/$V | grep -o '"version":"[^"]*"'         # scoped npm
gh release view v$V -R flisk-sh/releases --json isDraft,assets --jq '{draft:.isDraft,n:(.assets|length)}'
gh release view v$V -R flisk-sh/flisk --json isDraft,assets --jq '{draft:.isDraft,assets:[.assets[].name]}'
gh api repos/flisk-sh/flisk/git/refs/tags/v$V --jq .object.sha                                # tag exists
```

Expected:
- the scoped npm version exists;
- the binaries release is not a draft and has 5 binaries, the engine, the zip, the checksums and the signature;
- the `flisk-sh/flisk` release is not a draft and has `checksums.txt`, `.sigstore.json` and `.intoto.jsonl`;
- the tag exists.

GitHub Packages: `docs/github-packages.md#maintainer-release-checks`.

Repairs, all without a new release:
- **Draft or tag missing on `flisk-sh/flisk`:** check each piece, then create only what is missing.
  1. Pick the tag target. The tag must point at a commit whose `package.json` says `$V`:
     - the run bumped the version: the merged bump commit (`Release $V (automatic version bump)` on `main`);
     - no bump: the run's `headSha`.
     Confirm with `gh api "repos/flisk-sh/flisk/contents/package.json?ref=<commit>" --jq .content | base64 -d | grep '"version"'`.
  2. Tag, only if `gh api repos/flisk-sh/flisk/git/refs/tags/v$V` returns 404: `gh api repos/flisk-sh/flisk/git/refs -f ref=refs/tags/v$V -f sha=<commit>`.
  3. Release: if `gh release view v$V -R flisk-sh/flisk` fails, there is none. Create an empty draft (`gh release create v$V -R flisk-sh/flisk --draft --latest=false --title v$V --notes "Signed checksums for flisk $V."`) and run `sign-release.yml` (next item).
  4. Publish only once the draft has `checksums.txt` and `checksums.txt.sigstore.json`: `gh release edit v$V -R flisk-sh/flisk --tag v$V --draft=false --latest=false`. Never publish an unsigned release.
- **Signature missing:** `gh workflow run sign-release.yml -f version=$V`. It attaches `checksums.txt` and its signature to both releases.
- **GitHub Packages missing:** `gh workflow run publish-existing-npm-to-github-packages.yml -f version=$V`.
- **No unscoped `flisk` on npm:** expected. npm rejects the name as too similar to `plist` (`E403`), so the release no longer publishes it (`docs/releasing.md#unscoped-npm-package-flisk`).

## 7. Report and improve

Tell the user:
- the version and the release run URL;
- each channel's state from step 6;
- anything finished by hand and anything still open.

If this release hit a failure the troubleshooting table does not cover, add a row to `docs/releasing.md`, a case-study line, and, if the workflow can prevent it, a fix to `release-binaries.yml`, in a PR. Add one line to `.claude/memory/MEMORY.md` when it is a trap other agents will hit.
