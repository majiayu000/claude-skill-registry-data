---
name: bash-defensive-patterns
description: Use when writing or reviewing Bash scripts to apply defensive programming patterns including strict mode, proper error handling, safe variable handling, argument parsing, and idempotent design. Ensures scripts are robust, maintainable, and production-ready.
---

# Bash Defensive Patterns

## Overview

Apply defensive programming patterns to write robust, maintainable Bash scripts that handle errors gracefully and fail safely.

**Core principle:** Scripts should be safe by default, fail fast, and provide clear error messages.

## When to Use

- Writing new Bash scripts
- Reviewing existing shell scripts
- Debugging script failures
- Hardening automation scripts
- Creating production-ready scripts

## Defensive Foundations

### 1. Strict Mode (Always Required)

Use at the beginning of every script:

```bash
#!/bin/bash
set -Eeuo pipefail
```

**What each flag does:**

- `-e` - Exit immediately if any command fails
- `-E` - Inherit ERR trap by functions and subshells
- `-u` - Treat unset variables as errors
- `-o pipefail` - Exit if any command in a pipeline fails

### 2. Error Trapping

Catch and handle errors gracefully:

```bash
#!/bin/bash
set -Eeuo pipefail

cleanup() {
    local exit_code=$?
    echo "Cleanup triggered with exit code: $exit_code" >&2
    # Cleanup operations here
    rm -f "$TMPFILE" 2>/dev/null || true
}

trap cleanup EXIT
trap 'echo "Error on line $LINENO" >&2' ERR
```

### 3. Variable Quoting

Quote all variable expansions to prevent word splitting and globbing:

```bash
# Good - quoted
file_path="/path/to/my file.txt"
cp "$file_path" "$destination"

# Bad - unquoted (breaks with spaces)
cp $file_path $destination

# Use readonly for constants
readonly CONFIG_FILE="/etc/myapp/config"
readonly MAX_RETRIES=3

# Local variables in functions
function_name() {
    local -r required_arg="$1"
    local optional_arg="${2:-default}"
}
```

### 4. Array Handling

Use arrays properly for lists:

```bash
# Define arrays
files=("file1.txt" "file2.txt" "file3.txt")
items=("item 1" "item 2" "item 3")

# Iterate safely
for item in "${items[@]}"; do
    echo "Processing: $item"
done

# Read output into array safely
mapfile -t lines < <(some_command)
readarray -t numbers < <(seq 1 10)
```

### 5. Conditional Safety

Use `[[ ]]` for Bash-specific features, `[ ]` for POSIX:

```bash
# Bash - safer
if [[ -f "$file" && -r "$file" ]]; then
    content=$(<"$file")
fi

# POSIX - portable
if [ -f "$file" ] && [ -r "$file" ]; then
    content=$(cat "$file")
fi

# Test for existence before operations
if [[ -z "${VAR:-}" ]]; then
    echo "VAR is not set or is empty"
fi
```

## Fundamental Patterns

### Pattern 1: Safe Script Directory Detection

```bash
#!/bin/bash
set -Eeuo pipefail

# Correctly determine script directory
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd -P)"
SCRIPT_NAME="$(basename -- "${BASH_SOURCE[0]}")"

echo "Script location: $SCRIPT_DIR/$SCRIPT_NAME"
```

### Pattern 2: Comprehensive Function Template

```bash
#!/bin/bash
set -Eeuo pipefail

# Prefix for functions: handle_*, process_*, check_*, validate_*
# Include documentation and error handling

validate_file() {
    local -r file="$1"
    local -r message="${2:-File not found: $file}"

    if [[ ! -f "$file" ]]; then
        echo "ERROR: $message" >&2
        return 1
    fi
    return 0
}

process_files() {
    local -r input_dir="$1"
    local -r output_dir="$2"

    # Validate inputs
    [[ -d "$input_dir" ]] || { echo "ERROR: input_dir not a directory" >&2; return 1; }

    # Create output directory if needed
    mkdir -p "$output_dir" || { echo "ERROR: Cannot create output_dir" >&2; return 1; }

    # Process files safely
    while IFS= read -r -d '' file; do
        echo "Processing: $file"
        # Do work
    done < <(find "$input_dir" -maxdepth 1 -type f -print0)

    return 0
}
```

### Pattern 3: Safe Temporary File Handling

