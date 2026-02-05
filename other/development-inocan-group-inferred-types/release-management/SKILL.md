---
name: release-management
description: Manage GitHub releases - create releases, upload assets, manage tags, and generate release notes using gh CLI
---
# GitHub Release Management Skill

This skill provides operations for managing GitHub releases, including creating releases, uploading assets, managing tags, and distributing software versions.

## Available Operations

### 1. Create Release
Create a new release with tag, title, and release notes.

### 2. List Releases
View all releases in a repository.

### 3. View Release
Get details about a specific release.

### 4. Edit Release
Update release information.

### 5. Delete Release
Remove a release (keeps the tag).

### 6. Upload Assets
Add files to a release.

### 7. Download Assets
Download release assets.

### 8. Delete Assets
Remove assets from a release.

### 9. Manage Tags
Create and manage Git tags for releases.

## Usage Examples

### Create Release

**Create release from tag:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --notes "Initial release with core features"
```

**Create with auto-generated notes:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --generate-notes
```

**Create from notes file:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --notes-file CHANGELOG.md
```

**Create pre-release:**
```bash
gh release create v2.0.0-beta.1 --repo owner/repo-name \
  --title "Version 2.0.0 Beta 1" \
  --notes "Beta release for testing" \
  --prerelease
```

**Create draft release:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --notes "Release draft" \
  --draft
```

**Create with assets:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --notes "Release with binaries" \
  dist/app-linux-x64.tar.gz \
  dist/app-macos-x64.tar.gz \
  dist/app-windows-x64.zip
```

**Create on specific branch/commit:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --notes "Release notes" \
  --target main
```

**Latest release:**
```bash
gh release create v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0" \
  --notes "Latest stable release" \
  --latest
```

### List Releases

**List all releases:**
```bash
gh release list --repo owner/repo-name
```

**Limit results:**
```bash
gh release list --repo owner/repo-name --limit 10
```

**Exclude drafts:**
```bash
gh release list --repo owner/repo-name --exclude-drafts
```

**Exclude pre-releases:**
```bash
gh release list --repo owner/repo-name --exclude-pre-releases
```

**JSON output:**
```bash
gh release list --repo owner/repo-name --json tagName,name,publishedAt,isPrerelease,isDraft
```

**Using API:**
```bash
gh api repos/owner/repo-name/releases --jq '.[] | {tag: .tag_name, name: .name, published: .published_at}'
```

### View Release

**View latest release:**
```bash
gh release view --repo owner/repo-name
```

**View specific release:**
```bash
gh release view v1.0.0 --repo owner/repo-name
```

**View in browser:**
```bash
gh release view v1.0.0 --repo owner/repo-name --web
```

**JSON output:**
```bash
gh release view v1.0.0 --repo owner/repo-name --json tagName,name,body,assets,publishedAt
```

**View assets:**
```bash
gh release view v1.0.0 --repo owner/repo-name --json assets --jq '.assets[] | {name, size, download_count}'
```

### Edit Release

**Update title and notes:**
```bash
gh release edit v1.0.0 --repo owner/repo-name \
  --title "Version 1.0.0 - Updated" \
  --notes "Updated release notes"
```

**Update from file:**
```bash
gh release edit v1.0.0 --repo owner/repo-name \
  --notes-file RELEASE_NOTES.md
```

**Mark as latest:**
```bash
gh release edit v1.0.0 --repo owner/repo-name --latest
```

**Mark as pre-release:**
```bash
gh release edit v1.0.0 --repo owner/repo-name --prerelease
```

**Publish draft:**
```bash
gh release edit v1.0.0 --repo owner/repo-name --draft=false
```

**Change to draft:**
```bash
gh release edit v1.0.0 --repo owner/repo-name --draft
```

**Update discussion category:**
```bash
gh release edit v1.0.0 --repo owner/repo-name --discussion-category announcements
```

### Delete Release

**Delete release (keeps tag):**
```bash
gh release delete v1.0.0 --repo owner/repo-name
```

