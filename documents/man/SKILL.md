---
name: man
description: Use when unsure about command syntax, options, or behavior, or when the user asks to "check the man page", "look up the manual", or "what does [command] do". Consult system man pages for accurate, version-specific documentation.
allowed-tools: Bash(man:*), Read
---

# Unix Man Pages (Non-Interactive)

Consult system manual pages for accurate command documentation. Prefer man pages over training data when precision matters.

**CRITICAL: Never run bare `man <command>` - it opens an interactive pager that hangs.**

## How to Use Efficiently

Follow these rules to avoid flooding your context window:

1. **Search first** - If unsure of the command name, use `mancat -k <keyword>`
2. **Target sections** - Don't fetch the full man page immediately:
   - Read **SYNOPSIS** first to understand the structure
   - Read **DESCRIPTION** for a high-level overview
   - Fetch **OPTIONS** only when you need specific flags
3. **Sanitization is automatic** - The `mancat` tool strips formatting codes; raw control characters are handled

## Usage Workflows

### A. Discovery (Instead of Web Search)

When you don't know which command to use:

```bash
# CLAUDE_PLUGIN_ROOT is set automatically by Claude Code plugins
MANCAT="${CLAUDE_PLUGIN_ROOT}/skills/man/mancat.sh"
"$MANCAT" -k compress    # Returns: gzip, bzip2, tar, zip with descriptions
"$MANCAT" -k "file system"
```

### B. Syntax Verification

When you know the command but need exact argument order:

```bash
"$MANCAT" -s SYNOPSIS tar
# Output: tar [-] A --catenate --concatenate | c --create | d --diff ...
```

### C. Flag Investigation

When you need to understand a specific option:

```bash
"$MANCAT" -s OPTIONS tar
# Or for a specific flag:
"$MANCAT" tar | grep -A5 -- '-z'
```

## Quick Start

```bash
# Use the mancat helper (recommended)
"${CLAUDE_PLUGIN_ROOT}/skills/man/mancat.sh" ls

# Or pipe through col -b
man ls | col -b
```

## The mancat Helper

Use the included `mancat.sh` for convenient non-interactive access:

```bash
MANCAT="${CLAUDE_PLUGIN_ROOT}/skills/man/mancat.sh"

"$MANCAT" ls                 # Full man page, clean output
"$MANCAT" passwd 5           # Section 5 (file formats)
"$MANCAT" -s OPTIONS tar     # Extract just OPTIONS section
"$MANCAT" -k compress        # Search descriptions (apropos)
```

## Manual Non-Interactive Patterns

Use these raw patterns when `mancat.sh` is unavailable or when piping to tools like `grep`/`sed`:

```bash
man <command> | col -b
```

The `col -b` filter strips backspace formatting codes, producing clean plain text.

**Alternatives:**

```bash
PAGER=cat man <command>    # Force no pager (may include escape codes)
man <command> | cat        # Simple but less clean on some systems
```

## Efficient Lookups (Raw Patterns)

Full man pages waste context. Use targeted extraction with `grep`/`sed`:

### Get Specific Option

```bash
man tar | col -b | grep -A5 -- '-z'
man curl | col -b | grep -A8 -- '--data'
```

### Extract Section

```bash
# SYNOPSIS section
man ls | col -b | sed -n '/^SYNOPSIS/,/^[A-Z]/p' | head -20

# OPTIONS section (first 50 lines)
man curl | col -b | sed -n '/^OPTIONS/,/^[A-Z]/p' | head -50

# EXAMPLES section
man rsync | col -b | sed -n '/^EXAMPLES/,/^[A-Z]/p'
```

### Limit Output Length

Always limit long pages:

```bash
man bash | col -b | head -100
man git-rebase | col -b | head -150
```

## Quick Reference Commands

### Search for Commands

```bash
man -k <keyword>              # Search names and descriptions
man -k compress | head -10    # Find compression tools
man -k "file system"          # Search phrase
```

### One-Line Description

```bash
man -f tar
# tar (1) - manipulate tape archives
```

### Check Man Page Exists

```bash
man -w grep >/dev/null 2>&1 && echo "has man page"
```

### Get Man Page Path

```bash
man -w ls
# /usr/share/man/man1/ls.1
```

## Man Page Sections

| Section | Content |
|---------|---------|
| 1 | User commands |
| 2 | System calls |
| 3 | Library functions |
| 4 | Special files (/dev) |
| 5 | File formats (/etc/passwd) |
| 6 | Games |
| 7 | Miscellaneous (protocols, conventions) |
| 8 | System administration commands |

Specify section when a name exists in multiple:

```bash
man 1 printf | col -b   # Shell command
man 3 printf | col -b   # C library function
man 5 crontab | col -b  # File format
man 8 cron | col -b     # Daemon
```

## Reading Man Output

**SYNOPSIS** - Command syntax. `[]` = optional, `...` = repeatable.

**OPTIONS** - Flag descriptions with exact syntax.

**EXAMPLES** - Working command examples (not all pages have these).

**SEE ALSO** - Related commands worth checking.

## When to Use Man Pages

- **System commands** (`ls`, `find`, `tar`) - Options vary by OS
- **Config files** (`man 5 sudoers`) - Syntax documentation
- **Git subcommands** (`man git-rebase`) - Full option reference
- **Network tools** (`man curl`, `man ssh`) - Protocol-specific flags
