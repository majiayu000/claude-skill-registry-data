---
name: documentation-creation
description: Create a comprehensive frontend project documentation suite from scratch by analyzing the React/TypeScript codebase and verifying every claim against it. Use when setting up INITIAL documentation for a project or building a complete docs/ suite where none exists. NOT for updating existing docs (use documentation-sync instead). Covers project analysis, documentation structure, templates, and verification.
---

# Documentation Creation Skill

## Profile keys consumed

- `project.name`
- `project.repo`
- `framework.ui`
- `framework.state`
- `framework.di`
- `framework.router`
- `framework.bundler`
- `framework.package_manager`
- `framework.runtime`
- `framework.i18n`
- `framework.graphql_mock`
- `architecture.source_root`
- `architecture.modules`
- `architecture.component_prefix`
- `architecture.path_aliases`
- `make.ci`
- `make.start`
- `make.lint_md`
- `make.format`
- `make.test_unit_client`
- `make.test_unit_server`
- `make.test_e2e`
- `make.test_load`
- `make.lighthouse_desktop`
- `make.lighthouse_mobile`
- `quality.coverage_lines`
- `quality.mutation_msi`
- `quality.lighthouse_desktop`
- `quality.lighthouse_mobile`
- `capabilities.load_testing`
- `capabilities.lighthouse`
- `capabilities.storybook`

## Overview

This skill guides the creation of comprehensive project documentation
from scratch by analyzing the frontend codebase against the project
profile and applying consistent documentation patterns. It ensures
documentation accurately reflects the actual React/TypeScript
implementation.

**Use this skill for**: initial documentation creation from scratch
**Use documentation-sync for**: updating existing documentation when
code changes

## Context (Input)

- Need to create documentation for a frontend project from scratch
- Want consistent style across the whole documentation suite
- Need to ensure documentation accuracy against the actual codebase
- Project has no existing comprehensive documentation

## Task (Function)

Create comprehensive, accurate project documentation by:

1. Analyzing the project codebase thoroughly, starting from the profile
2. Creating documentation using the established templates
3. Verifying all references against the actual codebase
4. Ensuring consistent style and cross-linking

**Success criteria**:

- All documentation files created with consistent structure
- All code references verified against the actual project structure
- All directory paths and file mentions exist in the codebase
- All links between documentation files work correctly
- Technology stack accurately reflected (no false claims)
- Markdown passes the gate mapped by `make.lint_md`

---

## Quick Start: Documentation Creation Workflow

### Step 1: Analyze Project Structure

The profile declares what the project claims to be; the codebase shows
what it is. Read the profile first, then verify each claim. In the
commands below, `$SRC` is `architecture.source_root` and `$MOD` iterates
`architecture.modules` (each feature-module directory under
`<source_root>/modules`).

```bash
# Check project structure
ls -la "$SRC"/

# Identify the toolchain (deps, scripts, versions)
grep -A20 '"dependencies"' package.json
cat tsconfig.paths.json
cat rsbuild.config.ts

# Verify each declared feature module exists
for MOD in <each architecture.modules entry>; do
  ls -la "$SRC/modules/$MOD/" 2>/dev/null \
    || echo "Profile drift: $SRC/modules/$MOD missing"
done

# Reusable UI components (architecture.component_prefix, e.g. UI*)
find "$SRC/components" -maxdepth 2 -type d

# Feature surface: stores, repositories, hooks, components
find "$SRC" -path "*/features/*" -name "*.ts*" | head -20
```

**Key items to document**:

- [ ] Technology stack (`framework.ui`, `framework.state`,
      `framework.bundler`, `framework.runtime`, `framework.package_manager`)
- [ ] Architecture style (modular bulletproof-react, DI, reactive state)
- [ ] Feature modules (`architecture.modules`) and their purposes, plus
      the reusable component layer (`architecture.component_prefix`)
- [ ] Path aliases (`architecture.path_aliases`) and import conventions
- [ ] Available make targets (from the profile `make` map) and testing
      tools

### Step 2: Create Technology Stack Summary

Verify the profile's stack claims against the repository before
documenting them:

```bash
# Node runtime — must match framework.runtime
grep -i '"node"' package.json
cat .nvmrc

# UI + styling layer — must match framework.ui
grep -iE '@mui/material|@emotion' package.json

# Bundler — must match framework.bundler
grep -i rsbuild package.json rsbuild.config.ts

# Available make targets — the names the make.* map points at
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile | head -30
```