```bash
#!/bin/bash
set -Eeuo pipefail

trap 'rm -rf -- "$TMPDIR"' EXIT

# Create temporary directory
TMPDIR=$(mktemp -d) || { echo "ERROR: Failed to create temp directory" >&2; exit 1; }

# Create temporary files in directory
TMPFILE1="$TMPDIR/temp1.txt"
TMPFILE2="$TMPDIR/temp2.txt"

# Use temporary files
touch "$TMPFILE1" "$TMPFILE2"

echo "Temp files created in: $TMPDIR"
```

### Pattern 4: Robust Argument Parsing

```bash
#!/bin/bash
set -Eeuo pipefail

# Default values
VERBOSE=false
DRY_RUN=false
OUTPUT_FILE=""
THREADS=4

usage() {
    cat <<EOF
Usage: $0 [OPTIONS]

Options:
    -v, --verbose       Enable verbose output
    -d, --dry-run       Run without making changes
    -o, --output FILE   Output file path
    -j, --jobs NUM      Number of parallel jobs
    -h, --help          Show this help message
EOF
    exit "${1:-0}"
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -d|--dry-run)
            DRY_RUN=true
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -j|--jobs)
            THREADS="$2"
            shift 2
            ;;
        -h|--help)
            usage 0
            ;;
        --)
            shift
            break
            ;;
        *)
            echo "ERROR: Unknown option: $1" >&2
            usage 1
            ;;
    esac
done

# Validate required arguments
[[ -n "$OUTPUT_FILE" ]] || { echo "ERROR: -o/--output is required" >&2; usage 1; }
```

### Pattern 5: Structured Logging

```bash
#!/bin/bash
set -Eeuo pipefail

# Define logging functions
log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" >&2
}

log_warn() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] WARN: $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

log_debug() {
    if [[ "${DEBUG:-0}" == "1" ]]; then
        echo "[$(date +'%Y-%m-%d %H:%M:%S')] DEBUG: $*" >&2
    fi
}

# Usage examples
log_info "Starting script"
log_debug "Debug information"
log_warn "Warning message"
log_error "Error occurred"
```

### Pattern 6: Process Orchestration with Signals

```bash
#!/bin/bash
set -Eeuo pipefail

# Track background processes
PIDS=()

cleanup() {
    log_info "Shutting down..."

    # Terminate all background processes
    for pid in "${PIDS[@]}"; do
        if kill -0 "$pid" 2>/dev/null; then
            kill -TERM "$pid" 2>/dev/null || true
        fi
    done

    # Wait for graceful shutdown
    for pid in "${PIDS[@]}"; do
        wait "$pid" 2>/dev/null || true
    done
}

trap cleanup SIGTERM SIGINT

# Start background tasks
background_task &
PIDS+=($!)

another_task &
PIDS+=($!)

# Wait for all background processes
wait
```

### Pattern 7: Safe File Operations

```bash
#!/bin/bash
set -Eeuo pipefail

# Move files safely without overwriting
safe_move() {
    local -r source="$1"
    local -r dest="$2"

    if [[ ! -e "$source" ]]; then
        echo "ERROR: Source does not exist: $source" >&2
        return 1
    fi

    if [[ -e "$dest" ]]; then
        echo "ERROR: Destination already exists: $dest" >&2
        return 1
    fi

    mv "$source" "$dest"
}

# Safe directory cleanup
safe_rmdir() {
    local -r dir="$1"

    if [[ ! -d "$dir" ]]; then
        echo "ERROR: Not a directory: $dir" >&2
        return 1
    fi

    # Prompt before deletion
    rm -rI -- "$dir"
}

# Atomic file writes
atomic_write() {
    local -r target="$1"
    local -r tmpfile
    tmpfile=$(mktemp) || return 1

    # Write to temp file first
    cat > "$tmpfile"

    # Atomic rename
    mv "$tmpfile" "$target"
}
```

### Pattern 8: Idempotent Script Design

```bash
#!/bin/bash
set -Eeuo pipefail

# Check if resource already exists
ensure_directory() {
    local -r dir="$1"

    if [[ -d "$dir" ]]; then
        log_info "Directory already exists: $dir"
        return 0
    fi

    mkdir -p "$dir" || {
        log_error "Failed to create directory: $dir"
        return 1
    }

    log_info "Created directory: $dir"
}

# Ensure configuration state
ensure_config() {
    local -r config_file="$1"
    local -r default_value="$2"

    if [[ ! -f "$config_file" ]]; then
        echo "$default_value" > "$config_file"
        log_info "Created config: $config_file"
    fi
}

# Rerunning script multiple times should be safe
ensure_directory "/var/cache/myapp"
ensure_config "/etc/myapp/config" "DEBUG=false"
```

