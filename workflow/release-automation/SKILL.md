---
name: release-automation
description: Automate plugin releases, versioning, and changelog management. Use when working with releases, semantic versioning, release workflows, version bumping, CHANGELOG creation, or release note generation. Critical for establishing release process from scratch.
---
<!-- docval:ignore-workflow-refs -->
<!-- docval:ignore-script-refs -->

# Release Automation Specialist

## Mission
Establish and automate a complete release process for the Qobuzarr project, implementing semantic versioning, automated changelog generation, and GitHub release workflows.

## Expertise Areas

### 1. Release Process Establishment
- Design release workflow from scratch
- Implement semantic versioning strategy
- Create version management system
- Establish changelog practices
- Define release checklist and procedures

### 2. Semantic Versioning
- Implement MAJOR.MINOR.PATCH versioning
- Handle pre-release versions (alpha, beta, rc)
- Coordinate version numbers across files
- Detect breaking changes for version bumps
- Manage version in single source of truth

### 3. Changelog Automation
- Create and maintain CHANGELOG.md
- Parse commit messages (conventional commits)
- Generate release notes from git history
- Categorize changes (features, fixes, breaking)
- Format release notes for GitHub releases

### 4. Release Workflow Creation
- Design GitHub Actions release workflow
- Implement automated release on tag push
- Add release validation and testing
- Create artifact packaging and publishing
- Handle manual release triggers

### 5. Artifact Management
- Package plugin as ZIP with proper structure
- Generate checksums for verification
- Implement artifact signing
- Attach assets to GitHub releases
- Version artifacts appropriately

## Current Project Context

### Qobuzarr Release Status
- **Current Status**: CRITICAL GAP - Manual release process only
- **Current Version**: 0.0.14
- **Existing Release Workflow**: release.yml (basic, manual notes)
- **Version File**: VERSION (exists)
- **Build System**: MSBuild with .NET 6.0
- **Package Format**: ZIP (Lidarr.Plugin.Qobuzarr-v{version}.zip)
- **Missing**: CHANGELOG.md, automated notes, signing, SBOM

### Critical Missing Components
1. **CHANGELOG.md** - No version history file
2. **Automated Release Notes** - Manual entry required
3. **Artifact Signing** - No signing implemented
4. **SBOM Generation** - No software bill of materials
5. **Version Automation** - Manual VERSION file updates
6. **Release Validation** - Minimal pre-release checks

### Key Files to Create/Maintain
- `CHANGELOG.md` - **CREATE** - Version history
- `.github/workflows/release.yml` - **ENHANCE** - Current basic workflow
- `.github/scripts/bump-version.ps1` - **CREATE** - Version management
- `.github/scripts/generate-release-notes.sh` - **CREATE** - Note automation
- `VERSION` - Existing single source of truth
- `Qobuzarr.csproj` - Update version automatically
- `plugin.json` - Update version automatically

## Best Practices

### Version Management Strategy
1. **Single Source of Truth**: VERSION file is canonical
2. **Automated Propagation**: Script updates all references
3. **Validation**: Workflow validates tag matches VERSION
4. **Version Locations to Sync**:
   - VERSION file
   - Qobuzarr.csproj (Version, FileVersion, AssemblyVersion)
   - plugin.json (version field)

### Release Process Design
1. **Pre-release Phase**:
   - Developer updates VERSION file
   - Developer updates CHANGELOG.md (or runs script)
   - Developer commits changes
   - Developer creates and pushes version tag

2. **Automated Release Phase** (GitHub Actions):
   - Extract version from tag
   - Validate tag matches VERSION file
   - Restore dependencies and build Release config
   - Run full test suite (mandatory)
   - Package plugin as ZIP
   - Generate checksums (SHA256)
   - Sign artifacts (Cosign or GPG)
   - Generate SBOM (SPDX format)
   - Generate release notes from CHANGELOG + commits
   - Create GitHub release
   - Attach artifacts
   - Update wiki/documentation

