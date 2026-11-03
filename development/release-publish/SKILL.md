---
name: release-publish
description: "Use when tagging versions or publishing a GitHub release. Version in every manifest, build, gates, a pathspec commit, push of main or one tag (never --tags, never --force), a draft release with checksums, promotion and a stranger's download check."
version: 1.0.0
author: iCLONE / CLONE FRAME
license: MIT
platforms: [macos, linux]
metadata:
  hermes:
    tags: [iclone-os, github, release, versioning, publish]
    related_skills: [sterilise-before-commit, github, agent-self-repo, consent]
---

# Release — one version, everywhere, verified from outside

## When to use

The owner asks to cut a version, tag it, or publish a release with downloadable files. For `gh` login and repo basics see the `github` skill (`references/auth.md`, and `references/repo-management.md` for releases); this skill is the safe order around them.

## Prerequisites

- `git`, `gh` (`gh auth status` shows a login with `repo` scope) and `shasum` (macOS) or `sha256sum` (Linux). Truth: each tool's `--help`.
- A clean tree: `git status --porcelain` prints nothing you did not mean to ship.
- Tag, push and release are WRITES → `~/.iclone-os/bin/acp consent request terminal --reason "Publish <vX.Y.Z> of <owner>/<repo>"`, state the version, the branch and the asset list, and wait for the owner's yes.

## Quick reference

bump → build → gates → sterilise → commit the checked index → push `main` → push ONE tag → draft release + `SHA256SUMS.txt` → check → promote → fresh download + logged-out check.

## Procedure

1. **Bump the version in every manifest.** Find them all first, then change each one:

   ```sh
   git grep -n -I -e '"version"' -e '^version' -- '*package.json' '*pyproject.toml' '*Cargo.toml' '*.plist' '*.conf.json'  # example
   ```

   Node packages: `npm version <X.Y.Z> --no-git-tag-version` (also updates the lockfile). Add the entry to `CHANGELOG.md`. Then `git grep -n '<old-version>'` must list only history notes. Stage exactly the release files: `git add -- <path> <path>` (`# example`).

2. **Build and run the project's gates** (tests, lint, type check, packaging). A failing gate stops the release; never skip one to "fix later".

3. **Sterilise.** Run `sterilise-before-commit` on the staged release changes (stage any file the build changed first). Zero findings or stop.

4. **Commit the scanned index, with no pathspec.** A pathspec re-reads the working tree and re-adds a file step 3 untracked (`git rm --cached`). List the index first: every path must be a release file; a stray one: `git restore --staged <path>`, then redo step 3:

   ```sh
   git diff --cached --name-only  # example
   git commit -m "release: <vX.Y.Z>"  # example
   ```

5. **Push the branch, then one annotated tag** (after the owner's yes):

   ```sh
   git push origin main && git tag -a <vX.Y.Z> -m "<vX.Y.Z>" && git push origin refs/tags/<vX.Y.Z>  # example
   ```

   A rejected push means someone else pushed: `git pull --rebase`, re-run the gates, push again. Do not force.

6. **Checksums and a draft release:**

   ```sh
   cd <dist> && shasum -a 256 <asset> <asset> > SHA256SUMS.txt && cd -  # example
   ```

   ```sh
   gh release create <vX.Y.Z> <dist>/<asset> <dist>/SHA256SUMS.txt --repo <owner>/<repo> --verify-tag --draft --title "<vX.Y.Z>" --notes-file <notes.md>  # example
   ```

   `--verify-tag` aborts if the tag is not on the remote. Add `--prerelease` for a beta.

7. **Promote** once the draft's assets and notes look right:

   ```sh
   gh release edit <vX.Y.Z> --repo <owner>/<repo> --draft=false --latest  # example
   ```

8. **Download it fresh** (a new empty folder on every run, no local build in the path). `gh` uses your own login, so this proves the files and checksums, not anonymous access:

   ```sh
   d=$(mktemp -d) && cd "$d" && gh release download <vX.Y.Z> --repo <owner>/<repo> && shasum -a 256 -c SHA256SUMS.txt  # example
   ```

   Public repo only — prove a stranger can download it with the logged-out URL: `curl -sSL -o /dev/null -w '%{http_code}\n' https://github.com/<owner>/<repo>/releases/latest/download/<asset>` prints `200` (`# example`). A private repo has no anonymous download.

## Pitfalls

- A version left behind in one manifest ships an app that reports the wrong version and breaks update checks.
- `git push --tags` publishes every local tag, including experiments and imported upstream tags.
- A pushed tag is public history. If it is wrong, publish `<vX.Y.Z+1>`; moving or deleting a published tag needs the owner's explicit yes and breaks anyone who already fetched it.
- Bundled third-party code can trip the secret scanner; record a reviewed exception, never disable the scan.
- Signing and notarisation are project-specific: run the project's own release script, never improvise identities.

## Never

- Never `git push --force`, `--force-with-lease` or `--tags` in a release.
- Never `git commit -a` or a pathspec commit in a release: both ship the working tree, not the scanned index.
- Never publish before the owner's yes and a passing gate run.

## Verification

`gh release list --repo <owner>/<repo> --json tagName,isDraft,isLatest --limit 5` (`# example`) shows `<vX.Y.Z>` with `"isDraft":false` and `"isLatest":true`, and `shasum -a 256 -c SHA256SUMS.txt` prints `OK` for every asset.
