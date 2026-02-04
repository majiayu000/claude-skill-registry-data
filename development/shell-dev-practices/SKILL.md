---
name: shell-dev-practices
description: Shell scripting best practices for bash, sh, zsh with focus on error handling, portability, and automation.
---

# Shell development practices

## Purpose

Guide for shell scripting best practices covering POSIX compatibility, error handling, and robust automation scripts.

## When to use

This skill activates when:

- Writing shell scripts
- Creating build/deploy automation
- Writing bash/sh/zsh code
- Debugging shell issues
- Making scripts portable

## Core principles

### Always use strict mode

```bash
#!/usr/bin/env bash
set -euo pipefail

# -e: Exit on error
# -u: Error on undefined variables
# -o pipefail: Fail on pipe errors
```

### Quote all variables

```bash
# Bad: Word splitting and glob expansion
echo $filename
rm $path/*

# Good: Properly quoted
echo "$filename"
rm "$path"/*
```

## Error handling

### Trap for cleanup

```bash
#!/usr/bin/env bash
set -euo pipefail

TEMP_DIR=""

cleanup() {
    if [[ -n "$TEMP_DIR" && -d "$TEMP_DIR" ]]; then
        rm -rf "$TEMP_DIR"
    fi
}

trap cleanup EXIT

TEMP_DIR=$(mktemp -d)
# Use temp dir...
```

### Check command existence

```bash
# Check if command exists
if ! command -v git &> /dev/null; then
    echo "Error: git is required but not installed" >&2
    exit 1
fi
```

### Validate inputs

```bash
validate_args() {
    if [[ $# -lt 1 ]]; then
        echo "Usage: $0 <filename>" >&2
        exit 1
    fi

    if [[ ! -f "$1" ]]; then
        echo "Error: File not found: $1" >&2
        exit 1
    fi
}

validate_args "$@"
```

## Functions

### Function definitions

```bash
# Good: Local variables, clear return
process_file() {
    local file="$1"
    local output=""

    if [[ ! -f "$file" ]]; then
        return 1
    fi

    output=$(cat "$file")
    echo "$output"
}
```

### Return values

```bash
# Use return for status, echo for output
get_value() {
    local key="$1"

    if [[ -z "$key" ]]; then
        return 1
    fi

    echo "value_for_$key"
}

# Capture output
if value=$(get_value "mykey"); then
    echo "Got: $value"
else
    echo "Failed to get value"
fi
```

## Conditionals

### Test syntax

```bash
# Modern syntax with [[]]
if [[ -f "$file" ]]; then
    echo "File exists"
fi

# String comparison
if [[ "$string" == "value" ]]; then
    echo "Match"
fi

# Numeric comparison
if [[ "$count" -gt 10 ]]; then
    echo "Greater than 10"
fi
```

### Common tests

```bash
# File tests
[[ -f "$path" ]]  # Regular file
[[ -d "$path" ]]  # Directory
[[ -e "$path" ]]  # Exists
[[ -r "$path" ]]  # Readable
[[ -w "$path" ]]  # Writable
[[ -x "$path" ]]  # Executable

# String tests
[[ -z "$var" ]]   # Empty
[[ -n "$var" ]]   # Not empty
[[ "$a" == "$b" ]] # Equal
[[ "$a" != "$b" ]] # Not equal
```

## Arrays

```bash
# Declare array
declare -a files=()

# Add elements
files+=("file1.txt")
files+=("file2.txt")

# Iterate
for file in "${files[@]}"; do
    echo "Processing: $file"
done

# Array length
echo "Count: ${#files[@]}"
```

## Input handling

### Reading input

```bash
# Read line
read -r line < "$file"

# Read with prompt
read -rp "Enter name: " name

# Read password
read -rsp "Enter password: " password
echo  # newline after hidden input
```

### Process arguments

```bash
#!/usr/bin/env bash
set -euo pipefail

usage() {
    echo "Usage: $0 [-v] [-o output] input"
    exit 1
}

verbose=false
output=""

while getopts "vo:" opt; do
    case $opt in
        v) verbose=true ;;
        o) output="$OPTARG" ;;
        *) usage ;;
    esac
done

shift $((OPTIND - 1))

if [[ $# -lt 1 ]]; then
    usage
fi

input="$1"
```

## Output

### Logging

```bash
# Log levels
log_info() { echo "[INFO] $*"; }
log_warn() { echo "[WARN] $*" >&2; }
log_error() { echo "[ERROR] $*" >&2; }

# Usage
log_info "Starting process"
log_error "Failed to open file"
```

### Colors (optional)

```bash
# Only use if terminal supports it
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    NC=''
fi

echo -e "${GREEN}Success${NC}"
echo -e "${RED}Error${NC}"
```

## Portability

### POSIX compatibility

```bash
# More portable alternatives
# Instead of: echo -e
printf '%s\n' "$message"

# Instead of: [[ ]]
[ -f "$file" ]

# Instead of: $()
`command`  # Though $() is preferred when available
```

### Path handling

```bash
# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Resolve symlinks
REAL_PATH="$(realpath "$path")"
```

## ShellCheck

Always validate with ShellCheck:

```bash
# Install
brew install shellcheck  # macOS
apt install shellcheck   # Ubuntu

# Run
shellcheck script.sh
```

## Checklist

- [ ] Uses `set -euo pipefail`
- [ ] All variables quoted
- [ ] Functions use local variables
- [ ] Cleanup with trap
- [ ] Inputs validated
- [ ] ShellCheck passes

---

**Additional resources:**

- [Bash manual](https://www.gnu.org/software/bash/manual/)
- [ShellCheck](https://www.shellcheck.net/)
