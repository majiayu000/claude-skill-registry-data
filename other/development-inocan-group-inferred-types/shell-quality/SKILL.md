---
name: shell-quality
description: Interpretive guidance for shell script quality using shfmt and shellcheck. Use when linting shell files, configuring shell tools, troubleshooting shellcheck errors, or understanding formatting options.
---

# Shell Quality Skill

This skill teaches how to apply shell script formatting and linting tools effectively using mr-sparkle's tool selection system. It provides guidance on what the tools do, how they work together, and common error patterns you'll encounter.

## Official Documentation

Claude knows how to use shfmt and shellcheck. Fetch these docs only when you need:

- Specific shellcheck error codes you don't recognize (SC1000, SC2034, etc.)
- Advanced shfmt formatting options
- Recent feature changes

**Reference URLs:**

- **<https://www.shellcheck.net/wiki/>** - Shellcheck error codes and explanations
- **<https://github.com/mvdan/sh>** - shfmt formatter documentation
- **<https://editorconfig.org/>** - EditorConfig specification (used by shfmt)

## Core Understanding

### Tool Pairing Philosophy

**Key principle:** Shell uses BOTH tools together - shfmt for formatting, shellcheck for linting. Unlike Python/JS which have alternative tool groups, shell scripts get both tools applied sequentially.

**What this means:**

- **shfmt** - Formatter only (indentation, spacing, alignment)
- **shellcheck** - Linter only (logic errors, portability issues, best practices)
- **Both run together** - shfmt first, then shellcheck
- **Complementary roles** - shfmt makes it pretty, shellcheck makes it correct

**Decision test:** You don't choose between tools - both always run when available.

### How Tool Selection Works

The linting system applies both tools to shell files:

```text
Shell script detected (.sh, .bash, .zsh)
    ↓
Run: shfmt -w (format)
    ↓
Run: shellcheck (lint)
    ↓
Report results
```

**Detection logic:**

1. File extension matches `.sh`, `.bash`, or `.zsh`
2. Find project root (`.editorconfig`, `.shellcheckrc`, `.git`, etc.)
3. Run shfmt with project config or EditorConfig defaults
4. Run shellcheck with project config or built-in defaults
5. Both tools run even if only one has configuration

**Tools run sequentially:** shfmt modifies the file first, then shellcheck analyzes the result.

## shfmt: Shell Formatter (Official Specification)

**From official docs:**

- **Purpose:** Format shell scripts with consistent style
- **Capabilities:** Indentation, spacing, alignment, case/if formatting
- **Languages:** bash, POSIX sh, mksh
- **Command:** `shfmt -w <file>` (write changes)
- **Configuration:** Uses `.editorconfig` file (EditorConfig standard)

**Common options:**

- `-i <num>` - Indent with spaces (0 = tabs)
- `-bn` - Binary ops like `&&` and `|` may start a line
- `-ci` - Switch cases will be indented
- `-sr` - Redirect operators will be followed by a space

**Configuration location:**

- `.editorconfig` in project root or parent directories
- Command-line flags override EditorConfig settings

## shfmt: Shell Formatter (Best Practices)

**When shfmt helps:**

- ✅ Inconsistent indentation across scripts
- ✅ Mixed tabs and spaces
- ✅ Poorly aligned case statements
- ✅ Team standardization on formatting

**EditorConfig pattern for shell:**

```ini
# .editorconfig
[*.sh]
indent_style = space
indent_size = 2
```

**shfmt honors these EditorConfig properties:**

- `indent_style` (space or tab) → `-i` flag
- `indent_size` (number) → `-i` flag
- `binary_next_line` → `-bn` flag
- `switch_case_indent` → `-ci` flag
- `space_redirects` → `-sr` flag

**See `default-editorconfig`** for recommended settings.

**See `shfmt-reference.md`** for detailed formatting examples and options.

## shellcheck: Shell Linter (Official Specification)

**From official docs:**

- **Purpose:** Static analysis tool for shell scripts
- **Capabilities:** Detect syntax errors, semantic issues, portability problems
- **Languages:** sh/bash/dash/ksh
- **Command:** `shellcheck <file>`
- **Configuration:** `.shellcheckrc` file in project root

**Error code format:** `SC####` (e.g., SC2086, SC2034)

**Common categories:**

- **SC1xxx** - Syntax errors (parsing failures)
- **SC2xxx** - Semantic errors (logic issues, common mistakes)
- **SC3xxx** - Portability warnings (bash-isms in POSIX scripts)

**Configuration file format:**

```bash
# .shellcheckrc
disable=SC2086,SC2154  # Comma-separated codes to ignore
shell=bash             # Default shell to assume
```

