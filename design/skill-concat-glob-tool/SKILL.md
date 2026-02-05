---
name: skill-concat-glob-tool
description: File concatenation with glob patterns guide
---

# When to use
- Need to concatenate multiple files matching patterns
- Creating LLM context files from source code
- Merging documentation or configuration files
- Building single-file distributions

# concat-glob-tool Skill

## Purpose

Master file concatenation with glob patterns for efficient file merging, documentation bundling, and LLM context generation. This skill covers CLI usage, library integration, and advanced patterns.

## When to Use This Skill

**Use this skill when:**
- Concatenating files matching glob patterns (*.py, src/**/*.md)
- Creating context files for Large Language Models
- Merging multiple source files for documentation
- Building single-file distributions with separators
- Integrating file concatenation into Python scripts

**Do NOT use this skill for:**
- Single file operations (use `cat` or `cp`)
- Binary file concatenation (use specialized tools)
- Real-time streaming (this is batch processing)

## CLI Tool: concat-glob-tool

A production-ready CLI utility that concatenates files matching glob patterns with intelligent separators. Features dry-run mode, stdin support, and both CLI and library modes.

### Installation

```bash
# From source
git clone https://github.com/dnvriend/concat-glob-tool.git
cd concat-glob-tool
uv tool install .

# Verify
concat-glob-tool --version
```

### Prerequisites

- Python 3.14+
- uv package manager
- Access to file system

### Quick Start

```bash
# Preview (dry-run, default)
concat-glob-tool '*.py' -o output.txt

# Execute
concat-glob-tool '*.py' '*.md' -o output.txt --no-dry-run

# Stdin mode
find . -name '*.py' | concat-glob-tool --stdin -o output.txt --no-dry-run
```

## Progressive Disclosure

<details>
<summary><strong>📖 Core Commands (Click to expand)</strong></summary>

### concat - Concatenate Files with Glob Patterns

Concatenate files matching glob patterns to a single output file with intelligent separators.

**Usage:**
```bash
concat-glob-tool PATTERNS... --output-file FILE [OPTIONS]
```

**Arguments:**
- `PATTERNS...`: One or more glob patterns (e.g., `*.py`, `src/**/*.md`)
- `-o, --output-file FILE`: Output file path (required)
- `--separator TEXT`: Separator text between files (default: `---`)
- `-n, --dry-run`: Preview without writing (enabled by default)
- `--no-dry-run`: Actually execute the concatenation
- `-f, --force`: Overwrite existing output file
- `-v, --verbose`: Enable verbose output (repeatable: -v, -vv, -vvv)
- `--version`: Show version
- `--help`: Show help message with examples

**Examples:**
```bash
# Basic concatenation - preview mode (dry-run)
concat-glob-tool '*.py' -o output.txt

# Execute concatenation
concat-glob-tool '*.py' -o output.txt --no-dry-run

# Multiple patterns
concat-glob-tool '*.py' '*.md' '*.txt' -o combined.txt --no-dry-run

# Recursive patterns
concat-glob-tool 'src/**/*.py' -o all-code.txt --no-dry-run

# Multiple recursive patterns
concat-glob-tool 'src/**/*.py' 'tests/**/*.py' -o codebase.txt --no-dry-run

# Custom separator
concat-glob-tool '*.py' -o output.txt --separator '===' --no-dry-run

# Force overwrite existing file
concat-glob-tool '*.py' -o existing.txt --force --no-dry-run

# Verbose output
concat-glob-tool '*.py' -o output.txt -vv --no-dry-run

# LLM context generation
concat-glob-tool 'src/**/*.py' 'tests/**/*.py' '*.md' \
    -o llm-context.txt \
    --separator '---' \
    --no-dry-run
```

**Output Format:**
Files are concatenated with this separator format between each file:
```
---
# /path/to/file.py
---
[file contents]
```

The separator includes:
- Blank line before separator
- Separator line (configurable, default: `---`)
- Comment line with full file path
- Separator line  
- Blank line before file contents

**Dry-Run Mode (Default):**
By default, the tool runs in preview mode showing:
- Number of files that would be concatenated
- List of files to process
- Separator format
- Reminder to use `--no-dry-run` to execute

This prevents accidental overwrites and lets you verify operations first.

---

### stdin - Concatenate from Stdin

Read file paths from stdin and concatenate them. Useful for integration with `find`, `fd`, `grep`, and other tools.

**Usage:**
```bash
find ... | concat-glob-tool --stdin --output-file FILE [OPTIONS]
```

