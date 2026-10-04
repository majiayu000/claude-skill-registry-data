---
name: sed
description: >
  Expert GNU sed one-liner generation and transformation. Use this skill whenever
  the user asks to transform text, edit files in-place, refactor code via CLI,
  process logs, do bulk find/replace, extract lines, delete patterns, or perform
  any stream editing task. Trigger on keywords like "sed", "replace in files",
  "find and replace", "edit in place", "strip lines", "extract pattern", "log
  filtering", "batch rename content", "remove lines matching", "transform output",
  or any request that maps to a sed one-liner or pipeline. When in doubt, use this
  skill — sed is often the right tool.
---

# GNU sed Skill

All output assumes **GNU sed** (`sed --version` shows GNU). POSIX compatibility is
not a goal; use `-E` (extended regex) by default unless basic regex is clearly
sufficient.

---

## Core Principles

1. **Prefer one-liners.** Multi-line sed scripts are a last resort.
2. **Use `-E`** for extended regex (avoids backslash noise).
3. **Use `-i` for in-place edits**; always show the command with a backup suffix
   suggestion (`-i.bak`) if the operation is destructive.
4. **Dry-run first.** When editing files, show the `sed` without `-i` before the
   in-place version so the user can verify.
5. **Chain with pipes** when sed alone isn't the cleanest tool.
6. **Never use sed to parse structured formats** (JSON, YAML, XML). Redirect to
   `jq`, `yq`, or `xmllint` and say why.

---

## Flags to Always Know

| Flag         | Meaning                                          |
|--------------|--------------------------------------------------|
| `-E`         | Extended regex (ERE): `+`, `?`, `|`, `()` work without backslash |
| `-i[SUFFIX]` | Edit in place (GNU: `-i` or `-i''` for no backup, `-i.bak` for backup) |
| `-n`         | Suppress automatic print; use with `p` to print selectively |
| `-e`         | Multiple expressions in one invocation           |
| `-f FILE`    | Read commands from a script file                 |
| `--sandbox`  | Disallow `e`, `r`, `w` commands (safe mode)      |

---

## Command Quick Reference

### Substitution (`s`)

```bash
# Basic replace (first occurrence per line)
sed 's/foo/bar/'

# Replace all occurrences on each line
sed 's/foo/bar/g'

# Case-insensitive replace (GNU extension)
sed 's/foo/bar/gI'

# Replace only on lines matching a pattern
sed '/error/s/foo/bar/g'

# Replace on line ranges
sed '10,20s/foo/bar/g'

# Use & to reference the matched text
sed 's/[0-9]\+/(&)/g'   # wraps every number in parens

# Capture groups with \1, \2
sed -E 's/(foo)(bar)/\2\1/'

# Delimiter swap (useful when pattern contains /)
sed 's|/usr/local|/opt|g'
```

### Delete lines (`d`)

```bash
# Delete lines matching a pattern
sed '/^#/d'

# Delete blank lines
sed '/^[[:space:]]*$/d'

# Delete line range
sed '5,10d'

# Delete from pattern to end of file
sed '/START/,$d'

# Delete lines NOT matching (invert with !)
sed '/keep/!d'
```

### Print / Extract (`p`, `-n`)

```bash
# Print only matching lines (like grep)
sed -n '/error/p'

# Print line numbers with matches
sed -n '/error/='

# Print a line range
sed -n '10,20p'

# Print from pattern to pattern (inclusive)
sed -n '/START/,/END/p'

# Print only the captured group (GNU extension)
sed -En 's/.*key=([^ ]+).*/\1/p'
```

### Insert / Append / Change (`i`, `a`, `c`)

```bash
# Insert a line before match
sed '/pattern/i\NEW LINE'

# Append a line after match
sed '/pattern/a\NEW LINE'

# Replace the entire matching line
sed '/pattern/c\REPLACEMENT LINE'
```

