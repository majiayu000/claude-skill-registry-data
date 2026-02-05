---
name: nushell
description: Write and debug Nushell scripts, pipelines, and commands. Also build Nushell plugins in Rust. Use when working with .nu files, writing Nushell code, converting bash to Nushell, creating custom Nushell commands/plugins, or when the user mentions nushell.
---

# Nushell

## The Paradigm Shift: Text Streams → Structured Data

Nushell fundamentally reimagines shell design. Traditional Unix shells pass **unstructured text** between commands, requiring grep/awk/sed to parse strings. Nushell passes **structured, typed data**—tables, records, lists—eliminating brittle text parsing.

**Stop parsing strings, start solving problems.**

```nu
# POSIX: Parse text, hope format doesn't change
ps aux | grep 'nu' | awk '{print $2, $11}'

# Nushell: Query structured data directly
ps | where name =~ 'nu' | select pid name
```

The same verbs (`where`, `select`, `sort-by`, `group-by`) work universally across all data sources—filesystem, processes, JSON APIs, CSV files. Learn once, apply everywhere.

## Core Philosophy

- **Structured data**: Commands output tables/records/lists, not raw text
- **Type safety**: Data has types; errors caught early
- **Immutability**: Variables immutable by default (`mut` for mutable)
- **Cross-platform**: Internal commands work identically on Linux/macOS/Windows
- **Separation of concerns**: Commands produce data; pipeline transforms it; renderer displays it

## Essential Syntax

```nu
# Variables (immutable by default)
let name = "value"
mut counter = 0
$counter += 1

# String interpolation
$"Hello ($name), count: ($counter)"

# Pipeline input variable
"text" | { $in | str upcase }    # $in holds pipeline input

# Conditionals
if $condition { ... } else { ... }

# Loops
for item in $list { ... }
while $condition { ... }

# Pattern matching
match $value {
    "a" => { ... }
    "b" | "c" => { ... }
    _ => { ... }
}

# Closures
{|x| $x * 2 }

# Custom commands with typed parameters
def greet [name: string, --loud (-l)] {
    if $loud { $name | str upcase } else { $name }
}
```

## Pipeline Architecture: Input → Filter → Output

```nu
# Input (source): generates data
ls                              # Produces table of files

# Filter: transforms data
| where size > 1mb              # Keep rows matching condition
| select name size              # Choose columns
| sort-by size --reverse        # Order by column

# Output (sink): consumes data
| first 5                       # Take top 5
| save large-files.json         # Write to file (or display)
```

## Data Types

