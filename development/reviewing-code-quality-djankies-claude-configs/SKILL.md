---
name: reviewing-code-quality
description: Automated tooling and detection patterns for JavaScript/TypeScript code quality review
---

# Code Quality Review Skill

## Purpose

This skill provides automated analysis commands and detection patterns for code quality issues. Use this as a reference for WHAT to check and HOW to detect issues—not for output formatting or workflow.

## Automated Analysis Tools

Run these scripts to gather metrics (if tools available):

### Linting Analysis

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-lint.sh
```
````

**Returns:** Error count, violations with file:line, auto-fix suggestions

### Type Safety Analysis

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-types.sh
```

**Returns:** Type errors, missing annotations, error locations

### Unused Code Detection

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-unused-code.sh
```

**Returns:** Unused exports, unused dependencies, dead code

### TODO/FIXME Comments

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-todos.sh
```

**Returns:** Comment count by type, locations with context

### Debug Statements

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-debug-statements.sh
```

**Returns:** console.log/debugger statements with locations

### Large Files

```bash
bash ~/.claude/plugins/marketplaces/claude-configs/review/scripts/review-large-files.sh
```

**Returns:** Files >500 lines sorted by size

## Manual Detection Patterns

When automated tools unavailable or for deeper analysis, use Read/Grep/Glob to detect:

### Code Smells to Detect

**Long Functions:**

```bash
# Find functions with >50 lines
grep -n "function\|const.*=.*=>.*{" <file> | while read line; do
  # Count lines until closing brace
done
```

Look for: Functions spanning >50 lines, multiple responsibilities

**Deep Nesting:**

```bash
# Find lines with >3 levels of indentation
grep -E "^[[:space:]]{12,}" <file>
```

Look for: Nesting depth >3, complex conditionals

**Missing Error Handling:**

```bash
grep -n "async\|await\|Promise\|\.then\|\.catch" <file>
```

Look for: Async operations without try-catch or .catch()

**Poor Type Safety:**

```bash
grep -n "any\|as any\|@ts-ignore\|@ts-expect-error" <file>
```

Look for: Type assertions, any usage, suppression comments

**Repeated Patterns:**
Use Read to identify duplicate logic blocks (>5 lines similar code)

**Poor Naming:**
Look for: Single-letter variables (except i, j in loops), unclear abbreviations, misleading names

## Severity Mapping

Use these criteria when classifying findings:

| Pattern                                  | Severity | Rationale               |
| ---------------------------------------- | -------- | ----------------------- |
| Type errors blocking compilation         | critical | Prevents deployment     |
| Missing error handling in critical paths | high     | Production crashes      |
| Unused exports in public API             | high     | Breaking changes needed |
| Large files (>500 LOC)                   | medium   | Maintainability impact  |
| TODO comments                            | medium   | Incomplete work         |
| Debug statements (console.log)           | medium   | Production noise        |
| Deep nesting (>3 levels)                 | medium   | Complexity issues       |
| Long functions (>50 lines)               | medium   | Readability issues      |
| Linting warnings                         | nitpick  | Style consistency       |
| Minor naming issues                      | nitpick  | Clarity improvements    |

## Analysis Priority

1. **Run automated scripts first** (if tools available)
2. **Parse script outputs** for file:line references
3. **Read flagged files** using Read tool
4. **Apply manual detection patterns** to flagged files
5. **Cross-reference findings** (e.g., large file + many TODOs = higher priority)

## Integration Notes

- This skill provides detection methods only
- Output formatting is handled by the calling agent
- Severity classification should align with agent's schema
- Do NOT include effort estimates or workflow instructions

## Related Skills

**Cross-Plugin References:**

- If reviewing Zod schema patterns, use the reviewing-patterns skill for detecting validation issues and schema anti-patterns
- Uses skills tagged with `review: true` including reviewing-vitest-config from vitest-4 for detecting deprecated patterns and Vitest 4.x migration issues