**Arguments:**
- `-s, --stdin`: Read file paths from stdin (one per line)
- `-o, --output-file FILE`: Output file path (required)
- `--separator TEXT`: Separator text (default: `---`)
- `--no-dry-run`: Execute the concatenation
- `-f, --force`: Overwrite existing output file
- `-v, --verbose`: Verbose output

**Examples:**
```bash
# From find command
find . -name '*.py' -type f | concat-glob-tool --stdin -o output.txt --no-dry-run

# From fd (faster find alternative)
fd -e py | concat-glob-tool --stdin -o output.txt --no-dry-run

# Filter with grep
find . -name '*.py' | grep -v test | concat-glob-tool --stdin -o output.txt --no-dry-run

# Complex pipeline
find . -name '*.py' -type f | \
    grep -v __pycache__ | \
    grep -v .venv | \
    concat-glob-tool --stdin -o filtered.txt --no-dry-run

# With custom separator
find . -name '*.md' | concat-glob-tool --stdin -o docs.txt --separator '===' --no-dry-run
```

**Note:**
- Cannot use both `--stdin` and glob patterns in the same command
- Each line from stdin should be a valid file path
- Invalid paths will cause clear error messages with solutions

</details>

<details>
<summary><strong>⚙️ Advanced Features (Click to expand)</strong></summary>

### Environment Variable Expansion

Glob patterns support environment variable expansion and home directory shortcuts.

**Examples:**
```bash
# Home directory expansion
concat-glob-tool '~/projects/*.py' -o output.txt --no-dry-run

# Environment variables
concat-glob-tool '$HOME/src/**/*.py' -o output.txt --no-dry-run

# Mixed
concat-glob-tool '~/.config/*.conf' '$PROJECT_DIR/**/*.md' -o output.txt --no-dry-run
```

---

### Library Integration

Use concat-glob-tool as a Python library for programmatic integration.

**Installation:**
```bash
pip install concat-glob-tool
# or
uv add concat-glob-tool
```

**Core API:**
```python
from concat_glob_tool import (
    expand_glob_patterns,
    concatenate_files,
    format_separator,
    ConcatError,
    NoMatchesError,
    OutputExistsError,
)
from pathlib import Path

# Expand glob patterns
files = expand_glob_patterns(["*.py", "src/**/*.md"])
print(f"Found {len(files)} files")

# Concatenate files
result = concatenate_files(
    files=files,
    output_file=Path("output.txt"),
    separator="---",
    force=False,
    dry_run=False,
)

print(f"Concatenated {result['files_count']} files")
print(f"Wrote {result['bytes_written']} bytes to {result['output_file']}")
```

**Exception Handling:**
```python
from pathlib import Path
from concat_glob_tool import (
    concatenate_files,
    expand_glob_patterns,
    NoMatchesError,
    OutputExistsError,
    ConcatError,
)

try:
    files = expand_glob_patterns(["*.py"])
    result = concatenate_files(
        files=files,
        output_file=Path("output.txt"),
        force=False,
        dry_run=False,
    )
    print(f"Success: {result}")

except NoMatchesError as e:
    print(f"No files found: {e}")
except OutputExistsError as e:
    print(f"Output exists: {e}")
except ConcatError as e:
    print(f"Error: {e}")
```

**Integration Example:**
```python
#!/usr/bin/env python3
"""Example: Concatenate Python files with custom logic."""

from pathlib import Path
from concat_glob_tool import expand_glob_patterns, concatenate_files

def main():
    # Find all Python files
    files = expand_glob_patterns(["src/**/*.py", "tests/**/*.py"])
    
    # Filter files (e.g., exclude __init__.py)
    filtered_files = [f for f in files if f.name != "__init__.py"]
    
    # Concatenate
    result = concatenate_files(
        files=filtered_files,
        output_file=Path("codebase.txt"),
        separator="===",
        force=True,
        dry_run=False,
    )
    
    print(f"✅ Concatenated {result['files_count']} files")
    print(f"📝 Output: {result['output_file']}")
    print(f"💾 Size: {result['bytes_written']} bytes")

if __name__ == "__main__":
    main()
```

---

### Custom Separators

Customize the separator text while maintaining the format structure.

