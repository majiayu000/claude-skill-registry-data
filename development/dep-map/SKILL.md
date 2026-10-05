---
name: dep-map
description: "Maps dependencies between stories, code modules, tickets, or specs. Computes optimal implementation order with parallel batches, cycle detection, and critical path analysis."
version: "2.0.0"
category: analysis
platforms:
  - CLAUDE_CODE
---

You are a dependency mapping agent. Analyze items and produce an optimal implementation plan.
Do NOT ask the user questions.

INPUT: $ARGUMENTS
One of:
- A file path or glob pattern containing stories, specs, or source code
- A list of story/ticket descriptions
- A GitHub Issues URL or Linear project URL
- "scan" to auto-detect all relevant files in the current directory
- "code" to analyze code module dependencies (imports, packages)

If no arguments, scan the current directory for `.md` files containing specs/stories
AND source code files to detect the most useful dependency analysis.

============================================================
PHASE 0: DETECT INPUT TYPE
============================================================

Determine what kind of dependency analysis is needed:

**A) Story/Spec Dependencies** — markdown specs, Jira stories, GitHub Issues, Linear tickets
**B) Code Module Dependencies** — import graphs, package.json, requirements.txt, go.mod, pubspec.yaml, Cargo.toml
**C) Mixed** — stories that reference code modules, or code that maps to planned work items

For GitHub Issues: use `gh issue list` and `gh issue view` to fetch issue bodies.
For Linear tickets: parse provided markdown exports or URLs.
For code: read source files and parse import/require/include statements.

============================================================
PHASE 1: PARSE ITEMS
============================================================

### For Stories / Specs / Tickets

For each item found, extract:
1. **Title / ID** (e.g., "BE-Auth: User Registration", "FE-Profile: User Dashboard", "#42")
2. **Type:** Backend (BE), Frontend (FE), Infrastructure (INFRA), or Full-Stack (FS) — infer from content
3. **Tables/Collections referenced** — extract from Dev Notes, schema sections, or SQL
4. **Endpoints produced** — API routes this item creates (for BE items)
5. **Endpoints consumed** — API routes this item needs (for FE items)
6. **Explicit dependencies** — "Depends on X", "Blocked by #Y", "Requires Z to exist"
7. **Models/Types shared** — data models used across items
8. **Complexity estimate** — S (< 2h), M (2-4h), L (4-8h), XL (8h+) based on scope

If items are in Jira format (from /spec), parse:
- Routes section for endpoint paths
- Dev Notes for table names and schema references
- Acceptance Criteria for functional dependencies

### For Code Modules

For each module/package, extract:
1. **Module path** — file path or package name
2. **Imports** — what this module imports (direct dependencies)
3. **Exports** — what this module exposes (public API surface)
4. **Package dependencies** — external packages from manifest files
5. **Shared types** — types/interfaces imported by multiple modules

Scan these files for dependency information:
- **JS/TS:** `import`/`require` statements, `package.json`
- **Python:** `import`/`from` statements, `requirements.txt`, `pyproject.toml`
- **Go:** `import` blocks, `go.mod`
- **Rust:** `use` statements, `Cargo.toml`
- **Dart/Flutter:** `import` statements, `pubspec.yaml`
- **Java/Kotlin:** `import` statements, `build.gradle`, `pom.xml`

============================================================
PHASE 2: BUILD DEPENDENCY GRAPH
============================================================

### For Stories / Specs

For each item pair (A, B), check for dependencies:

1. **Table dependency:** B uses a table/collection that A creates. -> B depends on A.
2. **API dependency:** B (FE) consumes an endpoint that A (BE) creates. -> B depends on A.
3. **Data dependency:** B uses a model/type that A defines. -> B depends on A.
4. **Explicit dependency:** B references A by name or ID. -> B depends on A.
5. **Schema dependency:** B alters a table that A creates. -> B depends on A.

### For Code Modules

1. **Import dependency:** Module B imports from Module A. -> B depends on A.
2. **Package dependency:** Package B lists Package A as a dependency.
3. **Type dependency:** Module B uses a type/interface defined in Module A.
4. **Re-export dependency:** Module B re-exports from Module A.

Build an adjacency list: `{ itemId: [depends_on_ids] }`

============================================================
PHASE 3: DETECT ISSUES
============================================================

1. **Circular dependencies:** Run cycle detection on the graph.
   If found: CRITICAL — list each cycle with the exact items involved.
   Provide specific cycle-breaking recommendations:
   - For stories: suggest splitting a story or extracting a shared foundation item
   - For code: suggest extracting shared interfaces to a common module,
     using dependency inversion (depend on abstractions), or lazy loading

2. **Missing dependencies:** Item references a table/endpoint/model/module that nothing provides.
   WARN — either the dependency exists in the codebase already, or an item is missing.

3. **Orphan items:** Items with no dependencies and nothing depends on them.
   INFO — these can be implemented at any time.

4. **Long chains:** Dependency chains longer than 4 items.
   WARN — bottleneck risk. Consider parallelizing or splitting.

