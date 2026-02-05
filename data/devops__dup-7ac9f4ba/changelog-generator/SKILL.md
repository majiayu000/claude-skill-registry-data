---
name: changelog-generator
description: Automatically creates user-facing changelogs from git commits by analyzing commit history, categorizing changes, and transforming technical commits into clear, customer-friendly release notes. Turns hours of manual changelog writing into minutes of automated generation.
---

# Changelog Generator

Transform technical git commits into polished, user-friendly changelogs that customers and users will actually understand and appreciate.

## When to Use This Skill

- Preparing release notes for a new version
- Creating weekly or monthly product update summaries
- Documenting changes for customers
- Writing changelog entries for app store submissions
- Generating update notifications
- Creating internal release documentation
- Maintaining a public changelog/product updates page

## What This Skill Does

1. **Scans Git History**: Analyzes commits from a specific time period or between versions
2. **Categorizes Changes**: Groups commits into logical categories (features, improvements, bug fixes, breaking changes, security)
3. **Translates Technical → User-Friendly**: Converts developer commits into customer language
4. **Formats Professionally**: Creates clean, structured changelog entries
5. **Filters Noise**: Excludes internal commits (refactoring, tests, etc.)
6. **Follows Best Practices**: Applies changelog guidelines and brand voice

## Process

Follow these steps to generate a changelog:

1. **Retrieve Git Commit History**
   - Run `git log --oneline --since="<date>"` for date-based ranges
   - Run `git log --oneline <tag1>..<tag2>` for version-based ranges
   - Run `git log --oneline -n <number>` for last N commits

2. **Filter and Categorize Commits**
   - **Features**: New capabilities (look for "add", "implement", "create" keywords)
   - **Improvements**: Enhancements to existing features (look for "improve", "enhance", "update", "optimize")
   - **Bug Fixes**: Corrections (look for "fix", "resolve", "correct")
   - **Breaking Changes**: API/behavior changes requiring user action
   - **Security**: Security-related updates
   - **Skip**: Internal changes (refactor, test, build, docs, chore)

3. **Transform Technical Language to User-Friendly**
   - Convert: "Add OAuth2 authentication provider" → "Sign in with Google, GitHub, or Microsoft accounts"
   - Convert: "Implement lazy loading for image components" → "Images now load faster as you scroll"
   - Convert: "Fix race condition in sync worker" → "Resolved sync reliability issues"
   - Focus on user impact, not implementation details
   - Use active voice and present tense
   - Remove technical jargon (API, SDK, refactor, etc.)

4. **Format the Changelog**
   - Group by category with emoji/icons (✨ Features, 🔧 Improvements, 🐛 Fixes)
   - Use bullet points with bold titles
   - Include brief descriptions of user benefit
   - Add version number and date

5. **Review and Refine**
   - Ensure clarity for non-technical users
   - Check for consistent tone and voice
   - Verify all user-impacting changes are included
   - Remove or consolidate minor changes

## How to Use

### Basic Usage

From the project repository:

```
Create a changelog from commits since last release
```

```
Generate changelog for all commits from the past week
```

```
Create release notes for version 2.5.0
```

### With Specific Date Range

```
Create a changelog for all commits between March 1 and March 15
```

### With Custom Guidelines

```
Create a changelog for commits since v2.4.0, using changelog
guidelines from CHANGELOG_STYLE.md
```

## Example

**User**: "Create a changelog for commits from the past 7 days"

**Output**:
```markdown
# Updates - Week of March 10, 2024

## ✨ New Features

- **Team Workspaces**: Create separate workspaces for different
  projects. Invite team members and keep everything organized.

- **Keyboard Shortcuts**: Press ? to see all available shortcuts.
  Navigate faster without touching your mouse.

## 🔧 Improvements

- **Faster Sync**: Files now sync 2x faster across devices
- **Better Search**: Search now includes file contents, not just titles

## 🐛 Fixes

- Fixed issue where large images wouldn't upload
- Resolved timezone confusion in scheduled posts
- Corrected notification badge count
```

**Inspired by:** Manik Aggarwal's use case from Lenny's Newsletter

## Tips

- Run from git repository root
- Specify date ranges for focused changelogs
- Use CHANGELOG_STYLE.md for consistent formatting
- Review and adjust the generated changelog before publishing
- Save output directly to CHANGELOG.md

## Related Use Cases

- Creating GitHub release notes
- Writing app store update descriptions
- Generating email updates for users
- Creating social media announcement posts
