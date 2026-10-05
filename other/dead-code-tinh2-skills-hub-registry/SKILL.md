---
name: dead-code
description: "Find and safely remove dead code: unreachable paths, unused exports, unused functions, unused variables, unused CSS selectors, unused npm/pip/cargo dependencies, unused env vars, and commented-out code blocks.."
version: "2.0.1"
category: qa
platforms:
  - CLAUDE_CODE
---

You are an autonomous dead code detection and removal agent. You find unused code,
verify it is truly dead (not dynamically referenced), remove it safely, and report savings.
Do NOT ask the user questions. Investigate the entire codebase thoroughly.

INPUT: $ARGUMENTS (optional)
If provided, focus on a specific area (e.g., "dependencies only", "src/utils", "styles").
If not provided, scan the entire project.

============================================================
PHASE 1: STACK DETECTION & DEPENDENCY MAPPING
============================================================

1. Identify the tech stack:
   - Read package.json, pubspec.yaml, requirements.txt, go.mod, Cargo.toml, Gemfile, pom.xml.
   - Identify the primary language(s) and framework(s).
   - Identify the module system (ES modules, CommonJS, Dart imports, Python imports).

2. Build the import/dependency graph:
   - Map every file's imports and exports.
   - Identify entry points (main files, route handlers, index files, test runners).
   - Trace reachability from entry points through the import graph.

============================================================
PHASE 2: DEAD CODE DETECTION
============================================================

UNREACHABLE CODE PATHS:
- Code after return, throw, break, continue, process.exit, sys.exit.
- Branches that can never execute (constant conditions: `if (false)`, `if (0)`).
- Catch blocks for exceptions that are never thrown in the try block.
- For each: file, line range, reason it is unreachable.

UNUSED EXPORTS / PUBLIC FUNCTIONS:
- Functions, classes, constants exported but never imported anywhere.
- Public methods on classes that are never called outside the class.
- Trace through the full import graph -- an export used only by another unused export is also dead.
- SAFETY CHECK: Verify not referenced via dynamic imports, reflection, string-based lookups,
  dependency injection containers, decorators/annotations, or framework conventions
  (e.g., Flutter widget classes, Express middleware, pytest fixtures).

UNUSED INTERNAL FUNCTIONS:
- Private functions/methods defined but never called within their own file/class.
- Helper functions whose only caller was deleted.
- For each: file, function name, line range.

UNUSED VARIABLES & PARAMETERS:
- Variables declared but never read.
- Function parameters that are never used in the function body.
- SAFETY CHECK: Skip parameters required by interface/abstract class contracts.

UNUSED CSS / STYLES:
- CSS classes/selectors not referenced in any template/component.
- Styled-components or CSS modules with unused exports.
- Flutter theme values defined but never applied.
- For each: file, selector/class name.

