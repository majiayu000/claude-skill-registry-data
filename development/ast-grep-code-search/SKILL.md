---
name: AST-Grep Code Search
description: Performs structural code search and refactoring using AST-based patterns. Use when searching for code patterns, refactoring code structurally, finding function calls, class definitions, or when the user mentions "ast-grep", "structural search", "code pattern", or needs to find/replace code that's difficult with regex.
---

# AST-Grep Code Search

Helps perform structural code search and automated refactoring using Abstract Syntax Tree (AST) patterns. Unlike grep/regex which work on text, ast-grep understands code structure and can match patterns across multiple lines while ignoring formatting differences.

## Core Responsibilities

1. **Structural pattern matching** - Find code patterns based on AST structure, not text
2. **Language-aware search** - Understands syntax for multiple languages (JS, TS, Python, Rust, Go, etc.)
3. **Smart refactoring** - Replace code patterns while preserving formatting and semantics
4. **Cross-file operations** - Search and replace across entire codebases
5. **Metavariable capture** - Capture and reuse parts of matched patterns

## When to Use AST-Grep vs Regular Grep

**Use AST-Grep when**:
- Searching for code patterns that span multiple lines
- Formatting/whitespace differences should be ignored
- Need to match specific language constructs (functions, classes, expressions)
- Performing structural refactoring or code transformations
- Finding patterns that are difficult to express with regex

**Use Regular Grep when**:
- Simple string/regex search is sufficient
- Searching for text in non-code files
- Performance is critical for very large codebases

## Installation Check

Before using ast-grep, verify it's installed:
```bash
# Check if ast-grep is available
which ast-grep || echo "ast-grep not installed"
```

If not installed, guide the user to install it:
```bash
# Install via cargo (Rust)
cargo install ast-grep

# Or via npm
npm install -g @ast-grep/cli

# Or via homebrew (macOS)
brew install ast-grep
```

## Basic Usage

```bash
# Simple search
ast-grep --pattern 'console.log($$$)' --lang js

# With context lines
ast-grep --pattern 'useEffect($$$)' --lang tsx -C 3

# Search and replace (dry-run)
ast-grep --pattern 'console.log($$$ARGS)' --rewrite 'logger.debug($$$ARGS)' --lang js

# Apply changes
ast-grep --pattern 'console.log($$$ARGS)' --rewrite 'logger.debug($$$ARGS)' --lang js --update-all

# Language-specific patterns
ast-grep --pattern 'class $NAME: $$$' --lang python  # Python classes
ast-grep --pattern 'impl $$$' --lang rust            # Rust impl blocks
ast-grep --pattern 'interface $NAME { $$$ }' --lang typescript  # TS interfaces

# YAML config for complex patterns (pattern-config.yml)
# rule:
#   pattern: console.log($MSG)
#   constraints:
#     MSG:
#       regex: "error|warning|debug"
ast-grep scan --config pattern-config.yml
```

## Metavariable Syntax

- `$VAR` - Single AST node | `$OBJ.$PROP()`
- `$$$` - Zero or more nodes | `function $NAME($$$ARGS) { $$$BODY }`
- `$_` - Match without capture

## Common Patterns

```bash
# TODOs: ast-grep --pattern '// TODO: $$$' --lang js
# API refactor: ast-grep --pattern 'fetch($URL)' --rewrite 'axios.get($URL)' --lang js --update-all
# Security audit: ast-grep --pattern 'eval($$$)' --lang js
# Imports: ast-grep --pattern 'import { $$$NAMES } from "$MODULE"' --lang js
# Modernize: ast-grep --pattern 'var $NAME = $$$' --rewrite 'const $NAME = $$$' --lang js --update-all
```

## Refactoring Workflow

1. **Verify**: `ast-grep --pattern '<pattern>' --lang <lang>` - Review matches
2. **Dry-run**: Add `--rewrite '<replacement>'` - Preview changes
3. **Interactive**: Add `--interactive` - Review each change
4. **Apply**: Use `--update-all` instead of `--interactive`
5. **Verify**: `git diff && npm test && npm run lint`

## Language Support

AST-grep supports many languages. Specify with `--lang`:

- **JavaScript**: `js`, `javascript`
- **TypeScript**: `ts`, `typescript`, `tsx`
- **Python**: `py`, `python`
- **Rust**: `rs`, `rust`
- **Go**: `go`, `golang`
- **Java**: `java`
- **C/C++**: `c`, `cpp`, `cxx`
- **C#**: `cs`, `csharp`
- **Ruby**: `rb`, `ruby`
- **HTML**: `html`
- **CSS**: `css`
- **JSON**: `json`

## Output & Filtering

```bash
# JSON output: --json | Compact: --compact | Default: colored
# File: ast-grep --pattern '<pattern>' --lang js src/main.js
# Directory: ast-grep --pattern '<pattern>' --lang js src/
# Glob: find src -name "*.test.js" -exec ast-grep --pattern '<pattern>' --lang js {} +
```

## Advanced: Rule Configuration Files

For complex searches, create YAML configuration files:

**Example: `.ast-grep/rules/no-console.yml`**
```yaml
id: no-console-log
language: TypeScript
rule:
  pattern: console.log($$$)
message: "Avoid using console.log in production code"
severity: warning
fix:
  pattern: console.log($$$ARGS)
  rewrite: logger.debug($$$ARGS)
```

Then scan with:
```bash
ast-grep scan
```

## Best Practices

- Always specify `--lang` for performance
- Test patterns with dry-run before `--update-all`
- Commit code before bulk refactoring
- Review with `git diff` and run tests after changes
- Break large refactorings into incremental steps
- Save complex patterns as YAML rule files

## Integration Examples

```bash
# Git: git diff --staged --name-only | xargs ast-grep --pattern '<pattern>' --lang js
# CI/hooks: ast-grep scan --error-on-warning
```

## Troubleshooting

- **No matches**: Check `--lang`, verify syntax at https://ast-grep.github.io/playground.html, simplify pattern
- **Too many**: Add context, use YAML constraints, filter paths
- **Slow**: Use specific paths, patterns, language filters

## Example Workflows

```bash
# Remove console.logs
ast-grep --pattern 'console.log($$$)' --rewrite '' --lang js --interactive

# API migration (user.getName() → user.profile.name)
ast-grep --pattern '$USER.getName()' --rewrite '$USER.profile.name' --lang ts --update-all

# Security audit
ast-grep --pattern 'dangerouslySetInnerHTML={{ __html: $$$ }}' --lang jsx
ast-grep --pattern 'eval($$$)' --lang js
```

## Resources

- Docs: https://ast-grep.github.io/ | Playground: https://ast-grep.github.io/playground.html
- GitHub: https://github.com/ast-grep/ast-grep
