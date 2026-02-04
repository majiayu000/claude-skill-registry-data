---
name: bash-audit
description: Comprehensive security and quality audit for shell scripts (bash, sh, zsh) using defensive programming principles and ShellCheck static analysis. Use when user asks to audit, review, check, lint, validate, or analyze shell scripts for security vulnerabilities, bugs, errors, defensive programming compliance, or best practices. Also triggers for improving script quality, finding script errors or issues, checking portability problems (macOS vs Linux), validating error handling, fixing shellcheck warnings, reviewing legacy automation scripts before release, setting up CI/CD linting infrastructure, configuring pre-commit hooks, understanding ShellCheck error codes, suppressing false positives, or ensuring script portability and quality.
allowed-tools: [Read, Bash, Grep, Edit, Write, Glob]
---

## Reference Files

Advanced ShellCheck guidance and workflows:

- [configurations.md](configurations.md) - ShellCheck configuration examples and .shellcheckrc templates
- [error-codes.md](error-codes.md) - Detailed ShellCheck error code reference with fixes
- [fixes.md](fixes.md) - Solutions to common ShellCheck violations
- [integrations.md](integrations.md) - Pre-commit hooks, GitHub Actions, GitLab CI
- [performance.md](performance.md) - Optimization techniques for batch processing
- [workflows.md](workflows.md) - End-to-end workflows for development and CI/CD

---

# Bash Script Audit

Performs comprehensive security and quality audits of shell scripts, combining ShellCheck static analysis with defensive programming standards from the bash-scripting skill.

## Audit Workflow

### 1. Discovery - Find Shell Scripts

**Find .sh files**:

```bash
find . -type f -name "*.sh"
```

**Find executable scripts with shebang**:

```bash
find . -type f -executable -exec grep -l '^#!.*sh' {} \;
```

**Or use Glob for specific paths**:

- `**/*.sh` - All .sh files recursively
- `scripts/**/*.sh` - Scripts in scripts/ directory
- `bin/*` - Executables in bin/

### 2. Static Analysis - Run ShellCheck

**Basic ShellCheck scan**:

```bash
shellcheck --format=gcc --severity=warning <script.sh>
```

**For all scripts**:

```bash
find . -name "*.sh" -exec shellcheck --format=gcc --severity=warning {} \;
```

**ShellCheck severity levels**:

- `error` - Syntax errors, serious issues
- `warning` - Potential bugs, common mistakes (default)
- `info` - Minor suggestions
- `style` - Stylistic issues

**Common ShellCheck codes**:

- `SC2086` - Unquoted variables
- `SC2046` - Unquoted command substitution
- `SC2181` - Check exit code directly
- `SC2155` - Declare and assign separately
- `SC2164` - Use `cd ... || exit` pattern

For detailed error code reference and fixes, see [error-codes.md](error-codes.md) and [fixes.md](fixes.md).

**ShellCheck Configuration**:

Create `.shellcheckrc` in project root:

```conf
# Target shell
shell=bash

# Enable optional checks
enable=avoid-nullary-conditions
enable=require-variable-braces

# Disable specific warnings (with justification)
disable=SC1091  # Can't follow external sources
```

For complete configuration examples (minimal, development, CI/CD), see [configurations.md](configurations.md).

**CI/CD Integration**:

For pre-commit hooks, GitHub Actions, and GitLab CI pipelines, see [integrations.md](integrations.md).

**Advanced Workflows**:

For complete audit workflows including batch processing, legacy migration, and baseline approaches, see [workflows.md](workflows.md).

### 3. Defensive Programming Review

Use Grep to check for defensive programming patterns:

**Critical Safety Checks**:

```bash
# Check for set -Eeuo pipefail (should exist)
grep -n "set -[Eeu]*o pipefail" <script.sh>

# Check for unquoted variables (should NOT exist)
grep -n '\$[A-Za-z_][A-Za-z0-9_]*[^"]' <script.sh>

# Check for proper trap cleanup (should exist in non-trivial scripts)
grep -n "trap.*EXIT" <script.sh>

# Check for local variable usage (should exist in functions)
grep -n "local " <script.sh>

# Check for secure mktemp usage (should use mktemp, not /tmp/hardcoded)
grep -n "mktemp" <script.sh>
grep -n "/tmp/" <script.sh>

# Check for command substitution (should use $() not backticks)
grep -n '`.*`' <script.sh>
```

