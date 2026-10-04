---
name: release
description: Create a release PR with version bump on main or a release branch; CI tags it after merge
---

Create a release PR that bumps the version. After the PR is merged, `tag-release.yml` tags the merge commit (which triggers `release.yml` to build and publish packages) and opens the post-release version bump PR.

## Branching model

- `main` is the development line. New minor and major releases are cut from it.
- Each release line has a branch named `X.Y.x` (for example `0.0.x`), created at the line's first release tag. Patch releases for that line are cut from it, and fixes reach it by cherry-pick or backport PR.
- Run this skill on `main` for a new minor/major release, or on an `X.Y.x` branch for a patch release on that line. The release PR targets the branch you started from.

## Arguments

The skill accepts a version level argument:
- `patch` - 0.0.1 -> 0.0.2
- `minor` - 0.0.1 -> 0.1.0
- `major` - 0.0.1 -> 1.0.0
- Or an explicit version like `0.1.0`

Example: `/release minor`

On an `X.Y.x` branch only `patch` (or an explicit `X.Y.Z` on that line) makes sense.

## Steps

1. **Verify prerequisites**:
   - On `main` or an `X.Y.x` release branch
   - Working directory clean
   - Up to date with the same branch on origin

   ```bash
   git fetch origin
   BASE=$(git branch --show-current)
   if [ "$BASE" != "main" ] && ! echo "$BASE" | grep -Eq '^[0-9]+\.[0-9]+\.x$'; then
     echo "Error: run on main or an X.Y.x release branch"
     exit 1
   fi
   if [ -n "$(git status --porcelain)" ]; then
     echo "Error: Working directory not clean"
     exit 1
   fi
   if [ "$(git rev-parse HEAD)" != "$(git rev-parse origin/$BASE)" ]; then
     echo "Error: Not up to date with origin/$BASE"
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
   - Read the current version from `Cargo.toml` (root, single crate). On a development line it carries an `-alpha.N` suffix; the release version drops it.
   - Calculate the new version based on the level argument or use the explicit version provided. On an `X.Y.x` branch the result must stay on `X.Y`.

4. **Create release branch**:
   ```bash
   NEW_VERSION="X.Y.Z"  # from step 3
   git checkout -b release/v${NEW_VERSION}
   ```

5. **Bump version in Cargo.toml**:
   - Update the `version = "..."` field in the root `Cargo.toml`
   - Run `cargo check` to regenerate `Cargo.lock`

6. **Update CHANGELOG.md**:
   - Move items from the "Unreleased" section to a new version section with the release date
   - Create a new empty "Unreleased" section
   - The changelog follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) format
   - Ask the user if they want to review/edit the changelog before proceeding

7. **Commit changes**:

   **CRITICAL**: The commit message MUST start with `release: v`. `tag-release.yml` keys on it; any other prefix means no tag and no release.

   ```bash
   git add Cargo.toml Cargo.lock CHANGELOG.md
   git commit -m "release: v${NEW_VERSION}"
   ```

8. **Push and create PR** against the branch you started from:
   ```bash
   git push -u origin release/v${NEW_VERSION}

   gh pr create \
     --base "$BASE" \
     --title "release: v${NEW_VERSION}" \
     --body "$(cat <<EOF
   ## Release v${NEW_VERSION}

   This PR prepares the release of v${NEW_VERSION} from \`${BASE}\`.

   ### Changes
   - Version bump to ${NEW_VERSION}
   - Changelog update

   ### After Merge
   \`tag-release.yml\` tags the merge commit \`v${NEW_VERSION}\`, which triggers the release workflow, and opens the post-release bump PR against \`${BASE}\`.
   EOF
   )"
   ```

9. **Report the PR URL** to the user.

## After PR Merge

Do **not** tag by hand. Squash-merging the PR produces a commit on `$BASE` titled `release: vX.Y.Z (#N)`, and `tag-release.yml` then:

1. Creates and pushes the annotated tag `vX.Y.Z`
2. Opens `chore: bump to X.Y.(Z+1)-alpha.0` as a PR against `$BASE`

A tag pushed by hand before the workflow runs makes it see an existing tag and skip step 2, so the branch is left on the release version with no development bump.

The tag triggers `release.yml`, which:
1. Builds .deb and .rpm packages (amd64 + arm64)
2. Signs packages with GPG
3. Publishes to APT and YUM S3 repositories
4. Creates a GitHub Release with artifacts

Then merge the bump PR once its checks pass.

For a new minor or major release from `main`, create the release line's branch at the new tag once it exists:

```bash
git push origin vX.Y.0^{commit}:refs/heads/X.Y.x
```

## Troubleshooting

- **gh CLI not installed**: `brew install gh` or see https://cli.github.com/
- **Not authenticated with gh**: `gh auth login`
- **No tag after merge**: check the merge commit message starts with `release: v`, and that `tag-release.yml` triggers on this branch.
