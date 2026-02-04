---
name: filesystem
description: Filesystem operations and codebase navigation. Use when exploring project structure, finding files, searching code, reading/writing files, or understanding codebase organization.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Filesystem Operations

Efficient patterns for navigating and manipulating the codebase.

## Finding Files

### By Pattern (Glob)
```
Use tool: Glob
Parameter: pattern = "<glob pattern>"
```

Common patterns:
```
# All Rust files
**/*.rs

# All test files
**/tests/**/*.rs
**/*_test.rs

# Cargo manifests
**/Cargo.toml

# Specific crate
crates/nebula-core/**/*.rs

# Config files
**/*.toml
**/*.yaml
**/*.json

# Documentation
**/*.md
**/docs/**/*
```

### By Content (Grep)
```
Use tool: Grep
Parameters:
  pattern = "<regex pattern>"
  path = "<directory>" (optional)
  output_mode = "files_with_matches" | "content" | "count"
```

Examples:
```
# Find struct definitions
pattern: "pub struct \w+"
output_mode: "content"

# Find function implementations
pattern: "fn process_"
output_mode: "files_with_matches"

# Find TODO comments
pattern: "TODO|FIXME|HACK"
output_mode: "content"

# Find imports of specific module
pattern: "use crate::error"
output_mode: "files_with_matches"

# Count occurrences
pattern: "unwrap\(\)"
output_mode: "count"
```

### With Context (Grep -C)
```
# Show surrounding lines
pattern: "impl.*Error"
output_mode: "content"
-C: 5  # 5 lines before and after
```

## Reading Files

### Single File
```
Use tool: mcp__acp__Read
Parameter: file_path = "<absolute path>"
```

### Partial Read (Large Files)
```
Use tool: mcp__acp__Read
Parameters:
  file_path = "<absolute path>"
  offset = 100  # Start at line 100
  limit = 50    # Read 50 lines
```

### Multiple Files
Read files in parallel when independent:
```
# Call Read for each file simultaneously
file_path = "/path/to/file1.rs"
file_path = "/path/to/file2.rs"
file_path = "/path/to/file3.rs"
```

## Writing Files

### Create New File
```
Use tool: mcp__acp__Write
Parameters:
  file_path = "<absolute path>"
  content = "<file content>"
```

### Edit Existing File
```
Use tool: mcp__acp__Edit
Parameters:
  file_path = "<absolute path>"
  old_string = "<text to replace>"
  new_string = "<replacement text>"
```

For multiple replacements:
```
# Replace all occurrences
replace_all = true
```

## Directory Operations

### List Directory
```bash
ls -la <directory>
```

### Create Directory
```bash
mkdir -p path/to/new/directory
```

### Find by Type
```bash
# Only directories
find . -type d -name "*test*"

# Only files
find . -type f -name "*.rs"

# By modification time
find . -type f -mtime -1  # Modified in last day
```

## Project Structure Analysis

### Crate Dependencies
```bash
# Show dependency tree
cargo tree

# Show what depends on a crate
cargo tree --invert -p <crate-name>

# Show features
cargo tree -f "{p} {f}"
```

### Module Structure
```bash
# Find all mod.rs files
find . -name "mod.rs" -type f

# Find lib.rs files
find . -name "lib.rs" -type f
```

### Size Analysis
```bash
# Lines of code per file
find . -name "*.rs" -exec wc -l {} + | sort -n

# Count files by extension
find . -type f | sed 's/.*\.//' | sort | uniq -c | sort -rn
```

## Code Navigation Patterns

### Find Definition
```
# Struct/enum definition
Grep: pattern = "pub (struct|enum) TypeName"

# Function definition
Grep: pattern = "pub fn function_name"

# Trait definition
Grep: pattern = "pub trait TraitName"

# Impl block
Grep: pattern = "impl.*TypeName"
```

### Find Usages
```
# Type usage
Grep: pattern = "TypeName"

# Function calls
Grep: pattern = "function_name\("

# Import statements
Grep: pattern = "use.*module::item"
```

### Find Related Code
```
# All tests for a module
Glob: pattern = "**/module_name/**/*test*.rs"

# Error handling for a type
Grep: pattern = "Error::TypeName|TypeNameError"
```

## Workspace Navigation

### Nebula-Specific Patterns

```
# Find crate's main module
Glob: crates/<crate-name>/src/lib.rs

# Find crate's error types
Grep: pattern = "#\[derive.*Error\]"
      path = "crates/<crate-name>"

# Find public API
Grep: pattern = "^pub (fn|struct|enum|trait|type)"
      path = "crates/<crate-name>/src"

# Find tests
Glob: crates/<crate-name>/tests/**/*.rs
Glob: crates/<crate-name>/src/**/*test*.rs

# Find benchmarks
Glob: crates/<crate-name>/benches/**/*.rs
```

### Cross-Crate Analysis
```
# Find all uses of a core type
Grep: pattern = "use nebula_core::TypeName"

# Find inter-crate dependencies
Grep: pattern = 'nebula-\w+\s*=' path = "**/Cargo.toml"
```

## Best Practices

1. **Use Glob for file discovery**, Grep for content search
2. **Read files before editing** - understand context
3. **Minimize file reads** - batch related operations
4. **Use specific patterns** - avoid overly broad searches
5. **Check results** - verify changes with Read after Edit
6. **Respect .gitignore** - avoid generated files (target/, etc.)

## Common Workflows

### Explore New Module
1. Glob: `crates/<name>/src/**/*.rs` - list all files
2. Read: `lib.rs` - understand exports
3. Grep: `pub` - find public API
4. Read: specific files of interest

### Find and Fix Pattern
1. Grep: find all occurrences
2. Read: understand each context
3. Edit: apply fix
4. Grep: verify no remaining occurrences

### Understand Type Usage
1. Grep: find definition
2. Read: understand the type
3. Grep: find all usages
4. Read: understand usage patterns