3. **Post-release Phase**:
   - Update latest tag
   - Notify users/community
   - Monitor for issues
   - Begin next version development

### Conventional Commits
Adopt conventional commit format for automated changelog:
```
feat: add new quality profile selection
fix: correct album search query encoding
docs: update installation instructions
chore: bump dependencies
test: add integration tests for search
perf: optimize caching layer
refactor: restructure download service
BREAKING CHANGE: remove deprecated search API
```

### CHANGELOG.md Format
```markdown
# Changelog

All notable changes to Qobuzarr will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-24

### Added
- ✨ Initial public release
- 🎵 Full Qobuz streaming integration
- 🔍 ML-powered search optimization (65.8% API reduction)
- 💾 Multi-layer caching (94.7% hit rate)
- 📊 Performance telemetry

### Fixed
- 🐛 Album metadata parsing for special characters
- 🔧 Download retry logic for transient failures

### Performance
- ⚡ Progressive search with fallback strategies
- ⚡ Reduced average search latency by 2.3 seconds

### Documentation
- 📝 Comprehensive API reference
- 📝 Deployment guide for Docker environments

## [0.0.14] - 2025-11-20

### Added
- Initial private beta release
```

### Release Notes Template
```markdown
## What's New in v0.1.0

### 🎉 First Public Release
Qobuzarr is now available for public testing! This plugin brings high-quality Qobuz streaming integration to Lidarr with advanced search capabilities.

### ✨ Features
- Full Qobuz API integration with authentication
- ML-powered query optimization reducing API calls by 65.8%
- Multi-layer caching system with 94.7% hit rate
- Progressive search with intelligent fallback
- Performance telemetry and monitoring

### 🐛 Bug Fixes
- Fixed album metadata parsing for albums with special characters
- Improved download retry logic for transient API failures

### ⚡ Performance
- Average search latency reduced by 2.3 seconds
- Optimized caching reduces API calls significantly

### 📝 Documentation
- Added comprehensive installation guide
- Added API reference documentation
- Added troubleshooting guide

### 🔒 Security
- Updated dependencies with latest security patches

**Full Changelog**: https://github.com/.../compare/v0.0.14...v0.1.0

---

## Installation

Download `Lidarr.Plugin.Qobuzarr-v0.1.0.zip` and extract to your Lidarr plugins directory.

See the [Installation Guide](docs/INSTALLATION.md) for detailed instructions.
```

## Commands & Scripts to Create

### 1. Version Bump Script
**File**: `.github/scripts/bump-version.ps1`
```powershell
# Bump version in VERSION, csproj, and plugin.json
param(
    [Parameter(Mandatory=$true)]
    [string]$Version
)
# Update VERSION file
# Update Qobuzarr.csproj
# Update plugin.json
# Validate format
```

### 2. Release Notes Generator
**File**: `.github/scripts/generate-release-notes.sh`
```bash
#!/bin/bash
# Extract CHANGELOG section for version
# Parse recent commits
# Format with emojis and categories
# Generate full changelog link
```

### 3. Tag Release Script
**File**: `.github/scripts/tag-release.sh`
```bash
#!/bin/bash
# Validate VERSION file
# Create annotated tag
# Push tag to origin
```

## Workflow Enhancement

### Enhanced release.yml Structure
```yaml
name: Release

on:
  push:
    tags:
      - 'v*.*.*'
  workflow_dispatch:
    inputs:
      version:
        description: 'Release version (e.g., 0.1.0)'
        required: true

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Validate version format
      - name: Check tag matches VERSION file
      - name: Verify CHANGELOG updated

  build-and-test:
    needs: validate
    runs-on: ubuntu-latest
    steps:
      - name: Setup environment
      - name: Restore and build
      - name: Run tests (mandatory)

  package:
    needs: build-and-test
    runs-on: ubuntu-latest
    steps:
      - name: Build Release configuration
      - name: Package plugin ZIP
      - name: Generate checksums
      - name: Sign artifacts
      - name: Generate SBOM

  release:
    needs: package
    runs-on: ubuntu-latest
    steps:
      - name: Generate release notes
      - name: Create GitHub release
      - name: Upload artifacts
      - name: Update documentation
```

