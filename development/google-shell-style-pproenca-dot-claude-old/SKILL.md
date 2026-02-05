---
name: google-shell-style
description: Use when the user asks to "refactor shell script", "fix bash style", "apply Google style guide to shell", "review shell script style", "format bash script", or when writing, reviewing, or refactoring shell/bash scripts. Provides Google Shell Style Guide rules for formatting, quoting, naming, control flow, and common anti-patterns.
allowed-tools: Bash(shellcheck:*), Bash(bash -n:*), Read, Write, Edit
---

# Google Shell Style Guide

Apply consistent, safe, and readable shell scripting practices based on Google's Shell Style Guide.

## Core Principles

1. **Consistency** - Follow existing style in files being modified
2. **Safety** - Quote variables, use `[[ ]]`, avoid `eval`
3. **Readability** - 2-space indent, 80-char lines, clear naming

## Quick Reference

| Rule | Do | Avoid |
|------|-----|-------|
| Command substitution | `$(command)` | `` `command` `` |
| Tests | `[[ condition ]]` | `[ condition ]` or `test` |
| Arithmetic | `(( x + y ))` | `let`, `expr`, `$[ ]` |
| Variables | `"${var}"` | `$var` or `${var}` unquoted |
| Functions | `func_name() {` | `function func_name {` |
| Indentation | 2 spaces | Tabs |

## Formatting Rules

### Indentation

Use 2 spaces. Never tabs (exception: heredoc with `<<-`).

```bash
if [[ -n "${var}" ]]; then
  echo "indented with 2 spaces"
fi
```

### Line Length

Maximum 80 characters. For long strings, use heredocs or embedded newlines:

```bash
cat <<EOF
Long string content
spanning multiple lines
EOF

long_string="First line
second line"
```

### Pipelines

One line if fits, otherwise split with pipe on new line:

```bash
command1 | command2

command1 \
  | command2 \
  | command3
```

### Control Flow

Put `; then` and `; do` on same line as `if`/`for`/`while`:

```bash
if [[ -d "${dir}" ]]; then
  process_dir
fi

for file in "${files[@]}"; do
  process_file "${file}"
done

while read -r line; do
  echo "${line}"
done < input.txt
```

### Case Statements

Indent alternatives by 2 spaces. Simple cases on one line:

```bash
case "${option}" in
  a) action_a ;;
  b) action_b ;;
  complex)
    do_something
    do_more
    ;;
  *)
    error "Unknown option"
    ;;
esac
```

## Variable Handling

### Quoting

Always quote strings containing variables, command substitutions, or special characters:

```bash
flag="$(some_command)"
echo "${flag}"
grep -li Hugo /dev/null "$1"
```

### Variable Expansion

Prefer `"${var}"` with braces. Exception: single-character positional params (`$1`, `$@`):

```bash
echo "PATH=${PATH}, file=${filename}"
echo "Positional: $1 $2 $3"
echo "All args: $@"
```

### Arrays

Use arrays for lists, especially command arguments:

```bash
declare -a flags
flags=(--foo --bar='baz')
flags+=(--config="${config_file}")
mybinary "${flags[@]}"
```

## Command Substitution and Tests

### Command Substitution

Always use `$(command)`, never backticks:

```bash
var="$(command "$(nested_command)")"
```

### Tests

Use `[[ ]]` for all tests. Use `-z`/`-n` for string checks, `(( ))` for numeric:

```bash
if [[ -z "${my_var}" ]]; then
  echo "empty"
fi

if [[ "${my_var}" == "value" ]]; then
  echo "match"
fi

if (( count > 10 )); then
  echo "large"
fi
```

### Arithmetic

Use `(( ))` or `$(( ))`. Never `let`, `expr`, or `$[ ]`:

```bash
(( i += 3 ))
result=$(( x * y + z ))

if (( a < b )); then
  echo "a is smaller"
fi
```

## Naming Conventions

### Functions

Lowercase with underscores. Braces on same line:

```bash
my_function() {
  local result
  result="$(do_work)"
  echo "${result}"
}

mypackage::helper() {
  # namespaced function
}
```

### Variables

Lowercase with underscores for local variables:

```bash
local file_name
local -i count=0
```

### Constants

Uppercase with underscores. Use `readonly`:

```bash
readonly CONFIG_PATH='/etc/app/config'
declare -xr EXPORTED_VAR='value'
```

## Script Structure

### Function Location

Put all functions near top, after constants. No executable code between functions.

### Main Function

Scripts with multiple functions must have a `main` function:

```bash
#!/bin/bash

readonly SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

helper_func() {
  # helper implementation
}

main() {
  local arg="$1"
  helper_func "${arg}"
}

main "$@"
```

### Local Variables

Always declare function variables as `local`. Separate declaration from command substitution:

```bash
my_func() {
  local name="$1"
  local result
  result="$(some_command)"
  (( $? == 0 )) || return 1
  echo "${result}"
}
```

## Common Anti-Patterns

### Avoid eval

```bash
eval $(set_my_variables)
```

### Avoid Aliases in Scripts

Use functions instead:

```bash
fancy_ls() {
  ls -lh "$@"
}
```

### Avoid Pipes to While

Use process substitution to preserve variables:

```bash
while read -r line; do
  last_line="${line}"
done < <(your_command)
```

### Avoid mapfile/readarray (macOS Incompatible)

`mapfile` and `readarray` are Bash 4+ builtins not available on macOS (Bash 3.2). Use `while read` loop instead:

```bash
# AVOID - fails on macOS
mapfile -t files < <(find . -name "*.txt")

# USE - portable
files=()
while IFS= read -r file; do
  files+=("$file")
done < <(find . -name "*.txt")
```

### Wildcard Safety

Use explicit path prefix:

```bash
rm -v ./*
```

## Error Handling

### Check Return Values

```bash
if ! mv "${files[@]}" "${dest}/"; then
  echo "Move failed" >&2
  exit 1
fi
```

### PIPESTATUS

Check pipeline component failures:

```bash
tar -cf - ./* | ( cd "${dir}" && tar -xf - )
if (( PIPESTATUS[0] != 0 || PIPESTATUS[1] != 0 )); then
  echo "Pipeline failed" >&2
fi
```

## Security Patterns

### Safe Temporary Files

Always use `mktemp` with trap cleanup:

```bash
cleanup() {
  local exit_code=$?
  [[ -n "${TEMP_FILE:-}" ]] && rm -f "${TEMP_FILE}"
  exit "${exit_code}"
}
trap cleanup EXIT

TEMP_FILE="$(mktemp)"
# use TEMP_FILE...
```

### Input Validation

Validate user input before use:

```bash
validate_path() {
  local path="$1"
  # Reject empty
  [[ -z "${path}" ]] && return 1
  # Reject path traversal
  [[ "${path}" == *..* ]] && return 1
  # Require within allowed directory
  [[ "${path}" != "${ALLOWED_DIR}"/* ]] && return 1
  return 0
}
```

### Command Injection Prevention

Never use `eval` with external input. Use arrays for dynamic commands:

```bash
# DANGEROUS - injection risk
eval "${user_command}"

# SAFE - use arrays
declare -a cmd_args
cmd_args=("--flag" "${user_input}")
mycommand "${cmd_args[@]}"
```

Always quote variable expansions in commands:

```bash
# DANGEROUS
rm $file_path
grep $pattern $file

# SAFE
rm -- "${file_path}"
grep -- "${pattern}" "${file}"
```

Use `--` to prevent option injection with user-provided filenames.

## Issue Severity Classification

For shell-expert agent reviews, issues are classified as:

### Critical (Must Fix)

- Unquoted variables in `rm`, `mv`, or path operations
- Use of `eval` with external input
- Missing error handling on destructive operations
- Command injection vulnerabilities

### Important (Should Fix)

- Using `[ ]` instead of `[[ ]]`
- Missing `local` in functions
- Backticks instead of `$()`
- Missing `main` function in multi-function scripts

### Minor (Suggestions)

- Inconsistent indentation
- Long lines (> 80 chars)
- Missing braces on simple variables
- Comment formatting

## Additional Resources

For the complete Google Shell Style Guide, see: https://google.github.io/styleguide/shellguide.html