Create a technology summary table sourced from the verified profile
values:

| Component        | Technology                  | Source                           |
| ---------------- | --------------------------- | -------------------------------- |
| Language         | TypeScript                  | `package.json`                   |
| Runtime          | `framework.runtime`         | `.nvmrc` + `package.json`        |
| Package manager  | `framework.package_manager` | lockfile + `package.json`        |
| UI + styling     | `framework.ui`              | `package.json` dependencies      |
| State            | `framework.state`           | `package.json` dependencies      |
| DI container     | `framework.di`              | `package.json` dependencies      |
| Router           | `framework.router`          | `package.json` dependencies      |
| Bundler          | `framework.bundler`         | bundler config + `package.json`  |
| i18n             | `framework.i18n`            | `package.json` dependencies      |
| GraphQL mock     | `framework.graphql_mock`    | `package.json` dependencies      |

### Step 3: Create Documentation Files

Create each documentation file following this order:

1. **main.md** - Project overview and design principles
2. **getting-started.md** - Installation and quick start (Docker dev
   server + API mock)
3. **design-and-architecture.md** - Modular bulletproof-react layout, DI,
   state, and routing decisions
4. **developer-guide.md** - Code structure and development workflow
5. **components.md** - Reusable UI component catalog
   (`architecture.component_prefix`) and the data layer; include a
   GraphQL data-layer section only when `framework.graphql_mock` is a
   string (not `null`), and Storybook usage only when
   `capabilities.storybook` is true
6. **testing.md** - Testing strategy and commands
7. **glossary.md** - Domain and frontend terminology and naming
   conventions
8. **user-guide.md** - End-user flows and usage examples
9. **advanced-configuration.md** - Environment variables and
   configuration
10. **performance.md** - Web-vitals and Lighthouse budgets; cover the
    Lighthouse audits only when `capabilities.lighthouse` is true
    (targets mapped by `make.lighthouse_desktop` /
    `make.lighthouse_mobile`) and load testing only when
    `capabilities.load_testing` is true (target mapped by
    `make.test_load`)
11. **security.md** - Frontend security measures and practices
12. **operational.md** - Operational considerations
13. **onboarding.md** - New contributor guide
14. **community-and-support.md** - Support channels
15. **legal-and-licensing.md** - License and dependencies
16. **release-notes.md** - Release process
17. **versioning.md** - Versioning policy

> Add project-specific docs as needed (e.g. an `accessibility.md` for a
> mandatory a11y gate, or a `storybook.md` when `capabilities.storybook`
> is true)

### Step 4: Write Each Documentation File

For each documentation file:

1. **Use the appropriate template** (see Documentation Templates below)

2. **Fill in project-specific content**:

   - Project name: use `project.name` consistently throughout
   - Repository links: build from `project.repo`
     (`https://github.com/<project.repo>`)
   - Component names from the codebase (`architecture.component_prefix`)
   - Feature-module names from `architecture.modules`

3. **Verify all references**:

   - Directory paths exist under `architecture.source_root`
   - Import examples use a configured alias from
     `architecture.path_aliases` (never a deep `../../../` chain)
   - Every documented make invocation uses the actual target name the
     profile `make` map points at (e.g. the target mapped by `make.ci`)
     and that target exists in the Makefile. A `null` mapping means the
     capability is absent: do not document it; note the gap instead
   - Component and module names match the codebase

4. **Add cross-links** to related documentation

5. **Quality thresholds**: where testing.md or performance.md cite
   quality bars, take values only from the profile `quality.*` keys —
   canonical defaults are 100% coverage (`quality.coverage_lines`),
   mutation MSI seeded from the repo's Stryker `break`
   (`quality.mutation_msi`), and Lighthouse floors of 95 desktop
   (`quality.lighthouse_desktop`) / 85 mobile
   (`quality.lighthouse_mobile`). Thresholds are raise-only: never
   document a bar lower than the shipped default

6. **Markdown standards**: keep headings in order, give every fenced code
   block a language hint, keep lines under the markdownlint limit, avoid
   bare URLs (use markdown links), and keep tables narrow enough to pass
   the gate mapped by `make.lint_md`

### Step 5: Verify Accuracy

Run comprehensive verification (full checklist below):

1. **Technology Stack Verification**:

   ```bash
   cat .nvmrc                                     # framework.runtime
   grep -iE '@mui/material|@emotion' package.json # framework.ui
   grep -i rsbuild package.json                   # framework.bundler
   ```

