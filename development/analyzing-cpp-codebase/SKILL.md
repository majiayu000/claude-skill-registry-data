---
name: analyzing-cpp-codebase
description: Analyzes C++ desktop codebase architecture, dependency graphs, framework detection, and migration assessment. Use when exploring an unfamiliar C++ project or assessing upgrade paths.
compatibility: Designed for Claude Code
metadata:
  allowed-tools: Read, Grep, Glob, Bash
  argument-hint: [directory-or-question]
  stability: stable
  content-hash: sha256:0fccb258bd50eb0c465a69a8a9e1f59a74c49ce5f2ec2c3042bfe641b919b5d0
---

# C++ Codebase Analysis

**Target**: $ARGUMENTS

Analyzes C++ desktop project structure, dependencies, and architecture.
Delivers actionable findings, not exhaustive documentation.

## Workflow

1. **Detect project layout** — scan for CMakeLists.txt, .pro files, src/, include/
2. **Identify framework** — determine wxWidgets, GTK3, Qt, or mixed
3. **Map dependencies** — CMake targets, find_package calls, include graph
4. **Assess architecture** — module boundaries, coupling, layering
5. **Report findings** — structured summary with actionable items

## Framework Detection

Check these indicators in order:

| Framework  | CMake Signal                    | Include Signal          | Other               |
|------------|---------------------------------|-------------------------|----------------------|
| Qt         | `find_package(Qt6)` / `Qt5`    | `#include <QWidget>`    | `.pro`, `.qrc` files |
| wxWidgets  | `find_package(wxWidgets)`       | `#include <wx/wx.h>`    | —                    |
| GTK3       | `pkg_check_modules(GTK3)`      | `#include <gtk/gtk.h>`  | `.ui` (GtkBuilder)   |

## Dependency Mapping

```bash
# List all CMake targets
grep -rn "add_library\|add_executable" CMakeLists.txt */CMakeLists.txt 2>/dev/null

# List external dependencies
grep -rn "find_package\|pkg_check_modules" CMakeLists.txt */CMakeLists.txt 2>/dev/null

# Include graph (most-included headers)
grep -rh '#include "' src/ include/ 2>/dev/null | sort | uniq -c | sort -rn | head -20
```

## Architecture Assessment

Evaluate these dimensions:

**Module Boundaries**:

- Are source files organized by feature or by layer?
- Is there a clear `src/` vs `include/` separation?
- Are GUI components isolated from business logic?

**Coupling**:

- How many cross-module includes exist?
- Are there circular dependencies?
- Is dependency injection or interface abstraction used?

**Build Structure**:

- Single CMakeLists.txt or hierarchical?
- Are libraries split into reusable targets?
- Are tests in a separate target?

## Migration Assessment

When evaluating framework upgrades (e.g., wxWidgets 3.0 to 3.2, Qt5 to Qt6):

1. **Identify version** — check CMake version constraints, include paths
2. **List deprecated APIs** — grep for known deprecated symbols
3. **Assess scope** — count affected files and call sites
4. **Estimate effort** — categorize changes as mechanical vs architectural
5. **Flag blockers** — identify removed APIs requiring redesign

## Output Format

```markdown
## Project Summary
- Framework: [detected]
- C++ standard: [detected from CMake or compiler flags]
- Build system: [CMake version / qmake]
- Modules: [count and names]

## Dependency Graph
[CMake target relationships]

## Architecture Notes
[Key observations about structure and coupling]

## Recommendations
[Prioritized, actionable items]
```

## Rules

- Report facts, not opinions — cite file paths and line numbers
- Flag risks but do not refactor without explicit request
- Keep output structured and scannable
