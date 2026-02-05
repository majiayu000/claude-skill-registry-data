---
name: shellcheck
description: Lint and fix shell script issues using ShellCheck. Use when the user says "check this script", "lint shell", "shellcheck", "fix script warnings", "validate bash", or asks to review a shell script for issues.
allowed-tools: Bash, Read, Edit
---

# ShellCheck

Lint shell scripts and fix common issues using ShellCheck.

## Instructions

1. Run ShellCheck on the script
2. Analyze findings by severity
3. Explain each issue clearly
4. Provide fixes for each issue

## Run ShellCheck

```bash
# Basic check
shellcheck script.sh

# With severity filter
shellcheck --severity=warning script.sh

# Specific shell dialect
shellcheck --shell=bash script.sh

# Output formats
shellcheck --format=json script.sh
shellcheck --format=gcc script.sh

# Check multiple files
shellcheck *.sh
```

## Common issues and fixes

### SC2086: Double quote to prevent globbing

```bash
# Bad
rm $file
echo $var

# Good
rm "$file"
echo "$var"
```

### SC2046: Quote command substitution

```bash
# Bad
rm $(find . -name "*.tmp")

# Good
rm "$(find . -name "*.tmp")"
# Or for multiple results:
find . -name "*.tmp" -delete
```

### SC2006: Use $() instead of backticks

```bash
# Bad
date=`date`

# Good
date=$(date)
```

### SC2164: Use cd ... || exit

```bash
# Bad
cd /some/dir
do_something

# Good
cd /some/dir || exit 1
do_something
```

### SC2155: Declare and assign separately

```bash
# Bad
local var=$(command)

# Good
local var
var=$(command)
```

### SC2162: Read without -r mangles backslashes

```bash
# Bad
read line

# Good
read -r line
```

### SC2034: Variable appears unused

```bash
# Check if it's exported or used in eval/source
# Or prefix with _ to indicate intentionally unused
_unused_var="value"
```

## Disable warnings

```bash
# Disable for next line
# shellcheck disable=SC2086
echo $unquoted_var

# Disable for entire file (at top)
# shellcheck disable=SC2034,SC2086

# Disable for block
# shellcheck disable=SC2086
{
    echo $var1
    echo $var2
}
```

## Output format

```
## Issues Found

### Errors (must fix)
- Line 10, SC2086: Double quote to prevent globbing and word splitting

### Warnings (should fix)
- Line 15, SC2155: Declare and assign separately to avoid masking return values

### Suggestions
- Line 20, SC2034: UNUSED_VAR appears unused (verify or prefix with _)

## Fixed Code
[Show corrected version]
```

## Rules

- MUST run shellcheck before reviewing manually
- MUST explain why each issue matters
- MUST provide specific fix for each issue
- Never ignore errors (SC level error)
- Always explain when disabling is appropriate
- Offer to auto-fix simple issues with Edit tool