2. **Directory Structure Verification**:

   ```bash
   # Verify every source directory mentioned in the docs exists
   for dir in $(ls "$SRC"/); do
     ls -la "$SRC/$dir/" 2>/dev/null || echo "Check: $SRC/$dir"
   done
   ```

3. **Command Verification** — for every non-null `make.*` mapping
   documented (at minimum the targets mapped by `make.ci`, `make.start`,
   `make.test_unit_client`, `make.test_e2e`):

   ```bash
   for cmd in <each documented target name from the profile make map>; do
     grep -q "^$cmd:" Makefile && echo "Found: $cmd" || echo "Missing: $cmd"
   done
   ```

4. **Markdown & Link Verification**:
   - Run the gate mapped by `make.lint_md` (after `make.format`)
   - Check all internal markdown links resolve
   - Verify external links (including `project.repo` links) are accurate

Worked example against the reference SPA template:

```bash # profile-example
# architecture.modules: [user, back-to-main]; component_prefix: UI
ls -la src/modules/user/ src/modules/back-to-main/
# framework.bundler: rsbuild
grep -i rsbuild package.json
# make map: ci → ci, test_unit_client → test-unit-client, test_e2e → test-e2e
for cmd in ci test-unit-client test-e2e; do grep -q "^$cmd:" Makefile && echo "Found: $cmd"; done
```

---

## Documentation Templates

### Overview Document (main.md)

```markdown
# {project.name}

Welcome to the **{project.name}** documentation...

## Design Principles

{List project's core design principles — modular bulletproof-react,
accessibility-first UI, container-free render path, raise-only quality}

## Technology Stack

| Component | Technology          | Source       |
| --------- | ------------------- | ------------ |
| Language  | TypeScript          | package.json |
| UI        | {framework.ui}      | package.json |
| State     | {framework.state}   | package.json |
| Bundler   | {framework.bundler} | package.json |
```

### Getting Started (getting-started.md)

```markdown
# Getting Started

## Prerequisites

{List required software with versions — Docker, the runtime named by
framework.runtime, the manager named by framework.package_manager}

## Installation

{Step-by-step installation commands; boot the dev server + API mock via
the target mapped by make.start}

## Verification

{Commands to verify installation — open the dev server port, run the
target mapped by make.test_unit_client}
```

Derive the remaining files from the structure in Format (Output) below,
keeping headings and tone consistent with these two templates.

---

## Constraints

### NEVER

- Include references to non-existent directories or files
- Claim features or technologies the project doesn't use (e.g. a GraphQL
  data-layer page when `framework.graphql_mock` is `null`, or a Storybook
  page when `capabilities.storybook` is false)
- Leave placeholder text unreplaced
- Skip the verification step after creating documentation
- Document make targets that don't exist in the Makefile, or logical
  profile key names (`make.ci`) as if they were target names — always
  document the mapped target
- Document quality thresholds below the profile `quality.*` values

### ALWAYS

- Verify every directory path mentioned exists
- Confirm the technology stack matches both the profile and the repo
- Test command examples work in the project
- Update all cross-references to point to correct files
- Maintain consistent terminology throughout; `project.name` is the only
  name used for the project
- Show imports through a `architecture.path_aliases` alias, never a deep
  relative chain
- Run the formatter (`make.format`) and the markdown gate (`make.lint_md`)
  before presenting docs
- Add a Table of Contents to longer documents (100+ lines)

---

## Verification Checklist

After creating documentation:

### Technology Accuracy

- [ ] Node runtime matches `.nvmrc` and `framework.runtime`
- [ ] UI + styling layer matches `package.json` and `framework.ui`
- [ ] Bundler matches `rsbuild.config.ts` and `framework.bundler`
- [ ] State, DI, router, and i18n described per `framework.state` /
      `framework.di` / `framework.router` / `framework.i18n`
- [ ] GraphQL mock described per `framework.graphql_mock`
      (or omitted when `null`)
- [ ] No false claims about unused technologies

### Structure Accuracy

- [ ] All mentioned source directories exist under
      `architecture.source_root`
- [ ] All feature-module names match `architecture.modules`
- [ ] Reusable component names use `architecture.component_prefix`
- [ ] Import examples use a configured `architecture.path_aliases` alias

### Command Accuracy

