---
name: cli-ninja
description: Master CLI navigation and code exploration using modern command-line tools. Use this skill when navigating repositories, searching for files/text/code patterns, or working with structured data (JSON/YAML/XML). Provides guidance on fd (file finding), rg (text search), ast-grep (code structure), fzf (interactive selection), jq (JSON), and yq (YAML/XML).
---

# CLI Ninja

## Overview

This skill provides guidance for efficient repository navigation and code exploration using modern CLI tools. Each tool serves a specific purpose: `fd` for finding files, `rg` for searching text, `ast-grep` for understanding code structure, `fzf` for interactive selection, `jq` for JSON manipulation, and `yq` for YAML/XML processing.

## Tool Selection Decision Tree

When navigating or exploring a repository, choose the appropriate tool based on the task:

```
What are you looking for?

├─ FILES by name/path/extension?
│  └─ Use: fd
│     └─ Need to select from results? → Pipe to fzf
│
├─ TEXT/STRINGS in file contents?
│  └─ Use: rg (ripgrep)
│     └─ Need to select from results? → Pipe to fzf
│
├─ CODE STRUCTURE (functions, classes, imports)?
│  └─ Use: ast-grep
│     └─ Need to select from results? → Pipe to fzf
│     └─ Need to refactor/replace? → Use ast-grep --rewrite
│
├─ Working with JSON data?
│  └─ Use: jq
│
└─ Working with YAML or XML data?
   └─ Use: yq
```

## Quick Reference Guide

### fd - Find Files

**Basic patterns:**
```bash
# Find by name
fd 'pattern'

# Find by extension
fd -e py          # All Python files
fd -e 'test.py$'  # Files ending in test.py

# Find in specific directory
fd 'pattern' src/

# Case-insensitive
fd -i readme

# Hidden files
fd -H '.env'

# Exclude patterns
fd -e py -E '*test*'
```

**Common workflows:**
```bash
# Find and edit a config file interactively
fd config | fzf | xargs $EDITOR

# Find all Python files modified in last 7 days
fd -e py -td --changed-within 7d

# Find files by size
fd -e db --size +100m
```

See `references/fd-patterns.md` for comprehensive patterns and flags.

### rg - Search Text/Strings

**Basic patterns:**
```bash
# Basic search
rg 'search_term'

# Case-insensitive
rg -i 'search_term'

# Whole word only
rg -w 'word'

# With context lines
rg -C 3 'pattern'        # 3 lines before/after
rg -B 2 -A 5 'pattern'   # 2 before, 5 after

# Specific file types
rg -t py 'import'        # Python files
rg -t rust 'fn main'     # Rust files
```

**Advanced usage:**
```bash
# Search with line numbers and file names
rg -n 'pattern'

# Multiline search
rg -U 'pattern.*spanning.*lines'

# Exclude patterns
rg 'TODO' -g '!*test*'

# Search in specific directories
rg 'pattern' src/ core/

# JSON output for scripting
rg --json 'pattern'
```

**Interactive workflows:**
```bash
# Search and open in editor
rg -l 'TODO' | fzf | xargs $EDITOR

# Search with preview
rg --line-number 'pattern' | fzf --preview 'bat --color=always {1} --highlight-line {2}'
```

See `references/rg-patterns.md` for regex tips and advanced patterns.

### ast-grep - Find Code Structure

**Philosophy:** ast-grep searches code by structure, not strings. It understands programming language syntax and semantics.

**Basic patterns:**

**Python:**
```bash
# Find all function definitions
ast-grep --pattern 'def $FUNC($$$)' -l py

# Find specific function calls
ast-grep --pattern 'player.play($$$)' -l py

# Find class definitions
ast-grep --pattern 'class $CLASS:' -l py

# Find all imports of a module
ast-grep --pattern 'from $MOD import $$$' -l py
ast-grep --pattern 'import $MOD' -l py

# Find type annotations
ast-grep --pattern 'def $FUNC($$$) -> $TYPE:' -l py
```

**JavaScript/TypeScript:**
```bash
# Find React components
ast-grep --pattern 'function $COMP() { $$$ }' -l tsx

# Find useState hooks
ast-grep --pattern 'const [$STATE, $SETTER] = useState($$$)' -l tsx

# Find async functions
ast-grep --pattern 'async function $FUNC($$$) { $$$ }' -l js

# Find imports
ast-grep --pattern 'import $$ from "$MODULE"' -l ts
```

**Rust:**
```bash
# Find function definitions
ast-grep --pattern 'fn $FUNC($$$) { $$$ }' -l rs

# Find struct definitions
ast-grep --pattern 'struct $NAME { $$$ }' -l rs

# Find impl blocks
ast-grep --pattern 'impl $TRAIT for $TYPE { $$$ }' -l rs

# Find macro usage
ast-grep --pattern 'println!($$$)' -l rs
```

