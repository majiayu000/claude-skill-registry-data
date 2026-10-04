---
name: techdebt
description: Scan codebase for technical debt — duplicated code, dead exports, unused dependencies, TODO/FIXME comments, and oversized files. Run periodically or at session end.
disable-model-invocation: false
context: fork
allowed-tools: Read Grep Glob Bash
---

# Technical Debt Scanner

Perform a quick techdebt scan of the codebase. Report findings concisely — one line per issue found.

> **Continuous mode:** run this under `/loop` (e.g. `/loop 1d /techdebt`) to scan on an interval, or pair it with a `/goal` to keep chipping away — "the techdebt report has no findings above <threshold>" — until the backlog clears.

## Checks to Run

### 1. Large Files (>500 lines)
Find Vue components, TypeScript files, and composables exceeding 500 lines. These are candidates for extraction.

```bash
find app/ shared/ server/ -name '*.vue' -o -name '*.ts' | xargs wc -l | awk '$1 > 500 {print}' | sort -rn
```

### 2. TODO/FIXME/HACK Comments
Surface unresolved technical debt markers.

```bash
grep -rn 'TODO\|FIXME\|HACK\|XXX\|TEMP' app/ shared/ server/ --include='*.vue' --include='*.ts' --include='*.js'
```

### 3. Duplicated Code Patterns
Look for suspiciously similar blocks across files. Focus on:
- Identical fetch/API call patterns that should be composables
- Repeated template patterns that should be components
- Copy-pasted utility functions

Use Grep to search for repeated patterns (3+ occurrences of same multi-line block).

### 4. Unused Exports
Check for exported functions/types that have no imports elsewhere in the codebase. Focus on `shared/` and `app/composables/`.

For each export found, grep the codebase for its usage. If only the defining file references it, flag it.

### 5. Unused Dependencies
Compare `package.json` dependencies against actual imports in the codebase.

```bash
# List dependencies from package.json, then check each for usage
bun pm ls 2>/dev/null | head -50
```

For each dependency, search for `import ... from 'package-name'` or `require('package-name')`. Flag any with zero references.

## Output Format

```
## Techdebt Report

### Large Files
- `app/components/MovieCard.vue` — 623 lines (consider extraction)

### Unresolved TODOs
- `app/composables/useRankings.ts:45` — TODO: handle pagination edge case

### Duplicated Patterns
- API error handling pattern repeated in 4 composables — extract to shared utility

### Unused Exports
- `shared/utils/format.ts:export formatDuration` — no imports found

### Unused Dependencies
- `lodash-es` — no imports found in codebase

### Summary
Found X issues across Y categories.
```

If nothing notable is found, respond: "Techdebt scan clean — no issues found."