- [ ] All documented make targets exist in the Makefile and come from
      the profile `make` map; `null` capabilities are noted, not
      documented
- [ ] Docker commands work as documented
- [ ] Test commands (targets mapped by `make.test_unit_client`,
      `make.test_unit_server`, `make.test_e2e`) produce the documented
      output
- [ ] Markdown passes the gate mapped by `make.lint_md`

### Link Accuracy

- [ ] All internal markdown links resolve
- [ ] External repository links match `project.repo`
- [ ] No broken navigation links

### Content Consistency

- [ ] Project name (`project.name`) consistent throughout
- [ ] Terminology consistent across documents
- [ ] No placeholder text remaining

---

## Common Pitfalls

### Technology Mismatch

**Problem**: Documenting technologies the project doesn't use

**Solution**:

```bash
# Verify before documenting
grep -iE '@mui/material|@emotion|zustand|tsyringe' package.json
cat rsbuild.config.ts
# Only document what actually exists — and reconcile with the profile
```

### Missing Directories

**Problem**: Documenting directories that don't exist under the source
root

**Solution**:

```bash
# Verify before documenting
ls -la "$SRC"/ "$SRC/modules"/ "$SRC/components"/
# Update to match the actual structure
```

### Outdated Commands

**Problem**: Documenting non-existent make targets, or writing logical
key names instead of the mapped targets

**Solution**:

```bash
# Check the actual Makefile against the profile make map
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile
```

### Missing Table of Contents

**Problem**: Long documents hard to navigate

**Solution**: Add a TOC to documents over 100 lines:

```markdown
## Table of Contents

- [Section 1](#section-1)
- [Section 2](#section-2)
- [Section 3](#section-3)

---
```

---

## Format (Output)

### Expected Documentation Structure

```text
docs/
├── main.md                    # Project overview
├── getting-started.md         # Installation guide
├── design-and-architecture.md # Architecture patterns
├── developer-guide.md         # Development workflow
├── components.md              # UI component catalog (+ data layer)
├── testing.md                 # Testing strategy
├── glossary.md                # Domain & frontend terminology
├── user-guide.md              # End-user flows
├── advanced-configuration.md  # Environment config
├── performance.md             # Web-vitals & Lighthouse budgets
├── security.md                # Security measures
├── operational.md             # Operations guide
├── onboarding.md              # Contributor guide
├── community-and-support.md   # Support channels
├── legal-and-licensing.md     # License info
├── release-notes.md           # Release process
└── versioning.md              # Versioning policy
```

### Expected Verification Result

All verification checks pass:

- Technology stack matches reality (and the profile)
- All directory paths exist
- All commands work
- All links resolve
- Markdown passes the gate mapped by `make.lint_md`

---

## Related Skills

- [documentation-sync](../documentation-sync/SKILL.md) - Keep docs in
  sync with code changes (use AFTER initial creation)
- [frontend-component-development](../frontend-component-development/SKILL.md) -
  Component and data-layer documentation patterns
- [frontend-testing-workflow](../frontend-testing-workflow/SKILL.md) -
  Testing documentation (Jest client/server, Playwright E2E + visual,
  Stryker mutation)
- [frontend-performance-accessibility](../frontend-performance-accessibility/SKILL.md) -
  Performance and accessibility documentation (when
  `capabilities.lighthouse` is true)
- [load-testing](../load-testing/SKILL.md) - Load-test documentation
  (when `capabilities.load_testing` is true)

The `react-implementer` agent produces the code this skill documents;
the `accessibility-auditor` agent's findings feed any project-specific
`accessibility.md`.

**Skill Relationship**:

- **documentation-creation** (this skill): create initial documentation
  from scratch
- **documentation-sync**: keep existing documentation updated when code
  changes

---

## Quick Commands

```bash
# Check project structure ($SRC = architecture.source_root)
ls -laR "$SRC"/ | head -50

# Find feature modules (architecture.modules)
ls -la "$SRC/modules"/

# Find reusable UI components (architecture.component_prefix)
find "$SRC/components" -maxdepth 2 -type d

# Check make targets (compare against the profile make map)
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile

# Verify bundler (framework.bundler)
grep -i rsbuild package.json

# Verify UI layer (must match framework.ui)
grep -iE '@mui/material|@emotion' package.json

# Verify Node runtime (framework.runtime)
cat .nvmrc

# Verify path aliases (architecture.path_aliases)
cat tsconfig.paths.json
```