## Implementation Roadmap

### Phase 1: Foundation (Immediate)
1. **Create CHANGELOG.md**:
   - Initialize with current version (0.0.14)
   - Add structure for unreleased changes
   - Document all changes since initial development

2. **Create Version Bump Script**:
   - Update VERSION file
   - Update Qobuzarr.csproj
   - Update plugin.json
   - Validate semantic version format

3. **Adopt Conventional Commits**:
   - Document in CONTRIBUTING.md
   - Add commit message linting (optional)

### Phase 2: Automation (High Priority)
4. **Enhance release.yml Workflow**:
   - Add validation job
   - Add comprehensive testing
   - Add CHANGELOG extraction
   - Add automated release notes

5. **Create Release Notes Generator**:
   - Parse CHANGELOG.md for current version
   - Parse git log for additional commits
   - Format with emojis and categories
   - Include full changelog link

6. **Implement Artifact Signing**:
   - Add Cosign keyless signing
   - Or add GPG signing
   - Document verification process

### Phase 3: Advanced Features (Medium Priority)
7. **Generate SBOM**:
   - Use Anchore or similar tool
   - Attach SPDX JSON to releases
   - Document dependency tree

8. **Add Release Validation**:
   - Pre-release checklist automation
   - Version consistency checks
   - Documentation currency checks

9. **Create Release Dashboard**:
   - Track release metrics
   - Monitor download counts
   - Track issue reports post-release

## Troubleshooting

### Manual Release Process (Current)
**Problem**: Currently requires manual release note writing
**Solution**: Follow implementation roadmap to automate

### Version Synchronization
**Problem**: VERSION, csproj, plugin.json can get out of sync
**Solution**: Create bump-version.ps1 script to update all at once

### Missing CHANGELOG
**Problem**: No version history tracked
**Solution**: Initialize CHANGELOG.md with historical versions

## Enhancement Opportunities

### Immediate Needs
1. **CHANGELOG.md Creation**: Critical for version tracking
2. **Version Automation**: Eliminate manual sync errors
3. **Release Notes**: Auto-generate from changelog + commits
4. **Artifact Signing**: Add security verification

### Future Enhancements
5. **Pre-release Channel**: Beta releases from develop branch
6. **Release Notifications**: Discord/Slack announcements
7. **Rollback Automation**: Quick revert process
8. **Release Analytics**: Track adoption and issues

## Related Skills
- `code-quality` - Ensure tests pass before release
- `artifact-manager` - Handle artifact lifecycle
- `deployment-manager` - Deploy releases to environments

## Examples

### Example 1: First Automated Release
**User**: "Set up automated releases for Qobuzarr"
**Action**:
1. Create CHANGELOG.md with historical entries
2. Create bump-version.ps1 script
3. Create generate-release-notes.sh script
4. Enhance release.yml workflow
5. Document release process in CONTRIBUTING.md
6. Test with beta release

### Example 2: Create Release for v0.1.0
**User**: "Release version 0.1.0"
**Action**:
1. Run `./scripts/bump-version.ps1 -Version "0.1.0"`
2. Update CHANGELOG.md with finalized changes
3. Commit: `git commit -m "chore: release v0.1.0"`
4. Tag: `git tag -a v0.1.0 -m "Release 0.1.0"`
5. Push: `git push origin v0.1.0`
6. Monitor release workflow
7. Verify GitHub release created with notes

### Example 3: Fix Failed Release
**User**: "The release workflow failed on tests"
**Action**:
1. Review test failure logs
2. Fix failing tests
3. Commit fix
4. Delete failed tag: `git tag -d v0.1.0 && git push origin :refs/tags/v0.1.0`
5. Re-create tag after fix
6. Re-trigger release
