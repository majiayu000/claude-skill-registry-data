---
name: formatter-linter-expert
description: Universal code formatter and linter analyzer for multi-ecosystem projects (Laravel/PHP, Bun/Node/TS/JS, React, Vue, Astro, Nuxt, Go, Rust, Deno) with intelligent asdf version management, auto-detection, and interactive workflows
version: 1.0.0
dependencies:
  - python >= 3.9
  - asdf (optional but recommended)
allowed-tools: ["Bash", "Read", "Write", "Glob", "Grep"]
---

# Formatter & Linter Expert Analyzer

## Overview

A comprehensive, intelligent meta-formatter and linter system that automatically detects your project's ecosystem, respects asdf version management, and provides flexible formatting/linting workflows across 9+ development environments.

**When to use this skill:**
- "Analyze and format this Laravel project"
- "Lint my TypeScript code"
- "Check code style of this Go file"
- "Format all PHP files with Pint"
- "Quality report for this codebase"
- "Run formatter on src/ directory"
- "Interactive code cleanup"

**What it does:**
1. **Detects ecosystem** automatically (Laravel, Bun/Node, Go, Rust, Deno, etc.)
2. **Integrates with asdf** to use project-specific tool versions from `.tool-versions`
3. **Finds configurations** (auto-detect or use custom configs)
4. **Analyzes OR formats** code based on your choice
5. **Generates comprehensive reports** (Markdown + JSON export)
6. **Interactive mode** for file-by-file review and approval

## Supported Ecosystems

| Ecosystem | Formatter | Linter | Config Files |
|-----------|-----------|--------|--------------|
| **Laravel/PHP** | Laravel Pint, PHP-CS-Fixer | PHPStan | `pint.json`, `.php-cs-fixer.php`, `phpstan.neon` |
| **Bun/Node/TS/JS** | Prettier, Biome | ESLint, Biome | `.prettierrc`, `biome.json`, `.eslintrc*` |
| **React/Vue/Astro/Nuxt** | Prettier, Biome | ESLint + framework plugins | Framework-specific configs |
| **Go** | gofmt, goimports | golangci-lint | `.golangci.yml` |
| **Rust** | rustfmt | clippy | `rustfmt.toml`, `clippy.toml` |
| **Deno** | deno fmt | deno lint | `deno.json`, `deno.jsonc` |

## Prerequisites

**Required:**
- Python 3.9+ (for skill scripts)
- Ecosystem-specific tools installed (see below)