## shellcheck: Shell Linter (Best Practices)

**When shellcheck catches issues:**

- ✅ Unquoted variables that could word-split
- ✅ Unused variables
- ✅ Syntax errors and typos
- ✅ Portability issues (bash vs POSIX)
- ✅ Common security issues
- ✅ Logic errors (unreachable code, etc.)

**Most valuable checks:**

- **SC2086** - Unquoted variable may word-split (use `"$var"`)
- **SC2034** - Variable assigned but never used
- **SC2154** - Variable referenced but not assigned
- **SC2068** - Use `"$@"` not `$@` to prevent word splitting
- **SC2046** - Quote command substitution to prevent word splitting

**Configuration strategy:**

1. Start with no config (all rules enabled)
2. Fix what you can
3. Only disable rules you truly need to ignore
4. Document WHY rules are disabled

**See `shellcheck-reference.md`** for common error codes and fixes.

**See `default-shellcheckrc`** for recommended baseline configuration.

## Tool Interaction (Best Practices)

### Why Order Matters

**shfmt runs first:**

1. Formats code (indentation, spacing)
2. May break long lines
3. May reorder elements for consistency

**shellcheck runs second:**

1. Analyzes formatted code
2. Reports logic errors
3. Doesn't modify files

**Why this order:** Formatting changes can affect what shellcheck sees (e.g., line continuation), so format first, then analyze.

### Auto-Fix Capabilities

**shfmt auto-fixes:**

- ✅ Indentation
- ✅ Spacing around operators
- ✅ Alignment of case statements
- ✅ Line wrapping consistency

**shellcheck suggests but doesn't auto-fix:**

- ❌ Most errors require manual fixes
- ℹ️ Provides fix suggestions in output
- ℹ️ Use inline directives to disable specific warnings

**Result:** shfmt makes cosmetic changes automatically, shellcheck requires your attention.

## Common shellcheck Error Codes

### SC2086: Unquoted Variable

**What it means:** Variable expansion could word-split or glob.

**Problem:**

```bash
file=$1
cat $file  # SC2086: Double quote to prevent splitting
```

**Fix:**

```bash
file=$1
cat "$file"  # Properly quoted
```

**When to ignore:** Intentional word splitting (rare, document it).

### SC2034: Variable Unused

**What it means:** Variable assigned but never read.

**Problem:**

```bash
name="test"
# name is never used
echo "hello"
```

**Fix:** Remove the variable or actually use it.

**When to ignore:** Variables sourced by other scripts, exported for external use.

### SC2154: Variable Not Assigned

**What it means:** Variable used but never set in this script.

**Problem:**

```bash
echo "$USER_HOME"  # SC2154: USER_HOME not assigned
```

**Fix:** Assign before use, or disable if it's from environment/sourced file.

**Disable for specific variable:**

```bash
# shellcheck disable=SC2154
echo "$USER_HOME"  # Set by parent script
```

### SC2046: Unquoted Command Substitution

**What it means:** Command substitution needs quotes to prevent word splitting.

**Problem:**

```bash
rm $(find . -name "*.tmp")  # SC2046: Quote to prevent splitting
```

**Fix:**

```bash
rm "$(find . -name "*.tmp")"
# Or better: use while read loop for many files
```

### SC1091: File Not Found

**What it means:** shellcheck can't find sourced file.

**Problem:**

```bash
source ./config.sh  # SC1091: Not following
```

**Fix:** Either make file available or disable:

```bash
# shellcheck source=./config.sh
source ./config.sh
```

**See `shellcheck-reference.md`** for more error codes.

## Configuration Examples

### Minimal .editorconfig for shfmt

**2-space indentation (recommended):**

```ini
# .editorconfig
root = true

[*.sh]
indent_style = space
indent_size = 2
```

**Tab indentation:**

```ini
[*.{sh,bash}]
indent_style = tab
```

**See `default-editorconfig`** for complete example.

### Minimal .shellcheckrc

**Start here:**

```bash
# .shellcheckrc
# No configuration - use all defaults
```

**Common relaxations:**

```bash
# .shellcheckrc
# Allow source files that shellcheck can't find
disable=SC1091

# Target specific shell
shell=bash
```

**Project-specific:**

```bash
# .shellcheckrc
# Disable specific issues after review
disable=SC2086,SC2154  # Word splitting, external variables

# Target shell
shell=bash
```

**See `default-shellcheckrc`** for recommended starting point.

## Common Pitfalls

### Pitfall #1: Ignoring Quote Warnings

**Problem:** Dismissing SC2086 because "it works for me."

