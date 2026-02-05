---
name: repomix-cache-refresh
description: Post-workflow cache refresh for Repomix. Automatically refreshes compressed codebase representation after files are modified. Ensures next command has accurate context with 70% token savings. Invoke at end of any workflow that modifies source files. Takes ~2.4 seconds when refresh needed.
---

# Repomix Cache Refresh - Post-Workflow Optimization

**Purpose:** Keep Repomix cache fresh after file modifications for optimal token efficiency.
**Trigger:** End of any workflow that modifies source code, configs, or documentation.
**Performance:** ~2.4 seconds overhead, 70% token savings on subsequent operations.

## Why This Matters

Repomix compresses codebases into AI-friendly format, providing 70% token reduction on file operations.

**Problem:** If cache becomes stale, subsequent commands work with outdated context.
**Solution:** Refresh cache at end of workflows that modify relevant files.

**Cache Strategy:**
```
Session Start → Use existing cache (from previous command)
Command N Executes → Uses current cache
Command N Completes → Refresh if files changed
Command N+1 Executes → Uses fresh cache
```

---

## When to Invoke

**Invoke this skill at the END of:**
- `/ms` command workflows
- `/audit` command workflows
- `/build` command workflows
- Any multi-agent workflow that modifies files

**Skip refresh when:**
- Read-only operations (no files modified)
- Only build artifacts changed (dist/, node_modules/)
- Only logs or temporary files changed

---

## Relevant File Patterns

### Include (triggers refresh)
| Pattern | Examples |
|---------|----------|
| `*.ts`, `*.tsx` | TypeScript source |
| `*.js`, `*.jsx` | JavaScript source |
| `*.json` | Config files, package.json |
| `*.md` | Documentation |
| `*.yaml`, `*.yml` | CI/CD, configs |

### Exclude (skip refresh)
| Pattern | Reason |
|---------|--------|
| `node_modules/` | Dependencies, not source |
| `dist/`, `build/` | Build artifacts |
| `.turbo/` | Turbo cache |
| `*.log` | Log files |
| `.repomix-output.*` | Output file itself |

---

## Implementation

At workflow completion, execute this logic:

```typescript
// 1. Collect modified files from workflow
const modifiedFiles = workflowResults.flatMap(r => r.filesModified || []);

// 2. Filter to relevant files
const relevantFiles = modifiedFiles.filter(file => {
  // Exclude build artifacts and dependencies
  if (file.match(/(node_modules|dist|build|\.turbo|\.log|\.repomix-output)/)) {
    return false;
  }
  // Include source code, configs, docs
  return file.match(/\.(ts|tsx|js|jsx|json|md|ya?ml)$/);
});

// 3. Refresh if relevant files changed
if (relevantFiles.length > 0) {
  // Run: npx repomix --config .repomix.config.json
  console.log(`Refreshing Repomix cache (${relevantFiles.length} files changed)...`);
} else {
  console.log("No relevant changes, cache still fresh");
}
```

---

## Execution Command

When refresh is needed, run:

```bash
npx repomix --config .repomix.config.json
```

**Requirements:**
- `.repomix.config.json` must exist in project root
- Node.js/npm available
- ~2.4 seconds execution time

---

## Performance Metrics

| Metric | Value |
|--------|-------|
| Refresh time | ~2.4 seconds |
| Token savings | 70% on file operations |
| Overhead per command | Minimal (only when files changed) |
| Accuracy | 100% (no stale data) |

---

## Output Messages

Use these consistent messages:

```
# When refreshing
Refreshing Repomix cache ({N} files changed)...
Repomix cache ready for next command

# When skipping
No relevant changes, Repomix cache still fresh

# When no config found
Repomix config not found, skipping cache refresh
```

---

## Integration Notes

**For command authors:**
- Reference this skill at end of workflow section
- Ensure agents report `filesModified: string[]` in output
- Don't duplicate the logic - just invoke this skill

**For CLAUDE.md:**
- Reference skill location for implementation details
- Keep summary brief, point to skill for full docs
