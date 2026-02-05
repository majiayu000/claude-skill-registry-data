---
name: git.release.prep
description: Prepare releases with semantic versioning, changelog generation, git tags, GitHub releases, and deployment bundle creation.
---

# git.release.prep

## Purpose

This skill automates release preparation for Carbon ACX by:
- Determining next version using semantic versioning (semver)
- Generating/updating CHANGELOG with categorized changes
- Creating annotated git tags
- Generating GitHub release notes
- Building deployment bundles (`make package` or equivalent)
- Verifying builds succeed before tagging
- Publishing GitHub releases with artifacts

## When to Use

**Trigger Patterns:**
- "Prepare a release"
- "Create release v1.2.3"
- "Tag a new version"
- "Publish a release"
- After merging significant features to main
- When ready to deploy new dataset version (ACX042, etc.)

**Do NOT Use When:**
- Still in active development (not ready to release)
- Tests are failing
- Build is broken
- On a feature branch (releases should be from main/master)

## Allowed Tools

- `bash` - Git commands, build commands, gh CLI
- `read_file` - Read CHANGELOG, version files, package.json
- `write_file` - Update CHANGELOG, version files
- `edit_file` - Modify existing CHANGELOG entries

**Access Level:** 3 (Can modify files, create tags, publish releases)

**Tool Rationale:**
- `bash`: Required for git tagging, building, gh CLI
- `read_file`: Read current versions and changelogs
- `write_file`/`edit_file`: Update version files and changelog

**Explicitly Denied:**
- No force pushing tags
- No deleting existing tags without explicit approval
- No deploying to production (separate deployment workflow)

## Expected I/O

**Input:**
- Type: Release preparation request
- Context: Branch ready for release (usually main/master)
- Optional: Version number (e.g., "v1.2.3" or "ACX042")
- Optional: Release type (major, minor, patch)

**Example:**
```
"Prepare release v1.3.0"
"Create a patch release"
"Tag dataset version ACX042"
```

**Output:**
- Type: Release prepared and published
- Format: Git tag + GitHub release URL
- Includes:
  - Version number used
  - CHANGELOG updates
  - Build artifacts bundled
  - GitHub release created
  - Next steps (deployment instructions)

**Validation:**
- Version follows semver (MAJOR.MINOR.PATCH)
- CHANGELOG updated with categorized changes
- Build succeeds before tagging
- Git tag created and pushed
- GitHub release published with notes

## Dependencies

**Required:**
- Git repository on main/master branch
- `gh` CLI installed and authenticated
- Build system working (`make package` or equivalent)
- CHANGELOG file exists (or will be created)

**Optional:**
- `package.json` for Node.js version (web apps)
- `pyproject.toml` for Python version (calc engine)
- `calc/outputs/sprint_status.txt` for dataset versions

**Carbon ACX Specifics:**
- Dataset releases use `ACX###` format (ACX041, ACX042, etc.)
- Code releases use semver `vMAJOR.MINOR.PATCH`
- Both may happen in single release

## Workflow

### Step 1: Determine Current Version

Check multiple sources:
```bash
# Git tags
git describe --tags --abbrev=0 2>/dev/null

# package.json (if exists)
cat package.json | grep '"version"'

# pyproject.toml (if exists)
cat pyproject.toml | grep '^version'

# Dataset version
cat calc/outputs/sprint_status.txt 2>/dev/null
```

**Parse version:** Extract MAJOR.MINOR.PATCH
**Examples:**
- `v1.2.3` → major=1, minor=2, patch=3
- `ACX041` → dataset version 41

### Step 2: Determine Next Version

**Semantic Versioning Rules:**
- **MAJOR** (v2.0.0): Breaking changes, incompatible API changes
- **MINOR** (v1.3.0): New features, backwards-compatible
- **PATCH** (v1.2.4): Bug fixes, backwards-compatible