### Pattern 9: Safe Command Substitution

```bash
#!/bin/bash
set -Eeuo pipefail

# Use $() instead of backticks
name=$(<"$file")  # Modern, safe variable assignment from file
output=$(command -v python3)  # Get command location safely

# Handle command substitution with error checking
result=$(command -v node) || {
    log_error "node command not found"
    return 1
}

# For multiple lines
mapfile -t lines < <(grep "pattern" "$file")

# NUL-safe iteration
while IFS= read -r -d '' file; do
    echo "Processing: $file"
done < <(find /path -type f -print0)
```

### Pattern 10: Dry-Run Support

```bash
#!/bin/bash
set -Eeuo pipefail

DRY_RUN="${DRY_RUN:-false}"

run_cmd() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] Would execute: $*"
        return 0
    fi

    "$@"
}

# Usage examples
run_cmd cp "$source" "$dest"
run_cmd rm "$file"
run_cmd chown "$owner" "$target"
```

## Advanced Defensive Techniques

### Named Parameters Pattern

```bash
#!/bin/bash
set -Eeuo pipefail

process_data() {
    local input_file=""
    local output_dir=""
    local format="json"

    # Parse named parameters
    while [[ $# -gt 0 ]]; do
        case "$1" in
            --input=*)
                input_file="${1#*=}"
                ;;
            --output=*)
                output_dir="${1#*=}"
                ;;
            --format=*)
                format="${1#*=}"
                ;;
            *)
                echo "ERROR: Unknown parameter: $1" >&2
                return 1
                ;;
        esac
        shift
    done

    # Validate required parameters
    [[ -n "$input_file" ]] || { echo "ERROR: --input is required" >&2; return 1; }
    [[ -n "$output_dir" ]] || { echo "ERROR: --output is required" >&2; return 1; }
}
```

### Dependency Checking

```bash
#!/bin/bash
set -Eeuo pipefail

check_dependencies() {
    local -a missing_deps=()
    local -a required=("jq" "curl" "git")

    for cmd in "${required[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing_deps+=("$cmd")
        fi
    done

    if [[ ${#missing_deps[@]} -gt 0 ]]; then
        echo "ERROR: Missing required commands: ${missing_deps[*]}" >&2
        return 1
    fi
}

check_dependencies
```

## Real-World Examples

### Example 1: Backup Script with Rotation

```bash
#!/bin/bash
set -Eeuo pipefail

# Configuration
readonly BACKUP_SOURCE="/var/www/html"
readonly BACKUP_DEST="/backup/website"
readonly MAX_BACKUPS=7
readonly TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Setup logging
log_info() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] INFO: $*" >&2
}

log_error() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $*" >&2
}

# Cleanup temporary files on exit
cleanup() {
    if [[ -n "${TEMP_ARCHIVE:-}" && -f "$TEMP_ARCHIVE" ]]; then
        rm -f "$TEMP_ARCHIVE"
    fi
}

trap cleanup EXIT

# Validate source directory exists
[[ -d "$BACKUP_SOURCE" ]] || {
    log_error "Source directory not found: $BACKUP_SOURCE"
    exit 1
}

# Create backup destination if needed
mkdir -p "$BACKUP_DEST" || {
    log_error "Cannot create backup directory: $BACKUP_DEST"
    exit 1
}

# Create backup with atomic write
TEMP_ARCHIVE=$(mktemp) || exit 1
log_info "Creating backup archive..."

tar -czf "$TEMP_ARCHIVE" -C "$(dirname "$BACKUP_SOURCE")" "$(basename "$BACKUP_SOURCE")" || {
    log_error "Failed to create backup archive"
    exit 1
}

# Move to final location atomically
FINAL_BACKUP="$BACKUP_DEST/backup_$TIMESTAMP.tar.gz"
mv "$TEMP_ARCHIVE" "$FINAL_BACKUP"
log_info "Backup saved to: $FINAL_BACKUP"

# Rotate old backups
log_info "Rotating old backups..."
while IFS= read -r -d '' backup; do
    rm -f "$backup"
    log_info "Removed old backup: $(basename "$backup")"
done < <(find "$BACKUP_DEST" -name "backup_*.tar.gz" -type f -print0 | sort -z | head -z -n -"$MAX_BACKUPS")

log_info "Backup completed successfully"
```

### Example 2: Deploy Script with Validation

