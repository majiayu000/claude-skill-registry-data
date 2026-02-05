---
name: changelog-manager
description: Automatically create and update CHANGELOG.md files for scripts and tools following Keep a Changelog format. Use when creating new scripts, updating existing scripts, fixing bugs, or adding features to any tool in the repository.
allowed-tools: Read, Write, Edit, Glob
---

# Changelog Manager Skill

This Skill ensures that **every script and tool** in the tech-support-tools repository has a properly maintained changelog following the [Keep a Changelog](https://keepachangelog.com/en/1.0.0/) format and [Semantic Versioning](https://semver.org/spec/v2.0.0.html) principles.

## Purpose

All scripts and tools must have:
1. A `changelog/` directory within the script's folder
2. A `CHANGELOG.md` file tracking all version changes
3. Properly categorized entries for each update
4. Synchronized version numbers between the script and changelog

## When to Use This Skill

**ALWAYS use this Skill when:**
- Creating a new script or tool (create initial changelog with version 1.0)
- Updating an existing script (add new version entry)
- Fixing bugs in a script (add entry under ### Fixed)
- Adding new features (add entry under ### Added)
- Modifying existing functionality (add entry under ### Changed)
- Removing functionality (add entry under ### Removed)
- Marking features as deprecated (add entry under ### Deprecated)
- Addressing security vulnerabilities (add entry under ### Security)

**The workflow is:**
1. Make changes to the script
2. Update the version number in the script
3. **Immediately update the CHANGELOG.md** with the new version and changes

## Directory Structure

Each script should have its changelog in a dedicated subdirectory:

```
windows/
  script-name/
    ├── script-name.ps1
    └── changelog/
        └── CHANGELOG.md

macos/
  script-name/
    ├── script-name.sh
    └── changelog/
        └── CHANGELOG.md
```

## Changelog Format

Every CHANGELOG.md must follow this structure:

```markdown
# Changelog

All notable changes to the [Script Name] will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [X.Y] - YYYY-MM-DD

### Added
- New feature description

### Changed
- Modified functionality description

### Fixed
- Bug fix description

---

## [Previous Version] - YYYY-MM-DD

...

---

## [1.0] - Initial Release

### Added
- Initial features list
```

## Version Numbering (Semantic Versioning)

Use semantic versioning: `MAJOR.MINOR` (simplified for scripts)

**When to increment:**
- **MAJOR (1.0 → 2.0)**: Breaking changes, complete rewrites, incompatible changes
- **MINOR (1.0 → 1.1)**: New features, bug fixes, improvements (backward compatible)

**Examples:**
- Adding a parameter: `1.0 → 1.1`
- Fixing a bug: `1.0 → 1.1`
- Complete rewrite following new standards: `1.0 → 2.0`
- Removing a parameter: `1.0 → 2.0` (breaking change)

## Change Categories

Use these standard categories (as applicable):

### Added
For new features, parameters, functionality, or capabilities.

**Examples:**
- Added `-Quiet` parameter to suppress interactive banner
- Added export to JSON functionality
- Added support for remote computers
- Added progress bar for long-running operations
- Added ASCII banner with script information

### Changed
For changes in existing functionality.

**Examples:**
- Changed default timeout from 30s to 60s
- Improved error messages for better clarity
- Updated output format to include timestamps
- Refactored code to meet PowerShell standards
- Enhanced performance of data processing

### Deprecated
For features that will be removed in future versions.

**Examples:**
- Deprecated `-OldParameter` in favor of `-NewParameter`
- Deprecated XML export (use JSON instead)

### Removed
For removed features or functionality.

**Examples:**
- Removed support for Windows 7
- Removed deprecated `-OldParameter`
- Removed legacy output format

### Fixed
For bug fixes.

**Examples:**
- Fixed memory leak in data collection loop
- Fixed incorrect CPU calculation for multi-core systems
- Fixed crash when log directory doesn't exist
- Write-Log function now properly accepts empty strings
- Removed duplicate success message appearing twice

### Security
For security-related changes or vulnerability fixes.

**Examples:**
- Fixed command injection vulnerability in user input
- Updated credential handling to use SecureString
- Removed hardcoded API key

## Creating a New Changelog

When creating a new script, immediately create its changelog:

### Steps:
1. Create `changelog/` directory inside the script's folder
2. Create `CHANGELOG.md` using the template
3. Add initial release entry with version `[1.0]`
4. List all initial features under `### Added`
5. Use today's date in `YYYY-MM-DD` format

### Template:
See `templates/CHANGELOG-template.md`

## Updating an Existing Changelog

When modifying a script, update the changelog:

### Steps:
1. Determine the new version number (based on semantic versioning)
2. Add a new version section at the TOP of the changelog (after the header, before previous versions)
3. Use today's date
4. Categorize all changes appropriately
5. Be specific and clear in descriptions
6. Use bullet points for each change

### Format:
```markdown
## [New.Version] - YYYY-MM-DD

### [Category]
- Specific description of what changed
- Another change in this category

### [Another Category]
- Change description
```

## Best Practices

### ✅ Do:
- **Update changelog immediately** when changing scripts
- **Be specific** in change descriptions (not "bug fixes" but "Fixed memory leak in data collection")
- **Use present tense** ("Add feature" not "Added feature" in the description)
- **Group related changes** under appropriate categories
- **Keep version numbers synchronized** between script and changelog
- **Use today's date** for new entries
- **Order categories** as: Added, Changed, Deprecated, Removed, Fixed, Security
- **Add horizontal rules** (`---`) between version sections

### ❌ Don't:
- Don't use vague descriptions ("various improvements")
- Don't skip version numbers
- Don't use future dates
- Don't forget to update the script's version number to match
- Don't mix multiple categories in one bullet point
- Don't include internal/development-only changes users don't care about

## Synchronization Requirements

**Critical**: Version numbers must match in three places:

1. **Script's comment-based help** (`.NOTES` section):
   ```powershell
   .NOTES
       Version: 1.1
       Last Updated: 2025-12-26
   ```

2. **Script's banner** (if applicable):
   ```powershell
   Write-Host "| Version      : 1.1                                                          |"
   Write-Host "| Last Updated : 2025-12-26                                                   |"
   ```

3. **CHANGELOG.md** (latest entry):
   ```markdown
   ## [1.1] - 2025-12-26
   ```

**All three must always match!**

## Examples

### Example 1: Initial Changelog for New Script

```markdown
# Changelog

All notable changes to the Network Diagnostics Tool will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0] - 2025-12-26

### Added
- Network connectivity testing with ping, traceroute, and DNS lookup
- Bandwidth speed test functionality
- Port scanning for common services
- Log file generation with detailed diagnostic information
- Interactive banner with script information
- Export results to JSON format
```

### Example 2: Adding Features (1.0 → 1.1)

```markdown
## [1.1] - 2025-12-26

### Added
- Support for custom DNS servers in diagnostics
- Quiet mode parameter for scripting
- Progress bar for long-running tests

### Changed
- Improved timeout handling for network tests
- Enhanced error messages with troubleshooting tips

### Fixed
- Fixed incorrect bandwidth calculation on slow connections
- Resolved crash when network adapter is disabled

---

## [1.0] - 2025-12-25

### Added
- Initial network diagnostics functionality
...
```

### Example 3: Breaking Change (1.5 → 2.0)

```markdown
## [2.0] - 2025-12-26

### Changed
- **BREAKING**: Refactored to meet PowerShell standards
- Output now returns structured objects instead of formatted text
- Renamed `-OutputFile` parameter to `-ExportPath` for consistency

### Added
- CmdletBinding support with verbose and debug output
- Pipeline support with -PassThru parameter
- Comprehensive comment-based help

### Removed
- Removed deprecated `-LegacyFormat` parameter

---

## [1.5] - 2025-12-20

...
```

## Integration with Other Skills

This skill works together with:

- **script-banner**: When updating script version in banner, update changelog
- **commit-code**: Changelog entries help write better commit messages
- **create-changelog**: (Built-in skill) - This skill may supplement or replace it

## Workflow Example

When the user says: *"Add a -Quiet parameter to the backup script"*

1. **Edit the script** to add the parameter
2. **Update version** in script from `1.0` to `1.1`
3. **Update banner** (if present) to show `Version: 1.1` and today's date
4. **Update CHANGELOG.md**:
   ```markdown
   ## [1.1] - 2025-12-26

   ### Added
   - Quiet mode parameter to suppress interactive prompts and run silently
   ```
5. **Verify synchronization** across all three locations

## Checklist for Changelog Updates

Before completing any script modification, verify:
- ✅ Changelog directory exists (`scriptname/changelog/`)
- ✅ CHANGELOG.md file exists
- ✅ New version section added at top
- ✅ Version number follows semantic versioning
- ✅ Date is today's date in YYYY-MM-DD format
- ✅ Changes are categorized correctly (Added/Changed/Fixed/etc.)
- ✅ Descriptions are specific and clear
- ✅ Horizontal rule (`---`) separates version sections
- ✅ Script's .NOTES version matches changelog
- ✅ Script's banner version matches changelog (if applicable)
- ✅ No typos or formatting errors

## Reference Files

- `templates/CHANGELOG-template.md` - Template for creating new changelogs
- `reference/categories-guide.md` - Detailed guide for categorizing changes

## Special Cases

### Multiple Changes in One Update
Group by category, multiple bullets:
```markdown
## [1.2] - 2025-12-26

### Added
- Email notification support
- Scheduled task creation helper

### Fixed
- Memory leak in monitoring loop
- Incorrect timestamp in log files
```

### No Changes in a Category
Simply omit that category. Only include categories that have changes.

### Initial Release
Always use `[1.0]` and primarily use `### Added`:
```markdown
## [1.0] - Initial Release

### Added
- All initial features listed here
```

### Version Already Exists
If you're making additional changes to a version that's not yet released:
- **Add to the existing version section** (don't create a new version)
- Update the date if needed
- Add changes to appropriate categories

## Important Notes

- Changelogs are **user-facing documentation** - write for users, not developers
- Every user-visible change should be documented
- Internal refactoring that doesn't change behavior can be noted briefly or omitted
- Links to documentation or issues are optional but helpful
- Keep descriptions concise but informative
- When in doubt, err on the side of more detail rather than less

## Auto-Detection

This skill should automatically activate when:
- User requests a new script (create initial changelog)
- User requests changes to existing scripts (update changelog)
- User explicitly mentions "update changelog" or "add to changelog"
- Version numbers are being updated
- Features are being added, modified, or removed
