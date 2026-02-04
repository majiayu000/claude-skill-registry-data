---
name: release-publishing-workflow
description: "Complete release workflow including version updates, CHANGELOG management, npm publishing, git tagging, and deployment verification. Use when releasing new versions or publishing packages."
---

# Release Publishing Workflow for @j0kz/mcp-agents

Complete workflow for releasing and publishing new versions across the monorepo.

## When to Use This Skill

- Releasing new package versions
- Publishing to npm
- Updating version.json and CHANGELOG
- Creating git tags
- Multi-platform deployment verification
- Emergency hotfix releases

## Evidence Base

**Current State:**
- version.json as single source of truth
- 25+ releases documented in CHANGELOG.md
- Multi-package publishing (9 tools + shared + installer)
- Automated version synchronization
- Platform verification (npm, GitHub)
- Emergency rollback procedures

---

## Quick Release Checklist

**Pre-release validation:**
- [ ] All tests passing (`npm test`)
- [ ] Build successful (`npm run build`)
- [ ] Version alignment check (`npm run version:check-shared`)
- [ ] CHANGELOG updated with release notes
- [ ] All PRs merged to main

**Release steps:**
- [ ] Update version.json
- [ ] Run `npm run version:sync`
- [ ] Update CHANGELOG.md
- [ ] Commit changes
- [ ] Publish: `npm run publish-all`
- [ ] Create git tag
- [ ] Push tag to GitHub
- [ ] Verify deployment

**For complete checklist:** See [references/complete-release-checklist.md](references/complete-release-checklist.md)

---

## version.json (Single Source of Truth)

**Location:** `version.json` (root)

**Format:**
```json
{
  "version": "1.0.36",
  "sharedVersion": "1.0.36"
}
```

**Update version:**
```bash
# 1. Edit version.json
{
  "version": "1.0.37",
  "sharedVersion": "1.0.37"
}

# 2. Sync all package.json files
npm run version:sync
```

**This updates:**
- All package.json files (11 packages)
- README badges
- tools.json metadata

---

## CHANGELOG Management

**Add release entry:**
```markdown
## [1.0.37] - 2025-10-XX

### 🎉 New Features / 🐛 Bug Fixes

**Key Changes:**
- Feature/Fix 1: Description
- Feature/Fix 2: Description

**Impact:**
- ✅ Benefit 1
- ✅ Benefit 2

**Test Results:**
- ✅ 388/388 tests passing
- ✅ Build successful

**Breaking Changes:** None

---
```

**For CHANGELOG templates:** See [references/complete-release-checklist.md](references/complete-release-checklist.md)

---

## Publishing Workflow

### 1. Pre-Release Validation

```bash
# All tests must pass
npm test

# Build must succeed
npm run build

# Version alignment check
npm run version:check-shared

# Update test count if changed
npm run update:test-count
```

---

### 2. Update Version

```bash
# Edit version.json
vim version.json
# Change: "version": "1.0.37"

# Sync all packages
npm run version:sync
```

---

### 3. Update CHANGELOG

```bash
vim CHANGELOG.md
# Add new release entry at top
```

---

### 4. Commit Version Bump

```bash
git add version.json CHANGELOG.md package.json packages/*/package.json tools.json README.md packages/*/README.md
git commit -m "chore: bump version to 1.0.37

Updated:
- version.json
- All package.json files
- CHANGELOG.md with release notes
- README badges

🤖 Generated with [Claude Code](https://claude.com/claude-code)
Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

### 5. Publish to npm

```bash
# Publish all packages at once
npm run publish-all

# Or individually:
npm publish packages/smart-reviewer --access public
npm publish packages/test-generator --access public
# ... etc
```

**Expected output:**
```
+ @j0kz/smart-reviewer-mcp@1.0.37
+ @j0kz/test-generator-mcp@1.0.37
+ @j0kz/orchestrator-mcp@1.0.37
...
✓ 11 packages published successfully
```

---

### 6. Create Git Tag

```bash
# Create annotated tag
git tag -a v1.0.37 -m "Release v1.0.37

- Feature 1
- Feature 2
- Bug fix 1

See CHANGELOG.md for full details"

# Push tag to GitHub
git push origin v1.0.37

# Or push all tags
git push --tags
```

---

### 7. Verify Deployment

**Check npm:**
```bash
npm view @j0kz/smart-reviewer-mcp version
# Should show: 1.0.37

npm view @j0kz/orchestrator-mcp version
# Should show: 1.0.37
```

**Check GitHub:**
```
https://github.com/j0kz/mcp-agents/releases
# Tag should appear
```

**Test installation:**
```bash
npx @j0kz/mcp-agents@latest
# Should install v1.0.37
```

---

## Emergency Hotfix Release

**Quick hotfix for critical bugs:**

```bash
# 1. Create hotfix branch
git checkout -b hotfix/critical-fix

# 2. Make minimal fix
# ... edit code ...
npm test  # Verify fix

# 3. Update version (patch)
# version.json: 1.0.37 → 1.0.38
npm run version:sync

