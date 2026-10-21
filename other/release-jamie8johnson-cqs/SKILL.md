---
name: release
description: Release a new version of cqs. Bumps version, updates changelog, runs the recall gate, publishes to crates.io, creates GitHub release.
disable-model-invocation: true
argument-hint: "[major|minor|patch]"
---

# Release

Release a new version of cqs.

## Arguments

- `$ARGUMENTS` — version bump type: `major`, `minor`, or `patch` (default: `patch`)

## Process

1. **Pre-flight checks**:
   - `git status` — must be clean (no uncommitted changes)
   - `gh pr list --state open` (via PowerShell) — review any open PRs. Merge or close before releasing.
   - `cargo test --features cuda-index` — all tests must pass (full suite is correct here; this is the one place it runs deliberately)
   - `cargo clippy --all-targets --features cuda-index -- -D warnings` — no warnings (CI runs `--all-targets`)
   - Confirm on `main` branch

2. **Recall gate (REQUIRED before tagging)**:
   - Run BOTH fixtures against the current index:
     ```bash
     cqs eval evals/queries/v3_test.v2.json --json
     cqs eval evals/queries/v3_dev.v2.json --json
     ```
   - Compare R@1/R@5/R@20 against the previous release's snapshot (README TL;DR line / RESULTS log).
   - **If numbers dropped**: check for dead gold origins FIRST — the matcher is `(origin, name)`, so file splits/renames since the last release kill gold origins and cap R@K, masquerading as a recall regression. Line-number drift alone is harmless.
   - The definitive regression test is a same-corpus binary A/B: run the previous release binary and the new one against the SAME index and diff the reports. Only a regression confirmed by the A/B blocks the release.

3. **Version bump**:
   - Read current version from `Cargo.toml`
   - Calculate new version based on bump type
   - Update `Cargo.toml` version field
   - Run `cargo check` to update `Cargo.lock`

4. **Docs review**:
   Run `/docs-review`. Fix anything stale before cutting the release.

   **Eval-number sync** — if the recall-gate numbers changed, update every surface that quotes them:
   - `README.md` TL;DR line (R@1/R@5/R@20 + snapshot date/corpus size)
   - `Cargo.toml` `description` (crates.io one-liner quotes the same numbers)
   - GitHub repo description: `gh repo view` / `gh repo edit --description` (via PowerShell)

5. **Changelog**:
   - Read `CHANGELOG.md`
   - Stamp the `## [Unreleased]` section into `## [X.Y.Z] - YYYY-MM-DD` (run `date` first; create the section from `git log` since the last tag if no Unreleased block exists)
   - Categorize: Added, Changed, Fixed, Removed
   - Update the compare links at the bottom of the file

6. **Commit and tag**:
   - Create branch: `release/vX.Y.Z`
   - `cargo fmt` then commit: `chore: Release vX.Y.Z`
   - Push from WSL: `git push -u origin release/vX.Y.Z` (PowerShell only as fallback if GCM crashes)
   - Create PR via PowerShell with `--body-file` (never inline heredocs): write body to `/mnt/c/Projects/cqs/pr_body.md`, use it, delete it
   - **Wait for CI — pin the run ID** (do NOT use `gh pr checks --watch`; it latches onto the previous commit's completed run):
     ```
     sleep 45
     powershell.exe -Command 'cd C:\Projects\cqs; gh run list --branch release/vX.Y.Z --workflow CI --limit 1'
     powershell.exe -Command 'cd C:\Projects\cqs; gh run watch RUN_ID --exit-status'
     ```
   - **Pre-tag cross-build dry-run (REQUIRED — catches macOS/Windows breaks the Linux-only PR CI can't see).** The `v*` tag is the only thing that builds all three release targets, so a platform-specific break (e.g. the v1.46.0 `aarch64-apple-darwin` E0277) is otherwise invisible until you've already tagged and published the crate. Trigger release.yml on the release branch as a build-only dry-run (it skips the "Create GitHub Release" job, which is gated on a tag ref) and confirm all three Build jobs pass BEFORE tagging:
     ```
     powershell.exe -Command 'cd C:\Projects\cqs; gh workflow run release.yml --ref release/vX.Y.Z'
     sleep 45
     powershell.exe -Command 'cd C:\Projects\cqs; gh run list --workflow release.yml --limit 1 --json databaseId,headBranch'
     # poll `gh run view <id> --json status,conclusion,jobs`; every Build job must be green before you tag
     ```

7. **After PR merge**:
   - Sync main: `git checkout main && git pull`, then `cqs index` (watch misses bulk git ops on WSL)
   - Tag: `git tag vX.Y.Z` and push it: `git push origin vX.Y.Z`
   - GitHub Release with pre-built binaries is created automatically by `.github/workflows/release.yml`
   - **Publish order**: if `cqs-macros/` changed since the last release, `cargo publish -p cqs-macros` FIRST, wait for it to land on crates.io, then `cargo publish -p cqs`. Otherwise just `cargo publish -p cqs`.

8. **Post-release**:
   - Update PROJECT_CONTINUITY.md with new version
   - Update ROADMAP.md if phase milestones changed
   - Rebuild and install the binary so the daemon serves the release: `cargo build --release --features cuda-index && systemctl --user stop cqs-watch && cp ~/.cargo-target/cqs/release/cqs ~/.cargo/bin/cqs && systemctl --user start cqs-watch`

## WSL notes

- `git push` works directly from WSL (credential helper wired); PowerShell is the fallback when GCM crashes ("could not read Username")
- All `gh` commands go through PowerShell (with `cd C:\Projects\cqs` or `-R jamie8johnson/cqs`)
- Always use `--body-file` for PR/release bodies — never inline heredocs
- Write body content to `/mnt/c/Projects/cqs/pr_body.md`, use it, then delete
