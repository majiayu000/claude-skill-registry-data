---
name: ubs-scanner
description: Bug scanning with UBS (Ultimate Bug Scanner). Use before commits, when scanning for bugs, when the user mentions "ubs", "bugs", "scan", or "code quality".
---

# UBS (Ultimate Bug Scanner)

Scans for 1000+ bug patterns across multiple languages.

## When This Applies

| Signal | Action |
|--------|--------|
| Before committing | `ubs --staged` |
| Scanning changes | `ubs --diff` |
| Scanning specific file | `ubs path/to/file` |
| CI integration | `ubs --ci` |

---

## Pre-Commit (Required)

**Run before every commit:**

```bash
ubs --staged                       # Scan staged changes
ubs --staged --fail-on-warning     # Strict mode (exit 1 on any issue)
```

**Fix all issues before committing. Rerun until clean.**

---

## Scanning Options

```bash
# Scan current directory
ubs .

# Scan specific file
ubs path/to/file.ts

# Scan working tree changes vs HEAD
ubs --diff

# Verbose with code examples
ubs -v .
```

---

## Profiles

```bash
# Strict (fail on warnings) - for production code
ubs --profile=strict .

# Loose (skip nits) - for prototyping
ubs --profile=loose .
```

---

## Language Filters

```bash
# Single language
ubs --only=python .

# Multiple languages
ubs --only=typescript,javascript .
```

**Supported languages:**
- javascript, typescript
- python
- c, c++
- rust, go
- java, ruby

---

## Output Formats

```bash
ubs . --format=json                # JSON
ubs . --format=jsonl               # Line-delimited JSON
ubs . --format=sarif               # GitHub Code Scanning
```

---

## CI Integration

```bash
ubs --ci                           # CI mode
ubs --comparison baseline.json .   # Regression detection
```

---

## Suppressing False Positives

Add to the line:
```javascript
// ubs:ignore
const result = eval(userInput); // ubs:ignore
```

---

## Health Check

```bash
ubs doctor
ubs doctor --fix
```

---

## Quick Reference

```bash
ubs --staged               # Pre-commit scan (required)
ubs --staged --fail-on-warning   # Strict pre-commit
ubs --diff                 # Working tree changes
ubs path/to/file           # Specific file
ubs --profile=strict .     # Production mode
ubs doctor --fix           # Health check
```

---

## Workflow Integration

The standard pre-commit workflow:

```bash
# 1. Run tests
npm test  # or pytest, etc.

# 2. Scan staged changes
ubs --staged

# 3. Fix any issues found
# 4. Re-run until clean
ubs --staged

# 5. Commit
git add -A && git commit
```

---

## Anti-Patterns

| Don't | Why |
|-------|-----|
| Skip `ubs --staged` | Bugs slip into commits |
| Ignore warnings | May be real issues |
| Over-suppress with `// ubs:ignore` | Defeats the purpose |

---

## See Also

- `verification/` — Full pre-commit checklist
- `bead-workflow/` — Bead close workflow includes UBS
