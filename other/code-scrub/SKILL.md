---
name: code-scrub
description: Methodology and rules for scrubbing codebases — removing dead code, weak types, duplication, bad comments, defensive programming, and legacy cruft.
compatibility:
  - opencode
  - cursor
  - claude
metadata:
  audience: agents
  purpose: skill-routing
---
# Code Scrub Methodology

## Core principle

Scrubbing improves code quality by **removing waste** — not by adding abstractions. Every change must make the code simpler, not more complex. If a fix introduces more indirection than it removes duplication, don't make it.

## Confidence levels

Categorize every finding:

| Level | Criteria | Action |
|---|---|---|
| **High** | Clearly unused, clearly duplicated, clearly wrong type, clearly misleading comment. Removal/fix has no behavioral change. | Implement immediately |
| **Medium** | Likely an improvement but requires judgment — could affect behavior, might break an edge case, or the "right" fix is debatable. | Document as recommendation, don't implement |
| **Low** | Stylistic, cosmetic, or would require significant restructuring. | Mention in assessment only |

## Rules for each concern

### Deduplication (DRY)
- Only consolidate when the duplicated code is **genuinely the same concern**, not just similar-looking code that happens to share structure
- Don't extract utilities for code that's duplicated only twice — wait for three or more
- Don't create "god util" packages. Place shared code in the package that owns the concept
- If consolidation requires adding parameters or flags to handle variant behavior, it's probably not worth it

### Type strengthening
- `any`/`interface{}` is legitimate for: JSON marshaling, database/sql args, generic containers, protocol boundaries (MCP, GraphQL)
- Replace with concrete types when: the value is always used as one type, or the set of types is small and known
- Don't create wrapper types just to avoid `any` — the cure shouldn't be worse than the disease
- Check that replacement types are actually correct by tracing usage upstream and downstream

### Dead code removal
- Verify with static analysis tools first (`deadcode`, `knip`, tree-shaking analysis)
- Grep for all references before removing exported symbols
- Watch for: reflection, embed directives, interface implementations, build tags, test helpers
- If uncertain, leave it and document

### Dependency structure
- Go: no circular imports possible, focus on coupling and cohesion
- TypeScript/JS: use tools like `madge` to detect cycles
- Don't restructure working dependency graphs for cosmetic reasons
- A "god package" that wires things together (CLI layer, main, app bootstrap) is architecturally correct

### Defensive programming
- Keep error handling for: user input, network I/O, file I/O, external APIs, deserialization
- Remove error handling that: swallows errors silently, returns fallback values that mask bugs, catches panics without logging
- `_ = expr` is fine for: log writes, cache writes, cleanup operations, non-critical side effects
- `_ = expr` is not fine for: data writes the user expects to persist, operations where failure means silent data loss

### Legacy and fallback code
- Backward compatibility for **user-facing config** is legitimate — don't remove it without a migration path
- Backward compatibility for **internal data formats** should be removed if no deployments use the old format
- Comments saying "deprecated" or "legacy" don't automatically mean the code should be removed — check if it's still needed
- Feature flags and conditional paths that only have one active branch should be simplified

### Comments
- Remove: narrating comments ("increment counter"), section dividers that add nothing, AI boilerplate, work-in-progress references
- Keep: comments explaining **why** (not what), non-obvious algorithm explanations, links to specs/tickets, license headers, godoc/JSDoc for public APIs
- Replace (don't just remove): misleading comments that describe behavior the code doesn't have

## Language-specific tools

| Language | Dead code | Dependencies | Types |
|---|---|---|---|
| Go | `deadcode`, `go vet`, manual grep | `go list -json`, import analysis | grep for `any`/`interface{}` |
| TypeScript | `knip`, `ts-prune` | `madge`, `dependency-cruiser` | grep for `any`, `unknown`, `as any` |
| Python | `vulture`, `pylint` | `pydeps`, `import-linter` | grep for `Any`, `# type: ignore` |
| Java | IntelliJ inspections, `spotbugs` | `jdepend`, gradle dependencies | grep for `Object`, raw types |
| Rust | `cargo clippy`, dead_code warnings | `cargo tree` | rare — compiler enforces |

## Verification

After every change:
1. Build must pass
2. Tests must pass
3. No new warnings introduced

If build or tests fail after a change, **revert and document** — don't fix forward during a scrub.
