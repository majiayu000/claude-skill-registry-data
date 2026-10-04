---
name: documentation-creation
description: Create a comprehensive project documentation suite from scratch by analyzing the codebase and verifying every claim against it. Use when setting up INITIAL documentation for a project or building a complete docs/ suite where none exists. NOT for updating existing docs (use documentation-sync instead). Covers project analysis, documentation structure, templates, and verification.
---

# Documentation Creation Skill

## Profile keys consumed

- `project.name`
- `project.repo`
- `php.version`
- `framework.name`
- `framework.version`
- `framework.api_platform`
- `framework.graphql`
- `persistence.mapper`
- `persistence.engine`
- `architecture.source_root`
- `architecture.bounded_contexts`
- `architecture.shared_context`
- `make.ci`
- `make.start`
- `make.tests`
- `make.e2e`
- `make.load_tests`
- `quality.phpinsights.complexity`
- `quality.infection_msi`
- `capabilities.load_testing`

## Overview

This skill guides the creation of comprehensive project documentation
from scratch by analyzing the project codebase against the project
profile and applying consistent documentation patterns. It ensures
documentation accurately reflects the actual project implementation.

**Use this skill for**: initial documentation creation from scratch
**Use documentation-sync for**: updating existing documentation when
code changes

## Context (Input)

- Need to create documentation for a project from scratch
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

---

## Quick Start: Documentation Creation Workflow

### Step 1: Analyze Project Structure

The profile declares what the project claims to be; the codebase shows
what it is. Read the profile first, then verify each claim. In the
commands below, `$SRC` is `architecture.source_root` and `$CTX` iterates
`architecture.bounded_contexts` plus `architecture.shared_context`
(when not null).

```bash
# Check project structure
ls -la "$SRC"/

# Identify technology stack
cat composer.json | grep -A5 "require"
cat Dockerfile
cat docker-compose.yml

# Verify each declared bounded context exists
for CTX in <each architecture.bounded_contexts entry, plus architecture.shared_context>; do
  ls -la "$SRC/$CTX/" 2>/dev/null || echo "Profile drift: $SRC/$CTX missing"
done

# Check for entities
find "$SRC" -path "*/Entity/*.php"

# Check for commands and handlers (CQRS surface)
find "$SRC" -name "*Command.php" | head -20
find "$SRC" -name "*Handler.php" | head -20
```

**Key items to document**:

- [ ] Technology stack (`php.version`, `framework.name`/`framework.version`,
      `persistence.engine`, runtime)
- [ ] Architecture style (DDD, hexagonal, CQRS)
- [ ] Bounded contexts (`architecture.bounded_contexts`) and their purposes,
      plus the shared kernel (`architecture.shared_context`) when present
- [ ] Main entities and their relationships
- [ ] Available make targets (from the profile `make` map) and testing tools

### Step 2: Create Technology Stack Summary

Verify the profile's stack claims against the repository before
documenting them:

```bash
# PHP version — must match php.version
grep -i "php:" Dockerfile
grep '"php"' composer.json

# Framework — must match framework.name / framework.version
grep -i "<framework.name>" composer.json

# Database — must match persistence.engine
grep -iE "mysql|mariadb|postgres|mongo" docker-compose.yml

# Available make targets — the names the make.* map points at
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile | head -30
```

Create a technology summary table sourced from the verified profile
values:

| Component  | Technology             | Version               |
| ---------- | ---------------------- | --------------------- |
| Language   | PHP                    | `php.version`         |
| Runtime    | {from Dockerfile}      | -                     |
| Framework  | `framework.name`       | `framework.version`   |
| Database   | `persistence.engine`   | {from docker-compose} |
| Mapper     | `persistence.mapper`   | -                     |
| Web Server | {from docker-compose}  | -                     |

### Step 3: Create Documentation Files

Create each documentation file following this order:

1. **main.md** - Project overview and design principles
2. **getting-started.md** - Installation and quick start
3. **design-and-architecture.md** - Architectural decisions and patterns
4. **developer-guide.md** - Code structure and development workflow
5. **api-endpoints.md** - REST API documentation; include a GraphQL
   section only when `framework.graphql` is true, and API Platform
   specifics only when `framework.api_platform` is a version string
6. **testing.md** - Testing strategy and commands
7. **glossary.md** - Domain terminology and naming conventions
8. **user-guide.md** - API usage examples
9. **advanced-configuration.md** - Environment and configuration
10. **performance.md** - Benchmarks and optimization; cover load testing
    only when `capabilities.load_testing` is true, documenting the
    Makefile target mapped by `make.load_tests`
11. **security.md** - Security measures and practices
12. **operational.md** - Operational considerations
13. **onboarding.md** - New contributor guide
14. **community-and-support.md** - Support channels
15. **legal-and-licensing.md** - License and dependencies
16. **release-notes.md** - Release process
17. **versioning.md** - Versioning policy

> Add project-specific docs as needed (e.g. a runtime-specific
> performance page when the project uses a non-standard PHP runtime)

### Step 4: Write Each Documentation File

For each documentation file:

1. **Use the appropriate template** (see Documentation Templates below)

2. **Fill in project-specific content**:

   - Project name: use `project.name` consistently throughout
   - Repository links: build from `project.repo`
     (`https://github.com/<project.repo>`)
   - Entity names from the codebase
   - Bounded context names from `architecture.bounded_contexts`

