---
name: writing-release-notes
description: Generate release notes and changelog entries from git history and project changes. Use when the user asks to write release notes, create changelog, document version changes, or generate release documentation.
allowed-tools: read_file, write_file
---

# Write Release Notes

## Instructions

Generate professional release notes and changelog entries for software releases. Analyze project changes, git history, and version information to create comprehensive release documentation.

### Step 1: Gather Release Information

1. **Determine version information**:
   - Read `package.json`, `pyproject.toml`, `Cargo.toml`, or other version files
   - Check for version bumps or new version numbers
   - Identify if this is a major, minor, or patch release (semantic versioning)
   - Use `bash_command` to check version files: `cat package.json | grep version`

2. **Analyze git history**:
   - Use `bash_command` to get recent commits: `git log --oneline --since="2 weeks ago"` or `git log --oneline -20`
   - Use `bash_command` to get diff stats: `git diff --stat HEAD~10..HEAD`
   - Use `bash_command` to compare versions: `git log v1.0.0..HEAD --oneline` (if previous tag exists)
   - Look for conventional commit messages (feat:, fix:, docs:, etc.)

3. **Check for changelog files**:
   - Read existing `CHANGELOG.md`, `CHANGES.md`, or `RELEASE_NOTES.md` if they exist
   - Maintain consistency with existing format
   - Check for `CHANGELOG` or `HISTORY` files in project root

4. **Identify project type**:
   - Check for package managers: `package.json` (npm), `pyproject.toml` (Python), `Cargo.toml` (Rust)
   - This helps determine version format and release conventions

### Step 2: Categorize Changes

Organize changes into standard release note categories:

1. **Added** (Features):
   - New features, functionality, or capabilities
   - Look for: `feat:`, "add", "new", "introduce" in commit messages
   - Major new components or modules

2. **Changed** (Improvements):
   - Improvements to existing features
   - API changes (non-breaking)
   - Performance improvements
   - Look for: "improve", "enhance", "update", "refactor" in commits

3. **Fixed** (Bug Fixes):
   - Bug fixes and issue resolutions
   - Look for: `fix:`, "bug", "issue", "correct" in commit messages
   - Security fixes

4. **Deprecated**:
   - Features marked for removal
   - Look for: "deprecate", "deprecated" in commits or code comments

5. **Removed**:
   - Features or APIs removed
   - Look for: "remove", "delete", "drop" in commits

6. **Security**:
   - Security vulnerabilities fixed
   - Look for: "security", "CVE", "vulnerability" in commits

### Step 3: Analyze Commits and Changes

1. **Parse commit messages**:
   - Use `bash_command`: `git log --pretty=format:"%h - %s (%an, %ar)" -20`
   - Group by type using conventional commits or patterns
   - Extract meaningful descriptions

2. **Review code changes**:
   - Use `bash_command`: `git diff --stat HEAD~10..HEAD` to see file changes
   - Use `bash_command`: `git log --name-status --pretty=format:"" HEAD~10..HEAD` for changed files
   - Look at PR titles or commit descriptions for context

3. **Identify breaking changes**:
   - Look for: `BREAKING CHANGE:`, "breaking", "major", "incompatible" in commits
   - Check API changes in code
   - Review migration guides if they exist

### Step 4: Generate Release Notes Structure

Create a well-formatted release notes document with this structure:

```markdown
# Release Notes - Version X.Y.Z

**Release Date**: [Current date]
**Full Changelog**: [Link to full changelog if applicable]

## Summary

Brief 2-3 sentence summary of this release highlighting the most important changes.

## 🎉 Added

- [Feature description with context]
- [Another feature]

## ✨ Changed

- [Improvement description]
- [API change with migration notes if applicable]

## 🐛 Fixed

- [Bug fix description with issue reference if available]
- [Another fix]

## 🔒 Security

- [Security fix description]

## ⚠️ Breaking Changes

- [Breaking change description]
- [Migration guide reference or steps]

## 📚 Documentation

- [Documentation improvements]

## ⚙️ Internal

- [Internal improvements, refactoring, build changes]

## Contributors

Thank you to all contributors: [List of contributors if available from git log]

## Upgrade Instructions

[If applicable, provide upgrade/installation instructions]
```

