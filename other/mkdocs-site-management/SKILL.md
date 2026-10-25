---
name: mkdocs-site-management
description: Guide for creating and maintaining MkDocs sites, ensuring configuration consistency and resolving build issues. Use when working with MkDocs documentation sites, making changes to source directories, or modifying configuration files.
license: MIT
---

# MkDocs Site Management

This skill provides comprehensive guidance for creating and maintaining MkDocs documentation sites. It ensures that changes to source directories are properly reflected in the MkDocs configuration and that build issues are systematically resolved.

## When to Use This Skill

Use this skill when:
- Setting up a new MkDocs site
- Adding or removing documentation files in the source directory
- Modifying the MkDocs configuration file (mkdocs.yml)
- Troubleshooting MkDocs build failures or warnings
- Ensuring navigation and site structure consistency

## Prerequisites

- MkDocs installed in the project environment
- Basic understanding of MkDocs configuration structure
- Access to terminal commands for running MkDocs build

## Instructions

### 1. Initial Setup and Configuration Verification

1. Confirm MkDocs is installed by running `mkdocs --version` in the terminal
2. Locate the configuration file (typically `mkdocs.yml` in the project root)
3. Identify the source directory (usually `docs/` as specified in `mkdocs.yml`)
4. Verify the basic configuration structure exists

### 2. Handling Source Directory Changes

When files are added, removed, or reorganized in the source directory:

1. **Analyze the change**: Use `list_dir` to examine the current structure of the docs directory
2. **Check navigation configuration**: Read the `mkdocs.yml` file and examine the `nav` section
3. **Update navigation if needed**: If new pages are added or structure changed, update the `nav` in `mkdocs.yml`
   - Add new page entries to the navigation
   - Remove entries for deleted pages
   - Adjust nesting for reorganized directories
4. **Validate structure**: Ensure the navigation matches the actual file structure

### 3. Modifying MkDocs Configuration

When making changes to `mkdocs.yml`:

1. **Make the configuration change**: Edit the file using appropriate tools
2. **Run build validation**: Execute `mkdocs build --clean --strict` in the terminal
3. **Analyze output**: Review the build output for ERROR or WARNING messages
4. **Resolve issues**: Address any errors or warnings found

### 4. Resolving Build Issues

Common MkDocs build issues and resolutions:

#### Navigation Errors
- **Issue**: "Page 'path/to/page.md' listed in navigation but not found"
- **Solution**: Either add the missing file or remove the entry from nav

#### YAML Syntax Errors
- **Issue**: YAML parsing errors in mkdocs.yml
- **Solution**: Check YAML syntax, indentation, and quoting

#### Plugin Configuration Errors
- **Issue**: Plugin-related errors or warnings
- **Solution**: Verify plugin installation and configuration

#### Link/Reference Errors
- **Issue**: Broken internal links or references
- **Solution**: Update links to match current file structure

#### Theme Configuration Issues
- **Issue**: Theme-related warnings or errors
- **Solution**: Verify theme name and custom theme paths

### 5. Build Validation and Testing

After any configuration changes:

1. Run `mkdocs build --clean --strict`
2. Check for any ERROR or WARNING messages in the output
3. If issues found, resolve them using the appropriate fixes above
4. Re-run the build to confirm resolution
5. Optionally run `mkdocs serve` to test the site locally

## Examples

### Example 1: Adding a New Documentation Page

When adding `docs/new-feature.md`:

1. Add the page to mkdocs.yml nav section:
   ```yaml
   nav:
     - Home: index.md
     - New Feature: new-feature.md
   ```
2. Run `mkdocs build --clean --strict` to validate
3. Resolve any issues if they appear

### Example 2: Resolving a Missing Page Error

Build output shows: `ERROR - Page 'docs/missing-page.md' listed in navigation but not found`

1. Check if the file exists in docs/
2. If file doesn't exist, remove from nav in mkdocs.yml
3. If file exists but path is wrong, correct the path in nav
4. Re-run build to confirm fix

### Example 3: Fixing YAML Indentation

Build fails with YAML error:

1. Read mkdocs.yml and check indentation
2. Ensure consistent spacing (usually 2 spaces)
3. Fix any indentation issues
4. Run build again

## Best Practices

- Always run `mkdocs build --clean --strict` after configuration changes
- Keep navigation structure aligned with file system organization
- Use relative paths in navigation
- Regularly validate the site build to catch issues early
- Test the site with `mkdocs serve` before deploying

## Common Issues

**Issue**: Build succeeds but site doesn't update
**Solution**: Use `--clean` flag to clear the site directory cache

**Issue**: Navigation shows old structure
**Solution**: Ensure nav in mkdocs.yml matches current docs/ directory structure

**Issue**: Plugin not working
**Solution**: Verify plugin is installed and properly configured in mkdocs.yml

**Issue**: Theme not applying
**Solution**: Check theme name spelling and ensure custom themes are in correct location

## Additional Resources

- [MkDocs Documentation](https://www.mkdocs.org/)
- [MkDocs Configuration Reference](https://www.mkdocs.org/user-guide/configuration/)
- [MkDocs Themes](https://www.mkdocs.org/user-guide/choosing-your-theme/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)