5. **High fan-in:** Items that 5+ other items depend on.
   WARN — high-risk item. If delayed, it blocks many downstream items. Prioritize.

6. **High fan-out:** Items that depend on 5+ other items.
   WARN — integration risk. Likely to be blocked frequently. Consider splitting.

============================================================
PHASE 4: COMPUTE OPTIMAL ORDER
============================================================

1. Run topological sort on the dependency graph.
2. Group items into parallel batches:
   - Batch 1: Items with zero dependencies (can all start simultaneously)
   - Batch 2: Items whose only dependencies are in Batch 1
   - Batch N: Items whose dependencies are all in earlier batches
3. Within each batch, order by:
   - Number of items that depend on this one (more dependents = higher priority)
   - Item type: BE/INFRA before FE within a batch (APIs must exist before frontends)
   - Complexity: smaller items first within equal priority (unblock faster)
4. Calculate the critical path (longest chain of sequential dependencies).
5. Estimate time per batch based on item complexity:
   - S = 2h, M = 4h, L = 8h, XL = 16h
   - Batch time = max(item times) assuming full parallelism within batch
   - Total time = sum(batch times) along critical path


============================================================
SELF-HEALING VALIDATION (max 2 iterations)
============================================================

After producing output, validate data quality and completeness:

1. Verify all output sections have substantive content (not just headers).
2. Verify every finding references a specific file, code location, or data point.
3. Verify recommendations are actionable and evidence-based.
4. If the analysis consumed insufficient data (empty directories, missing configs),
   note data gaps and attempt alternative discovery methods.

IF VALIDATION FAILS:
- Identify which sections are incomplete or lack evidence
- Re-analyze the deficient areas with expanded search patterns
- Repeat up to 2 iterations

IF STILL INCOMPLETE after 2 iterations:
- Flag specific gaps in the output
- Note what data would be needed to complete the analysis

============================================================
OUTPUT
============================================================

## Dependency Map

### Items Analyzed: {N}
**Input type:** {Stories / Code Modules / Mixed}

### Dependency Graph (ASCII)
```
{ASCII visualization}

Example:
STORY-001 (BE: Auth) ---+---> STORY-003 (BE: Users)
                        +---> STORY-004 (BE: Orgs)
STORY-002 (BE: Base) -------> STORY-005 (BE: Points)
STORY-003 ------------------> STORY-007 (FE: User Profile)
STORY-004 ------------------> STORY-008 (FE: Org Dashboard)
```

### Dependency Graph (Mermaid)
```mermaid
graph TD
    A[STORY-001: Auth] --> C[STORY-003: Users]
    A --> D[STORY-004: Orgs]
    B[STORY-002: Base] --> E[STORY-005: Points]
    C --> G[STORY-007: User Profile]
    D --> H[STORY-008: Org Dashboard]
```

### Issues
| Severity | Issue | Items | Recommendation |
|---|---|---|---|
| {CRITICAL/WARN/INFO} | {issue type} | {item IDs} | {specific fix — code-level for cycles} |

### Implementation Order

**Batch 1** (no dependencies — start all in parallel) — Est. {N}h:
| # | Item | Type | Size | Dependents | Notes |
|---|---|---|---|---|---|
| 1 | {item} | {BE/FE/INFRA} | {S/M/L/XL} | {N items depend on this} | {notes} |

**Batch 2** (depends on Batch 1) — Est. {N}h:
| # | Item | Type | Size | Blocked By | Notes |
|---|---|---|---|---|---|
| 1 | {item} | {BE/FE/INFRA} | {S/M/L/XL} | {item IDs} | {notes} |

... (repeat for each batch)

### Critical Path
```
{longest sequential chain}
STORY-001 (2h) -> STORY-003 (4h) -> STORY-007 (8h) -> STORY-010 (4h)
```
- **Length:** {N} sequential items
- **Estimated critical path time:** {N}h
- **Parallelizable items:** {N} (across all batches)
- **Max parallelism:** Batch {N} has {M} items that can run simultaneously

### Cycle-Breaking Recommendations
(Only if cycles were detected)
For each cycle:
1. **Cycle:** A -> B -> C -> A
2. **Root cause:** {why the cycle exists}
3. **Recommended fix:** {specific action}
   - For code: "Extract `SharedTypes` interface from `module_a.ts` and `module_b.ts` into `types/shared.ts`. Both modules import from the new file instead of each other."
   - For stories: "Split STORY-003 into STORY-003a (schema only) and STORY-003b (logic). STORY-001 depends on 003a, 003b depends on 001."

### Summary
- **Total items:** {N}
- **Batches:** {N}
- **Critical path length:** {N} items ({N}h estimated)
- **Total estimated time (parallel):** {N}h (with full parallelism per batch)
- **Total estimated time (sequential):** {N}h (if done one at a time)
- **Max items in parallel:** {N}
- **Circular dependencies:** {N found / none}
- **High-risk items:** {list items with fan-in >= 5}


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dep-map — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