# 4. Update CHANGELOG
# Add hotfix entry

# 5. Commit
git add .
git commit -m "fix: critical security patch"

# 6. Merge to main
git checkout main
git merge hotfix/critical-fix

# 7. Publish immediately
npm run publish-all

# 8. Tag and push
git tag -a v1.0.38 -m "Hotfix: Critical security patch"
git push origin main --tags
```

**For emergency procedures:** See [references/emergency-rollback-procedures.md](references/emergency-rollback-procedures.md)

---

## Common Workflows

### Standard Feature Release

```bash
# 1. Validation
npm test && npm run build

# 2. Version bump
# Edit version.json: 1.0.36 → 1.0.37
npm run version:sync

# 3. CHANGELOG
# Add release entry

# 4. Commit
git add .
git commit -m "chore: bump version to 1.0.37"

# 5. Publish
npm run publish-all

# 6. Tag
git tag -a v1.0.37 -m "Release v1.0.37"
git push origin v1.0.37

# 7. Verify
npm view @j0kz/smart-reviewer-mcp version
```

---

### Major Version Release (Breaking Changes)

```bash
# 1. Update version.json
# 1.0.37 → 2.0.0

# 2. Sync
npm run version:sync

# 3. CHANGELOG with migration guide
## [2.0.0] - 2025-XX-XX

### 💥 Breaking Changes

**Changed API signature:**
- Old: `function(param1, param2)`
- New: `function({ param1, param2 })`

**Migration Guide:**
[Detailed migration steps]

# 4. Commit, publish, tag (same as above)
```

---

## Troubleshooting Releases

### Issue: npm publish fails

**Check:**
```bash
# Verify logged in
npm whoami

# Verify package access
npm owner ls @j0kz/smart-reviewer-mcp

# Verify version not already published
npm view @j0kz/smart-reviewer-mcp versions
```

**For complete troubleshooting:** See [references/troubleshooting-releases.md](references/troubleshooting-releases.md)

---

### Issue: Version mismatch

```bash
# Fix with version sync
npm run version:check-shared
# Shows mismatches

npm run version:sync
# Fixes all versions
```

---

### Issue: Tag already exists

```bash
# Delete local tag
git tag -d v1.0.37

# Delete remote tag
git push origin :refs/tags/v1.0.37

# Recreate tag
git tag -a v1.0.37 -m "Release v1.0.37"
git push origin v1.0.37
```

---

## Post-Release

**After successful release:**

1. **Update wiki** (if user-facing changes)
   ```powershell
   ./publish-wiki.ps1
   ```

2. **Announce release** (optional)
   - GitHub Discussions
   - Twitter/social media
   - Discord/community channels

3. **Monitor for issues**
   - Check GitHub issues
   - Monitor npm downloads
   - Watch for bug reports

4. **Update documentation** (if needed)
   - README updates
   - Wiki pages
   - API documentation

---

## Quick Command Reference

```bash
# Version management
npm run version:sync               # Sync all versions from version.json
npm run version:check-shared       # Check for mismatches

# Publishing
npm run publish-all                # Publish all packages
npm publish packages/tool --access public  # Publish single package

# Validation
npm test                           # Run all tests
npm run build                      # Build all packages
npm run update:test-count          # Update test count badges

# Git tagging
git tag -a v1.0.37 -m "Message"   # Create tag
git push origin v1.0.37            # Push tag
git push --tags                    # Push all tags

# Verification
npm view @j0kz/package version     # Check published version
```

---

## Best Practices

### ✅ DO

1. **Always update version.json first** (single source of truth)
2. **Run version:sync after version changes**
3. **Update CHANGELOG before publishing**
4. **Run full test suite before publishing**
5. **Create annotated tags** (not lightweight)
6. **Verify deployment after publishing**

### ❌ DON'T

1. **Don't manually edit package.json versions** (use version.json)
2. **Don't skip CHANGELOG updates**
3. **Don't publish without testing**
4. **Don't forget to push tags**
5. **Don't force push tags** (coordinate with team)

---

## Related Skills

- **git-pr-workflow** - Creating PRs before release
- **documentation-generation** - Updating docs for release
- **project-standardization** - Version.json usage

---

## References

**Detailed Guides:**
- [Complete Release Checklist](references/complete-release-checklist.md) - Step-by-step release process
- [Emergency Rollback Procedures](references/emergency-rollback-procedures.md) - Handling failed releases
- [Troubleshooting Releases](references/troubleshooting-releases.md) - Common release issues

**Project Files:**
- version.json - Single source of truth for versions
- CHANGELOG.md - 25+ documented releases
- scripts/version-sync.js - Automated version synchronization
- package.json workspaces - Multi-package setup

---

**Release Principles:**
1. version.json is the ONLY source of truth
2. ALWAYS run version:sync after version changes
3. ALWAYS update CHANGELOG before releasing
4. ALWAYS test before publishing
5. NEVER skip verification steps
6. Document breaking changes clearly
7. Have rollback plan ready