```bash
#!/bin/bash
set -Eeuo pipefail

# Script configuration
DEPLOY_ENV="${DEPLOY_ENV:-staging}"
DRY_RUN="${DRY_RUN:-false}"

# Validate environment
case "$DEPLOY_ENV" in
    staging|production)
        readonly DEPLOY_PATH="/var/www/$DEPLOY_ENV"
        readonly SERVICE_NAME="app-$DEPLOY_ENV"
        ;;
    *)
        echo "ERROR: Invalid environment: $DEPLOY_ENV (must be staging or production)" >&2
        exit 1
        ;;
esac

# Check required commands
check_dependencies() {
    local -a required=("rsync" "systemctl" "git")
    local -a missing=()

    for cmd in "${required[@]}"; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "ERROR: Missing required commands: ${missing[*]}" >&2
        return 1
    fi
}

# Execute command with dry-run support
run_cmd() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY RUN] Would execute: $*"
        return 0
    fi
    "$@"
}

# Main deployment
check_dependencies

echo "Deploying to: $DEPLOY_ENV"
echo "Deploy path: $DEPLOY_PATH"

# Create backup before deployment
BACKUP_DIR="$DEPLOY_PATH.backup.$(date +%Y%m%d_%H%M%S)"
run_cmd cp -a "$DEPLOY_PATH" "$BACKUP_DIR"

# Deploy new code
run_cmd rsync -av --delete ./build/ "$DEPLOY_PATH/"

# Restart service
run_cmd systemctl restart "$SERVICE_NAME"

echo "Deployment completed successfully"
echo "Backup available at: $BACKUP_DIR"
```

### Example 3: Log Processing Pipeline

```bash
#!/bin/bash
set -Eeuo pipefail

# Process and analyze log files from multiple sources
readonly LOG_DIR="/var/log/apps"
readonly OUTPUT_FILE="/tmp/log_analysis_$(date +%Y%m%d).txt"
readonly ERROR_THRESHOLD=100

# Process logs safely
process_logs() {
    local -r log_pattern="$1"
    local error_count=0
    
    while IFS= read -r -d '' logfile; do
        if [[ ! -r "$logfile" ]]; then
            echo "WARNING: Cannot read file: $logfile" >&2
            continue
        fi
        
        # Count errors in this log file
        local file_errors
        file_errors=$(grep -c "ERROR" "$logfile" 2>/dev/null || echo "0")
        error_count=$((error_count + file_errors))
        
        echo "$(basename "$logfile"): $file_errors errors"
    done < <(find "$LOG_DIR" -name "$log_pattern" -type f -print0)
    
    echo "---"
    echo "Total errors: $error_count"
    
    # Alert if threshold exceeded
    if [[ $error_count -gt $ERROR_THRESHOLD ]]; then
        echo "WARNING: Error count ($error_count) exceeds threshold ($ERROR_THRESHOLD)" >&2
        return 1
    fi
    
    return 0
}

# Validate log directory exists
[[ -d "$LOG_DIR" ]] || {
    echo "ERROR: Log directory not found: $LOG_DIR" >&2
    exit 1
}

# Process logs and save results
{
    echo "Log Analysis Report - $(date)"
    echo "================================"
    echo ""
    process_logs "*.log"
} > "$OUTPUT_FILE"

echo "Analysis complete. Results saved to: $OUTPUT_FILE"
```

## Best Practices Summary

1. **Always use strict mode** - `set -Eeuo pipefail`
2. **Quote all variables** - `"$variable"` prevents word splitting
3. **Use `[[ ]]` conditionals** - More robust than `[ ]`
4. **Implement error trapping** - Catch and handle errors gracefully
5. **Validate all inputs** - Check file existence, permissions, formats
6. **Use functions for reusability** - Prefix with meaningful names
7. **Implement structured logging** - Include timestamps and levels
8. **Support dry-run mode** - Allow users to preview changes
9. **Handle temporary files safely** - Use mktemp, cleanup with trap
10. **Design for idempotency** - Scripts should be safe to rerun
11. **Document requirements** - List dependencies and minimum versions
12. **Test error paths** - Ensure error handling works correctly
13. **Use `command -v`** - Safer than `which` for checking executables
14. **Prefer printf over echo** - More predictable across systems

## Resources

- [Bash Strict Mode](http://redsymbol.net/articles/unofficial-bash-strict-mode/)
- [Google Shell Style Guide](https://google.github.io/styleguide/shellguide.html)
- [Defensive BASH Programming](https://kfirlavi.herokuapp.com/blog/2012/11/14/defensive-bash-programming/)