**Delete with confirmation:**
```bash
gh release delete v1.0.0 --repo owner/repo-name --yes
```

**Delete and cleanup tag:**
```bash
gh release delete v1.0.0 --repo owner/repo-name --yes
git push --delete origin v1.0.0  # Delete remote tag
```

### Upload Assets

**Upload single file:**
```bash
gh release upload v1.0.0 dist/app.tar.gz --repo owner/repo-name
```

**Upload multiple files:**
```bash
gh release upload v1.0.0 --repo owner/repo-name \
  dist/app-linux.tar.gz \
  dist/app-macos.tar.gz \
  dist/app-windows.zip
```

**Upload with glob pattern:**
```bash
gh release upload v1.0.0 dist/*.tar.gz --repo owner/repo-name
```

**Overwrite existing asset:**
```bash
gh release upload v1.0.0 dist/app.tar.gz --repo owner/repo-name --clobber
```

**Using API:**
```bash
# Get upload URL
UPLOAD_URL=$(gh api repos/owner/repo-name/releases/tags/v1.0.0 --jq '.upload_url' | sed 's/{?name,label}//')

# Upload asset
gh api "$UPLOAD_URL?name=app.tar.gz" \
  -X POST \
  -H "Content-Type: application/gzip" \
  --input dist/app.tar.gz
```

### Download Assets

**Download all assets:**
```bash
gh release download v1.0.0 --repo owner/repo-name
```

**Download specific asset:**
```bash
gh release download v1.0.0 --repo owner/repo-name --pattern "*.tar.gz"
```

**Download to directory:**
```bash
gh release download v1.0.0 --repo owner/repo-name --dir downloads/
```

**Download latest release:**
```bash
gh release download --repo owner/repo-name
```

**Download with pattern matching:**
```bash
gh release download v1.0.0 --repo owner/repo-name --pattern "*linux*"
```

**Using API to get download URL:**
```bash
# Get asset URL
gh api repos/owner/repo-name/releases/tags/v1.0.0 --jq '.assets[] | {name, browser_download_url}'

# Download with curl
ASSET_URL=$(gh api repos/owner/repo-name/releases/tags/v1.0.0 --jq '.assets[0].browser_download_url')
curl -L -o app.tar.gz "$ASSET_URL"
```

### Delete Assets

**Using API to delete asset:**
```bash
# Get asset ID
ASSET_ID=$(gh api repos/owner/repo-name/releases/tags/v1.0.0 --jq '.assets[] | select(.name=="app.tar.gz") | .id')

# Delete asset
gh api repos/owner/repo-name/releases/assets/$ASSET_ID -X DELETE
```

**Delete and re-upload:**
```bash
# Delete old asset
ASSET_ID=$(gh api repos/owner/repo-name/releases/tags/v1.0.0 --jq '.assets[] | select(.name=="app.tar.gz") | .id')
gh api repos/owner/repo-name/releases/assets/$ASSET_ID -X DELETE

# Upload new version
gh release upload v1.0.0 dist/app.tar.gz --repo owner/repo-name
```

### Manage Tags

**Create tag:**
```bash
cd repo-name
git tag -a v1.0.0 -m "Version 1.0.0"
git push origin v1.0.0
```

**List tags:**
```bash
cd repo-name
git tag -l
```

**View tag details:**
```bash
cd repo-name
git show v1.0.0
```

**Delete tag:**
```bash
cd repo-name
git tag -d v1.0.0  # Delete local
git push --delete origin v1.0.0  # Delete remote
```

**Create tag from specific commit:**
```bash
cd repo-name
git tag -a v1.0.0 abc123def -m "Version 1.0.0"
git push origin v1.0.0
```

## Common Patterns

### Standard Release Workflow

