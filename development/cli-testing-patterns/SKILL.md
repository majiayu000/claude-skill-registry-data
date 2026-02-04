---
name: CLI Testing Patterns
description: This skill should be used when performing exploratory testing of command-line tools and scripts, including help text validation, option testing, error handling verification, and output validation. Triggers when testing CLI commands, scripts, build tools, or command-line interfaces.
version: 0.1.0
---

# CLI Testing Patterns

## Purpose

Provide systematic patterns for autonomous command-line tool exploratory testing. Guide agents through comprehensive CLI testing including help discovery, option validation, error handling checks, exit code verification, and output correctness testing.

## Core Testing Methodology

### Systematic CLI Testing Approach

Test command-line tools using a structured approach:

1. **Discovery**: Find command and understand its options
2. **Basic smoke test**: Verify command runs
3. **Help validation**: Check help text completeness
4. **Option testing**: Test all flags and arguments
5. **Error handling**: Test edge cases and invalid inputs
6. **Output validation**: Verify correctness and formatting
7. **Scoped comprehensive testing**: Focus on changed areas

### CLI Discovery Methods

Identify command to test from context:

**Script path**: `./scripts/build.sh`
**Binary name**: `mycommand`
**Package.json script**: `npm run test`
**System command**: `git status`

Verify command exists:
```bash
which mycommand
command -v mycommand
[ -f ./script.sh ] && echo "exists"
```

## Help Text Discovery

### Common Help Patterns

Try these flags to discover usage:

```bash
command --help
command -h
command help
command
```

### Parse Help Output

Extract from help text:
- Available options/flags
- Required vs optional arguments
- Expected input formats
- Subcommands (if applicable)
- Usage examples

Example help parsing:
```markdown
Usage: deploy [options] <environment>

Options:
  -v, --verbose    Enable verbose output
  -d, --dry-run    Show what would be deployed
  --config <file>  Use custom config

Identifies:
- Required: <environment>
- Optional flags: -v, -d, --config
- Config file option
```

## Smoke Testing

### Basic Execution Tests

Test command works at all:

```bash
# Version check
command --version
command -v

# No arguments (if allowed)
command

# Help (should never error)
command --help
```

Verify:
- Command executes without crashing
- Returns appropriate exit code
- Produces expected output or error

## Comprehensive Option Testing

### Test All Flags

For each discovered flag:

```markdown
1. Test flag alone: `command --flag`
2. Test with valid value: `command --flag value`
3. Test with invalid value: `command --flag invalid`
4. Test flag combinations: `command --flag1 --flag2`
5. Test conflicting flags: `command --yes --no`
```

### Argument Testing

Test required and optional arguments:

```markdown
Valid inputs:
- Correct type and format
- Boundary values (min/max)
- Typical use cases

Invalid inputs:
- Wrong type (string instead of number)
- Out of range (negative when positive required)
- Missing required arguments
- Too many arguments
- Special characters
```

### Scoped Testing Strategy

Focus testing based on context:

```markdown
If context says "I updated the --config flag":
- Comprehensive tests on --config
  - Valid config files
  - Invalid config files
  - Missing config files
  - Malformed config data
- Smoke tests on other flags (ensure still work)
- Quick validation on core functionality

Balance depth with scope:
- Changed areas: Comprehensive testing
- Related areas: Thorough testing
- Unrelated areas: Smoke testing only
```

## Error Handling Validation

### Exit Codes

Verify proper exit codes:

```markdown
Success: Exit 0
General error: Exit 1
Usage error: Exit 2
Permission denied: Exit 126
Command not found: Exit 127
```

Test:
```bash
command; echo "Exit code: $?"
```

### Error Messages

Validate error messages are:
- **Clear**: Explain what went wrong
- **Actionable**: Suggest how to fix
- **Specific**: Not generic "error occurred"
- **Helpful**: Include relevant details

**Good error:**
```
Error: Config file 'config.json' not found.
Please create a config file or specify path with --config
```

**Bad error:**
```
Error
```

### stderr vs stdout

Verify output streams used correctly:

```bash
# Errors should go to stderr
command 2>&1 | grep "Error" # Should find errors here

# Normal output should go to stdout
command 2>/dev/null # Should show normal output
```

## Output Validation

### Format Validation

Check output is correctly formatted:

**JSON output:**
```bash
command --json | jq . # Should parse without error
```

**CSV output:**
```bash
command --csv | head -1 # Check headers present
```

**Table output:**
```bash
command --table | column # Check column alignment
```

### Correctness Validation

Verify output matches expected:

```markdown
Known inputs → Verify outputs:
1. Use predictable test data
2. Run command
3. Parse output
4. Verify values match expected
5. Report discrepancies
```

## Test Data Management

### Using Test Data Generators

Check for test data support:

```bash
# Common patterns
command test generate
command fixtures create
command seed --test
```

If available:
- Use for realistic testing
- More comprehensive coverage
- Matches app's data model

### Creating Temporary Data

When generating test data:

```bash
# Create temp directory
TMPDIR=$(mktemp -d)

# Create test files
echo "test data" > "$TMPDIR/test.txt"

# Run command with test data
command --input "$TMPDIR/test.txt"

# Cleanup
rm -rf "$TMPDIR"
```

### Safe Test Data

Generate data that:
- Doesn't interfere with real data
- Uses temporary locations (/tmp)
- Avoids destructive operations
- Is properly cleaned up after testing

## Common CLI Issues

### Missing Help Text

**Issue**: No --help flag or unclear help
**Impact**: Users don't know how to use command
**Test**: Try `command --help`
**Report**: Missing or inadequate help text

### Poor Error Messages

**Issue**: Cryptic or missing error messages
**Impact**: Users can't diagnose problems
**Test**: Trigger errors, check messages
**Report**: Unhelpful error messages

### Inconsistent Exit Codes

**Issue**: Command always exits 0 even on errors
**Impact**: Scripts can't detect failures
**Test**: Cause error, check exit code
**Report**: Exit code should be non-zero on error

### Destructive Defaults

**Issue**: Dangerous operations without confirmation
**Impact**: Accidental data loss
**Test**: Run potentially destructive commands
**Report**: Should require --force flag or confirmation

### Missing Input Validation

**Issue**: Accepts invalid inputs without error
**Impact**: Silent failures or unexpected behavior
**Test**: Provide malformed inputs
**Report**: Should validate and reject bad inputs

## Testing Workflow

### Complete CLI Test Flow

```markdown
1. Discover command and help text
2. Run smoke tests (version, help, basic execution)
3. Test each flag individually
4. Test flag combinations
5. Test with valid arguments
6. Test with invalid arguments
7. Test edge cases (empty, very long, special chars)
8. Verify exit codes
9. Validate error messages
10. Check output formatting
11. Report findings by severity
```

## Reporting Template

```markdown
## Critical Issues ❌

### Command Crashes on Empty Input - Critical
- **Command**: `deploy`
- **Issue**: Crashes when no environment specified
- **Test**:
  ```bash
  ./deploy.sh
  ```
- **Exit Code**: 139 (Segmentation fault)
- **Expected**: Exit 2 with usage message
- **Impact**: Confusing user experience, possibly destructive

## Error Handling Issues ⚠️

### Unhelpful Error Message - Medium
- **Command**: `deploy --config invalid.json`
- **Issue**: Error message doesn't explain problem
- **Output**: `Error: Invalid config`
- **Better**: `Error: Config file 'invalid.json' not found. Expected JSON file with keys: ...`

## Documentation Issues 📝

### Missing --help Flag - Medium
- **Command**: `deploy --help`
- **Issue**: No help text available
- **Output**: `Unknown option: --help`
- **Expected**: Usage information and option descriptions

## Tests Passed ✅

- Command executes successfully with valid inputs
- Exit codes are correct (0 for success, 1 for errors)
- Verbose flag produces additional output
- Version flag shows current version
```

## Additional Resources

For complete CLI testing procedures, see:
- **`references/exit-code-standards.md`** - Exit code conventions and validation
- **`references/output-validation.md`** - Output format testing patterns