**Heuristic (if user doesn't specify):**
1. Check commits since last release:
   ```bash
   git log v1.2.3...HEAD --oneline
   ```
2. Analyze commit types:
   - Any `BREAKING CHANGE:` or `!` → MAJOR
   - Any `feat:` commits → MINOR
   - Only `fix:`, `chore:`, `docs:` → PATCH

**Dataset Versions:**
- Increment by 1: ACX041 → ACX042
- Update `calc/outputs/sprint_status.txt`

**User can override:** "Create major release v2.0.0"

### Step 3: Generate CHANGELOG

**Read commits since last release:**
```bash
git log v1.2.3...HEAD --pretty=format:"%s (%h)"
```

**Categorize commits:**
- **Features:** `feat:` commits
- **Fixes:** `fix:` commits
- **Chores:** `chore:`, `refactor:`, `style:`, `perf:`
- **Documentation:** `docs:` commits
- **Breaking Changes:** Any with `BREAKING CHANGE:` or `!`

**CHANGELOG format (append to existing file):**
```markdown
## [1.3.0] - 2025-10-24

### Features
- Add dark mode toggle to dashboard (a1b2c3d)
- Implement emission chart component (d4e5f6g)
- Support CSV export for reports (g7h8i9j)

### Fixes
- Correct aviation emission factor calculation (j0k1l2m)
- Fix responsive layout on mobile (n3o4p5q)

### Chores
- Update React to 18.3.1 (r6s7t8u)
- Refactor component directory structure (v9w0x1y)

### Documentation
- Add theming guide to docs (z2a3b4c)
```

**If CHANGELOG doesn't exist, create with header:**
```markdown
# Changelog

All notable changes to Carbon ACX will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.3.0] - 2025-10-24
...
```

### Step 4: Update Version Files

**package.json (if exists):**
```json
{
  "version": "1.3.0"
}
```

**pyproject.toml (if exists):**
```toml
[tool.poetry]
version = "1.3.0"
```

**calc/outputs/sprint_status.txt (dataset):**
```
ACX042
```

**Commit version updates:**
```bash
git add CHANGELOG.md package.json pyproject.toml calc/outputs/sprint_status.txt
git commit -m "chore: prepare release v1.3.0

Updates version files and CHANGELOG for v1.3.0 release.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 5: Build and Verify

```bash
# Run build
make build || pnpm build

# Run tests
make validate || pnpm test

# Create deployment bundle
make package
```

**Verification:**
- ✅ Build succeeds without errors
- ✅ Tests pass
- ✅ Package created in `dist/` or equivalent

**If build fails:** Stop, report error, do NOT create tag

### Step 6: Create Git Tag

**Annotated tag with message:**
```bash
git tag -a v1.3.0 -m "Release v1.3.0

Features:
- Dark mode toggle
- Emission chart component
- CSV export

Fixes:
- Aviation emission factor calculation
- Mobile responsive layout

See CHANGELOG.md for full details."
```

**Push tag:**
```bash
git push origin v1.3.0
```

**Also push commit:**
```bash
git push origin main
```

### Step 7: Create GitHub Release

**Generate release notes from CHANGELOG:**
Extract the section for this version from CHANGELOG.md

**Create release with gh CLI:**
```bash
gh release create v1.3.0 \
  --title "Release v1.3.0" \
  --notes "$(cat <<'EOF'
## Features
- Add dark mode toggle to dashboard
- Implement emission chart component
- Support CSV export for reports

## Fixes
- Correct aviation emission factor calculation
- Fix responsive layout on mobile

## Chores
- Update React to 18.3.1
- Refactor component directory structure

## Documentation
- Add theming guide to docs

See [CHANGELOG.md](https://github.com/owner/carbon-acx/blob/main/CHANGELOG.md) for full details.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Attach artifacts (if applicable):**
```bash
gh release upload v1.3.0 dist/site.tar.gz dist/artifacts.zip
```

### Step 8: Report Success

**Output to user:**
```
✅ Release v1.3.0 Prepared

Version: v1.3.0 (from v1.2.3)
Type: Minor release
Commits: 12 commits since last release

Changes:
- 4 features
- 2 bug fixes
- 3 chores
- 1 documentation update

Artifacts:
✅ CHANGELOG.md updated
✅ Version files updated
✅ Build succeeded
✅ Tests passed
✅ Git tag created: v1.3.0
✅ Tag pushed to origin
✅ GitHub release created

Release URL: https://github.com/owner/carbon-acx/releases/tag/v1.3.0

Next Steps:
- Deploy to staging: [deployment command]
- Test in staging environment
- Deploy to production when ready
- Announce release to users
```

## Examples

### Example 1: Minor Release

**User:** "Prepare release v1.3.0"

**Claude Process:**
1. Verify current version: v1.2.3 (from git tags)
2. Analyze commits: 12 commits with feat, fix, chore types
3. Generate CHANGELOG section for v1.3.0
4. Update package.json version to 1.3.0
5. Commit version updates
6. Run `make build` - succeeds ✅
7. Run `make validate` - passes ✅
8. Create tag: `git tag -a v1.3.0 -m "..."`
9. Push tag: `git push origin v1.3.0`
10. Create GitHub release with notes
11. Attach `dist/site.tar.gz` as artifact
12. Report success with URL

### Example 2: Patch Release

**User:** "Create a patch release"

**Claude Process:**
1. Current version: v1.2.3
2. Analyze commits: Only bug fixes, no features
3. Next version: v1.2.4 (patch bump)
4. Generate CHANGELOG:
   ```markdown
   ## [1.2.4] - 2025-10-24

   ### Fixes
   - Fix memory leak in chart rendering (a1b2c3d)
   - Correct date formatting in reports (d4e5f6g)
   ```
5. Update version files to 1.2.4
6. Build and test
7. Tag v1.2.4
8. Create GitHub release
9. Report: "Patch release v1.2.4 created"

### Example 3: Major Release (Breaking Changes)

**User:** "Prepare major release v2.0.0"

**Claude Process:**
1. Current version: v1.5.3
2. User specified MAJOR bump
3. Check commits for breaking changes:
   ```
   feat!: redesign API endpoints
   BREAKING CHANGE: /api/v1/* endpoints removed
   ```
4. Generate CHANGELOG with prominent breaking changes section:
   ```markdown
   ## [2.0.0] - 2025-10-24

   ### ⚠️ BREAKING CHANGES
   - API endpoints redesigned - /api/v1/* removed
   - Minimum Node.js version now 20.x
   - CSV schema updated - requires migration

   ### Features
   - New API v2 with improved performance
   - GraphQL support

   ### Migration Guide
   See docs/MIGRATION_v2.md for upgrade instructions
   ```
5. Update version to 2.0.0
6. Build and test thoroughly
7. Tag v2.0.0 with detailed message
8. Create GitHub release marking as major version
9. Warn user: "This is a MAJOR release with breaking changes"

### Example 4: Dataset Release

**User:** "Tag dataset version ACX042"

**Claude Process:**
1. Read current dataset version: ACX041
2. Next version: ACX042
3. Update `calc/outputs/sprint_status.txt` to ACX042
4. Check what data changed:
   ```bash
   git diff ACX041...HEAD -- data/
   ```
5. Generate dataset-specific CHANGELOG:
   ```markdown
   ## Dataset ACX042 - 2025-10-24

   ### Data Updates
   - Updated grid intensity factors for Q4 2024
   - Added 15 new activities in professional services layer
   - Corrected emission factors for aviation (long-haul)

   ### Schema Changes
   - Added `data_vintage` column to emission_factors.csv

   ### Validation
   - All integrity checks pass
   - Manifest hashes regenerated
   ```
6. Rebuild dataset: `make build`
7. Tag: `git tag -a ACX042 -m "Dataset release ACX042"`
8. Create GitHub release with dataset artifacts
9. Attach manifest files

### Example 5: Combined Code + Dataset Release

**User:** "Prepare release with code v1.4.0 and dataset ACX042"

**Claude Process:**
1. Dual versioning:
   - Code: v1.3.1 → v1.4.0
   - Dataset: ACX041 → ACX042
2. Generate combined CHANGELOG:
   ```markdown
   ## [v1.4.0 / ACX042] - 2025-10-24

   ### Code Changes
   #### Features
   - Add new visualization for grid intensity

   ### Dataset Changes
   - Dataset version ACX041 → ACX042
   - Updated grid intensity factors
   - Added 15 new activities
   ```
3. Update both version files
4. Rebuild everything: `make build && make package`
5. Create tag: `v1.4.0-ACX042`
6. GitHub release notes include both code and data changes
7. Attach both code bundle and dataset artifacts

## Limitations

**Scope Limitations:**
- Cannot automatically deploy to production (separate process)
- Cannot delete or modify existing releases without approval
- Cannot create releases on branches other than main/master
- Requires manual verification that changes are release-ready

**Known Edge Cases:**
- First release (no previous tags) → Start at v1.0.0 or v0.1.0
- Unreleased commits on main → Ask user if intentional or accidental
- Build failures → Stop process, report error, do NOT tag
- Conflicting version numbers → Ask user which to use

**Performance Constraints:**
- Large builds (webpack, packaging) may take 2-5 minutes
- Many commits (100+) slow CHANGELOG generation
- Large artifacts may fail to upload (GitHub limit: 2GB per file)

**Security Boundaries:**
- Does not auto-approve releases (human must verify)
- Does not skip tests or builds
- Does not force push tags
- Respects branch protection rules

## Validation Criteria

**Success Metrics:**
- ✅ Version follows semver (or dataset versioning)
- ✅ CHANGELOG updated with categorized changes
- ✅ Version files updated consistently
- ✅ Build succeeded before tagging
- ✅ Tests passed before tagging
- ✅ Git tag created with proper message
- ✅ Tag pushed to remote
- ✅ GitHub release created with notes
- ✅ Artifacts attached (if applicable)
- ✅ User informed of release URL

**Failure Modes:**
- ❌ Build fails → Stop, report error, do NOT tag
- ❌ Tests fail → Stop, suggest fixing tests first
- ❌ Not on main/master → Warn, suggest merging to main first
- ❌ Uncommitted changes → Ask user to commit or stash
- ❌ Tag already exists → Ask if should overwrite or increment

**Recovery:**
- If build fails: Report error logs, suggest fixes
- If tag conflicts: Suggest alternative version number
- If GitHub release fails: Provide manual creation instructions
- If uncertain about version bump: Ask user to specify

## Related Skills

**Composes With:**
- `git.commit.smart` - Commit version updates before tagging
- `git.pr.create` - Create release PR for review before tagging
- `carbon.data.qa` - Verify dataset changes before release

**Dependencies:**
- Git repository on releasable branch
- Build system functional

**Alternative Skills:**
- For commits: `git.commit.smart`
- For PRs: `git.pr.create`

## Maintenance

**Owner:** Workspace Team (shared skill)
**Review Cycle:** Quarterly (or before each major release)
**Last Updated:** 2025-10-24
**Version:** 1.0.0

**Maintenance Notes:**
- Update CHANGELOG format if Carbon ACX adopts different style
- Adjust semver rules if project changes versioning scheme
- Review artifact packaging as build process evolves
- Keep dataset versioning logic synchronized with actual practice