```bash
# 1. Prepare release
VERSION="v1.2.0"
cd repo-name

# 2. Update version files
echo "1.2.0" > VERSION
git add VERSION
git commit -m "Bump version to 1.2.0"
git push

# 3. Create and push tag
git tag -a $VERSION -m "Release $VERSION"
git push origin $VERSION

# 4. Build release artifacts
npm run build  # or your build command
mkdir -p dist

# 5. Create release with artifacts
gh release create $VERSION \
  --title "Release $VERSION" \
  --generate-notes \
  dist/*.tar.gz \
  dist/*.zip
```

### Pre-release to Stable

```bash
# 1. Create pre-release
gh release create v2.0.0-rc.1 --repo owner/repo-name \
  --title "Release Candidate 1" \
  --notes "Testing release" \
  --prerelease \
  dist/*

# 2. After testing, promote to stable
gh release edit v2.0.0-rc.1 --repo owner/repo-name \
  --prerelease=false \
  --latest

# 3. Or create new stable release
gh release create v2.0.0 --repo owner/repo-name \
  --title "Version 2.0.0" \
  --notes "Stable release" \
  dist/*
```

### Draft Release for Review

```bash
# 1. Create draft
gh release create v1.5.0 --repo owner/repo-name \
  --title "Version 1.5.0" \
  --notes-file CHANGELOG.md \
  --draft \
  dist/*

# 2. Review in browser
gh release view v1.5.0 --repo owner/repo-name --web

# 3. Publish when ready
gh release edit v1.5.0 --repo owner/repo-name --draft=false
```

### Multi-Platform Release

```bash
VERSION="v1.0.0"

# Build for all platforms
./build-linux.sh
./build-macos.sh
./build-windows.sh

# Create release with all platform binaries
gh release create $VERSION --repo owner/repo-name \
  --title "Version 1.0.0 - Multi-platform" \
  --notes "Available for Linux, macOS, and Windows" \
  dist/app-linux-amd64.tar.gz \
  dist/app-linux-arm64.tar.gz \
  dist/app-darwin-amd64.tar.gz \
  dist/app-darwin-arm64.tar.gz \
  dist/app-windows-amd64.zip \
  dist/app-windows-arm64.zip
```

### Automated Release with GitHub Actions

```bash
# Trigger release workflow (example)
gh workflow run release.yml --repo owner/repo-name \
  -f version=1.2.0 \
  -f prerelease=false

# Monitor release workflow
gh run watch $(gh run list --workflow release.yml --limit 1 --json databaseId --jq '.[0].databaseId')
```

### Rollback Release

```bash
# 1. Delete problematic release
gh release delete v1.2.0 --repo owner/repo-name --yes

# 2. Delete tag
git push --delete origin v1.2.0

# 3. Mark previous version as latest
gh release edit v1.1.0 --repo owner/repo-name --latest
```

### Generate Release Notes from Commits

```bash
VERSION="v1.3.0"
PREV_VERSION="v1.2.0"

# Get commits since last release
git log $PREV_VERSION..HEAD --pretty=format:"- %s (%h)" > release_notes.txt

# Create release
gh release create $VERSION --repo owner/repo-name \
  --title "Release $VERSION" \
  --notes-file release_notes.txt \
  dist/*
```

### Download Latest Release for Installation

```bash
# Script to download and install latest release
REPO="owner/repo-name"

# Get latest release tag
LATEST=$(gh release view --repo $REPO --json tagName --jq '.tagName')

# Download release assets
gh release download $LATEST --repo $REPO --pattern "*linux*"

# Extract and install
tar -xzf app-linux-*.tar.gz
sudo mv app /usr/local/bin/
```

## Advanced Usage

### Release Statistics

**View download counts:**
```bash
gh api repos/owner/repo-name/releases --jq '.[] | {
  tag: .tag_name,
  downloads: [.assets[].download_count] | add
}'
```

**Most popular release:**
```bash
gh api repos/owner/repo-name/releases --jq 'map({
  tag: .tag_name,
  downloads: [.assets[].download_count] | add
}) | sort_by(.downloads) | reverse | .[0]'
```