**Defensive Programming Checklist** (from bash-scripting skill):

Read the script and verify:

- [ ] Script starts with `set -Eeuo pipefail`
- [ ] All variables are quoted: `"$var"` not `$var`
- [ ] Functions use `local` for variables
- [ ] Cleanup trap is defined: `trap cleanup EXIT`
- [ ] Error messages go to stderr: `>&2`
- [ ] External commands are checked: `command -v foo || { echo "error" >&2; exit 1; }`
- [ ] Temporary files use `mktemp`: `tmp=$(mktemp)` not `/tmp/myfile`
- [ ] Permissions are verified before operations
- [ ] No hardcoded paths (use `command -v` or relative paths)
- [ ] Exit codes are explicit: `exit 0` or `exit 1`

### 4. Report Generation

Generate a structured audit report using this template:

```markdown
# Bash Script Audit Report

**Date**: [YYYY-MM-DD]
**Script(s)**: [list of audited files]
**Auditor**: Claude Code bash-audit skill

---

## Summary

- **Scripts Audited**: [count]
- **Critical Issues**: [count]
- **High Priority**: [count]
- **Medium Priority**: [count]
- **Low Priority**: [count]

---

## Critical Security Issues

[List issues that could cause security vulnerabilities or data loss]

### [Filename]:[Line]

- **Severity**: CRITICAL
- **Issue**: [description]
- **ShellCheck Code**: [SCxxxx] (if applicable)
- **Fix**: [specific remediation]

---

## High Priority Issues

[List issues that could cause script failures or unexpected behavior]

### [Filename]:[Line]

- **Severity**: HIGH
- **Issue**: [description]
- **Fix**: [specific remediation]

---

## Medium Priority Issues

[List best practice violations or portability concerns]

### [Filename]:[Line]

- **Severity**: MEDIUM
- **Issue**: [description]
- **Fix**: [specific remediation]

---

## Low Priority (Style/Polish)

[List stylistic improvements or minor optimizations]

---

## Defensive Programming Compliance

| Requirement                  | Status | Notes     |
| ---------------------------- | ------ | --------- |
| `set -Eeuo pipefail`         | ✓/✗    | [details] |
| Variable quoting             | ✓/✗    | [details] |
| Local variables in functions | ✓/✗    | [details] |
| Cleanup trap defined         | ✓/✗    | [details] |
| Secure mktemp usage          | ✓/✗    | [details] |
| Error handling               | ✓/✗    | [details] |

---

## Recommendations

1. [Prioritized action items]
2. [...]

---

## Reference

See the bash-scripting skill for comprehensive defensive programming standards.
```

## Quick Usage Examples

**Audit a single script**:

```text
User: "Audit my deploy.sh script for security issues"
Assistant: [Runs shellcheck, checks defensive patterns, generates report]
```

**Audit all scripts in a directory**:

```text
User: "Check all my shell scripts in ./scripts/ for best practices"
Assistant: [Finds all .sh files, analyzes each, generates consolidated report]
```

**Find specific issues**:

```text
User: "Find portability issues in my bash scripts"
Assistant: [Runs shellcheck with focus on portability, checks for bashisms]
```

**Pre-release review**:

```text
User: "Review my automation scripts before production release"
Assistant: [Comprehensive audit with critical/high priority focus]
```

**Configure ShellCheck for project**:

```text
User: "Set up ShellCheck configuration for my bash project"
Assistant: [Creates .shellcheckrc, explains options, references configurations.md]
```

**Fix ShellCheck violations**:

```text
User: "How do I fix SC2086 warnings in my script?"
Assistant: [Explains double quoting, shows examples, references fixes.md]
```

**Set up CI/CD linting**:

```text
User: "Add ShellCheck to my GitHub Actions workflow"
Assistant: [Provides workflow configuration, references integrations.md]
```