**Go:**
```bash
# Find function definitions
ast-grep --pattern 'func $FUNC($$$) $$$ { $$$ }' -l go

# Find struct definitions
ast-grep --pattern 'type $NAME struct { $$$ }' -l go

# Find interface implementations
ast-grep --pattern 'func ($RECV $TYPE) $METHOD($$$) $$$ { $$$ }' -l go

# Find goroutines
ast-grep --pattern 'go $FUNC($$$)' -l go
```

**Zig:**
```bash
# Find function definitions
ast-grep --pattern 'pub fn $FUNC($$$) $$$ { $$$ }' -l zig

# Find struct definitions
ast-grep --pattern 'const $NAME = struct { $$$ };' -l zig

# Find test functions
ast-grep --pattern 'test "$NAME" { $$$ }' -l zig

# Find error handling
ast-grep --pattern 'try $EXPR' -l zig
```

**Ruby:**
```bash
# Find method definitions
ast-grep --pattern 'def $METHOD($$$); $$$; end' -l rb

# Find class definitions
ast-grep --pattern 'class $CLASS; $$$; end' -l rb

# Find blocks
ast-grep --pattern '$EXPR do |$PARAM|; $$$; end' -l rb

# Find Rails routes
ast-grep --pattern 'get "$PATH", to: "$HANDLER"' -l rb
```

**Refactoring with ast-grep:**
```bash
# Rename a function across the codebase
ast-grep --pattern 'old_function($$$)' --rewrite 'new_function($$$)' -l py --interactive

# Update API calls
ast-grep --pattern 'api.v1.$METHOD($$$)' --rewrite 'api.v2.$METHOD($$$)' -l py

# Modernize code patterns
ast-grep --pattern 'var $VAR = $EXPR' --rewrite 'const $VAR = $EXPR' -l js
```

**Interactive workflows:**
```bash
# Find and select a function to edit
ast-grep --pattern 'def $FUNC($$$)' -l py | fzf | cut -d: -f1 | xargs $EDITOR

# Find all TODOs in code comments (use rg instead)
rg 'TODO|FIXME' | fzf
```

See `references/ast-grep-guide.md` for comprehensive patterns across all languages.

### fzf - Interactive Selection

**Basic usage:**
```bash
# Pipe any list to fzf for selection
command | fzf

# Multi-select mode
command | fzf -m

# With preview window
command | fzf --preview 'bat {}'
```

**Preview configurations:**
```bash
# Preview files with syntax highlighting
fd -t f | fzf --preview 'bat --color=always {}'

# Preview with line numbers
rg --line-number 'pattern' | fzf --preview 'bat --color=always {1} --highlight-line {2}'

# Preview JSON files
fd -e json | fzf --preview 'jq . {}'

# Custom preview window size
fzf --preview 'cat {}' --preview-window=right:50%
```

**Keybindings:**
```bash
# ctrl-t: Paste selected files
# ctrl-r: Paste from history
# alt-c: cd into selected directory

# Custom keybindings
fzf --bind 'ctrl-y:execute-silent(echo {} | pbcopy)'
```

See `references/fzf-workflows.md` for advanced interactive workflows.

### jq - JSON Processing

**Basic queries:**
```bash
# Pretty print
jq . file.json

# Extract field
jq '.name' file.json

# Array indexing
jq '.[0]' file.json

# Nested access
jq '.user.name' file.json

# Array operations
jq '.[] | .name' file.json
```

**Common transformations:**
```bash
# Filter arrays
jq '.users[] | select(.active == true)' file.json

# Map over arrays
jq '.users | map(.name)' file.json

# Sorting
jq '.users | sort_by(.age)' file.json

# Group by
jq 'group_by(.category)' file.json

# Count items
jq '.items | length' file.json

# Keys extraction
jq 'keys' file.json
```

**Advanced usage:**
```bash
# Multiple filters
jq '.users[] | select(.age > 18) | .name' file.json

# Construct new objects
jq '{name: .firstName, email: .emailAddress}' file.json

# Combine multiple files
jq -s '.[0] + .[1]' file1.json file2.json

# Read from stdin
curl -s https://api.example.com/data | jq '.results[]'
```

See `references/jq-cookbook.md` for comprehensive transformations.

### yq - YAML/XML Processing

**YAML queries:**
```bash
# Pretty print
yq . file.yaml

# Extract field
yq '.name' file.yaml

# Nested access
yq '.services.web.image' docker-compose.yml

# Array operations
yq '.dependencies[]' file.yaml

# Convert to JSON
yq -o json . file.yaml
```

