---
name: bash-scripting
description: >
  Write reliable, defensive, and portable Bash scripts following industry
  best practices. Use when authoring shell scripts, automating build/deploy
  steps, implementing error traps and signal handling, working with bash arrays
  and functions, or linting with ShellCheck.
compatibility: >
  Agent Skills-compatible coding agents creating or reviewing Bash 4+
  shell scripts.
metadata:
  author: michaelweissdev
  version: "1.0.0"
  tags: "bash, shell, scripting, automation, shellcheck, posix"
  topics: "operating-systems, devtools, software-development"
---

# Defensive Bash Scripting

Bash scripting automates infrastructure, deployment, and task pipelines. Because shell interpreters are permissive by default, scripts must be written defensively with strict error modes, rigorous quoting, signal traps, and structured functions to prevent silent data corruption and unexpected aborts.

## Non-Negotiable Boilerplate

Every production Bash script should start with this canonical header:

```bash
#!/usr/bin/env bash
set -euo pipefail
IFS=$'\n\t'
```

- `set -e`: Exit immediately if any command exits with a non-zero status (unless handled in an `if`/`while` test).
- `set -u`: Treat unset variables and parameters as an error when performing parameter expansion.
- `set -o pipefail`: Return the exit status of the last command in the pipe that failed, not the status of the rightmost command.
- `IFS=$'\n\t'`: Prevent word-splitting on spaces in unquoted expansions (splits only on newlines and tabs).

---

## 1. Robust Variable Handling and Quoting

Always quote variable references in double quotes to prevent word splitting and globbing:

```bash
# Correct:
target_file="$1"
cp "$target_file" "$destination_dir/"

# WRONG: if $target_file is "my document.txt", this splits into two arguments
cp $target_file $destination_dir/
```

### Parameter Expansion and Defaults
```bash
# Set a default value if unset or null
output_dir="${OUTPUT_DIR:-/tmp/build}"

# Throw an error with a custom message if variable is unset or empty
api_key="${API_KEY:?Error: API_KEY environment variable must be set}"

# Extract filename without extension
base_name="${filename%.*}"

# Replace substring
clean_path="${path//\/\///}"
```

---

## 2. Functions, Local Scope, and Return Values

- Always declare internal variables with `local`.
- Never rely on global variable leakage between functions.
- Functions return status codes `0-255` via `return`. Data is passed back via `stdout`.

```bash
calculate_checksum() {
  local file_path="$1"
  local algorithm="${2:-sha256}"

  if [[ ! -f "$file_path" ]]; then
    echo "Error: file not found: $file_path" >&2
    return 1
  fi

  if [[ "$algorithm" == "sha256" ]]; then
    sha256sum "$file_path" | awk '{print $1}'
  else
    echo "Unsupported algorithm: $algorithm" >&2
    return 2
  fi
}

# Usage: capture stdout, exit code is checked by `set -e`
hash=$(calculate_checksum "package.tar.gz")
```

---

## 3. Signal Traps and Cleanup

Never leave temporary files or orphaned background processes on exit or failure. Use `trap` to ensure deterministic cleanup:

```bash
#!/usr/bin/env bash
set -euo pipefail

# Create a secure temporary directory
TMP_DIR=$(mktemp -d "/tmp/task_runner.XXXXXX")

# Register cleanup function on EXIT, SIGINT (Ctrl+C), and SIGTERM
cleanup() {
  local exit_code=$?
  rm -rf "$TMP_DIR"
  if [[ $exit_code -ne 0 ]]; then
    echo "[ERROR] Script failed with exit code $exit_code" >&2
  fi
  exit "$exit_code"
}
trap cleanup EXIT INT TERM

# All temporary work happens safely inside $TMP_DIR
echo "Working in $TMP_DIR"
```

---

## 4. Arrays and Safe Iteration

Use indexed and associative arrays instead of space-delimited strings:

```bash
# Define an indexed array
declare -a servers=("web-01" "web-02" "worker-01")

# Append to array
servers+=("worker-02")

# Iterate over elements safely (preserves spaces within items)
for server in "${servers[@]}"; do
  echo "Checking health for: $server"
done

# Array length
echo "Total servers: ${#servers[@]}"
```

---

## 5. Handling `set -e` Pitfalls

### Testing Commands Without Aborting
When a command is expected to potentially fail without aborting the script:

```bash
# WRONG: Under set -e, this aborts the script immediately if grep finds no match:
grep "CRITICAL" server.log

# CORRECT: Explicitly handle the exit status
if grep "CRITICAL" server.log >/dev/null 2>&1; then
  echo "Critical errors found"
else
  echo "Clean log"
fi

# OR use a fallback `|| true`:
grep "WARNING" server.log || true
```

---

## 6. Common Mistakes and Anti-Patterns

| Anti-Pattern | Risk | Correct Practice |
| :--- | :--- | :--- |
| `[ $val == "foo" ]` | Fails if `$val` is empty (`[: ==: unary operator expected`) | Use bash double brackets: `[[ "$val" == "foo" ]]` |
| `for file in $(find . -type f)` | Breaks on spaces or newlines in filenames | Use `while IFS= read -r -d '' file; do ... done < <(find . -type f -print0)` |
| `rm -rf $DIR/*` | If `$DIR` is empty or unset, executes `rm -rf /*` | Guard: `rm -rf "${DIR:?}"/*` |
| Ignoring ShellCheck warnings | Latent bugs, injection vulnerabilities | Run `shellcheck script.sh` before deployment |
| Parsing output of `ls` | Fragile, non-portable, breaks on whitespace | Use path globs: `for f in *.txt; do [[ -e "$f" ]] \|\| continue; ...; done` |

---

## 7. Complete Production Script Template

```bash
#!/usr/bin/env bash
# ==============================================================================
# Script: backup_db.sh
# Purpose: Create a compressed PostgreSQL backup and verify integrity.
# ==============================================================================
set -euo pipefail
IFS=$'\n\t'

readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly BACKUP_DIR="${BACKUP_DIR:-/var/backups/db}"
readonly RETENTION_DAYS=7

log() {
  local level="$1"
  shift
  echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] [$level] $*" >&2
}

cleanup() {
  local code=$?
  if [[ -n "${TMP_ARCHIVE:-}" && -f "${TMP_ARCHIVE:-}" ]]; then
    rm -f "$TMP_ARCHIVE"
  fi
  if [[ $code -ne 0 ]]; then
    log "ERROR" "Backup procedure failed with code $code"
  fi
  exit "$code"
}
trap cleanup EXIT INT TERM

main() {
  log "INFO" "Starting backup process..."
  mkdir -p "$BACKUP_DIR"

  TMP_ARCHIVE=$(mktemp "$BACKUP_DIR/backup_XXXXXX.sql.gz")
  
  log "INFO" "Dumping database to temporary archive..."
  # Example: pg_dump -U postgres app_db | gzip > "$TMP_ARCHIVE"
  echo "SIMULATED DB DUMP" | gzip > "$TMP_ARCHIVE"

  local final_name="$BACKUP_DIR/app_db_$(date +%Y%m%d_%H%M%S).sql.gz"
  mv "$TMP_ARCHIVE" "$final_name"
  TMP_ARCHIVE=""  # Clear so cleanup doesn't delete the final file

  log "INFO" "Backup successfully written to $final_name"

  # Prune old backups older than retention policy
  find "$BACKUP_DIR" -name "app_db_*.sql.gz" -mtime +"$RETENTION_DAYS" -delete
  log "INFO" "Pruning completed."
}

main "$@"
```

---

## 8. Verification Checklist

- [ ] Script starts with `#!/usr/bin/env bash` and `set -euo pipefail`.
- [ ] Passed `shellcheck <script.sh>` without errors or warnings.
- [ ] All variable interpolations in command executions are double-quoted.
- [ ] Temporary files are registered with an EXIT trap for safe cleanup.
- [ ] Script handles missing arguments with informative usage messages.