**Examples:**
```bash
# Simple separator
concat-glob-tool '*.py' -o output.txt --separator '---' --no-dry-run

# Equals signs
concat-glob-tool '*.py' -o output.txt --separator '===' --no-dry-run

# Hash separator
concat-glob-tool '*.py' -o output.txt --separator '###' --no-dry-run

# Custom text
concat-glob-tool '*.py' -o output.txt --separator 'FILE' --no-dry-run
```

**Separator Format:**
The separator structure is always: `\n{separator}\n# {filename}\n{separator}\n`

Example with `--separator '==='`:
```
===
# /path/to/file.py
===
[file contents]
```

</details>

<details>
<summary><strong>🔧 Troubleshooting (Click to expand)</strong></summary>

### Common Issues

**Issue: No files matched the patterns**
```bash
$ concat-glob-tool '*.nonexistent' -o out.txt --no-dry-run
Error: No files matched the patterns: *.nonexistent

Solution: Verify glob patterns are correct. Examples:
  - '*.py' for Python files in current directory
  - '**/*.py' for Python files recursively
  - 'src/**/*.{py,md}' for multiple extensions
```

**Solution:**
- Check glob pattern syntax
- Verify files exist in specified locations
- Use `--verbose` to see detailed logging
- Test pattern with `ls` first: `ls *.py`

---

**Issue: Output file already exists**
```bash
$ concat-glob-tool '*.py' -o existing.txt --no-dry-run
Error: Output file already exists: existing.txt

Solution: Use --force to overwrite or choose a different output file.
```

**Solution:**
- Use `--force` flag to overwrite: `concat-glob-tool '*.py' -o existing.txt --force --no-dry-run`
- Choose different output filename
- Remove existing file first

---

**Issue: Cannot use both --stdin and glob patterns**
```bash
$ concat-glob-tool '*.py' --stdin -o out.txt
Error: Cannot use both --stdin and glob patterns.

Solution: Use either --stdin OR provide glob patterns, not both.
```

**Solution:**
- Use glob patterns: `concat-glob-tool '*.py' -o out.txt --no-dry-run`
- OR use stdin: `find . -name '*.py' | concat-glob-tool --stdin -o out.txt --no-dry-run`

---

**Issue: Forgot --no-dry-run flag**
```bash
$ concat-glob-tool '*.py' -o output.txt
[DRY-RUN] Would concatenate 10 files to: output.txt
...
To execute, add --no-dry-run flag.
```

**Solution:**
- This is expected behavior (dry-run is default)
- Add `--no-dry-run` to actually execute
- Dry-run mode prevents accidental overwrites

### Getting Help

```bash
# Full help with examples
concat-glob-tool --help

# Version information
concat-glob-tool --version

# Verbose output for debugging
concat-glob-tool '*.py' -o output.txt -vv --no-dry-run
```

### Verbose Logging Levels

- No flag (default): WARNING only
- `-v`: INFO level (operations and progress)
- `-vv`: DEBUG level (detailed information)
- `-vvv`: TRACE level (library internals)

All logs go to stderr, keeping stdout clean for piping.

</details>

## Exit Codes

- `0`: Success
- `1`: Error (NoMatchesError, OutputExistsError, ConcatError, validation errors)

## Output Formats

**Separator Format:**
```
\n---\n# /path/to/filename\n---\n
```

Components:
- Blank line before separator
- Separator line (customizable via `--separator`)
- Comment line with full file path
- Separator line
- Blank line before file contents

**Dry-Run Output:**
- Number of files to concatenate
- List of file paths
- Separator format preview
- Instructions to execute

**Execution Output:**
```
Successfully concatenated 10 files to output.txt (52482 bytes)
```

## Best Practices

1. **Always Preview First**: Use default dry-run mode to verify operations before executing with `--no-dry-run`

2. **Use Descriptive Output Names**: Name output files clearly indicating contents (e.g., `llm-context.txt`, `all-python-code.txt`)

3. **Leverage Verbose Mode**: Use `-v` or `-vv` when troubleshooting or learning the tool's behavior

4. **Quote Glob Patterns**: Always quote patterns in shell to prevent premature expansion: `'*.py'` not `*.py`

5. **Test Patterns with ls**: Verify glob patterns work with `ls` before using in concat-glob-tool

6. **Use stdin for Complex Filtering**: Combine with `find`, `fd`, `grep` for advanced file selection

7. **Custom Separators for Context**: Use meaningful separators when creating context files for specific purposes

## Resources

- **GitHub**: https://github.com/dnvriend/concat-glob-tool
- **Documentation**: README.md in repository
- **Python Package**: Available via pip/uv
- **License**: MIT
