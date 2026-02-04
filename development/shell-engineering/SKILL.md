---
name: shell-engineering
description: Comprehensive shell/bash engineering guidelines based on Google's Shell Style Guide. This skill should be used when writing shell scripts, reviewing bash code, or answering questions about shell scripting best practices. Applies to .sh files, bash scripts, and any shell programming tasks.
---

# Shell Engineering

Comprehensive guidelines for writing production-quality shell scripts based on Google's Shell Style Guide.

## When to Use Shell

- Small utilities and simple wrapper scripts
- Scripts calling other tools with straightforward logic
- **Rewrite in a structured language (Go, Python) when exceeding ~100 lines or using complex control flow**

## Shell Choice

- Bash is the only permitted shell for executables
- Start scripts with `#!/bin/bash` with minimal flags
- Libraries must have `.sh` extension and not be executable
- SUID/SGID are forbidden on shell scripts

## File Structure

```bash
#!/bin/bash
#
# Brief description of the script's purpose.

set -euo pipefail

# Constants and environment variables (UPPERCASE)
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/tmp/script.log"

# Source libraries
source "${SCRIPT_DIR}/lib/utils.sh"

# Function definitions (lowercase_with_underscores)
my_function() {
  local arg1="$1"
  # ...
}

# Main function
main() {
  # Script logic here
}

main "$@"
```

## Formatting Rules

### Indentation and Length
- **2 spaces** for indentation (no tabs)
- **80 characters** maximum line length
- Split long pipelines with pipe at line start:

```bash
command1 \
  | command2 \
  | command3
```

### Control Structures
- `; then` and `; do` on same line as `if`/`while`/`for`:

```bash
if [[ -n "${var}" ]]; then
  # ...
fi

for file in "${files[@]}"; do
  # ...
done
```

### Quoting
- Always quote strings with variables, command substitutions, or spaces
- Use `"${var}"` format with braces for clarity
- Use `"$@"` not `$*` for argument lists
- Use arrays for lists with spaces in elements

## Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Functions | `lowercase_underscores` | `process_file()` |
| Variables | `lowercase_underscores` | `file_count` |
| Constants | `UPPERCASE_UNDERSCORES` | `readonly MAX_RETRIES=3` |
| Environment vars | `UPPERCASE` | `export PATH` |
| Source files | `lowercase_underscores.sh` | `string_utils.sh` |

## Preferred Syntax

### Use These

```bash
# Command substitution
result=$(command)

# Test conditions
if [[ -n "${var}" ]]; then

# Arithmetic
if (( count > 10 )); then
total=$(( a + b ))

# Local variables in functions
my_func() {
  local name="$1"
}

# Arrays for lists
files=("file1.txt" "file2.txt" "file with spaces.txt")
for f in "${files[@]}"; do
```

### Avoid These

```bash
# Backticks (use $() instead)
result=`command`

# Single brackets (use [[ ]] instead)
if [ -n "$var" ]; then

# let, expr, $[ ] (use $(( )) instead)
let count=count+1

# eval (security risk)
eval "$cmd"

# Piping to while (loses variable scope)
cat file | while read line; do

# alias in scripts (use functions)
alias ll='ls -la'

# Unquoted wildcards
for f in *; do  # Use ./* instead
```

## Error Handling

### STDERR for Errors
```bash
err() {
  echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

if ! process_file "${file}"; then
  err "Failed to process ${file}"
  exit 1
fi
```

### Check Return Values
```bash
# Direct if check
if ! mv "${file}" "${dest}"; then
  err "Failed to move file"
fi

# Pipeline status
tar -cf - . | gzip > archive.tar.gz
if (( PIPESTATUS[0] != 0 || PIPESTATUS[1] != 0 )); then
  err "Archive creation failed"
fi
```

## Comments and Documentation

### File Header (Required)
```bash
#!/bin/bash
#
# Script description explaining purpose and usage.
#
# Usage: script.sh [options] <input_file>
```

### Function Documentation
```bash
#######################################
# Process a data file and output results.
# Globals:
#   OUTPUT_DIR
# Arguments:
#   $1 - Input file path
#   $2 - Output format (csv|json)
# Outputs:
#   Writes processed data to OUTPUT_DIR
# Returns:
#   0 on success, non-zero on error
#######################################
process_data() {
  local input_file="$1"
  local format="${2:-csv}"
  # ...
}
```

### TODO Comments
```bash
# TODO(username): Handle edge case for empty input
```

## Testing and Validation

- Use [ShellCheck](https://www.shellcheck.net/) to identify bugs
- Test string emptiness explicitly:

```bash
# Good
if [[ -z "${var}" ]]; then  # empty
if [[ -n "${var}" ]]; then  # non-empty

# Avoid
if [[ "${var}" ]]; then
```

## Built-in Preference

Prefer bash builtins over external commands:

```bash
# Good: parameter expansion
filename="${path##*/}"
extension="${filename##*.}"
basename="${filename%.*}"

# Avoid: external commands
filename=$(basename "$path")
extension=$(echo "$filename" | sed 's/.*\.//')
```

## Quick Reference

| Do | Don't |
|----|-------|
| `$(command)` | `` `command` `` |
| `[[ condition ]]` | `[ condition ]` |
| `(( arithmetic ))` | `let`, `expr` |
| `"${var}"` | `$var` |
| `"$@"` | `$*` |
| `local var` | global variables in functions |
| `./*` wildcards | `*` wildcards |
| functions | aliases |
| arrays | space-separated strings |
