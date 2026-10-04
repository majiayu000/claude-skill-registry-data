---
name: impact-analysis
description: This skill should be used before any non-trivial code modification to assess the blast radius and risk of the change. Trigger when the user discusses renaming, refactoring, deleting, moving, restructuring, or modifying code. Also trigger when the user asks "what would break if...", "is X safe to remove", or wants to estimate risk before a refactor.
---

# Impact Analysis

Use the `code_intel` tool to assess the impact of proposed code changes before they happen, identifying affected files, dependents, public API exposure, and risk level.

## When to Run

Run an impact analysis when **any** of the following apply:

- About to rename, move, delete, or significantly modify a code symbol
- About to change a function signature, class shape, or exported interface
- Considering removing code suspected to be dead
- Planning a multi-file refactor and need a safe order
- User asks "what uses X?", "what would break?", "is X safe to remove?"

If the change is purely additive (new file, new function, no signature changes to existing exports), impact analysis is usually unnecessary — skip it.

## How to Run

Call the `code_intel` tool with this code:

```javascript
const result = await api.impactAnalysis({
	symbolName: "TargetSymbol",
	filePath: "src/path/to/file.ts", // optional, helps disambiguate
	depth: 3
});
return result;
```

For broader context (large refactors, whole-file changes), pair with dependency mapping:

```javascript
const [impact, deps, dependents] = await Promise.all([
	api.impactAnalysis({ symbolName, filePath, depth: 3 }),
	api.getDependencies({ filePath, depth: 2 }),
	api.getDependents({ filePath, depth: 2 }),
]);
return { impact, deps, dependents };
```

For confirming dead code:

```javascript
const usage = await api.traceSymbolUsage({ symbolName, filePath });
return usage;
```

## Interpreting Results

The `impactAnalysis` response includes a `data.breakingChangeRisk.riskLevel` field (`low` | `medium` | `high` | `critical`). Use this as the headline risk indicator. Cross-reference with:

| Signal | Where to find it | What it tells you |
|--------|------------------|-------------------|
| Affected file count | `data.summary.impactedFileCount` | Blast radius |
| Public API exposure | `data.symbol.isExported` | External consumers may break |
| Test exposure | `data.summary.testFileCount` vs `data.summary.productionFileCount` | Confidence in catching regressions |
| Direct dependents | `data.directDependents[]` | Where to look first |
| Risk factors | `data.breakingChangeRisk.factors[]` | Why the risk level is what it is |
| Recommendations | `data.breakingChangeRisk.recommendations[]` | Suggested mitigation steps |

**Risk thresholds (rule of thumb):**

- **Low**: < 5 files affected, internal-only, tests among the dependents → proceed normally
- **Medium**: 5–15 files affected, or some public surface → review dependents before changing
- **High**: > 15 files affected, exported API, or no impacted test files → stage the change, add tests first
- **Critical**: Core infrastructure, security-adjacent, or hub modules → pause, propose a migration plan

## Reporting Format

When presenting results to the user, structure as:

1. **Symbol** — name, kind, location
2. **Risk** — level + one-sentence rationale
3. **Scope** — `N files, M symbols affected; public API: yes/no`
4. **Top dependents** — first 5–10 from `directDependents`
5. **Test exposure** — impacted test files vs production files from `data.summary`
6. **Recommendation** — concrete next step (proceed / review listed files / stage in N steps / add tests first)

For high or critical risk, lead with the warning and offer to suggest a safer change order.

## Fallbacks

If the `code_intel` call fails:

| Failure | Fallback |
|---------|----------|
| MCP unavailable | Use Grep to find textual usages of the symbol; warn the result is incomplete (misses indirect/dynamic refs) |
| `AUTH_ERROR`, `PROJECT_NOT_INDEXED` | Note the error briefly, suggest `/constellation:diagnose`, then fall back to Grep |
| `SYMBOL_NOT_FOUND` | Symbol may be renamed/deleted/misspelled. Try a broader `searchSymbols` or confirm the file path |

A partial Grep-based assessment is always better than skipping the analysis.

## Related

- `/constellation:impact <symbol> [file]` — one-shot slash command equivalent
- `/constellation:deps <file>` — dependency-only view
- `/constellation:unused` — proactive dead-code scan
