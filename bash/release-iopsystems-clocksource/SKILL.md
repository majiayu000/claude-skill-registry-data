---
name: release
description: Create a release PR with version bump, then auto-tag after merge
---

Create a release PR that bumps the version and updates the changelog. After the PR is merged, the `tag-release.yml` workflow will automatically tag the release, trigger `cargo publish`, and bump to the next development version.

## Arguments

The skill accepts a version level argument:
- `patch` - 0.0.1 -> 0.0.2
- `minor` - 0.0.1 -> 0.1.0
- `major` - 0.0.1 -> 1.0.0
- Or an explicit version like `0.2.0`

Example: `/release minor`

## Steps

1. **Verify prerequisites**:
   - Must be on `main` branch
   - Working directory must be clean
   - Must be up to date with origin/main

   ```bash
   git fetch origin
   if [ "$(git branch --show-current)" != "main" ]; then
     echo "Error: Must be on main branch"
     exit 1
   fi
   if [ -n "$(git status --porcelain)" ]; then
     echo "Error: Working directory not clean"
     exit 1
   fi
   if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/main)" ]; then
     echo "Error: Not up to date with origin/main"
     exit 1
   fi
   ```

2. **Run local checks**:
   ```bash
   cargo clippy --all-targets --all-features -- -D warnings
   cargo test --all
   ```
   If checks fail, stop and report the errors.

3. **Determine the new version**:
   - Read the current version from `Cargo.toml`
   - Calculate the new version based on the level argument (patch/minor/major) or use the explicit version provided

4. **Create release branch**:
   ```bash
   NEW_VERSION="X.Y.Z"  # from step 3
   git checkout -b release/v${NEW_VERSION}
   ```

5. **Bump version in Cargo.toml**:
   - Update the `version = "..."` field in the root `Cargo.toml`

6. **Update CHANGELOG.md**:
   - Move items from the "Unreleased" section to a new version section with the release date
   - Create a new empty "Unreleased" section
   - The changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format
   - Ask the user if they want to review/edit the changelog before proceeding

7. **Commit changes**:

   **CRITICAL**: The commit message MUST start with `release: v` (no other words before the version).
   The `tag-release.yml` workflow matches `startsWith(message, 'release: v')` on the merge commit.
   When GitHub squash-merges a single-commit PR, the commit message becomes the merge commit message.

   ```bash
   git add Cargo.toml CHANGELOG.md
   git commit -m "release: v${NEW_VERSION}"
   ```

8. **Push and create PR**:
   ```bash
   git push -u origin release/v${NEW_VERSION}

   gh pr create \
     --title "release: v${NEW_VERSION}" \
     --body "$(cat <<EOF
   ## Release v${NEW_VERSION}

   This PR prepares the release of v${NEW_VERSION}.

   ### Changes
   - Version bump to ${NEW_VERSION}
   - Changelog update

   ### After Merge
   The tag-release workflow will automatically:
   1. Create git tag \`v${NEW_VERSION}\`
   2. Trigger CI + publish to crates.io
   3. Create a GitHub Release
   4. Bump to next development version (\`-alpha.0\`)

   ---
   See CHANGELOG.md for details.
   EOF
   )"
   ```

9. **Report the PR URL** to the user.

## After PR Merge

When the PR is merged to main, the `tag-release.yml` workflow will:
1. Detect the version from `Cargo.toml`
2. Create and push the git tag `vX.Y.Z`
3. The `release.yml` workflow then runs CI and publishes to crates.io
4. Create a commit bumping to next dev version (e.g., `0.0.2-alpha.0`)

## Troubleshooting

- **gh CLI not installed**: `brew install gh` or see https://cli.github.com/
- **Not authenticated with gh**: `gh auth login`
- **RELEASE_TOKEN secret missing**: The tag-release workflow needs a PAT with `contents: write` stored as `RELEASE_TOKEN` in repo secrets (the default GITHUB_TOKEN can't trigger other workflows)
- **CARGO_REGISTRY_TOKEN secret missing**: The release workflow needs a crates.io API token stored as `CARGO_REGISTRY_TOKEN` in repo secrets