### Transform characters (`y`)

```bash
# Like tr: map chars one-to-one
sed 'y/abc/ABC/'
```

### Multi-expression

```bash
sed -E -e 's/foo/bar/g' -e 's/baz/qux/g'
```

---

## Patterns & Addresses

```
/regex/         — lines matching regex
/re1/,/re2/     — line range from re1 to re2 (inclusive)
N               — line number N
N,M             — line numbers N through M
N~STEP          — every STEP lines starting at N  (e.g. 1~2 = odd lines)
$               — last line
/re/!           — lines NOT matching
```

---

## Common Use Cases

### Shell scripting: rewrite config values

```bash
# Dry-run
sed -E 's/^(TIMEOUT=).*/\1120/' config.env

# In-place with backup
sed -E -i.bak 's/^(TIMEOUT=).*/\1120/' config.env
```

### Code refactoring: rename symbol across files

```bash
# Preview
grep -rl 'OldClass' src/ | xargs sed -E 's/\bOldClass\b/NewClass/g'

# In-place
grep -rl 'OldClass' src/ | xargs sed -E -i.bak 's/\bOldClass\b/NewClass/g'
```

Use `\b` for word boundaries (GNU sed supports `\b` in ERE).

### Log processing: extract fields

```bash
# Extract timestamps from nginx logs
sed -En 's/.*\[([^\]]+)\].*/\1/p' access.log

# Show only lines between two timestamps (approximate)
sed -n '/2024-01-01 10:00/,/2024-01-01 11:00/p' app.log

# Strip ANSI color codes
sed -E 's/\x1B\[[0-9;]*[mK]//g'
```

### File batch editing: add/remove lines

```bash
# Add a shebang to all .sh files missing one
find . -name '*.sh' | xargs sed -i '1{/^#!/!i\#!/usr/bin/env bash
}'

# Remove trailing whitespace
sed -E -i 's/[[:space:]]+$//' file.rb

# Comment out lines matching a pattern
sed -i 's/^FEATURE_X=/#FEATURE_X=/' .env
```

### Delete lines between markers (exclusive)

```bash
sed '/START/,/END/{/START/!{/END/!d}}' file.txt
```

### Number lines (print with line numbers)

```bash
sed = file.txt | sed 'N;s/\n/\t/'
```

---

## Combining with Other Tools

```bash
# sed + xargs: batch replace in files found by grep
grep -rl 'pattern' . | xargs sed -i 's/pattern/replacement/g'

# sed + awk: sed for line filtering, awk for field extraction
sed -n '/error/p' app.log | awk '{print $1, $NF}'

# sed in a pipeline
cat access.log | sed -n '/POST/p' | cut -d' ' -f7 | sort | uniq -c
```

---

## Output Format

When responding to a sed request:

1. **Show the one-liner** in a code block, ready to copy-paste.
2. If editing files in-place, show **dry-run first**, then the `-i` version.
3. Add a **one-line comment** explaining what each part does if non-obvious.
4. If the task is better served by `awk`, `perl`, `jq`, or `ripgrep`, say so briefly
   and optionally provide that alternative instead.

---

## Gotchas

- **macOS ships BSD sed**, not GNU sed. `-i` requires a mandatory suffix (`-i ''`
  is valid on BSD, `-i.bak` on both). If the user is on macOS, note this.
- Regex in sed is greedy by default; there is no non-greedy quantifier in GNU sed
  ERE. Workaround: use negated character classes (`[^x]*` instead of `.*?`).
- `\w` is a GNU sed extension, not portable sed. Use `[[:alnum:]_]` for portable
  word characters, and `[0-9]` or `[[:digit:]]` for digits. Use Perl (`perl -pe`)
  when you need PCRE shorthands such as `\d`.
- Multiline matching across line breaks requires the `N` command or a hold-space
  trick. If the user needs real multiline regex, recommend `perl -0777 -pe`.