| Type      | Example                          | Notes                                  |
| --------- | -------------------------------- | -------------------------------------- |
| string    | `"hello"`                        | Interpolation: `$"value: ($var)"`      |
| int       | `42`, `0xff`                     | Hex, octal (`0o755`), binary (`0b101`) |
| float     | `3.14`                           |                                        |
| bool      | `true` / `false`                 |                                        |
| list      | `[1, 2, 3]`                      | Access: `$list.0` or \`$list           |
| record    | `{name: "x", value: 1}`          | Access: `$rec.name`                    |
| table     | `[[col1, col2]; [a, 1], [b, 2]]` | List of records                        |
| duration  | `1hr + 30min`                    | Semantic units                         |
| filesize  | `10mb`                           | Semantic units                         |
| datetime  | `2024-01-15`                     | Native date operations                 |
| range     | `1..10` or `1..<10`              | Inclusive / exclusive                  |
| closure   | \`{                              | x                                      |
| cell-path | `$table.0.name`                  | Path into data structures              |
| nothing   | `null`                           |                                        |

## Common Commands Quick Reference

**Files & Navigation**

```nu
ls **/*.rs                    # Recursive glob (no find needed!)
cd ~/projects
open file.json                # Auto-parses by extension
save output.json              # Saves structured data
```

**Data Manipulation**

```nu
where condition               # Filter rows
select col1 col2              # Choose columns
get column                    # Extract as list (not table)
sort-by column                # Sort
group-by column               # Aggregate
each {|x| transform $x}       # Transform items
update col { new_value }      # Modify column
```

**Text Processing**

```nu
lines                         # Split text into lines
split row ","                 # Split string
parse "{name}: {value}"       # Extract with pattern
from json / to json           # Format conversion
```

## External Commands: Bridging Worlds

```nu
# External commands run automatically, output captured as text
git status

# Use ^ to force external version (bypass internal command)
^ls -la                       # System ls, not Nushell ls

# Capture stdout, stderr, and exit_code with complete
let result = (git push | complete)
if $result.exit_code != 0 {
    print $"Error: ($result.stderr)"
}

# Parse external output into structured data
docker ps --format json | from json
```

## Bash to Nushell Translation

| Bash                      | Nushell                                    |
| ------------------------- | ------------------------------------------ |
| `$VAR`                    | `$env.VAR` (env) or `$var` (local)         |
| `export VAR=x`            | `$env.VAR = "x"`                           |
| `$(cmd)`                  | `(cmd)`                                    |
| `cmd \| grep pattern`     | `cmd \| where col =~ pattern`              |
| `cmd \| awk '{print $1}'` | `cmd \| get column` or `cmd \| select col` |
| `cmd \| wc -l`            | `cmd \| length`                            |
| `[ -f file ]`             | `("file" \| path exists)`                  |
| `for i in ...; do`        | `for i in ... { }`                         |
| `VAR=x cmd`               | `with-env {VAR: x} { cmd }`                |
| `cmd > file`              | `cmd \| save file`                         |
| `cmd 2>&1`                | `cmd \| complete`                          |

## Error Handling

```nu
# Try/catch
try {
    risky-operation
} catch {|e|
    print $"Error: ($e.msg)"
}

# Optional chaining (safe navigation)
$record.field?                # Returns null if missing
$record | get -i field        # Same with command
```

## Critical: Pipeline Input vs Parameters

Pipeline input (`$in`) is NOT interchangeable with function parameters:

```nu
# ✗ WRONG - treats $in as first parameter
def my-func [list: list, value: any] {
    $list | append $value
}

# ✓ CORRECT - declares pipeline signature
def my-func [value: any]: list -> list {
    $in | append $value
}

# Usage
[1 2 3] | my-func 4  # Works correctly
```

**Why this matters**:

- Pipeline input can be **lazily evaluated** (streaming)
- Parameters are **eagerly evaluated** (loaded into memory)
- Different calling conventions entirely

### Type Signatures

```nu
def func [x: int] { ... }                    # params only
def func []: string -> int { ... }           # pipeline only
def func [x: int]: string -> int { ... }     # both
```

## Row Conditions vs Closures

Many commands accept either a **row condition** or a **closure**:

```nu
# Row condition - auto expands $it
$table | where size > 100           # Expands to: $it.size > 100
$table | where name =~ "test"

# Closure - explicit parameter
$table | where {|row| $row.size > 100}
$list | where {$in > 10}

# Closures can be stored and reused
let big_files = {|row| $row.size > 1mb}
ls | where $big_files
```

## Common Gotchas

1. **Parentheses for subexpressions**: `(ls | length)` not `ls | length` in expressions
1. **Closures need parameter**: `each {|it| $it.name }` not `each { $it.name }`
1. **`$in` for pipeline input**: `"text" | { $in | str upcase }`
1. **External output is text**: Pipe through `lines` or `from json` to structure
1. **Semicolons separate statements** on same line, not for line endings
1. **`^` prefix**: Force system command over Nushell builtin
1. **`each` on records**: Only runs once! Use `items` or `transpose` instead
1. **Optional fields**: Use `$record.field?` to avoid errors on missing fields

## References

Read the relevant reference files based on the task at hand:

- [commands.md](references/commands.md) - Command reference and POSIX translations
- [data-types.md](references/data-types.md) - Structured data handling (records, tables, lists, type conversions)
- [pipelines.md](references/pipelines.md) - Advanced pipeline patterns, functional programming, streaming
- [interop.md](references/interop.md) - External command integration, `complete`, `extern`
- [scripting.md](references/scripting.md) - Custom commands, modules, `main`, control flow
- [production.md](references/production.md) - Testing, validation, logging, error handling patterns

**Plugin Development** (for building Nushell plugins in Rust):

- [plugins.md](references/plugins.md) - Complete guide to building Nushell plugins
- Template: `scripts/init_plugin.py` and `assets/plugin-template/`

## Running Nushell

```bash
nu                           # Interactive shell
nu script.nu                 # Run script
nu -c 'command'              # One-liner
```
