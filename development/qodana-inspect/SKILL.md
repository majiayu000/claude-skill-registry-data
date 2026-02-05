---
name: qodana-inspect
description: Run Qodana code inspection and get parsed results. Use when you need to analyze code quality, find unused code, detect potential bugs, or check for JetBrains IDE inspections. Supports all major programming languages (Java, Kotlin, Python, JavaScript, TypeScript, C#, C++, Go, Ruby, PHP). Returns structured list of problems grouped by file with severity, location, and code snippets.
---

# Qodana Code Inspector

This skill runs Qodana static analysis on the current project and returns parsed inspection results in an easy-to-read format. It supports all JetBrains Qodana linters for comprehensive multi-language code analysis.

## When to Use

Use this skill when you need to:
- Find code quality issues (unused code, redundant constructs, etc.)
- Detect potential bugs and problematic code patterns
- Check for JetBrains IDE inspections (IntelliJ IDEA, PyCharm, WebStorm, etc.)
- Get a list of issues to fix in the codebase
- Analyze code changes after modifications
- Perform language-specific static analysis across your tech stack

## How to Use

### Basic Usage

Run full project inspection (specify the appropriate linter for your project):

```bash
# Java/Kotlin project
bash .claude/skills/qodana-inspect/scripts/run-qodana.sh --linter qodana-jvm-community

# Python project
bash .claude/skills/qodana-inspect/scripts/run-qodana.sh --linter qodana-python-community

# TypeScript/JavaScript project
bash .claude/skills/qodana-inspect/scripts/run-qodana.sh --linter qodana-js
```

### Incremental Analysis

Analyze only changes since a specific commit:

```bash
bash .claude/skills/qodana-inspect/scripts/run-qodana.sh --linter <linter-name> --diff-start <commit-hash>
```

### Help

View all available linters and options:

```bash
bash .claude/skills/qodana-inspect/scripts/run-qodana.sh --help
```

## Platform Fixes (Automatic)

The skill includes automatic platform-specific fixes for known Qodana issues. These fixes are applied automatically before analysis based on the selected linter.

### PyCharm/Python Platform Fix

**Issue:** Qodana native mode for Python may fail to create `jdk.table.xml`, causing it to not recognize installed libraries from virtual environments (bug QD-11375).

**Automatic Fix:** When using `qodana-python` or `qodana-python-community` linters, the skill:
1. Detects if `jdk.table.xml` is missing in Qodana's config directory
2. Extracts Python SDK configuration from `.idea/misc.xml`
3. Automatically generates `jdk.table.xml` with proper paths to:
   - Virtual environment site-packages
   - Python standard library
   - Python DLLs

**Result:** Eliminates false positives like:
- `PyTypeHintsInspection` errors on valid PEP 604 union types (`dict | None`)
- `PyClassHasNoInitInspection` errors on `@dataclass` classes
- Import resolution errors for installed packages

This fix is transparent and requires no user configuration. If the project has `.idea/misc.xml` with a configured Python SDK, the fix applies automatically.

### Future Platform Fixes

The architecture supports adding fixes for other platforms:
- IntelliJ IDEA (JVM projects)
- WebStorm (JavaScript/TypeScript)
- Rider (.NET projects)

## Output Format

The script returns results grouped by file:

```
=== FILE: src/main/kotlin/example/Example.kt ===

[HIGH] UnusedSymbol
Location: line 45, column 13
Message: Variable 'unusedVar' is never used
Code:
val unusedVar = "test"

---

[MODERATE] NamingConvention
Location: line 52, column 9
Message: Property name should follow naming convention
Code:
private val MyProperty = "value"

=== FILE: src/main/kotlin/example/Another.kt ===
...
```

## Severity Levels

- **HIGH**: Important issues (unused code, potential bugs, API problems)
- **MODERATE**: Style and convention issues
- **INFO**: Informational notices

## Available Linters

### JVM Ecosystem
- **qodana-jvm-community** - Java, Kotlin, Groovy (Community, free)
- **qodana-jvm** - Java, Kotlin, Groovy (Ultimate, paid)
- **qodana-jvm-android** - Android development (Community, free)
- **qodana-android** - Android development (Ultimate, paid)

### Web Development
- **qodana-js** - JavaScript, TypeScript (Ultimate, paid)
- **qodana-php** - PHP, JavaScript, TypeScript (Ultimate, paid)

### .NET & C/C++
- **qodana-cdnet** - C#, VB.NET (Community, free)
- **qodana-dotnet** - C#, VB.NET, C, C++ (Ultimate, paid)
- **qodana-clang** - C, C++ (Community, free)
- **qodana-cpp** - C, C++ (Ultimate, paid)

### Other Languages
- **qodana-python-community** - Python (Community, free)
- **qodana-python** - Python (Ultimate, paid)
- **qodana-go** - Go (Ultimate, paid)
- **qodana-ruby** - Ruby (Ultimate, paid)

## Technical Details

- **Mode**: Native (no Docker required, uses `--within-docker=false`)
- **Output**: Parsed SARIF JSON format
- **Results location**:
  - Windows: `~/AppData/Local/JetBrains/Qodana/*/results/`
  - macOS: `~/Library/Caches/JetBrains/Qodana/*/results/`
  - Linux: `~/.cache/JetBrains/Qodana/*/results/`

## Requirements

- Qodana CLI must be installed (`qodana` command available)
- `jq` must be installed for JSON parsing
- Appropriate linter must be specified for the project's programming language

## Notes

- Full scan typically takes 30 seconds to several minutes depending on project size
- Incremental scan with `--diff-start` takes longer (analyzes two project states)
- Results include exact line/column numbers and code snippets for context
- Script filters out Qodana progress messages, showing only final results
- Cross-platform support: Windows, macOS, Linux

## Limitations

- Quick-Fix auto-correction is not available in Community Edition linters
- You must manually fix identified issues using Edit tool
- Use code context and snippets provided in output to understand and fix problems
- Ultimate linters (qodana-jvm, qodana-js, qodana-python, etc.) require a license