**Optional but Recommended:**
- asdf version manager ([installation guide](https://asdf-vm.com/guide/getting-started.html))
- `.tool-versions` file in your project root

**Ecosystem-specific tools:**
- **PHP**: `composer global require laravel/pint`, `composer global require friendsofphp/php-cs-fixer`
- **JavaScript/TypeScript**: `npm install -g prettier eslint @biomejs/biome` or `bun add -g prettier eslint @biomejs/biome`
- **Go**: `go install golang.org/x/tools/cmd/goimports@latest`, `go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest`
- **Rust**: rustfmt and clippy (included with `rustup`)
- **Deno**: deno cli (includes fmt and lint)

## Instructions

### Step 1: Invoke the Skill

Activate the skill naturally:
```
"Analyze this Laravel project"
"Format all TypeScript files"
"Lint and report on src/ directory"
"Interactive format for Go code"
```

### Step 2: Environment Detection

The skill will automatically:

1. **Search for `.tool-versions`** (asdf integration)
   ```bash
   # Reads versions from current dir up to $HOME
   php 8.2.0
   nodejs 20.10.0
   golang 1.21.0
   ```

2. **Detect ecosystem** via file markers:
   - `composer.json` + `artisan` → Laravel
   - `package.json` + `bun.lockb` → Bun/*
   - `go.mod` → Go
   - `Cargo.toml` → Rust
   - `deno.json` → Deno

3. **Find framework** (if JavaScript/TypeScript):
   - Check `package.json` dependencies for react, vue, astro, nuxt

4. **Locate configurations**:
   - Auto-detect: `pint.json`, `.eslintrc`, `.prettierrc`, etc.
   - Custom: User can provide path
   - Fallback: Use skill's default configs

### Step 3: Choose Operation Mode

**Mode A: Analyze Only** (default if ambiguous)
```
Generate comprehensive report WITHOUT modifying files
→ Ideal for CI/CD, code review, initial assessment
```

**Mode B: Format** (apply fixes directly)
```
Auto-fix all formatting issues
→ Fast, non-interactive, writes changes
```

**Mode C: Interactive**
```
Review and approve changes file-by-file
→ Safe, controlled, educational
```

### Step 4: Execute Analysis/Formatting

The skill orchestrates:

```python
# Pseudo-workflow
python scripts/main.py \
  --mode analyze \
  --scope project \
  --asdf-strict \
  --output markdown \
  --export-json report.json
```

**Behind the scenes:**
1. **Environment detection** runs first
2. **Version validation** checks asdf versions match
3. **Config resolution** finds or uses defaults
4. **Formatter/Linter execution** runs ecosystem tools
5. **Report generation** creates output

### Step 5: Review Output

**Analyze mode output:**
```markdown
# Code Quality Report

**Project:** my-laravel-app
**Environment:** Laravel 12 (PHP 8.2.0)
**Date:** 2025-10-30 14:23:45

## Summary
- Files analyzed: 127
- Issues found: 42
  - 🔴 Errors: 5
  - 🟡 Warnings: 15
  - 🔵 Info: 22

## Issues by Category
[Detailed breakdown...]

## Configuration Used
- Formatter: Laravel Pint
- Config: pint.json (detected)
- PHP Version: 8.2.0 (asdf)

## Recommendations
[Actionable next steps...]
```

**Interactive mode prompt:**
```
File: src/Controllers/UserController.php
Issues: 5 formatting, 2 linting

Preview of changes:
[diff display]

Apply fixes to this file? [y/n/s(kip)/q(uit)]: _
```

### Step 6: Handle Multiple Ecosystems

If **multiple ecosystems** detected (e.g., Laravel backend + Vue frontend):

```
🔍 Detected multiple ecosystems:
  1. Laravel/PHP (app/, routes/, database/)
  2. Vue.js (resources/js/)

→ Formatting BOTH ecosystems...

[Run PHP formatters on PHP files]
[Run JS formatters on JS/Vue files]
```

## Error Handling

### Common Issues

| Error | Cause | Solution |
|-------|-------|----------|
| `Tool not found: pint` | Formatter not installed | Install via `composer global require laravel/pint` |
| `asdf version mismatch` | `.tool-versions` version not installed | Run `asdf install` |
| `No ecosystem detected` | No recognizable file markers | Use `--env` flag to specify manually |
| `Config parsing failed` | Invalid configuration file | Check config syntax or use `--use-defaults` |
| `Permission denied` | Cannot write formatted files | Check file permissions or run as appropriate user |

### asdf Integration Modes

**Strict mode** (default):
```bash
# Uses ONLY asdf versions, fails if not installed
--asdf-strict
```

**Fallback mode**:
```bash
# Tries asdf, falls back to system PATH if unavailable
--asdf-fallback
```

**Report mode**:
```bash
# Warns about version mismatch but continues
--asdf-warn
```

## Examples

### Example 1: Analyze Laravel Project

**Input:**
```
User: "Analyze and generate quality report for this Laravel API"
```

**Execution:**
```bash
# Skill detects:
# - Laravel 12 (composer.json + artisan)
# - PHP 8.2.0 from .tool-versions
# - Existing pint.json config

# Runs:
vendor/bin/pint --test --config pint.json
vendor/bin/phpstan analyze --level 5

# Outputs:
# report.md (detailed analysis)
# report.json (structured data)
```

**Expected Output:**
Markdown report + JSON file showing 127 files analyzed, 42 issues categorized by severity.

---

### Example 2: Format TypeScript with Biome

**Input:**
```
User: "Format all TypeScript files using Biome"
```

**Execution:**
```bash
# Skill detects:
# - TypeScript project (package.json with typescript dep)
# - Node 20.10.0 from .tool-versions
# - biome.json config present

# Runs:
biome format --write src/

# Outputs:
# Console: "✅ Formatted 45 files"
```

---

### Example 3: Interactive Go Formatting

**Input:**
```
User: "Interactive format for Go files in cmd/ directory"
```

**Execution:**
```bash
# Skill detects:
# - Go project (go.mod)
# - Go 1.21.0 from .tool-versions
# - No config (uses defaults)

# Runs interactively:
# For each .go file:
#   - Shows gofmt diff
#   - Prompts: Apply? [y/n/s/q]
#   - Applies only if 'y'
```

**Interactive Flow:**
```
File: cmd/server/main.go (3 formatting issues)

--- Original
+++ Formatted
@@ -15,7 +15,7 @@
-func main(){
+func main() {

Apply fixes? [y/n/s/q]: y
✅ Applied

File: cmd/worker/worker.go (1 issue)
[...]
```

---

### Example 4: Multi-Ecosystem Project (Laravel + Vue)

**Input:**
```
User: "Full project format - both backend and frontend"
```

**Execution:**
```bash
# Skill detects:
# - Laravel (composer.json)
# - Vue.js (package.json with vue dependency)
# - PHP 8.2.0 + Node 20.10.0 from .tool-versions

# Runs sequentially:
# 1. PHP formatting (Pint on app/, routes/, database/)
# 2. Vue formatting (Prettier on resources/js/)

# Outputs:
# Combined report for both ecosystems
```

**Output:**
```markdown
# Multi-Ecosystem Report

## PHP (Laravel)
- Files: 87
- Fixed: 12 formatting issues

## JavaScript (Vue)
- Files: 40
- Fixed: 8 formatting issues

Total: 127 files processed, 20 issues fixed
```

## Advanced Usage

### Custom Configuration Path

```
User: "Format with custom config at configs/my-pint.json"
```

Skill will use `--config configs/my-pint.json` flag.

### Specific File/Directory Scope

```
User: "Lint only the app/Services/ directory"
```

Skill scopes analysis to that path only.

### Export JSON for CI/CD

```
User: "Generate JSON report for pipeline"
```

Outputs `report.json`:
```json
{
  "project": "my-app",
  "timestamp": "2025-10-30T14:23:45Z",
  "environment": {
    "ecosystem": "laravel",
    "php_version": "8.2.0",
    "tools": ["pint", "phpstan"]
  },
  "summary": {
    "files_analyzed": 127,
    "issues": {
      "errors": 5,
      "warnings": 15,
      "info": 22
    }
  },
  "issues": [
    {
      "file": "app/Http/Controllers/UserController.php",
      "line": 45,
      "severity": "error",
      "message": "Indentation incorrect",
      "rule": "PSR-12"
    }
  ],
  "exit_code": 1
}
```

## Best Practices

### ✅ Do This

1. **Use asdf** for version consistency across team
2. **Commit configs** (`.prettierrc`, `pint.json`) to version control
3. **Run analyze first** before formatting to understand impact
4. **Use interactive mode** when learning or unsure about changes
5. **Export JSON** for integration with CI/CD pipelines
6. **Check exit codes** in scripts (0 = clean, >0 = issues found)

### ⚠️ Avoid This

1. **Don't skip analyze** - Always review before mass formatting
2. **Don't ignore version mismatches** - Formatting can vary between tool versions
3. **Don't mix formatters** - Pick one (Prettier vs Biome) and stick with it
4. **Don't format generated code** - Exclude `vendor/`, `node_modules/`, `dist/`
5. **Don't commit without testing** - Run tests after formatting

## Troubleshooting

### Issue: "No ecosystem detected"

**Cause:** Project lacks recognizable file markers

**Fix:**
```bash
# Manual specification
User: "Format this PHP project using Pint"
# Or create marker file
touch composer.json  # for PHP projects
```

---

### Issue: "asdf: command not found"

**Cause:** asdf not installed or not in PATH

**Fix:**
```bash
# Install asdf
git clone https://github.com/asdf-vm/asdf.git ~/.asdf --branch v0.14.0

# Add to shell
echo '. "$HOME/.asdf/asdf.sh"' >> ~/.bashrc
source ~/.bashrc

# Or use fallback mode
User: "Format with system tools (ignore asdf)"
```

---

### Issue: "Version mismatch: PHP 8.2.0 not installed"

**Cause:** `.tool-versions` specifies version not installed via asdf

**Fix:**
```bash
# Install missing version
asdf plugin add php
asdf install php 8.2.0

# Or use fallback mode to use system PHP
```

---

### Issue: "Config parsing error: Invalid JSON in biome.json"

**Cause:** Malformed configuration file

**Fix:**
```bash
# Validate JSON
cat biome.json | jq .

# Or use default config
User: "Format using default Biome config"
```

## Technical Details

### Architecture

```
User Request
    ↓
Environment Detector
    ├─ asdf Manager (version resolution)
    ├─ Config Finder (locate configs)
    └─ File Analyzer (detect ecosystem)
    ↓
Orchestrator
    ├─ PHP Formatter/Linter
    ├─ JS Formatter/Linter
    ├─ Go Formatter/Linter
    ├─ Rust Formatter/Linter
    └─ Deno Formatter/Linter
    ↓
Reporter
    ├─ Markdown Report
    ├─ JSON Export
    └─ Console Output
```

### Token Efficiency

- **Metadata load**: ~500 tokens (always loaded in context)
- **Full instructions** (this file): ~3,500 tokens (loaded on activation)
- **Script execution**: 0 tokens (Python runs externally, only output returned)
- **Total skill overhead**: ~4,000 tokens

### Performance Considerations

- **Small projects** (<100 files): ~5-10 seconds
- **Medium projects** (100-500 files): ~30-60 seconds
- **Large projects** (>500 files): 1-3 minutes

**Optimization tips:**
- Use `--scope` to limit analysis to specific directories
- Exclude large directories with `--exclude node_modules,vendor`
- Run formatters in parallel for multi-ecosystem projects

### Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success - no issues found |
| 1 | Formatting issues found (fixable) |
| 2 | Linting warnings found |
| 3 | Linting errors found (requires manual fix) |
| 10 | Tool not found / not installed |
| 11 | asdf version mismatch |
| 12 | Configuration error |
| 99 | Unknown error |

## Related Skills

*No related skills detected in current environment*

## Maintenance

**Version History:**
- v1.0.0 (2025-10-30) - Initial release with 9 ecosystem support

**Roadmap:**
- [ ] Add Python support (black, ruff)
- [ ] Add Swift support (swift-format)
- [ ] Add Kotlin support (ktlint)
- [ ] GitHub Actions integration
- [ ] VS Code extension

**Known Limitations:**
- Requires tools to be pre-installed (doesn't auto-install)
- asdf integration tested on Unix-like systems only
- Interactive mode not suitable for CI/CD pipelines

**Author:** Created for personal cross-project use
**Created:** 2025-10-30
**License:** Personal use

---

## Quick Command Reference

```bash
# Analyze only (default)
"Analyze this project"

# Format directly
"Format all files"

# Interactive review
"Interactive format"

# Specific scope
"Lint the src/ directory"
"Format app/Services/PaymentService.php"

# Custom config
"Format using my custom Pint config at config/pint.json"

# Export report
"Generate quality report with JSON export"

# Multi-ecosystem
"Format both PHP and Vue code"

# Ignore asdf
"Format using system tools"
```

---

**Need Help?**
- Check tool installation: `which pint`, `which prettier`, etc.
- Verify asdf setup: `asdf current`
- Review config files: `cat pint.json`, `cat .eslintrc`
- Test manually: `vendor/bin/pint --test`, `prettier --check src/`