3. **Verify all references**:

   - Directory paths exist under `architecture.source_root`
   - Every documented make invocation uses the actual target name the
     profile `make` map points at (e.g. the target mapped by `make.ci`)
     and that target exists in the Makefile. A `null` mapping means the
     capability is absent: do not document it; note the gap instead
   - Entity names match the codebase

4. **Add cross-links** to related documentation

5. **Quality thresholds**: where testing.md or performance.md cite
   quality bars, take values only from the profile `quality.*` keys —
   canonical defaults are complexity 94 (`quality.phpinsights.complexity`)
   and MSI 100 (`quality.infection_msi`). Thresholds are raise-only:
   never document a bar lower than the shipped default

### Step 5: Verify Accuracy

Run comprehensive verification (full checklist below):

1. **Technology Stack Verification**:

   ```bash
   grep -i "php" Dockerfile                          # php.version
   grep -i "<framework.name>" composer.json          # framework.name
   grep -iE "mysql|mariadb|postgres|mongo" docker-compose.yml  # persistence.engine
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
   `make.tests`, `make.e2e`):

   ```bash
   for cmd in <each documented target name from the profile make map>; do
     grep -q "^$cmd:" Makefile && echo "Found: $cmd" || echo "Missing: $cmd"
   done
   ```

4. **Link Verification**:
   - Check all internal markdown links resolve
   - Verify external links (including `project.repo` links) are accurate

Worked example against the upstream reference service:

```bash # profile-example
# architecture.bounded_contexts: [User, OAuth]; shared_context: Shared
ls -la src/User/ src/OAuth/ src/Shared/
# persistence.engine: mongodb
grep -i mongo docker-compose.yml
# make map: ci → ci, tests → tests, e2e → e2e-tests
for cmd in ci tests e2e-tests; do grep -q "^$cmd:" Makefile && echo "Found: $cmd"; done
```

---

## Documentation Templates

### Overview Document (main.md)

```markdown
# {project.name}

Welcome to the **{project.name}** documentation...

## Design Principles

{List project's core design principles}

## Technology Stack

| Component | Technology           | Version             |
| --------- | -------------------- | ------------------- |
| Language  | PHP                  | {php.version}       |
| Framework | {framework.name}     | {framework.version} |
| Database  | {persistence.engine} | X.Y                 |
```

### Getting Started (getting-started.md)

```markdown
# Getting Started

## Prerequisites

{List required software with versions}

## Installation

{Step-by-step installation commands; boot the service via the target
mapped by make.start}

## Verification

{Commands to verify installation}
```

Derive the remaining files from the structure in Format (Output) below,
keeping headings and tone consistent with these two templates.

---

## Constraints

### NEVER

- Include references to non-existent directories or files
- Claim features or technologies the project doesn't use (e.g. a GraphQL
  page when `framework.graphql` is false)
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
- Add a Table of Contents to longer documents (100+ lines)

---

## Verification Checklist

After creating documentation:

### Technology Accuracy

- [ ] PHP version matches Dockerfile and `php.version`
- [ ] Framework version matches composer.json and `framework.version`
- [ ] Database type matches docker-compose.yml and `persistence.engine`
- [ ] Mapper (ORM vs ODM) described per `persistence.mapper`
- [ ] Runtime environment correctly described
- [ ] No false claims about unused technologies

### Structure Accuracy

- [ ] All mentioned source directories exist under
      `architecture.source_root`
- [ ] All bounded context names match `architecture.bounded_contexts`
      (and `architecture.shared_context`)
- [ ] Entity names match the actual codebase
- [ ] Command and handler names are accurate

### Command Accuracy

- [ ] All documented make targets exist in the Makefile and come from
      the profile `make` map; `null` capabilities are noted, not documented
- [ ] Docker commands work as documented
- [ ] Test commands (targets mapped by `make.tests`, `make.e2e`) produce
      the documented output

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
grep -i "fpm\|franken" Dockerfile
cat docker-compose.yml
# Only document what actually exists — and reconcile with the profile
```

### Missing Directories

**Problem**: Documenting directories that don't exist under the source
root

**Solution**:

```bash
# Verify before documenting
ls -la "$SRC"/
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
├── api-endpoints.md           # REST (and GraphQL, when enabled) docs
├── testing.md                 # Testing strategy
├── glossary.md                # Domain terminology
├── user-guide.md              # API usage examples
├── advanced-configuration.md  # Environment config
├── performance.md             # Benchmarks
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

---

## Related Skills

- [documentation-sync](../documentation-sync/SKILL.md) - Keep docs in
  sync with code changes (use AFTER initial creation)
- [api-platform-crud](../api-platform-crud/SKILL.md) - API documentation
  patterns
- [testing-workflow](../testing-workflow/SKILL.md) - Testing
  documentation
- [load-testing](../load-testing/SKILL.md) - Performance documentation
  (when `capabilities.load_testing` is true)

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

# Find entities
find "$SRC" -path "*/Entity/*.php"

# Find commands
find "$SRC" -name "*Command.php"

# Check make targets (compare against the profile make map)
grep -E "^[a-zA-Z][a-zA-Z0-9_-]*:" Makefile

# Verify runtime
grep -i "fpm\|franken" Dockerfile

# Check database (must match persistence.engine)
grep -iE "mysql|mariadb|postgres|mongo" docker-compose.yml

# Verify technology stack (php.version, framework.name)
grep -i "php:" Dockerfile
grep -i "<framework.name>" composer.json
```
