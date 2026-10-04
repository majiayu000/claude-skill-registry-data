---
name: release-decoder
description: This skill should be used when the user wants to decode Claude Code release notes, compare versions, check what's new in a release, or understand changes between versions. Automatically triggers when user mentions "release notes", "what's new", "changelog", "version comparison", "decode release", or asks about Claude Code updates.
---

# Release Decoder

Decode and analyze Claude Code release notes to understand what changed between versions.

## Capabilities

1. **Fetch Latest Release Info** - Get the current installed version and latest available version
2. **Compare Versions** - Show what changed between two specific versions
3. **Decode Release Notes** - Parse and summarize changelog entries
4. **Highlight Important Changes** - Identify breaking changes, new features, and bug fixes

## Workflow

### Step 1: Check Current Version

Run the following to get version info:

```bash
echo "Current: $(claude --version)" && echo "Latest: $(npm view @anthropic-ai/claude-code version)"
```

### Step 2: Fetch Release Notes

To get release notes, fetch the Claude Code changelog from GitHub:

```bash
curl -s "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md" | head -500
```

Alternatively, use WebFetch to get the changelog:
- URL: `https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md`
- Prompt: "Extract release notes for version X.X.X and summarize the changes"

### Step 3: Decode and Categorize Changes

When presenting release notes, categorize changes into:

1. **Breaking Changes** - Changes that may affect existing workflows
2. **New Features** - New capabilities added
3. **Improvements** - Enhancements to existing features
4. **Bug Fixes** - Issues that were resolved
5. **Security** - Security-related updates
6. **Deprecations** - Features being phased out

### Step 4: Present Summary

Format the decoded release as:

```
## Claude Code vX.X.X Release Summary

### Breaking Changes
- [List any breaking changes]

### New Features
- [List new features with brief descriptions]

### Improvements
- [List improvements]

### Bug Fixes
- [List bug fixes]

### Upgrade Recommendation
[Provide recommendation: "Safe to upgrade", "Review breaking changes first", etc.]
```

## Version Comparison

When comparing versions (e.g., "What changed from 2.0.60 to 2.0.71"):

1. Fetch the full changelog
2. Extract entries between the two versions
3. Aggregate all changes by category
4. Highlight the most significant updates
5. Note any cumulative breaking changes

## Quick Commands

- **Check if update available**: Compare installed vs latest npm version
- **Decode latest**: Fetch and decode the most recent release entry
- **Full changelog**: Get complete changelog for deep analysis
