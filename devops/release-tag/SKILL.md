---
description: Create a release tag on `main` following GitHub flow conventions (no release/* branch — tag the relevant `main` commit directly).
---

# Release Tag Creation Instructions

Assuming the release preparation is complete and the `main` branch is up to date, follow the instructions below to create a release.

## Instructions

### Prerequisites

- Latest changes have been merged into `main` branch
- All tests are passing
- Deployment has completed successfully
- Release notes are ready

### Steps

1. **Verify Release Readiness**

   ```bash
   # Switch to latest main branch
   git checkout main
   git pull origin main

   # Check current status
   git status
   git log --oneline -5
   ```

2. **Pre-tag Verification**

   ```bash
   # Check existing tags
   git tag --sort=-version:refname | head -10

   # Verify current branch
   git branch --show-current
   ```

3. **Confirm Release Version**

   **Confirm with user:**
   - New release version (e.g., v1.2.3)
   - Whether this is a pre-release or regular release

   **Release title is auto-generated:** version only (e.g., v1.2.3)

4. **Create Tag Based on Semantic Versioning**

   ```bash
   # Create new version tag (user-confirmed version)
   git tag -a v<USER_CONFIRMED_VERSION> -m "Release v<USER_CONFIRMED_VERSION>"

   # Push tag to remote
   git push origin v<USER_CONFIRMED_VERSION>
   ```

5. **Create Release Using GitHub CLI**

   ```bash
   # Create GitHub Release (title is version only)
   TODAY=$(date +%Y/%m/%d)

   # Create temporary release notes file
   cat > temp_release_notes.md << EOF
   **Release Date:** $TODAY

   ## Overview
   Key changes and improvements in this release

   ## Key Changes
   - [Manually add key changes here]

   EOF

   # Append auto-generated What's Changed
   echo "## What's Changed" >> temp_release_notes.md
   gh api repos/:owner/:repo/releases/generate-notes \
     -f tag_name="v<USER_CONFIRMED_VERSION>" \
     --jq '.body' >> temp_release_notes.md

   # Create release (use --latest for regular releases, --prerelease for pre-releases)
   gh release create v<USER_CONFIRMED_VERSION> \
     --title "v<USER_CONFIRMED_VERSION>" \
     --notes-file temp_release_notes.md \
     --latest

   # Remove temporary file
   rm temp_release_notes.md
   ```

6. **Post-release Verification**

   ```bash
   # Verify release
   gh release view v<USER_CONFIRMED_VERSION>

   # Check deployment status
   gh run list --workflow="CD Backend" --limit=5
   ```

### Release Flow

```
feature/* or fix/*  →  PR → merge to main  →  tag the main commit
```

GitHub flow なので `develop` / `release/*` といった長命ブランチは存在しない。
リリース対象の変更が `main` にマージされたら、その `main` のコミットに直接 semver タグを打つ。
通常は HEAD だが、過去のコミットを指定したい場合は `git tag v<VERSION> <SHA>` で固定する。

緊急修正も区別なし: `fix/*` ブランチからの PR を `main` にマージし、必要なら直後に新しいタグを打つ。

### Versioning Rules

Follow **Semantic Versioning (SemVer)**:

- **MAJOR**: Breaking changes
- **MINOR**: Backward-compatible feature additions
- **PATCH**: Backward-compatible bug fixes

### Automatic Deployment

After pushing the tag, the following are triggered automatically:

1. **CI/CD Pipeline**: Build and test via GitHub Actions
2. **Deployment**: Automatic deployment of `main` branch to AWS production environment
3. **Notification**: Deployment result notification

### Notes

- Create releases **only from the main branch**
- Complete **production environment verification** before releasing
- **Release notes are required** with clear description of changes
- Strictly follow **semantic versioning**
- **Release title is auto-generated** in version-only format
- **No user confirmation needed for title**
- **Include release date in the body**
- Use **`--latest` for regular releases and `--prerelease` for pre-releases**

## Language

- **All user-facing output, release notes, and descriptions must be written in Japanese(すべてのユーザーへの出力は日本語にしてください)**
