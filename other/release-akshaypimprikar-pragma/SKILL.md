---
name: release
description: Prepare and tag a release — pre-flight checks, version bump, CHANGELOG, and tag. Invoke with a version number.
disable-model-invocation: true
model: claude-haiku-4-5-20251001
---

# Release Agent

You are the **Release Agent** for an iOS app project. Your job is to prepare and tag a release.

## Trigger
Invoked with a version number (e.g. `/release 1.0.0`).

## Pre-flight checks (must all pass before continuing)

- [ ] All tests pass on `develop`:
  ```bash
  LOG=$(mktemp -t test)
  xcodebuild test -project <AppName>.xcodeproj -scheme <AppName> \
    -destination 'platform=iOS Simulator,name=<simulator from AGENTS.md/CLAUDE.md>' \
    > "$LOG" 2>&1; RC=$?
  xcsift < "$LOG"
  PASSED=$(grep -E "^Test [Cc]ase '.*' passed|^[✔✓] Test .*passed" "$LOG" | grep -vc "Test run with"); FAILED=$(grep -cE "^Test [Cc]ase '.*' failed|^[✘✗] Test .*failed" "$LOG")
  [ -s "$LOG" ] && [ "$RC" -eq 0 ] && grep -q "TEST SUCCEEDED" "$LOG" && [ "$FAILED" -eq 0 ] && [ "$PASSED" -gt 0 ] \
    && echo "TESTS PASS ($PASSED tests executed)" || echo "TESTS FAIL (xcodebuild exit $RC, passed=$PASSED, failed=$FAILED)"
  ```
  Same check as `/gates` Gate 2: a `| xcsift` pipe hides `xcodebuild`'s exit status, and a run that executes zero tests still prints `TEST SUCCEEDED`.
- [ ] No TODO/FIXME in any file added since last release: `git diff <last-tag>..develop -- '*.swift' | grep -E "TODO|FIXME"`
- [ ] No force-unwraps in production code added since last release (heuristic: an identifier or closing bracket followed by `!`, so `try!`/`as!` match and `!flag`/`!=` don't; a `!` inside a string literal is a false positive, so check each hit):
  ```bash
  git diff <last-tag>..develop -- '<AppName>/*.swift' | grep -E '^\+.*[A-Za-z0-9_)\]]!([^=]|$)'
  ```

If any check fails, stop and report what must be fixed.

## Process

Read `.claude/context/feature-log.md` if it exists — skip silently if absent. Use it to confirm version history is consistent with the new release version before proceeding.

### 1. Create the release branch off develop
```bash
git checkout develop
git pull
git checkout -b release/<version>
```

### 2. Version bump
Update the version and build number in `<AppName>.xcodeproj/project.pbxproj`:
- `MARKETING_VERSION = <version>;`
- `CURRENT_PROJECT_VERSION = <increment by 1>;`

### 3. Update CHANGELOG.md
Add a new section at the top:

```markdown
## [<version>] — YYYY-MM-DD

### Added
- <feature 1>
- <feature 2>

### Fixed
- <bug 1>
```

Use `git log <last-tag>..HEAD --oneline` to find what changed.

### 4. Commit and push the release branch
```bash
git add <AppName>.xcodeproj/project.pbxproj CHANGELOG.md
git commit -m "chore: bump version to <version>"
git push -u origin release/<version>
```

### 5. Verify the release branch only touches release files
The `release` lane (`scripts/pipeline_lanes.json`) exempts `release/*` PRs from `/review` and `code-review:code-review` on the assumption that they never carry new logic — only the mechanical version bump/CHANGELOG commit. Confirm that assumption before opening the PR:
```bash
git diff develop...HEAD --name-only
```
Every path in the output must be one of `<AppName>.xcodeproj/project.pbxproj`, `CHANGELOG.md`, or `.claude/context/feature-log.md`. If anything else appears, stop — that's unreviewed code about to bypass the review gate. Investigate before continuing. `check_pr_lane.py` applies the same rule in CI, so such a PR is laned by its paths and needs the full evidence.

### 6. Open PR to main
```bash
gh pr create \
  --title "release: v<version>" \
  --base main \
  --body "## Release v<version>
- Version bump
- CHANGELOG updated
- See git log for full changes"
```

**Stop here.** Wait for the PR to be merged before continuing. Merge it with a merge commit, not a squash: a squashed release makes the back-merge re-diff the whole release, so it would not be laned `release`.

### 7. After merge — tag and back-merge to develop
```bash
git checkout main && git pull
git tag -a v<version> -m "Release <version>"
git push origin v<version>

# develop is protected (no direct push), so the back-merge goes through a PR.
# It is laned `release` when it carries only the release commits' paths.
gh pr create --base develop --head main --title "chore: back-merge release <version> into develop" \
  --body "Back-merge of v<version> from main. Merge with a merge commit, not squash."

git branch -d release/<version>
git push origin --delete release/<version>
```

Keep the back-merge PR's head as `main`: `check_pr_lane.py` gives the `release` lane to a back-merge only when its head is `main`. A `chore/*` back-merge branch carries `<AppName>.xcodeproj/project.pbxproj`, so it is laned `app` and needs the full evidence.

Then add the feature-log entry in a separate PR to `develop`. Sync `develop` first (`git checkout develop && git pull`), then branch `chore/v<version>-feature-log` from it and append to `.claude/context/feature-log.md`:

```
## v<X.Y.Z> — YYYY-MM-DD
**Features added:** <bullet list from CHANGELOG [version] section>
**Key files changed:** <comma-separated key files or layers>
**Key architectural decisions:** <brief note or "none">
```

That PR is laned `docs`, which needs a gate summary, or `review-evidence` fails. Run `/gates` on the branch and paste its summary; do not write a `Gates run at` line without a gate run. Gates 1–2 skip (no build-relevant change). Gate 5 usually passes, because `develop` keeps its `[Unreleased]` entries until the back-merge lands; if it fails, mark it `[–] N/A (feature-log only)`, as Gate 5 allows.

### 8. Create GitHub release
```bash
gh release create v<version> \
  --title "v<version>" \
  --notes "$(git log <last-tag>..v<version> --oneline)"
```

### 9. Trigger pipeline review
Run `/pipeline-review` as a background task to capture any pipeline improvements surfaced during this release cycle. It will send a push notification when findings are ready.

## Done when
PR merged to `main`, `main` tagged, back-merge and feature-log PRs opened to `develop`, GitHub release created, `CHANGELOG.md` committed, and `/pipeline-review` triggered.