**Why it fails:**

```bash
file="my document.txt"
cat $file  # Tries to cat "my" and "document.txt" separately
```

**Better:**

```bash
file="my document.txt"
cat "$file"  # Treats as single argument
```

**Rule:** Always quote variable expansions unless you specifically want word splitting.

### Pitfall #2: Using `source` for Config Files shellcheck Can't Find

**Problem:** shellcheck warns about unfound sourced files.

```bash
source /etc/myapp/config  # SC1091: Not following
```

**Why it's noisy:** shellcheck can't verify external files.

**Better:** Use directive to tell shellcheck about it:

```bash
# shellcheck source=/dev/null
source /etc/myapp/config
```

**Or:** If file is in repo:

```bash
# shellcheck source=./config/defaults.sh
source "${CONFIG_DIR}/defaults.sh"
```

### Pitfall #3: Disabling All Checks in Complex Scripts

**Problem:** Adding `# shellcheck disable=SC2086,SC2046,SC2068...` to every function.

**Why it fails:** Defeats purpose of linting - you're hiding real issues.

**Better:** Fix the code to pass checks, or carefully disable specific lines:

```bash
# This one case legitimately needs word splitting
# shellcheck disable=SC2086
eval $command_string
```

**Philosophy:** Disables should be rare and documented.

### Pitfall #4: Fighting shfmt Formatting

**Problem:** Manually reformatting code after shfmt runs.

**Why it fails:** Hook will reformat again, creating formatting loops.

**Better:** Configure shfmt to match your style via `.editorconfig`:

```ini
[*.sh]
indent_style = space
indent_size = 4  # If you prefer 4 spaces
binary_next_line = true  # If you want &&/|| to start lines
```

**Let the tool enforce consistency.**

### Pitfall #5: Not Testing Scripts After Fixes

**Problem:** Blindly applying shellcheck suggestions without testing.

**Why it fails:** Some suggestions change behavior (quotes, command substitution).

**Better:** Test scripts after applying fixes:

```bash
# Before applying fixes
bash -n script.sh  # Syntax check
./script.sh        # Test execution

# After applying suggested fixes
bash -n script.sh  # Verify syntax still valid
./script.sh        # Verify behavior unchanged
```

## Automatic Hook Behavior

The mr-sparkle plugin's linting hook:

1. Triggers after Write and Edit operations
2. Detects shell files (`.sh`, `.bash`, `.zsh`)
3. Runs shfmt -w (auto-formats)
4. Runs shellcheck (analyzes and reports)
5. Reports shellcheck warnings (non-blocking)
6. Silently skips if tools not installed

**What this means:** Formatting happens automatically, but you need to address shellcheck warnings manually.

## Quality Checklist

**Before finalizing shell scripts:**

**Auto-fixed by shfmt:**

- ✓ Indentation consistency
- ✓ Spacing around operators
- ✓ Case statement alignment
- ✓ Line continuation style

**Requires manual attention (shellcheck):**

- ✓ Unquoted variables
- ✓ Unused variables
- ✓ Missing variable assignments
- ✓ Command substitution quoting
- ✓ Portability issues (if targeting POSIX)
- ✓ Logic errors and unreachable code
- ✓ Exit code handling

## CLI Tool Usage

The universal linting script handles shell files automatically:

```bash
# Lint shell script (applies fixes and checks)
./plugins/mr-sparkle/skills/linting/scripts/lint.py script.sh

# JSON output for programmatic use
./plugins/mr-sparkle/skills/linting/scripts/lint.py script.sh --format json
```

**Exit codes:**

- `0` - Clean or successfully formatted
- `1` - shellcheck warnings found (non-blocking)
- `2` - Tool execution error

See `linting` skill for complete CLI documentation.

## Reference Documentation

**Detailed guides** (linked from this skill for progressive disclosure):

- `shfmt-reference.md` - Formatting options and EditorConfig integration
- `shellcheck-reference.md` - Common error codes with examples and fixes
- `default-editorconfig` - Recommended shfmt configuration
- `default-shellcheckrc` - Recommended shellcheck baseline

**Official documentation to fetch:**

- <https://www.shellcheck.net/wiki/> - Comprehensive shellcheck error explanations
- <https://github.com/mvdan/sh/blob/master/cmd/shfmt/shfmt.1.scd> - shfmt manual page
- <https://editorconfig.org/> - EditorConfig specification
- <https://www.gnu.org/software/bash/manual/> - Bash reference manual
- <https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html> - POSIX shell specification

**Remember:** This skill documents mr-sparkle's shell linting approach. Fetch official docs when you need specific error code explanations or advanced configuration options.
