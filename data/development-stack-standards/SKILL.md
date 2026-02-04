---
name: development-stack-standards
description: Development stack standards - five-level maturity model, dimension specs, assessment criteria, tool guidance
---

# Development Stack Standards

Reference for creating and assessing language-specific development stacks. Defines maturity progression and assessment criteria.

**Used by:**
- `/stack-assess` - Grade projects against stack standards
- `/stack-guide` - Create/validate/customize stack definitions
- Stack skills (configuring-python-stack, configuring-javascript-stack, etc.)

## Five-Level Maturity Model

### Level 0: Foundation (EVERY project)

**8 dimensions required:**

| Dimension | Purpose | Justfile Recipe |
|-----------|---------|-----------------|
| Package manager | Reproducible builds (lockfile, isolation) | `dev-install` |
| Format | Consistent style (auto-fix) | `format` |
| Lint | Catch bugs (auto-fix safe changes) | `lint` |
| Typecheck | Static correctness | `typecheck` |
| Test | Verify behavior | `test` |
| Coverage | Measure testing | `coverage` |
| Build | Create artifacts | `build` |
| Clean | Reset state | `clean` |

**Additional recipes:** `check-all` (format -> lint -> typecheck -> coverage), `default`

**Assessment:** Fresh clone can `just dev-install && just check-all`

### Level 1: Quality Gates (CI/CD)

**Adds 4 dimensions:**

| Dimension | Requirement | Justfile Recipe |
|-----------|-------------|-----------------|
| Coverage threshold | 96% for unit tests | `coverage` (updated) |
| Complexity | <= 10 cyclomatic | `lint` checks, `complexity` reports |
| Test separation | Unit (fast) vs integration (slow) | `integration-test` |
| Test watch | Continuous on file changes | `test-watch` |

**Additional recipes:** `loc` (largest files)

**Assessment:** Coverage fails below 96%, complexity enforced, integration tests excluded from threshold

### Level 2: Security & Compliance (Production)

**Adds 4 dimensions:**

| Dimension | Purpose | Justfile Recipe |
|-----------|---------|-----------------|
| Vulnerability scanning | CVE detection | `vulns` |
| License analysis | Compliance (flag GPL/restrictive) | `lic` |
| SBOM | Supply chain (CycloneDX) | `sbom` |
| Dependency tracking | Show outdated packages | `deps` |

**Assessment:** All four commands succeed with meaningful output

### Level 3: Metrics (Large codebases)

Uses Level 1 tools (`complexity`, `loc`) for detailed analysis:
- File-by-file complexity breakdown
- Average and max metrics
- Identifies refactoring targets

### Level 4: Polyglot (Multi-language)

**Structure:** Root justfile orchestrates language-specific subprojects

**Root recipes (subset):** `dev-install`, `check-all`, `clean`, `build`, `deps`, `vulns`, `lic`, `sbom`

**Each subproject:** Implements Level 0+ independently, standalone `just check-all`

## Tool Selection by Language

### Python
- **Package:** uv (fast, handles venv + install + lock)
- **Format/Lint:** ruff (handles both)
- **Typecheck:** mypy (strict mode)
- **Test:** pytest with pytest-cov
- **Complexity:** radon (reports), ruff (threshold)
- **Security:** pip-audit, pip-licenses, cyclonedx-py

### JavaScript/TypeScript
- **Package:** pnpm (fast, efficient)
- **Format:** prettier
- **Lint:** eslint (with complexity rule)
- **Typecheck:** tsc (strict mode)
- **Test:** vitest (with coverage)
- **Security:** pnpm audit, license-checker, @cyclonedx/cyclonedx-npm

### Java
- **Package:** Maven (standard)
- **Format:** spotless + Google Java Format
- **Lint:** spotbugs, checkstyle
- **Typecheck:** javac (warnings as errors)
- **Test:** JUnit 5 with JaCoCo
- **Security:** dependency-check, license-maven-plugin, cyclonedx-maven-plugin

## Standard Settings

- **Line length:** 100 (balance readability vs horizontal space)
- **Coverage threshold:** 96% (unit tests only)
- **Complexity threshold:** <= 10 cyclomatic
- **Strict typing:** Always enabled

## Assessment Criteria

### Level 0
- [ ] All 8 dimensions present
- [ ] All 10 justfile recipes present
- [ ] `just dev-install && just check-all` succeeds

### Level 1
- [ ] Level 0 complete
- [ ] Coverage fails below 96% for unit tests
- [ ] Complexity <= 10 enforced in lint
- [ ] Integration tests marked/tagged and excluded from coverage

### Level 2
- [ ] Level 1 complete
- [ ] `vulns`, `lic`, `sbom`, `deps` all succeed

### Level 4
- [ ] Root orchestrates without duplication
- [ ] Each subproject standalone
- [ ] `_run-all` fails fast

## YAGNI Enforcement

**Stop at the level you need:**
- Library (no deployment): 0 -> 1 -> 2 (stop)
- Web app (CI/CD + deploy): 0 -> 1 -> 2 -> maybe 3
- Solo project: 0 -> 2 (skip quality overhead, add security)
- Monorepo: 0 -> 1 -> 4 -> 2 -> 3

**Don't add:**
- Level 1 if no CI/CD
- Level 2 if not deploying
- Level 3 if codebase small
- Level 4 if single language