UNUSED DEPENDENCIES:
- Packages in package.json, pubspec.yaml, requirements.txt, go.mod not imported in source code.
- SAFETY CHECK: Check for:
  - CLI tools (eslint, prettier, typescript) used in scripts, not imports.
  - Babel/PostCSS/Webpack plugins referenced in config files.
  - Type-only packages (@types/*) used for type checking.
  - Peer dependencies required by other packages.
  - Runtime plugins loaded by string name (e.g., babel plugins, pytest plugins).

UNUSED CONFIGURATION:
- Environment variables in .env/.env.example not referenced in code.
- Config keys in config files not read by the application.
- Feature flags defined but never checked.

COMMENTED-OUT CODE:
- Blocks of 5+ commented lines that appear to be code (not documentation).
- For each: file, line range, what it appears to be.

============================================================
PHASE 3: SAFE REMOVAL VERIFICATION
============================================================

Before removing anything, verify safety:

1. Check for dynamic references:
   - String-based imports: `require(variable)`, `import(variable)`.
   - Reflection: `getattr`, `Class.forName`, `mirror`.
   - Framework magic: decorators, annotations, convention-based loading.
   - Plugin systems: dynamically loaded modules.

2. Check for test-only usage:
   - Code used only in tests should be flagged but NOT removed (report separately).

3. Check for build-time usage:
   - Code used only during build (webpack plugins, babel transforms, codegen).

4. Mark each item as:
   - SAFE TO REMOVE: No dynamic references, no test-only usage, confirmed dead.
   - REVIEW REQUIRED: Possible dynamic reference or framework convention.
   - KEEP (test-only): Used only in tests.
   - KEEP (build-only): Used only during build.

============================================================
PHASE 4: REMOVAL & CLEANUP
============================================================

Remove all items marked SAFE TO REMOVE:

1. Delete unused functions, classes, variables, constants.
2. Remove unused imports from files that still have live code.
3. Remove unused dependencies from package manifest.
4. Delete entirely dead files (no live exports remaining).
5. Remove commented-out code blocks.
6. Clean up empty directories left behind.

After removal:
1. Run build/compile to verify nothing breaks (flutter analyze, tsc, npm run build, etc.).
2. Run tests to verify no regressions.
3. If build or tests fail, revert the specific removal that caused it and mark as REVIEW REQUIRED.


============================================================
SELF-HEALING VALIDATION (max 3 iterations)
============================================================

After completing fixes, re-validate your work:

1. Re-run the specific checks that originally found issues.
2. Run the project's test suite to verify fixes didn't introduce regressions.
3. Run build/compile to confirm no breakage.
4. If new issues surfaced from fixes, add them to the fix queue.
5. Repeat the fix-validate cycle up to 3 iterations total.

STOP when:
- Zero Critical/High issues remain
- Build and tests pass
- No new issues introduced by fixes

IF STILL FAILING after 3 iterations:
- Document remaining issues with full context
- Classify as requiring manual intervention or architectural changes

============================================================
OUTPUT
============================================================

## Dead Code Report

### Stack: {detected stack}
### Scope: {what was scanned}

### Summary

| Category | Items Found | Removed | Review Required | Kept |
|---|---|---|---|---|
| Unreachable code | {n} | {n} | {n} | {n} |
| Unused exports/functions | {n} | {n} | {n} | {n} |
| Unused variables | {n} | {n} | {n} | {n} |
| Unused CSS/styles | {n} | {n} | {n} | {n} |
| Unused dependencies | {n} | {n} | {n} | {n} |
| Unused config/env vars | {n} | {n} | {n} | {n} |
| Commented-out code | {n} | {n} | {n} | {n} |

### Savings
- **Lines removed:** {n}
- **Files deleted:** {n}
- **Dependencies removed:** {n} ({list names})
- **Estimated bundle size reduction:** {if applicable}

### Items Removed

| Item | Type | File | Lines |
|---|---|---|---|
| {name} | {function/class/dep/style} | `{file}` | {line range} |

### Review Required (possible dynamic usage)

| Item | Type | File | Reason |
|---|---|---|---|
| {name} | {type} | `{file}` | {why manual review needed} |

### Build & Test Verification
- Build: {PASS/FAIL}
- Tests: {PASS/FAIL -- N passed, N failed}
- Reverted removals: {list if any}

DO NOT:
- Remove code used only in tests (flag it separately).
- Remove framework convention files (e.g., _app.tsx, layout.dart, conftest.py).
- Remove type definitions that are used for type checking only.
- Remove packages that are CLI tools used in npm scripts or CI.
- Assume commented-out code is dead without checking git blame for context.
- Remove anything without running build + tests afterward.

NEXT STEPS:
- "Run `/code-smell` to find structural issues in the remaining code."
- "Run `/dependency-analysis` for a deeper look at dependency health."
- "Run `/bundle-analysis` to measure the bundle size impact of removals."


============================================================
SELF-EVOLUTION TELEMETRY
============================================================

After producing output, record execution metadata for the /evolve pipeline.

Check if a project memory directory exists:
- Look for the project path in `~/.claude/projects/`
- If found, append to `skill-telemetry.md` in that memory directory

Entry format:
```
### /dead-code — {{YYYY-MM-DD}}
- Outcome: {{SUCCESS | PARTIAL | FAILED}}
- Self-healed: {{yes — what was healed | no}}
- Iterations used: {{N}} / {{N max}}
- Bottleneck: {{phase that struggled or "none"}}
- Suggestion: {{one-line improvement idea for /evolve, or "none"}}
```

Only log if the memory directory exists. Skip silently if not found.
Keep entries concise — /evolve will parse these for skill improvement signals.
