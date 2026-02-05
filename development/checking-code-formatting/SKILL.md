---
name: checking-code-formatting
description: Check code formatting, detect style issues, and identify inconsistencies. Use when the user asks to check formatting, code style, linting, format issues, or code formatting problems.
allowed-tools: read_file, grep_search
---

# Code Formatting Checker

## Instructions

Analyze code files for formatting issues and inconsistencies. Provide a comprehensive report with specific file locations and recommendations.

### Step 1: Determine Scope

1. **Identify target files**:
   - If user specifies files/directories, check those
   - If no target specified, analyze current directory recursively
   - Focus on source code files: `.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.rs`, `.go`, `.java`, `.cpp`, `.c`, `.h`, etc.

2. **Use `list_directory`** to explore the codebase structure
3. **Use `grep_search`** to find source files by extension

### Step 2: Language-Agnostic Formatting Checks

Use `grep_search` and `read_file` to check for these common issues:

#### 2.1 Trailing Whitespace
- **Pattern**: Search for lines ending with spaces or tabs (`[ \t]+$`)
- **Impact**: High - causes unnecessary diffs
- **Fix**: Remove trailing whitespace

#### 2.2 Mixed Line Endings
- **Pattern**: Check for mixed `\r\n` (Windows) and `\n` (Unix)
- **Impact**: Medium - can cause issues in version control
- **Fix**: Normalize to one style (prefer `\n` for Unix)

#### 2.3 Inconsistent Indentation
- **Method**: Read files and analyze leading whitespace
- **Check for**:
  - Mix of tabs and spaces
  - Inconsistent indentation levels (2 vs 4 spaces)
  - Files that should be consistent but aren't
- **Impact**: High - breaks code readability and can cause errors
- **Fix**: Choose one style per language (Python: 4 spaces, JavaScript: 2 spaces typically)

#### 2.4 File Ending Issues
- **Check**: Missing newline at end of file (POSIX compliance)
- **Check**: Extra blank lines at end of file
- **Pattern**: Read last few lines of files
- **Impact**: Low-Medium - style consistency
- **Fix**: Ensure exactly one newline at end of file

#### 2.5 Line Length
- **Threshold**: Typically 80, 100, or 120 characters (language/project dependent)
- **Method**: Read files and check line lengths
- **Impact**: Medium - readability
- **Report**: List lines exceeding threshold with line numbers

#### 2.6 Blank Line Consistency
- **Check**: Missing blank lines between functions/classes
- **Check**: Extra blank lines between sections
- **Method**: Analyze code structure patterns
- **Impact**: Low-Medium - style consistency

### Step 3: Language-Specific Checks

#### 3.1 Python
- **Quotes**: Check for inconsistent quote style (single vs double)
- **Imports**: Check import order and grouping
- **Whitespace**: PEP 8 spacing around operators, after commas
- **Use bash_command**: Run `black --check` or `flake8 --select=E,W` if available
- **Use bash_command**: Run `ruff check` if available (fast Python linter)

#### 3.2 JavaScript/TypeScript
- **Quotes**: Single vs double quotes consistency
- **Semicolons**: Consistent use (or lack) of semicolons
- **Spacing**: Consistent spacing in object literals, function calls
- **Use bash_command**: Run `prettier --check` if available
- **Use bash_command**: Run `eslint --fix --dry-run` if available

#### 3.3 Rust
- **Use bash_command**: Run `cargo fmt -- --check` if available
- **Indentation**: Standard Rust uses 4 spaces
- **Line length**: Standard is 100 characters

#### 3.4 Go
- **Use bash_command**: Run `gofmt -l` to list files needing formatting
- **Use bash_command**: Run `gofmt -d` to show diffs

#### 3.5 General
- Look for project-specific formatters: `.prettierrc`, `.editorconfig`, `pyproject.toml` (with black/flake8 config)
- If formatter config exists, use it for standards

### Step 4: Generate Report

Create a comprehensive report with this structure:

```markdown
# Code Formatting Report

## Summary
- Total files checked: X
- Files with issues: Y
- Critical issues: Z
- Warnings: W

## Issues by Category

### [Category Name]
**Impact**: [High/Medium/Low]
**Count**: [number]

#### Files Affected:
- `path/to/file.ext:line:column` - [description]
- `path/to/file.ext:line:column` - [description]

**Recommendations**:
- [Specific fix instructions]

## Language-Specific Issues

### Python
[Issues found and fixes]

### JavaScript/TypeScript
[Issues found and fixes]

## Suggested Actions

1. [Priority fix]
2. [Next fix]
3. [Optional improvement]

## Formatter Availability

- black: [available/unavailable]
- prettier: [available/unavailable]
- cargo fmt: [available/unavailable]
- gofmt: [available/unavailable]

If formatters are available, suggest running:
```bash
[formatter command]
```
```

### Report Format Guidelines

1. **Be specific**: Include file paths, line numbers, and column positions
2. **Prioritize**: Group by impact (Critical, High, Medium, Low)
3. **Actionable**: Provide clear fix instructions
4. **Quantify**: Show counts and statistics
5. **Organize**: Group by issue type and then by file

### Step 5: Provide Fix Suggestions

For each issue type, provide:

1. **Manual fixes**: Exact steps to fix manually
2. **Automated fixes**: Commands to run (if formatters available)
3. **Prevention**: How to avoid in future (editor config, pre-commit hooks)

## Examples

### Example 1: Python Project
User: "Check formatting in this Python project"
- Scan for trailing whitespace
- Check indentation (should be 4 spaces)
- Check line length (PEP 8: 79 chars, but often 100-120 is acceptable)
- Run `black --check` if available
- Report inconsistencies

### Example 2: JavaScript Project
User: "Find formatting issues"
- Check quote consistency
- Check semicolon usage
- Run `prettier --check` if available
- Report all issues with file:line references

### Example 3: Mixed Language Project
User: "Check code style"
- Identify files by extension
- Run language-specific checks
- Use appropriate formatters per language
- Generate unified report

## Best Practices

1. **Check formatter availability first**: Use `bash_command` to test if formatters are installed before suggesting their use
2. **Respect project conventions**: Look for `.editorconfig`, formatter config files
3. **Be thorough but efficient**: Check multiple files in parallel where possible
4. **Prioritize critical issues**: Focus on issues that break functionality (wrong indentation) vs style (quote preference)
5. **Provide context**: Explain why each issue matters

## Tools to Use

- `grep_search`: Find patterns across files (trailing spaces, inconsistent quotes)
- `read_file`: Analyze file contents for indentation, line lengths
- `bash_command`: Run formatters and linters if available
- `list_directory`: Discover project structure and find source files

## Notes

- Some issues are subjective (quote style) - report but note they're style preferences
- Critical issues (wrong indentation) can break code - prioritize these
- Formatters may not be installed - gracefully handle unavailable tools
- Respect existing project style even if it differs from "standard" - consistency within project is key