### Step 5: Write Professional Release Notes

1. **Use clear, user-facing language**:
   - Avoid technical jargon where possible
   - Explain what changed and why it matters
   - Include examples or use cases for major features

2. **Be specific and actionable**:
   - "Fixed memory leak in data processing" not just "Fixed bugs"
   - "Added support for Python 3.12" not just "Updated Python support"
   - Include issue numbers or PR references if available

3. **Group related changes**:
   - Combine similar fixes or features
   - Use sub-bullets for detailed changes
   - Keep each category organized

4. **Include migration notes**:
   - For breaking changes, provide clear upgrade paths
   - Reference migration guides if they exist
   - Show before/after examples for API changes

5. **Add context**:
   - Link to relevant documentation
   - Reference related issues or PRs
   - Include contributor credits if appropriate

### Step 6: Format and Style

1. **Use markdown formatting**:
   - Headers for version and date
   - Bullet points for lists
   - Code blocks for examples
   - Links for references

2. **Consistent style**:
   - Start each item with a verb (Added, Fixed, Changed)
   - Use present tense or past tense consistently
   - Keep line lengths reasonable (80-100 chars)

3. **Emoji usage** (optional but helpful):
   - 🎉 for new features
   - ✨ for improvements
   - 🐛 for bug fixes
   - 🔒 for security
   - ⚠️ for breaking changes
   - 📚 for documentation

4. **Version format**:
   - Follow semantic versioning: `MAJOR.MINOR.PATCH`
   - Use consistent format: `v1.2.3` or `1.2.3`
   - Match project's existing versioning style

### Step 7: Handle Different Scenarios

#### First Release:
- Focus on initial features and setup
- Explain what the project does
- Include installation/setup instructions

#### Patch Release:
- Focus on bug fixes
- May not need full structure
- Quick summary format

#### Major Release:
- Include migration guide
- Highlight breaking changes prominently
- Provide upgrade checklist

#### No Git History:
- Use file changes detected via `list_directory` and `read_file`
- Analyze code modifications
- Create notes from current state vs expected state

### Step 8: Verify and Complete

1. **Check completeness**:
   - All significant changes included
   - No placeholder text remaining
   - Version number is correct
   - Date is current

2. **Validate format**:
   - Markdown renders correctly
   - Links work (if any)
   - Consistent style throughout

3. **Save appropriately**:
   - Save as `RELEASE_NOTES.md` or `CHANGELOG.md`
   - Or append to existing `CHANGELOG.md`
   - Follow project conventions

## Examples

### Example 1: Semantic Versioning Project
User: "Write release notes for version 2.1.0"
- Check `package.json` or `pyproject.toml` for version
- Analyze git commits since last tag
- Categorize into Added/Changed/Fixed
- Generate formatted release notes

### Example 2: Update Existing Changelog
User: "Update the changelog"
- Read existing `CHANGELOG.md`
- Get recent commits since last entry
- Add new entry at top
- Maintain existing format style

### Example 3: First Release
User: "Create release notes for the initial release"
- Analyze current project state
- List initial features from codebase
- Create comprehensive first-release notes
- Include installation instructions

## Best Practices

1. **Be accurate**: Only include changes that actually happened
2. **Be user-focused**: Write for end users, not just developers
3. **Be complete**: Include all significant changes
4. **Be concise**: Don't list every single commit, group intelligently
5. **Be helpful**: Provide context and upgrade instructions
6. **Follow conventions**: Match existing project style and format

## Tools to Use

- `bash_command`: Run git commands to analyze history
- `read_file`: Read version files and existing changelogs
- `list_directory`: Explore project structure
- `grep_search`: Find version numbers or change indicators in files

## Notes

- If git history is not available, focus on analyzing current code state
- Respect existing changelog format if one exists
- When unsure about a change, err on the side of inclusion
- Major releases should always include migration guides for breaking changes
- Security fixes should be clearly highlighted

