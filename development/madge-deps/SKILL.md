---
name: madge-deps
description: "Run Madge against a JS/TS production source tree to detect circular dependencies, find orphan modules, and visualize the module graph. Scoped to production code via `excludeRegExp` for test files. Use when a build compiles but throws `Cannot read property X of undefined` on a module that is clearly imported, or when a repo needs a CI gate that blocks new import cycles."
metadata:
  keywords: "madge, circular-dependency, module-graph, dependency-analysis, javascript, typescript"
  version: "1.1.5"
---

# madge-deps

Madge analyzes JavaScript module graphs (AMD, CommonJS, ES6) and CSS
preprocessor imports (Sass, Stylus, Less) per the [Madge README]. NPM
deps and Node core modules are excluded by default.

## When to use

- A bundle that compiles but throws `Cannot read property X of
  undefined` at runtime - likely a circular import causing partial
  module init.
- Pre-merge gate to block any new circular dep.
- Finding orphan files (no imports + no exports referenced) to delete.

## Step 1 - Install

```bash
npm install -g madge
# or per-project
npm install -D madge
```

Optional Graphviz for visual graphs:

| OS | Install |
|---|---|
| macOS | `brew install graphviz` |
| Ubuntu | `apt-get install graphviz` |
| Windows | `choco install graphviz` |

Per the [Madge README].

## Step 2 - Detect circular dependencies

```bash
# Single entry point
madge --circular src/index.ts

# Whole directory
madge --circular src/
```

Exit code: 0 if none found, 1 if any circular path exists. Use
directly in CI.

## Step 3 - Find orphans + leaves

```bash
# Files imported by nothing
madge --orphans src/

# Files that import nothing (terminal modules)
madge --leaves src/
```

Orphans are deletion candidates; verify usage outside source tree
(scripts, configs, side-effect imports) before removal.

## Step 4 - Visualize

```bash
# Render full graph as SVG (requires Graphviz)
madge --image graph.svg src/

# Show what depends on a specific file
madge --depends src/config/db.ts src/

# Export raw DOT for custom rendering
madge --dot src/ > graph.gv
```

## Step 5 - Configure for production-only scope

`.madgerc` in project root:

```json
{
  "fileExtensions": ["ts", "tsx", "js", "jsx"],
  "excludeRegExp": [
    "\\.test\\.(ts|tsx|js|jsx)$",
    "\\.spec\\.(ts|tsx|js|jsx)$",
    "__tests__/",
    "__mocks__/",
    "node_modules/",
    "dist/",
    "build/"
  ],
  "tsConfig": "tsconfig.json"
}
```

Test files are excluded so tests can intentionally
import production modules without flagging the production tree.

## Step 6 - CI gate

```yaml
# GitHub Actions
- name: Block circular deps
  run: npx madge --circular --extensions ts,tsx src/

- name: Detect new orphans (advisory)
  run: npx madge --orphans --extensions ts,tsx src/ || true
```

The first step fails on any circular path; the second is informational
only (orphans require human judgment - could be webpack entry, dynamic
import, etc.).

## Anti-patterns

| Anti-pattern | Why it fails | Fix |
|---|---|---|
| Scan whole repo including `node_modules/` | OOM on large workspaces | `excludeRegExp: ["node_modules/"]` (Step 5) - actually default behavior, but verify |
| Treat orphans as "always delete" | Webpack/Vite entry points + dynamic imports look orphaned | Manual review per orphan; use `--depends` to verify (Step 4) |
| Allow circular deps in non-prod with "we'll fix later" | Cycles compound; mid-project untangling is brutal | Block on first cycle (Step 6); waiver template if scope-exclusion needed |
| Forget `tsconfig.json` for path aliases | Madge can't resolve `@/foo` imports; reports false positives | `"tsConfig": "tsconfig.json"` in `.madgerc` (Step 5) |
| Run with default extensions (`js` only) for TS project | Misses 100% of TS files | `fileExtensions: ["ts", "tsx", "js", "jsx"]` (Step 5) |

## Limitations

- Madge resolves *static* imports only; dynamic `import()` calls and
  `require()` with computed strings are not in the graph.
- ESM-only projects: ensure Madge version supports your Node ESM
  resolver. Check the [Madge README] for current ESM compat notes.

## References

- [Madge README] - CLI flags, .madgerc schema, extension support

[Madge README]: https://github.com/pahen/madge