**XML queries:**
```bash
# Parse XML
yq -p xml . file.xml

# Extract elements
yq -p xml '.root.element' file.xml

# Convert XML to JSON
yq -p xml -o json . file.xml
```

**Common operations:**
```bash
# Update values
yq '.version = "2.0"' file.yaml

# Merge files
yq '. *= load("other.yaml")' file.yaml

# Filter arrays
yq '.items[] | select(.enabled == true)' file.yaml
```

See `references/yq-examples.md` for YAML/XML processing patterns.

## Combination Workflows

Real-world tasks often combine multiple tools:

### 1. Find and Edit Files with Context

```bash
# Find Python files containing a function, preview them, then edit
rg -l 'def process_data' -t py | fzf --preview 'rg -C 5 "def process_data" {}' | xargs $EDITOR
```

### 2. Code Refactoring Workflow

```bash
# Find all usages of a function across the codebase
ast-grep --pattern 'old_function($$$)' -l py | fzf -m

# Then refactor with interactive confirmation
ast-grep --pattern 'old_function($$$)' --rewrite 'new_function($$$)' -l py --interactive
```

### 3. Interactive Configuration Explorer

```bash
# Find config files and explore their structure
fd -e json -e yaml | fzf --preview 'bat --color=always {} --style=numbers'

# Or with jq/yq preview
fd -e json | fzf --preview 'jq . {}'
fd -e yaml | fzf --preview 'yq . {}'
```

### 4. Find Related Code

```bash
# Find a class definition, then find all its usages
CLASS=$(ast-grep --pattern 'class $NAME:' -l py | fzf | cut -d: -f2)
rg -w "$CLASS" --type py
```

### 5. Dependency Analysis

```bash
# Find all imports of a module
ast-grep --pattern 'from mymodule import $$$' -l py -t python

# Combine with text search for dynamic imports
rg 'importlib.*mymodule' -t py
```

### 6. Multi-File Search and Replace

```bash
# Find files with pattern, select multiple, and apply changes
rg -l 'TODO.*urgent' | fzf -m | xargs sed -i '' 's/TODO.*urgent/DONE/g'
```

### 7. Code Structure Analysis

```bash
# Find all functions in a module, count them
ast-grep --pattern 'def $FUNC($$$)' -l py src/module.py | wc -l

# Find function complexity (functions with many parameters)
ast-grep --pattern 'def $FUNC($A, $B, $C, $D, $E, $$$)' -l py
```

See `scripts/combo-search.sh` and `scripts/interactive-code-finder.sh` for reusable combination workflows.

## Best Practices

### Performance Tips

1. **Use the right tool for the job:**
   - File names → `fd`
   - Text content → `rg`
   - Code structure → `ast-grep`

2. **Narrow your search scope:**
   ```bash
   # Good: Search specific directory
   rg 'pattern' src/

   # Better: Search specific file types
   rg 'pattern' -t py src/
   ```

3. **Use `.gitignore` respect:**
   - Both `fd` and `rg` respect `.gitignore` by default
   - Use `-u` or `--no-ignore` to override when needed

### Pattern Matching Tips

1. **ast-grep patterns:**
   - Use `$VAR` for single identifiers
   - Use `$$$` for arbitrary code sequences
   - Use `$$` for statement lists

2. **ripgrep regex:**
   - Use `-F` for literal strings (faster)
   - Use `-w` for whole words
   - Use `\b` for word boundaries

3. **fzf fuzzy matching:**
   - Space for AND search: `foo bar` matches files with both
   - `|` for OR search: `foo|bar`
   - `^` for prefix match, `$` for suffix match

### Debugging Searches

```bash
# See what rg is searching
rg --debug 'pattern' 2>&1 | head -20

# Dry-run ast-grep refactoring
ast-grep --pattern 'old' --rewrite 'new' --interactive

# Test jq queries incrementally
echo '{"name":"test"}' | jq .
echo '{"name":"test"}' | jq '.name'
```

## Resources

This skill includes bundled resources to support CLI navigation:

### scripts/

Example scripts demonstrating tool combinations:

- `combo-search.sh` - Common combination workflows
- `interactive-code-finder.sh` - Interactive ast-grep + fzf workflow

### references/

Comprehensive guides for each tool:

- `fd-patterns.md` - File finding patterns and flags
- `rg-patterns.md` - Text search patterns and regex tips
- `ast-grep-guide.md` - Code structure patterns for Python, Zig, Go, Ruby, JS/TS, Rust
- `fzf-workflows.md` - Interactive selection and preview configurations
- `jq-cookbook.md` - JSON transformations and filters
- `yq-examples.md` - YAML/XML processing examples