**Asset-level statistics:**
```bash
gh release view v1.0.0 --repo owner/repo-name --json assets --jq '.assets[] | {
  name,
  size,
  downloads: .download_count
} | sort_by(.downloads) | reverse'
```

### Bulk Release Management

**List all tags without releases:**
```bash
# Get all tags
ALL_TAGS=$(git tag)

# Get tags with releases
RELEASE_TAGS=$(gh release list --repo owner/repo-name --limit 1000 --json tagName --jq '.[].tagName')

# Find difference
comm -23 <(echo "$ALL_TAGS" | sort) <(echo "$RELEASE_TAGS" | sort)
```

**Delete old pre-releases:**
```bash
gh api repos/owner/repo-name/releases --jq '.[] | select(.prerelease==true) | select(.created_at < "2024-01-01") | .tag_name' | \
  while read tag; do
    echo "Deleting $tag"
    gh release delete $tag --repo owner/repo-name --yes
  done
```

### Custom Release Notes Template

```bash
# Create release notes from template
cat > release_notes.md << EOF
## What's Changed

$(git log v1.0.0..v1.1.0 --pretty=format:"- %s by @%an" | grep -v "Merge pull request")

## New Contributors

$(git log v1.0.0..v1.1.0 --pretty=format:"%an" | sort -u | sed 's/^/* @/')

**Full Changelog**: https://github.com/owner/repo-name/compare/v1.0.0...v1.1.0
EOF

gh release create v1.1.0 --notes-file release_notes.md
```

## Error Handling

### Tag Already Exists
```bash
# Check if tag exists
git tag -l v1.0.0

# Delete and recreate if needed
git tag -d v1.0.0
git push --delete origin v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

### Release Already Exists
```bash
# Check if release exists
gh release view v1.0.0 --repo owner/repo-name 2>&1 | grep -q "release not found" || echo "Release exists"

# Delete and recreate
gh release delete v1.0.0 --repo owner/repo-name --yes
gh release create v1.0.0 --title "Version 1.0.0" --notes "Release notes"
```

### Asset Upload Failures
```bash
# Verify asset exists locally
[ -f dist/app.tar.gz ] && echo "File exists" || echo "File not found"

# Check file size (GitHub limit is 2GB per asset)
ls -lh dist/app.tar.gz

# Retry upload
gh release upload v1.0.0 dist/app.tar.gz --repo owner/repo-name --clobber
```

## Best Practices

1. **Use semantic versioning**: Follow vX.Y.Z format (e.g., v1.2.3)
2. **Write meaningful notes**: Include what changed, breaking changes, and upgrade instructions
3. **Use draft releases**: Review before publishing
4. **Tag commits properly**: Create annotated tags with messages
5. **Include checksums**: Provide SHA256 checksums for assets
6. **Test pre-releases**: Use beta/rc releases for testing
7. **Clean naming**: Use consistent asset naming conventions
8. **Keep releases focused**: One release per version
9. **Link to documentation**: Include links to docs in release notes
10. **Archive old releases**: Delete very old pre-releases to reduce clutter

## Semantic Versioning

- **Major (X.0.0)**: Breaking changes
- **Minor (1.X.0)**: New features, backwards compatible
- **Patch (1.2.X)**: Bug fixes, backwards compatible
- **Pre-release**: v1.2.0-alpha.1, v1.2.0-beta.1, v1.2.0-rc.1

## Integration with Other Skills

- Use `workflow-management` to automate releases with GitHub Actions
- Use `issue-management` to reference issues fixed in release
- Use `pull-request-management` to include PR links in notes
- Use `commit-operations` to generate changelog from commits

## References

- [GitHub CLI Release Documentation](https://cli.github.com/manual/gh_release)
- [GitHub Releases Guide](https://docs.github.com/en/repositories/releasing-projects-on-github)
- [Semantic Versioning](https://semver.org/)
- [GitHub Releases API](https://docs.github.com/en/rest/releases)
