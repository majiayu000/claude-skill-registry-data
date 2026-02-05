---
name: shell-workflow
description: Shell script workflow guidelines. Activate when working with shell scripts (.sh), bash scripts, or shell-specific tooling like shellcheck, shfmt.
location: user
---

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

# Shell Script Workflow

## Tool Grid

| Task | Tool | Command |
|------|------|---------|
| Lint | shellcheck | `shellcheck *.sh` |
| Format | shfmt | `shfmt -w *.sh` |
| Coverage | bashcov | `bashcov ./test.sh` |

## Shebang

Scripts MUST use the portable shebang:

```bash
#!/usr/bin/env bash
```

POSIX-only scripts MAY use `#!/bin/sh` when bash features are not needed.

## Strict Mode

All bash scripts MUST enable strict mode at the top:

```bash
set -euo pipefail
```

| Flag | Meaning |
|------|---------|
| `-e` | Exit on error |
| `-u` | Error on undefined variables |
| `-o pipefail` | Fail on pipe errors |

For debugging, scripts MAY temporarily add `set -x` for trace output.

## Size Limit

Scripts SHOULD NOT exceed 100 lines of code (excluding comments and blank lines).

When a script exceeds 100 lines:
- The script SHOULD be refactored into smaller functions
- Complex logic SHOULD be converted to Python for maintainability

## Variable Quoting

Variables MUST be quoted to prevent word splitting and glob expansion:

```bash
# Correct
echo "$variable"
cp "$source" "$destination"

# Incorrect - MUST NOT use
echo $variable
cp $source $destination
```

Arrays MUST use proper expansion:

```bash
# Correct
"${array[@]}"

# For single string with spaces
"${array[*]}"
```

## Variable Naming

| Scope | Convention | Example |
|-------|------------|---------|
| Environment/Global | UPPER_CASE | `LOG_LEVEL`, `CONFIG_PATH` |
| Local/Script | lower_case | `file_count`, `temp_dir` |
| Constants | UPPER_CASE | `readonly MAX_RETRIES=3` |

Constants SHOULD be declared with `readonly`:

```bash
readonly CONFIG_FILE="/etc/app/config"
readonly -a VALID_OPTIONS=("start" "stop" "restart")
```

## Test Syntax

In bash scripts, `[[ ]]` MUST be used over `[ ]`:

```bash
# Correct - bash
if [[ -f "$file" ]]; then
    echo "File exists"
fi

if [[ "$string" == "value" ]]; then
    echo "Match"
fi

# Pattern matching (bash-only)
if [[ "$string" =~ ^[0-9]+$ ]]; then
    echo "Numeric"
fi
```

POSIX scripts MUST use `[ ]` for compatibility.

## Functions

Functions MUST use `local` for internal variables:

```bash
my_function() {
    local input="$1"
    local result=""

    # Process input
    result=$(process "$input")

    echo "$result"
}
```

Function naming conventions:
- Use snake_case: `process_file`, `validate_input`
- Prefix private functions with underscore: `_helper_function`

## Temporary Files

Temporary files MUST be created with `mktemp`:

```bash
temp_file=$(mktemp)
temp_dir=$(mktemp -d)
```

Cleanup MUST be ensured with `trap`:

```bash
cleanup() {
    rm -f "$temp_file"
    rm -rf "$temp_dir"
}
trap cleanup EXIT
```

The `EXIT` trap ensures cleanup runs on normal exit, error, or interrupt.

## Exit Codes

Scripts MUST use standard exit codes:

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error |
| 2 | Misuse (invalid arguments, missing dependencies) |

Example usage:

```bash
main() {
    if [[ $# -lt 1 ]]; then
        echo "Usage: $0 <argument>" >&2
        exit 2
    fi

    if ! process_data "$1"; then
        echo "Error: Processing failed" >&2
        exit 1
    fi

    exit 0
}
```

## Error Handling

### Continuing on Error

Use `|| true` when a command failure SHOULD NOT stop execution:

```bash
rm -f "$optional_file" || true
```

### Explicit Failure

Use `|| exit 1` for critical operations:

```bash
cd "$required_dir" || exit 1
source "$config_file" || exit 1
```

### Custom Error Messages

```bash
command_that_might_fail || {
    echo "Error: command failed" >&2
    exit 1
}
```

## Portability Considerations

### POSIX vs Bash

| Feature | POSIX | Bash |
|---------|-------|------|
| Test syntax | `[ ]` | `[[ ]]` |
| Arrays | Not available | Supported |
| `local` | Not standard | Supported |
| `source` | Use `.` | Both work |
| Process substitution | Not available | `<(cmd)` |

### Portable Alternatives

When POSIX compatibility is REQUIRED:

```bash
# Instead of bash arrays, use positional parameters or newline-separated strings
files=$(find . -name "*.txt")

# Instead of [[ ]], use [ ]
if [ -f "$file" ]; then
    echo "exists"
fi

# Instead of source, use .
. ./config.sh
```

## Input Validation

User input MUST be validated:

```bash
validate_input() {
    local input="$1"

    if [[ -z "$input" ]]; then
        echo "Error: Input cannot be empty" >&2
        return 1
    fi

    if [[ ! "$input" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        echo "Error: Invalid characters in input" >&2
        return 1
    fi

    return 0
}
```

## Command Substitution

Modern syntax MUST be used:

```bash
# Correct
result=$(command)
nested=$(echo $(inner_command))

# Incorrect - MUST NOT use backticks
result=`command`
```

## Logging

Scripts SHOULD include consistent logging:

```bash
log_info() {
    echo "[INFO] $*"
}

log_error() {
    echo "[ERROR] $*" >&2
}

log_debug() {
    [[ "${DEBUG:-0}" == "1" ]] && echo "[DEBUG] $*"
}
```

## Script Template

```bash
#!/usr/bin/env bash
set -euo pipefail

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly SCRIPT_NAME="$(basename "$0")"

usage() {
    cat <<EOF
Usage: $SCRIPT_NAME [options] <argument>

Options:
    -h, --help    Show this help message
    -v, --verbose Enable verbose output

EOF
}

main() {
    local verbose=0

    while [[ $# -gt 0 ]]; do
        case "$1" in
            -h|--help)
                usage
                exit 0
                ;;
            -v|--verbose)
                verbose=1
                shift
                ;;
            *)
                break
                ;;
        esac
    done

    if [[ $# -lt 1 ]]; then
        usage >&2
        exit 2
    fi

    # Script logic here
}

main "$@"
```
