---
name: ca-django-linters
description: ALWAYS use this skill proactively for Consumer Affairs Django repositories (located in ../ca/ directory) when ANY of these occur - (1) After writing or modifying ANY Python code files in CA repos (2) After tests pass and before telling user work is complete (3) User mentions linting, formatting, ruff, code style, or code quality (4) After using the ca-django-tests skill successfully (5) Before preparing to commit code. This skill runs 'ca exec ruff format' and 'ca exec ruff check --fix' to ensure code quality. CRITICAL - Always run this automatically after code changes and before declaring work complete.
---

# CA Django Linters Skill

This skill runs code formatters and linters on Consumer Affairs repositories to ensure code quality and style compliance before commits.

## When to Use This Skill

**AUTOMATIC ACTIVATION TRIGGERS** - Activate this skill immediately when:

- ✅ You've finished writing or modifying ANY Python code in a CA repository
- ✅ Tests have just passed after using the ca-django-tests skill
- ✅ You're about to tell the user that implementation is ready/complete/done
- ✅ User explicitly asks to run linters, format code, or check code style
- ✅ User mentions "ruff", "linting", "formatting", "code quality", "style compliance"
- ✅ Before preparing commits or telling user to commit code

**CRITICAL WORKFLOW RULE**:

🚨 **NEVER** tell the user "implementation is complete" or "work is done" UNTIL you have:
1. Run both ruff commands (format + check --fix)
2. Fixed all linting errors
3. Verified code is clean and formatted

This skill should ALWAYS run automatically after code changes and BEFORE declaring work complete.

## IMPORTANT: When to Activate

**CRITICAL**: This skill should run AFTER:

1. ✅ Code implementation is complete
2. ✅ Tests have been written and are passing
3. ✅ You're ready to tell the user the work is done

**DO NOT** tell the user implementation is complete until:

- ✅ Both ruff commands have been run successfully
- ✅ All linting errors have been fixed
- ✅ Code is clean and ready for commit

## Linting Commands

Run these two commands in order:

### 1. Format Code with Ruff

```bash
ca exec ruff format --config pyproject.toml .
```

This command:
- Automatically formats Python code according to project standards
- Fixes spacing, indentation, and line length issues
- Updates files in place

### 2. Check and Fix Linting Issues

```bash
ca exec ruff check --fix --config pyproject.toml .
```

This command:
- Checks for code quality issues
- Automatically fixes issues when possible (with `--fix` flag)
- Reports issues that need manual fixing

## Running Linters

### Priority Order for Running Linters

#### 1. First Try: `ca exec` (PREFERRED)

```bash
ca exec ruff format --config pyproject.toml .
ca exec ruff check --fix --config pyproject.toml .
```

**This is the preferred method** - it uses containers that are already running.

#### 2. If ca exec fails: `ca bash` then run commands

```bash
ca bash
# Inside container:
ruff format --config pyproject.toml .
ruff check --fix --config pyproject.toml .
```

Use this if `ca exec` doesn't work for some reason.

### IMPORTANT: Container Usage

- **DO NOT** use `docker compose run` - this starts a separate container
- **DO USE** the `ca` script - it uses already running containers
- The containers should already be running before executing linters

## Handling Linting Errors

### Auto-fixable Errors

Many errors are automatically fixed by ruff:

- Import sorting issues
- Unused imports
- Whitespace issues
- Simple style violations

After running `ruff check --fix`, these will be corrected automatically.

### Manual Fixes Required

Some errors require manual intervention:

#### Common Issues and Fixes

1. **Undefined names / unused variables**
   ```python
   # Before
   def my_function(arg1, arg2):
       return arg1  # arg2 is unused

   # After
   def my_function(arg1, arg2):
       _ = arg2  # Explicitly mark as unused
       return arg1
   ```

2. **Line too long**
   ```python
   # Before
   result = some_function(very_long_argument_1, very_long_argument_2, very_long_argument_3)

   # After
   result = some_function(
       very_long_argument_1,
       very_long_argument_2,
       very_long_argument_3
   )
   ```

3. **Missing docstrings**
   ```python
   # Before
   def complex_function(data):
       return process(data)

   # After
   def complex_function(data):
       """Process data and return result."""
       return process(data)
   ```

4. **Complexity issues (too many branches)**
   - Refactor complex functions into smaller ones
   - Extract logic into helper functions
   - Simplify conditional statements

### Workflow for Fixing Errors

1. **Run both linting commands**
2. **Review the output** - note all errors and warnings
3. **Fix errors one by one**:
   - Start with files you recently modified
   - Fix auto-fixable issues first (run with `--fix`)
   - Then address issues requiring manual fixes
4. **Re-run linters** to verify all issues are resolved
5. **Repeat** until both commands pass with no errors

## Complete Workflow Example

When user asks to "implement a new authentication feature":

1. **Implement the feature** - write the code
2. **Write tests** - use the `ca-django-tests` skill
3. **Run tests** - ensure they pass with `ca magictest`
4. **Run linters** - use this skill:

   ```bash
   ca exec ruff format --config pyproject.toml .
   ca exec ruff check --fix --config pyproject.toml .
   ```

5. **Fix any linting errors** that require manual intervention
6. **Re-run linters** to confirm all issues are resolved
7. **Verify tests still pass** after code formatting changes
8. **Tell the user** the implementation is complete and ready

## Success Criteria

Before telling the user work is complete:

- ✅ Both ruff commands run without errors
- ✅ No linting warnings remain
- ✅ Code is properly formatted
- ✅ Tests still pass after formatting
- ✅ Code is ready for commit and CI

## Common Patterns in CA Repos

### Ignoring Specific Rules

Sometimes you need to ignore a specific rule for a line:

```python
# noqa: E501 - ignore line too long
very_long_line_that_cannot_be_broken = "some value"  # noqa: E501
```

### Configuration Files

The `pyproject.toml` contains ruff configuration:
- Rule selections
- Line length limits
- Import sorting settings
- File excludes

Do not modify these without discussing with the team.

## Error Examples and Solutions

### Example 1: Import Sorting

```bash
Error: Imports are incorrectly sorted
```

**Solution**: Run `ruff check --fix` - it will auto-fix import order

### Example 2: Unused Import

```bash
Error: `UserModel` imported but unused
```

**Solution**: Remove the import or use it in the code

### Example 3: Line Too Long

```bash
Error: Line too long (120 > 88 characters)
```

**Solution**: Break the line into multiple lines

### Example 4: Missing Docstring

```bash
Error: Missing docstring in public function
```

**Solution**: Add a docstring explaining what the function does

## Remember

✅ Always run linters before telling user work is complete
✅ Run both `ruff format` and `ruff check --fix`
✅ Fix all errors before finishing
✅ Use `ca exec` for running linters
✅ Verify tests still pass after formatting
✅ Clean code = ready for commit
✅ Don't modify `pyproject.toml` without discussion
✅ Fix errors in files you modified first
